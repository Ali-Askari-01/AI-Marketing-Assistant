"""
Campaign Routes
Implements the API contract for campaign endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from contracts.api_contract import (
    APIContract, ErrorCode, CampaignGenerateRequest, CampaignResponse,
    RequestContext, ValidationRules, get_status_code
)
from core.security import security_manager, get_current_user
from models.mongo_db import campaign_repo
from services.campaign_service import campaign_service
from ai.ai_service import ai_service

router = APIRouter(prefix="/api/v1/campaign", tags=["campaign"])
security = HTTPBearer()

@router.post("/generate", response_model=Dict[str, Any])
async def generate_campaign_strategy(
    request: Request,
    campaign_data: CampaignGenerateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate campaign strategy (AI)"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate request
        if not ValidationRules.validate_duration_days(campaign_data.duration_days):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("duration_days", "Duration must be 7-365 days")
            )
        
        # Prepare AI request data
        ai_request_data = {
            "business_id": campaign_data.business_id,
            "user_id": current_user.get("sub"),
            "duration_days": campaign_data.duration_days,
            "campaign_goal": "Increase brand awareness and engagement",
            "industry": "Technology",
            "target_audience": {
                "age_range": "25-45",
                "interests": ["Technology", "Innovation", "Productivity"]
            },
            "brand_voice": "Professional but innovative",
            "platforms": ["instagram", "linkedin", "email"],
            "content_types": ["image", "text", "video"]
        }
        
        # Generate AI strategy
        ai_result = await ai_service.generate_strategy(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "AI strategy generation failed"
                )
            )
        
        # Create campaign with AI strategy
        campaign_dict = {
            "business_id": campaign_data.business_id,
            "name": f"AI Generated Campaign - {datetime.utcnow().strftime('%Y-%m-%d')}",
            "description": "AI-generated marketing campaign",
            "duration_days": campaign_data.duration_days,
            "start_date": datetime.utcnow(),
            "primary_goal": "Increase brand awareness and engagement",
            "secondary_goals": ["Engagement", "Brand building"],
            "ai_strategy": ai_result.get("data"),
            "status": "draft",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        campaign_id = await campaign_service.create_campaign(campaign_dict, current_user.get("sub"))
        
        # Format calendar from AI response
        ai_data = ai_result.get("data", {})
        calendar = ai_data.get("campaign_calendar", [])
        
        response_data = {
            "campaign_id": campaign_id,
            "calendar": calendar,
            "weekly_themes": ai_data.get("weekly_themes", []),
            "content_distribution": ai_data.get("content_distribution", {}),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.get("", response_model=Dict[str, Any])
async def list_campaigns(
    request: Request,
    business_id: Optional[str] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """List campaigns"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        if business_id:
            campaigns = await campaign_service.get_business_campaigns(business_id, current_user.get("sub"))
        else:
            # Get all campaigns for user (would need to implement this)
            campaigns = []
        
        response_data = [
            {
                "campaign_id": campaign.get("id"),
                "business_id": campaign.get("business_id"),
                "name": campaign.get("name"),
                "status": campaign.get("status"),
                "start_date": campaign.get("start_date"),
                "end_date": campaign.get("end_date"),
                "created_at": campaign.get("created_at")
            }
            for campaign in campaigns
        ]
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.get("/{campaign_id}", response_model=Dict[str, Any])
async def get_campaign(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get campaign details"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=campaign_id)
    
    try:
        campaign = await campaign_service.get_campaign(campaign_id, current_user.get("sub"))
        
        response_data = {
            "campaign_id": campaign.get("id"),
            "business_id": campaign.get("business_id"),
            "name": campaign.get("name"),
            "description": campaign.get("description"),
            "status": campaign.get("status"),
            "duration_days": campaign.get("duration_days"),
            "start_date": campaign.get("start_date"),
            "end_date": campaign.get("end_date"),
            "primary_goal": campaign.get("primary_goal"),
            "secondary_goals": campaign.get("secondary_goals", []),
            "ai_strategy": campaign.get("ai_strategy"),
            "calendar": campaign.get("ai_strategy", {}).get("campaign_calendar", []),
            "weekly_themes": campaign.get("ai_strategy", {}).get("weekly_themes", []),
            "created_at": campaign.get("created_at"),
            "updated_at": campaign.get("updated_at")
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.put("/{campaign_id}", response_model=Dict[str, Any])
async def update_campaign(
    request: Request,
    campaign_id: str,
    campaign_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update campaign"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=campaign_id)
    
    try:
        # Validate duration if provided
        if "duration_days" in campaign_data and not ValidationRules.validate_duration_days(campaign_data["duration_days"]):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("duration_days", "Duration must be 7-365 days")
            )
        
        updated_campaign = await campaign_service.update_campaign(campaign_id, campaign_data, current_user.get("sub"))
        
        response_data = {
            "campaign_id": updated_campaign.get("id"),
            "business_id": updated_campaign.get("business_id"),
            "name": updated_campaign.get("name"),
            "description": updated_campaign.get("description"),
            "status": updated_campaign.get("status"),
            "duration_days": updated_campaign.get("duration_days"),
            "start_date": updated_campaign.get("start_date"),
            "end_date": updated_campaign.get("end_date"),
            "primary_goal": updated_campaign.get("primary_goal"),
            "secondary_goals": updated_campaign.get("secondary_goals", []),
            "ai_strategy": updated_campaign.get("ai_strategy"),
            "created_at": updated_campaign.get("created_at"),
            "updated_at": updated_campaign.get("updated_at")
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.delete("/{campaign_id}", response_model=Dict[str, Any])
async def delete_campaign(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Delete campaign"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=campaign_id)
    
    try:
        success = await campaign_service.delete_campaign(campaign_id, current_user.get("sub"))
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=APIContract.internal_error_response("Failed to delete campaign")
            )
        
        response_data = {
            "message": "Campaign deleted successfully",
            "campaign_id": campaign_id
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/{campaign_id}/activate", response_model=Dict[str, Any])
async def activate_campaign(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Activate campaign"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=campaign_id)
    
    try:
        activated_campaign = await campaign_service.activate_campaign(campaign_id, current_user.get("sub"))
        
        response_data = {
            "campaign_id": activated_campaign.get("id"),
            "status": activated_campaign.get("status"),
            "message": "Campaign activated successfully"
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/{campaign_id}/pause", response_model=Dict[str, Any])
async def pause_campaign(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Pause campaign"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=campaign_id)
    
    try:
        paused_campaign = await campaign_service.pause_campaign(campaign_id, current_user.get("sub"))
        
        response_data = {
            "campaign_id": paused_campaign.get("id"),
            "status": paused_campaign.get("status"),
            "message": "Campaign paused successfully"
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/{campaign_id}/complete", response_model=Dict[str, Any])
async def complete_campaign(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Complete campaign"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=campaign_id)
    
    try:
        completed_campaign = await campaign_service.complete_campaign(campaign_id, current_user.get("sub"))
        
        response_data = {
            "campaign_id": completed_campaign.get("id"),
            "status": completed_campaign.get("status"),
            "message": "Campaign completed successfully"
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/{campaign_id}/generate-ai-strategy", response_model=Dict[str, Any])
async def generate_ai_strategy(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate AI strategy for existing campaign"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=campaign_id)
    
    try:
        updated_campaign = await campaign_service.generate_ai_strategy(campaign_id, current_user.get("sub"))
        
        response_data = {
            "campaign_id": updated_campaign.get("id"),
            "ai_strategy": updated_campaign.get("ai_strategy"),
            "message": "AI strategy generated successfully"
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.get("/{campaign_id}/analytics", response_model=Dict[str, Any])
async def get_campaign_analytics(
    request: Request,
    campaign_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get campaign analytics"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=campaign_id)
    
    try:
        analytics = await campaign_service.get_campaign_analytics(campaign_id, current_user.get("sub"))
        
        return APIContract.success_response(
            analytics,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )
