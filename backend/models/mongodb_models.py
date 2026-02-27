"""
MongoDB Models for AI Marketing Command Center
Implements the database schema as defined in design documents
Using Beanie ODM for type-safe MongoDB operations
"""

from beanie import Document, Indexed, Link, before_event, Replace, Insert, Update
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Dict, Any, Union, Literal
from datetime import datetime, timezone
from enum import Enum
import pymongo
from bson import ObjectId

# Enums for validation
class UserRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin" 
    EDITOR = "editor"
    VIEWER = "viewer"

class BusinessPlan(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class ContentStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    ARCHIVED = "archived"

class Platform(str, Enum):
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    EMAIL = "email"
    SMS = "sms"

class ContentType(str, Enum):
    POST = "post"
    STORY = "story"
    REEL = "reel"
    CAROUSEL = "carousel"
    VIDEO = "video"
    LIVE = "live"
    EMAIL_TEMPLATE = "email"
    SMS_TEMPLATE = "sms"

# Embedded Documents
class BusinessProfile(BaseModel):
    """Business profile information embedded in Business document"""
    name: str = Field(..., min_length=1, max_length=100)
    industry: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    target_audience: Optional[str] = Field(None, max_length=300)
    brand_voice: Optional[str] = Field(None, max_length=200)
    website: Optional[str] = None
    logo_url: Optional[str] = None

class SocialMediaAccounts(BaseModel):
    """Social media accounts configuration"""
    instagram_handle: Optional[str] = None
    linkedin_page: Optional[str] = None
    twitter_handle: Optional[str] = None
    tiktok_handle: Optional[str] = None
    youtube_channel: Optional[str] = None

class AIMetadata(BaseModel):
    """AI generation metadata embedded in content"""
    model_used: str = Field(default="gpt-4o-mini")
    prompt_version: str = Field(default="1.0")
    generation_time: float = Field(default=0.0)
    tokens_used: int = Field(default=0)
    cost: float = Field(default=0.0)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    regenerated: bool = Field(default=False)
    regeneration_count: int = Field(default=0)
    human_feedback: Optional[str] = None

class PerformanceMetrics(BaseModel):
    """Content performance metrics"""
    views: int = Field(default=0)
    likes: int = Field(default=0)
    comments: int = Field(default=0)
    shares: int = Field(default=0)
    clicks: int = Field(default=0)
    engagement_rate: float = Field(default=0.0)
    reach: int = Field(default=0)
    impressions: int = Field(default=0)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Main Document Models
class User(Document):
    """User Collection - Authentication and profile"""
    email: Indexed(EmailStr, unique=True) = Field(...)
    password_hash: str = Field(...)
    full_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    plan: BusinessPlan = Field(default=BusinessPlan.FREE)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None
    
    # Subscription info
    subscription_expires: Optional[datetime] = None
    trial_ends: Optional[datetime] = None
    
    # Preferences
    timezone: str = Field(default="UTC")
    language: str = Field(default="en")
    notifications_enabled: bool = Field(default=True)

    @before_event([Replace, Insert, Update])
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "users"
        indexes = [
            [("email", pymongo.ASCENDING)],
            [("created_at", pymongo.DESCENDING)],
        ]

class Business(Document):
    """Business Collection - Business profiles and settings"""
    owner: Link[User] = Field(...)
    profile: BusinessProfile = Field(...)
    social_accounts: Optional[SocialMediaAccounts] = Field(default_factory=SocialMediaAccounts)
    
    # Business health metrics
    total_campaigns: int = Field(default=0)
    active_campaigns: int = Field(default=0)
    total_content: int = Field(default=0)
    monthly_content: int = Field(default=0)
    health_score: float = Field(default=0.0, ge=0.0, le=100.0)
    
    # Settings
    ai_preferences: Dict[str, Any] = Field(default_factory=dict)
    content_guidelines: Optional[str] = Field(None, max_length=1000)
    approval_required: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @before_event([Replace, Insert, Update])
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "businesses"
        indexes = [
            [("owner", pymongo.ASCENDING)],
            [("profile.name", pymongo.TEXT)],
            [("created_at", pymongo.DESCENDING)],
        ]

class Campaign(Document):
    """Campaign Collection - Marketing campaigns"""
    business: Link[Business] = Field(...)
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: CampaignStatus = Field(default=CampaignStatus.DRAFT)
    
    # Campaign configuration
    platforms: List[Platform] = Field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    posting_schedule: Dict[str, Any] = Field(default_factory=dict)
    
    # AI-generated strategy
    ai_strategy: Optional[Dict[str, Any]] = Field(default=None)
    ai_metadata: Optional[AIMetadata] = Field(default=None)
    
    # Performance tracking
    total_posts: int = Field(default=0)
    published_posts: int = Field(default=0)
    pending_posts: int = Field(default=0)
    
    # KPIs and goals
    target_reach: Optional[int] = Field(None, gt=0)
    target_engagement: Optional[float] = Field(None, gt=0)
    budget: Optional[float] = Field(None, gt=0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @before_event([Replace, Insert, Update])
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "campaigns"
        indexes = [
            [("business", pymongo.ASCENDING)],
            [("status", pymongo.ASCENDING)],
            [("start_date", pymongo.DESCENDING)],
            [("created_at", pymongo.DESCENDING)],
        ]

class Content(Document):
    """Content Collection - Generated content pieces"""
    campaign: Link[Campaign] = Field(...)
    business: Link[Business] = Field(...)
    
    # Content details
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    content_type: ContentType = Field(...)
    platform: Platform = Field(...)
    status: ContentStatus = Field(default=ContentStatus.DRAFT)
    
    # Scheduling
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    
    # Visual content
    image_urls: List[str] = Field(default_factory=list)
    video_url: Optional[str] = None
    hashtags: List[str] = Field(default_factory=list)
    mentions: List[str] = Field(default_factory=list)
    
    # AI generation data
    ai_metadata: Optional[AIMetadata] = Field(default=None)
    
    # Performance metrics
    performance: Optional[PerformanceMetrics] = Field(default=None)
    
    # Human oversight
    reviewed_by: Optional[Link[User]] = None
    review_notes: Optional[str] = None
    approved_at: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @before_event([Replace, Insert, Update])
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "contents"
        indexes = [
            [("campaign", pymongo.ASCENDING)],
            [("business", pymongo.ASCENDING)],
            [("status", pymongo.ASCENDING)],
            [("platform", pymongo.ASCENDING)],
            [("scheduled_time", pymongo.ASCENDING)],
            [("created_at", pymongo.DESCENDING)],
        ]

class Message(Document):
    """Messages Collection - Customer communications"""
    business: Link[Business] = Field(...)
    platform: Platform = Field(...)
    
    # Message details
    customer_name: Optional[str] = Field(None, max_length=100)
    customer_handle: Optional[str] = Field(None, max_length=100)
    customer_email: Optional[EmailStr] = None
    
    # Message content
    original_message: str = Field(..., min_length=1)
    ai_suggested_reply: Optional[str] = None
    actual_reply: Optional[str] = None
    
    # Status and metadata
    is_read: bool = Field(default=False)
    is_resolved: bool = Field(default=False)
    priority: Literal["low", "medium", "high"] = Field(default="medium")
    tags: List[str] = Field(default_factory=list)
    
    # AI processing
    ai_category: Optional[str] = None
    ai_sentiment: Optional[str] = None
    ai_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    # Response tracking
    responded_at: Optional[datetime] = None
    response_time_minutes: Optional[int] = None
    
    # Timestamps
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @before_event([Replace, Insert, Update])
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "messages"
        indexes = [
            [("business", pymongo.ASCENDING)],
            [("is_read", pymongo.ASCENDING)],
            [("priority", pymongo.ASCENDING)],
            [("received_at", pymongo.DESCENDING)],
        ]

class Analytics(Document):
    """Analytics Collection - Performance metrics aggregation"""
    business: Link[Business] = Field(...)
    campaign: Optional[Link[Campaign]] = None
    
    # Time period
    date: datetime = Field(...)
    period_type: Literal["daily", "weekly", "monthly"] = Field(...)
    
    # Aggregated metrics
    total_posts: int = Field(default=0)
    total_views: int = Field(default=0)
    total_likes: int = Field(default=0)
    total_comments: int = Field(default=0)
    total_shares: int = Field(default=0)
    total_clicks: int = Field(default=0)
    total_reach: int = Field(default=0)
    total_impressions: int = Field(default=0)
    
    # Calculated metrics
    average_engagement_rate: float = Field(default=0.0)
    growth_rate: float = Field(default=0.0)
    performance_score: float = Field(default=0.0, ge=0.0, le=100.0)
    
    # Platform breakdown
    platform_metrics: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    
    # AI insights
    ai_insights: Optional[List[str]] = Field(default_factory=list)
    recommendations: Optional[List[str]] = Field(default_factory=list)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @before_event([Replace, Insert, Update])
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "analytics"
        indexes = [
            [("business", pymongo.ASCENDING)],
            [("date", pymongo.DESCENDING)],
            [("period_type", pymongo.ASCENDING)],
        ]

class AILog(Document):
    """AI Logs Collection - Track AI service usage and costs"""
    business: Optional[Link[Business]] = None
    user: Optional[Link[User]] = None
    
    # Request details
    service_type: str = Field(..., max_length=50)  # "content_generation", "strategy_planning", etc.
    model_used: str = Field(..., max_length=50)
    input_tokens: int = Field(default=0)
    output_tokens: int = Field(default=0)
    total_tokens: int = Field(default=0)
    
    # Cost tracking
    cost_usd: float = Field(default=0.0)
    
    # Performance metrics
    response_time_ms: int = Field(default=0)
    success: bool = Field(default=True)
    error_message: Optional[str] = None
    
    # Context
    endpoint: str = Field(..., max_length=100)
    prompt_hash: Optional[str] = Field(None, max_length=64)  # For deduplication
    
    # Timestamps
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "ai_logs"
        indexes = [
            [("business", pymongo.ASCENDING)],
            [("timestamp", pymongo.DESCENDING)],
            [("service_type", pymongo.ASCENDING)],
        ]

# Document list for Beanie initialization
document_models = [
    User,
    Business,
    Campaign,
    Content,
    Message,
    Analytics,
    AILog
]