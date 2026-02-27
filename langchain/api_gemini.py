"""
FastAPI wrapper for Gemini AI Agent
Exposes the agent via REST API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(__file__))

# Import the agent
try:
    from main_gemini import ask_agent
    agent_available = True
except ImportError as e:
    print(f"Warning: Could not import agent: {e}")
    agent_available = False
    def ask_agent(question):
        return "Agent not available. Please install dependencies: pip install -r requirements_gemini.txt"

app = FastAPI(
    title="Gemini AI Marketing Agent",
    description="AI Agent powered by Google Gemini for marketing insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryInput(BaseModel):
    """Input model for agent queries"""
    question: str
    context: Optional[str] = None

class AgentResponse(BaseModel):
    """Response model from agent"""
    success: bool
    response: str
    agent_available: bool

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Gemini AI Marketing Agent",
        "version": "1.0.0",
        "status": "online",
        "agent_available": agent_available
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_available": agent_available
    }

@app.post("/ask", response_model=AgentResponse)
async def ask_question(query: QueryInput):
    """
    Ask the AI agent a question
    
    Args:
        query: QueryInput with question and optional context
        
    Returns:
        AgentResponse with the agent's answer
    """
    try:
        if not agent_available:
            return AgentResponse(
                success=False,
                response="AI Agent is not available. Please install dependencies.",
                agent_available=False
            )
        
        # Prepare the question with context if provided
        full_question = query.question
        if query.context:
            full_question = f"Context: {query.context}\n\nQuestion: {query.question}"
        
        # Get response from agent
        response = ask_agent(full_question)
        
        return AgentResponse(
            success=True,
            response=response,
            agent_available=True
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )

@app.post("/marketing-insights")
async def get_marketing_insights(query: QueryInput):
    """
    Get marketing insights from the AI agent
    Specialized endpoint for marketing questions
    """
    try:
        # Add marketing context to the question
        marketing_question = f"""As a marketing expert, please provide insights on: {query.question}
        
        Consider:
        - Current market trends
        - Best practices
        - Actionable recommendations
        - Data-driven insights
        """
        
        if query.context:
            marketing_question += f"\n\nAdditional context: {query.context}"
        
        response = ask_agent(marketing_question)
        
        return {
            "success": True,
            "insights": response,
            "category": "marketing"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting marketing insights: {str(e)}"
        )

@app.post("/campaign-advice")
async def get_campaign_advice(query: QueryInput):
    """
    Get campaign strategy advice from the AI agent
    """
    try:
        campaign_question = f"""As a campaign strategist, provide advice on: {query.question}
        
        Include:
        - Strategic recommendations
        - Target audience considerations
        - Channel suggestions
        - Key performance indicators
        - Timeline and milestones
        """
        
        if query.context:
            campaign_question += f"\n\nCampaign context: {query.context}"
        
        response = ask_agent(campaign_question)
        
        return {
            "success": True,
            "advice": response,
            "category": "campaign"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting campaign advice: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Gemini AI Agent API on port 8004...")
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=True)
