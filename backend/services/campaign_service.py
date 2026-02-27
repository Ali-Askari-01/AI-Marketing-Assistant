"""
Campaign Service Layer
Handles all campaign-related business logic and operations
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from models.mongo_db import campaign_repo, business_repo
from core.errors import ValidationError, NotFoundError, AuthorizationError, DatabaseError
from core.security import security_manager
from schemas.requests import CampaignCreateRequest, CampaignUpdateRequest
from ai.ai_service import ai_service
import uuid

class CampaignService:
    """Campaign service for handling campaign operations"""
    
    def __init__(self):
        self.campaign_repo = campaign_repo
        self.business_repo = business_repo
    
    async def create_campaign(self, campaign_data: CampaignCreateRequest, user_id: str) -> Dict[str, Any]:
        """Create a new campaign"""
        try:
            # Validate business ownership
            business = await self._validate_business_ownership(campaign_data.business_id, user_id)
            
            # Validate campaign dates
            if campaign_data.start_date < datetime.utcnow():
                raise ValidationError("Start date cannot be in the past")
            
            # Calculate end date
            end_date = campaign_data.start_date + timedelta(days=campaign_data.duration_days)
            
            # Prepare campaign data
            campaign_dict = campaign_data.dict()
            campaign_dict.update({
                "id": str(uuid.uuid4()),
                "end_date": end_date,
                "status": "draft",
                "total_engagement": 0,
                "total_impressions": 0,
                "total_conversions": 0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            # Set default values if not provided
            if not campaign_dict.get("target_audience"):
                campaign_dict["target_audience"] = business.get("target_audience", {})
            
            if not campaign_dict.get("secondary_goals"):
                campaign_dict["secondary_goals"] = []
            
            if not campaign_dict.get("content_types"):
                campaign_dict["content_types"] = business.get("content_preferences", {}).get("content_types", ["image", "text"])
            
            if not campaign_dict.get("platforms"):
                campaign_dict["platforms"] = business.get("content_preferences", {}).get("platforms", ["instagram", "linkedin"])
            
            # Create campaign
            campaign_id = await self.campaign_repo.create(campaign_dict)
            
            # Generate AI strategy if requested
            if campaign_dict.get("ai_generate_strategy", False):
                await self._generate_ai_strategy(campaign_id, business)
            
            # Return created campaign
            created_campaign = await self.campaign_repo.get_by_id(campaign_id)
            return self._format_campaign_response(created_campaign)
            
        except ValidationError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to create campaign: {str(e)}")
    
    async def get_campaign(self, campaign_id: str, user_id: str) -> Dict[str, Any]:
        """Get campaign by ID with ownership validation"""
        try:
            # Get campaign
            campaign = await self.campaign_repo.get_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            # Validate ownership
            await self._validate_business_ownership(campaign["business_id"], user_id)
            
            return self._format_campaign_response(campaign)
            
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get campaign: {str(e)}")
    
    async def update_campaign(self, campaign_id: str, update_data: CampaignUpdateRequest, user_id: str) -> Dict[str, Any]:
        """Update campaign with ownership validation"""
        try:
            # Get existing campaign
            existing_campaign = await self.campaign_repo.get_by_id(campaign_id)
            if not existing_campaign:
                raise NotFoundError("Campaign not found")
            
            # Validate ownership
            await self._validate_business_ownership(existing_campaign["business_id"], user_id)
            
            # Prepare update data
            update_dict = update_data.dict(exclude_unset=True)
            update_dict["updated_at"] = datetime.utcnow()
            
            # Validate status change
            if "status" in update_dict:
                valid_statuses = ["draft", "active", "paused", "completed"]
                if update_dict["status"] not in valid_statuses:
                    raise ValidationError(f"Invalid status. Must be one of: {valid_statuses}")
            
            # Update campaign
            success = await self.campaign_repo.update(campaign_id, update_dict)
            if not success:
                raise DatabaseError("Failed to update campaign")
            
            # Return updated campaign
            updated_campaign = await self.campaign_repo.get_by_id(campaign_id)
            return self._format_campaign_response(updated_campaign)
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to update campaign: {str(e)}")
    
    async def delete_campaign(self, campaign_id: str, user_id: str) -> bool:
        """Delete campaign with ownership validation"""
        try:
            # Get existing campaign
            existing_campaign = await self.campaign_repo.get_by_id(campaign_id)
            if not existing_campaign:
                raise NotFoundError("Campaign not found")
            
            # Validate ownership
            await self._validate_business_ownership(existing_campaign["business_id"], user_id)
            
            # Check if campaign has published content
            # In production, you might want to prevent deletion if there are published contents
            
            # Delete campaign
            success = await self.campaign_repo.delete(campaign_id)
            if not success:
                raise DatabaseError("Failed to delete campaign")
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to delete campaign: {str(e)}")
    
    async def get_business_campaigns(self, business_id: str, user_id: str) -> List[Dict[str, Any]]:
        """Get all campaigns for a business"""
        try:
            # Validate ownership
            await self._validate_business_ownership(business_id, user_id)
            
            # Get campaigns
            campaigns = await self.campaign_repo.get_by_business_id(business_id)
            return [self._format_campaign_response(campaign) for campaign in campaigns]
            
        except AuthorizationError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get business campaigns: {str(e)}")
    
    async def activate_campaign(self, campaign_id: str, user_id: str) -> Dict[str, Any]:
        """Activate a campaign"""
        try:
            # Get existing campaign
            existing_campaign = await self.campaign_repo.get_by_id(campaign_id)
            if not existing_campaign:
                raise NotFoundError("Campaign not found")
            
            # Validate ownership
            await self._validate_business_ownership(existing_campaign["business_id"], user_id)
            
            # Validate campaign can be activated
            if existing_campaign["status"] == "active":
                raise ValidationError("Campaign is already active")
            
            if existing_campaign["status"] == "completed":
                raise ValidationError("Cannot activate a completed campaign")
            
            # Check if campaign has required data
            if not existing_campaign.get("ai_strategy"):
                raise ValidationError("Campaign must have AI strategy before activation")
            
            # Activate campaign
            success = await self.campaign_repo.update(campaign_id, {
                "status": "active",
                "updated_at": datetime.utcnow()
            })
            
            if not success:
                raise DatabaseError("Failed to activate campaign")
            
            # Return updated campaign
            updated_campaign = await self.campaign_repo.get_by_id(campaign_id)
            return self._format_campaign_response(updated_campaign)
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to activate campaign: {str(e)}")
    
    async def pause_campaign(self, campaign_id: str, user_id: str) -> Dict[str, Any]:
        """Pause a campaign"""
        try:
            # Get existing campaign
            existing_campaign = await self.campaign_repo.get_by_id(campaign_id)
            if not existing_campaign:
                raise NotFoundError("Campaign not found")
            
            # Validate ownership
            await self._validate_business_ownership(existing_campaign["business_id"], user_id)
            
            # Validate campaign can be paused
            if existing_campaign["status"] != "active":
                raise ValidationError("Only active campaigns can be paused")
            
            # Pause campaign
            success = await self.campaign_repo.update(campaign_id, {
                "status": "paused",
                "updated_at": datetime.utcnow()
            })
            
            if not success:
                raise DatabaseError("Failed to pause campaign")
            
            # Return updated campaign
            updated_campaign = await self.campaign_repo.get_by_id(campaign_id)
            return self._format_campaign_response(updated_campaign)
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to pause campaign: {str(e)}")
    
    async def complete_campaign(self, campaign_id: str, user_id: str) -> Dict[str, Any]:
        """Complete a campaign"""
        try:
            # Get existing campaign
            existing_campaign = await self.campaign_repo.get_by_id(campaign_id)
            if not existing_campaign:
                raise NotFoundError("Campaign not found")
            
            # Validate ownership
            await self._validate_business_ownership(existing_campaign["business_id"], user_id)
            
            # Validate campaign can be completed
            if existing_campaign["status"] == "completed":
                raise ValidationError("Campaign is already completed")
            
            # Complete campaign
            success = await self.campaign_repo.update(campaign_id, {
                "status": "completed",
                "end_date": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            if not success:
                raise DatabaseError("Failed to complete campaign")
            
            # Return updated campaign
            updated_campaign = await self.campaign_repo.get_by_id(campaign_id)
            return self._format_campaign_response(updated_campaign)
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to complete campaign: {str(e)}")
    
    async def generate_ai_strategy(self, campaign_id: str, user_id: str) -> Dict[str, Any]:
        """Generate AI strategy for campaign"""
        try:
            # Get campaign
            campaign = await self.campaign_repo.get_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            # Validate ownership
            await self._validate_business_ownership(campaign["business_id"], user_id)
            
            # Get business data
            business = await self.business_repo.get_by_id(campaign["business_id"])
            if not business:
                raise NotFoundError("Business not found")
            
            # Generate AI strategy
            ai_strategy = await ai_service.generate_strategy({
                "campaign_goal": campaign.get("primary_goal", ""),
                "duration_days": campaign.get("duration_days", 30),
                "industry": business.get("industry", ""),
                "target_audience": business.get("target_audience", {}),
                "brand_voice": business.get("brand_voice", "Professional"),
                "platforms": campaign.get("platforms", []),
                "content_types": campaign.get("content_types", [])
            })
            
            # Update campaign with AI strategy
            success = await self.campaign_repo.update(campaign_id, {
                "ai_strategy": ai_strategy,
                "updated_at": datetime.utcnow()
            })
            
            if not success:
                raise DatabaseError("Failed to update campaign with AI strategy")
            
            # Return updated campaign
            updated_campaign = await self.campaign_repo.get_by_id(campaign_id)
            return self._format_campaign_response(updated_campaign)
            
        except (NotFoundError, AuthorizationError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to generate AI strategy: {str(e)}")
    
    async def get_campaign_analytics(self, campaign_id: str, user_id: str) -> Dict[str, Any]:
        """Get campaign analytics"""
        try:
            # Get campaign
            campaign = await self.campaign_repo.get_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            # Validate ownership
            await self._validate_business_ownership(campaign["business_id"], user_id)
            
            # Get campaign analytics (mock data for now)
            # In production, you would aggregate data from content and analytics
            analytics = {
                "campaign_id": campaign_id,
                "total_engagement": campaign.get("total_engagement", 0),
                "total_impressions": campaign.get("total_impressions", 0),
                "total_conversions": campaign.get("total_conversions", 0),
                "engagement_rate": 0.0,
                "conversion_rate": 0.0,
                "platform_performance": {
                    "instagram": {"engagement": 450, "impressions": 3000, "conversions": 20},
                    "linkedin": {"engagement": 320, "impressions": 2500, "conversions": 15},
                    "email": {"engagement": 180, "impressions": 1500, "conversions": 10}
                },
                "content_type_performance": {
                    "image": {"engagement": 350, "impressions": 2500, "conversions": 18},
                    "video": {"engagement": 420, "impressions": 2800, "conversions": 22},
                    "text": {"engagement": 180, "impressions": 1700, "conversions": 5}
                },
                "daily_performance": [],
                "top_performing_content": [],
                "recommendations": []
            }
            
            # Calculate rates
            if analytics["total_impressions"] > 0:
                analytics["engagement_rate"] = analytics["total_engagement"] / analytics["total_impressions"]
                analytics["conversion_rate"] = analytics["total_conversions"] / analytics["total_impressions"]
            
            return analytics
            
        except (NotFoundError, AuthorizationError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get campaign analytics: {str(e)}")
    
    async def _validate_business_ownership(self, business_id: str, user_id: str) -> Dict[str, Any]:
        """Validate business ownership and return business data"""
        business = await self.business_repo.get_by_id(business_id)
        if not business:
            raise NotFoundError("Business not found")
        
        if not security_manager.validate_business_ownership(user_id, business_id, None):
            raise AuthorizationError("Access denied: You don't own this business")
        
        return business
    
    async def _generate_ai_strategy(self, campaign_id: str, business: Dict[str, Any]) -> None:
        """Generate AI strategy for campaign (internal method)"""
        try:
            ai_strategy = await ai_service.generate_strategy({
                "campaign_goal": "Increase brand awareness",
                "duration_days": 30,
                "industry": business.get("industry", ""),
                "target_audience": business.get("target_audience", {}),
                "brand_voice": business.get("brand_voice", "Professional"),
                "platforms": business.get("content_preferences", {}).get("platforms", []),
                "content_types": business.get("content_preferences", {}).get("content_types", [])
            })
            
            await self.campaign_repo.update(campaign_id, {
                "ai_strategy": ai_strategy,
                "updated_at": datetime.utcnow()
            })
        except Exception as e:
            # Log error but don't fail the operation
            print(f"Failed to generate AI strategy: {str(e)}")
    
    def _format_campaign_response(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Format campaign data for response"""
        return {
            "id": campaign.get("id"),
            "business_id": campaign.get("business_id"),
            "name": campaign.get("name"),
            "description": campaign.get("description"),
            "status": campaign.get("status"),
            "duration_days": campaign.get("duration_days"),
            "start_date": campaign.get("start_date"),
            "end_date": campaign.get("end_date"),
            "budget": campaign.get("budget"),
            "primary_goal": campaign.get("primary_goal"),
            "secondary_goals": campaign.get("secondary_goals", []),
            "target_audience": campaign.get("target_audience", {}),
            "ai_strategy": campaign.get("ai_strategy"),
            "weekly_themes": campaign.get("weekly_themes", []),
            "kpi_targets": campaign.get("kpi_targets", {}),
            "media_mix": campaign.get("media_mix", {}),
            "total_engagement": campaign.get("total_engagement", 0),
            "total_impressions": campaign.get("total_impressions", 0),
            "total_conversions": campaign.get("total_conversions", 0),
            "created_at": campaign.get("created_at"),
            "updated_at": campaign.get("updated_at")
        }

# Global campaign service instance
campaign_service = CampaignService()
