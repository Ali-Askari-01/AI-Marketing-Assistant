"""
Database Models and ORM Configuration
SQLite models with proper relationships, indexing, and repository patterns
Production-ready implementation with advanced features
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import BaseModel, Field, EmailStr, validator
import uuid
import json
import logging
from enum import Enum
import sqlite3
from contextlib import contextmanager

# Configure logging
logger = logging.getLogger(__name__)

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
    CAPTION = "caption"
    EMAIL_TEMPLATE = "email"
    SMS_TEMPLATE = "sms"
    POST_IDEA = "post_idea"

# SQLAlchemy Base
Base = declarative_base()

# Database Connection Manager
class DatabaseManager:
    """Advanced SQLite Database Manager with SQLAlchemy ORM"""
    
    def __init__(self, database_url: str = "sqlite:///./aimarketing.db"):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self._connected = False
    
    def connect(self):
        """Establish database connection"""
        try:
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},  # SQLite specific
                echo=False  # Set to True for SQL debugging
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            self._connected = True
            
            logger.info(f"Connected to SQLite database: {self.database_url}")
                
        except SQLAlchemyError as e:
            logger.error(f"Failed to connect to SQLite: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            self._connected = False
            logger.info("SQLite connection closed")
    
    @contextmanager
    def get_session(self):
        """Get database session with automatic cleanup"""
        if not self._connected:
            self.connect()
        
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

# SQLAlchemy Models
class User(Base):
    """User model with comprehensive authentication and profile features"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    picture = Column(String)
    provider = Column(String, default="email")  # 'google', 'microsoft', 'email'
    provider_id = Column(String)
    password_hash = Column(String)
    role = Column(String, default="owner")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    login_count = Column(Integer, default=0)
    timezone = Column(String, default="UTC")
    language = Column(String, default="en")
    
    # Subscription & Billing
    subscription_plan = Column(String, default="free")
    subscription_expires_at = Column(DateTime)
    trial_ends_at = Column(DateTime)
    
    # Usage Statistics
    businesses_created = Column(Integer, default=0)
    campaigns_created = Column(Integer, default=0)
    content_generated = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    businesses = relationship("Business", back_populates="owner", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_email', email),
        Index('idx_user_provider', provider, provider_id),
        Index('idx_user_created', created_at),
    )

class Business(Base):
    """Enhanced business model with comprehensive features"""
    __tablename__ = "businesses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    description = Column(Text)
    website = Column(String)
    logo_url = Column(String)
    plan = Column(String, default="free")
    
    # Contact Information
    contact_email = Column(String)
    phone_number = Column(String)
    address = Column(JSON)  # Store as JSON
    
    # Target audience and preferences stored as JSON
    target_audience = Column(JSON, default=lambda: {
        "age_range": "25-45",
        "gender_focus": "All", 
        "location": "Global",
        "interests": [],
        "income_level": "Middle",
        "education_level": "College",
        "lifestyle": []
    })
    
    # Brand identity
    brand_voice = Column(String, default="Professional")
    brand_colors = Column(JSON, default=list)  # Store as JSON array
    brand_guidelines = Column(Text)
    brand_keywords = Column(JSON, default=list)
    brand_values = Column(JSON, default=list)
    
    # Content strategy
    content_preferences = Column(JSON, default=lambda: {
        "platforms": ["instagram", "linkedin", "email"],
        "tone": "Professional",
        "post_frequency_per_week": 3,
        "content_types": ["image", "text", "video"],
        "best_posting_times": {},
        "hashtag_strategy": "moderate",
        "content_length_preference": "medium"
    })
    
    # Analytics & Performance
    total_campaigns = Column(Integer, default=0)
    total_content_pieces = Column(Integer, default=0)
    average_engagement_rate = Column(Float, default=0.0)
    total_followers_across_platforms = Column(Integer, default=0)
    
    # Settings
    auto_publish = Column(Boolean, default=False)
    ai_suggestions_enabled = Column(Boolean, default=True)
    analytics_tracking = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="businesses")
    campaigns = relationship("Campaign", back_populates="business", cascade="all, delete-orphan")
    contents = relationship("Content", back_populates="business", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_business_owner', owner_id),
        Index('idx_business_industry', industry),
        Index('idx_business_plan', plan),
    )

class Campaign(Base):
    """Comprehensive campaign model with advanced features"""
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    name = Column(String, nullable=False)
    objective = Column(String, nullable=False)
    description = Column(Text)
    target_platforms = Column(JSON, default=list)  # Store as JSON array
    
    # Campaign Status and Scheduling
    status = Column(String, default="draft")
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Budget and Performance
    budget_allocated = Column(Float, default=0.0)
    budget_spent = Column(Float, default=0.0)
    
    # Content Strategy
    content_strategy = Column(JSON, default=dict)
    target_audience_override = Column(JSON)  # Override business target audience
    
    # Performance Metrics
    total_content_pieces = Column(Integer, default=0)
    total_impressions = Column(Integer, default=0)
    total_engagements = Column(Integer, default=0)
    total_clicks = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    click_through_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    cost_per_click = Column(Float, default=0.0)
    cost_per_conversion = Column(Float, default=0.0)
    roi = Column(Float, default=0.0)
    
    # AI Generation Settings
    ai_generation_preferences = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="campaigns")
    contents = relationship("Content", back_populates="campaign", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_campaign_business', business_id),
        Index('idx_campaign_status', status),
        Index('idx_campaign_dates', start_date, end_date),
    )

class Content(Base):
    """Flexible content model for various platforms and formats"""
    __tablename__ = "contents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    title = Column(String, nullable=False)
    content_text = Column(Text)
    content_type = Column(String, nullable=False)  # 'post', 'story', 'reel', 'email', etc.
    platform = Column(String, nullable=False)
    
    # Content Structure and Media
    media_urls = Column(JSON, default=list)  # Store as JSON array
    hashtags = Column(JSON, default=list)
    mentions = Column(JSON, default=list)
    links = Column(JSON, default=list)
    
    # Publishing and Status
    status = Column(String, default="draft")
    scheduled_publish_time = Column(DateTime)
    published_at = Column(DateTime)
    is_published = Column(Boolean, default=False)
    
    # AI Generation Context
    ai_generated = Column(Boolean, default=False)
    ai_model_used = Column(String)
    ai_prompt_used = Column(Text)
    ai_generation_cost = Column(Float, default=0.0)
    ai_generation_tokens = Column(Integer, default=0)
    
    # Performance Analytics
    impressions = Column(Integer, default=0)
    engagements = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    
    # Content Metadata
    word_count = Column(Integer, default=0)
    character_count = Column(Integer, default=0)
    reading_time_minutes = Column(Float, default=0.0)
    sentiment_score = Column(Float)  # -1 to 1
    target_audience_tags = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="contents")
    campaign = relationship("Campaign", back_populates="contents")
    
    # Indexes
    __table_args__ = (
        Index('idx_content_business', business_id),
        Index('idx_content_campaign', campaign_id),
        Index('idx_content_platform_type', platform, content_type),
        Index('idx_content_status', status),
        Index('idx_content_published', published_at),
    )

class Analytics(Base):
    """Comprehensive analytics and reporting model"""
    __tablename__ = "analytics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    content_id = Column(String, ForeignKey("contents.id"))
    
    # Metrics Type and Platform
    metric_type = Column(String, nullable=False)  # 'daily', 'campaign', 'content', 'platform'
    platform = Column(String)
    date_recorded = Column(DateTime, default=datetime.utcnow)
    
    # Core Metrics
    impressions = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    engagements = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    
    # Advanced Metrics
    follower_count = Column(Integer, default=0)
    follower_growth = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    click_through_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    
    # Audience Demographics stored as JSON
    demographics = Column(JSON, default=dict)
    top_locations = Column(JSON, default=list)
    device_breakdown = Column(JSON, default=dict)
    traffic_sources = Column(JSON, default=dict)
    
    # Time-based Analytics
    best_posting_times = Column(JSON, default=dict)
    engagement_by_hour = Column(JSON, default=dict)
    performance_trends = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_analytics_business', business_id),
        Index('idx_analytics_campaign', campaign_id),
        Index('idx_analytics_content', content_id),
        Index('idx_analytics_date', date_recorded),
        Index('idx_analytics_platform', platform),
        Index('idx_analytics_type', metric_type),
    )

class Message(Base):
    """Message model for customer communications and support"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    platform = Column(String, nullable=False)
    
    # Customer Information
    customer_id = Column(String)
    customer_name = Column(String)
    customer_email = Column(String)
    customer_phone = Column(String)
    
    # Message Content
    subject = Column(String)
    content = Column(Text, nullable=False)
    media_urls = Column(JSON, default=list)
    
    # Message Metadata
    direction = Column(String, nullable=False)  # 'inbound', 'outbound'
    thread_id = Column(String)
    reply_to_message_id = Column(String)
    is_read = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    is_flagged = Column(Boolean, default=False)
    priority = Column(String, default="normal")  # 'low', 'normal', 'high', 'urgent'
    
    # AI Processing
    ai_generated = Column(Boolean, default=False)
    ai_suggested_reply = Column(Text)
    ai_sentiment = Column(String)  # 'positive', 'neutral', 'negative'
    ai_category = Column(String)
    ai_confidence_score = Column(Float, default=0.0)
    
    # Timestamps
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)
    replied_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_message_business', business_id),
        Index('idx_message_customer', customer_id),
        Index('idx_message_thread', thread_id),
        Index('idx_message_platform', platform),
        Index('idx_message_priority', priority),
        Index('idx_message_created', created_at),
    )

class AILog(Base):
    """AI service usage tracking and cost management"""
    __tablename__ = "ai_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("businesses.id"))
    user_id = Column(String, ForeignKey("users.id"))
    
    # Request Information
    service_type = Column(String, nullable=False)  # 'content', 'strategy', 'analytics', 'messaging'
    operation = Column(String, nullable=False)  # 'generate', 'analyze', 'optimize', 'respond'
    model_used = Column(String, nullable=False)
    model_version = Column(String)
    
    # Input/Output
    input_data = Column(JSON)  # Store request parameters
    output_data = Column(JSON)  # Store response data
    prompt_template = Column(Text)
    actual_prompt = Column(Text)
    
    # Usage Metrics
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    processing_time_seconds = Column(Float, default=0.0)
    
    # Cost Tracking
    estimated_cost = Column(Float, default=0.0)
    cost_per_token = Column(Float, default=0.0)
    
    # Quality Metrics
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    user_rating = Column(Integer)  # 1-5 scale
    used_in_production = Column(Boolean, default=False)
    
    # Context
    request_id = Column(String)
    session_id = Column(String)
    ip_address = Column(String)
    user_agent = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_ailog_business', business_id),
        Index('idx_ailog_user', user_id),
        Index('idx_ailog_service', service_type),
        Index('idx_ailog_model', model_used),
        Index('idx_ailog_created', created_at),
        Index('idx_ailog_cost', estimated_cost),
    )

# Repository Pattern Implementation
class BaseRepository:
    """Base repository class with common CRUD operations"""
    
    def __init__(self, session: Session, model_class):
        self.session = session
        self.model_class = model_class
    
    def create(self, entity_data: dict) -> Any:
        """Create a new entity"""
        try:
            if "id" not in entity_data:
                entity_data["id"] = str(uuid.uuid4())
            
            entity = self.model_class(**entity_data)
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            self.session.rollback()
            logger.error(f"Integrity error creating {self.model_class.__name__}: {e}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating {self.model_class.__name__}: {e}")
            raise
    
    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """Get entity by ID"""
        return self.session.query(self.model_class).filter(
            self.model_class.id == entity_id
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        """Get all entities with pagination"""
        return self.session.query(self.model_class).offset(skip).limit(limit).all()
    
    def update(self, entity_id: str, update_data: dict) -> Optional[Any]:
        """Update entity by ID"""
        try:
            entity = self.get_by_id(entity_id)
            if not entity:
                return None
            
            for field, value in update_data.items():
                if hasattr(entity, field):
                    setattr(entity, field, value)
            
            if hasattr(entity, 'updated_at'):
                entity.updated_at = datetime.utcnow()
            
            self.session.commit()
            self.session.refresh(entity)
            return entity
            
        except IntegrityError as e:
            self.session.rollback()
            logger.error(f"Integrity error updating {self.model_class.__name__}: {e}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating {self.model_class.__name__}: {e}")
            raise
    
    def delete(self, entity_id: str) -> bool:
        """Delete entity by ID"""
        try:
            entity = self.get_by_id(entity_id)
            if not entity:
                return False
                
            self.session.delete(entity)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting {self.model_class.__name__}: {e}")
            raise
    
    def count(self) -> int:
        """Count total entities"""
        return self.session.query(self.model_class).count()

class UserRepository(BaseRepository):
    """Repository for User operations"""
    
    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.session.query(User).filter(User.email == email.lower()).first()
    
    def get_by_provider(self, provider: str, provider_id: str) -> Optional[User]:
        """Get user by external provider"""
        return self.session.query(User).filter(
            User.provider == provider,
            User.provider_id == provider_id
        ).first()
    
    def update_login_stats(self, user_id: str):
        """Update user login statistics"""
        user = self.get_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            user.login_count += 1
            self.session.commit()

class BusinessRepository(BaseRepository):
    """Repository for Business operations"""
    
    def __init__(self, session: Session):
        super().__init__(session, Business)
    
    def get_by_owner(self, owner_id: str) -> List[Business]:
        """Get businesses by owner"""
        return self.session.query(Business).filter(Business.owner_id == owner_id).all()
    
    def get_by_industry(self, industry: str) -> List[Business]:
        """Get businesses by industry"""
        return self.session.query(Business).filter(Business.industry == industry).all()

class CampaignRepository(BaseRepository):
    """Repository for Campaign operations"""
    
    def __init__(self, session: Session):
        super().__init__(session, Campaign)
    
    def get_by_business(self, business_id: str) -> List[Campaign]:
        """Get campaigns by business"""
        return self.session.query(Campaign).filter(Campaign.business_id == business_id).all()
    
    def get_by_status(self, status: str) -> List[Campaign]:
        """Get campaigns by status"""
        return self.session.query(Campaign).filter(Campaign.status == status).all()

class ContentRepository(BaseRepository):
    """Repository for Content operations"""
    
    def __init__(self, session: Session):
        super().__init__(session, Content)
    
    def get_by_campaign(self, campaign_id: str) -> List[Content]:
        """Get content by campaign"""
        return self.session.query(Content).filter(Content.campaign_id == campaign_id).all()
    
    def get_by_business(self, business_id: str) -> List[Content]:
        """Get content by business"""
        return self.session.query(Content).filter(Content.business_id == business_id).all()
    
    def get_by_platform(self, platform: str) -> List[Content]:
        """Get content by platform"""
        return self.session.query(Content).filter(Content.platform == platform).all()

class AnalyticsRepository(BaseRepository):
    """Repository for Analytics operations"""
    
    def __init__(self, session: Session):
        super().__init__(session, Analytics)
    
    def get_by_business(self, business_id: str) -> List[Analytics]:
        """Get analytics by business"""
        return self.session.query(Analytics).filter(Analytics.business_id == business_id).all()
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Analytics]:
        """Get analytics by date range"""
        return self.session.query(Analytics).filter(
            Analytics.date_recorded >= start_date,
            Analytics.date_recorded <= end_date
        ).all()

class MessageRepository(BaseRepository):
    """Repository for Message operations"""
    
    def __init__(self, session: Session):
        super().__init__(session, Message)
    
    def get_by_business(self, business_id: str) -> List[Message]:
        """Get messages by business"""
        return self.session.query(Message).filter(Message.business_id == business_id).all()
    
    def get_unread(self, business_id: str) -> List[Message]:
        """Get unread messages"""
        return self.session.query(Message).filter(
            Message.business_id == business_id,
            Message.is_read == False
        ).all()

class AILogRepository(BaseRepository):
    """Repository for AILog operations"""
    
    def __init__(self, session: Session):
        super().__init__(session, AILog)
    
    def get_by_business(self, business_id: str) -> List[AILog]:
        """Get AI logs by business"""
        return self.session.query(AILog).filter(AILog.business_id == business_id).all()
    
    def get_cost_summary(self, business_id: str, start_date: datetime, end_date: datetime) -> float:
        """Get cost summary for a business in a date range"""
        return self.session.query(AILog).filter(
            AILog.business_id == business_id,
            AILog.created_at >= start_date,
            AILog.created_at <= end_date
        ).with_entities(func.sum(AILog.estimated_cost)).scalar() or 0.0

# Database Configuration and Utilities
def get_database_health() -> Dict[str, Any]:
    """Get database health status"""
    db_manager = DatabaseManager()
    try:
        db_manager.connect()
        with db_manager.get_session() as session:
            user_count = session.query(User).count()
            business_count = session.query(Business).count()
            campaign_count = session.query(Campaign).count()
            content_count = session.query(Content).count()
            
        return {
            "status": "healthy",
            "database_type": "SQLite",
            "connection": "active",
            "statistics": {
                "users": user_count,
                "businesses": business_count,
                "campaigns": campaign_count,
                "content_pieces": content_count
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        db_manager.disconnect()

# Export all models and classes
__all__ = [
    # Enums
    "UserRole", "BusinessPlan", "CampaignStatus", "ContentStatus", "Platform", "ContentType",
    # Models
    "User", "Business", "Campaign", "Content", "Analytics", "Message", "AILog",
    # Database Management  
    "DatabaseManager", "Base",
    # Repositories
    "BaseRepository", "UserRepository", "BusinessRepository", "CampaignRepository",
    "ContentRepository", "AnalyticsRepository", "MessageRepository", "AILogRepository",
    # Utilities
    "get_database_health"
]