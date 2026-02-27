"""
Content Routes
Implements the API contract for content endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from contracts.api_contract import (
    APIContract, ErrorCode, ContentGenerateRequest, ContentResponse,
    ContentScheduleRequest, ContentScheduleResponse,
    RequestContext, ValidationRules, get_status_code
)
from core.security import security_manager, get_current_user
from models.mongo_db import content_repo
from ai.ai_service import ai_service

router = APIRouter(prefix="/api/v1/content", tags=["content"])
security = HTTPBearer()

@router.post("/generate", response_model=Dict[str, Any])
async def generate_content(
    request: Request,
    content_data: ContentGenerateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate content (AI)"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate request
        if not ValidationRules.validate_campaign_day(content_data.day):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("day", "Day must be 1-31")
            )
        
        if not ValidationRules.validate_content_type(content_data.content_type):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("content_type", "Invalid content type")
            )
        
        # Prepare AI request data
        ai_request_data = {
            "business_id": "demo_business_id",  # Would get from campaign
            "user_id": current_user.get("sub"),
            "content_type": content_data.content_type,
            "platform": "instagram",  # Would get from campaign
            "topic": f"Day {content_data.day} campaign content",
            "tone": "Professional but engaging",
            "brand_voice": "Professional",
            "length": "medium",
            "include_hashtags": True,
            "include_cta": True
        }
        
        # Generate AI content
        ai_result = await ai_service.generate_content(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "AI content generation failed"
                )
            )
        
        # Create content record
        content_dict = {
            "campaign_id": content_data.campaign_id,
            "business_id": "demo_business_id",  # Would get from campaign
            "title": f"Day {content_data.day} - {content_data.content_type.title()}",
            "content_type": content_data.content_type,
            "platform": "instagram",  # Would get from campaign
            "text_content": ai_result.get("data", {}).get("body"),
            "hashtags": ai_result.get("data", {}).get("hashtags", []),
            "call_to_action": ai_result.get("data", {}).get("cta"),
            "ai_generated": True,
            "ai_prompt_used": f"Generate {content_data.content_type} for day {content_data.day}",
            "ai_model_used": ai_result.get("model"),
            "predicted_engagement_score": ai_result.get("data", {}).get("predicted_engagement_score", 75),
            "status": "draft",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Add content type specific fields
        if content_data.content_type == "video":
            content_dict["script"] = ai_result.get("data", {}).get("script")
        elif content_data.content_type in ["image", "reel", "story"]:
            content_dict["visual_description"] = ai_result.get("data", {}).get("visual_description")
        
        content_id = await content_repo.create(content_dict)
        
        # Format response
        ai_data = ai_result.get("data", {})
        response_data = {
            "content_id": content_id,
            "caption": ai_data.get("body"),
            "hashtags": ai_data.get("hashtags", []),
            "script": ai_data.get("script"),
            "visual_description": ai_data.get("visual_description"),
            "estimated_engagement_score": ai_data.get("predicted_engagement_score", 75),
            "tone_analysis": ai_data.get("tone_analysis"),
            "character_count": ai_data.get("character_count"),
            "content_type": content_data.content_type,
            "platform": "instagram"
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
async def list_content(
    request: Request,
    campaign_id: Optional[str] = Query(None),
    business_id: Optional[str] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """List content"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        if campaign_id:
            contents = await content_repo.get_by_campaign_id(campaign_id)
        elif business_id:
            contents = await content_repo.get_by_business_id(business_id)
        else:
            contents = []
        
        response_data = [
            {
                "content_id": content.get("id"),
                "campaign_id": content.get("campaign_id"),
                "business_id": content.get("business_id"),
                "title": content.get("title"),
                "content_type": content.get("content_type"),
                "platform": content.get("platform"),
                "status": content.get("status"),
                "scheduled_date": content.get("scheduled_date"),
                "published_date": content.get("published_date"),
                "created_at": content.get("created_at"),
                "ai_generated": content.get("ai_generated"),
                "predicted_engagement_score": content.get("predicted_engagement_score")
            }
            for content in contents
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

@router.get("/{content_id}", response_model=Dict[str, Any])
async def get_content(
    request: Request,
    content_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get content details"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        content = await content_repo.get_by_id(content_id)
        
        if not content:
            raise HTTPException(
                status_code=404,
                detail=APIContract.error_response(
                    ErrorCode.CONTENT_NOT_FOUND,
                    "Content not found"
                )
            )
        
        response_data = {
            "content_id": content.get("id"),
            "campaign_id": content.get("campaign_id"),
            "business_id": content.get("business_id"),
            "title": content.get("title"),
            "content_type": content.get("content_type"),
            "platform": content.get("platform"),
            "text_content": content.get("text_content"),
            "visual_description": content.get("visual_description"),
            "script": content.get("script"),
            "hashtags": content.get("hashtags", []),
            "call_to_action": content.get("call_to_action"),
            "media_urls": content.get("media_urls", []),
            "thumbnail_url": content.get("thumbnail_url"),
            "scheduled_date": content.get("scheduled_date"),
            "published_date": content.get("published_date"),
            "status": content.get("status"),
            "ai_generated": content.get("ai_generated"),
            "ai_prompt_used": content.get("ai_prompt_used"),
            "ai_model_used": content.get("ai_model_used"),
            "predicted_engagement_score": content.get("predicted_engagement_score"),
            "engagement_count": content.get("engagement_count", 0),
            "impression_count": content.get("impression_count", 0),
            "click_count": content.get("click_count", 0),
            "conversion_count": content.get("conversion_count", 0),
            "created_at": content.get("created_at"),
            "updated_at": content.get("updated_at")
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

@router.put("/{content_id}", response_model=Dict[str, Any])
async def update_content(
    request: Request,
    content_id: str,
    content_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update content"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate content type if provided
        if "content_type" in content_data and not ValidationRules.validate_content_type(content_data["content_type"]):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("content_type", "Invalid content type")
            )
        
        # Check if content exists
        existing_content = await content_repo.get_by_id(content_id)
        if not existing_content:
            raise HTTPException(
                status_code=404,
                detail=APIContract.error_response(
                    ErrorCode.CONTENT_NOT_FOUND,
                    "Content not found"
                )
            )
        
        # Update content
        content_data["updated_at"] = datetime.utcnow()
        success = await content_repo.update(content_id, content_data)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=APIContract.internal_error_response("Failed to update content")
            )
        
        # Get updated content
        updated_content = await content_repo.get_by_id(content_id)
        
        response_data = {
            "content_id": updated_content.get("id"),
            "title": updated_content.get("title"),
            "content_type": updated_content.get("content_type"),
            "platform": updated_content.get("platform"),
            "text_content": updated_content.get("text_content"),
            "hashtags": updated_content.get("hashtags", []),
            "call_to_action": updated_content.get("call_to_action"),
            "status": updated_content.get("status"),
            "updated_at": updated_content.get("updated_at")
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

@router.post("/schedule", response_model=Dict[str, Any])
async def schedule_content(
    request: Request,
    schedule_data: ContentScheduleRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Schedule content"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate scheduled time
        if not ValidationRules.validate_scheduled_time(schedule_data.scheduled_at):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("scheduled_at", "Scheduled time must be in the future")
            )
        
        # Check if content exists
        existing_content = await content_repo.get_by_id(schedule_data.content_id)
        if not existing_content:
            raise HTTPException(
                status_code=404,
                detail=APIContract.error_response(
                    ErrorCode.CONTENT_NOT_FOUND,
                    "Content not found"
                )
            )
        
        # Update content with schedule
        update_data = {
            "scheduled_date": schedule_data.scheduled_at,
            "status": "scheduled",
            "updated_at": datetime.utcnow()
        }
        
        success = await content_repo.update(schedule_data.content_id, update_data)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=APIContract.internal_error_response("Failed to schedule content")
            )
        
        response_data = {
            "status": "scheduled",
            "content_id": schedule_data.content_id,
            "scheduled_at": schedule_data.scheduled_at.isoformat()
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

@router.post("/{content_id}/publish", response_model=Dict[str, Any])
async def publish_content(
    request: Request,
    content_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Publish content"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Check if content exists
        existing_content = await content_repo.get_by_id(content_id)
        if not existing_content:
            raise HTTPException(
                status_code=404,
                detail=APIContract.error_response(
                    ErrorCode.CONTENT_NOT_FOUND,
                    "Content not found"
                )
            )
        
        # Check if already published
        if existing_content.get("status") == "published":
            raise HTTPException(
                status_code=409,
                detail=APIContract.error_response(
                    ErrorCode.CONTENT_ALREADY_PUBLISHED,
                    "Content already published"
                )
            )
        
        # Update content as published
        update_data = {
            "published_date": datetime.utcnow(),
            "status": "published",
            "updated_at": datetime.utcnow()
        }
        
        success = await content_repo.update(content_id, update_data)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=APIContract.internal_error_response("Failed to publish content")
            )
        
        response_data = {
            "status": "published",
            "content_id": content_id,
            "published_at": datetime.utcnow().isoformat()
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

@router.delete("/{content_id}", response_model=Dict[str, Any])
async def delete_content(
    request: Request,
    content_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Delete content"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Check if content exists
        existing_content = await content_repo.get_by_id(content_id)
        if not existing_content:
            raise HTTPException(
                status_code=404,
                detail=APIContract.error_response(
                    ErrorCode.CONTENT_NOT_FOUND,
                    "Content not found"
                )
            )
        
        # Delete content
        success = await content_repo.delete(content_id)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=APIContract.internal_error_response("Failed to delete content")
            )
        
        response_data = {
            "message": "Content deleted successfully",
            "content_id": content_id
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
