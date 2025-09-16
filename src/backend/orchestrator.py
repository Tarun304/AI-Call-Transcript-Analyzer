from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langsmith import traceable
import os
from dotenv import load_dotenv
from src.utils.logger import logger

# Load environment variables from .env file
load_dotenv()  


# Define the workflow state
class WorkflowState(TypedDict):
    transcript: str      # Input transcript
    summary: str         # Generated summary
    sentiment: str       # Analyzed sentiment

# Define Pydantic models for structured output
class TranscriptSummary(BaseModel):
    """Structured output for transcript summary."""
    summary: str = Field(..., description="Concise 2-3 sentence summary of the customer call focusing on main issue and resolution.")

class SentimentAnalysis(BaseModel):
    """Structured output for sentiment analysis."""
    sentiment: str = Field(..., description="Customer's emotional state and sentiment expressed during the call (e.g., frustrated, satisfied, confused, angry, grateful, etc.)")

# Main Orchestrator class
class CallTranscriptAnalyzer:
    def __init__(self):
        """Initialize the analyzer with Groq LLM and structured outputs."""
        
        # Initialize base LLM
        self.base_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Initialize structured LLMs
        self.summary_llm = self.base_llm.with_structured_output(TranscriptSummary)
        self.sentiment_llm = self.base_llm.with_structured_output(SentimentAnalysis)
        
        logger.info("CallTranscriptAnalyzer initialized successfully")

    @traceable(name="node_summarize_transcript", tags=["workflow:summary"])
    def summary_node(self, state: WorkflowState) -> Dict[str, Any]:
        """Generate summary from transcript using structured output."""
        try:
            transcript = state["transcript"]
            
            # Define the prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert at summarizing customer service calls.
                            Create a concise 2-3 sentence summary that captures:
                            - The main customer issue or request
                            - Any actions taken or solutions provided
                            - The overall outcome or next steps
                            Focus on the key business-relevant information."""),
                ("human", "Transcript to summarize:\n\n{transcript}")
            ])
            
            # Create chain and invoke
            chain = prompt | self.summary_llm
            result = chain.invoke({"transcript": transcript})
            
            logger.info(f"Summary generated successfully")
            
            return {"summary": result.summary}
            
        except Exception as e:
            logger.error(f"Error in summary_node: {e}")
            return {"summary": "Error generating summary"}

    
    @traceable(name="node_analyze_sentiment", tags=["workflow:sentiment"])
    def sentiment_node(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze sentiment from transcript using structured output."""
        try:
            transcript = state["transcript"]
            
            # Define the prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert at analyzing customer emotions and sentiment from service calls.
                            Identify the customer's primary emotional state and sentiment throughout the conversation.
                            Be specific and descriptive - use terms like:
                            - Frustrated, Angry, Irritated (for negative emotions)
                            - Satisfied, Grateful, Happy (for positive emotions)  
                            - Confused, Uncertain, Neutral (for neutral states)
                            - Anxious, Concerned, Worried (for concern-based emotions)
                            
                            Provide the most accurate emotional descriptor that captures the customer's overall tone."""),
                ("human", "Transcript to analyze:\n\n{transcript}")
            ])
            
            # Create chain and invoke
            chain = prompt | self.sentiment_llm
            result = chain.invoke({"transcript": transcript})
            
            logger.info(f"Sentiment analyzed: {result.sentiment}")
            
            return {"sentiment": result.sentiment}
            
        except Exception as e:
            logger.error(f"Error in sentiment_node: {e}")
            return {"sentiment": "Neutral"}

    
    @traceable(name="node_save_results", tags=["workflow:save"])
    def save_node(self, state: WorkflowState) -> Dict[str, Any]:
        """Save results to CSV using data_manager."""
        try:
            # Import here to avoid circular imports
            from .data_manager import DataManager
            
            # Create data manager and save results
            data_manager = DataManager()
            success = data_manager.save_to_csv({
                "transcript": state["transcript"],
                "summary": state["summary"],
                "sentiment": state["sentiment"]
            })
            
            if success:
                logger.info("Results saved to CSV successfully")
            else:
                logger.error("Failed to save results to CSV")
                
            return {}
                
        except Exception as e:
            logger.error(f"Error in save_node: {e}")
            return {}

    
    @traceable(name="call_transcript_workflow", tags=["main", "workflow"])
    def analyze_transcript(self, transcript: str) -> Dict[str, Any]:
        """
        Main workflow execution: Input → Summary → Sentiment → Save → Output
        """
        try:
            # Create the workflow graph
            graph = StateGraph(WorkflowState)
            
            # Add nodes
            graph.add_node("summarize", self.summary_node)
            graph.add_node("analyze_sentiment", self.sentiment_node)
            graph.add_node("save_results", self.save_node)
            
            # Add edges (linear workflow)
            graph.add_edge(START, "summarize")
            graph.add_edge("summarize", "analyze_sentiment")
            graph.add_edge("analyze_sentiment", "save_results")
            graph.add_edge("save_results", END)
            
            # Compile the workflow
            workflow = graph.compile()
            
            # Initial state
            initial_state: WorkflowState = {
                "transcript": transcript,
                "summary": "",
                "sentiment": ""
            }
            
            logger.info("Starting transcript analysis workflow")
            
            # Execute workflow
            final_state = workflow.invoke(initial_state)
            
            logger.info("Workflow completed successfully")
            
            # Return results
            return {
                "transcript": final_state["transcript"],
                "summary": final_state["summary"],
                "sentiment": final_state["sentiment"]
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {
                "transcript": transcript,
                "summary": "Error processing transcript",
                "sentiment": "Neutral"
            }

