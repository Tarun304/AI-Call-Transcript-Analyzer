import logging
from src.backend.orchestrator import CallTranscriptAnalyzer
from src.api.models import TranscriptRequest, TranscriptResponse, HealthResponse
from fastapi import APIRouter, HTTPException
from langsmith import traceable
from src.utils.logger import logger

# Create the router instance
router = APIRouter()

# Define the health check endpoint
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    logger.info("Health check requested")
    return HealthResponse(
        status="Healthy",
        message="Call Transcript Analyzer API is running"
    )

# Define the main transcript analysis endpoint
@router.post("/analyze-transcript", response_model=TranscriptResponse)
@traceable(name="api_analyze_transcript", tags=["api", "analysis"])
async def analyze_transcript(request: TranscriptRequest):
    """Main endpoint for transcript analysis and CSV saving."""
    try:
        logger.info("Transcript analysis requested")
        
        # Basic input validation
        if not request.transcript.strip():
            raise HTTPException(status_code=400, detail="Transcript cannot be empty")
        
        if len(request.transcript.strip()) < 10:
            raise HTTPException(status_code=400, detail="Transcript too short for meaningful analysis")
        
        # Create analyzer and process transcript
        analyzer = CallTranscriptAnalyzer()
        result = analyzer.analyze_transcript(request.transcript)
        
        # Check if analysis was successful
        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail="Analysis failed")
        
        logger.info("Transcript analysis and CSV save completed successfully")
        
        # Return the response
        return TranscriptResponse(
            transcript=result["transcript"],
            summary=result["summary"],
            sentiment=result["sentiment"],
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_transcript: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
