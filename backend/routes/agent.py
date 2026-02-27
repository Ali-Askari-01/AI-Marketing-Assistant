"""
AI Agent Routes – exposes the Gemini agent to the frontend via /api/v1/agent/*
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/agent", tags=["AI Agent"])

# Import the thin client (functions, not classes)
try:
    from ai import gemini_agent_client as agent
    _ok = True
except ImportError:
    _ok = False
    logger.warning("gemini_agent_client not importable")


# ── Request schemas ─────────────────────────────────────────────────
class AskBody(BaseModel):
    question: str
    context: Optional[str] = None

class CampaignBody(BaseModel):
    campaign_type: str
    target_audience: Optional[str] = None
    budget: Optional[str] = None
    goals: Optional[str] = None
    context: Optional[str] = None

class EnhanceBody(BaseModel):
    content: str
    content_type: str = "social_post"

class HashtagBody(BaseModel):
    content: str
    count: int = 10

class IdeasBody(BaseModel):
    topic: str
    count: int = 5

class StrategyBody(BaseModel):
    business_name: str = "My Business"
    industry: str = "technology"
    target_audience: str = "General audience"
    brand_voice: str = "professional"
    campaign_goal: str = "Increase brand awareness"
    duration_days: int = 30
    platforms: list = ["instagram", "linkedin"]
    budget: Optional[str] = None


def _wrap(data):
    """Uniform success envelope."""
    return {"success": True, "data": data}

def _err(msg: str, code: int = 500):
    return {"success": False, "error": {"message": msg, "code": code}}


# ── Endpoints ───────────────────────────────────────────────────────
@router.get("/status")
async def status():
    if not _ok:
        return _wrap({"available": False, "reason": "client not loaded"})
    available = await agent.is_available()
    return _wrap({"available": available, "service": "Gemini AI Agent", "url": "http://localhost:8004"})


@router.post("/ask")
async def ask(body: AskBody):
    if not _ok:
        return _err("Agent client not loaded")
    result = await agent.ask(body.question, body.context)
    if not result.get("success"):
        return _err(result.get("answer", "Agent error"))
    return _wrap({"question": body.question, "answer": result["answer"]})


@router.post("/marketing-insights")
async def insights(body: AskBody):
    if not _ok:
        return _err("Agent client not loaded")
    result = await agent.marketing_insights(body.question, body.context)
    if not result.get("success"):
        return _err(result.get("answer", "Agent error"))
    return _wrap({"topic": body.question, "insights": result["answer"]})


@router.post("/campaign-advice")
async def advice(body: CampaignBody):
    if not _ok:
        return _err("Agent client not loaded")
    result = await agent.campaign_advice(
        body.campaign_type,
        target_audience=body.target_audience,
        budget=body.budget,
        goals=body.goals,
        context=body.context,
    )
    if not result.get("success"):
        return _err(result.get("answer", "Agent error"))
    return _wrap({"campaign_type": body.campaign_type, "advice": result["answer"]})


@router.post("/enhance-content")
async def enhance(body: EnhanceBody):
    if not _ok:
        return _err("Agent client not loaded")
    result = await agent.enhance_content(body.content, body.content_type)
    if not result.get("success"):
        return _err(result.get("answer", "Agent error"))
    return _wrap({"original": body.content, "enhanced": result.get("enhanced", result.get("answer", ""))})


@router.post("/generate-hashtags")
async def hashtags(body: HashtagBody):
    if not _ok:
        return _err("Agent client not loaded")
    result = await agent.generate_hashtags(body.content, body.count)
    if not result.get("success"):
        return _err(result.get("answer", "Agent error"))
    return _wrap({"hashtags": result.get("hashtags", []), "count": len(result.get("hashtags", []))})


@router.post("/content-ideas")
async def ideas(body: IdeasBody):
    if not _ok:
        return _err("Agent client not loaded")
    result = await agent.content_ideas(body.topic, body.count)
    if not result.get("success"):
        return _err(result.get("answer", "Agent error"))
    return _wrap({"topic": body.topic, "ideas": result.get("ideas", []), "count": len(result.get("ideas", []))})


@router.post("/generate-strategy")
async def generate_strategy(body: StrategyBody):
    if not _ok:
        return _err("Agent client not loaded")
    result = await agent.generate_strategy(
        business_name=body.business_name,
        industry=body.industry,
        target_audience=body.target_audience,
        brand_voice=body.brand_voice,
        campaign_goal=body.campaign_goal,
        duration_days=body.duration_days,
        platforms=body.platforms,
        budget=body.budget,
    )
    if not result.get("success"):
        return _err(result.get("error", "Strategy generation failed"))
    return _wrap({"strategy": result.get("strategy", {})})
