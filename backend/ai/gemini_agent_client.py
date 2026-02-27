"""
Gemini AI Agent Client – connects the main backend to the agent service on port 8004.
Uses aiohttp for async HTTP.  No LangChain, no SerpAPI.
"""
import aiohttp, logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

AGENT_URL = "http://localhost:8004"
TIMEOUT   = aiohttp.ClientTimeout(total=30)


async def _post(path: str, payload: dict) -> dict:
    """POST to the agent service and return JSON."""
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as s:
            async with s.post(f"{AGENT_URL}{path}", json=payload) as r:
                if r.status == 200:
                    return await r.json()
                return {"success": False, "answer": f"Agent HTTP {r.status}"}
    except Exception as e:
        logger.warning(f"Agent call to {path} failed: {e}")
        return {"success": False, "answer": str(e)}


async def _get(path: str) -> dict:
    """GET from the agent service."""
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as s:
            async with s.get(f"{AGENT_URL}{path}") as r:
                if r.status == 200:
                    return await r.json()
                return {"status": "error"}
    except Exception as e:
        logger.warning(f"Agent GET {path} failed: {e}")
        return {"status": "error"}


# ── Public helpers used by routes/agent.py ─────────────────────────

async def is_available() -> bool:
    data = await _get("/health")
    return data.get("status") == "healthy"


async def ask(question: str, context: Optional[str] = None) -> Dict[str, Any]:
    payload: dict = {"question": question}
    if context:
        payload["context"] = context
    return await _post("/ask", payload)


async def marketing_insights(question: str, context: Optional[str] = None) -> Dict[str, Any]:
    payload: dict = {"question": question}
    if context:
        payload["context"] = context
    return await _post("/marketing-insights", payload)


async def campaign_advice(campaign_type: str, **kwargs) -> Dict[str, Any]:
    payload: dict = {"campaign_type": campaign_type}
    for k in ("target_audience", "budget", "goals", "context"):
        if kwargs.get(k):
            payload[k] = kwargs[k]
    return await _post("/campaign-advice", payload)


async def enhance_content(content: str, content_type: str = "social_post") -> Dict[str, Any]:
    return await _post("/enhance-content", {"content": content, "content_type": content_type})


async def generate_hashtags(content: str, count: int = 10) -> Dict[str, Any]:
    return await _post("/generate-hashtags", {"content": content, "count": count})


async def content_ideas(topic: str, count: int = 5) -> Dict[str, Any]:
    return await _post("/content-ideas", {"topic": topic, "count": count})


async def generate_strategy(
    business_name: str = "My Business",
    industry: str = "technology",
    target_audience: str = "General audience",
    brand_voice: str = "professional",
    campaign_goal: str = "Increase brand awareness",
    duration_days: int = 30,
    platforms: List[str] = None,
    budget: Optional[str] = None,
) -> Dict[str, Any]:
    return await _post("/generate-strategy", {
        "business_name": business_name,
        "industry": industry,
        "target_audience": target_audience,
        "brand_voice": brand_voice,
        "campaign_goal": campaign_goal,
        "duration_days": duration_days,
        "platforms": platforms or ["instagram", "linkedin"],
        "budget": budget,
    })
