"""
AI Chat Service — The "Conversational Brain" (AI Strategist)
═══════════════════════════════════════════════════════════════
Hybrid Architecture:
  1. Primary  → Google Gemini 2.5-flash  (contextual RAG-lite)
  2. Fallback → Rule-Based Regex Engine  (keyword matching + DB lookup)

The service NEVER sends a bare user question to the LLM.
It always wraps it with live business context from the database,
producing a "RAG-lite" prompt that prevents hallucinated numbers.
"""

import re
import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# ── Gemini SDK (optional — graceful degradation) ────────────────────────
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

# ── Gemini Configuration ───────────────────────────────────────────────
GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    os.getenv("GOOGLE_API_KEY", ""),
)

_gemini_model = None

def _get_gemini():
    """Lazy-init Gemini so import never crashes."""
    global _gemini_model
    if _gemini_model is not None:
        return _gemini_model
    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        _gemini_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1024,
            ),
        )
        logger.info("Gemini model initialised for AI Chat")
        return _gemini_model
    except Exception as e:
        logger.warning(f"Gemini init failed, falling back to rules: {e}")
        return None


# ═════════════════════════════════════════════════════════════════════════
# Business Context Builder  — fetches live stats from SQLite
# ═════════════════════════════════════════════════════════════════════════

def build_business_context(db_session) -> Dict[str, Any]:
    """
    Pull key marketing metrics from the database and return a dict
    that can be injected into the Gemini system prompt.
    """
    from models.database import Campaign, Content, Analytics, Business, Message

    ctx: Dict[str, Any] = {
        "total_campaigns": 0,
        "active_campaigns": 0,
        "total_content": 0,
        "published_content": 0,
        "total_impressions": 0,
        "total_engagements": 0,
        "total_clicks": 0,
        "avg_engagement_rate": 0.0,
        "top_platforms": [],
        "recent_content": [],
        "unread_messages": 0,
        "campaigns_list": [],
    }

    try:
        # Campaigns
        campaigns = db_session.query(Campaign).all()
        ctx["total_campaigns"] = len(campaigns)
        ctx["active_campaigns"] = sum(1 for c in campaigns if c.status == "active")
        ctx["campaigns_list"] = [
            {"name": c.name, "status": c.status, "platforms": c.target_platforms}
            for c in campaigns[:5]
        ]

        # Content
        contents = db_session.query(Content).all()
        ctx["total_content"] = len(contents)
        ctx["published_content"] = sum(1 for c in contents if c.is_published)
        ctx["recent_content"] = [
            {"title": c.title, "platform": c.platform, "status": c.status,
             "engagements": c.engagements, "impressions": c.impressions}
            for c in sorted(contents, key=lambda x: x.created_at or datetime.min, reverse=True)[:5]
        ]

        # Analytics aggregation
        analytics = db_session.query(Analytics).all()
        if analytics:
            ctx["total_impressions"] = sum(a.impressions or 0 for a in analytics)
            ctx["total_engagements"] = sum(a.engagements or 0 for a in analytics)
            ctx["total_clicks"] = sum(a.clicks or 0 for a in analytics)
            rates = [a.engagement_rate for a in analytics if a.engagement_rate]
            ctx["avg_engagement_rate"] = round(sum(rates) / len(rates), 2) if rates else 0.0

            # Top platforms by engagement
            plat_eng: Dict[str, int] = {}
            for a in analytics:
                if a.platform:
                    plat_eng[a.platform] = plat_eng.get(a.platform, 0) + (a.engagements or 0)
            ctx["top_platforms"] = sorted(plat_eng.items(), key=lambda x: x[1], reverse=True)[:3]

        # Messages
        ctx["unread_messages"] = db_session.query(Message).filter(
            Message.is_read == False
        ).count()

    except Exception as e:
        logger.warning(f"Context build partial failure: {e}")

    return ctx


def _context_to_text(ctx: Dict[str, Any]) -> str:
    """Format the context dict into a readable block for the LLM."""
    lines = [
        "=== LIVE BUSINESS DATA ===",
        f"Campaigns: {ctx['total_campaigns']} total, {ctx['active_campaigns']} active",
        f"Content: {ctx['total_content']} pieces, {ctx['published_content']} published",
        f"Impressions: {ctx['total_impressions']:,}",
        f"Engagements: {ctx['total_engagements']:,}",
        f"Clicks: {ctx['total_clicks']:,}",
        f"Avg Engagement Rate: {ctx['avg_engagement_rate']}%",
        f"Top Platforms: {', '.join(p[0] + ' (' + str(p[1]) + ')' for p in ctx['top_platforms']) or 'N/A'}",
        f"Unread Messages: {ctx['unread_messages']}",
    ]
    if ctx["campaigns_list"]:
        lines.append("Recent Campaigns:")
        for c in ctx["campaigns_list"]:
            lines.append(f"  • {c['name']} [{c['status']}] on {', '.join(c.get('platforms') or ['—'])}")
    if ctx["recent_content"]:
        lines.append("Recent Content:")
        for c in ctx["recent_content"]:
            lines.append(f"  • {c['title']} ({c['platform']}) — {c['impressions']} imp, {c['engagements']} eng")
    return "\n".join(lines)


# ═════════════════════════════════════════════════════════════════════════
# Gemini Chat  (Primary Path)
# ═════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = (
    "You are a world-class AI marketing strategist embedded in the AI Marketing "
    "Command Center. You have access to the user's real-time business data "
    "(provided below). Answer questions with specific, data-backed advice.\n"
    "Rules:\n"
    "1. Reference the ACTUAL numbers from the data — never invent figures.\n"
    "2. Keep answers concise (3-5 paragraphs max).\n"
    "3. When suggesting actions, be specific: platform, timing, content type.\n"
    "4. If the data is insufficient, say so and suggest what to track.\n"
    "5. Format with markdown: bold key numbers, use bullet lists.\n\n"
)


async def _ask_gemini(question: str, context_text: str) -> str:
    """Send the question + context to Gemini and return the answer."""
    model = _get_gemini()
    if model is None:
        raise RuntimeError("Gemini unavailable")

    full_prompt = (
        SYSTEM_PROMPT
        + context_text
        + "\n\n=== USER QUESTION ===\n"
        + question
    )

    # Run in executor since the SDK is synchronous
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, lambda: model.generate_content(full_prompt)
    )
    return response.text


# ═════════════════════════════════════════════════════════════════════════
# Rule-Based Fallback Engine  (offline / no-API-key path)
# ═════════════════════════════════════════════════════════════════════════

# Pattern → handler mapping
_RULE_PATTERNS: List[tuple] = []

def _rule(pattern: str):
    """Decorator to register a regex rule."""
    def decorator(fn):
        _RULE_PATTERNS.append((re.compile(pattern, re.IGNORECASE), fn))
        return fn
    return decorator


@_rule(r"(how many|total|count).*(campaign|campaigns)")
def _rule_campaign_count(ctx, match):
    return (
        f"You have **{ctx['total_campaigns']}** campaigns in total, "
        f"of which **{ctx['active_campaigns']}** are currently active."
    )


@_rule(r"(engagement|engagement rate|er)")
def _rule_engagement(ctx, match):
    return (
        f"Your average engagement rate is **{ctx['avg_engagement_rate']}%**. "
        f"Total engagements across all content: **{ctx['total_engagements']:,}**."
    )


@_rule(r"(impression|impressions|reach)")
def _rule_impressions(ctx, match):
    return (
        f"Your total impressions are **{ctx['total_impressions']:,}** "
        f"with **{ctx['total_clicks']:,}** clicks."
    )


@_rule(r"(content|posts|published)")
def _rule_content(ctx, match):
    recent = ""
    if ctx["recent_content"]:
        items = [f"• {c['title']} ({c['platform']})" for c in ctx["recent_content"][:3]]
        recent = "\n\nRecent content:\n" + "\n".join(items)
    return (
        f"You have **{ctx['total_content']}** content pieces, "
        f"**{ctx['published_content']}** published.{recent}"
    )


@_rule(r"(platform|best platform|top platform|where should)")
def _rule_platforms(ctx, match):
    if ctx["top_platforms"]:
        ranked = ", ".join(f"**{p[0]}** ({p[1]} engagements)" for p in ctx["top_platforms"])
        return f"Your top platforms by engagement: {ranked}."
    return "No platform analytics data yet. Start posting and check back!"


@_rule(r"(message|inbox|unread)")
def _rule_messages(ctx, match):
    return f"You have **{ctx['unread_messages']}** unread messages in your inbox."


@_rule(r"(click|ctr|click.?through)")
def _rule_clicks(ctx, match):
    ctr = 0
    if ctx["total_impressions"] > 0:
        ctr = round((ctx["total_clicks"] / ctx["total_impressions"]) * 100, 2)
    return (
        f"Total clicks: **{ctx['total_clicks']:,}**. "
        f"Calculated CTR: **{ctr}%** based on {ctx['total_impressions']:,} impressions."
    )


@_rule(r"(suggest|recommend|what should|advice|improve|tip)")
def _rule_advice(ctx, match):
    tips = []
    if ctx["avg_engagement_rate"] < 3:
        tips.append("Your engagement rate is below 3%. Try using more video/reel content and interactive polls.")
    if ctx["total_content"] < 10:
        tips.append("You have fewer than 10 content pieces. Consistency is key — aim for at least 3 posts per week.")
    if not ctx["top_platforms"]:
        tips.append("Start tracking platform-specific analytics to identify where your audience is most active.")
    if ctx["unread_messages"] > 5:
        tips.append(f"You have {ctx['unread_messages']} unread messages. Quick responses boost customer trust.")
    if not tips:
        tips.append("Your metrics look solid! Focus on A/B testing content formats to find what resonates most.")
    return "**AI Recommendations:**\n" + "\n".join(f"• {t}" for t in tips)


@_rule(r"(hello|hi|hey|help)")
def _rule_greeting(ctx, match):
    return (
        "Hello! I'm your AI Marketing Strategist. I can help you with:\n"
        "• Campaign performance analysis\n"
        "• Content strategy recommendations\n"
        "• Platform engagement insights\n"
        "• Click-through rate analysis\n"
        "Ask me anything about your marketing data!"
    )


def _fallback_answer(question: str, ctx: Dict[str, Any]) -> str:
    """Run through rule patterns and return the first match."""
    for pattern, handler in _RULE_PATTERNS:
        m = pattern.search(question)
        if m:
            return handler(ctx, m)
    # No pattern matched — generic summary
    return (
        f"Here's a quick summary of your marketing data:\n"
        f"• **{ctx['total_campaigns']}** campaigns ({ctx['active_campaigns']} active)\n"
        f"• **{ctx['total_content']}** content pieces ({ctx['published_content']} published)\n"
        f"• **{ctx['total_impressions']:,}** impressions, **{ctx['total_engagements']:,}** engagements\n"
        f"• Avg engagement rate: **{ctx['avg_engagement_rate']}%**\n\n"
        f"Try asking something more specific like:\n"
        f"• \"What's my engagement rate?\"\n"
        f"• \"Which platform performs best?\"\n"
        f"• \"Give me tips to improve.\""
    )


# ═════════════════════════════════════════════════════════════════════════
# Public API  — one function to rule them all
# ═════════════════════════════════════════════════════════════════════════

async def chat(question: str, db_session) -> Dict[str, Any]:
    """
    Main entry point.
    1. Build context from the database.
    2. Try Gemini (primary).
    3. Fall back to rule engine on any failure.
    Returns: { answer: str, source: "gemini"|"rules", context: dict }
    """
    ctx = build_business_context(db_session)
    context_text = _context_to_text(ctx)

    # ── Primary: Gemini ───────────────────────────────────────────────
    try:
        answer = await _ask_gemini(question, context_text)
        return {"answer": answer, "source": "gemini", "context_summary": ctx}
    except Exception as e:
        logger.info(f"Gemini unavailable ({e}), using rule fallback")

    # ── Fallback: Rule-based ──────────────────────────────────────────
    answer = _fallback_answer(question, ctx)
    return {"answer": answer, "source": "rules", "context_summary": ctx}
