from fastapi import FastAPI, HTTPException
import os
from .models import TroubleshootingCase, DiagnosisResponse
from .ai_diagnosis import diagnose_case
from .config import GEMINI_API_KEY

app = FastAPI(
    title="NetSage AI - Diagnosis Engine",
    description="Backend API for NetSage AI network troubleshooting diagnosis.",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    api_key_configured = bool(GEMINI_API_KEY)
    return {
        "status": "healthy",
        "api_key_configured": api_key_configured,
        "message": "NetSage AI backend is running."
    }

@app.post("/diagnose", response_model=DiagnosisResponse)
def diagnose(case: TroubleshootingCase):
    """
    Accepts a troubleshooting case and returns an AI diagnosis.
    
    RESPONSIBLE AI REQUIREMENT:
    AI suggestions are advisory and require human review before any fix is accepted or applied.
    Do not apply automatic changes to network infrastructure.
    """
    try:
        diagnosis = diagnose_case(case)
        return diagnosis
    except ValueError as e:
        # Catch our custom value errors (API key missing, malformed JSON, etc)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Catch unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
