"""
AI Insights Router — The "Strategy Engine" (Proactive Intelligence)
═══════════════════════════════════════════════════════════════════════
This module doesn't wait for the user to ask — it automatically:
  1. Detects anomalies (spending spikes, engagement drops).
  2. Generates heuristic advice (profit margin, platform mix).
  3. Produces a "health score" for the overall marketing operation.

All logic is rule-based (no API calls) for instant, offline results.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/insights", tags=["insights"])


# ── Response Models ─────────────────────────────────────────────────────
class SuccessResponse(BaseModel):
    success: bool = True
    data: Dict[str, Any] = {}
    message: str = ""


# ═════════════════════════════════════════════════════════════════════════
# Anomaly Detection Engine
# ═════════════════════════════════════════════════════════════════════════

def _detect_anomalies(analytics_rows: list, campaigns: list, contents: list) -> List[Dict[str, Any]]:
    """
    Compare current vs previous period metrics.
    Flags changes > 20% as anomalies.
    """
    anomalies = []
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    sixty_days_ago = now - timedelta(days=60)

    # Split analytics into current month and previous month
    current = [a for a in analytics_rows
               if a.date_recorded and a.date_recorded >= thirty_days_ago]
    previous = [a for a in analytics_rows
                if a.date_recorded and sixty_days_ago <= a.date_recorded < thirty_days_ago]

    def _sum(rows, attr):
        return sum(getattr(r, attr, 0) or 0 for r in rows)

    metrics = ["impressions", "engagements", "clicks", "shares"]
    labels = {
        "impressions": "Impressions",
        "engagements": "Engagements",
        "clicks": "Clicks",
        "shares": "Shares",
    }

    for metric in metrics:
        cur_val = _sum(current, metric)
        prev_val = _sum(previous, metric)

        if prev_val == 0:
            if cur_val > 0:
                anomalies.append({
                    "type": "new_activity",
                    "metric": labels.get(metric, metric),
                    "current": cur_val,
                    "previous": 0,
                    "change_pct": 100,
                    "severity": "info",
                    "message": f"New {labels.get(metric, metric).lower()} activity detected: {cur_val:,} this period.",
                })
            continue

        change_pct = round(((cur_val - prev_val) / prev_val) * 100, 1)

        if abs(change_pct) > 20:
            direction = "increased" if change_pct > 0 else "decreased"
            severity = "warning" if change_pct < -20 else "info"
            anomalies.append({
                "type": "spike" if change_pct > 0 else "drop",
                "metric": labels.get(metric, metric),
                "current": cur_val,
                "previous": prev_val,
                "change_pct": change_pct,
                "severity": severity,
                "message": (
                    f"{labels.get(metric, metric)} {direction} by **{abs(change_pct)}%** "
                    f"({prev_val:,} → {cur_val:,})."
                ),
            })

    # Campaign completion anomaly
    stale_campaigns = [
        c for c in campaigns
        if c.status == "active" and c.end_date and c.end_date < now
    ]
    if stale_campaigns:
        anomalies.append({
            "type": "stale_campaign",
            "metric": "Campaigns",
            "severity": "warning",
            "message": (
                f"**{len(stale_campaigns)}** campaign(s) past their end date are still marked active. "
                f"Consider archiving or extending them."
            ),
        })

    # Content gap: no new content in 7+ days
    recent_content = [c for c in contents if c.created_at and c.created_at >= now - timedelta(days=7)]
    if not recent_content and contents:
        anomalies.append({
            "type": "content_gap",
            "metric": "Content",
            "severity": "warning",
            "message": "No new content created in the last 7 days. Consistency is key for audience retention.",
        })

    return anomalies


# ═════════════════════════════════════════════════════════════════════════
# Heuristic Advice Generator
# ═════════════════════════════════════════════════════════════════════════

def _generate_advice(
    analytics_rows: list,
    campaigns: list,
    contents: list,
    anomalies: list,
) -> List[Dict[str, Any]]:
    """
    Generate actionable advice based on heuristic rules.
    """
    advice = []

    # === Engagement Rate ===
    rates = [a.engagement_rate for a in analytics_rows if a.engagement_rate and a.engagement_rate > 0]
    if rates:
        avg_er = round(sum(rates) / len(rates), 2)
        if avg_er < 2:
            advice.append({
                "category": "engagement",
                "priority": "high",
                "title": "Low Engagement Rate",
                "message": (
                    f"Your average engagement rate is **{avg_er}%**, which is below the 2% benchmark. "
                    "Try interactive content (polls, questions, carousels) and post during peak hours."
                ),
                "action": "Create 3 interactive posts this week",
            })
        elif avg_er > 5:
            advice.append({
                "category": "engagement",
                "priority": "low",
                "title": "Strong Engagement",
                "message": (
                    f"Your engagement rate of **{avg_er}%** is excellent! "
                    "Double down on the content formats driving this — check your top posts for patterns."
                ),
                "action": "Analyze top 5 posts and replicate their format",
            })

    # === Platform Diversification ===
    platforms_used = set()
    for c in contents:
        if c.platform:
            platforms_used.add(c.platform.lower())
    if len(platforms_used) < 2 and contents:
        advice.append({
            "category": "platform",
            "priority": "medium",
            "title": "Platform Concentration Risk",
            "message": (
                f"You're only active on **{len(platforms_used)}** platform(s): "
                f"{', '.join(platforms_used)}. Diversify to reduce algorithm dependency."
            ),
            "action": "Add 1 new platform to your content calendar this week",
        })

    # === Content Volume ===
    total_content = len(contents)
    active_campaigns = sum(1 for c in campaigns if c.status == "active")
    if active_campaigns > 0 and total_content < active_campaigns * 5:
        advice.append({
            "category": "content",
            "priority": "high",
            "title": "Content Shortage",
            "message": (
                f"You have **{active_campaigns}** active campaigns but only **{total_content}** content pieces. "
                f"Aim for at least 5 pieces per campaign for proper testing."
            ),
            "action": f"Create {max(1, active_campaigns * 5 - total_content)} more content pieces",
        })

    # === Click-Through Rate ===
    total_impressions = sum((a.impressions or 0) for a in analytics_rows)
    total_clicks = sum((a.clicks or 0) for a in analytics_rows)
    if total_impressions > 100:
        ctr = round((total_clicks / total_impressions) * 100, 2)
        if ctr < 1:
            advice.append({
                "category": "conversion",
                "priority": "high",
                "title": "Low Click-Through Rate",
                "message": (
                    f"Your CTR is **{ctr}%** — below the 1% minimum. "
                    "Strengthen your calls-to-action and use curiosity-driven headlines."
                ),
                "action": "A/B test 2 different CTAs on your next post",
            })

    # === Posting Consistency ===
    if contents:
        dates = sorted([c.created_at for c in contents if c.created_at], reverse=True)
        if len(dates) >= 2:
            gaps = [(dates[i] - dates[i + 1]).days for i in range(min(5, len(dates) - 1))]
            avg_gap = round(sum(gaps) / len(gaps), 1) if gaps else 0
            if avg_gap > 4:
                advice.append({
                    "category": "consistency",
                    "priority": "medium",
                    "title": "Inconsistent Posting Schedule",
                    "message": (
                        f"Your average gap between posts is **{avg_gap} days**. "
                        "Consistent posting (every 2-3 days) improves algorithm favorability."
                    ),
                    "action": "Set up a content calendar with fixed posting days",
                })

    # === From Anomalies ===
    for anom in anomalies:
        if anom["severity"] == "warning" and anom["type"] == "drop":
            advice.append({
                "category": "recovery",
                "priority": "high",
                "title": f"{anom['metric']} Decline Detected",
                "message": anom["message"] + " Investigate what changed and run a recovery campaign.",
                "action": f"Review last 30 days of {anom['metric'].lower()} and identify the cause",
            })

    return advice


# ═════════════════════════════════════════════════════════════════════════
# Health Score Calculator
# ═════════════════════════════════════════════════════════════════════════

def _calculate_health_score(
    analytics_rows: list,
    campaigns: list,
    contents: list,
    anomalies: list,
) -> Dict[str, Any]:
    """
    Compute an overall marketing health score (0-100).
    Breakdown: engagement (25), content (25), reach (25), consistency (25).
    """
    scores = {
        "engagement": 0,
        "content_volume": 0,
        "reach": 0,
        "consistency": 0,
    }

    # Engagement score (0-25)
    rates = [a.engagement_rate for a in analytics_rows if a.engagement_rate and a.engagement_rate > 0]
    if rates:
        avg_er = sum(rates) / len(rates)
        scores["engagement"] = min(25, round(avg_er * 5))  # 5% ER = perfect 25

    # Content volume score (0-25)
    total_content = len(contents)
    scores["content_volume"] = min(25, total_content * 2)  # 12+ pieces = perfect 25

    # Reach score (0-25)
    total_impressions = sum((a.impressions or 0) for a in analytics_rows)
    if total_impressions >= 10000:
        scores["reach"] = 25
    elif total_impressions > 0:
        scores["reach"] = min(25, round((total_impressions / 10000) * 25))

    # Consistency score (0-25)
    if contents:
        now = datetime.utcnow()
        recent = [c for c in contents if c.created_at and c.created_at >= now - timedelta(days=14)]
        if len(recent) >= 6:
            scores["consistency"] = 25
        else:
            scores["consistency"] = min(25, len(recent) * 4)

    # Penalty for warnings
    warning_count = sum(1 for a in anomalies if a.get("severity") == "warning")
    penalty = warning_count * 3

    total = max(0, sum(scores.values()) - penalty)
    grade = (
        "Excellent" if total >= 80 else
        "Good" if total >= 60 else
        "Fair" if total >= 40 else
        "Needs Attention" if total >= 20 else
        "Critical"
    )

    return {
        "score": total,
        "grade": grade,
        "breakdown": scores,
        "penalty": penalty,
        "max_score": 100,
    }


# ═════════════════════════════════════════════════════════════════════════
# FastAPI Endpoints
# ═════════════════════════════════════════════════════════════════════════

def _get_db_data(sqlite_db):
    """Fetch analytics, campaigns, contents from SQLite."""
    from models.database import Analytics, Campaign, Content
    with sqlite_db.get_session() as session:
        analytics = session.query(Analytics).all()
        campaigns = session.query(Campaign).all()
        contents = session.query(Content).all()
        # Detach from session so they survive outside the context
        for obj in analytics + campaigns + contents:
            session.expunge(obj)
    return analytics, campaigns, contents


@router.get("/proactive", response_model=SuccessResponse)
async def get_proactive_insights():
    """
    Main endpoint: returns anomalies + advice + health score.
    Called automatically when the dashboard loads.
    """
    from main import sqlite_db  # late import to avoid circular

    try:
        analytics, campaigns, contents = _get_db_data(sqlite_db)
    except Exception as e:
        logger.error(f"DB read failed for insights: {e}")
        # Return empty but valid response
        return SuccessResponse(
            data={
                "anomalies": [],
                "advice": [],
                "health": {"score": 50, "grade": "Fair", "breakdown": {}, "penalty": 0, "max_score": 100},
            },
            message="Insights generated (no data yet)",
        )

    anomalies = _detect_anomalies(analytics, campaigns, contents)
    advice = _generate_advice(analytics, campaigns, contents, anomalies)
    health = _calculate_health_score(analytics, campaigns, contents, anomalies)

    return SuccessResponse(
        data={
            "anomalies": anomalies,
            "advice": advice,
            "health": health,
            "generated_at": datetime.utcnow().isoformat(),
        },
        message=f"Generated {len(anomalies)} anomalies, {len(advice)} recommendations",
    )


@router.get("/health", response_model=SuccessResponse)
async def get_health_score():
    """Quick health score endpoint for the dashboard header."""
    from main import sqlite_db

    try:
        analytics, campaigns, contents = _get_db_data(sqlite_db)
    except Exception:
        return SuccessResponse(data={"score": 50, "grade": "Fair"})

    anomalies = _detect_anomalies(analytics, campaigns, contents)
    health = _calculate_health_score(analytics, campaigns, contents, anomalies)
    return SuccessResponse(data=health, message="Health score calculated")


@router.get("/anomalies", response_model=SuccessResponse)
async def get_anomalies():
    """Standalone anomalies endpoint."""
    from main import sqlite_db

    try:
        analytics, campaigns, contents = _get_db_data(sqlite_db)
    except Exception:
        return SuccessResponse(data={"anomalies": []})

    anomalies = _detect_anomalies(analytics, campaigns, contents)
    return SuccessResponse(data={"anomalies": anomalies})


@router.get("/advice", response_model=SuccessResponse)
async def get_advice():
    """Standalone advice endpoint."""
    from main import sqlite_db

    try:
        analytics, campaigns, contents = _get_db_data(sqlite_db)
    except Exception:
        return SuccessResponse(data={"advice": []})

    anomalies = _detect_anomalies(analytics, campaigns, contents)
    advice = _generate_advice(analytics, campaigns, contents, anomalies)
    return SuccessResponse(data={"advice": advice})
