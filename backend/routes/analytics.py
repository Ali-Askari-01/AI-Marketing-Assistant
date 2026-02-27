"""
Analytics Routes
Implements the API contract for analytics endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import uuid

from contracts.api_contract import (
    APIContract, ErrorCode, AnalyticsResponse,
    RequestContext, ValidationRules, get_status_code
)
from core.security import security_manager, get_current_user
from models.mongo_db import content_repo
from ai.ai_service import ai_service

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])
security = HTTPBearer()

@router.get("/{business_id}", response_model=Dict[str, Any])
async def get_business_analytics(
    request: Request,
    business_id: str,
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get business analytics"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=business_id)
    
    try:
        # Parse date range
        if date_from:
            try:
                date_from_dt = datetime.fromisoformat(date_from)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=APIContract.validation_error_response("date_from", "Invalid date format")
                )
        else:
            date_from_dt = datetime.utcnow() - timedelta(days=30)
        
        if date_to:
            try:
                date_to_dt = datetime.fromisoformat(date_to)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=APIContract.validation_error_response("date_to", "Invalid date format")
                )
        else:
            date_to_dt = datetime.utcnow()
        
        # Generate mock analytics data (in production, this would be calculated from real data)
        analytics_data = {
            "health_score": 78.5,
            "engagement_rate": 4.2,
            "top_content_type": "Reel",
            "recommendations": [
                "Post more video content to increase engagement",
                "Increase CTA strength in posts",
                "Optimize posting times for better reach",
                "Focus on Instagram Stories for daily engagement"
            ],
            "period": {
                "from": date_from_dt.isoformat(),
                "to": date_to_dt.isoformat()
            },
            "metrics": {
                "total_impressions": 125000,
                "total_engagement": 5250,
                "total_clicks": 875,
                "total_conversions": 45,
                "total_posts": 25,
                "average_engagement_rate": 4.2,
                "average_ctr": 0.7,
                "conversion_rate": 3.6
            },
            "platform_performance": {
                "instagram": {
                    "impressions": 75000,
                    "engagement": 3500,
                    "engagement_rate": 4.7,
                    "clicks": 525,
                    "conversions": 28
                },
                "linkedin": {
                    "impressions": 35000,
                    "engagement": 1400,
                    "engagement_rate": 4.0,
                    "clicks": 280,
                    "conversions": 12
                },
                "email": {
                    "impressions": 15000,
                    "engagement": 350,
                    "engagement_rate": 2.3,
                    "clicks": 70,
                    "conversions": 5
                }
            },
            "content_type_performance": {
                "reel": {
                    "posts": 8,
                    "engagement_rate": 6.2,
                    "avg_engagement": 650,
                    "top_performing": True
                },
                "image": {
                    "posts": 10,
                    "engagement_rate": 3.8,
                    "avg_engagement": 380,
                    "top_performing": False
                },
                "carousel": {
                    "posts": 5,
                    "engagement_rate": 4.5,
                    "avg_engagement": 450,
                    "top_performing": False
                },
                "story": {
                    "posts": 2,
                    "engagement_rate": 5.1,
                    "avg_engagement": 255,
                    "top_performing": False
                }
            },
            "trends": {
                "daily_engagement": [
                    {"date": "2024-01-01", "engagement": 180},
                    {"date": "2024-01-02", "engagement": 195},
                    {"date": "2024-01-03", "engagement": 210},
                    {"date": "2024-01-04", "engagement": 185},
                    {"date": "2024-01-05", "engagement": 225}
                ],
                "weekly_growth": {
                    "engagement": 15.2,
                    "impressions": 8.7,
                    "conversions": 12.5
                }
            }
        }
        
        return APIContract.success_response(
            analytics_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.get("/content/{content_id}", response_model=Dict[str, Any])
async def get_content_analytics(
    request: Request,
    content_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get content analytics"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Check if content exists
        content = await content_repo.get_by_id(content_id)
        if not content:
            raise HTTPException(
                status_code=404,
                detail=APIContract.error_response(
                    ErrorCode.ANALYTICS_NOT_FOUND,
                    "Content not found"
                )
            )
        
        # Generate mock content analytics (in production, this would be real data)
        analytics_data = {
            "content_id": content_id,
            "content_type": content.get("content_type"),
            "platform": content.get("platform"),
            "published_date": content.get("published_date"),
            "metrics": {
                "impressions": 5000,
                "engagement": 210,
                "likes": 180,
                "comments": 25,
                "shares": 5,
                "clicks": 35,
                "conversions": 3,
                "engagement_rate": 4.2,
                "click_through_rate": 0.7,
                "conversion_rate": 1.4
            },
            "performance": {
                "score": 82,
                "grade": "B+",
                "vs_average": {
                    "engagement_rate": "+0.8%",
                    "click_through_rate": "+0.2%",
                    "conversion_rate": "+0.5%"
                }
            },
            "audience_demographics": {
                "age_groups": {
                    "18-24": 15,
                    "25-34": 35,
                    "35-44": 30,
                    "45-54": 15,
                    "55+": 5
                },
                "gender": {
                    "male": 45,
                    "female": 55
                },
                "locations": {
                    "United States": 40,
                    "United Kingdom": 20,
                    "Canada": 15,
                    "Australia": 10,
                    "Other": 15
                }
            },
            "time_performance": {
                "best_posting_time": "7:00 PM",
                "peak_engagement_hour": "8:00 PM",
                "engagement_by_hour": [
                    {"hour": 6, "engagement": 15},
                    {"hour": 7, "engagement": 25},
                    {"hour": 8, "engagement": 35},
                    {"hour": 9, "engagement": 20},
                    {"hour": 10, "engagement": 10}
                ]
            }
        }
        
        return APIContract.success_response(
            analytics_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.get("/campaign/{campaign_id}", response_model=Dict[str, Any])
async def get_campaign_analytics(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get campaign analytics"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Generate mock campaign analytics
        analytics_data = {
            "campaign_id": campaign_id,
            "overall_performance": {
                "health_score": 82.3,
                "total_impressions": 45000,
                "total_engagement": 1890,
                "total_conversions": 67,
                "engagement_rate": 4.2,
                "conversion_rate": 3.6
            },
            "content_performance": [
                {
                    "content_id": "content_1",
                    "title": "Morning Motivation",
                    "type": "image",
                    "engagement_rate": 5.2,
                    "conversions": 12,
                    "performance_score": 88
                },
                {
                    "content_id": "content_2",
                    "title": "Workout Tips",
                    "type": "reel",
                    "engagement_rate": 6.8,
                    "conversions": 18,
                    "performance_score": 92
                },
                {
                    "content_id": "content_3",
                    "title": "Client Success Story",
                    "type": "carousel",
                    "engagement_rate": 4.1,
                    "conversions": 8,
                    "performance_score": 76
                }
            ],
            "daily_performance": [
                {"date": "2024-01-01", "impressions": 1500, "engagement": 63, "conversions": 2},
                {"date": "2024-01-02", "impressions": 1600, "engagement": 67, "conversions": 2},
                {"date": "2024-01-03", "impressions": 1400, "engagement": 59, "conversions": 2},
                {"date": "2024-01-04", "impressions": 1700, "engagement": 71, "conversions": 3},
                {"date": "2024-01-05", "impressions": 1800, "engagement": 76, "conversions": 3}
            ],
            "platform_breakdown": {
                "instagram": {
                    "impressions": 30000,
                    "engagement": 1350,
                    "conversions": 45,
                    "engagement_rate": 4.5
                },
                "linkedin": {
                    "impressions": 12000,
                    "engagement": 480,
                    "conversions": 18,
                    "engagement_rate": 4.0
                },
                "email": {
                    "impressions": 3000,
                    "engagement": 60,
                    "conversions": 4,
                    "engagement_rate": 2.0
                }
            },
            "recommendations": [
                "Focus more on Reel content for higher engagement",
                "Optimize posting times for LinkedIn",
                "Add stronger CTAs in email campaigns",
                "Create more video content for Instagram"
            ]
        }
        
        return APIContract.success_response(
            analytics_data,
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.get("/health-score/{campaign_id}", response_model=Dict[str, Any])
async def get_health_score(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get marketing health score"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Calculate health score based on multiple factors
        health_data = {
            "campaign_id": campaign_id,
            "overall_score": 78.5,
            "score_breakdown": {
                "engagement_rate": {
                    "score": 82,
                    "weight": 0.4,
                    "contribution": 32.8,
                    "details": {
                        "current_rate": 4.2,
                        "benchmark_rate": 3.5,
                        "performance": "Above average"
                    }
                },
                "consistency_score": {
                    "score": 75,
                    "weight": 0.3,
                    "contribution": 22.5,
                    "details": {
                        "posting_frequency": "Regular",
                        "quality_consistency": "Good",
                        "brand_voice_consistency": "Excellent"
                    }
                },
                "media_diversity": {
                    "score": 85,
                    "weight": 0.2,
                    "contribution": 17.0,
                    "details": {
                        "content_types": ["image", "video", "carousel"],
                        "diversity_score": "Well balanced"
                    }
                },
                "response_time": {
                    "score": 70,
                    "weight": 0.1,
                    "contribution": 7.0,
                    "details": {
                        "average_response_time": "2.5 hours",
                        "response_rate": "85%"
                    }
                }
            },
            "grade": "B+",
            "trend": {
                "direction": "improving",
                "change": "+5.2%",
                "period": "Last 30 days"
            },
            "improvement_suggestions": [
                {
                    "area": "Response Time",
                    "suggestion": "Reduce average response time to under 2 hours",
                    "potential_impact": "+3 points",
                    "effort": "Medium"
                },
                {
                    "area": "Content Consistency",
                    "suggestion": "Maintain consistent posting schedule",
                    "potential_impact": "+2 points",
                    "effort": "Low"
                },
                {
                    "area": "Engagement Rate",
                    "suggestion": "Add more interactive elements to posts",
                    "potential_impact": "+4 points",
                    "effort": "Medium"
                }
            ],
            "historical_scores": [
                {"date": "2024-01-01", "score": 73.3},
                {"date": "2024-01-08", "score": 75.1},
                {"date": "2024-01-15", "score": 76.8},
                {"date": "2024-01-22", "score": 77.2},
                {"date": "2024-01-29", "score": 78.5}
            ]
        }
        
        return APIContract.success_response(
            health_data,
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/simulate", response_model=Dict[str, Any])
async def simulate_analytics(
    request: Request,
    simulation_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Simulate analytics data"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate simulation parameters
        days_to_simulate = simulation_data.get("days_to_simulate", 30)
        base_engagement_rate = simulation_data.get("base_engagement_rate", 0.05)
        content_count = simulation_data.get("content_count", 10)
        
        if not (1 <= days_to_simulate <= 365):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("days_to_simulate", "Days must be 1-365")
            )
        
        if not (0.0 <= base_engagement_rate <= 1.0):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("base_engagement_rate", "Rate must be 0.0-1.0")
            )
        
        # Generate simulated data
        simulated_data = {
            "simulation_id": str(uuid.uuid4()),
            "parameters": {
                "days_to_simulate": days_to_simulate,
                "base_engagement_rate": base_engagement_rate,
                "content_count": content_count
            },
            "results": {
                "total_impressions": int(content_count * 1000 * (1 + base_engagement_rate)),
                "total_engagement": int(content_count * 1000 * base_engagement_rate),
                "total_conversions": int(content_count * 1000 * base_engagement_rate * 0.03),
                "average_engagement_rate": base_engagement_rate,
                "daily_data": []
            }
        }
        
        # Generate daily data
        import random
        for day in range(days_to_simulate):
            daily_impressions = random.randint(800, 1200)
            daily_engagement = int(daily_impressions * base_engagement_rate * random.uniform(0.8, 1.2))
            daily_conversions = int(daily_engagement * 0.03 * random.uniform(0.5, 1.5))
            
            simulated_data["results"]["daily_data"].append({
                "date": (datetime.utcnow() - timedelta(days=days_to_simulate - day)).strftime("%Y-%m-%d"),
                "impressions": daily_impressions,
                "engagement": daily_engagement,
                "conversions": daily_conversions,
                "engagement_rate": daily_engagement / daily_impressions
            })
        
        return APIContract.success_response(
            simulated_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )
