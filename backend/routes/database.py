"""
Database Management API Routes
SQLite implementation with SQLAlchemy ORM
Comprehensive CRUD operations for all models
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import logging

# Import database models and repositories
from models.database import (
    DatabaseManager, User, Business, Campaign, Content, Analytics, Message, AILog,
    UserRepository, BusinessRepository, CampaignRepository, ContentRepository,
    AnalyticsRepository, MessageRepository, AILogRepository,
    get_database_health
)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/database", tags=["Database Management"])

# Database Manager Instance
db_manager = DatabaseManager()

def get_db_session():
    """Dependency to get database session"""
    db_manager.connect()
    with db_manager.get_session() as session:
        yield session

# Health and Status Endpoints
@router.get("/health")
def database_health():
    """Get database health and connection status"""
    return get_database_health()

@router.get("/stats")
def database_statistics(session=Depends(get_db_session)):
    """Get comprehensive database statistics"""
    try:
        user_repo = UserRepository(session)
        business_repo = BusinessRepository(session)
        campaign_repo = CampaignRepository(session)
        content_repo = ContentRepository(session)
        analytics_repo = AnalyticsRepository(session)
        message_repo = MessageRepository(session)
        ailog_repo = AILogRepository(session)
        
        return {
            "statistics": {
                "users": user_repo.count(),
                "businesses": business_repo.count(),
                "campaigns": campaign_repo.count(),
                "content_pieces": content_repo.count(),
                "analytics_records": analytics_repo.count(),
                "messages": message_repo.count(),
                "ai_logs": ailog_repo.count()
            },
            "database_type": "SQLite",
            "status": "connected"
        }
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# User Management Endpoints
@router.get("/users")
def get_users(skip: int = 0, limit: int = 100, session=Depends(get_db_session)):
    """Get all users with pagination"""
    try:
        user_repo = UserRepository(session)
        users = user_repo.get_all(skip=skip, limit=limit)
        return {"users": users, "count": len(users)}
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {e}")

@router.get("/users/{user_id}")
def get_user(user_id: str, session=Depends(get_db_session)):
    """Get user by ID"""
    try:
        user_repo = UserRepository(session)
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {e}")

@router.post("/users")
def create_user(user_data: dict, session=Depends(get_db_session)):
    """Create a new user"""
    try:
        user_repo = UserRepository(session)
        user = user_repo.create(user_data)
        return {"message": "User created successfully", "user": user}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")

@router.put("/users/{user_id}")
def update_user(user_id: str, update_data: dict, session=Depends(get_db_session)):
    """Update user by ID"""
    try:
        user_repo = UserRepository(session)
        user = user_repo.update(user_id, update_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User updated successfully", "user": user}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(status_code=400, detail=f"Error updating user: {e}")

@router.delete("/users/{user_id}")
def delete_user(user_id: str, session=Depends(get_db_session)):
    """Delete user by ID"""
    try:
        user_repo = UserRepository(session)
        success = user_repo.delete(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(status_code=400, detail=f"Error deleting user: {e}")

# Business Management Endpoints
@router.get("/businesses")
def get_businesses(skip: int = 0, limit: int = 100, session=Depends(get_db_session)):
    """Get all businesses with pagination"""
    try:
        business_repo = BusinessRepository(session)
        businesses = business_repo.get_all(skip=skip, limit=limit)
        return {"businesses": businesses, "count": len(businesses)}
    except Exception as e:
        logger.error(f"Error getting businesses: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving businesses: {e}")

@router.get("/businesses/{business_id}")
def get_business(business_id: str, session=Depends(get_db_session)):
    """Get business by ID"""
    try:
        business_repo = BusinessRepository(session)
        business = business_repo.get_by_id(business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        return business
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting business {business_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving business: {e}")

@router.post("/businesses")
def create_business(business_data: dict, session=Depends(get_db_session)):
    """Create a new business"""
    try:
        business_repo = BusinessRepository(session)
        business = business_repo.create(business_data)
        return {"message": "Business created successfully", "business": business}
    except Exception as e:
        logger.error(f"Error creating business: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating business: {e}")

@router.put("/businesses/{business_id}")
def update_business(business_id: str, update_data: dict, session=Depends(get_db_session)):
    """Update business by ID"""
    try:
        business_repo = BusinessRepository(session)
        business = business_repo.update(business_id, update_data)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        return {"message": "Business updated successfully", "business": business}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating business {business_id}: {e}")
        raise HTTPException(status_code=400, detail=f"Error updating business: {e}")

@router.delete("/businesses/{business_id}")
def delete_business(business_id: str, session=Depends(get_db_session)):
    """Delete business by ID"""
    try:
        business_repo = BusinessRepository(session)
        success = business_repo.delete(business_id)
        if not success:
            raise HTTPException(status_code=404, detail="Business not found")
        return {"message": "Business deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting business {business_id}: {e}")
        raise HTTPException(status_code=400, detail=f"Error deleting business: {e}")

# Campaign Management Endpoints
@router.get("/campaigns")
def get_campaigns(skip: int = 0, limit: int = 100, session=Depends(get_db_session)):
    """Get all campaigns with pagination"""
    try:
        campaign_repo = CampaignRepository(session)
        campaigns = campaign_repo.get_all(skip=skip, limit=limit)
        return {"campaigns": campaigns, "count": len(campaigns)}
    except Exception as e:
        logger.error(f"Error getting campaigns: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving campaigns: {e}")

@router.get("/campaigns/{campaign_id}")
def get_campaign(campaign_id: str, session=Depends(get_db_session)):
    """Get campaign by ID"""
    try:
        campaign_repo = CampaignRepository(session)
        campaign = campaign_repo.get_by_id(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving campaign: {e}")

@router.post("/campaigns")
def create_campaign(campaign_data: dict, session=Depends(get_db_session)):
    """Create a new campaign"""
    try:
        campaign_repo = CampaignRepository(session)
        campaign = campaign_repo.create(campaign_data)
        return {"message": "Campaign created successfully", "campaign": campaign}
    except Exception as e:
        logger.error(f"Error creating campaign: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating campaign: {e}")

@router.put("/campaigns/{campaign_id}")
def update_campaign(campaign_id: str, update_data: dict, session=Depends(get_db_session)):
    """Update campaign by ID"""
    try:
        campaign_repo = CampaignRepository(session)
        campaign = campaign_repo.update(campaign_id, update_data)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return {"message": "Campaign updated successfully", "campaign": campaign}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating campaign {campaign_id}: {e}")
        raise HTTPException(status_code=400, detail=f"Error updating campaign: {e}")

@router.delete("/campaigns/{campaign_id}")
def delete_campaign(campaign_id: str, session=Depends(get_db_session)):
    """Delete campaign by ID"""
    try:
        campaign_repo = CampaignRepository(session)
        success = campaign_repo.delete(campaign_id)
        if not success:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return {"message": "Campaign deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting campaign {campaign_id}: {e}")
        raise HTTPException(status_code=400, detail=f"Error deleting campaign: {e}")

# Content Management Endpoints
@router.get("/content")
def get_content(skip: int = 0, limit: int = 100, session=Depends(get_db_session)):
    """Get all content with pagination"""
    try:
        content_repo = ContentRepository(session)
        content = content_repo.get_all(skip=skip, limit=limit)
        return {"content": content, "count": len(content)}
    except Exception as e:
        logger.error(f"Error getting content: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving content: {e}")

@router.get("/content/{content_id}")
def get_content_item(content_id: str, session=Depends(get_db_session)):
    """Get content by ID"""
    try:
        content_repo = ContentRepository(session)
        content = content_repo.get_by_id(content_id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return content
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting content {content_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving content: {e}")

@router.post("/content")
def create_content(content_data: dict, session=Depends(get_db_session)):
    """Create new content"""
    try:
        content_repo = ContentRepository(session)
        content = content_repo.create(content_data)
        return {"message": "Content created successfully", "content": content}
    except Exception as e:
        logger.error(f"Error creating content: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating content: {e}")

# Analytics Endpoints
@router.get("/analytics")
def get_analytics(skip: int = 0, limit: int = 100, session=Depends(get_db_session)):
    """Get all analytics with pagination"""
    try:
        analytics_repo = AnalyticsRepository(session)
        analytics = analytics_repo.get_all(skip=skip, limit=limit)
        return {"analytics": analytics, "count": len(analytics)}
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving analytics: {e}")

@router.get("/analytics/{business_id}/summary")
def get_business_analytics_summary(business_id: str, session=Depends(get_db_session)):
    """Get analytics summary for a business"""
    try:
        analytics_repo = AnalyticsRepository(session)
        analytics = analytics_repo.get_by_business(business_id)
        return {"business_id": business_id, "analytics": analytics, "count": len(analytics)}
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving analytics: {e}")

# Message Management Endpoints
@router.get("/messages")
def get_messages(skip: int = 0, limit: int = 100, session=Depends(get_db_session)):
    """Get all messages with pagination"""
    try:
        message_repo = MessageRepository(session)
        messages = message_repo.get_all(skip=skip, limit=limit)
        return {"messages": messages, "count": len(messages)}
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {e}")

@router.get("/messages/{business_id}/unread")
def get_unread_messages(business_id: str, session=Depends(get_db_session)):
    """Get unread messages for a business"""
    try:
        message_repo = MessageRepository(session)
        messages = message_repo.get_unread(business_id)
        return {"business_id": business_id, "unread_messages": messages, "count": len(messages)}
    except Exception as e:
        logger.error(f"Error getting unread messages: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {e}")

# AI Log Endpoints
@router.get("/ai-logs")
def get_ai_logs(skip: int = 0, limit: int = 100, session=Depends(get_db_session)):
    """Get all AI logs with pagination"""
    try:
        ailog_repo = AILogRepository(session)
        logs = ailog_repo.get_all(skip=skip, limit=limit)
        return {"ai_logs": logs, "count": len(logs)}
    except Exception as e:
        logger.error(f"Error getting AI logs: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving AI logs: {e}")

@router.post("/ai-logs")
def create_ai_log(log_data: dict, session=Depends(get_db_session)):
    """Create new AI log entry"""
    try:
        ailog_repo = AILogRepository(session)
        log = ailog_repo.create(log_data)
        return {"message": "AI log created successfully", "log": log}
    except Exception as e:
        logger.error(f"Error creating AI log: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating AI log: {e}")

# Utility Endpoints
@router.post("/init")
def initialize_database(session=Depends(get_db_session)):
    """Initialize database with sample data"""
    try:
        # Create sample user
        user_repo = UserRepository(session)
        sample_user = {
            "email": "test@example.com",
            "full_name": "Test User",
            "first_name": "Test",
            "last_name": "User",
            "role": "owner",
            "is_active": True
        }
        user = user_repo.create(sample_user)
        
        # Create sample business
        business_repo = BusinessRepository(session)
        sample_business = {
            "owner_id": user.id,
            "name": "Sample Business",
            "industry": "Technology",
            "description": "A sample business for testing"
        }
        business = business_repo.create(sample_business)
        
        return {
            "message": "Database initialized successfully",
            "sample_data": {
                "user": user.email,
                "business": business.name
            }
        }
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise HTTPException(status_code=500, detail=f"Error initializing database: {e}")

@router.delete("/reset")
def reset_database():
    """Reset database (delete all data)"""
    try:
        db_manager.connect()
        # Drop all tables and recreate them
        from models.database import Base
        Base.metadata.drop_all(bind=db_manager.engine)
        Base.metadata.create_all(bind=db_manager.engine)
        
        return {"message": "Database reset successfully"}
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise HTTPException(status_code=500, detail=f"Error resetting database: {e}")
    finally:
        db_manager.disconnect()