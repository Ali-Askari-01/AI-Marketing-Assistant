"""
Business Routes
Implements the API contract for business endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from contracts.api_contract import (
    APIContract, ErrorCode, BusinessCreateRequest, BusinessResponse,
    RequestContext, ValidationRules, get_status_code
)
from core.security import security_manager, get_current_user
from models.mongo_db import business_repo
from services.business_service import business_service

router = APIRouter(prefix="/api/v1/business", tags=["business"])
security = HTTPBearer()

@router.post("", response_model=Dict[str, Any])
async def create_business(
    request: Request,
    business_data: BusinessCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Create business"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate request
        if not ValidationRules.validate_business_name(business_data.name):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("name", "Business name must be 2-100 characters")
            )
        
        # Create business
        business_dict = business_data.dict()
        business_dict.update({
            "owner_id": current_user.get("sub"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        business_id = await business_service.create_business(business_dict, current_user.get("sub"))
        
        response_data = {
            "business_id": business_id,
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
async def get_all_businesses(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get all businesses for current user"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        businesses = await business_service.get_user_businesses(current_user.get("sub"))
        
        response_data = [
            {
                "business_id": business.get("id"),
                "name": business.get("name"),
                "industry": business.get("industry"),
                "created_at": business.get("created_at")
            }
            for business in businesses
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

@router.get("/{business_id}", response_model=Dict[str, Any])
async def get_business(
    request: Request,
    business_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get business details"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=business_id)
    
    try:
        business = await business_service.get_business(business_id, current_user.get("sub"))
        
        response_data = {
            "business_id": business.get("id"),
            "name": business.get("name"),
            "industry": business.get("industry"),
            "description": business.get("description"),
            "website": business.get("website"),
            "target_audience": business.get("target_audience"),
            "brand_voice": business.get("brand_voice"),
            "brand_colors": business.get("brand_colors"),
            "created_at": business.get("created_at"),
            "updated_at": business.get("updated_at")
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

@router.put("/{business_id}", response_model=Dict[str, Any])
async def update_business(
    request: Request,
    business_id: str,
    business_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update business"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=business_id)
    
    try:
        # Validate business name if provided
        if "name" in business_data and not ValidationRules.validate_business_name(business_data["name"]):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("name", "Business name must be 2-100 characters")
            )
        
        updated_business = await business_service.update_business(business_id, business_data, current_user.get("sub"))
        
        response_data = {
            "business_id": updated_business.get("id"),
            "name": updated_business.get("name"),
            "industry": updated_business.get("industry"),
            "description": updated_business.get("description"),
            "website": updated_business.get("website"),
            "target_audience": updated_business.get("target_audience"),
            "brand_voice": updated_business.get("brand_voice"),
            "brand_colors": updated_business.get("brand_colors"),
            "created_at": updated_business.get("created_at"),
            "updated_at": updated_business.get("updated_at")
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

@router.delete("/{business_id}", response_model=Dict[str, Any])
async def delete_business(
    request: Request,
    business_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Delete business"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=business_id)
    
    try:
        success = await business_service.delete_business(business_id, current_user.get("sub"))
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=APIContract.internal_error_response("Failed to delete business")
            )
        
        response_data = {
            "message": "Business deleted successfully",
            "business_id": business_id
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

@router.get("/{business_id}/analytics", response_model=Dict[str, Any])
async def get_business_analytics(
    request: Request,
    business_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get business analytics"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"), business_id=business_id)
    
    try:
        analytics = await business_service.get_business_analytics(business_id, current_user.get("sub"))
        
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
