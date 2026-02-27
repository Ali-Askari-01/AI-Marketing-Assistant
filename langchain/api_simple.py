"""
Simple Gemini AI Agent API - Direct Gemini integration without LangChain
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import  google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("⚠️  WARNING: GOOGLE_API_KEY not found in .env file")
else:
    print("✅ Gemini API key loaded")
    genai.configure(api_key=GOOGLE_API_KEY)

# Initialize FastAPI app
app = FastAPI(
    title="Gemini AI Agent API",
    description="Simple AI Agent powered by Google Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini model
try:
    model = genai.GenerativeModel('gemini-pro')
    print("✅ Gemini model initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Gemini model: {e}")
    model = None

# Request/Response models
class QuestionRequest(BaseModel):
    question: str
    context: Optional[str] = None

class MarketingInsightRequest(BaseModel):
    question: str
    context: Optional[str] = None

class CampaignAdviceRequest(BaseModel):
    campaign_type: str
    target_audience: Optional[str] = None
    budget: Optional[str] = None
    goals: Optional[str] = None
    context: Optional[str] = None

class ResponseModel(BaseModel):
    answer: str
    success: bool = True

# Helper function to ask Gemini
async def ask_gemini(prompt: str) -> str:
    """Ask Gemini AI a question"""
    if not model:
        return "Error: Gemini model not initialized. Please check your API key."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return f"Error generating response: {str(e)}"

# Routes
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Gemini AI Agent API",
        "version": "1.0.0",
        "status": "running",
        "model": "gemini-pro",
        "endpoints": {
            "/health": "Health check",
            "/ask": "Ask any question",
            "/marketing-insights": "Get marketing insights",
            "/campaign-advice": "Get campaign strategy advice"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_status = "ready" if model else "error"
    return {
        "status": "healthy",
        "model": model_status,
        "api_key_configured": bool(GOOGLE_API_KEY)
    }

@app.post("/ask", response_model=ResponseModel)
async def ask_question(request: QuestionRequest):
    """
    Ask the AI agent any question
    """
    try:
        # Build prompt with context
        prompt = request.question
        if request.context:
            prompt = f"Context: {request.context}\n\nQuestion: {request.question}"
        
        answer = await ask_gemini(prompt)
        
        return ResponseModel(
            answer=answer,
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/marketing-insights", response_model=ResponseModel)
async def get_marketing_insights(request: MarketingInsightRequest):
    """
    Get marketing insights and trends
    """
    try:
        # Build marketing-focused prompt
        prompt = f"""You are a marketing expert. Provide detailed insights about: {request.question}

Include:
1. Current trends and best practices
2. Key strategies and tactics
3. Common challenges and solutions
4. Actionable recommendations
5. Expected outcomes and metrics

Please provide comprehensive, professional marketing insights."""

        if request.context:
            prompt = f"Background: {request.context}\n\n{prompt}"
        
        answer = await ask_gemini(prompt)
        
        return ResponseModel(
            answer=answer,
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/campaign-advice", response_model=ResponseModel)
async def get_campaign_advice(request: CampaignAdviceRequest):
    """
    Get strategic advice for marketing campaigns
    """
    try:
        # Build campaign advice prompt
        prompt = f"""You are an experienced marketing strategist. Provide detailed campaign advice for:

Campaign Type: {request.campaign_type}"""

        if request.target_audience:
            prompt += f"\nTarget Audience: {request.target_audience}"
        if request.budget:
            prompt += f"\nBudget: {request.budget}"
        if request.goals:
            prompt += f"\nGoals: {request.goals}"
        
        prompt += """

Please provide:
1. Campaign strategy and positioning
2. Key messaging and creative direction
3. Recommended channels and platforms
4. Content ideas and examples
5. Success metrics and KPIs
6. Timeline and milestones
7. Potential risks and mitigation strategies

Provide detailed, actionable advice."""

        if request.context:
            prompt = f"Additional Context: {request.context}\n\n{prompt}"
        
        answer = await ask_gemini(prompt)
        
        return ResponseModel(
            answer=answer,
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Gemini AI Agent API (Simple Version) on port 8004...")
    print("📡 Service endpoints:")
    print("   - GET  /          (Service info)")
    print("   - GET  /health    (Health check)")
    print("   - POST /ask       (Ask questions)")
    print("   - POST /marketing-insights")
    print("   - POST /campaign-advice")
    print("\n✨ Ready to receive requests!")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8004,
        log_level="info"
    )
