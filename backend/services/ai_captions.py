"""
AI Caption Generator — Trend-Aware, Platform-Optimized
═══════════════════════════════════════════════════════════
Uses Gemini 2.5-flash to analyze post content and generate:
  • Platform-optimized captions (Instagram, Facebook)
  • Trending hashtags for the current moment
  • Engagement insights & post tips
  • Multiple caption variations (formal, casual, viral)

The AI is instructed to act as a 2026 social-media strategist
who tracks current trends, viral formats, and algorithm changes.
"""

import os
import re
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

# ── Gemini SDK ──────────────────────────────────────────────────────────
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    os.getenv("GOOGLE_API_KEY", "AIzaSyCczWxiW2Shg9D-xTQYeTyYAWyLOkkbkbs"),
)

_model = None

def _get_model():
    global _model
    if _model is not None:
        return _model
    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.85,
                top_p=0.92,
                max_output_tokens=2048,
            ),
        )
        return _model
    except Exception as e:
        logger.error(f"Gemini init failed: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT — trend-aware social media strategist
# ═══════════════════════════════════════════════════════════════════════

CAPTION_SYSTEM_PROMPT = """You are an elite social-media strategist in {year}.
You know every trending format, viral hook, and algorithm trick across
Instagram, Facebook, TikTok, LinkedIn, and X/Twitter.

Your job: analyze the user's post content (text, description of image,
or topic) and produce OUTSTANDING platform-optimized captions.

CURRENT CONTEXT:
• Date:  {date}
• Platform(s): {platforms}
• Tone: {tone}
• Industry/Niche: {niche}

RULES:
1. Follow the LATEST trends for {year} — hook-first writing, micro-stories,
   carousel-style captions, engagement bait that ACTUALLY works.
2. Hashtags must be CURRENTLY trending or evergreen power-tags for the niche.
   Mix 3-5 high-volume + 3-5 niche-specific tags.
3. Start with an attention hook (emoji-first, question, bold statement).
4. Include a clear CTA (save, share, comment, link in bio, etc.).
5. For Instagram: use line breaks, emojis strategically, up to 2200 chars.
   For Facebook: natural conversational tone, can include links.
6. Provide 3 caption variations: Formal, Casual, Viral-Bait.
7. Also provide: engagement_tips (list of 3), best_posting_time, and
   a one-line content_insight about why this post can perform well.

Return a **valid JSON** object with this exact structure:
{{
  "captions": [
    {{"style": "formal", "text": "..."}},
    {{"style": "casual", "text": "..."}},
    {{"style": "viral", "text": "..."}}
  ],
  "hashtags": ["#tag1", "#tag2", ...],
  "engagement_tips": ["tip1", "tip2", "tip3"],
  "best_posting_time": "e.g. Tuesday 6-8 PM EST",
  "content_insight": "one-line insight about the post's potential",
  "trending_hooks": ["hook1", "hook2"]
}}

IMPORTANT: Return ONLY the JSON object, no markdown fences, no extra text.
"""


# ═══════════════════════════════════════════════════════════════════════
# MAIN — generate_captions()
# ═══════════════════════════════════════════════════════════════════════

async def generate_captions(
    content: str,
    platforms: List[str] = None,
    tone: str = "engaging",
    niche: str = "general marketing",
    image_description: str = "",
) -> Dict[str, Any]:
    """
    Generate AI captions, hashtags, insights for a post.
    Uses Gemini first, falls back to rule-based generation.
    """
    platforms = platforms or ["instagram", "facebook"]
    now = datetime.now()

    # Build the prompt
    user_message = f"POST CONTENT:\n{content}"
    if image_description:
        user_message += f"\n\nIMAGE DESCRIPTION:\n{image_description}"

    system = CAPTION_SYSTEM_PROMPT.format(
        year=now.year,
        date=now.strftime("%B %d, %Y"),
        platforms=", ".join(platforms),
        tone=tone,
        niche=niche,
    )

    # Try Gemini
    model = _get_model()
    if model:
        try:
            result = await _ai_generate(model, system, user_message)
            if result:
                result["source"] = "gemini"
                result["platform_targets"] = platforms
                return {"success": True, "data": result}
        except Exception as e:
            logger.warning(f"Gemini caption generation failed: {e}")

    # Fallback: rule-based
    fallback = _fallback_captions(content, platforms, tone, niche)
    fallback["source"] = "rules"
    fallback["platform_targets"] = platforms
    return {"success": True, "data": fallback}


async def _ai_generate(model, system: str, user_msg: str) -> Optional[Dict]:
    """Call Gemini and parse JSON response."""
    full_prompt = f"{system}\n\n{user_msg}"

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, lambda: model.generate_content(full_prompt)
    )
    text = response.text.strip()

    # Strip markdown fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    parsed = json.loads(text)

    # Validate structure
    if "captions" not in parsed:
        raise ValueError("Missing 'captions' in response")

    return parsed


# ═══════════════════════════════════════════════════════════════════════
# FALLBACK — rule-based caption generator
# ═══════════════════════════════════════════════════════════════════════

_HOOKS = [
    "🚀 Stop scrolling — this changes everything.",
    "⚡ Here's what nobody tells you about {topic}...",
    "🔥 {topic} just got a whole lot more interesting.",
    "💡 The secret to {topic}? It's simpler than you think.",
    "✨ POV: You just discovered the best {topic} hack of 2026.",
    "📢 Attention {niche} community — big update!",
]

_CTAS = [
    "💬 Drop your thoughts below!",
    "🔖 Save this for later — you'll thank yourself.",
    "📲 Share with someone who needs to see this!",
    "👉 Link in bio for more.",
    "❤️ Double-tap if you agree!",
    "🔄 Repost to spread the word.",
]

_TRENDING_TAGS_2026 = {
    "general marketing": ["#Marketing2026", "#DigitalMarketing", "#GrowthHacking", "#ContentStrategy", "#MarketingTips", "#SocialMediaTrends", "#BrandBuilding", "#MarketingHacks"],
    "technology": ["#TechTrends", "#AI", "#Innovation", "#FutureTech", "#StartupLife", "#TechNews", "#DigitalTransformation", "#AIpowered"],
    "fashion": ["#FashionTrends2026", "#OOTD", "#StyleInspo", "#FashionForward", "#StreetStyle", "#SustainableFashion", "#FashionBlogger"],
    "food": ["#FoodTrends2026", "#Foodie", "#RecipeOfTheDay", "#HealthyEating", "#FoodPhotography", "#Instafood", "#Homemade"],
    "fitness": ["#FitnessMotivation", "#Workout", "#FitLife", "#HealthyLifestyle", "#GymTok", "#FitnessJourney", "#ActiveLiving"],
    "business": ["#Entrepreneurship", "#BusinessGrowth", "#StartupLife", "#Leadership", "#Success", "#BusinessTips", "#SmallBusiness"],
    "default": ["#Trending", "#ViralContent", "#MustSee", "#ForYou", "#Explore", "#ContentCreator", "#2026Trends"],
}


def _fallback_captions(content: str, platforms: list, tone: str, niche: str) -> Dict:
    """Generate three caption variations using templates + trending tags."""
    topic = content[:60].strip().rstrip(".")
    safe_niche = niche.lower().strip()

    # Pick hashtags
    tags = _TRENDING_TAGS_2026.get(safe_niche, _TRENDING_TAGS_2026["default"])
    # Add content-derived tags
    words = re.findall(r"[A-Za-z]{4,}", content)
    extra_tags = [f"#{w.capitalize()}" for w in set(words[:3])]
    all_tags = list(dict.fromkeys(tags + extra_tags))[:12]

    # Pick hooks
    import random
    hook = random.choice(_HOOKS).replace("{topic}", topic).replace("{niche}", niche)
    cta = random.choice(_CTAS)

    # Three variations
    formal = f"{hook}\n\n{content}\n\nStay ahead of the curve — excellence starts with smart strategy.\n\n{cta}\n\n{' '.join(all_tags[:8])}"
    casual = f"{hook}\n\n{content}\n\nHonestly? This is a game-changer. 🔥\n\n{cta}\n\n{' '.join(all_tags[:8])}"
    viral = f"{hook}\n\nYou're NOT ready for this 👇\n\n{content}\n\nIf this doesn't blow your mind, nothing will. 🤯\n\n{cta}\n\n{' '.join(all_tags[:8])}"

    return {
        "captions": [
            {"style": "formal", "text": formal},
            {"style": "casual", "text": casual},
            {"style": "viral", "text": viral},
        ],
        "hashtags": all_tags,
        "engagement_tips": [
            "Post during peak hours (6-9 PM in your audience's timezone)",
            "Reply to every comment in the first hour to boost algorithmic reach",
            f"Use carousel format on Instagram for 2-3x higher saves",
        ],
        "best_posting_time": "Tuesday/Thursday 6-8 PM",
        "content_insight": f"Posts about {topic} are trending this week — capitalize on the momentum!",
        "trending_hooks": [h.replace("{topic}", topic).replace("{niche}", niche) for h in _HOOKS[:3]],
    }


# ═══════════════════════════════════════════════════════════════════════
# HASHTAG OPTIMIZER — standalone
# ═══════════════════════════════════════════════════════════════════════

async def optimize_hashtags(
    content: str,
    platform: str = "instagram",
    niche: str = "general marketing",
    count: int = 15,
) -> Dict[str, Any]:
    """Generate optimized, trend-aware hashtags for content."""
    model = _get_model()
    if model:
        try:
            prompt = (
                f"You are a social media hashtag expert in {datetime.now().year}. "
                f"Generate {count} optimized hashtags for this {platform} post:\n\n"
                f"{content}\n\n"
                f"Niche: {niche}\n"
                f"Mix high-volume trending tags with niche-specific ones.\n"
                f"Return ONLY a JSON array of hashtag strings like [\"#tag1\", \"#tag2\"]."
            )
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
            text = resp.text.strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            tags = json.loads(text)
            if isinstance(tags, list):
                return {"success": True, "hashtags": tags[:count], "source": "gemini"}
        except Exception as e:
            logger.warning(f"Gemini hashtag generation failed: {e}")

    # Fallback
    safe_niche = niche.lower().strip()
    tags = _TRENDING_TAGS_2026.get(safe_niche, _TRENDING_TAGS_2026["default"])
    return {"success": True, "hashtags": tags[:count], "source": "rules"}


# ═══════════════════════════════════════════════════════════════════════
# CONTENT INSIGHT — analyze an existing post
# ═══════════════════════════════════════════════════════════════════════

async def analyze_post(
    content: str,
    platform: str = "instagram",
) -> Dict[str, Any]:
    """Analyze a post and provide engagement predictions + improvements."""
    model = _get_model()
    if model:
        try:
            prompt = (
                f"You are a social media analyst in {datetime.now().year}. "
                f"Analyze this {platform} post and provide actionable feedback.\n\n"
                f"POST:\n{content}\n\n"
                f"Return JSON with: "
                f'{{"score": 0-100, "strengths": [...], "weaknesses": [...], '
                f'"improved_caption": "...", "predicted_engagement": "X%", '
                f'"trending_elements": [...], "suggestions": [...]}}\n'
                f"Return ONLY valid JSON, no markdown."
            )
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
            text = resp.text.strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            analysis = json.loads(text)
            analysis["source"] = "gemini"
            return {"success": True, "data": analysis}
        except Exception as e:
            logger.warning(f"Gemini post analysis failed: {e}")

    # Fallback
    word_count = len(content.split())
    has_emoji = bool(re.search(r"[\U0001f300-\U0001f9ff]", content))
    has_hashtags = bool(re.search(r"#\w+", content))
    has_cta = bool(re.search(r"(?:comment|share|save|click|link|dm|follow)", content, re.I))

    score = 40
    strengths, weaknesses = [], []
    if has_emoji:
        score += 10; strengths.append("Uses emojis for visual appeal")
    else:
        weaknesses.append("Add emojis to catch attention in the feed")
    if has_hashtags:
        score += 10; strengths.append("Includes hashtags for discoverability")
    else:
        weaknesses.append("Add 5-10 relevant hashtags for reach")
    if has_cta:
        score += 15; strengths.append("Has a clear call-to-action")
    else:
        weaknesses.append("Add a CTA (e.g., 'Save this!', 'Comment below')")
    if 20 <= word_count <= 150:
        score += 10; strengths.append("Good caption length")
    elif word_count < 20:
        weaknesses.append("Caption is too short — aim for 30-100 words")
    else:
        weaknesses.append("Caption might be too long — consider breaking into carousel")

    return {
        "success": True,
        "data": {
            "score": min(score, 100),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improved_caption": "",
            "predicted_engagement": f"{min(score / 15, 8):.1f}%",
            "trending_elements": [],
            "suggestions": ["Add trending audio reference", "Use carousel format", "Post during peak hours"],
            "source": "rules",
        },
    }
