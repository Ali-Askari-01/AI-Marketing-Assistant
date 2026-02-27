"""
Enhanced AI Service Module - Comprehensive Implementation
Main interface for all AI operations with complete orchestration and management
Designed according to AI Service Layer Finalization and AI Prompt Architecture specifications
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import asyncio
import uuid
import logging

# Import all enhanced AI components
from ai.ai_client import AI, AIConfig, AIResponse
from ai.cost_tracker import EnhancedCostTracker, SubscriptionTier
from ai.schema_validator import SchemaValidator
from ai.ai_orchestration_service import (
    AIOrchestrationService, AITaskRequest, AITaskResult,
    AITaskType, AITaskPriority
)
from ai.prompt_builder_enhanced import prompt_builder, PromptBuilder
from models.mongodb_models import Business, Campaign, Content
from core.errors import AIServiceError, ValidationError, RateLimitError

logger = logging.getLogger(__name__)

class ComprehensiveAIService:
    """
    Complete AI Service with full orchestration capabilities
    Main interface for all AI operations in the marketing platform
    """
    
    def __init__(self):
        # Initialize core AI components
        self.ai_client = AI()
        self.cost_tracker = EnhancedCostTracker()
        self.schema_validator = SchemaValidator()
        self.prompt_builder = prompt_builder
        
        # Initialize orchestration service
        self.orchestration_service = AIOrchestrationService(
            ai_client=self.ai_client,
            cost_tracker=self.cost_tracker
        )
        
        # Service configuration
        self.service_config = {
            "max_concurrent_requests": 10,
            "default_timeout": 60,  # seconds
            "retry_attempts": 3,
            "enable_caching": True,
            "cache_ttl": 300  # 5 minutes
        }
        
        # Request cache for performance optimization
        self.response_cache: Dict[str, Dict] = {}
        self.active_requests: Dict[str, Dict] = {}
        
        logger.info("Comprehensive AI Service initialized with full orchestration capabilities")
    
    # === CAMPAIGN STRATEGY GENERATION ===
    
    async def generate_campaign_strategy(
        self, 
        business_id: str, 
        user_id: str,
        campaign_goal: str,
        duration_days: int = 30,
        platforms: List[str] = None,
        budget_target: Optional[float] = None,
        priority: AITaskPriority = AITaskPriority.NORMAL
    ) -> Dict[str, Any]:
        """
        Generate comprehensive campaign strategy with full context injection
        
        Returns detailed campaign calendar with weekly themes, daily content plan,
        KPI targets, and platform-specific recommendations
        """
        try:
            request_id = str(uuid.uuid4())
            logger.info(f"[{request_id}] Generating campaign strategy for business {business_id}")
            
            # Check budget availability
            budget_check = await self.cost_tracker.check_budget_before_request(
                business_id=business_id,
                estimated_tokens=1500
            )
            
            if not budget_check.get("can_proceed", False):
                raise RateLimitError("Budget limits exceeded for campaign strategy generation")
            
            # Create structured task request
            task_request = AITaskRequest(
                task_type=AITaskType.STRATEGY_GENERATION,
                business_id=business_id,
                user_id=user_id,
                priority=priority,
                parameters={
                    "campaign_goal": campaign_goal,
                    "duration_days": duration_days,
                    "platforms": platforms or ["instagram", "linkedin"],
                    "budget_target": budget_target,
                    "request_id": request_id
                }
            )
            
            self.active_requests[request_id] = {
                "type": "campaign_strategy",
                "started_at": datetime.now(),
                "business_id": business_id
            }
            
            # Process through enhanced orchestration
            result = await self.orchestration_service.process_strategy_generation(task_request)
            
            # Clean up active request tracking
            self.active_requests.pop(request_id, None)
            
            # Format comprehensive response
            if result.success:
                response_data = {
                    "success": True,
                    "request_id": request_id,
                    "strategy": result.result_data,
                    "metadata": {
                        "cost": result.cost,
                        "tokens_used": result.tokens_used,
                        "processing_time": result.processing_time,
                        "model_used": result.model_used,
                        "task_id": result.task_id,
                        "generated_at": datetime.now().isoformat(),
                        "validation_passed": True
                    },
                    "context": {
                        "campaign_goal": campaign_goal,
                        "duration_days": duration_days,
                        "target_platforms": platforms or ["instagram", "linkedin"],
                        "budget_target": budget_target
                    }
                }
                
                # Cache successful response
                if self.service_config["enable_caching"]:
                    cache_key = f"strategy_{business_id}_{hash(str(task_request.parameters))}"
                    self.response_cache[cache_key] = {
                        "data": response_data,
                        "cached_at": datetime.now(),
                        "ttl": self.service_config["cache_ttl"]
                    }
                
                logger.info(f"[{request_id}] Campaign strategy generated successfully")
                return response_data
            else:
                logger.error(f"[{request_id}] Campaign strategy generation failed: {result.error}")
                return {
                    "success": False,
                    "request_id": request_id,
                    "error": result.error,
                    "error_type": "generation_failed",
                    "task_id": result.task_id
                }
                
        except Exception as e:
            logger.error(f"Campaign strategy generation failed: {str(e)}")
            self.active_requests.pop(request_id, None)
            return {
                "success": False,
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    # === CONTENT GENERATION ===
    
    async def generate_content(
        self,
        business_id: str,
        user_id: str,
        content_type: str,
        platform: str,
        campaign_id: Optional[str] = None,
        theme: Optional[str] = None,
        target_audience: Optional[str] = None,
        tone: Optional[str] = None,
        priority: AITaskPriority = AITaskPriority.NORMAL
    ) -> Dict[str, Any]:
        """
        Generate platform-optimized content with comprehensive context injection
        
        Returns detailed content with hashtags, CTAs, visual suggestions,
        engagement predictions, and optimization notes
        """
        try:
            request_id = str(uuid.uuid4())
            logger.info(f"[{request_id}] Generating {content_type} content for {platform}")
            
            # Budget validation
            budget_check = await self.cost_tracker.check_budget_before_request(
                business_id=business_id,
                estimated_tokens=1000
            )
            
            if not budget_check.get("can_proceed", False):
                raise RateLimitError("Budget limits exceeded for content generation")
            
            # Create enhanced task request
            task_request = AITaskRequest(
                task_type=AITaskType.CONTENT_CREATION,
                business_id=business_id,
                user_id=user_id,
                priority=priority,
                parameters={
                    "content_type": content_type,
                    "platform": platform,
                    "campaign_id": campaign_id,
                    "theme": theme,
                    "target_audience": target_audience,
                    "tone": tone,
                    "request_id": request_id
                }
            )
            
            self.active_requests[request_id] = {
                "type": "content_generation",
                "started_at": datetime.now(),
                "business_id": business_id
            }
            
            # Process through orchestration
            result = await self.orchestration_service.process_content_creation(task_request)
            
            self.active_requests.pop(request_id, None)
            
            # Format response with enhancement
            if result.success:
                response_data = {
                    "success": True,
                    "request_id": request_id,
                    "content": result.result_data,
                    "metadata": {
                        "cost": result.cost,
                        "tokens_used": result.tokens_used,
                        "processing_time": result.processing_time,
                        "model_used": result.model_used,
                        "task_id": result.task_id,
                        "generated_at": datetime.now().isoformat()
                    },
                    "context": {
                        "content_type": content_type,
                        "platform": platform,
                        "theme": theme,
                        "target_audience": target_audience,
                        "tone": tone
                    }
                }
                
                logger.info(f"[{request_id}] Content generated successfully")
                return response_data
            else:
                return {
                    "success": False,
                    "request_id": request_id,
                    "error": result.error,
                    "task_id": result.task_id
                }
                
        except Exception as e:
            logger.error(f"Content generation failed: {str(e)}")
            self.active_requests.pop(request_id, None)
            return {
                "success": False,
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    # === VIDEO SCRIPT GENERATION ===
    
    async def generate_video_script(
        self,
        business_id: str,
        user_id: str,
        video_type: str = "reel",
        duration: int = 30,
        campaign_id: Optional[str] = None,
        topic: Optional[str] = None,
        style: Optional[str] = None,
        priority: AITaskPriority = AITaskPriority.NORMAL
    ) -> Dict[str, Any]:
        """
        Generate comprehensive video scripts with scene-by-scene breakdown,
        production notes, and engagement optimization
        """
        try:
            request_id = str(uuid.uuid4())
            logger.info(f"[{request_id}] Generating {duration}s {video_type} script")
            
            # Budget check
            budget_check = await self.cost_tracker.check_budget_before_request(
                business_id=business_id,
                estimated_tokens=1200
            )
            
            if not budget_check.get("can_proceed", False):
                raise RateLimitError("Budget limits exceeded for video script generation")
            
            # Create task request
            task_request = AITaskRequest(
                task_type=AITaskType.VIDEO_SCRIPTING,
                business_id=business_id,
                user_id=user_id,
                priority=priority,
                parameters={
                    "video_type": video_type,
                    "duration": duration,
                    "campaign_id": campaign_id,
                    "topic": topic,
                    "style": style,
                    "request_id": request_id
                }
            )
            
            self.active_requests[request_id] = {
                "type": "video_script",
                "started_at": datetime.now(),
                "business_id": business_id
            }
            
            # Process through orchestration
            result = await self.orchestration_service.process_video_scripting(task_request)
            
            self.active_requests.pop(request_id, None)
            
            if result.success:
                return {
                    "success": True,
                    "request_id": request_id,
                    "script": result.result_data,
                    "metadata": {
                        "cost": result.cost,
                        "tokens_used": result.tokens_used,
                        "processing_time": result.processing_time,
                        "model_used": result.model_used,
                        "task_id": result.task_id,
                        "generated_at": datetime.now().isoformat()
                    },
                    "context": {
                        "video_type": video_type,
                        "duration": duration,
                        "topic": topic,
                        "style": style
                    }
                }
            else:
                return {
                    "success": False,
                    "request_id": request_id,
                    "error": result.error,
                    "task_id": result.task_id
                }
                
        except Exception as e:
            logger.error(f"Video script generation failed: {str(e)}")
            self.active_requests.pop(request_id, None)
            return {
                "success": False,
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    # === ANALYTICS INSIGHTS ===
    
    async def analyze_performance(
        self,
        business_id: str,
        user_id: str,
        campaign_id: Optional[str] = None,
        performance_data: Optional[Dict[str, Any]] = None,
        analysis_type: str = "comprehensive",
        priority: AITaskPriority = AITaskPriority.NORMAL
    ) -> Dict[str, Any]:
        """
        Generate comprehensive analytics insights with actionable recommendations,
        trend analysis, and performance forecasting
        """
        try:
            request_id = str(uuid.uuid4())
            logger.info(f"[{request_id}] Analyzing performance for business {business_id}")
            
            # Budget validation
            budget_check = await self.cost_tracker.check_budget_before_request(
                business_id=business_id,
                estimated_tokens=1300
            )
            
            if not budget_check.get("can_proceed", False):
                raise RateLimitError("Budget limits exceeded for analytics insights")
            
            # Create task request
            task_request = AITaskRequest(
                task_type=AITaskType.ANALYTICS_INSIGHTS,
                business_id=business_id,
                user_id=user_id,
                priority=priority,
                parameters={
                    "campaign_id": campaign_id,
                    "performance_data": performance_data or {},
                    "analysis_type": analysis_type,
                    "request_id": request_id
                }
            )
            
            self.active_requests[request_id] = {
                "type": "analytics_insights",
                "started_at": datetime.now(),
                "business_id": business_id
            }
            
            # Process through orchestration
            result = await self.orchestration_service.process_analytics_insights(task_request)
            
            self.active_requests.pop(request_id, None)
            
            if result.success:
                return {
                    "success": True,
                    "request_id": request_id,
                    "insights": result.result_data,
                    "metadata": {
                        "cost": result.cost,
                        "tokens_used": result.tokens_used,
                        "processing_time": result.processing_time,
                        "model_used": result.model_used,
                        "task_id": result.task_id,
                        "analyzed_at": datetime.now().isoformat()
                    },
                    "context": {
                        "campaign_id": campaign_id,
                        "analysis_type": analysis_type
                    }
                }
            else:
                return {
                    "success": False,
                    "request_id": request_id,
                    "error": result.error,
                    "task_id": result.task_id
                }
                
        except Exception as e:
            logger.error(f"Performance analysis failed: {str(e)}")
            self.active_requests.pop(request_id, None)
            return {
                "success": False,
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    # === CUSTOMER MESSAGING ===
    
    async def generate_customer_reply(
        self,
        business_id: str,
        user_id: str,
        customer_message: str,
        context_messages: List[Dict] = None,
        urgency: str = "normal",
        department: Optional[str] = None,
        priority: AITaskPriority = AITaskPriority.HIGH  # Customer service is high priority
    ) -> Dict[str, Any]:
        """
        Generate professional customer service replies with sentiment analysis,
        escalation recommendations, and response alternatives
        """
        try:
            request_id = str(uuid.uuid4())
            logger.info(f"[{request_id}] Generating customer reply for business {business_id}")
            
            # Budget check with priority for customer service
            budget_check = await self.cost_tracker.check_budget_before_request(
                business_id=business_id,
                estimated_tokens=800
            )
            
            if not budget_check.get("can_proceed", False):
                # For customer service, allow some overage
                logger.warning(f"Budget limits approached for customer messaging - proceeding due to priority")
            
            # Create task request
            task_request = AITaskRequest(
                task_type=AITaskType.CUSTOMER_MESSAGING,
                business_id=business_id,
                user_id=user_id,
                priority=priority,
                parameters={
                    "customer_message": customer_message,
                    "context_messages": context_messages or [],
                    "urgency": urgency,
                    "department": department,
                    "request_id": request_id
                }
            )
            
            self.active_requests[request_id] = {
                "type": "customer_messaging",
                "started_at": datetime.now(),
                "business_id": business_id
            }
            
            # Process through orchestration
            result = await self.orchestration_service.process_customer_messaging(task_request)
            
            self.active_requests.pop(request_id, None)
            
            if result.success:
                return {
                    "success": True,
                    "request_id": request_id,
                    "reply": result.result_data,
                    "metadata": {
                        "cost": result.cost,
                        "tokens_used": result.tokens_used,
                        "processing_time": result.processing_time,
                        "model_used": result.model_used,
                        "task_id": result.task_id,
                        "generated_at": datetime.now().isoformat()
                    },
                    "context": {
                        "urgency": urgency,
                        "department": department,
                        "message_length": len(customer_message)
                    }
                }
            else:
                return {
                    "success": False,
                    "request_id": request_id,
                    "error": result.error,
                    "task_id": result.task_id
                }
                
        except Exception as e:
            logger.error(f"Customer reply generation failed: {str(e)}")
            self.active_requests.pop(request_id, None)
            return {
                "success": False, 
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    # === USAGE ANALYTICS & MANAGEMENT ===
    
    async def get_usage_analytics(self, business_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive AI usage analytics"""
        try:
            return await self.cost_tracker.get_usage_analytics(business_id, days)
        except Exception as e:
            logger.error(f"Usage analytics failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def set_subscription_tier(self, business_id: str, subscription_tier: SubscriptionTier) -> Dict[str, Any]:
        """Set subscription tier and update budget limits"""
        try:
            if business_id not in self.cost_tracker.usage_cache:
                self.cost_tracker.usage_cache[business_id] = self.cost_tracker._initialize_business_usage()
            
            self.cost_tracker.usage_cache[business_id]["subscription_tier"] = subscription_tier
            
            return {
                "success": True,
                "business_id": business_id,
                "subscription_tier": subscription_tier,
                "daily_limits": self.cost_tracker.daily_limits[subscription_tier]
            }
            
        except Exception as e:
            logger.error(f"Subscription tier update failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def configure_budget_alerts(self, business_id: str, alert_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Configure budget alerts"""
        try:
            return await self.cost_tracker.set_budget_alerts(business_id, alert_configs)
        except Exception as e:
            logger.error(f"Budget alert configuration failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    # === SERVICE MONITORING ===
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get comprehensive service status and health metrics"""
        try:
            return {
                "status": "healthy",
                "service_info": {
                    "version": "2.0.0",
                    "features": [
                        "campaign_strategy_generation",
                        "content_creation",
                        "video_script_generation", 
                        "analytics_insights",
                        "customer_messaging",
                        "usage_analytics",
                        "budget_management"
                    ]
                },
                "active_requests": len(self.active_requests),
                "cache_size": len(self.response_cache),
                "cost_tracker": {
                    "tracked_businesses": len(self.cost_tracker.usage_cache),
                    "active_sessions": len(getattr(self.cost_tracker, 'active_sessions', {}))
                },
                "ai_client": await self.ai_client.health_check(),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Service status check failed: {str(e)}")
            return {
                "status": "degraded",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_active_requests(self) -> Dict[str, Any]:
        """Get information about currently active requests"""
        return {
            "active_count": len(self.active_requests),
            "requests": [
                {
                    "request_id": req_id,
                    "type": req_info["type"],
                    "business_id": req_info["business_id"],
                    "duration_seconds": (datetime.now() - req_info["started_at"]).total_seconds()
                }
                for req_id, req_info in self.active_requests.items()
            ]
        }

# Global service instance
ai_service = ComprehensiveAIService()

# Backward compatibility
AIService = ComprehensiveAIService

# Export main service instance
__all__ = ["ai_service", "AIService", "ComprehensiveAIService"]