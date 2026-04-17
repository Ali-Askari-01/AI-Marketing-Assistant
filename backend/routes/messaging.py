"""
Messaging Routes
Implements the API contract for messaging endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from contracts.api_contract import (
    APIContract, ErrorCode, MessageReplyRequest, MessageReplyResponse,
    RequestContext, ValidationRules, get_status_code
)
from core.security import security_manager, get_current_user
from ai.ai_service import ai_service

router = APIRouter(prefix="/api/v1/messages", tags=["messaging"])
security = HTTPBearer()

@router.get("", response_model=Dict[str, Any])
async def list_messages(
    request: Request,
    business_id: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get messages"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate platform if provided
        if platform and not ValidationRules.validate_platform(platform):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("platform", "Invalid platform")
            )
        
        # Generate mock messages data (in production, this would be real data)
        messages_data = {
            "messages": [
                {
                    "id": "msg_1",
                    "business_id": business_id or "demo_business_id",
                    "platform": platform or "instagram",
                    "sender_name": "Sarah Johnson",
                    "sender_type": "customer",
                    "message_text": "How much is your monthly membership?",
                    "message_type": "inquiry",
                    "status": status or "pending",
                    "priority": "normal",
                    "received_at": "2024-01-15T10:30:00Z",
                    "ai_suggested_reply": "Thanks for your interest! Our monthly membership starts at $29 and includes unlimited classes. Would you like to schedule a tour?",
                    "ai_sentiment": "neutral",
                    "ai_category": "pricing_inquiry",
                    "thread_id": "thread_1"
                },
                {
                    "id": "msg_2",
                    "business_id": business_id or "demo_business_id",
                    "platform": platform or "instagram",
                    "sender_name": "Mike Chen",
                    "sender_type": "customer",
                    "message_text": "Do you offer personal training sessions?",
                    "message_type": "inquiry",
                    "status": status or "replied",
                    "priority": "normal",
                    "received_at": "2024-01-15T09:15:00Z",
                    "ai_suggested_reply": "Yes! We offer personal training with certified trainers. Sessions are $45/hour. Would you like to book a consultation?",
                    "ai_sentiment": "neutral",
                    "ai_category": "service_inquiry",
                    "thread_id": "thread_2"
                },
                {
                    "id": "msg_3",
                    "business_id": business_id or "demo_business_id",
                    "platform": platform or "instagram",
                    "sender_name": "Emma Wilson",
                    "sender_type": "customer",
                    "message_text": "I love your gym! The trainers are amazing! 💪",
                    "message_type": "feedback",
                    "status": status or "replied",
                    "priority": "low",
                    "received_at": "2024-01-14T16:45:00Z",
                    "ai_suggested_reply": "Thank you so much for the kind words! We're thrilled you're having a great experience. Keep up the great work! 🎉",
                    "ai_sentiment": "positive",
                    "ai_category": "positive_feedback",
                    "thread_id": "thread_3"
                },
                {
                    "id": "msg_4",
                    "business_id": business_id or "demo_business_id",
                    "platform": platform or "instagram",
                    "sender_name": "David Brown",
                    "sender_type": "customer",
                    "message_text": "What are your opening hours?",
                    "message_type": "inquiry",
                    "status": status or "pending",
                    "priority": "normal",
                    "received_at": "2024-01-15T11:20:00Z",
                    "ai_suggested_reply": "We're open Monday-Friday 6AM-10PM, Saturday 7AM-8PM, and Sunday 8AM-6PM. Stop by anytime for a tour!",
                    "ai_sentiment": "neutral",
                    "ai_category": "hours_inquiry",
                    "thread_id": "thread_4"
                }
            ],
            "pagination": {
                "total": 4,
                "limit": limit,
                "offset": offset,
                "has_next": False
            },
            "filters": {
                "business_id": business_id,
                "platform": platform,
                "status": status
            }
        }
        
        return APIContract.success_response(
            messages_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/reply", response_model=Dict[str, Any])
async def generate_ai_reply(
    request: Request,
    reply_data: MessageReplyRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Generate AI reply suggestion"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate request
        if not reply_data.customer_message.strip():
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("customer_message", "Message cannot be empty")
            )
        
        # Prepare AI request data
        ai_request_data = {
            "business_id": reply_data.business_id,
            "user_id": current_user.get("sub"),
            "customer_message": reply_data.customer_message,
            "conversation_context": {
                "last_messages": [
                    {
                        "sender": "customer",
                        "message": reply_data.customer_message,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                ],
                "sentiment": "neutral",
                "customer_profile": {
                    "name": "Customer",
                    "history": "First interaction"
                }
            },
            "brand_voice": "Professional but friendly",
            "platform": "instagram",
            "tone": "Professional"
        }
        
        # Generate AI reply
        ai_result = await ai_service.generate_message_reply(ai_request_data)
        
        if not ai_result.get("success"):
            raise HTTPException(
                status_code=503,
                detail=APIContract.error_response(
                    ErrorCode.AI_GENERATION_FAILED,
                    "AI reply generation failed"
                )
            )
        
        # Format response
        ai_data = ai_result.get("data", {})
        response_data = {
            "suggested_reply": ai_data.get("reply_text"),
            "response_type": ai_data.get("response_type"),
            "platform": ai_data.get("platform"),
            "tone": ai_data.get("tone"),
            "escalation_needed": ai_data.get("escalation_needed", False),
            "follow_up_required": ai_data.get("follow_up_required", False),
            "sentiment": ai_data.get("sentiment"),
            "confidence_score": ai_data.get("confidence_score"),
            "next_action": ai_data.get("next_action"),
            "ai_model_used": ai_result.get("model"),
            "processing_time_ms": ai_result.get("response_time_ms")
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

@router.post("/{message_id}/mark-replied", response_model=Dict[str, Any])
async def mark_message_replied(
    request: Request,
    message_id: str,
    reply_data: Optional[Dict[str, Any]] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Mark message as replied"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # In production, this would update the message in the database
        # For now, return success
        
        response_data = {
            "message_id": message_id,
            "status": "replied",
            "replied_at": datetime.utcnow().isoformat(),
            "replied_by": current_user.get("sub"),
            "reply_text": reply_data.get("reply_text") if reply_data else None
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/{message_id}/escalate", response_model=Dict[str, Any])
async def escalate_message(
    request: Request,
    message_id: str,
    escalation_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Escalate message"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate escalation data
        reason = escalation_data.get("reason", "")
        priority = escalation_data.get("priority", "high")
        
        if not reason.strip():
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("reason", "Escalation reason cannot be empty")
            )
        
        response_data = {
            "message_id": message_id,
            "status": "escalated",
            "escalated_at": datetime.utcnow().isoformat(),
            "escalated_by": current_user.get("sub"),
            "reason": reason,
            "priority": priority,
            "assigned_to": escalation_data.get("assigned_to", "manager")
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

@router.get("/{message_id}/thread", response_model=Dict[str, Any])
async def get_message_thread(
    request: Request,
    message_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get message thread"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Generate mock thread data
        thread_data = {
            "thread_id": f"thread_{message_id}",
            "customer_name": "Sarah Johnson",
            "customer_email": "sarah.johnson@email.com",
            "platform": "instagram",
            "messages": [
                {
                    "id": message_id,
                    "sender": "customer",
                    "message": "How much is your monthly membership?",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "type": "text"
                },
                {
                    "id": f"reply_{message_id}",
                    "sender": "business",
                    "message": "Thanks for your interest! Our monthly membership starts at $29 and includes unlimited classes. Would you like to schedule a tour?",
                    "timestamp": "2024-01-15T10:35:00Z",
                    "type": "text"
                },
                {
                    "id": f"followup_{message_id}",
                    "sender": "customer",
                    "message": "That sounds great! When would be a good time for a tour?",
                    "timestamp": "2024-01-15T10:45:00Z",
                    "type": "text"
                }
            ],
            "status": "active",
            "last_message_at": "2024-01-15T10:45:00Z",
            "message_count": 3,
            "unread_count": 1,
            "priority": "normal",
            "customer_info": {
                "first_contact": "2024-01-10T14:20:00Z",
                "total_messages": 5,
                "conversion_stage": "consideration",
                "lead_score": 75
            }
        }
        
        return APIContract.success_response(
            thread_data,
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/simulate", response_model=Dict[str, Any])
async def simulate_messages(
    request: Request,
    simulation_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Simulate messages"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Validate simulation parameters
        message_count = simulation_data.get("message_count", 10)
        platforms = simulation_data.get("platforms", ["instagram", "linkedin"])
        
        if not (1 <= message_count <= 100):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("message_count", "Count must be 1-100")
            )
        
        # Generate simulated messages
        import random
        simulated_data = {
            "simulation_id": str(uuid.uuid4()),
            "parameters": {
                "message_count": message_count,
                "platforms": platforms
            },
            "generated_messages": []
        }
        
        message_templates = [
            "How much is your membership?",
            "Do you offer personal training?",
            "What are your opening hours?",
            "Do you have a trial membership?",
            "What equipment do you have?",
            "Do you offer group classes?",
            "Can I freeze my membership?",
            "Do you have parking available?",
            "What's your cancellation policy?"
        ]
        
        for i in range(message_count):
            platform = random.choice(platforms)
            template = random.choice(message_templates)
            
            simulated_data["generated_messages"].append({
                "id": f"sim_msg_{i+1}",
                "platform": platform,
                "sender_name": f"Customer {i+1}",
                "sender_type": "customer",
                "message_text": template,
                "message_type": "inquiry",
                "status": "pending",
                "priority": random.choice(["low", "normal", "high"]),
                "received_at": (datetime.utcnow() - timedelta(hours=random.randint(0, 24))).isoformat()
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

@router.get("/stats", response_model=Dict[str, Any])
async def get_messaging_stats(
    request: Request,
    business_id: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get messaging statistics"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id, user_id=current_user.get("sub"))
    
    try:
        # Generate mock stats data
        stats_data = {
            "business_id": business_id or "demo_business_id",
            "period": {
                "from": date_from or (datetime.utcnow() - timedelta(days=30)).isoformat(),
                "to": date_to or datetime.utcnow().isoformat()
            },
            "total_messages": 45,
            "unread_messages": 8,
            "response_rate": 0.85,
            "average_response_time": 2.5,
            "platform_breakdown": {
                "instagram": {
                    "total": 30,
                    "unread": 5,
                    "response_rate": 0.87
                },
                "linkedin": {
                    "total": 10,
                    "unread": 2,
                    "response_rate": 0.80
                },
                "email": {
                    "total": 5,
                    "unread": 1,
                    "response_rate": 0.90
                }
            },
            "message_types": {
                "inquiry": 25,
                "feedback": 8,
                "complaint": 3,
                "appointment": 9
            },
            "priority_breakdown": {
                "high": 2,
                "normal": 35,
                "low": 8
            },
            "ai_suggestions_used": 38,
            "ai_satisfaction_rate": 0.92
        }
        
        return APIContract.success_response(
            stats_data,
            meta=context.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )
