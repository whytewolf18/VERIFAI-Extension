from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from utils.security_config import (
    ALLOWED_ORIGINS,
    REMOVED_HEADERS,
    CORS_SETTINGS,
    SECURITY_HEADERS
)
from services.llm_service import get_gpt_fact_check, analyze_politician_claim, get_gpt_chat_response
from services.news_retrieval import (
    fetch_articles,
    detect_politicians,
    POLITICIANS,
    POLITICIAN_INFO
)
from services.ui_highlighter import highlight_claims

# --- Models ---
class ClaimRequest(BaseModel):
    text: str
    language: str = "en"

class HighlightRequest(BaseModel):
    text: str
    language: str = "en"

class AnalyzeRequest(BaseModel):
    text: str
    context: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    message: str
    context: Dict[str, Any]

class PoliticianResponse(BaseModel):
    politicians: Dict[str, Any]

class VerifyRequest(BaseModel):
    text: str
    type: str = "facebook_post"
    source: str = "facebook"
    politicians: List[str] = []

class VerifyResponse(BaseModel):
    is_claim: bool
    fact_check: Dict[str, Any]

# --- Middleware ---
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # Remove headers safely
        for header in REMOVED_HEADERS:
            if header in response.headers:
                del response.headers[header]
        # Add security headers
        response.headers.update(SECURITY_HEADERS)
        return response

# --- App Configuration ---
app = FastAPI(
    title="Filipino Fact Check API",
    description="API for detecting and fact-checking claims in English and Filipino text",
    version="1.0.0"
)

# Configure CORS middleware with specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Then add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# --- Helper Functions ---
def get_classification_color(classification: str) -> str:
    colors = {
        "False": "#ff6b6b",
        "Misleading": "#ffd93d",
        "Needs Context": "#4dabf7",
        "Verified": "#51cf66",
        "Error": "#868e96"
    }
    return colors.get(classification, "#868e96")

def get_classification_style(classification: str) -> str:
    styles = {
        "False": "wavy",
        "Misleading": "wavy",
        "Needs Context": "dotted",
        "Verified": "solid",
        "Error": "dashed"
    }
    return styles.get(classification, "dashed")

def get_canonical_name(politician: str) -> str:
    aliases = {
        "BBM": "Ferdinand Marcos Jr.",
        "Bongbong Marcos": "Ferdinand Marcos Jr.",
        "Noynoy Aquino": "Benigno Aquino III",
        "GMA": "Gloria Macapagal Arroyo",
        "Chiz Escudero": "Francis Escudero",
        "Ping Lacson": "Panfilo Lacson",
        "Dick Gordon": "Richard Gordon"
    }
    return aliases.get(politician, politician)

# Update verify endpoint to handle errors properly
@app.post("/verify")
async def verify_content(request: VerifyRequest):
    try:
        result = await get_gpt_fact_check(request.text)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )

@app.post("/fact-check")
async def fact_check(request: VerifyRequest):
    """Endpoint for fact-checking content"""
    try:
        result = await get_gpt_fact_check(request.text)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        return {
            "status": "success",
            "classification": result["classification"],
            "analysis": result["analysis"],
            "style": get_classification_style(result["classification"]),
            "color": get_classification_color(result["classification"])
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )

@app.post("/analyze")
async def analyze_text(text: str):
    try:
        # Process directly through LLM
        result = await app.state.gpt_model.analyze_text(text)
        
        return {"result": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/highlight")
async def highlight_text(request: HighlightRequest):
    """Process text and return highlighted claims with annotations."""
    text = request.text.strip()
    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty" if request.language == "en" else "Hindi maaaring walang laman ang teksto"
        )
    return highlight_claims(text)

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await get_gpt_chat_response(
            message=request.message,
            context=request.context
        )
        return {
            "status": "success",
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/politicians", response_model=PoliticianResponse)
async def get_politicians():
    return {"politicians": POLITICIAN_INFO}

@app.get("/health")
async def health_check():
    """Health check endpoint with CORS verification."""
    return {
        "status": "healthy",
        "message": "System is operational using GPT model",
        "cors_enabled": True,
        "security_headers": {
            "permissions_policy_removed": True,
            "cors_origins": ALLOWED_ORIGINS,
            "headers_removed": REMOVED_HEADERS
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)