"""
Business Service Layer - Core Business Logic
Implements business rules, validation, and orchestrates between API and data layers
Updated for MongoDB with Beanie ODM
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from models.mongodb_models import (
    Business, User, Campaign, Content, BusinessProfile, SocialMediaAccounts,
    Platform, CampaignStatus, ContentStatus
)
from models.mongo_db import (
    db_manager, user_repo, business_repo, campaign_repo, content_repo
)
from core.errors import (
    BusinessNotFoundError, UserNotFoundError, BusinessOwnershipError,
    ValidationError, BusinessLogicError, raise_validation_error
)
from core.security import validate_business_ownership

logger = logging.getLogger(__name__)

class BusinessService:
    """Business Logic Service - Centralized business operations"""
    
    def __init__(self):
        pass
    
    async def create_business(self, user_id: str, business_data: Dict[str, Any]) -> Business:
        """Create a new business with validation and business rules"""
        
        try:
            # Validate user exists
            user = await user_repo.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)
            
            # Check business limits
            user_businesses = await business_repo.get_businesses_by_owner(user)
            
            # Business limit validation
            from core.config import settings
            if len(user_businesses) >= settings.MAX_BUSINESSES_PER_USER:
                raise BusinessLogicError(
                    f"Maximum number of businesses ({settings.MAX_BUSINESSES_PER_USER}) reached",
                    error_code="BUSINESS_LIMIT_EXCEEDED"
                )
            
            # Validate required fields
            required_fields = ['name', 'industry']
            for field in required_fields:
                if not business_data.get(field):
                    raise_validation_error(f"{field} is required", field=field)
            
            # Business name uniqueness check (per user)
            existing_business = next(
                (b for b in user_businesses if b.profile.name.lower() == business_data['name'].lower()),
                None
            )
            if existing_business:
                raise ValidationError(
                    "Business name already exists for this user",
                    field="name"
                )
            
            # Create business profile
            business_profile = BusinessProfile(
                name=business_data['name'],
                industry=business_data['industry'],
                description=business_data.get('description', ''),
                target_audience=business_data.get('target_audience', ''),
                brand_voice=business_data.get('brand_voice', 'Professional'),
                website=business_data.get('website'),
                logo_url=business_data.get('logo_url')
            )
            
            # Create social media accounts
            social_accounts = SocialMediaAccounts(
                instagram_handle=business_data.get('instagram_handle'),
                linkedin_page=business_data.get('linkedin_page'),
                twitter_handle=business_data.get('twitter_handle'),
                tiktok_handle=business_data.get('tiktok_handle'),
                youtube_channel=business_data.get('youtube_channel')
            )
            
            # Set default AI preferences
            ai_preferences = {
                "preferred_tone": business_data.get('brand_voice', 'Professional'),
                "content_frequency": business_data.get('content_frequency', 3),
                "platforms": business_data.get('platforms', ['instagram', 'linkedin']),
                "hashtag_strategy": business_data.get('hashtag_strategy', 'moderate'),
                "content_length": business_data.get('content_length', 'medium')
            }
            
            # Create business
            business = await business_repo.create_business(
                {
                    "profile": business_profile,
                    "social_accounts": social_accounts,
                    "ai_preferences": ai_preferences,
                    "approval_required": business_data.get('approval_required', False)
                },
                user
            )
            
            logger.info(f"Created business {business.id} for user {user_id}")
            return business
            
        except Exception as e:
            logger.error(f"Failed to create business: {e}")
            raise
    
    async def get_business(self, business_id: str, user_id: str) -> Business:
        """Get business with ownership validation"""
        
        try:
            business = await business_repo.get_business_by_id(business_id)
            
            if not business:
                raise BusinessNotFoundError(business_id)
            
            # Verify ownership
            if str(business.owner.id) != user_id:
                raise BusinessOwnershipError(business_id)
            
            return business
            
        except Exception as e:
            logger.error(f"Failed to get business {business_id}: {e}")
            raise
    
    async def update_business(self, business_id: str, user_id: str, update_data: Dict[str, Any]) -> Business:
        """Update business with validation"""
        
        try:
            business = await business_repo.get_business_by_id(business_id)
            
            if not business:
                raise BusinessNotFoundError(business_id)
            
            # Verify ownership
            if str(business.owner.id) != user_id:
                raise BusinessOwnershipError(business_id)
            
            # Validate business name uniqueness if changing name
            if 'name' in update_data and update_data['name'] != business.profile.name:
                user = await user_repo.get_user_by_id(user_id)
                user_businesses = await business_repo.get_businesses_by_owner(user)
                existing_business = next(
                    (b for b in user_businesses if b.profile.name.lower() == update_data['name'].lower()),
                    None
                )
                if existing_business:
                    raise ValidationError(
                        "Business name already exists for this user",
                        field="name"
                    )
            
            # Update business
            updated_business = await business_repo.update_business(business_id, update_data)
            
            logger.info(f"Updated business {business_id}")
            return updated_business
            
        except Exception as e:
            logger.error(f"Failed to update business {business_id}: {e}")
            raise
    
    def delete_business(self, business_id: str, user_id: str) -> bool:
        """Delete business with cascade cleanup"""
        
        with self.db_manager.get_session() as session:
            business_repo = BusinessRepository(session)
            business = business_repo.get_by_id(business_id)
            
            if not business:
                raise BusinessNotFoundError(business_id)
    
    async def delete_business(self, business_id: str, user_id: str) -> bool:
        """Delete business with ownership validation"""
        
        try:
            business = await business_repo.get_business_by_id(business_id)
            
            if not business:
                raise BusinessNotFoundError(business_id)
            
            # Verify ownership
            if str(business.owner.id) != user_id:
                raise BusinessOwnershipError(business_id)
            
            # Delete business (MongoDB will handle cascading through references)
            await business.delete()
            
            logger.info(f"Deleted business {business_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete business {business_id}: {e}")
            raise
    
    async def get_user_businesses(self, user_id: str) -> List[Business]:
        """Get all businesses for a user"""
        
        try:
            user = await user_repo.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)
            
            businesses = await business_repo.get_businesses_by_owner(user)
            return businesses
            
        except Exception as e:
            logger.error(f"Failed to get businesses for user {user_id}: {e}")
            raise
    
    async def get_business_analytics(self, business_id: str, user_id: str) -> Dict[str, Any]:
        """Get comprehensive business analytics"""
        
        business = await self.get_business(business_id, user_id)
        
        try:
            campaigns = await campaign_repo.get_campaigns_by_business(business)
            content = await content_repo.get_content_by_campaign_business(business)
            
            # Calculate analytics
            total_campaigns = len(campaigns)
            total_content = len(content)
            active_campaigns = len([c for c in campaigns if c.status == CampaignStatus.ACTIVE])
            
            # Content performance
            total_impressions = sum(c.performance.impressions if c.performance else 0 for c in content)
            total_engagements = sum(
                (c.performance.likes + c.performance.comments + c.performance.shares) 
                if c.performance else 0 for c in content
            )
            engagement_rate = (total_engagements / total_impressions * 100) if total_impressions > 0 else 0
            
            return {
                'business_id': str(business.id),
                'business_name': business.profile.name,
                'total_campaigns': total_campaigns,
                'active_campaigns': active_campaigns,
                'total_content_pieces': total_content,
                'total_impressions': total_impressions,
                'total_engagements': total_engagements,
                'engagement_rate': round(engagement_rate, 2),
                'created_at': business.created_at.isoformat(),
                'last_updated': business.updated_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get analytics for business {business_id}: {e}")
            raise
    
    async def validate_business_access(self, business_id: str, user_id: str) -> bool:
        """Validate user has access to business"""
        try:
            await self.get_business(business_id, user_id)
            return True
        except (BusinessNotFoundError, BusinessOwnershipError):
            return False
    
    async def update_business_statistics(self, business_id: str):
        """Update business statistics (called after major operations)"""
        
        try:
            business = await business_repo.get_business_by_id(business_id)
            if not business:
                return
                
            campaigns = await campaign_repo.get_campaigns_by_business(business)
            content = await content_repo.get_content_by_campaign_business(business)
            
            # Calculate statistics
            total_campaigns = len(campaigns)
            total_content = len(content)
            active_campaigns = len([c for c in campaigns if c.status == CampaignStatus.ACTIVE])
            
            total_engagements = sum(
                (c.performance.likes + c.performance.comments + c.performance.shares) 
                if c.performance else 0 for c in content
            )
            total_impressions = sum(c.performance.impressions if c.performance else 0 for c in content)
            avg_engagement_rate = (total_engagements / total_impressions * 100) if total_impressions > 0 else 0
            
            # Update business
            update_data = {
                'total_campaigns': total_campaigns,
                'total_content': total_content,
                'active_campaigns': active_campaigns,
                'health_score': min(100.0, avg_engagement_rate * 2)  # Simple health score calculation
            }
            
            await business_repo.update_business(business_id, update_data)
            
            logger.info(f"Updated statistics for business {business_id}")
            
        except Exception as e:
            logger.error(f"Failed to update statistics for business {business_id}: {e}")
    
    def check_business_limits(self, limit_type: str, current_count: int) -> bool:
        """Check if business has reached limits for campaigns or content"""
        
        from core.config import settings
        
        limits = {
            'campaigns': settings.MAX_CAMPAIGNS_PER_BUSINESS,
            'content': settings.MAX_CONTENT_PIECES_PER_CAMPAIGN
        }
        
        limit = limits.get(limit_type)
        if limit and current_count >= limit:
            return False
        
        return True


# Global business service instance
business_service = BusinessService()