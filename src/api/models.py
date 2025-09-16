from pydantic import BaseModel, Field

# Define the Request Schema
class TranscriptRequest(BaseModel):
    """Request model for transcript analysis."""
    transcript: str = Field(..., description="Customer call transcript to be analyzed")

# Define the Response Schema
class TranscriptResponse(BaseModel):
    """Response model for transcript analysis."""
    transcript: str = Field(..., description="The original transcript")
    summary: str = Field(..., description="AI-generated summary of the call")
    sentiment: str = Field(..., description="Detected customer sentiment")
    success: bool = Field(..., description="Whether the analysis was successful")

# Health check Schema
class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="API Status")
    message: str = Field(..., description="Health check message")
