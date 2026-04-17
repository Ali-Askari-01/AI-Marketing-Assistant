"""
API Contract Finalization
Enterprise-grade API contract implementation following the detailed design specifications
"""

from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from enum import Enum
import uuid

# Standard Error Codes
class ErrorCode(str, Enum):
    # Authentication Errors
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INVALID_TOKEN = "INVALID_TOKEN"
    
    # Business Errors
    BUSINESS_NOT_FOUND = "BUSINESS_NOT_FOUND"
    BUSINESS_ALREADY_EXISTS = "BUSINESS_ALREADY_EXISTS"
    INVALID_BUSINESS_DATA = "INVALID_BUSINESS_DATA"
    
    # Campaign Errors
    CAMPAIGN_NOT_FOUND = "CAMPAIGN_NOT_FOUND"
    CAMPAIGN_ALREADY_EXISTS = "CAMPAIGN_ALREADY_EXISTS"
    INVALID_CAMPAIGN_DATA = "INVALID_CAMPAIGN_DATA"
    AI_GENERATION_FAILED = "AI_GENERATION_FAILED"
    
    # Content Errors
    CONTENT_NOT_FOUND = "CONTENT_NOT_FOUND"
    INVALID_CONTENT_TYPE = "INVALID_CONTENT_TYPE"
    CONTENT_ALREADY_PUBLISHED = "CONTENT_ALREADY_PUBLISHED"
    INVALID_SCHEDULE_TIME = "INVALID_SCHEDULE_TIME"
    
    # Analytics Errors
    ANALYTICS_NOT_FOUND = "ANALYTICS_NOT_FOUND"
    INVALID_ANALYTICS_REQUEST = "INVALID_ANALYTICS_REQUEST"
    
    # Messaging Errors
    MESSAGE_NOT_FOUND = "MESSAGE_NOT_FOUND"
    INVALID_MESSAGE_DATA = "INVALID_MESSAGE_DATA"
    
    # General Errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"

# Standard Response Format
class SuccessResponse(BaseModel):
    success: bool = True
    data: Dict[str, Any]
    meta: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: Dict[str, Any]

class MetaData(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "1.0.0"
    processing_time_ms: Optional[int] = None

# Request/Response Schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user_id: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

class BusinessCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    industry: str = Field(..., min_length=2, max_length=50)
    target_audience: str = "Young professionals"
    brand_tone: str = "Professional but motivational"
    primary_goal: str = "Lead Generation"

class BusinessResponse(BaseModel):
    business_id: str
    created_at: datetime

class CampaignGenerateRequest(BaseModel):
    business_id: str
    duration_days: int = Field(..., ge=7, le=365)

class CampaignResponse(BaseModel):
    campaign_id: str
    calendar: List[Dict[str, Any]]
    created_at: datetime

class ContentGenerateRequest(BaseModel):
    campaign_id: str
    day: int = Field(..., ge=1, le=31)
    content_type: str = Field(..., pattern=r'^(text|image|video|reel|story|carousel)$')

class ContentResponse(BaseModel):
    content_id: str
    caption: str
    hashtags: List[str]
    script: Optional[Dict[str, Any]]
    estimated_engagement_score: float

class ContentScheduleRequest(BaseModel):
    content_id: str
    scheduled_at: datetime

class ContentScheduleResponse(BaseModel):
    status: str

class AnalyticsResponse(BaseModel):
    health_score: float
    engagement_rate: float
    top_content_type: str
    recommendations: List[str]

class MessageReplyRequest(BaseModel):
    business_id: str
    customer_message: str

class MessageReplyResponse(BaseModel):
    suggested_reply: str

# API Contract Implementation
class APIContract:
    """Enterprise-grade API contract implementation"""
    
    @staticmethod
    def success_response(data: Dict[str, Any], meta: Optional[Dict[str, Any]] = None) -> SuccessResponse:
        """Create standardized success response"""
        return SuccessResponse(
            data=data,
            meta=meta or MetaData()
        )
    
    @staticmethod
    def error_response(error_code: ErrorCode, message: str, details: Optional[Dict[str, Any]] = None) -> ErrorResponse:
        """Create standardized error response"""
        return ErrorResponse(
            error={
                "code": error_code.value,
                "message": message,
                "details": details or {}
            }
        )
    
    @staticmethod
    def validation_error_response(field: str, message: str, value: Any = None) -> ErrorResponse:
        """Create validation error response"""
        return APIContract.error_response(
            ErrorCode.VALIDATION_ERROR,
            message,
            {"field": field, "value": str(value) if value is not None else None}
        )
    
    @staticmethod
    def unauthorized_response(message: str = "Authentication required") -> ErrorResponse:
        """Create unauthorized response"""
        return APIContract.error_response(
            ErrorCode.UNAUTHORIZED,
            message
        )
    
    @staticmethod
    def forbidden_response(message: str = "Access denied") -> ErrorResponse:
        """Create forbidden response"""
        return APIContract.error_response(
            ErrorCode.FORBIDDEN,
            message
        )
    
    @staticmethod
    def not_found_response(resource: str = "Resource not found") -> ErrorResponse:
        """Create not found response"""
        return APIContract.error_response(
            ErrorCode.NOT_FOUND,
            resource
        )
    
    @staticmethod
    def rate_limited_response(retry_after: int = 60) -> ErrorResponse:
        """Create rate limited response"""
        return APIContract.error_response(
            ErrorCode.RATE_LIMITED,
            f"Rate limit exceeded. Retry after {retry_after} seconds"
        )
    
    @staticmethod
    def internal_error_response(message: str = "Internal server error") -> ErrorResponse:
        """Create internal error response"""
        return APIContract.error_response(
            ErrorCode.INTERNAL_ERROR,
            message
        )
    
    @staticmethod
    def service_unavailable_response(message: str = "Service temporarily unavailable") -> ErrorResponse:
        """Create service unavailable response"""
        return APIContract.error_response(
            ErrorCode.SERVICE_UNAVAILABLE,
            message
        )

# HTTP Status Code Mapping
STATUS_CODES = {
    # Success
    200: "OK",
    201: "Created",
    
    # Client Errors
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    429: "Too Many Requests",
    
    # Server Errors
    500: "Internal Server Error",
    503: "Service Unavailable"
}

# API Endpoint Specifications
class APIEndpoints:
    """API endpoint specifications following the contract"""
    
    # Authentication Endpoints
    AUTH_REGISTER = {
        "path": "/api/v1/auth/register",
        "method": "POST",
        "description": "Register new user",
        "request": RegisterRequest,
        "response": AuthResponse,
        "errors": [ErrorCode.EMAIL_ALREADY_EXISTS, ErrorCode.INVALID_PASSWORD]
    }
    
    AUTH_LOGIN = {
        "path": "/api/v1/auth/login",
        "method": "POST",
        "description": "Login user",
        "request": LoginRequest,
        "response": AuthResponse,
        "errors": [ErrorCode.INVALID_CREDENTIALS]
    }
    
    AUTH_ME = {
        "path": "/api/v1/auth/me",
        "method": "GET",
        "description": "Get current user profile",
        "response": Dict[str, Any],
        "errors": [ErrorCode.INVALID_TOKEN, ErrorCode.TOKEN_EXPIRED]
    }
    
    # Business Endpoints
    BUSINESS_CREATE = {
        "path": "/api/v1/business",
        "method": "POST",
        "description": "Create business",
        "request": BusinessCreateRequest,
        "response": BusinessResponse,
        "errors": [ErrorCode.INVALID_BUSINESS_DATA],
        "requires_auth": True
    }
    
    BUSINESS_GET_ALL = {
        "path": "/api/v1/business",
        "method": "GET",
        "description": "Get all businesses",
        "response": List[BusinessResponse],
        "requires_auth": True
    }
    
    BUSINESS_GET = {
        "path": "/api/v1/business/{business_id}",
        "method": "API/v1/business/{business_id}",
        "method": "GET",
        "description": "Get business details",
        "response": BusinessResponse,
        "errors": [ErrorCode.BUSINESS_NOT_FOUND],
        "requires_auth": True
    }
    
    BUSINESS_UPDATE = {
        "path": "/api/v1/business/{business_id}",
        "method": "PUT",
        "description": "Update business",
        "response": BusinessResponse,
        "errors": [ErrorCode.BUSINESS_NOT_FOUND, ErrorCode.INVALID_BUSINESS_DATA],
        "requires_auth": True
    }
    
    BUSINESS_DELETE = {
        "path": "/api/v1/business/{business_id}",
        "method": "DELETE",
        "description": "Delete business",
        "response": SuccessResponse,
        "errors": [ErrorCode.BUSINESS_NOT_FOUND],
        "requires_auth": True
    }
    
    # Campaign Endpoints
    CAMPAIGN_GENERATE = {
        "path": "/api/v1/campaign/generate",
        "method": "POST",
        "description": "Generate campaign strategy (AI)",
        "request": CampaignGenerateRequest,
        "response": CampaignResponse,
        "errors": [ErrorCode.BUSINESS_NOT_FOUND, ErrorCode.AI_GENERATION_FAILED],
        "requires_auth": True
    }
    
    CAMPAIGN_GET = {
        "path": "/api/v1/campaign/{campaign_id}",
        "method": "GET",
        "description": "Get campaign details",
        "response": CampaignResponse,
        "errors": [ErrorCode.CAMPAIGN_NOT_FOUND],
        "requires_auth": True
    }
    
    CAMPAIGN_LIST = {
        "path": "/api/v1/campaign",
        "method": "GET",
        "description": "List campaigns",
        "response": List[CampaignResponse],
        "requires_auth": True
    }
    
    # Content Endpoints
    CONTENT_GENERATE = {
        "path": "/api/v1/content/generate",
        "method": "POST",
        "description": "Generate content (AI)",
        "request": ContentGenerateRequest,
        "response": ContentResponse,
        "errors": [ErrorCode.CAMPAIGN_NOT_FOUND, ErrorCode.INVALID_CONTENT_TYPE, ErrorCode.AI_GENERATION_FAILED],
        "requires_auth": True
    }
    
    CONTENT_GET = {
        "path": "/api/v1/content/{content_id}",
        "method": "GET",
        "description": "Get content details",
        "response": ContentResponse,
        "errors": [ErrorCode.CONTENT_NOT_FOUND],
        "requires_auth": True
    }
    
    CONTENT_SCHEDULE = {
        "path": "/api/v1/content/schedule",
        "method": "POST",
        "description": "Schedule content",
        "request": ContentScheduleRequest,
        "response": ContentScheduleResponse,
        "errors": [ErrorCode.CONTENT_NOT_FOUND, ErrorCode.INVALID_SCHEDULE_TIME],
        "requires_auth": True
    }
    
    CONTENT_PUBLISH = {
        "path": "/api/v1/content/{content_id}/publish",
        "method": "POST",
        "description": "Publish content",
        "response": SuccessResponse,
        "errors": [ErrorCode.CONTENT_NOT_FOUND, ErrorCode.CONTENT_ALREADY_PUBLISHED],
        "requires_auth": True
    }
    
    # Analytics Endpoints
    ANALYTICS_BUSINESS = {
        "path": "/api/v1/analytics/{business_id}",
        "method": "GET",
        "description": "Get business analytics",
        "response": AnalyticsResponse,
        "errors": [ErrorCode.ANALYTICS_NOT_FOUND],
        "requires_auth": True
    }
    
    ANALYTICS_CONTENT = {
        "path": "/api/v1/analytics/content/{content_id}",
        "method": "GET",
        "description": "Get content analytics",
        "response": Dict[str, Any],
        "errors": [ErrorCode.ANALYTICS_NOT_FOUND],
        "requires_auth": True
    }
    
    ANALYTICS_CAMPAIGN = {
        "path": "/api/v1/analytics/campaign/{campaign_id}",
        "method": "GET",
        "description": "Get campaign analytics",
        "response": Dict[str, Any],
        "errors": [ErrorCode.ANALYTICS_NOT_FOUND],
        "requires_auth": True
    }
    
    ANALYTICS_HEALTH_SCORE = {
        "path": "/api/v1/analytics/health-score/{campaign_id}",
        "method": "GET",
        "description": "Get marketing health score",
        "response": Dict[str, Any],
        "errors": [ErrorCode.ANALYTICS_NOT_FOUND],
        "requires_auth": True
    }
    
    # Messaging Endpoints
    MESSAGES_LIST = {
        "path": "/api/v1/messages",
        "method": "GET",
        "description": "Get messages",
        "response": List[Dict[str, Any]],
        "requires_auth": True
    }
    
    MESSAGE_AI_REPLY = {
        "path": "/api/v1/message/reply",
        "method": "POST",
        "description": "Generate AI reply suggestion",
        "request": MessageReplyRequest,
        "response": MessageReplyResponse,
        "errors": [ErrorCode.INVALID_MESSAGE_DATA],
        "requires_auth": True
    }
    
    MESSAGE_MARK_REPLIED = {
        "path": "/api/v1/message/{message_id}/mark-replied",
        "method": "POST",
        "description": "Mark message as replied",
        "response": SuccessResponse,
        "errors": [ErrorCode.MESSAGE_NOT_FOUND],
        "requires_auth": True
    }

# Validation Rules
class ValidationRules:
    """Validation rules for API contracts"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        return True
    
    @staticmethod
    def validate_business_name(name: str) -> bool:
        """Validate business name"""
        return len(name.strip()) >= 2 and len(name.strip()) <= 100
    
    @staticmethod
    def validate_content_type(content_type: str) -> bool:
        """Validate content type"""
        valid_types = ["text", "image", "video", "reel", "story", "carousel"]
        return content_type.lower() in valid_types
    
    @staticmethod
    def validate_platform(platform: str) -> bool:
        """Validate platform"""
        valid_platforms = ["instagram", "linkedin", "email", "sms"]
        return platform.lower() in valid_platforms
    
    @staticmethod
    def validate_campaign_day(day: int) -> bool:
        """Validate campaign day"""
        return 1 <= day <= 31
    
    @staticmethod
    def validate_duration_days(days: int) -> bool:
        """Validate campaign duration"""
        return 7 <= days <= 365
    
    @staticmethod
    def validate_scheduled_time(scheduled_at: datetime) -> bool:
        """Validate scheduled time is in the future"""
        return scheduled_at > datetime.utcnow()
    
    @staticmethod
    def validate_engagement_score(score: float) -> bool:
        """Validate engagement score"""
        return 0.0 <= score <= 100.0

# Rate Limiting Configuration
RATE_LIMITS = {
    "/api/v1/auth/register": "5/minute",
    "/api/v1/auth/login": "5/minute",
    "/api/v1/business": "10/minute",
    "/api/v1/campaign": "10/minute",
    "/api/v1/content": "20/minute",
    "/api/v1/analytics": "30/minute",
    "/api/v1/messages": "50/minute",
    "/api/v1/message/reply": "10/minute"
}

# Request Context for Logging
class RequestContext:
    """Request context for logging and monitoring"""
    
    def __init__(self, request_id: str, user_id: Optional[str] = None, business_id: Optional[str] = None):
        self.request_id = request_id
        self.user_id = user_id
        self.business_id = business_id
        self.start_time = datetime.utcnow()
        self.ip_address = None
        self.user_agent = None
    
    def get_processing_time(self) -> int:
        """Get processing time in milliseconds"""
        return int((datetime.utcnow() - self.start_time).total_seconds() * 1000)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging"""
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "business_id": self.business_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "processing_time_ms": self.get_processing_time()
        }

# Contract Enforcement Decorator
def enforce_contract(endpoint_spec: Dict[str, Any]):
    """Decorator to enforce API contract"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would be implemented in the actual API routes
            # For now, it's a placeholder
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Contract Validation
def validate_request(request_data: Dict[str, Any], endpoint_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Validate request against contract specification"""
    # This would implement actual validation logic
    # For now, return the data as-is
    return request_data

# Response Formatting
def format_response(data: Dict[str, Any], endpoint_spec: Dict[str, Any], meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Format response according to contract specification"""
    return APIContract.success_response(data, meta)

# Error Formatting
def format_error(error_code: ErrorCode, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Format error according to contract specification"""
    return APIContract.error_response(error_code, message, details)

# HTTP Status Code Helper
def get_status_code(error_code: ErrorCode) -> int:
    """Get HTTP status code for error code"""
    status_mapping = {
        ErrorCode.EMAIL_ALREADY_EXISTS: 409,
        ErrorCode.INVALID_PASSWORD: 400,
        ErrorCode.INVALID_CREDENTIALS: 401,
        ErrorCode.TOKEN_EXPIRED: 401,
        ErrorCode.INVALID_TOKEN: 401,
        ErrorCode.BUSINESS_NOT_FOUND: 404,
        ErrorCode.CAMPAIGN_NOT_FOUND: 404,
        ErrorCode.AI_GENERATION_FAILED: 503,
        ErrorCode.CONTENT_NOT_FOUND: 404,
        ErrorCode.INVALID_CONTENT_TYPE: 400,
        ErrorCode.CONTENT_ALREADY_PUBLISHED: 409,
        ErrorCode.INVALID_SCHEDULE_TIME: 400,
        ErrorCode.ANALYTICS_NOT_FOUND: 404,
        ErrorCode.INVALID_ANALYTICS_REQUEST: 400,
        ErrorCode.MESSAGE_NOT_FOUND: 404,
        ErrorCode.INVALID_MESSAGE_DATA: 400,
        ErrorCode.VALIDATION_ERROR: 400,
        ErrorCode.UNAUTHORIZED: 401,
        ErrorCode.FORBIDDEN: 403,
        ErrorCode.NOT_FOUND: 404,
        ErrorCode.RATE_LIMITED: 429,
        ErrorCode.INTERNAL_ERROR: 500,
        ErrorCode.SERVICE_UNAVAILABLE: 503
    }
    return status_mapping.get(error_code, 500)

# Global API Contract Instance
api_contract = APIContract()
