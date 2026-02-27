"""
AssemblyAI Client for Content Analysis
Uses AssemblyAI API for text/sentiment analysis of marketing content
"""

import aiohttp
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

ASSEMBLY_AI_KEY = "4c01bda685ef4313a48e1f7f71889bf4"
BASE_URL = "https://api.assemblyai.com/v2"
HEADERS = {
    "authorization": ASSEMBLY_AI_KEY,
    "content-type": "application/json",
}


async def analyze_text(text: str) -> Dict[str, Any]:
    """
    Use AssemblyAI LeMUR to analyze marketing content text.
    Returns sentiment, key themes, and improvement suggestions.
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Use LeMUR task endpoint for text analysis
            payload = {
                "prompt": (
                    f"Analyze the following marketing content and provide:\n"
                    f"1. Overall sentiment (positive/neutral/negative)\n"
                    f"2. Key themes (list of 3-5 keywords)\n"
                    f"3. Engagement prediction (low/medium/high)\n"
                    f"4. One improvement suggestion\n\n"
                    f"Content: {text}\n\n"
                    f"Respond in JSON format with keys: sentiment, themes, engagement, suggestion"
                ),
                "final_model": "default",
            }
            async with session.post(
                f"{BASE_URL}/lemur/v3/generate/task",
                json=payload,
                headers=HEADERS,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "success": True,
                        "analysis": data.get("response", ""),
                        "request_id": data.get("request_id", ""),
                    }
                else:
                    error_text = await resp.text()
                    logger.warning(f"AssemblyAI returned {resp.status}: {error_text}")
                    return {
                        "success": False,
                        "error": f"AssemblyAI API error: {resp.status}",
                        "fallback": _fallback_analysis(text),
                    }
    except Exception as e:
        logger.error(f"AssemblyAI request failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "fallback": _fallback_analysis(text),
        }


async def transcribe_audio(audio_url: str) -> Dict[str, Any]:
    """
    Transcribe audio from URL using AssemblyAI.
    Useful for analyzing voice-based marketing content.
    """
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "audio_url": audio_url,
                "sentiment_analysis": True,
                "entity_detection": True,
                "auto_highlights": True,
            }
            async with session.post(
                f"{BASE_URL}/transcript",
                json=payload,
                headers=HEADERS,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {"success": True, "transcript_id": data.get("id"), "status": data.get("status")}
                else:
                    return {"success": False, "error": f"Status {resp.status}"}
    except Exception as e:
        logger.error(f"AssemblyAI transcribe failed: {e}")
        return {"success": False, "error": str(e)}


async def get_transcript(transcript_id: str) -> Dict[str, Any]:
    """Poll for transcript result."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}/transcript/{transcript_id}",
                headers=HEADERS,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "success": True,
                        "status": data.get("status"),
                        "text": data.get("text"),
                        "sentiment_analysis_results": data.get("sentiment_analysis_results"),
                        "auto_highlights_result": data.get("auto_highlights_result"),
                    }
                else:
                    return {"success": False, "error": f"Status {resp.status}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _fallback_analysis(text: str) -> Dict[str, Any]:
    """Simple fallback analysis when API is unavailable."""
    word_count = len(text.split())
    has_question = "?" in text
    has_emoji = any(ord(c) > 127 for c in text)
    has_cta = any(w in text.lower() for w in ["click", "buy", "sign up", "subscribe", "link", "shop"])

    engagement = "high" if (has_question and has_emoji) else "medium" if (has_question or has_emoji) else "low"

    return {
        "sentiment": "positive" if has_emoji else "neutral",
        "themes": ["marketing", "content"],
        "engagement": engagement,
        "suggestion": "Add a question to boost engagement" if not has_question else "Great use of questions!",
        "word_count": word_count,
        "has_cta": has_cta,
    }


async def health_check() -> Dict[str, Any]:
    """Check AssemblyAI connectivity."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}/transcript",
                headers=HEADERS,
                timeout=aiohttp.ClientTimeout(total=5),
            ) as resp:
                return {
                    "status": "healthy" if resp.status in (200, 401, 422) else "unhealthy",
                    "api_key_configured": bool(ASSEMBLY_AI_KEY),
                    "status_code": resp.status,
                }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
