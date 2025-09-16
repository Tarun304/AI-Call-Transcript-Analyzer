# 📞 AI Call Transcript Analyzer

An intelligent customer service call analysis application that leverages AI to automatically summarize transcripts and detect customer sentiment. Built with modern Python frameworks and powered by Groq's LLM and LangGraph orchestration.

## 🚀 Features

- **🤖 AI-Powered Analysis**: Uses Groq's Llama-3.3-70B model for intelligent transcript processing
- **📝 Automatic Summarization**: Generates concise 2-3 sentence summaries focusing on key issues and resolutions
- **😊 Sentiment Detection**: Identifies customer emotional states (frustrated, satisfied, confused, angry, etc.)
- **🕸️ Workflow Orchestration**: LangGraph-powered pipeline for reliable processing
- **💾 Data Persistence**: Automatically saves results to CSV for tracking and analysis
- **🎨 Modern UI**: Clean Streamlit interface with real-time processing
- **⚡ Fast API**: RESTful FastAPI backend with automatic documentation
- **📊 Analytics Dashboard**: View analysis history and sentiment trends

## 🏗️ Architecture

The application follows a modern microservices architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   LangGraph     │
│   Frontend      │◄──►│   Backend       │◄──►│   Orchestrator  │
│   (Default Port)│    │   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Groq LLM      │
                                               │   (Llama-3.3)   │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Data Manager  │
                                               │   (CSV Storage) │
                                               └─────────────────┘
```

### Application Flow

1. **Main Launcher** (`app.py`): Starts both FastAPI backend and Streamlit frontend
2. **Streamlit Frontend**: User interface that sends HTTP requests to FastAPI
3. **FastAPI Backend**: Receives requests and creates LangGraph orchestrator instance
4. **LangGraph Orchestrator**: Executes workflow (Summary → Sentiment → Save)
5. **Groq LLM**: Provides AI analysis for both summary and sentiment tasks
6. **Data Manager**: Called by orchestrator to save results to CSV file

## 📁 Project Structure

```
AI Call Transcript Analyzer/
├── app.py                          # Main application launcher
├── requirements.txt                # Python dependencies
├── call_analysis.csv              # Generated analysis results
├── README.md                      # This file
└── src/
    ├── api/                       # FastAPI backend
    │   ├── fastapi_app.py         # FastAPI application setup
    │   ├── models.py              # Pydantic data models
    │   └── routes.py              # API endpoints
    ├── backend/                   # Core business logic
    │   ├── orchestrator.py        # LangGraph workflow orchestration
    │   └── data_manager.py        # CSV data persistence
    ├── frontend/                  # Streamlit UI
    │   └── streamlit_app.py       # Main user interface
    └── utils/                     # Utility modules
        └── logger.py              # Logging configuration
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Main programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **Streamlit**: Rapid web app development for data science
- **Uvicorn**: ASGI server for FastAPI

### AI & ML Stack
- **Groq**: High-performance LLM inference platform
- **LangChain**: Framework for developing LLM applications
- **LangGraph**: Workflow orchestration for complex AI pipelines
- **Llama-3.3-70B-Versatile**: Advanced language model for analysis

### Data & Utilities
- **Pandas**: Data manipulation and analysis
- **Pydantic**: Data validation and settings management
- **Loguru**: Advanced logging framework
- **Python-dotenv**: Environment variable management

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Groq API Key** - Sign up at [console.groq.com](https://console.groq.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "AI Call Transcript Analyzer"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   LANGSMITH_API_KEY=your_api_key_here
   LANGSMITH_TRACING="true"
   LANGSMITH_ENDPOINT= "https://api.smith.langchain.com"
   LANGSMITH_PROJECT= "AI Call Transcript Analyzer"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The application will:
- Start the FastAPI backend on `http://localhost:8000`
- Launch the Streamlit frontend (default port, typically 8501)
- Automatically open your browser to the Streamlit interface

## 📖 Usage Guide

### Web Interface

1. **Access the Application**: Navigate to the Streamlit URL shown in your terminal (typically `http://localhost:8501`)
2. **Enter Transcript**: Paste your customer call transcript in the text area
3. **Quick Start**: Use the sample transcripts for testing
4. **Analyze**: Click "🚀 Analyze Transcript" to process
5. **View Results**: See summary, sentiment, and analysis history
6. **Export Data**: Download CSV file with all analysis results

### API Usage

The FastAPI backend provides RESTful endpoints:

#### Health Check
```bash
GET http://localhost:8000/api/health
```

#### Analyze Transcript
```bash
POST http://localhost:8000/api/analyze-transcript
Content-Type: application/json

{
  "transcript": "Your customer call transcript here..."
}
```

#### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

### Sample Transcripts

The application includes several sample transcripts for testing:

- **Billing Confusion**: Customer confused about unexpected charges
- **Tech Support Anxiety**: Customer worried about laptop issues
- **Product Return**: Customer requesting refund for defective product
- **Account Access**: Customer having login difficulties
- **Delivery Delay**: Customer frustrated with shipping delays

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for LLM access | Yes |

### Model Configuration

The application uses the following default settings:
- **Model**: `llama-3.3-70b-versatile`
- **Temperature**: `0.3` (balanced creativity/consistency)
- **Backend Port**: `8000` (FastAPI)
- **Frontend Port**: Streamlit default (typically 8501)

## 📊 Data Output

### CSV Format

Analysis results are saved to `call_analysis.csv` with the following columns:

| Column | Description |
|--------|-------------|
| `Transcript` | Original customer call transcript |
| `Summary` | AI-generated 2-3 sentence summary |
| `Sentiment` | Detected customer emotional state |

### Sentiment Categories

The system detects various customer emotions:
- **Negative**: Frustrated, Angry, Irritated
- **Positive**: Satisfied, Grateful, Happy
- **Neutral**: Confused, Uncertain, Neutral
- **Concerned**: Anxious, Concerned, Worried

## 🔍 Workflow Process

The LangGraph orchestration follows this workflow:

1. **Input Validation**: Verify transcript quality and length
2. **Summarization**: Generate concise business-focused summary
3. **Sentiment Analysis**: Detect customer emotional state
4. **Data Persistence**: Save results to CSV file
5. **Response**: Return structured results to frontend

## 🛡️ Error Handling

The application includes comprehensive error handling:

- **Input Validation**: Checks for empty or too-short transcripts
- **API Error Handling**: Graceful handling of LLM API failures
- **File System Errors**: Safe CSV writing with error recovery
- **Network Issues**: Timeout handling for API calls

## 📈 Performance Features

- **Structured Output**: Uses Pydantic models for reliable data parsing
- **LangSmith Tracing**: Built-in observability for workflow monitoring
- **Efficient Logging**: Structured logging with Loguru
- **Background Processing**: Non-blocking API calls
- **Session Management**: Streamlit session state for better UX

## 🔧 Development

### Running in Development Mode

The application supports hot-reload for development:

```bash
# Backend with auto-reload
uvicorn src.api.fastapi_app:app --reload --host 0.0.0.0 --port 8000

# Frontend with auto-reload
streamlit run src/frontend/streamlit_app.py --server.runOnSave true
```

### Code Structure

- **Modular Design**: Clear separation between frontend, backend, and business logic
- **Type Hints**: Full type annotation for better code maintainability
- **Error Handling**: Comprehensive exception handling throughout
- **Logging**: Structured logging for debugging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the [API Documentation](http://localhost:8000/docs) when running
2. Review the sample transcripts for expected input format
3. Ensure your Groq API key is valid and has sufficient credits
4. Check the application logs for detailed error information

## 🔮 Future Enhancements

Potential improvements for future versions:

- **Multi-language Support**: Analysis in different languages
- **Advanced Analytics**: Trend analysis and reporting dashboards
- **Integration APIs**: Connect with CRM systems
- **Batch Processing**: Analyze multiple transcripts simultaneously
- **Custom Models**: Fine-tuned models for specific industries
- **Real-time Processing**: WebSocket support for live call analysis

---

**Built with ❤️ using Python, FastAPI, Streamlit, and Groq AI**
