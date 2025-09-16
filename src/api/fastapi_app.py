from src.api.routes import router
from fastapi import FastAPI

# Create the FastAPI app instance
app = FastAPI(
    title="Call Transcript Analyzer API",
    description="AI-powered customer call transcript analysis using Groq and LangGraph",
    version="1.0.0",
    docs_url="/docs"
)

# Include the router
app.include_router(router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Call Transcript Analyzer API",
        "docs": "/docs",
        "health": "/api/health"
    }
