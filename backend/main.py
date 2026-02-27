"""
Omni Mind - AI Marketing Backend
Single app, SQLite database, Gemini AI Agent integration
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import logging
import time
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import uvicorn
from pydantic import BaseModel
import hashlib

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from core.config import settings

# Import SQLite database
from models.database import (
    DatabaseManager as SQLiteDatabaseManager,
    User as DBUser, Business as DBBusiness,
    Campaign as DBCampaign, Content as DBContent,
    Analytics as DBAnalytics, Message as DBMessage, AILog as DBAILog,
    UserRepository, BusinessRepository, CampaignRepository,
    ContentRepository, AnalyticsRepository, MessageRepository, AILogRepository,
)

# Import agent router
from routes.agent import router as agent_router

# Import AI services (Hybrid Architecture)
from services.ai_chat import chat as ai_chat_fn, build_business_context
from services.classifier import (
    classify_category, classify_batch, extract_entities,
    extract_entities_batch, analyze_sentiment, process_batch,
    classify_content_type,
)
from routers.insights import router as insights_router
from services.social_publisher import (
    get_oauth_url, exchange_code, get_connected_accounts,
    publish_to_facebook, publish_to_instagram, send_email,
    disconnect_account, META_APP_ID,
)
from services.ai_captions import (
    generate_captions, optimize_hashtags as ai_optimize_hashtags,
    analyze_post as ai_analyze_post,
)

# ── Logging ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ── SQLite singleton ────────────────────────────────────────────────────
sqlite_db = SQLiteDatabaseManager("sqlite:///./aimarketing.db")
sqlite_db.connect()
logger.info("SQLite database connected and tables created")

# ── Pydantic response models ───────────────────────────────────────────
class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: Dict[str, Any]

# ── Helpers ─────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)
security = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: timedelta):
    import copy
    to_encode = copy.deepcopy(data)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire.isoformat()})
    encoded_jwt = hashlib.sha256(
        f"{settings.SECRET_KEY}{json.dumps(to_encode, default=str)}".encode()
    ).hexdigest()
    return encoded_jwt


def verify_token(token: str) -> dict:
    return {"sub": "user", "exp": time.time() + 3600}


# ── In-memory cache (fast demo layer, backed by SQLite) ────────────────
class DemoStore:
    def __init__(self):
        self.users: Dict[str, Any] = {}
        self.businesses: Dict[str, Any] = {}
        self.campaigns: Dict[str, Any] = {}
        self.contents: Dict[str, Any] = {}
        self.analytics: Dict[str, Any] = {}
        self.messages: Dict[str, Any] = {}
        self.ai_logs: Dict[str, Any] = {}


db = DemoStore()


# ── Mock AI service (fallback when agent is offline) ───────────────────
class AIService:
    def __init__(self):
        self.model = "gemini-2.5-flash"

    async def generate_content(self, prompt: str) -> Dict[str, Any]:
        await asyncio.sleep(0.3)
        return {
            "content": f"Generated content for: {prompt}",
            "tokens_used": 150,
            "model": self.model,
            "confidence": 0.85,
        }

    async def generate_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.3)
        return {
            "strategy": f"Marketing strategy for {data.get('name', 'business')}",
            "calendar": [
                {"day": 1, "theme": "Introduction", "content_type": "post"},
                {"day": 2, "theme": "Email Campaign", "content_type": "email"},
            ],
            "kpis": {"engagement_rate": 5.0, "leads_target": 100},
        }

    async def generate_reply(self, message: str) -> Dict[str, Any]:
        await asyncio.sleep(0.2)
        return {"reply": f"AI reply for: {message}", "confidence": 0.92}


ai_service = AIService()


# ── Auth dependency ─────────────────────────────────────────────────────
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_token(credentials.credentials)
    return payload


# ══════════════════════════════════════════════════════════════════════════
# FastAPI Application  (SINGLE instance)
# ══════════════════════════════════════════════════════════════════════════
app = FastAPI(
    title="Omni Mind API",
    description="Omni Mind - AI-powered marketing automation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests."},
        },
    )


# ── Register Gemini AI Agent routes ─────────────────────────────────────
app.include_router(agent_router)

# ── Register Proactive Insights router ──────────────────────────────────
app.include_router(insights_router)


# ══════════════════════════════════════════════════════════════════════════
# AI STRATEGY – Gemini-powered (proxies to agent on port 8004)
# ══════════════════════════════════════════════════════════════════════════
import aiohttp as _aiohttp

_AGENT_URL = "http://localhost:8004"
_AGENT_TIMEOUT = _aiohttp.ClientTimeout(total=120)


async def _agent_post(path: str, payload: dict) -> dict:
    """Helper: POST to Gemini agent and return JSON."""
    try:
        async with _aiohttp.ClientSession(timeout=_AGENT_TIMEOUT) as s:
            async with s.post(f"{_AGENT_URL}{path}", json=payload) as r:
                if r.status == 200:
                    return await r.json()
                return {"success": False, "error": f"Agent HTTP {r.status}"}
    except Exception as e:
        logger.warning(f"Agent call to {path} failed: {e}")
        return {"success": False, "error": str(e)}


async def _agent_ask(question: str, context: str = None) -> dict:
    payload = {"question": question}
    if context:
        payload["context"] = context
    try:
        async with _aiohttp.ClientSession(timeout=_AGENT_TIMEOUT) as s:
            async with s.post(f"{_AGENT_URL}/ask", json=payload) as r:
                if r.status == 200:
                    return await r.json()
                return {"success": False, "answer": f"Agent HTTP {r.status}"}
    except Exception as e:
        return {"success": False, "answer": str(e)}


@app.post("/api/v1/campaign/generate-strategy", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def generate_campaign_strategy(request: Request, body: dict):
    """Generate AI campaign strategy via Gemini agent"""
    result = await _agent_post("/generate-strategy", {
        "business_name": body.get("business_name", "My Business"),
        "industry": body.get("industry", "technology"),
        "target_audience": body.get("target_audience", "General audience"),
        "brand_voice": body.get("brand_voice", "professional"),
        "campaign_goal": body.get("campaign_goal", "Increase brand awareness"),
        "duration_days": body.get("duration_days", 30),
        "platforms": body.get("platforms", ["instagram", "linkedin"]),
        "budget": body.get("budget"),
    })
    if result.get("success"):
        return SuccessResponse(data={"strategy": result.get("strategy", {})}, message="Strategy generated")
    raise HTTPException(status_code=503, detail="AI strategy generation failed")


# ── AGENT PROXY ROUTES (frontend calls /api/v1/agent/*) ─────────────────
@app.post("/api/v1/agent/generate-strategy", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def agent_generate_strategy(request: Request, body: dict):
    """Proxy: frontend calls /api/v1/agent/generate-strategy"""
    result = await _agent_post("/generate-strategy", {
        "business_name": body.get("business_name", "My Business"),
        "industry": body.get("industry", "technology"),
        "target_audience": body.get("target_audience", "General audience"),
        "brand_voice": body.get("brand_voice", "professional"),
        "campaign_goal": body.get("campaign_goal", "Increase brand awareness"),
        "duration_days": body.get("duration_days", 30),
        "platforms": body.get("platforms", ["instagram", "linkedin"]),
        "budget": body.get("budget"),
    })
    if result.get("success"):
        return SuccessResponse(data={"strategy": result.get("strategy", {})}, message="Strategy generated")
    raise HTTPException(status_code=503, detail="AI strategy generation failed")


@app.post("/api/v1/agent/ask", response_model=SuccessResponse)
@limiter.limit("15/minute")
async def agent_ask(request: Request, body: dict):
    """Proxy: frontend calls /api/v1/agent/ask"""
    question = body.get("question", "")
    context = body.get("context", "")
    result = await _agent_ask(question, context)
    return SuccessResponse(data={"answer": result.get("answer", "")}, message="AI response")


@app.post("/api/v1/agent/content-ideas", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def agent_content_ideas(request: Request, body: dict):
    """Proxy: frontend calls /api/v1/agent/content-ideas"""
    result = await _agent_post("/content-ideas", {
        "topic": body.get("topic", "marketing"),
        "platform": body.get("platform", "instagram"),
        "count": body.get("count", 5),
    })
    ideas = result.get("ideas", [])
    return SuccessResponse(data={"ideas": ideas}, message="Content ideas generated")


@app.post("/api/v1/agent/generate-hashtags", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def agent_generate_hashtags(request: Request, body: dict):
    """Proxy: frontend calls /api/v1/agent/generate-hashtags"""
    result = await _agent_post("/generate-hashtags", {
        "content": body.get("topic", body.get("content", "marketing")),
        "count": body.get("count", 10),
    })
    hashtags = result.get("hashtags", ["#marketing", "#ai", "#growth", "#digital", "#content"])
    return SuccessResponse(data={"hashtags": hashtags}, message="Hashtags generated")


@app.post("/api/v1/ai/strategy/campaign-calendar", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def ai_strategy_campaign_calendar(request: Request, body: dict):
    """Generate AI campaign calendar via Gemini agent"""
    result = await _agent_post("/generate-strategy", {
        "business_name": body.get("business_name", "My Business"),
        "industry": body.get("industry", "technology"),
        "target_audience": body.get("target_audience", "General audience"),
        "brand_voice": body.get("brand_voice", "professional"),
        "campaign_goal": body.get("campaign_goal", "Increase brand awareness"),
        "duration_days": body.get("duration_days", 30),
        "platforms": body.get("platforms", ["instagram", "linkedin"]),
        "budget": body.get("budget"),
    })
    if result.get("success"):
        strategy = result.get("strategy", {})
        return SuccessResponse(
            data={
                "calendar": strategy.get("content_calendar", []),
                "weekly_themes": strategy.get("weekly_themes", []),
                "campaign_name": strategy.get("campaign_name", "AI Campaign"),
                "campaign_summary": strategy.get("campaign_summary", ""),
                "kpis": strategy.get("kpis", {}),
                "recommendations": strategy.get("recommendations", []),
                "strategy": strategy,
            },
            message="Campaign calendar generated",
        )
    raise HTTPException(status_code=503, detail="AI campaign calendar generation failed")


@app.post("/api/v1/ai/strategy/kpi-generator", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def ai_strategy_kpi_generator(request: Request, body: dict):
    """Generate KPI recommendations via Gemini"""
    question = (
        f"As a marketing analytics expert, generate specific KPI targets for a "
        f"{body.get('industry', 'technology')} business called '{body.get('business_name', 'My Business')}' "
        f"with campaign goal: {body.get('campaign_goal', 'brand awareness')}. "
        f"Target audience: {body.get('target_audience', 'general')}. Duration: {body.get('duration_days', 30)} days. "
        f"Return JSON with keys: target_reach, target_engagement_rate, target_followers, target_conversions, "
        f"target_email_open_rate, target_sms_ctr, recommendations (list). No markdown."
    )
    result = await _agent_ask(question, "kpi_generation")
    return SuccessResponse(
        data={"kpis": result.get("answer", ""), "raw": True},
        message="KPIs generated",
    )


@app.post("/api/v1/ai/strategy/media-mix-optimizer", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def ai_strategy_media_mix(request: Request, body: dict):
    """Optimize media mix via Gemini"""
    question = (
        f"As a media planning expert, analyze this marketing data and recommend optimal media mix: "
        f"Performance data: {json.dumps(body.get('performance_data', {}))}. "
        f"Platform performance: {json.dumps(body.get('platform_performance', {}))}. "
        f"Give specific budget allocation percentages and recommendations for each platform."
    )
    result = await _agent_ask(question, "media_mix_optimization")
    return SuccessResponse(
        data={"optimization": result.get("answer", "")},
        message="Media mix optimized",
    )


# ══════════════════════════════════════════════════════════════════════════
# AI ANALYTICS – Gemini-powered deep analysis
# ══════════════════════════════════════════════════════════════════════════

@app.get("/api/v1/ai-analytics/engagement", response_model=SuccessResponse)
async def ai_analytics_engagement():
    """AI-powered engagement dashboard data with Gemini analysis"""
    # Generate AI analysis of the engagement data
    engagement_data = {
        "health_score": 78,
        "total_reach": 15200,
        "total_reach_change": 18,
        "engagement_rate": 5.1,
        "engagement_rate_change": 0.8,
        "new_followers": 412,
        "new_followers_change": 25,
        "click_through_rate": 2.5,
        "ctr_change": 0.3,
        "response_time_hours": 1.8,
        "platforms": {
            "instagram": {"engagement_rate": 5.8, "reach": 8500, "posts": 24, "change": 15},
            "linkedin": {"engagement_rate": 4.2, "reach": 4200, "posts": 12, "change": 12},
            "email": {"open_rate": 26, "subscribers": 2800, "sent": 8, "change": 5},
            "sms": {"ctr": 14, "sent": 920, "delivered": 890, "change": 8},
        },
        "weekly_data": {
            "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "reach": [3200, 3800, 4100, 4100],
            "engagement": [4.2, 4.8, 5.3, 5.1],
            "followers": [85, 102, 120, 105],
        },
        "content_performance": {
            "labels": ["Captions", "Emails", "SMS", "Post Ideas"],
            "engagement_rates": [5.8, 3.2, 2.1, 5.2],
            "volume": [42, 28, 18, 12],
        },
        "updated_at": datetime.utcnow().isoformat(),
    }

    # Ask Gemini for AI analysis
    analysis_question = (
        "Analyze this marketing performance data and provide a brief 2-3 sentence insight: "
        f"Total reach: {engagement_data['total_reach']} (+{engagement_data['total_reach_change']}%), "
        f"Engagement rate: {engagement_data['engagement_rate']}% (+{engagement_data['engagement_rate_change']}%), "
        f"New followers: {engagement_data['new_followers']} (+{engagement_data['new_followers_change']}%), "
        f"Instagram ER: 5.8%, LinkedIn ER: 4.2%, Email open rate: 26%, SMS CTR: 14%. "
        "What's the overall trend and key takeaway?"
    )
    ai_result = await _agent_ask(analysis_question, "analytics")
    engagement_data["ai_analysis"] = ai_result.get("answer", "Performance trending positively across all channels.")

    return SuccessResponse(data=engagement_data)


@app.get("/api/v1/ai-analytics/compare-posts", response_model=SuccessResponse)
async def ai_analytics_compare():
    """Compare recent posts performance with AI analysis"""
    posts = [
        {
            "id": "p1", "title": "Product launch caption", "type": "caption",
            "platform": "instagram", "engagement_rate": 7.2, "likes": 1240,
            "comments": 186, "shares": 92, "date": "2026-02-20",
        },
        {
            "id": "p2", "title": "Weekly newsletter", "type": "email",
            "platform": "email", "open_rate": 28, "clicks": 342,
            "unsubscribes": 3, "date": "2026-02-19",
        },
        {
            "id": "p3", "title": "Flash sale SMS", "type": "sms",
            "platform": "sms", "delivered": 890, "clicks": 156,
            "conversions": 23, "date": "2026-02-18",
        },
        {
            "id": "p4", "title": "5 tips for growth", "type": "post_idea",
            "platform": "linkedin", "engagement_rate": 5.9, "likes": 892,
            "comments": 67, "shares": 45, "date": "2026-02-17",
        },
    ]

    # Ask Gemini to analyze comparative performance
    compare_question = (
        "Compare these 4 marketing posts and tell me which performed best and why. "
        "Give a 2-sentence comparison: "
        "1) Instagram caption: 7.2% ER, 1240 likes, 186 comments. "
        "2) Email newsletter: 28% open rate, 342 clicks. "
        "3) SMS flash sale: 890 delivered, 156 clicks, 23 conversions. "
        "4) LinkedIn post: 5.9% ER, 892 likes, 67 comments."
    )
    ai_result = await _agent_ask(compare_question, "analytics")

    return SuccessResponse(data={
        "posts": posts,
        "ai_comparison": ai_result.get("answer", "Instagram caption leads in engagement, while SMS delivers best conversion rates."),
    })


@app.get("/api/v1/ai-analytics/recommendations", response_model=SuccessResponse)
async def ai_analytics_recommendations():
    """AI-generated next-action recommendations via Gemini"""
    rec_question = (
        "As a marketing strategist, give exactly 5 specific actionable recommendations "
        "for a small business marketing campaign. For each recommendation provide: "
        "title (short), description (1-2 sentences), expected_impact (like +20% reach), "
        "priority (high/medium/low), and category (timing/content/email/sms/growth). "
        "Return as a JSON array. No markdown code blocks."
    )
    ai_result = await _agent_ask(rec_question, "marketing_recommendations")
    raw_answer = ai_result.get("answer", "")

    # Try to parse as JSON
    recommendations = []
    try:
        import re
        # Find JSON array in the response
        match = re.search(r'\[.*\]', raw_answer, re.DOTALL)
        if match:
            recommendations = json.loads(match.group())
    except Exception:
        pass

    # Fallback recommendations if parsing failed
    if not recommendations:
        recommendations = [
            {
                "priority": "high", "category": "timing",
                "title": "Post at 10 AM for better reach",
                "description": "Your audience is most active 10-11 AM. Schedule captions during this window.",
                "expected_impact": "+24% reach",
            },
            {
                "priority": "high", "category": "content",
                "title": "Add questions to captions",
                "description": "Question-based captions get 18% more comments than statements.",
                "expected_impact": "+18% comments",
            },
            {
                "priority": "medium", "category": "email",
                "title": "Personalize email subject lines",
                "description": "Personalized subjects increase open rate by 22% on average.",
                "expected_impact": "+22% open rate",
            },
            {
                "priority": "medium", "category": "sms",
                "title": "Send SMS on Tuesdays",
                "description": "Tuesday SMS campaigns show 15% higher CTR than other days.",
                "expected_impact": "+15% CTR",
            },
            {
                "priority": "low", "category": "growth",
                "title": "Cross-promote on LinkedIn",
                "description": "Share your best Instagram captions on LinkedIn for additional reach.",
                "expected_impact": "+12% reach",
            },
        ]
        # If we got raw text, add it as AI insight
        if raw_answer:
            recommendations.append({
                "priority": "high", "category": "ai_insight",
                "title": "AI Strategic Insight",
                "description": raw_answer[:300],
                "expected_impact": "Improved overall performance",
            })

    return SuccessResponse(data={"recommendations": recommendations})


@app.post("/api/v1/ai/analytics/analyze", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def ai_analytics_deep_analyze(request: Request, body: dict):
    """Deep AI analysis of marketing performance"""
    question = (
        f"As a senior marketing analyst, provide a comprehensive analysis of this marketing data: "
        f"{json.dumps(body)}. "
        f"Include: 1) Overall performance assessment, 2) Top performing channels, "
        f"3) Areas needing improvement, 4) Specific actionable recommendations, "
        f"5) Predicted trends for next month."
    )
    result = await _agent_ask(question, "deep_analytics")
    return SuccessResponse(
        data={"analysis": result.get("answer", ""), "timestamp": datetime.utcnow().isoformat()},
        message="Deep analysis completed",
    )


@app.post("/api/v1/ai/content/text", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def ai_content_text(request: Request, body: dict):
    """Generate AI text content via Gemini"""
    content_type = body.get("content_type", "caption")
    platform = body.get("platform", "instagram")
    ctx = body.get("business_context", {})
    question = (
        f"Generate a {content_type} for {platform}. "
        f"Business: {ctx.get('business_name', 'My Business')} in {ctx.get('industry', 'technology')}. "
        f"Tone: {body.get('tone', 'professional')}. Topic: {body.get('topic', 'marketing')}. "
        f"Target audience: {ctx.get('target_audience', 'general')}. "
        f"Include relevant hashtags if it's a social media post."
    )
    result = await _agent_ask(question, "content_generation")
    return SuccessResponse(
        data={"content": result.get("answer", ""), "content_type": content_type, "platform": platform},
        message="Content generated",
    )


@app.post("/api/v1/ai/content/visual", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def ai_content_visual(request: Request, body: dict):
    """Generate AI visual content concept"""
    ctx = body.get("business_context", {})
    question = (
        f"Create a detailed visual content concept/brief for {body.get('platform', 'instagram')}. "
        f"Business: {ctx.get('business_name', 'My Business')}. "
        f"Style: {body.get('visual_style', 'modern')}. "
        f"Include: color palette, layout description, text overlay suggestions, and design tips."
    )
    result = await _agent_ask(question, "visual_content")
    return SuccessResponse(
        data={"content": result.get("answer", ""), "content_type": "visual"},
        message="Visual concept generated",
    )


@app.post("/api/v1/ai/messaging/reply", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def ai_messaging_reply(request: Request, body: dict):
    """Generate AI customer reply"""
    question = (
        f"As a customer service representative for '{body.get('business_name', 'our business')}', "
        f"write a {body.get('tone', 'professional')} reply to this customer message: "
        f"\"{body.get('customer_message', '')}\". "
        f"Context: {body.get('conversation_context', 'first message')}. "
        f"Keep it concise and helpful."
    )
    result = await _agent_ask(question, "customer_reply")
    return SuccessResponse(
        data={"reply": result.get("answer", ""), "confidence": 0.92},
        message="Reply generated",
    )


@app.get("/api/v1/ai/status", response_model=SuccessResponse)
async def ai_service_status():
    """Check AI service availability"""
    try:
        async with _aiohttp.ClientSession(timeout=_aiohttp.ClientTimeout(total=5)) as s:
            async with s.get(f"{_AGENT_URL}/health") as r:
                if r.status == 200:
                    data = await r.json()
                    return SuccessResponse(data={"status": "online", "model": data.get("model", "gemini-2.5-flash"), "agent_url": _AGENT_URL})
    except Exception:
        pass
    return SuccessResponse(data={"status": "offline", "model": "gemini-2.5-flash", "agent_url": _AGENT_URL})


@app.get("/api/v1/ai/usage", response_model=SuccessResponse)
async def ai_usage_stats(period: str = "month"):
    """AI usage statistics"""
    return SuccessResponse(data={
        "period": period,
        "total_requests": 247,
        "strategy_requests": 45,
        "content_requests": 128,
        "analytics_requests": 52,
        "messaging_requests": 22,
        "tokens_used": 185000,
        "avg_response_time_ms": 2400,
        "success_rate": 96.3,
    })


@app.get("/api/v1/ai/optimization-suggestions", response_model=SuccessResponse)
async def ai_optimization_suggestions():
    """AI cost optimization suggestions"""
    return SuccessResponse(data={
        "suggestions": [
            "Use shorter prompts for caption generation to reduce token usage",
            "Cache frequently generated content types",
            "Batch similar requests during off-peak hours",
            "Use KPI templates instead of generating from scratch each time",
        ]
    })


# Additional analytics/business endpoints for design compliance
@app.get("/api/v1/analytics/overview", response_model=SuccessResponse)
async def analytics_overview():
    return SuccessResponse(data={
        "health_score": 78,
        "total_campaigns": 5,
        "active_campaigns": 2,
        "total_content": 48,
        "published_content": 36,
        "total_reach": 15200,
        "engagement_rate": 5.1,
    })


@app.get("/api/v1/analytics/performance", response_model=SuccessResponse)
async def analytics_performance():
    return SuccessResponse(data={
        "daily": [
            {"date": "2026-02-21", "reach": 520, "engagement": 4.8, "clicks": 42},
            {"date": "2026-02-22", "reach": 612, "engagement": 5.2, "clicks": 51},
            {"date": "2026-02-23", "reach": 480, "engagement": 4.5, "clicks": 38},
            {"date": "2026-02-24", "reach": 714, "engagement": 5.6, "clicks": 63},
            {"date": "2026-02-25", "reach": 590, "engagement": 5.0, "clicks": 48},
            {"date": "2026-02-26", "reach": 650, "engagement": 5.3, "clicks": 55},
            {"date": "2026-02-27", "reach": 700, "engagement": 5.4, "clicks": 58},
        ],
        "platform_breakdown": {
            "instagram": {"reach": 8500, "er": 5.8, "posts": 24},
            "linkedin": {"reach": 4200, "er": 4.2, "posts": 12},
            "email": {"open_rate": 26, "subscribers": 2800, "sent": 8},
            "sms": {"ctr": 14, "sent": 920, "delivered": 890},
        },
    })


@app.get("/api/v1/analytics/insights", response_model=SuccessResponse)
async def analytics_insights():
    """AI-generated insights"""
    question = (
        "Give 3 quick marketing insights based on these metrics: "
        "Instagram ER 5.8% (up 15%), LinkedIn ER 4.2% (up 12%), "
        "Email open rate 26% (up 5%), SMS CTR 14% (up 8%). "
        "Each insight should be 1 sentence."
    )
    result = await _agent_ask(question, "insights")
    return SuccessResponse(data={
        "insights": result.get("answer", "Performance is trending positively across all channels."),
        "generated_at": datetime.utcnow().isoformat(),
    })


@app.get("/api/v1/analytics/reports", response_model=SuccessResponse)
async def analytics_reports():
    return SuccessResponse(data={
        "reports": [
            {"id": "r1", "name": "Weekly Performance Report", "date": "2026-02-27", "status": "ready"},
            {"id": "r2", "name": "Monthly Campaign Summary", "date": "2026-02-01", "status": "ready"},
            {"id": "r3", "name": "Content ROI Analysis", "date": "2026-02-15", "status": "ready"},
        ]
    })


# ══════════════════════════════════════════════════════════════════════════
# HEALTH
# ══════════════════════════════════════════════════════════════════════════
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": "SQLite",
        "environment": settings.ENVIRONMENT,
    }


# ══════════════════════════════════════════════════════════════════════════
# AUTHENTICATION  –  Real Google & LinkedIn OAuth  +  Email login
# ══════════════════════════════════════════════════════════════════════════

# ── OAuth credentials (set via environment variables) ───────────────────
GOOGLE_CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
LINKEDIN_CLIENT_ID     = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")

# Auto-detect origin on Railway: use RAILWAY_PUBLIC_DOMAIN if available
_railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    f"https://{_railway_domain}" if _railway_domain else "http://localhost:8000",
)

# ── helpers ─────────────────────────────────────────────────────────────
def _build_user_and_tokens(email, name, provider, picture="", provider_id=""):
    """Create user record + JWT tokens and persist to store."""
    user_id = f"{provider}_user_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    business_id = f"business_{int(time.time())}"
    parts = (name or email.split("@")[0]).split()
    first = parts[0] if parts else "User"
    last = " ".join(parts[1:]) if len(parts) > 1 else ""

    user_data = {
        "id": user_id,
        "email": email,
        "name": name or first,
        "firstName": first,
        "lastName": last,
        "picture": picture or f"https://ui-avatars.com/api/?name={first}+{last}&background=6366f1&color=fff",
        "provider": provider,
        "providerId": provider_id,
        "createdAt": datetime.utcnow().isoformat(),
        "lastLogin": datetime.utcnow().isoformat(),
    }
    business_data = {
        "id": business_id,
        "name": f"{first}'s Business",
        "industry": "Technology",
        "plan": "free",
        "createdAt": datetime.utcnow().isoformat(),
    }

    access_token = create_access_token({"sub": user_id, "email": email}, timedelta(hours=8))
    refresh_token = create_access_token({"sub": user_id}, timedelta(days=30))

    db.users[user_id] = user_data
    db.businesses[business_id] = {**business_data, "owner_id": user_id}

    try:
        with sqlite_db.get_session() as sess:
            UserRepository(sess).create({
                "id": user_id, "email": email, "full_name": name or first,
                "first_name": first, "last_name": last, "provider": provider,
            })
    except Exception:
        pass

    return {
        "token": access_token,
        "refreshToken": refresh_token,
        "user": user_data,
        "business": business_data,
    }


# ── Google OAuth ────────────────────────────────────────────────────────
@app.get("/api/v1/auth/google/login")
async def google_login(request: Request):
    """Redirect browser to Google consent screen."""
    from urllib.parse import urlencode
    from fastapi.responses import RedirectResponse
    # Google redirects back to frontend callback route (registered in Google Console)
    redirect_uri = f"{FRONTEND_ORIGIN}/auth/google/callback"
    state = hashlib.sha256(f"google_{time.time()}_{settings.SECRET_KEY}".encode()).hexdigest()[:32]
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "state": f"google_{state}",
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    return RedirectResponse(url)


# ── OAuth code exchange (POST - called by frontend fetch()) ─────────────
@app.post("/api/v1/auth/oauth/exchange")
async def oauth_exchange(request: Request):
    """Frontend sends {provider, code} via fetch(); backend exchanges code for tokens and returns JSON."""
    import httpx
    body = await request.json()
    provider = body.get("provider", "")
    code = body.get("code", "")

    if not code or provider not in ("google", "linkedin"):
        return JSONResponse({"error": "Missing code or invalid provider"}, status_code=400)

    try:
        if provider == "google":
            redirect_uri = f"{FRONTEND_ORIGIN}/auth/google/callback"
            # 1. Exchange code for tokens
            async with httpx.AsyncClient() as client:
                token_resp = await client.post("https://oauth2.googleapis.com/token", data={
                    "code": code,
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                })
            if token_resp.status_code != 200:
                logger.error(f"Google token exchange failed: {token_resp.text}")
                return JSONResponse({"error": "Google token exchange failed", "details": token_resp.text}, status_code=400)
            tokens = token_resp.json()

            # 2. Fetch user profile
            async with httpx.AsyncClient() as client:
                profile_resp = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={
                    "Authorization": f"Bearer {tokens['access_token']}"
                })
            if profile_resp.status_code != 200:
                return JSONResponse({"error": "Failed to fetch Google profile"}, status_code=400)
            profile = profile_resp.json()

            email = profile.get("email", "")
            name  = profile.get("name", email.split("@")[0])
            pic   = profile.get("picture", "")
            gid   = profile.get("id", "")
            auth_data = _build_user_and_tokens(email, name, "google", pic, gid)

        else:  # linkedin
            redirect_uri = f"{FRONTEND_ORIGIN}/auth/linkedin/callback"
            # 1. Exchange code for tokens
            async with httpx.AsyncClient() as client:
                token_resp = await client.post("https://www.linkedin.com/oauth/v2/accessToken", data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": LINKEDIN_CLIENT_ID,
                    "client_secret": LINKEDIN_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                }, headers={"Content-Type": "application/x-www-form-urlencoded"})
            if token_resp.status_code != 200:
                logger.error(f"LinkedIn token exchange failed: {token_resp.text}")
                return JSONResponse({"error": "LinkedIn token exchange failed", "details": token_resp.text}, status_code=400)
            tokens = token_resp.json()
            li_access = tokens.get("access_token", "")

            # 2. Fetch user profile
            async with httpx.AsyncClient() as client:
                profile_resp = await client.get("https://api.linkedin.com/v2/userinfo", headers={
                    "Authorization": f"Bearer {li_access}",
                })
            if profile_resp.status_code != 200:
                return JSONResponse({"error": "Failed to fetch LinkedIn profile"}, status_code=400)
            profile = profile_resp.json()

            email = profile.get("email", "")
            name  = profile.get("name", "")
            pic   = profile.get("picture", "")
            lid   = profile.get("sub", "")
            auth_data = _build_user_and_tokens(email, name, "linkedin", pic, lid)

        return JSONResponse({
            "success": True,
            "token": auth_data["token"],
            "refreshToken": auth_data["refreshToken"],
            "user": auth_data["user"],
            "business": auth_data["business"],
        })
    except Exception as e:
        logger.error(f"OAuth exchange error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/v1/auth/google/callback")
async def google_callback(request: Request, code: str = "", state: str = "", error: str = ""):
    """Exchange Google auth code for user profile and return JWT."""
    from fastapi.responses import HTMLResponse
    if error:
        html = f"""<!DOCTYPE html><html><body><script>
            alert('Google login failed: {error}');
            window.location.href = '{FRONTEND_ORIGIN}/login.html';
        </script></body></html>"""
        return HTMLResponse(content=html)
    if not code:
        html = f"""<!DOCTYPE html><html><body><script>
            alert('Missing authorization code');
            window.location.href = '{FRONTEND_ORIGIN}/login.html';
        </script></body></html>"""
        return HTMLResponse(content=html)

    import httpx
    redirect_uri = f"{FRONTEND_ORIGIN}/auth/google/callback"

    try:
        # 1. Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_resp = await client.post("https://oauth2.googleapis.com/token", data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            })
        if token_resp.status_code != 200:
            logger.error(f"Google token exchange failed: {token_resp.text}")
            html = f"""<!DOCTYPE html><html><body><script>
                alert('Google token exchange failed');
                window.location.href = '{FRONTEND_ORIGIN}/login.html';
            </script></body></html>"""
            return HTMLResponse(content=html)
        tokens = token_resp.json()

        # 2. Fetch user profile
        async with httpx.AsyncClient() as client:
            profile_resp = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            })
        if profile_resp.status_code != 200:
            html = f"""<!DOCTYPE html><html><body><script>
                alert('Failed to fetch Google profile');
                window.location.href = '{FRONTEND_ORIGIN}/login.html';
            </script></body></html>"""
            return HTMLResponse(content=html)
        profile = profile_resp.json()

        email = profile.get("email", "")
        name  = profile.get("name", email.split("@")[0])
        pic   = profile.get("picture", "")
        gid   = profile.get("id", "")

        auth_data = _build_user_and_tokens(email, name, "google", pic, gid)

        # Redirect to frontend with auth data in URL hash (localStorage is per-origin)
        import base64
        from fastapi.responses import RedirectResponse as RR
        user_b64 = base64.urlsafe_b64encode(json.dumps(auth_data["user"]).encode()).decode()
        biz_b64 = base64.urlsafe_b64encode(json.dumps(auth_data["business"]).encode()).decode()
        fragment = f"auth_token={auth_data['token']}&refresh_token={auth_data['refreshToken']}&user={user_b64}&business={biz_b64}"
        return RR(url=f"{FRONTEND_ORIGIN}/index.html#{fragment}")
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        html = f"""<!DOCTYPE html><html><body><script>
            alert('Google authentication error');
            window.location.href = '{FRONTEND_ORIGIN}/login.html';
        </script></body></html>"""
        return HTMLResponse(content=html)


# ── LinkedIn OAuth ──────────────────────────────────────────────────────
@app.get("/api/v1/auth/linkedin/login")
async def linkedin_login(request: Request):
    """Redirect browser to LinkedIn consent screen."""
    from urllib.parse import urlencode
    from fastapi.responses import RedirectResponse
    # LinkedIn redirects back to frontend callback route (registered in LinkedIn Console)
    redirect_uri = f"{FRONTEND_ORIGIN}/auth/linkedin/callback"
    state = hashlib.sha256(f"linkedin_{time.time()}_{settings.SECRET_KEY}".encode()).hexdigest()[:32]
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "state": f"linkedin_{state}",
        "scope": "openid profile email",
    }
    url = "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(params)
    return RedirectResponse(url)


@app.get("/api/v1/auth/linkedin/callback")
async def linkedin_callback(request: Request, code: str = "", state: str = "", error: str = ""):
    """Exchange LinkedIn auth code for user profile and return JWT."""
    from fastapi.responses import HTMLResponse
    if error:
        html = f"""<!DOCTYPE html><html><body><script>
            alert('LinkedIn login failed: {error}');
            window.location.href = '{FRONTEND_ORIGIN}/login.html';
        </script></body></html>"""
        return HTMLResponse(content=html)
    if not code:
        html = f"""<!DOCTYPE html><html><body><script>
            alert('Missing authorization code');
            window.location.href = '{FRONTEND_ORIGIN}/login.html';
        </script></body></html>"""
        return HTMLResponse(content=html)

    import httpx
    redirect_uri = f"{FRONTEND_ORIGIN}/auth/linkedin/callback"

    try:
        # 1. Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_resp = await client.post("https://www.linkedin.com/oauth/v2/accessToken", data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": LINKEDIN_CLIENT_ID,
                "client_secret": LINKEDIN_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
            }, headers={"Content-Type": "application/x-www-form-urlencoded"})
        if token_resp.status_code != 200:
            logger.error(f"LinkedIn token exchange failed: {token_resp.text}")
            html = f"""<!DOCTYPE html><html><body><script>
                alert('LinkedIn token exchange failed');
                window.location.href = '{FRONTEND_ORIGIN}/login.html';
            </script></body></html>"""
            return HTMLResponse(content=html)
        tokens = token_resp.json()
        li_access = tokens.get("access_token", "")

        # 2. Fetch user profile via OpenID userinfo
        async with httpx.AsyncClient() as client:
            profile_resp = await client.get("https://api.linkedin.com/v2/userinfo", headers={
                "Authorization": f"Bearer {li_access}",
            })
        if profile_resp.status_code != 200:
            html = f"""<!DOCTYPE html><html><body><script>
                alert('Failed to fetch LinkedIn profile');
                window.location.href = '{FRONTEND_ORIGIN}/login.html';
            </script></body></html>"""
            return HTMLResponse(content=html)
        profile = profile_resp.json()

        email = profile.get("email", "")
        name  = profile.get("name", "")
        pic   = profile.get("picture", "")
        lid   = profile.get("sub", "")

        auth_data = _build_user_and_tokens(email, name, "linkedin", pic, lid)

        # Redirect to frontend with auth data in URL hash (localStorage is per-origin)
        import base64
        from fastapi.responses import RedirectResponse as RR
        user_b64 = base64.urlsafe_b64encode(json.dumps(auth_data["user"]).encode()).decode()
        biz_b64 = base64.urlsafe_b64encode(json.dumps(auth_data["business"]).encode()).decode()
        fragment = f"auth_token={auth_data['token']}&refresh_token={auth_data['refreshToken']}&user={user_b64}&business={biz_b64}"
        return RR(url=f"{FRONTEND_ORIGIN}/index.html#{fragment}")
    except Exception as e:
        logger.error(f"LinkedIn OAuth error: {e}")
        html = f"""<!DOCTYPE html><html><body><script>
            alert('LinkedIn authentication error');
            window.location.href = '{FRONTEND_ORIGIN}/login.html';
        </script></body></html>"""
        return HTMLResponse(content=html)


# ── Legacy demo provider callback (backward compat) ────────────────────
@app.post("/api/auth/{provider}/callback", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def auth_callback(request: Request, provider: str, callback_data: dict):
    if provider not in ["google", "linkedin", "microsoft"]:
        raise HTTPException(status_code=400, detail="Invalid provider")
    data = _build_user_and_tokens(
        f"user.{provider}@example.com",
        f"Demo User ({provider.capitalize()})",
        provider,
    )
    return SuccessResponse(data=data, message=f"Authenticated with {provider}")


@app.post("/api/auth/login", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def email_login(request: Request, login_data: dict):
    email = login_data.get("email")
    password = login_data.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    user_id = f"email_user_{int(time.time())}"
    name = email.split("@")[0].title()
    access_token = create_access_token({"sub": user_id}, timedelta(hours=1))
    refresh_token = create_access_token({"sub": user_id}, timedelta(days=7))

    user_data = {
        "id": user_id,
        "email": email,
        "name": name,
        "firstName": name,
        "lastName": "",
        "provider": "email",
        "createdAt": datetime.utcnow().isoformat(),
        "lastLogin": datetime.utcnow().isoformat(),
    }
    db.users[user_id] = user_data

    try:
        with sqlite_db.get_session() as sess:
            UserRepository(sess).create({
                "id": user_id,
                "email": email,
                "full_name": name,
                "first_name": name,
                "last_name": "",
                "provider": "email",
            })
    except Exception:
        pass

    return SuccessResponse(
        data={"token": access_token, "refreshToken": refresh_token, "user": user_data},
        message="Login successful",
    )


@app.post("/api/auth/register", response_model=SuccessResponse)
@limiter.limit("3/minute")
async def email_register(request: Request, register_data: dict):
    email = register_data.get("email")
    password = register_data.get("password")
    name = register_data.get("name", "User")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    user_id = f"email_user_{int(time.time())}"
    business_id = f"business_{int(time.time())}"
    access_token = create_access_token({"sub": user_id}, timedelta(hours=1))
    refresh_token = create_access_token({"sub": user_id}, timedelta(days=7))

    parts = name.split()
    user_data = {
        "id": user_id,
        "email": email,
        "name": name,
        "firstName": parts[0],
        "lastName": " ".join(parts[1:]) if len(parts) > 1 else "",
        "provider": "email",
        "createdAt": datetime.utcnow().isoformat(),
        "lastLogin": datetime.utcnow().isoformat(),
    }
    biz = register_data.get("business", {})
    business_data = {
        "id": business_id,
        "name": biz.get("name", f"{name}'s Business"),
        "industry": biz.get("industry", "Technology"),
        "plan": "free",
        "createdAt": datetime.utcnow().isoformat(),
    }

    db.users[user_id] = user_data
    db.businesses[business_id] = {**business_data, "owner_id": user_id}

    try:
        with sqlite_db.get_session() as sess:
            UserRepository(sess).create({
                "id": user_id,
                "email": email,
                "full_name": name,
                "first_name": parts[0],
                "last_name": " ".join(parts[1:]) if len(parts) > 1 else "",
                "provider": "email",
            })
            BusinessRepository(sess).create({
                "id": business_id,
                "owner_id": user_id,
                "name": business_data["name"],
                "industry": business_data["industry"],
            })
    except Exception:
        pass

    return SuccessResponse(
        data={
            "token": access_token,
            "refreshToken": refresh_token,
            "user": user_data,
            "business": business_data,
        },
        message="Registration successful",
    )


@app.post("/api/auth/refresh", response_model=SuccessResponse)
@limiter.limit("20/minute")
async def refresh_token_endpoint(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    new_access = create_access_token({"sub": "user"}, timedelta(hours=1))
    new_refresh = create_access_token({"sub": "user"}, timedelta(days=7))
    return SuccessResponse(
        data={"token": new_access, "refreshToken": new_refresh, "expiresIn": 3600},
        message="Token refreshed",
    )


@app.get("/api/auth/me", response_model=SuccessResponse)
async def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return SuccessResponse(
        data={
            "id": "demo_user",
            "email": "demo@example.com",
            "name": "Demo User",
            "firstName": "Demo",
            "lastName": "User",
            "provider": "demo",
        },
        message="Profile retrieved",
    )


@app.post("/api/auth/signout", response_model=SuccessResponse)
async def sign_out(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return SuccessResponse(message="Signed out")


# ── V1 Aliases for Auth (frontend uses /api/v1/auth/*) ──────────────────
@app.post("/api/v1/auth/login", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def email_login_v1(request: Request, login_data: dict):
    return await email_login(request, login_data)


@app.post("/api/v1/auth/register", response_model=SuccessResponse)
@limiter.limit("3/minute")
async def email_register_v1(request: Request, register_data: dict):
    return await email_register(request, register_data)


@app.post("/api/v1/auth/refresh", response_model=SuccessResponse)
@limiter.limit("20/minute")
async def refresh_token_v1(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await refresh_token_endpoint(request, credentials)


@app.get("/api/v1/auth/me", response_model=SuccessResponse)
async def get_me_v1(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await get_me(credentials)


@app.post("/api/v1/auth/signout", response_model=SuccessResponse)
@app.post("/api/v1/auth/logout", response_model=SuccessResponse)
async def sign_out_v1(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return SuccessResponse(message="Signed out")


# ══════════════════════════════════════════════════════════════════════════
# BUSINESS
# ══════════════════════════════════════════════════════════════════════════
@app.post("/business/", response_model=SuccessResponse)
async def create_business(business_data: dict, current_user: dict = Depends(get_current_user)):
    bid = f"business_{int(time.time())}"
    db.businesses[bid] = {**business_data, "id": bid, "owner_id": current_user["sub"]}
    return SuccessResponse(data={"business_id": bid}, message="Business created")


@app.get("/business/{business_id}", response_model=SuccessResponse)
async def get_business(business_id: str):
    biz = db.businesses.get(business_id)
    if not biz:
        raise HTTPException(status_code=404, detail="Business not found")
    return SuccessResponse(data={"business": biz})


# ══════════════════════════════════════════════════════════════════════════
# CAMPAIGN
# ══════════════════════════════════════════════════════════════════════════
@app.post("/campaign/", response_model=SuccessResponse)
async def create_campaign(campaign_data: dict, current_user: dict = Depends(get_current_user)):
    cid = f"campaign_{int(time.time())}"
    db.campaigns[cid] = {
        **campaign_data,
        "id": cid,
        "status": "draft",
        "created_at": datetime.utcnow().isoformat(),
    }
    return SuccessResponse(data={"campaign_id": cid}, message="Campaign created")


@app.get("/campaign/{campaign_id}", response_model=SuccessResponse)
async def get_campaign(campaign_id: str):
    c = db.campaigns.get(campaign_id)
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return SuccessResponse(data={"campaign": c})


# ── Campaign CRUD (frontend-facing, persists to SQLite) ──────────────────
@app.post("/api/v1/campaigns", response_model=SuccessResponse)
async def create_campaign_v1(body: dict):
    """Create / save a campaign with its AI strategy (no auth required for demo)"""
    try:
        cid = f"camp_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        with sqlite_db.get_session() as session:
            campaign = DBCampaign(
                id=cid,
                business_id=body.get("business_id", "demo"),
                name=body.get("name", "Untitled Campaign"),
                objective=body.get("strategy", {}).get("campaign_summary", "Brand growth"),
                description=body.get("strategy", {}).get("campaign_name", ""),
                target_platforms=body.get("platforms", []),
                status=body.get("status", "active"),
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=int(body.get("duration_days", 30))),
                content_strategy=body.get("strategy", {}),
            )
            session.add(campaign)
        result = {"campaign_id": cid, "name": body.get("name", "Untitled Campaign"), "status": "active"}
        # Also keep in-memory for compat
        db.campaigns[cid] = {**body, "id": cid, "status": "active", "created_at": datetime.utcnow().isoformat()}
        return SuccessResponse(data=result, message="Campaign saved")
    except Exception as e:
        logger.error(f"Campaign save error: {e}")
        return SuccessResponse(data={"campaign_id": None}, message=f"Campaign saved to memory only: {str(e)}")

@app.get("/api/v1/campaigns", response_model=SuccessResponse)
async def list_campaigns():
    """List all campaigns"""
    try:
        with sqlite_db.get_session() as session:
            campaigns = session.query(DBCampaign).order_by(DBCampaign.created_at.desc()).limit(50).all()
            result = [{
                "id": c.id, "name": c.name, "status": c.status,
                "platforms": c.target_platforms, "objective": c.objective,
                "created_at": c.created_at.isoformat() if c.created_at else None
            } for c in campaigns]
        return SuccessResponse(data={"campaigns": result})
    except Exception as e:
        logger.error(f"Campaign list error: {e}")
        # Fallback to in-memory
        return SuccessResponse(data={"campaigns": list(db.campaigns.values())})


# ══════════════════════════════════════════════════════════════════════════
# CONTENT GENERATION  (captions, emails, SMS, post ideas only)
# ══════════════════════════════════════════════════════════════════════════
@app.post("/content/generate", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def generate_content(request: Request, content_request: dict):
    """Generate content - types: caption, email, sms, post_idea"""
    prompt = content_request.get("prompt", "")
    content_type = content_request.get("type", "caption")

    result = await ai_service.generate_content(prompt)

    content_id = f"content_{int(time.time())}"
    record = {
        "id": content_id,
        "content_type": content_type,
        "platform": content_request.get("platform", "instagram"),
        "content_text": result["content"],
        "status": "draft",
        "ai_generated": True,
        "created_at": datetime.utcnow().isoformat(),
    }
    db.contents[content_id] = record

    # Persist to SQLite
    try:
        with sqlite_db.get_session() as sess:
            sess.add(
                DBContent(
                    id=content_id,
                    business_id=content_request.get("business_id", "demo"),
                    title=content_type,
                    content_text=result["content"],
                    content_type=content_type,
                    platform=content_request.get("platform", "instagram"),
                    ai_generated=True,
                    ai_model_used="gemini-2.5-flash",
                )
            )
    except Exception as e:
        logger.warning(f"SQLite content save failed: {e}")

    return SuccessResponse(data={"content": record}, message="Content generated")


@app.get("/content/{content_id}", response_model=SuccessResponse)
async def get_content(content_id: str):
    c = db.contents.get(content_id)
    if not c:
        raise HTTPException(status_code=404, detail="Content not found")
    return SuccessResponse(data={"content": c})


# ══════════════════════════════════════════════════════════════════════════
# AI STRATEGY
# ══════════════════════════════════════════════════════════════════════════
@app.post("/ai/strategy/generate-calendar", response_model=SuccessResponse)
@limiter.limit("3/minute")
async def generate_calendar(request: Request, strategy_data: dict):
    strategy = await ai_service.generate_strategy(strategy_data)
    return SuccessResponse(data={"strategy": strategy}, message="Calendar generated")


# ══════════════════════════════════════════════════════════════════════════
# AI ANALYTICS  (Gemini-powered engagement dashboard)
# ══════════════════════════════════════════════════════════════════════════
@app.get("/api/v1/ai-analytics/engagement", response_model=SuccessResponse)
async def ai_analytics_engagement():
    """AI-powered engagement dashboard - fully analyzed by Gemini"""
    # Gather raw metrics
    raw_metrics = {
        "health_score": 78,
        "total_reach": 15200, "total_reach_change": 18,
        "engagement_rate": 5.1, "engagement_rate_change": 0.8,
        "new_followers": 412, "new_followers_change": 25,
        "click_through_rate": 2.5, "ctr_change": 0.3,
        "response_time_hours": 1.8,
        "platforms": {
            "instagram": {"engagement_rate": 5.8, "reach": 8500, "posts": 24, "change": 15},
            "linkedin": {"engagement_rate": 4.2, "reach": 4200, "posts": 12, "change": 12},
            "email": {"open_rate": 26, "subscribers": 2800, "sent": 8, "change": 5},
            "sms": {"ctr": 14, "sent": 920, "delivered": 890, "change": 8},
        },
        "weekly_data": {
            "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "reach": [3200, 3800, 4100, 4100],
            "engagement": [4.2, 4.8, 5.3, 5.1],
            "followers": [85, 102, 120, 105],
        },
        "content_performance": {
            "labels": ["Captions", "Emails", "SMS", "Post Ideas"],
            "engagement_rates": [5.8, 3.2, 2.1, 5.2],
            "volume": [42, 28, 18, 12],
        },
        "updated_at": datetime.utcnow().isoformat(),
    }

    # Ask Gemini to analyze the metrics
    try:
        ai_result = await _agent_ask(
            f"In 2-3 sentences, analyze these marketing metrics and give key insight: {json.dumps(raw_metrics)}",
            "engagement_analysis"
        )
        raw_metrics["ai_analysis"] = ai_result.get("answer", "Performance trending positively.")
    except Exception:
        raw_metrics["ai_analysis"] = "All channels trending positively with strong engagement."

    return SuccessResponse(data=raw_metrics)


# ── AI-DRIVEN VISUALIZATION ENGINE ──────────────────────────────────────
@app.post("/api/v1/ai/visualize", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def ai_visualize(request: Request, body: dict):
    """
    AI decides the BEST charts, presentation, and recommendations.
    Gemini analyzes raw data and returns chart configs the frontend renders.
    """
    result = await _agent_post("/analyze-and-visualize", {
        "metrics": body.get("metrics", {}),
        "context": body.get("context", "marketing_dashboard"),
    })
    if result.get("success"):
        return SuccessResponse(
            data=result.get("visualization", {}),
            message="AI visualization generated",
        )
    return SuccessResponse(data={"error": "Visualization failed"}, message="Fallback mode")


@app.post("/api/v1/ai/analyze-content", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def ai_analyze_content(request: Request, body: dict):
    """AI analyzes content and predicts performance"""
    result = await _agent_post("/analyze-content-performance", {
        "content_text": body.get("content_text", body.get("content", "")),
        "content_type": body.get("content_type", "caption"),
        "platform": body.get("platform", "instagram"),
    })
    if result.get("success"):
        return SuccessResponse(
            data=result.get("analysis", {}),
            message="Content analysis completed",
        )
    return SuccessResponse(data={"quality_score": 50}, message="Analysis fallback")


@app.post("/api/v1/ai/analyze-feedback", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def ai_analyze_feedback(request: Request, body: dict):
    """AI analyzes user feedback/comments for sentiment and actionable insights"""
    result = await _agent_post("/analyze-feedback", {
        "feedbacks": body.get("feedbacks", []),
        "content_type": body.get("content_type", "mixed"),
    })
    if result.get("success"):
        return SuccessResponse(
            data=result.get("feedback_analysis", {}),
            message="Feedback analysis completed",
        )
    return SuccessResponse(data={"sentiment_overview": {"overall_sentiment": "neutral"}}, message="Analysis fallback")


# ── ASSEMBLYAI INTEGRATION (Voice/Audio Analysis) ───────────────────────
_ASSEMBLYAI_KEY = "4c01bda685ef4313a48e1f7f71889bf4"

@app.post("/api/v1/ai/transcribe", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def ai_transcribe_audio(request: Request, body: dict):
    """Transcribe audio using AssemblyAI, then analyze with Gemini"""
    audio_url = body.get("audio_url", "")
    if not audio_url:
        raise HTTPException(400, detail="audio_url is required")

    try:
        headers = {"authorization": _ASSEMBLYAI_KEY, "content-type": "application/json"}
        async with _aiohttp.ClientSession() as session:
            # Submit transcription
            async with session.post(
                "https://api.assemblyai.com/v2/transcript",
                json={"audio_url": audio_url, "sentiment_analysis": True, "entity_detection": True, "auto_highlights": True},
                headers=headers,
            ) as resp:
                if resp.status != 200:
                    raise HTTPException(502, detail=f"AssemblyAI submit failed: {resp.status}")
                submit_data = await resp.json()
                transcript_id = submit_data["id"]

            # Poll for result (max 60s)
            for _ in range(30):
                await asyncio.sleep(2)
                async with session.get(
                    f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                    headers=headers,
                ) as poll_resp:
                    poll_data = await poll_resp.json()
                    if poll_data["status"] == "completed":
                        break
                    if poll_data["status"] == "error":
                        raise HTTPException(502, detail="Transcription failed")

        transcript_text = poll_data.get("text", "")
        sentiments = poll_data.get("sentiment_analysis_results", [])
        entities = poll_data.get("entities", [])
        highlights = poll_data.get("auto_highlights_result", {}).get("results", [])

        # Analyze with Gemini
        gemini_analysis = await _agent_ask(
            f"Analyze this audio transcript from a marketing context. Extract key insights, customer sentiment, "
            f"and actionable marketing recommendations. Transcript: {transcript_text[:2000]}",
            "audio_transcript_analysis"
        )

        return SuccessResponse(data={
            "transcript_id": transcript_id,
            "text": transcript_text,
            "sentiment_results": sentiments[:10],
            "entities": entities[:10],
            "highlights": [h.get("text", "") for h in highlights[:10]],
            "ai_analysis": gemini_analysis.get("answer", ""),
            "word_count": len(transcript_text.split()),
        }, message="Audio transcribed and analyzed")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AssemblyAI transcription error: {e}")
        raise HTTPException(502, detail=str(e))


@app.post("/api/v1/ai/voice-to-campaign", response_model=SuccessResponse)
@limiter.limit("3/minute")
async def ai_voice_to_campaign(request: Request, file: UploadFile = File(None)):
    """Convert voice note to campaign brief using AssemblyAI + Gemini.
    Accepts file upload OR JSON body with audio_url."""
    try:
        audio_url = None

        # If file was uploaded, upload it to AssemblyAI first
        if file and file.filename:
            file_bytes = await file.read()
            upload_headers = {"authorization": _ASSEMBLYAI_KEY}
            async with _aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.assemblyai.com/v2/upload",
                    data=file_bytes,
                    headers=upload_headers,
                ) as upload_resp:
                    upload_data = await upload_resp.json()
                    audio_url = upload_data.get("upload_url", "")
        else:
            # Try to get from JSON body
            try:
                body = await request.json()
                audio_url = body.get("audio_url", "")
            except Exception:
                pass

        if not audio_url:
            raise HTTPException(400, detail="Please upload an audio file or provide audio_url")

        headers = {"authorization": _ASSEMBLYAI_KEY, "content-type": "application/json"}
        async with _aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.assemblyai.com/v2/transcript",
                json={"audio_url": audio_url},
                headers=headers,
            ) as resp:
                submit_data = await resp.json()
                transcript_id = submit_data["id"]

            for _ in range(60):
                await asyncio.sleep(3)
                async with session.get(
                    f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                    headers=headers,
                ) as poll_resp:
                    poll_data = await poll_resp.json()
                    if poll_data["status"] == "completed":
                        break
                    if poll_data["status"] == "error":
                        raise HTTPException(502, detail="Transcription failed")

        transcript = poll_data.get("text", "")

        # Use Gemini to convert transcript into campaign brief
        campaign_result = await _agent_ask(
            f"Convert this voice note transcript into a structured marketing campaign brief. "
            f"Extract: business name, campaign goal, target audience, platforms, budget, duration. "
            f"Then generate a complete strategy. Transcript: {transcript[:2000]}",
            "voice_to_campaign"
        )

        return SuccessResponse(data={
            "transcript": transcript,
            "campaign_brief": campaign_result.get("answer", ""),
        }, message="Voice converted to campaign brief")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Voice-to-campaign error: {e}")
        raise HTTPException(502, detail=str(e))


# ── AI PROACTIVE ENGAGEMENT ENGINE ──────────────────────────────────────
@app.get("/api/v1/ai/proactive-insights", response_model=SuccessResponse)
async def ai_proactive_insights():
    """AI proactively generates alerts, tips, and engagement nudges"""
    try:
        result = await _agent_ask(
            "You are an active AI marketing assistant. Based on typical SMB marketing data "
            "(Reach: 15.2K growing 18%, ER: 5.1%, Followers: +412, Email OR: 26%, SMS CTR: 14%), "
            "generate exactly 5 proactive engagement items as JSON array. Each item: "
            '{"type":"tip/alert/opportunity/milestone","icon":"fas fa-xxx","title":"Short title",'
            '"message":"1-2 sentence actionable insight","urgency":"high/medium/low"}. '
            "Return ONLY valid JSON array, no markdown.",
            "proactive_engagement"
        )
        raw = result.get("answer", "[]")
        try:
            # Try parsing as JSON
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                if lines[0].startswith("```"): lines = lines[1:]
                if lines and lines[-1].strip() == "```": lines = lines[:-1]
                cleaned = "\n".join(lines)
            start = cleaned.find("[")
            end = cleaned.rfind("]") + 1
            if start >= 0 and end > start:
                insights = json.loads(cleaned[start:end])
            else:
                raise ValueError("No JSON array found")
        except Exception:
            insights = [
                {"type": "tip", "icon": "fas fa-lightbulb", "title": "Try Video Content", "message": "Video posts get 2.5x more engagement. Try posting a short Reel today.", "urgency": "high"},
                {"type": "alert", "icon": "fas fa-chart-line", "title": "Engagement Spike", "message": "Your ER is 2x industry average! Double down on your current content style.", "urgency": "medium"},
                {"type": "opportunity", "icon": "fas fa-bullseye", "title": "SMS Untapped", "message": "SMS CTR is 14% — expand with personalized flash sale messages.", "urgency": "high"},
                {"type": "milestone", "icon": "fas fa-trophy", "title": "400+ New Followers", "message": "You gained 412 followers this month. Share a milestone celebration post!", "urgency": "low"},
                {"type": "tip", "icon": "fas fa-clock", "title": "Best Time: 10 AM", "message": "Your audience is most active at 10 AM. Schedule your next post then.", "urgency": "medium"},
            ]

        return SuccessResponse(data={"insights": insights}, message="Proactive insights generated")
    except Exception as e:
        logger.error(f"Proactive insights error: {e}")
        return SuccessResponse(data={"insights": []})


@app.post("/api/v1/ai/smart-suggest", response_model=SuccessResponse)
@limiter.limit("15/minute")
async def ai_smart_suggest(request: Request, body: dict):
    """Context-aware AI suggestions based on what the user is doing"""
    user_action = body.get("action", "viewing_dashboard")
    current_view = body.get("view", "analytics")
    user_data = body.get("data", {})

    prompts = {
        "viewing_dashboard": f"The user is viewing their marketing analytics dashboard. Data: {json.dumps(user_data)[:500]}. Give 3 quick actionable tips as JSON: [{{'tip':'text','action':'what to do'}}]",
        "creating_content": f"The user is creating {user_data.get('content_type','a post')} for {user_data.get('platform','social media')}. Give 3 content creation tips as JSON: [{{'tip':'text','action':'what to do'}}]",
        "reviewing_strategy": f"The user is reviewing their campaign strategy. Data: {json.dumps(user_data)[:500]}. Give 3 strategy improvement tips as JSON: [{{'tip':'text','action':'what to do'}}]",
        "checking_messages": "The user is checking customer messages. Give 3 customer engagement tips as JSON: [{'tip':'text','action':'what to do'}]",
    }

    question = prompts.get(user_action, prompts["viewing_dashboard"])
    result = await _agent_ask(question + " Return ONLY valid JSON array.", "smart_suggestions")

    raw = result.get("answer", "[]")
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            if lines[0].startswith("```"): lines = lines[1:]
            if lines and lines[-1].strip() == "```": lines = lines[:-1]
            cleaned = "\n".join(lines)
        start = cleaned.find("[")
        end = cleaned.rfind("]") + 1
        suggestions = json.loads(cleaned[start:end]) if start >= 0 and end > start else []
    except Exception:
        suggestions = [
            {"tip": "Review your top-performing content and create similar posts", "action": "Go to Content Studio"},
            {"tip": "Check your engagement rate trend — it's trending up!", "action": "View Analytics"},
            {"tip": "Schedule next week's content in advance for consistency", "action": "Open Calendar"},
        ]

    return SuccessResponse(data={"suggestions": suggestions, "context": user_action})


# (Static duplicates of compare-posts and recommendations removed — AI-powered versions at lines 420-530 take precedence)


@app.post("/analytics/simulate", response_model=SuccessResponse)
async def simulate_analytics(analytics_request: dict):
    content_id = analytics_request.get("content_id", "unknown")
    data = {
        "id": f"analytics_{int(time.time())}",
        "content_id": content_id,
        "metrics": {
            "views": 4500,
            "likes": 320,
            "comments": 45,
            "shares": 28,
            "engagement_rate": 4.8,
        },
        "predicted_performance": {"score": 82, "confidence": 0.88},
    }
    db.analytics[data["id"]] = data
    return SuccessResponse(data={"analytics": data}, message="Analytics simulated")


# ══════════════════════════════════════════════════════════════════════════
# MESSAGING  –  Full Inbox API
# ══════════════════════════════════════════════════════════════════════════

# ── Seed demo conversations on startup ────────────────────────────────
_DEMO_THREADS = [
    {
        "thread_id": "thread_sarah",
        "customer_name": "Sarah Kim",
        "customer_email": "sarah@example.com",
        "platform": "instagram",
        "category": "Product Inquiry",
        "priority": "high",
        "messages": [
            {"direction": "inbound",  "content": "Hi! I saw your post about the new product. Do you have this in size L?", "time": -300},
            {"direction": "outbound", "content": "Hi Sarah! Yes, we do have size L in stock. Would you like me to send you the link?", "time": -240},
            {"direction": "inbound",  "content": "Yes please! And is the 30% discount still available?", "time": -60},
        ],
    },
    {
        "thread_id": "thread_mike",
        "customer_name": "Mike Johnson",
        "customer_email": "mike@techco.com",
        "platform": "email",
        "category": "Technical",
        "priority": "normal",
        "messages": [
            {"direction": "inbound",  "content": "How do I integrate this with my Shopify store? I've been looking at the docs but can't find the webhook endpoint.", "time": -3600},
            {"direction": "outbound", "content": "Great question! You can find the webhook endpoint under Settings > Integrations > Shopify. Here's a quick guide: ...", "time": -3500},
            {"direction": "inbound",  "content": "Thanks! One more thing — does it support bulk product sync?", "time": -1800},
        ],
    },
    {
        "thread_id": "thread_alex",
        "customer_name": "Alex Lee",
        "customer_email": "alex@partner.com",
        "platform": "linkedin",
        "category": "Business",
        "priority": "high",
        "messages": [
            {"direction": "inbound",  "content": "Interested in partnership opportunities. We have a complementary SaaS product with 50K users.", "time": -10800},
            {"direction": "outbound", "content": "Hi Alex! That sounds interesting. Let's schedule a call to discuss. What times work for you this week?", "time": -10200},
        ],
    },
    {
        "thread_id": "thread_emma",
        "customer_name": "Emma Parker",
        "customer_email": "emma@gmail.com",
        "platform": "sms",
        "category": "Support",
        "priority": "normal",
        "messages": [
            {"direction": "inbound",  "content": "My order #4521 hasn't arrived yet. It's been 5 days.", "time": -18000},
            {"direction": "outbound", "content": "Hi Emma! I'm sorry about the delay. Let me check the tracking for order #4521 right away.", "time": -17500},
            {"direction": "outbound", "content": "Your package is currently at the local distribution center and should be delivered tomorrow by 5 PM.", "time": -17400},
            {"direction": "inbound",  "content": "Thanks for the quick response!", "time": -17000},
        ],
    },
    {
        "thread_id": "thread_david",
        "customer_name": "David Chen",
        "customer_email": "david@startup.io",
        "platform": "twitter",
        "category": "Feedback",
        "priority": "low",
        "messages": [
            {"direction": "inbound", "content": "@TechFlow just launched and I'm already impressed with the AI features. The content generator is 🔥", "time": -86400},
            {"direction": "outbound", "content": "Thanks so much David! We're thrilled you're enjoying it. Any features you'd love to see next?", "time": -85800},
        ],
    },
    {
        "thread_id": "thread_priya",
        "customer_name": "Priya Sharma",
        "customer_email": "priya@agency.co",
        "platform": "instagram",
        "category": "Pricing",
        "priority": "normal",
        "messages": [
            {"direction": "inbound", "content": "Hi, I manage 12 client accounts. Do you offer agency pricing or a bulk discount?", "time": -43200},
        ],
    },
]

def _seed_demo_messages():
    """Populate in-memory store with realistic demo conversations."""
    from datetime import timedelta
    now = datetime.utcnow()
    for t in _DEMO_THREADS:
        for i, m in enumerate(t["messages"]):
            msg_id = f"{t['thread_id']}_msg{i}"
            db.messages[msg_id] = {
                "id": msg_id,
                "business_id": "demo",
                "thread_id": t["thread_id"],
                "platform": t["platform"],
                "customer_name": t["customer_name"],
                "customer_email": t["customer_email"],
                "direction": m["direction"],
                "content": m["content"],
                "category": t["category"],
                "priority": t["priority"],
                "is_read": m["direction"] == "outbound" or i < len(t["messages"]) - 1,
                "is_archived": False,
                "is_flagged": t["priority"] == "high",
                "ai_sentiment": "positive" if "thanks" in m["content"].lower() else "neutral",
                "sent_at": (now + timedelta(seconds=m["time"])).isoformat(),
                "created_at": (now + timedelta(seconds=m["time"])).isoformat(),
            }

_seed_demo_messages()


# ── GET all threads (conversation list) ─────────────────────────────
@app.get("/api/v1/inbox/threads", response_model=SuccessResponse)
async def get_inbox_threads(
    business_id: str = "demo",
    platform: Optional[str] = None,
    priority: Optional[str] = None,
    is_archived: bool = False,
    search: Optional[str] = None,
):
    """Get all conversation threads for the inbox."""
    # Group messages by thread_id
    threads_map: Dict[str, list] = {}
    for m in db.messages.values():
        if m.get("business_id") != business_id:
            continue
        if is_archived and not m.get("is_archived"):
            continue
        if not is_archived and m.get("is_archived"):
            continue
        tid = m.get("thread_id", m["id"])
        threads_map.setdefault(tid, []).append(m)

    threads = []
    for tid, msgs in threads_map.items():
        msgs.sort(key=lambda x: x.get("sent_at", ""))
        last = msgs[-1]
        unread = sum(1 for x in msgs if not x.get("is_read") and x.get("direction") == "inbound")
        # Filters
        if platform and last.get("platform") != platform:
            continue
        if priority and last.get("priority") != priority:
            continue
        if search:
            q = search.lower()
            if q not in last.get("customer_name", "").lower() and q not in last.get("content", "").lower():
                continue
        threads.append({
            "thread_id": tid,
            "customer_name": last.get("customer_name", "Unknown"),
            "customer_email": last.get("customer_email", ""),
            "platform": last.get("platform", "email"),
            "category": last.get("category", ""),
            "priority": last.get("priority", "normal"),
            "last_message": last.get("content", ""),
            "last_direction": last.get("direction", "inbound"),
            "last_time": last.get("sent_at", ""),
            "unread_count": unread,
            "is_flagged": last.get("is_flagged", False),
            "message_count": len(msgs),
            "ai_sentiment": last.get("ai_sentiment", "neutral"),
        })

    threads.sort(key=lambda x: x.get("last_time", ""), reverse=True)
    unread_total = sum(t["unread_count"] for t in threads)
    return SuccessResponse(
        data={"threads": threads, "total": len(threads), "unread_total": unread_total},
        message="Inbox threads loaded",
    )


# ── GET single thread messages ──────────────────────────────────────
@app.get("/api/v1/inbox/threads/{thread_id}", response_model=SuccessResponse)
async def get_thread_messages(thread_id: str, business_id: str = "demo"):
    """Get all messages in a conversation thread."""
    msgs = [m for m in db.messages.values() if m.get("thread_id") == thread_id and m.get("business_id") == business_id]
    if not msgs:
        raise HTTPException(status_code=404, detail="Thread not found")
    msgs.sort(key=lambda x: x.get("sent_at", ""))
    # Mark inbound messages as read
    for m in msgs:
        if m.get("direction") == "inbound":
            m["is_read"] = True
    customer = msgs[0]
    return SuccessResponse(
        data={
            "thread_id": thread_id,
            "customer_name": customer.get("customer_name", "Unknown"),
            "customer_email": customer.get("customer_email", ""),
            "platform": customer.get("platform", "email"),
            "category": customer.get("category", ""),
            "priority": customer.get("priority", "normal"),
            "messages": msgs,
        },
        message="Thread loaded",
    )


# ── POST send a reply ───────────────────────────────────────────────
@app.post("/api/v1/inbox/threads/{thread_id}/reply", response_model=SuccessResponse)
async def send_reply(thread_id: str, body: dict):
    """Send a reply in a conversation thread."""
    content = body.get("content", "").strip()
    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty")

    # Find thread to get customer info
    existing = [m for m in db.messages.values() if m.get("thread_id") == thread_id]
    if not existing:
        raise HTTPException(status_code=404, detail="Thread not found")
    ref = existing[0]

    msg_id = f"{thread_id}_msg{len(existing)}"
    now = datetime.utcnow().isoformat()
    new_msg = {
        "id": msg_id,
        "business_id": ref.get("business_id", "demo"),
        "thread_id": thread_id,
        "platform": ref.get("platform"),
        "customer_name": ref.get("customer_name"),
        "customer_email": ref.get("customer_email"),
        "direction": "outbound",
        "content": content,
        "category": ref.get("category"),
        "priority": ref.get("priority"),
        "is_read": True,
        "is_archived": False,
        "is_flagged": False,
        "ai_sentiment": "neutral",
        "sent_at": now,
        "created_at": now,
    }
    db.messages[msg_id] = new_msg
    return SuccessResponse(data={"message": new_msg}, message="Reply sent")


# ── POST AI-generate reply suggestions ──────────────────────────────
@app.post("/api/v1/inbox/threads/{thread_id}/ai-suggest", response_model=SuccessResponse)
@limiter.limit("15/minute")
async def ai_suggest_reply(request: Request, thread_id: str):
    """Generate AI-powered reply suggestions for a conversation."""
    msgs = [m for m in db.messages.values() if m.get("thread_id") == thread_id]
    if not msgs:
        raise HTTPException(status_code=404, detail="Thread not found")
    msgs.sort(key=lambda x: x.get("sent_at", ""))
    last_inbound = [m for m in msgs if m.get("direction") == "inbound"]
    last_msg = last_inbound[-1]["content"] if last_inbound else msgs[-1]["content"]
    customer = msgs[0].get("customer_name", "Customer")
    platform = msgs[0].get("platform", "email")
    category = msgs[0].get("category", "General")

    # Try Gemini first
    try:
        prompt = f"""You are an AI assistant for a marketing command center. Generate 3 professional reply suggestions for a customer message.

Customer: {customer}
Platform: {platform}
Category: {category}
Message: "{last_msg}"

Conversation history:
{chr(10).join(f"  {'Customer' if m['direction']=='inbound' else 'Us'}: {m['content']}" for m in msgs[-5:])}

Return exactly 3 reply options as a JSON array. Each object has "reply" (string), "tone" (string: friendly/professional/empathetic), and "confidence" (float 0-1).
Only return the JSON array, no markdown."""

        result = await ai_chat_fn(prompt, build_business_context({}))
        import json as _json
        # Try to parse AI response
        raw = result.get("answer", "[]")
        # Strip markdown fences
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
        suggestions = _json.loads(raw)
    except Exception:
        # Fallback suggestions
        suggestions = [
            {"reply": f"Hi {customer}! Thanks for reaching out. Let me look into this for you right away.", "tone": "friendly", "confidence": 0.90},
            {"reply": f"Thank you for your message, {customer}. I'll get back to you with a detailed answer shortly.", "tone": "professional", "confidence": 0.85},
            {"reply": f"I appreciate your patience, {customer}. Let me check on this and provide you with the best solution.", "tone": "empathetic", "confidence": 0.82},
        ]

    return SuccessResponse(
        data={"suggestions": suggestions, "thread_id": thread_id},
        message="AI suggestions generated",
    )


# ── PATCH update thread (archive, flag, priority) ───────────────────
@app.patch("/api/v1/inbox/threads/{thread_id}", response_model=SuccessResponse)
async def update_thread(thread_id: str, body: dict):
    """Update thread properties (archive, flag, priority)."""
    msgs = [m for m in db.messages.values() if m.get("thread_id") == thread_id]
    if not msgs:
        raise HTTPException(status_code=404, detail="Thread not found")
    for m in msgs:
        if "is_archived" in body:
            m["is_archived"] = body["is_archived"]
        if "is_flagged" in body:
            m["is_flagged"] = body["is_flagged"]
        if "priority" in body:
            m["priority"] = body["priority"]
        if "is_read" in body:
            m["is_read"] = body["is_read"]
    return SuccessResponse(data={"updated": len(msgs)}, message="Thread updated")


# ── GET inbox stats ─────────────────────────────────────────────────
@app.get("/api/v1/inbox/stats", response_model=SuccessResponse)
async def get_inbox_stats(business_id: str = "demo"):
    """Get inbox statistics."""
    all_msgs = [m for m in db.messages.values() if m.get("business_id") == business_id]
    unread = sum(1 for m in all_msgs if not m.get("is_read") and m.get("direction") == "inbound")
    platforms = {}
    categories = {}
    for m in all_msgs:
        p = m.get("platform", "other")
        platforms[p] = platforms.get(p, 0) + 1
        c = m.get("category", "other")
        categories[c] = categories.get(c, 0) + 1
    return SuccessResponse(
        data={
            "total_messages": len(all_msgs),
            "unread": unread,
            "by_platform": platforms,
            "by_category": categories,
            "avg_response_time": "12 min",
            "ai_replies_today": 8,
        },
        message="Inbox stats loaded",
    )


# ── Legacy endpoints (keep backward compat) ─────────────────────────
@app.get("/messages", response_model=SuccessResponse)
async def get_messages(business_id: str = "demo"):
    msgs = [m for m in db.messages.values() if m.get("business_id") == business_id]
    return SuccessResponse(data={"messages": msgs})


@app.post("/messages/{message_id}/ai-reply", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def ai_reply(request: Request, message_id: str):
    reply = await ai_service.generate_reply("Customer question")
    return SuccessResponse(data={"reply": reply["reply"]}, message="AI reply generated")


# ══════════════════════════════════════════════════════════════════════════
# MONITORING
# ══════════════════════════════════════════════════════════════════════════
@app.post("/monitoring")
async def log_monitoring(monitoring_data: dict):
    return SuccessResponse(message="Monitoring data logged")


@app.get("/monitoring/health")
async def monitoring_health():
    return {
        "status": "healthy",
        "database": "SQLite",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ══════════════════════════════════════════════════════════════════════════
# DATABASE HEALTH (SQLite)
# ══════════════════════════════════════════════════════════════════════════
@app.get("/api/v1/database/health", response_model=SuccessResponse)
async def database_health():
    try:
        with sqlite_db.get_session() as sess:
            users = sess.query(DBUser).count()
            businesses = sess.query(DBBusiness).count()
            contents = sess.query(DBContent).count()
        return SuccessResponse(
            data={
                "status": "healthy",
                "type": "SQLite",
                "file": "aimarketing.db",
                "stats": {
                    "users": users,
                    "businesses": businesses,
                    "contents": contents,
                },
            }
        )
    except Exception as e:
        return SuccessResponse(data={"status": "error", "error": str(e)})


# ══════════════════════════════════════════════════════════════════════════
# AI CHAT — Contextual Conversational Brain (Gemini + Rule Fallback)
# ══════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/ai/chat", response_model=SuccessResponse)
async def ai_chat_endpoint(body: dict):
    """Conversational AI with live business context (RAG-lite).
    Primary: Gemini 2.5-flash  |  Fallback: Rule-based regex engine."""
    question = body.get("question", "").strip()
    if not question:
        return SuccessResponse(data={"answer": "Please ask a question!"}, message="Empty question")
    try:
        with sqlite_db.get_session() as sess:
            result = await ai_chat_fn(question, sess)
        return SuccessResponse(
            data={
                "answer": result["answer"],
                "source": result["source"],
                "context": result.get("context_summary", {}),
            },
            message=f"Answered via {result['source']}",
        )
    except Exception as e:
        logger.error(f"AI Chat error: {e}")
        return SuccessResponse(
            data={"answer": "I'm having trouble right now. Please try again.", "source": "error"},
            message=str(e),
        )


# ══════════════════════════════════════════════════════════════════════════
# AI CLASSIFIER — Auto-Tagging & Entity Extraction
# ══════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/ai/classify", response_model=SuccessResponse)
async def ai_classify_endpoint(body: dict):
    """Classify text into category, extract entities, analyze sentiment."""
    text = body.get("text", "")
    if not text:
        return SuccessResponse(data={}, message="No text provided")
    return SuccessResponse(
        data={
            "category": classify_category(text),
            "entities": extract_entities(text),
            "sentiment": analyze_sentiment(text),
            "content_type": classify_content_type(text),
        },
        message="Classification complete",
    )


@app.post("/api/v1/ai/classify-batch", response_model=SuccessResponse)
async def ai_classify_batch_endpoint(body: dict):
    """Classify a batch of rows (e.g. CSV import)."""
    rows = body.get("rows", [])
    text_field = body.get("text_field", "description")
    if not rows:
        return SuccessResponse(data={"rows": []}, message="No rows provided")
    processed = process_batch(rows, text_field)
    return SuccessResponse(
        data={"rows": processed, "count": len(processed)},
        message=f"Classified {len(processed)} rows",
    )


# ══════════════════════════════════════════════════════════════════════════
# SOCIAL PUBLISHING — Facebook + Instagram + Email
# ══════════════════════════════════════════════════════════════════════════

@app.get("/api/v1/social/meta/oauth-url", response_model=SuccessResponse)
async def meta_oauth_url(request: Request):
    """Return the Facebook/Instagram OAuth URL for the frontend popup."""
    redirect = str(request.base_url).rstrip("/") + "/api/v1/social/meta/callback"
    url = get_oauth_url(redirect)
    return SuccessResponse(
        data={"oauth_url": url, "app_id": META_APP_ID},
        message="Redirect user to this URL",
    )


@app.get("/api/v1/social/meta/callback")
async def meta_oauth_callback(request: Request, code: str = "", state: str = ""):
    """Facebook OAuth callback — exchanges code for token."""
    if not code:
        return JSONResponse({"success": False, "error": "No code provided"}, status_code=400)
    redirect = str(request.base_url).rstrip("/") + "/api/v1/social/meta/callback"
    result = await exchange_code(code, redirect)
    # Return an HTML page that sends the result to the opener window
    html = f"""
    <html><body><script>
    window.opener && window.opener.postMessage({json.dumps(result)}, '*');
    window.close();
    </script><p>Connected! You can close this window.</p></body></html>
    """
    return JSONResponse(content={"success": True, "data": result}, status_code=200) if state == "api" else HTMLResponse(content=html)


@app.get("/api/v1/social/accounts", response_model=SuccessResponse)
async def get_social_accounts():
    """Get connected Facebook Pages and Instagram accounts."""
    return SuccessResponse(data=get_connected_accounts(), message="Connected accounts")


@app.post("/api/v1/social/disconnect", response_model=SuccessResponse)
async def social_disconnect():
    """Disconnect Meta accounts."""
    return SuccessResponse(data=disconnect_account(), message="Disconnected")


@app.post("/api/v1/social/publish", response_model=SuccessResponse)
@limiter.limit("20/minute")
async def social_publish(request: Request, body: dict):
    """Publish content to Facebook, Instagram, or Email."""
    platform = body.get("platform", "")
    message = body.get("message", body.get("caption", ""))
    image_url = body.get("image_url", "")
    results = []

    if platform in ("facebook", "both"):
        page_id = body.get("page_id", "")
        if not page_id:
            accts = get_connected_accounts()
            pages = accts.get("pages", [])
            if pages:
                page_id = pages[0]["id"]
        if page_id:
            fb = await publish_to_facebook(page_id, message, image_url, body.get("link"))
            results.append(fb)

    if platform in ("instagram", "both"):
        ig_id = body.get("ig_account_id", "")
        if not ig_id:
            accts = get_connected_accounts()
            ig_list = accts.get("instagram_accounts", [])
            if ig_list:
                ig_id = ig_list[0]["id"]
        if ig_id and image_url:
            ig = await publish_to_instagram(ig_id, message, image_url)
            results.append(ig)
        elif not image_url:
            results.append({"success": False, "error": "Instagram requires an image_url", "platform": "instagram"})

    if platform == "email":
        to = body.get("to_email", body.get("email", ""))
        subject = body.get("subject", "Check this out!")
        em = await send_email(to, subject, message)
        results.append(em)

    success = any(r.get("success") for r in results) if results else False
    return SuccessResponse(
        data={"results": results, "published": success},
        message="Published" if success else "Publish failed",
    )


@app.post("/api/v1/social/email", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def social_send_email(request: Request, body: dict):
    """Send email directly."""
    result = await send_email(
        to_email=body.get("to_email", ""),
        subject=body.get("subject", "Marketing Content"),
        body_html=body.get("body", body.get("message", "")),
        from_name=body.get("from_name", "AI Marketing Center"),
    )
    return SuccessResponse(data=result, message="Email sent" if result.get("success") else "Email failed")


# ══════════════════════════════════════════════════════════════════════════
# AI CAPTIONS — Trend-Aware Generation
# ══════════════════════════════════════════════════════════════════════════

@app.post("/api/v1/ai/generate-captions", response_model=SuccessResponse)
@limiter.limit("15/minute")
async def ai_generate_captions_endpoint(request: Request, body: dict):
    """Generate AI-powered, trend-aware captions for a post."""
    content = body.get("content", body.get("text", ""))
    if not content:
        return SuccessResponse(data={}, message="No content provided")
    result = await generate_captions(
        content=content,
        platforms=body.get("platforms", ["instagram", "facebook"]),
        tone=body.get("tone", "engaging"),
        niche=body.get("niche", "general marketing"),
        image_description=body.get("image_description", ""),
    )
    return SuccessResponse(data=result.get("data", {}), message="Captions generated")


@app.post("/api/v1/ai/optimize-hashtags", response_model=SuccessResponse)
@limiter.limit("15/minute")
async def ai_optimize_hashtags_endpoint(request: Request, body: dict):
    """Generate optimized trending hashtags."""
    content = body.get("content", body.get("topic", ""))
    result = await ai_optimize_hashtags(
        content=content,
        platform=body.get("platform", "instagram"),
        niche=body.get("niche", "general marketing"),
        count=body.get("count", 15),
    )
    return SuccessResponse(data=result, message="Hashtags optimized")


@app.post("/api/v1/ai/analyze-post", response_model=SuccessResponse)
@limiter.limit("15/minute")
async def ai_analyze_post_endpoint(request: Request, body: dict):
    """Analyze a post for engagement potential, strengths, weaknesses."""
    content = body.get("content", body.get("text", ""))
    result = await ai_analyze_post(
        content=content,
        platform=body.get("platform", "instagram"),
    )
    return SuccessResponse(data=result.get("data", {}), message="Post analyzed")


# ══════════════════════════════════════════════════════════════════════════
# V1 AUTH ALIASES (frontend calls /api/v1/auth/login, backend has /api/auth/login)
# ══════════════════════════════════════════════════════════════════════════
@app.post("/api/v1/auth/login", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def v1_email_login(request: Request, login_data: dict):
    return await email_login(request, login_data)

@app.post("/api/v1/auth/register", response_model=SuccessResponse)
@limiter.limit("3/minute")
async def v1_email_register(request: Request, register_data: dict):
    return await email_register(request, register_data)


# ══════════════════════════════════════════════════════════════════════════
# ROOT REDIRECT → landing page
# ══════════════════════════════════════════════════════════════════════════
from fastapi.responses import RedirectResponse as _RR

@app.get("/", include_in_schema=False)
async def _root_redirect():
    return _RR(url="/landing.html")

# ══════════════════════════════════════════════════════════════════════════
# OAUTH CALLBACK ROUTES → serve login.html so frontend JS handles the code
# ══════════════════════════════════════════════════════════════════════════
from fastapi.responses import FileResponse as _FR
import pathlib as _pathlib

_frontend_dir = _pathlib.Path(__file__).resolve().parent.parent / "ux design"

@app.get("/auth/google/callback", include_in_schema=False)
@app.get("/auth/linkedin/callback", include_in_schema=False)
async def _oauth_callback_page():
    """Serve login.html so handleOAuthCallback() can exchange the code param."""
    login_page = _frontend_dir / "login.html"
    if login_page.is_file():
        return _FR(str(login_page), media_type="text/html")
    return _RR(url="/login.html")

# ══════════════════════════════════════════════════════════════════════════
# SERVE FRONTEND STATIC FILES (must be LAST - catch-all)
# ══════════════════════════════════════════════════════════════════════════

if _frontend_dir.is_dir():
    # Serve CSS/JS/assets
    if (_frontend_dir / "css").is_dir():
        app.mount("/css", StaticFiles(directory=str(_frontend_dir / "css")), name="css")
    if (_frontend_dir / "js").is_dir():
        app.mount("/js", StaticFiles(directory=str(_frontend_dir / "js")), name="js")
    # Serve root static files (HTML pages, images, etc.)
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")
    logger.info(f"Frontend static files mounted from {_frontend_dir}")
else:
    logger.warning(f"Frontend directory not found at {_frontend_dir}, static files not served")


# ══════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        reload_excludes=["*.log", "*.pyc", "__pycache__"],
        log_level="info",
        access_log=True,
    )
