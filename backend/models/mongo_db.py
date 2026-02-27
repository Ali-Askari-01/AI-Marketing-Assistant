"""
MongoDB Database Configuration and Connection Management
Production-ready MongoDB setup with Beanie ODM integration
"""

import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional, List
from contextlib import asynccontextmanager

from models.mongodb_models import document_models, User, Business, Campaign, Content, Message, Analytics, AILog
from core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class MongoDBManager:
    """MongoDB Connection and Management"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
        self._connected = False
        
    async def connect(self, database_url: str = None, database_name: str = "aimarketing"):
        """Initialize MongoDB connection and Beanie ODM"""
        try:
            # Use provided URL or default from settings
            db_url = database_url or getattr(settings, 'MONGODB_URL', 'mongodb://localhost:27017')
            
            # Create motor client
            self.client = AsyncIOMotorClient(db_url, serverSelectionTimeoutMS=5000)
            self.database = self.client[database_name]
            
            # Test connection with timeout
            await self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB at {db_url}")
            
            # Initialize Beanie with our document models
            await init_beanie(
                database=self.database,
                document_models=document_models
            )
            
            self._connected = True
            logger.info("Beanie ODM initialized successfully")
            
            # Create indexes
            await self._ensure_indexes()
            
            return True
            
        except Exception as e:
            logger.warning(f"Failed to connect to MongoDB: {e}")
            logger.info("Will run in demo mode without database persistence")
            self._connected = False
            return False
            
    async def _ensure_indexes(self):
        """Ensure all required indexes are created"""
        try:
            # Users indexes
            await User.create_index([("email", 1)], unique=True)
            await User.create_index([("created_at", -1)])
            
            # Business indexes  
            await Business.create_index([("owner", 1)])
            await Business.create_index([("profile.name", "text")])
            await Business.create_index([("created_at", -1)])
            
            # Campaign indexes
            await Campaign.create_index([("business", 1)])
            await Campaign.create_index([("status", 1)])
            await Campaign.create_index([("start_date", -1)])
            await Campaign.create_index([("created_at", -1)])
            
            # Content indexes
            await Content.create_index([("campaign", 1)])
            await Content.create_index([("business", 1)])
            await Content.create_index([("status", 1)])
            await Content.create_index([("platform", 1)]) 
            await Content.create_index([("scheduled_time", 1)])
            await Content.create_index([("created_at", -1)])
            
            # Message indexes
            await Message.create_index([("business", 1)])
            await Message.create_index([("is_read", 1)])
            await Message.create_index([("priority", 1)])
            await Message.create_index([("received_at", -1)])
            
            # Analytics indexes
            await Analytics.create_index([("business", 1)])
            await Analytics.create_index([("date", -1)])
            await Analytics.create_index([("period_type", 1)])
            
            # AI Logs indexes
            await AILog.create_index([("business", 1)])
            await AILog.create_index([("timestamp", -1)])
            await AILog.create_index([("service_type", 1)])
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Error creating indexes: {e}")
            
    async def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self._connected = False
            logger.info("Disconnected from MongoDB")
            
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self._connected
        
    async def health_check(self) -> dict:
        """Perform database health check"""
        try:
            if not self._connected:
                return {"status": "disconnected", "details": "Not connected to database"}
                
            # Ping database
            await self.client.admin.command('ping')
            
            # Check collections
            collections = await self.database.list_collection_names()
            
            # Get basic stats
            stats = {}
            for doc_model in document_models:
                try:
                    count = await doc_model.count()
                    stats[doc_model.Settings.name] = count
                except Exception as e:
                    stats[doc_model.Settings.name] = f"Error: {e}"
                    
            return {
                "status": "healthy",
                "collections": collections,
                "document_counts": stats,
                "database_name": self.database.name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "details": str(e)
            }

# Global database manager instance
db_manager = MongoDBManager()

# Repository classes for data access patterns
class UserRepository:
    """User data access layer"""
    
    @staticmethod
    async def create_user(user_data: dict) -> User:
        """Create a new user"""
        user = User(**user_data)
        await user.insert()
        return user
        
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return await User.find_one(User.email == email)
        
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        from bson import ObjectId
        return await User.get(ObjectId(user_id))
        
    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> Optional[User]:
        """Update user data"""
        from bson import ObjectId
        user = await User.get(ObjectId(user_id))
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            await user.save()
        return user
        
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Delete a user"""
        from bson import ObjectId
        user = await User.get(ObjectId(user_id))
        if user:
            await user.delete()
            return True
        return False

class BusinessRepository:
    """Business data access layer"""
    
    @staticmethod
    async def create_business(business_data: dict, owner: User) -> Business:
        """Create a new business"""
        business = Business(**business_data, owner=owner)
        await business.insert()
        return business
        
    @staticmethod
    async def get_businesses_by_owner(owner: User) -> List[Business]:
        """Get all businesses owned by a user"""
        return await Business.find(Business.owner == owner).to_list()
        
    @staticmethod
    async def get_business_by_id(business_id: str) -> Optional[Business]:
        """Get business by ID"""
        from bson import ObjectId
        return await Business.get(ObjectId(business_id))
        
    @staticmethod
    async def update_business(business_id: str, update_data: dict) -> Optional[Business]:
        """Update business data"""
        from bson import ObjectId
        business = await Business.get(ObjectId(business_id))
        if business:
            for key, value in update_data.items():
                if hasattr(business, key):
                    setattr(business, key, value)
            await business.save()
        return business

class CampaignRepository:
    """Campaign data access layer"""
    
    @staticmethod 
    async def create_campaign(campaign_data: dict, business: Business) -> Campaign:
        """Create a new campaign"""
        campaign = Campaign(**campaign_data, business=business)
        await campaign.insert()
        return campaign
        
    @staticmethod
    async def get_campaigns_by_business(business: Business) -> List[Campaign]:
        """Get all campaigns for a business"""
        return await Campaign.find(Campaign.business == business).to_list()
        
    @staticmethod
    async def get_campaign_by_id(campaign_id: str) -> Optional[Campaign]:
        """Get campaign by ID"""
        from bson import ObjectId
        return await Campaign.get(ObjectId(campaign_id))

class ContentRepository:
    """Content data access layer"""
    
    @staticmethod
    async def create_content(content_data: dict, campaign: Campaign, business: Business) -> Content:
        """Create new content"""
        content = Content(**content_data, campaign=campaign, business=business)
        await content.insert()
        return content
        
    @staticmethod
    async def get_content_by_campaign(campaign: Campaign) -> List[Content]:
        """Get all content for a campaign"""
        return await Content.find(Content.campaign == campaign).to_list()
        
    @staticmethod
    async def get_content_by_campaign_business(business: Business) -> List[Content]:
        """Get all content for a business"""
        return await Content.find(Content.business == business).to_list()
        
    @staticmethod
    async def get_scheduled_content(limit: int = 100) -> List[Content]:
        """Get content scheduled for publishing"""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        return await Content.find(
            Content.scheduled_time <= now,
            Content.status == "scheduled"
        ).limit(limit).to_list()

# Export repositories
user_repo = UserRepository()
business_repo = BusinessRepository()
campaign_repo = CampaignRepository() 
content_repo = ContentRepository()

# Database connection context manager
@asynccontextmanager
async def get_database():
    """Context manager for database operations"""
    if not db_manager.is_connected():
        await db_manager.connect()
    
    try:
        yield db_manager
    finally:
        # Connection stays open for the application lifecycle
        pass

# Helper function for startup
async def initialize_database():
    """Initialize database connection for application startup"""
    await db_manager.connect()
    logger.info("Database initialization complete")
    return db_manager