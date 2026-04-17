"""
Request Schemas
Pydantic models for API request validation
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime

# Authentication Schemas
class LoginRequest(BaseModel):
    """Login request schema"""
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

class RegisterRequest(BaseModel):
    """Register request schema"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    business: Optional[Dict[str, Any]] = None
    
    @validator('full_name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class OAuthCallbackRequest(BaseModel):
    """OAuth callback request schema"""
    code: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)

# Business Schemas
class BusinessCreateRequest(BaseModel):
    """Business creation request schema"""
    name: str = Field(..., min_length=2, max_length=100)
    industry: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = None
    
    # Target audience
    target_audience: Optional[Dict[str, Any]] = None
    
    # Brand preferences
    brand_voice: str = "Professional"
    brand_colors: Optional[List[str]] = None
    
    # Content preferences
    content_preferences: Optional[Dict[str, Any]] = None

class BusinessUpdateRequest(BaseModel):
    """Business update request schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    industry: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = None
    
    # Target audience
    target_audience: Optional[Dict[str, Any]] = None
    
    # Brand preferences
    brand_voice: Optional[str] = None
    brand_colors: Optional[List[str]] = None
    
    # Content preferences
    content_preferences: Optional[Dict[str, Any]] = None

# Campaign Schemas
class CampaignCreateRequest(BaseModel):
    """Campaign creation request schema"""
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    duration_days: int = Field(30, ge=7, le=365)
    start_date: datetime
    primary_goal: str = Field(..., min_length=2, max_length=100)
    secondary_goals: Optional[List[str]] = None
    budget: Optional[float] = Field(None, ge=0)
    
    # Target audience
    target_audience: Optional[Dict[str, Any]] = None
    
    # Content preferences
    content_types: Optional[List[str]] = None
    platforms: Optional[List[str]] = None

class CampaignUpdateRequest(BaseModel):
    """Campaign update request schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = Field(None, ge=0)
    
    # Target audience
    target_audience: Optional[Dict[str, Any]] = None
    
    # Content preferences
    content_types: Optional[List[str]] = None
    platforms: Optional[List[str]] = None

# Content Schemas
class ContentCreateRequest(BaseModel):
    """Content creation request schema"""
    campaign_id: str
    title: str = Field(..., min_length=2, max_length=200)
    content_type: str = Field(..., min_length=2, max_length=50)
    platform: str = Field(..., min_length=2, max_length=50)
    
    # Content data
    text_content: Optional[str] = Field(None, max_length=2000)
    visual_description: Optional[str] = Field(None, max_length=500)
    script: Optional[Dict[str, Any]] = None
    hashtags: Optional[List[str]] = None
    call_to_action: Optional[str] = Field(None, max_length=200)
    
    # Scheduling
    scheduled_date: Optional[datetime] = None
    
    # AI generation options
    ai_generate: bool = False
    ai_prompt: Optional[str] = None

class ContentUpdateRequest(BaseModel):
    """Content update request schema"""
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    text_content: Optional[str] = Field(None, max_length=2000)
    visual_description: Optional[str] = Field(None, max_length=500)
    script: Optional[Dict[str, Any]] = None
    hashtags: Optional[List[str]] = None
    call_to_action: Optional[str] = Field(None, max_length=200)
    
    # Scheduling
    scheduled_date: Optional[datetime] = None
    status: Optional[str] = None

class ContentGenerateRequest(BaseModel):
    """Content generation request schema"""
    content_type: str = Field(..., min_length=2, max_length=50)
    platform: str = Field(..., min_length=2, max_length=50)
    topic: Optional[str] = Field(None, max_length=200)
    tone: Optional[str] = "Professional"
    length: Optional[str] = "medium"  # 'short', 'medium', 'long'
    include_hashtags: bool = True
    include_cta: bool = True

# AI Service Schemas
class AIStrategyRequest(BaseModel):
    """AI strategy generation request schema"""
    campaign_goal: str = Field(..., min_length=2, max_length=100)
    duration_days: int = Field(30, ge=7, le=365)
    industry: str = Field(..., min_length=2, max_length=50)
    target_audience: Optional[Dict[str, Any]] = None
    brand_voice: Optional[str] = "Professional"
    platforms: Optional[List[str]] = None
    content_types: Optional[List[str]] = None

class AIContentRequest(BaseModel):
    """AI content generation request schema"""
    content_type: str = Field(..., min_length=2, max_length=50)
    platform: str = Field(..., min_length=2, max_length=50)
    topic: str = Field(..., min_length=2, max_length=200)
    tone: Optional[str] = "Professional"
    brand_voice: Optional[str] = None
    target_audience: Optional[Dict[str, Any]] = None
    length: Optional[str] = "medium"
    include_hashtags: bool = True
    include_cta: bool = True

class AIAnalyticsRequest(BaseModel):
    """AI analytics request schema"""
    campaign_id: Optional[str] = None
    business_id: Optional[str] = None
    date_range: Optional[Dict[str, Any]] = None
    metrics: Optional[List[str]] = None
    focus_area: Optional[str] = None  # 'engagement', 'conversion', 'reach', 'sentiment'

class AIMessageRequest(BaseModel):
    """AI message reply request schema"""
    message_id: str
    platform: str = Field(..., min_length=2, max_length=50)
    message_content: str = Field(..., min_length=1, max_length=1000)
    conversation_context: Optional[List[Dict[str, Any]]] = None
    brand_voice: Optional[str] = "Professional"
    tone: Optional[str] = "Professional"

# Analytics Schemas
class AnalyticsRequest(BaseModel):
    """Analytics request schema"""
    business_id: Optional[str] = None
    campaign_id: Optional[str] = None
    content_id: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    metrics: Optional[List[str]] = None
    group_by: Optional[str] = None  # 'day', 'week', 'month', 'platform', 'content_type'

class AnalyticsSimulateRequest(BaseModel):
    """Analytics simulation request schema"""
    campaign_id: str
    days_to_simulate: int = Field(30, ge=1, le=365)
    base_engagement_rate: float = Field(0.05, ge=0.0, le=1.0)
    content_count: int = Field(10, ge=1, le=100)
    platforms: Optional[List[str]] = None

# Messaging Schemas
class MessageSendRequest(BaseModel):
    """Message send request schema"""
    platform: str = Field(..., min_length=2, max_length=50)
    recipient_id: Optional[str] = None
    recipient_email: Optional[EmailStr] = None
    subject: Optional[str] = Field(None, max_length=200)
    content: str = Field(..., min_length=1, max_length=2000)
    media_urls: Optional[List[str]] = None
    thread_id: Optional[str] = None
    priority: str = "normal"  # 'low', 'normal', 'high', 'urgent'

class MessageReplyRequest(BaseModel):
    """Message reply request schema"""
    message_id: str
    content: str = Field(..., min_length=1, max_length=2000)
    media_urls: Optional[List[str]] = None
    ai_suggested: bool = False

class MessageAIReplyRequest(BaseModel):
    """AI message reply request schema"""
    message_id: str
    tone: Optional[str] = "Professional"
    brand_voice: Optional[str] = None
    include_cta: bool = False
    max_length: int = Field(500, ge=50, le=2000)

# General Schemas
class PaginationRequest(BaseModel):
    """Pagination request schema"""
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"  # 'asc', 'desc'

class SearchRequest(BaseModel):
    """Search request schema"""
    query: str = Field(..., min_length=1, max_length=100)
    filters: Optional[Dict[str, Any]] = None
    pagination: Optional[PaginationRequest] = None

# Bulk Operations Schemas
class BulkContentCreateRequest(BaseModel):
    """Bulk content creation request schema"""
    campaign_id: str
    contents: List[ContentCreateRequest]
    
    @validator('contents')
    def validate_contents(cls, v):
        if len(v) == 0:
            raise ValueError('At least one content item is required')
        if len(v) > 50:
            raise ValueError('Maximum 50 content items allowed per bulk request')
        return v

class BulkPublishRequest(BaseModel):
    """Bulk publish request schema"""
    content_ids: List[str]
    publish_date: Optional[datetime] = None
    
    @validator('content_ids')
    def validate_content_ids(cls, v):
        if len(v) == 0:
            raise ValueError('At least one content ID is required')
        if len(v) > 100:
            raise ValueError('Maximum 100 content items allowed per bulk publish')
        return v

# Export Schemas
class ExportRequest(BaseModel):
    """Export request schema"""
    export_type: str = Field(..., min_length=2, max_length=50)  # 'csv', 'json', 'pdf'
    data_type: str = Field(..., min_length=2, max_length=50)  # 'campaigns', 'content', 'analytics', 'messages'
    filters: Optional[Dict[str, Any]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    include_media: bool = False

# ==================== AI SERVICE REQUEST SCHEMAS ====================

# Strategy AI Schemas
class CampaignCalendarRequest(BaseModel):
    """Campaign calendar generation request"""
    business_id: str
    business_name: Optional[str] = None
    industry: Optional[str] = None
    brand_voice: Optional[str] = None
    target_audience: Optional[str] = None
    campaign_goal: Optional[str] = None
    duration_days: Optional[int] = Field(30, ge=7, le=365)
    platforms: Optional[List[str]] = None
    content_types: Optional[List[str]] = None

class KPIGeneratorRequest(BaseModel):
    """KPI generation request"""
    business_id: str
    business_name: Optional[str] = None
    industry: Optional[str] = None
    campaign_goal: Optional[str] = None
    target_audience: Optional[str] = None
    duration_days: Optional[int] = Field(30, ge=7, le=365)

class MediaMixOptimizerRequest(BaseModel):
    """Media mix optimization request"""
    business_id: str
    performance_data: Optional[Dict[str, Any]] = None
    platform_performance: Optional[Dict[str, Any]] = None
    content_type_performance: Optional[Dict[str, Any]] = None

# Content AI Schemas
class TextContentRequest(BaseModel):
    """Text content generation request"""
    business_id: str
    business_name: Optional[str] = None
    industry: Optional[str] = None
    brand_voice: Optional[str] = None
    target_audience: Optional[str] = None
    topic: Optional[str] = None
    platform: Optional[str] = "instagram"
    tone: Optional[str] = "engaging"
    length: Optional[str] = "medium"
    character_limit: Optional[int] = 150

class VisualContentRequest(BaseModel):
    """Visual content generation request"""
    business_id: str
    business_name: Optional[str] = None
    industry: Optional[str] = None
    brand_colors: Optional[List[str]] = None
    brand_guidelines: Optional[str] = None
    target_audience: Optional[str] = None
    topic: Optional[str] = None
    platform: Optional[str] = "instagram"
    visual_style: Optional[str] = "modern and clean"

class VideoContentRequest(BaseModel):
    """Video content generation request"""
    business_id: str
    business_name: Optional[str] = None
    industry: Optional[str] = None
    brand_voice: Optional[str] = None
    target_audience: Optional[str] = None
    topic: Optional[str] = None
    platform: Optional[str] = "instagram"
    duration_seconds: Optional[int] = Field(30, ge=15, le=300)
    script_style: Optional[str] = "conversational"

# Analytics AI Schemas
class AnalyticsRequest(BaseModel):
    """Performance analytics request"""
    business_id: str
    performance_data: Optional[Dict[str, Any]] = None
    platform_performance: Optional[Dict[str, Any]] = None
    content_type_performance: Optional[Dict[str, Any]] = None
    time_period: Optional[str] = "last 30 days"
    campaign_goals: Optional[str] = "engagement and growth"

# Messaging AI Schemas
class CustomerReplyRequest(BaseModel):
    """Customer reply generation request"""
    business_id: str
    business_name: Optional[str] = None
    brand_voice: Optional[str] = None
    industry: Optional[str] = None
    customer_message: str = Field(..., min_length=1)
    conversation_history: Optional[str] = None
    platform: Optional[str] = "instagram"
    customer_profile: Optional[Dict[str, Any]] = None
