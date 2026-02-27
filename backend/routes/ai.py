"""
AI Routes
Dedicated endpoints for AI services (Strategy, Content, Analytics, Messaging)
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from contracts.api_contract import APIContract, ErrorCode, RequestContext
from core.security import security_manager, get_current_user
from core.errors import AIServiceError, ValidationError, RateLimitError
from ai.ai_service import ai_service
from schemas.requests import (
    CampaignCalendarRequest,
    KPIGeneratorRequest,
    MediaMixOptimizerRequest,
    TextContentRequest,
    VisualContentRequest,
    VideoContentRequest,
    AnalyticsRequest,
    CustomerReplyRequest
)

# Alias for backward compatibility
BudgetExceededError = RateLimitError

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])
security = HTTPBearer()

# ==================== STRATEGY AI ENDPOINTS ====================

@router.post("/strategy/campaign-calendar", response_model=Dict[str, Any])
async def generate_campaign_calendar(
    request: Request,
    calendar_request: CampaignCalendarRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate AI-powered campaign calendar"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Prepare AI request data
        ai_request_data = {
            "business_id": calendar_request.business_id,
            "user_id": current_user.get("sub"),
            "strategy_type": "campaign_calendar",
            "business_name": calendar_request.business_name or "Your Business",
            "industry": calendar_request.industry or "General",
            "brand_voice": calendar_request.brand_voice or "Professional",
            "target_audience": calendar_request.target_audience or "General audience",
            "campaign_goal": calendar_request.campaign_goal or "Increase engagement",
            "duration_days": str(calendar_request.duration_days or 30),
            "platforms": ", ".join(calendar_request.platforms or ["Instagram", "LinkedIn"]),
            "content_types": ", ".join(calendar_request.content_types or ["posts", "reels", "stories"])
        }
        
        # Generate AI strategy
        ai_result = await ai_service.generate_strategy(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "AI campaign calendar generation failed"
                )
            )
        
        return APIContract.success_response(
            {
                "calendar": ai_result.get("data"),
                "model": ai_result.get("model"),
                "response_time_ms": ai_result.get("response_time_ms"),
                "cost_estimate": ai_result.get("cost_estimate")
            },
            meta=context.to_dict()
        )
        
    except BudgetExceededError as e:
        raise HTTPException(
            status_code=429,
            detail=APIContract.error_response(ErrorCode.RATE_LIMIT_EXCEEDED, str(e))
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


@router.post("/strategy/kpi-generator", response_model=Dict[str, Any])
async def generate_kpis(
    request: Request,
    kpi_request: KPIGeneratorRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate AI-powered KPI recommendations"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Prepare AI request data
        ai_request_data = {
            "business_id": kpi_request.business_id,
            "user_id": current_user.get("sub"),
            "strategy_type": "kpi_generator",
            "business_name": kpi_request.business_name or "Your Business",
            "industry": kpi_request.industry or "General",
            "campaign_goal": kpi_request.campaign_goal or "Increase engagement",
            "target_audience": kpi_request.target_audience or "General audience",
            "duration_days": str(kpi_request.duration_days or 30)
        }
        
        # Generate KPI recommendations
        ai_result = await ai_service.generate_strategy(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "KPI generation failed"
                )
            )
        
        return APIContract.success_response(
            {
                "kpis": ai_result.get("data"),
                "model": ai_result.get("model"),
                "response_time_ms": ai_result.get("response_time_ms"),
                "cost_estimate": ai_result.get("cost_estimate")
            },
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


@router.post("/strategy/media-mix-optimizer", response_model=Dict[str, Any])
async def optimize_media_mix(
    request: Request,
    optimizer_request: MediaMixOptimizerRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Optimize media mix based on performance data"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Prepare AI request data
        ai_request_data = {
            "business_id": optimizer_request.business_id,
            "user_id": current_user.get("sub"),
            "strategy_type": "media_mix_optimizer",
            "performance_data": optimizer_request.performance_data or {},
            "platform_performance": optimizer_request.platform_performance or {},
            "content_type_performance": optimizer_request.content_type_performance or {}
        }
        
        # Generate media mix optimization
        ai_result = await ai_service.generate_strategy(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "Media mix optimization failed"
                )
            )
        
        return APIContract.success_response(
            {
                "optimization": ai_result.get("data"),
                "model": ai_result.get("model"),
                "response_time_ms": ai_result.get("response_time_ms"),
                "cost_estimate": ai_result.get("cost_estimate")
            },
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


# ==================== CONTENT AI ENDPOINTS ====================

@router.post("/content/text", response_model=Dict[str, Any])
async def generate_text_content(
    request: Request,
    text_request: TextContentRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate AI-powered text content"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Prepare AI request data
        ai_request_data = {
            "business_id": text_request.business_id,
            "user_id": current_user.get("sub"),
            "content_type": "text",
            "business_name": text_request.business_name or "Your Business",
            "industry": text_request.industry or "General",
            "brand_voice": text_request.brand_voice or "Professional",
            "target_audience": text_request.target_audience or "General audience",
            "content_topic": text_request.topic or "marketing content",
            "platform": text_request.platform or "instagram",
            "tone": text_request.tone or "engaging",
            "length": text_request.length or "medium",
            "character_limit": str(text_request.character_limit or 150),
            "platform_guidelines": "Follow platform best practices"
        }
        
        # Generate text content
        ai_result = await ai_service.generate_content(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "Text content generation failed"
                )
            )
        
        return APIContract.success_response(
            {
                "content": ai_result.get("data"),
                "model": ai_result.get("model"),
                "response_time_ms": ai_result.get("response_time_ms"),
                "cost_estimate": ai_result.get("cost_estimate")
            },
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


@router.post("/content/visual", response_model=Dict[str, Any])
async def generate_visual_content(
    request: Request,
    visual_request: VisualContentRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate AI-powered visual content concept"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Prepare AI request data
        ai_request_data = {
            "business_id": visual_request.business_id,
            "user_id": current_user.get("sub"),
            "content_type": "visual",
            "business_name": visual_request.business_name or "Your Business",
            "industry": visual_request.industry or "General",
            "brand_colors": ", ".join(visual_request.brand_colors or ["blue", "white"]),
            "brand_guidelines": visual_request.brand_guidelines or "Modern and clean",
            "target_audience": visual_request.target_audience or "General audience",
            "visual_topic": visual_request.topic or "promotional content",
            "platform": visual_request.platform or "instagram",
            "visual_style": visual_request.visual_style or "modern and clean"
        }
        
        # Generate visual content
        ai_result = await ai_service.generate_content(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "Visual content generation failed"
                )
            )
        
        return APIContract.success_response(
            {
                "content": ai_result.get("data"),
                "model": ai_result.get("model"),
                "response_time_ms": ai_result.get("response_time_ms"),
                "cost_estimate": ai_result.get("cost_estimate")
            },
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


@router.post("/content/video", response_model=Dict[str, Any])
async def generate_video_script(
    request: Request,
    video_request: VideoContentRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate AI-powered video script"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Prepare AI request data
        ai_request_data = {
            "business_id": video_request.business_id,
            "user_id": current_user.get("sub"),
            "content_type": "video",
            "business_name": video_request.business_name or "Your Business",
            "industry": video_request.industry or "General",
            "brand_voice": video_request.brand_voice or "Professional",
            "target_audience": video_request.target_audience or "General audience",
            "video_topic": video_request.topic or "promotional video",
            "platform": video_request.platform or "instagram",
            "duration_seconds": str(video_request.duration_seconds or 30),
            "script_style": video_request.script_style or "conversational"
        }
        
        # Generate video script
        ai_result = await ai_service.generate_content(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "Video script generation failed"
                )
            )
        
        return APIContract.success_response(
            {
                "content": ai_result.get("data"),
                "model": ai_result.get("model"),
                "response_time_ms": ai_result.get("response_time_ms"),
                "cost_estimate": ai_result.get("cost_estimate")
            },
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


# ==================== ANALYTICS AI ENDPOINTS ====================

@router.post("/analytics/analyze", response_model=Dict[str, Any])
async def analyze_performance(
    request: Request,
    analytics_request: AnalyticsRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Analyze campaign performance with AI insights"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Prepare AI request data
        ai_request_data = {
            "business_id": analytics_request.business_id,
            "user_id": current_user.get("sub"),
            "performance_data": analytics_request.performance_data or {},
            "platform_performance": analytics_request.platform_performance or {},
            "content_type_performance": analytics_request.content_type_performance or {},
            "time_period": analytics_request.time_period or "last 30 days",
            "campaign_goals": analytics_request.campaign_goals or "engagement and growth"
        }
        
        # Generate analytics
        ai_result = await ai_service.generate_analytics(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "Performance analysis failed"
                )
            )
        
        return APIContract.success_response(
            {
                "analytics": ai_result.get("data"),
                "model": ai_result.get("model"),
                "response_time_ms": ai_result.get("response_time_ms"),
                "cost_estimate": ai_result.get("cost_estimate")
            },
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


# ==================== MESSAGING AI ENDPOINTS ====================

@router.post("/messaging/reply", response_model=Dict[str, Any])
async def generate_customer_reply(
    request: Request,
    reply_request: CustomerReplyRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate AI-powered customer reply"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Prepare AI request data
        ai_request_data = {
            "business_id": reply_request.business_id,
            "user_id": current_user.get("sub"),
            "business_name": reply_request.business_name or "Your Business",
            "brand_voice": reply_request.brand_voice or "Professional",
            "industry": reply_request.industry or "General",
            "customer_message": reply_request.customer_message,
            "conversation_history": reply_request.conversation_history or "No previous messages",
            "platform": reply_request.platform or "instagram",
            "customer_profile": reply_request.customer_profile or {}
        }
        
        # Generate reply
        ai_result = await ai_service.generate_message_reply(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "Reply generation failed"
                )
            )
        
        return APIContract.success_response(
            {
                "reply": ai_result.get("data"),
                "model": ai_result.get("model"),
                "response_time_ms": ai_result.get("response_time_ms"),
                "cost_estimate": ai_result.get("cost_estimate")
            },
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


# ==================== AI SERVICE STATUS ENDPOINTS ====================

@router.get("/status", response_model=Dict[str, Any])
async def get_ai_status(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get AI service status"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        status = await ai_service.get_service_status()
        
        return APIContract.success_response(
            status,
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


@router.get("/usage", response_model=Dict[str, Any])
async def get_ai_usage(
    request: Request,
    period: str = Query("daily", regex="^(daily|weekly|monthly)$"),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get AI usage statistics"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        usage = await ai_service.get_usage_statistics(period)
        
        return APIContract.success_response(
            usage,
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )


@router.get("/optimization-suggestions", response_model=Dict[str, Any])
async def get_optimization_suggestions(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get cost optimization suggestions"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        suggestions = await ai_service.get_cost_optimization_suggestions()
        
        return APIContract.success_response(
            {"suggestions": suggestions},
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )
