"""
Response Schemas
Pydantic models for API response formatting
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# Base Response Schema
class BaseResponse(BaseModel):
    """Base response schema"""
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SuccessResponse(BaseResponse):
    """Success response schema"""
    data: Optional[Dict[str, Any]] = None
    message: str = "Operation successful"

class ErrorResponse(BaseResponse):
    """Error response schema"""
    success: bool = False
    error: Dict[str, Any]
    message: str = "Operation failed"

# Authentication Responses
class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: str
    full_name: str
    first_name: str
    last_name: str
    picture: Optional[str] = None
    provider: str
    provider_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

class AuthResponse(BaseModel):
    """Authentication response schema"""
    token: str
    refresh_token: str
    expires_in: int
    user: UserResponse
    business: Optional[Dict[str, Any]] = None

# Business Responses
class BusinessResponse(BaseModel):
    """Business response schema"""
    id: str
    owner_id: str
    name: str
    industry: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    plan: str
    target_audience: Dict[str, Any]
    brand_voice: str
    brand_colors: List[str]
    brand_guidelines: Optional[str] = None
    content_preferences: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class BusinessListResponse(BaseModel):
    """Business list response schema"""
    businesses: List[BusinessResponse]
    total: int
    page: int
    limit: int
    has_next: bool

# Campaign Responses
class CampaignResponse(BaseModel):
    """Campaign response schema"""
    id: str
    business_id: str
    name: str
    description: Optional[str] = None
    status: str
    duration_days: int
    start_date: datetime
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    primary_goal: str
    secondary_goals: List[str]
    target_audience: Dict[str, Any]
    ai_strategy: Optional[Dict[str, Any]]
    weekly_themes: List[Dict[str, Any]]
    kpi_targets: Dict[str, Any]
    media_mix: Dict[str, float]
    total_engagement: int
    total_impressions: int
    total_conversions: int
    created_at: datetime
    updated_at: datetime

class CampaignListResponse(BaseModel):
    """Campaign list response schema"""
    campaigns: List[CampaignResponse]
    total: int
    page: int
    limit: int
    has_next: bool

# Content Responses
class ContentResponse(BaseModel):
    """Content response schema"""
    id: str
    campaign_id: str
    business_id: str
    title: str
    content_type: str
    platform: str
    text_content: Optional[str] = None
    visual_description: Optional[str] = None
    script: Optional[Dict[str, Any]] = None
    hashtags: List[str]
    call_to_action: Optional[str] = None
    media_urls: List[str]
    thumbnail_url: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    published_date: Optional[datetime] = None
    status: str
    ai_generated: bool
    ai_prompt_used: Optional[str] = None
    ai_model_used: Optional[str] = None
    predicted_engagement_score: Optional[float] = None
    engagement_count: int
    impression_count: int
    click_count: int
    conversion_count: int
    sentiment_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

class ContentListResponse(BaseModel):
    """Content list response schema"""
    contents: List[ContentResponse]
    total: int
    page: int
    limit: int
    has_next: bool

# Analytics Responses
class AnalyticsResponse(BaseModel):
    """Analytics response schema"""
    content_id: str
    business_id: str
    campaign_id: Optional[str] = None
    date: datetime
    platform: str
    impressions: int
    engagement: int
    clicks: int
    shares: int
    comments: int
    conversions: int
    engagement_rate: float
    click_through_rate: float
    conversion_rate: float
    audience_demographics: Dict[str, Any]
    ai_insights: Optional[Dict[str, Any]]
    performance_grade: Optional[str]

class AnalyticsSummaryResponse(BaseModel):
    """Analytics summary response schema"""
    total_impressions: int
    total_engagement: int
    total_clicks: int
    total_conversions: int
    average_engagement_rate: float
    average_ctr: float
    average_conversion_rate: float
    top_performing_content: List[Dict[str, Any]]
    platform_performance: Dict[str, Any]
    content_type_performance: Dict[str, Any]
    trend_data: List[Dict[str, Any]]

# Message Responses
class MessageResponse(BaseModel):
    """Message response schema"""
    id: str
    business_id: str
    platform: str
    sender: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    subject: Optional[str] = None
    content: str
    media_urls: List[str]
    thread_id: Optional[str] = None
    reply_to_message_id: Optional[str] = None
    is_read: bool
    is_archived: bool
    is_flagged: bool
    priority: str
    ai_generated: bool
    ai_suggested_reply: Optional[str] = None
    ai_sentiment: Optional[str] = None
    ai_category: Optional[str] = None
    received_at: datetime
    replied_at: Optional[datetime] = None

class MessageListResponse(BaseModel):
    """Message list response schema"""
    messages: List[MessageResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    unread_count: int

class MessageThreadResponse(BaseModel):
    """Message thread response schema"""
    thread_id: str
    platform: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    messages: List[MessageResponse]
    last_message_at: datetime
    message_count: int
    unread_count: int
    priority: str
    status: str

# AI Service Responses
class AIStrategyResponse(BaseModel):
    """AI strategy response schema"""
    campaign_calendar: List[Dict[str, Any]]
    weekly_themes: List[Dict[str, Any]]
    content_distribution: Dict[str, Any]
    kpi_recommendations: List[Dict[str, Any]]
    media_mix_optimization: Dict[str, Any]
    success_probability: float
    estimated_cost: float

class AIContentResponse(BaseModel):
    """AI content response schema"""
    content_type: str
    platform: str
    title: str
    text_content: str
    visual_description: Optional[str] = None
    script: Optional[Dict[str, Any]] = None
    hashtags: List[str]
    call_to_action: Optional[str] = None
    image_generation_prompt: Optional[str] = None
    predicted_engagement_score: float
    tone_analysis: str
    character_count: int
    estimated_cost: float

class AIAnalyticsResponse(BaseModel):
    """AI analytics response schema"""
    performance_summary: Dict[str, Any]
    top_performing_content: List[Dict[str, Any]]
    weak_segments: List[Dict[str, Any]]
    optimization_opportunities: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    success_metrics: Dict[str, Any]
    estimated_cost: float

class AIMessageResponse(BaseModel):
    """AI message response schema"""
    response_type: str
    platform: str
    reply_text: str
    tone: str
    escalation_needed: bool
    follow_up_required: bool
    sentiment: str
    confidence_score: float
    next_action: str
    estimated_cost: float

# Health Check Responses
class HealthCheckResponse(BaseModel):
    """Health check response schema"""
    status: str
    timestamp: datetime
    version: str
    environment: str
    database: Dict[str, Any]
    ai_service: Dict[str, Any]
    uptime_seconds: int
    memory_usage: Dict[str, Any]
    cpu_usage: Dict[str, Any]

# System Info Responses
class SystemInfoResponse(BaseModel):
    """System info response schema"""
    app_name: str
    version: str
    environment: str
    uptime_seconds: int
    database_status: str
    ai_service_status: str
    active_users: int
    total_campaigns: int
    total_content: int
    total_messages: int
    ai_requests_today: int
    ai_cost_today: float

# Export Responses
class ExportResponse(BaseModel):
    """Export response schema"""
    export_id: str
    export_type: str
    data_type: str
    status: str  # 'pending', 'processing', 'completed', 'failed'
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    record_count: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

# Search Responses
class SearchResult(BaseModel):
    """Search result schema"""
    id: str
    type: str  # 'campaign', 'content', 'message', 'business'
    title: str
    description: Optional[str] = None
    relevance_score: float
    highlights: List[str]
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    """Search response schema"""
    results: List[SearchResult]
    total: int
    page: int
    limit: int
    has_next: bool
    search_time_ms: float

# Bulk Operation Responses
class BulkOperationResponse(BaseModel):
    """Bulk operation response schema"""
    operation_id: str
    operation_type: str
    total_items: int
    processed_items: int
    successful_items: int
    failed_items: int
    status: str  # 'pending', 'processing', 'completed', 'failed'
    errors: List[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime] = None

# Validation Responses
class ValidationErrorDetail(BaseModel):
    """Validation error detail schema"""
    field: str
    message: str
    value: Optional[Any] = None

class ValidationErrorResponse(BaseModel):
    """Validation error response schema"""
    errors: List[ValidationErrorDetail]
    message: str = "Validation failed"

# Rate Limit Responses
class RateLimitResponse(BaseModel):
    """Rate limit response schema"""
    limit: int
    remaining: int
    reset_time: datetime
    retry_after: int

# File Upload Responses
class FileUploadResponse(BaseModel):
    """File upload response schema"""
    file_id: str
    filename: str
    file_size: int
    file_type: str
    file_url: str
    thumbnail_url: Optional[str] = None
    uploaded_at: datetime

# Notification Responses
class NotificationResponse(BaseModel):
    """Notification response schema"""
    id: str
    type: str  # 'info', 'success', 'warning', 'error'
    title: str
    message: str
    data: Optional[Dict[str, Any]] = None
    read: bool
    created_at: datetime
    expires_at: Optional[datetime] = None

# Pagination Metadata
class PaginationMeta(BaseModel):
    """Pagination metadata schema"""
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

# API Metadata
class APIMetadata(BaseModel):
    """API metadata schema"""
    version: str
    environment: str
    timestamp: datetime
    request_id: str
    processing_time_ms: float
    rate_limit: Optional[RateLimitResponse] = None
