import streamlit as st
import requests
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Call Transcript Analyzer",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "transcript_input" not in st.session_state:
    st.session_state.transcript_input = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# Simple CSS for clean alignment and spacing (removed sentiment color classes)
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        text-align: center;
        font-size: 1rem;
        color: #666;
        font-style: italic;
        margin-bottom: 1.5rem;
    }
    .metric-small {
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
        color: #1f77b4;
    }
    .metric-label {
        text-align: center;
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000/api"

def make_api_call(endpoint, data=None):
    """Make API calls to FastAPI backend."""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if data:
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def get_csv_download_data():
    """Get CSV data for download."""
    csv_file = "call_analysis.csv"
    if os.path.exists(csv_file):
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            return None
    return None

def display_csv_data():
    """Display CSV data if available."""
    csv_file = "call_analysis.csv"
    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
            if not df.empty:
                st.markdown("#### Recent Analysis Results")
                
                # Show stats with smaller layout
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'<p class="metric-small">{len(df)}</p>', unsafe_allow_html=True)
                    st.markdown('<p class="metric-label">Total Analyses</p>', unsafe_allow_html=True)
                with col2:
                    sentiment_counts = df['Sentiment'].value_counts()
                    most_common = sentiment_counts.index[0] if not sentiment_counts.empty else "N/A"
                    st.markdown(f'<p class="metric-small">{most_common}</p>', unsafe_allow_html=True)
                    st.markdown('<p class="metric-label">Most Common</p>', unsafe_allow_html=True)
                with col3:
                    unique_sentiments = df['Sentiment'].nunique()
                    st.markdown(f'<p class="metric-small">{unique_sentiments}</p>', unsafe_allow_html=True)
                    st.markdown('<p class="metric-label">Unique Sentiments</p>', unsafe_allow_html=True)
                
                # CSV Download Button
                csv_data = get_csv_download_data()
                if csv_data:
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name="call_analysis.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                # Show recent entries
                st.markdown("#### Analysis History")
                recent_df = df.tail(3).iloc[::-1]  # Show latest 3
                
                for idx, row in recent_df.iterrows():
                    with st.expander(f"#{idx + 1} - {row['Sentiment']}", expanded=False):
                        st.markdown("**Transcript:**")
                        st.write(row['Transcript'])
                        st.markdown("**Summary:**")
                        st.write(row['Summary'])
                        st.markdown(f"**Sentiment:** {row['Sentiment']}")
                
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
    else:
        st.info("No analysis data yet. Analyze your first transcript!")

def clear_input():
    """Clear input and results."""
    st.session_state.transcript_input = ""
    st.session_state.analysis_result = None
    st.session_state.show_results = False

def main():
    """Main application interface."""
    
    # Centered header
    st.markdown('<h1 class="main-title">📞 Call Transcript Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">AI-powered customer call analysis using Groq and LangGraph</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("📊 Application Info")
        
        # Health check
        if st.button("🔍 Check API Status"):
            health_response = make_api_call("/health")
            if health_response:
                st.success(f"✅ {health_response.get('message', 'API is healthy')}")
            else:
                st.error("❌ API is not responding")
        
        st.markdown("---")
        st.markdown("**Features:**")
        st.markdown("• 🤖 AI-powered summarization")
        st.markdown("• 😊 Emotion detection")
        st.markdown("• 💾 CSV export")
        st.markdown("• ⚡ Real-time processing")
        
        st.markdown("---")
        st.markdown("**Tech Stack:**")
        st.markdown("• 🦜 LangChain + Groq")
        st.markdown("• 🕸️ LangGraph Orchestration") 
        st.markdown("• 🚀 FastAPI Backend")
        st.markdown("• 🎨 Streamlit Frontend")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Analyze New Transcript")
        
        # Sample transcripts
        sample_transcripts = {
            "Billing Confusion": "Hello, I'm calling about my monthly bill. I usually pay around $45 but this month it's $78 and I don't understand why. I didn't use any extra services or change my plan. Can you help me figure out what these additional charges are for? I'm not angry, just really confused about what happened.",
            "Tech Support Anxiety": "Hi, my laptop has been running extremely slow for the past week and now it's not starting up properly. I have an important presentation tomorrow and all my files are on this computer. I'm really worried I might lose everything. Can you please help me fix this quickly?",
            "Product Return": "I ordered a wireless headset last week expecting premium quality based on your website description, but the sound quality is terrible and it keeps disconnecting from my phone. This is really disappointing because I specifically chose your brand based on the reviews. I'd like to return this and get a full refund please.",
            "Account Access": "Good morning, I'm trying to log into my online account but I can't remember my password. I've tried the password reset option but I'm not receiving the email. Could you help me reset my password or check if there's an issue with my email address on file?",
            "Delivery Delay": "This is ridiculous! I paid extra for express shipping and my package was supposed to arrive three days ago. I need these items for my daughter's birthday party this weekend. Every time I track the package it just says 'in transit' with no real updates. Where is my order and when will it actually arrive?"
        }
        
        # Quick select samples
        st.write("**Quick Start - Sample Transcripts:**")
        selected_sample = st.selectbox(
            "Choose a sample transcript:", 
            ["New Transcript"] + list(sample_transcripts.keys()),
            index=0
        )
        
        # Update input if sample selected
        if selected_sample and selected_sample != "New Transcript":
            st.session_state.transcript_input = sample_transcripts.get(selected_sample, "")
        
        # Transcript input using session state
        transcript_input = st.text_area(
            "Enter Customer Call Transcript:",
            value=st.session_state.transcript_input,
            height=150,
            placeholder="Paste your customer call transcript here...",
            help="Enter the complete customer service call transcript for analysis"
        )
        
        # Update session state
        st.session_state.transcript_input = transcript_input
        
        # Buttons row
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            analyze_button = st.button("🚀 Analyze Transcript", type="primary", use_container_width=True)
        with btn_col2:
            clear_button = st.button("🗑️ Clear Input", on_click=clear_input, use_container_width=True)
        
        # Process analysis
        if analyze_button:
            if not st.session_state.transcript_input.strip():
                st.error("❌ Please enter a transcript to analyze")
            elif len(st.session_state.transcript_input.strip()) < 10:
                st.error("❌ Transcript is too short for meaningful analysis")
            else:
                with st.spinner("🤖 Analyzing transcript with AI..."):
                    # Make API call
                    result = make_api_call("/analyze-transcript", {"transcript": st.session_state.transcript_input})
                    
                    if result and result.get("success"):
                        st.session_state.analysis_result = result
                        st.session_state.show_results = True
                        
                        # Clear input after successful analysis
                        st.session_state.transcript_input = ""
                    else:
                        st.error("❌ Analysis failed. Please check the API connection.")
        
        # Display results if available
        if st.session_state.show_results and st.session_state.analysis_result:
            st.success("✅ Analysis completed successfully!")
            
            # Display results
            st.subheader("📋 Analysis Results")
            
            # Vertical layout - Summary first, then Sentiment below
            st.write("**📝 Summary:**")
            st.info(st.session_state.analysis_result["summary"])
            
            st.write("**😊 Detected Sentiment:**")
            st.info(st.session_state.analysis_result["sentiment"])
            
            # Original transcript
            with st.expander("📄 Original Transcript"):
                st.write(st.session_state.analysis_result["transcript"])
            
            st.success("💾 Results automatically saved to call_analysis.csv")
    
    with col2:
        st.header("📊 Data Overview")
        display_csv_data()

if __name__ == "__main__":
    main()
