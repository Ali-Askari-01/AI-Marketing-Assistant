"""
Advanced AI Orchestration Service
Implements comprehensive AI system with context injection, cost tracking, retry mechanisms, and safety guardrails
Designed according to AI Service Layer Finalization specifications
"""

from typing import Dict, Any, Optional, List, Union, Tuple
from datetime import datetime, timedelta
import json
import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum

from ai.ai_client import AI, AIConfig, AIResponse
from ai.cost_tracker import CostTracker, UsageTracker
from ai.schema_validator import SchemaValidator
from ai.prompt_builder_enhanced import prompt_builder, PromptBuilder
from models.mongodb_models import Business, Campaign, Content, AILog, Platform, ContentType
from core.errors import AIServiceError, ValidationError, RateLimitError

# Configure logging
logger = logging.getLogger(__name__)

class AITaskType(str, Enum):
    """Supported AI task types"""
    STRATEGY_GENERATION = "strategy_generation"
    CONTENT_CREATION = "content_creation" 
    VIDEO_SCRIPTING = "video_scripting"
    ANALYTICS_INSIGHTS = "analytics_insights"
    CUSTOMER_MESSAGING = "customer_messaging"

class AITaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AITaskRequest:
    """Structured AI task request"""
    task_type: AITaskType
    business_id: str
    user_id: str
    priority: AITaskPriority = AITaskPriority.NORMAL
    parameters: Dict[str, Any] = field(default_factory=dict)
    deadline: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class AITaskResult:
    """Structured AI task result"""
    task_id: str
    task_type: AITaskType
    success: bool
    result_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    cost: float = 0.0
    tokens_used: int = 0
    processing_time: float = 0.0
    model_used: str = ""
    completed_at: datetime = field(default_factory=datetime.now)

class AIOrchestrationService:
    """Advanced AI orchestration with context injection and safety mechanisms"""
    
    def __init__(self, ai_client: AI, cost_tracker: CostTracker):
        self.ai_client = ai_client
        self.cost_tracker = cost_tracker
        self.usage_tracker = UsageTracker()
        self.schema_validator = SchemaValidator()
        self.prompt_builder = prompt_builder
        
        # Rate limiting configuration
        self.rate_limits = {
            AITaskPriority.LOW: {"requests_per_minute": 10, "concurrent_tasks": 2},
            AITaskPriority.NORMAL: {"requests_per_minute": 20, "concurrent_tasks": 5}, 
            AITaskPriority.HIGH: {"requests_per_minute": 40, "concurrent_tasks": 8},
            AITaskPriority.CRITICAL: {"requests_per_minute": 60, "concurrent_tasks": 12}
        }
        
        # Task queues by priority
        self.task_queues = {priority: asyncio.Queue() for priority in AITaskPriority}
        
        # Active task tracking
        self.active_tasks: Dict[str, AITaskRequest] = {}
        
        # Safety and monitoring
        self.safety_monitor = SafetyMonitor()
        self.performance_monitor = PerformanceMonitor()
        
    async def process_strategy_generation(self, request: AITaskRequest) -> AITaskResult:
        """Process campaign strategy generation request"""
        start_time = datetime.now()
        
        try:
            # Get business context
            business = await self._get_business(request.business_id)
            if not business:
                raise AIServiceError(f"Business not found: {request.business_id}")
            
            # Extract parameters
            campaign_goal = request.parameters.get("campaign_goal", "Increase brand awareness")
            duration_days = request.parameters.get("duration_days", 30)
            platforms = request.parameters.get("platforms", ["instagram", "linkedin"])
            
            # Build prompt with context injection
            prompt_config = self.prompt_builder.build_strategy_prompt(
                business=business,
                campaign_goal=campaign_goal,
                duration_days=duration_days,
                platforms=platforms
            )
            
            # Check safety constraints
            await self.safety_monitor.validate_request(request, prompt_config)
            
            # Execute AI request with retry logic
            ai_response = await self._execute_ai_request_with_retry(
                task_id=f"strategy_{request.business_id}_{int(start_time.timestamp())}",
                prompt_config=prompt_config,
                request=request
            )
            
            # Validate response schema
            validated_data = await self.schema_validator.validate_response(
                ai_response.content,
                prompt_config["schema_type"]
            )
            
            # Track costs and usage
            cost = await self.cost_tracker.calculate_cost(ai_response)
            await self.usage_tracker.track_usage(request.business_id, ai_response, cost)
            
            # Store AI interaction log
            await self._log_ai_interaction(
                business_id=request.business_id,
                user_id=request.user_id,
                task_type=request.task_type,
                prompt=prompt_config["user_prompt"],
                response=ai_response.content,
                cost=cost,
                success=True
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"strategy_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=True,
                result_data=validated_data,
                cost=cost,
                tokens_used=ai_response.tokens_used,
                processing_time=processing_time,
                model_used=ai_response.model
            )
            
        except Exception as e:
            logger.error(f"Strategy generation failed: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            await self._log_ai_interaction(
                business_id=request.business_id,
                user_id=request.user_id,
                task_type=request.task_type,
                prompt=prompt_config.get("user_prompt", "") if 'prompt_config' in locals() else "",
                response="",
                cost=0.0,
                success=False,
                error=str(e)
            )
            
            return AITaskResult(
                task_id=f"strategy_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    async def process_content_creation(self, request: AITaskRequest) -> AITaskResult:
        """Process content creation request"""
        start_time = datetime.now()
        
        try:
            # Get business and campaign context
            business = await self._get_business(request.business_id)
            campaign_id = request.parameters.get("campaign_id")
            campaign = await self._get_campaign(campaign_id) if campaign_id else None
            
            if not business:
                raise AIServiceError(f"Business not found: {request.business_id}")
            
            # Extract parameters
            content_type = request.parameters.get("content_type", "post")
            platform = request.parameters.get("platform", "instagram")
            theme = request.parameters.get("theme", "")
            
            # Build prompt with context injection
            prompt_config = self.prompt_builder.build_content_prompt(
                business=business,
                campaign=campaign,
                content_type=content_type,
                platform=platform,
                theme=theme
            )
            
            # Check safety constraints
            await self.safety_monitor.validate_request(request, prompt_config)
            
            # Execute AI request
            ai_response = await self._execute_ai_request_with_retry(
                task_id=f"content_{request.business_id}_{int(start_time.timestamp())}",
                prompt_config=prompt_config,
                request=request
            )
            
            # Validate response schema
            validated_data = await self.schema_validator.validate_response(
                ai_response.content,
                prompt_config["schema_type"]
            )
            
            # Track costs and usage
            cost = await self.cost_tracker.calculate_cost(ai_response)
            await self.usage_tracker.track_usage(request.business_id, ai_response, cost)
            
            # Store AI interaction log
            await self._log_ai_interaction(
                business_id=request.business_id,
                user_id=request.user_id,
                task_type=request.task_type,
                prompt=prompt_config["user_prompt"],
                response=ai_response.content,
                cost=cost,
                success=True
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"content_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=True,
                result_data=validated_data,
                cost=cost,
                tokens_used=ai_response.tokens_used,
                processing_time=processing_time,
                model_used=ai_response.model
            )
            
        except Exception as e:
            logger.error(f"Content creation failed: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"content_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    async def process_video_scripting(self, request: AITaskRequest) -> AITaskResult:
        """Process video script generation request"""
        start_time = datetime.now()
        
        try:
            # Get business and campaign context
            business = await self._get_business(request.business_id)
            campaign_id = request.parameters.get("campaign_id")
            campaign = await self._get_campaign(campaign_id) if campaign_id else None
            
            if not business:
                raise AIServiceError(f"Business not found: {request.business_id}")
            
            # Extract parameters
            video_type = request.parameters.get("video_type", "reel")
            duration = request.parameters.get("duration", 30)
            
            # Build prompt with context injection
            prompt_config = self.prompt_builder.build_video_script_prompt(
                business=business,
                campaign=campaign,
                video_type=video_type,
                duration=duration
            )
            
            # Check safety constraints
            await self.safety_monitor.validate_request(request, prompt_config)
            
            # Execute AI request
            ai_response = await self._execute_ai_request_with_retry(
                task_id=f"video_{request.business_id}_{int(start_time.timestamp())}",
                prompt_config=prompt_config,
                request=request
            )
            
            # Validate response schema
            validated_data = await self.schema_validator.validate_response(
                ai_response.content,
                prompt_config["schema_type"]
            )
            
            # Track costs and usage
            cost = await self.cost_tracker.calculate_cost(ai_response)
            await self.usage_tracker.track_usage(request.business_id, ai_response, cost)
            
            # Store AI interaction log
            await self._log_ai_interaction(
                business_id=request.business_id,
                user_id=request.user_id,
                task_type=request.task_type,
                prompt=prompt_config["user_prompt"],
                response=ai_response.content,
                cost=cost,
                success=True
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"video_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=True,
                result_data=validated_data,
                cost=cost,
                tokens_used=ai_response.tokens_used,
                processing_time=processing_time,
                model_used=ai_response.model
            )
            
        except Exception as e:
            logger.error(f"Video scripting failed: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"video_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    async def process_analytics_insights(self, request: AITaskRequest) -> AITaskResult:
        """Process analytics insights generation request"""
        start_time = datetime.now()
        
        try:
            # Get business and campaign context
            business = await self._get_business(request.business_id)
            campaign_id = request.parameters.get("campaign_id")
            campaign = await self._get_campaign(campaign_id) if campaign_id else None
            
            if not business:
                raise AIServiceError(f"Business not found: {request.business_id}")
            
            # Get performance data
            performance_data = request.parameters.get("performance_data", {})
            
            if not performance_data:
                # Gather recent performance data if not provided
                performance_data = await self._gather_performance_data(request.business_id, campaign_id)
            
            # Build prompt with context injection
            prompt_config = self.prompt_builder.build_analytics_prompt(
                business=business,
                campaign=campaign,
                performance_data=performance_data
            )
            
            # Check safety constraints
            await self.safety_monitor.validate_request(request, prompt_config)
            
            # Execute AI request
            ai_response = await self._execute_ai_request_with_retry(
                task_id=f"analytics_{request.business_id}_{int(start_time.timestamp())}",
                prompt_config=prompt_config,
                request=request
            )
            
            # Validate response schema
            validated_data = await self.schema_validator.validate_response(
                ai_response.content,
                prompt_config["schema_type"]
            )
            
            # Track costs and usage
            cost = await self.cost_tracker.calculate_cost(ai_response)
            await self.usage_tracker.track_usage(request.business_id, ai_response, cost)
            
            # Store AI interaction log
            await self._log_ai_interaction(
                business_id=request.business_id,
                user_id=request.user_id,
                task_type=request.task_type,
                prompt=prompt_config["user_prompt"],
                response=ai_response.content,
                cost=cost,
                success=True
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"analytics_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=True,
                result_data=validated_data,
                cost=cost,
                tokens_used=ai_response.tokens_used,
                processing_time=processing_time,
                model_used=ai_response.model
            )
            
        except Exception as e:
            logger.error(f"Analytics insights failed: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"analytics_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    async def process_customer_messaging(self, request: AITaskRequest) -> AITaskResult:
        """Process customer message reply generation"""
        start_time = datetime.now()
        
        try:
            # Get business context
            business = await self._get_business(request.business_id)
            if not business:
                raise AIServiceError(f"Business not found: {request.business_id}")
            
            # Extract parameters
            customer_message = request.parameters.get("customer_message", "")
            context_messages = request.parameters.get("context_messages", [])
            
            if not customer_message:
                raise ValidationError("Customer message is required")
            
            # Build prompt with context injection
            prompt_config = self.prompt_builder.build_messaging_prompt(
                business=business,
                customer_message=customer_message,
                context_messages=context_messages
            )
            
            # Check safety constraints
            await self.safety_monitor.validate_request(request, prompt_config)
            
            # Execute AI request
            ai_response = await self._execute_ai_request_with_retry(
                task_id=f"messaging_{request.business_id}_{int(start_time.timestamp())}",
                prompt_config=prompt_config,
                request=request
            )
            
            # Validate response schema
            validated_data = await self.schema_validator.validate_response(
                ai_response.content,
                prompt_config["schema_type"]
            )
            
            # Track costs and usage
            cost = await self.cost_tracker.calculate_cost(ai_response)
            await self.usage_tracker.track_usage(request.business_id, ai_response, cost)
            
            # Store AI interaction log
            await self._log_ai_interaction(
                business_id=request.business_id,
                user_id=request.user_id,
                task_type=request.task_type,
                prompt=prompt_config["user_prompt"],
                response=ai_response.content,
                cost=cost,
                success=True
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"messaging_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=True,
                result_data=validated_data,
                cost=cost,
                tokens_used=ai_response.tokens_used,
                processing_time=processing_time,
                model_used=ai_response.model
            )
            
        except Exception as e:
            logger.error(f"Customer messaging failed: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AITaskResult(
                task_id=f"messaging_{request.business_id}_{int(start_time.timestamp())}",
                task_type=request.task_type,
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    async def _execute_ai_request_with_retry(self, task_id: str, prompt_config: Dict[str, Any], request: AITaskRequest) -> AIResponse:
        """Execute AI request with exponential backoff retry logic"""
        max_retries = request.max_retries
        base_delay = 1.0  # seconds
        
        for attempt in range(max_retries + 1):
            try:
                # Check rate limits
                await self._check_rate_limits(request.priority)
                
                # Create AI config
                ai_config = AIConfig(
                    model=self._select_optimal_model(request.task_type, request.priority),
                    temperature=prompt_config.get("temperature", 0.5),
                    max_tokens=prompt_config.get("max_tokens", 1500),
                    stop_sequences=prompt_config.get("stop_sequences", [])
                )
                
                # Execute AI request
                response = await self.ai_client.generate(
                    prompt=prompt_config["user_prompt"],
                    system_prompt=prompt_config["system_prompt"],
                    config=ai_config
                )
                
                # Log successful request
                await self.performance_monitor.log_request(task_id, attempt + 1, True, response)
                
                return response
                
            except RateLimitError as e:
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit hit for task {task_id}, retrying in {delay}s")
                    await asyncio.sleep(delay)
                    continue
                else:
                    logger.error(f"Max retries exceeded for task {task_id} due to rate limits")
                    raise e
                    
            except Exception as e:
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"AI request failed for task {task_id}, retrying in {delay}s: {str(e)}")
                    await asyncio.sleep(delay)
                    continue
                else:
                    logger.error(f"Max retries exceeded for task {task_id}: {str(e)}")
                    await self.performance_monitor.log_request(task_id, attempt + 1, False, None, str(e))
                    raise e
                    
        raise AIServiceError(f"Failed to execute AI request after {max_retries + 1} attempts")
    
    async def _check_rate_limits(self, priority: AITaskPriority):
        """Check and enforce rate limits based on priority"""
        # Implementation would involve checking current request rates
        # and enforcing limits based on priority
        pass
    
    def _select_optimal_model(self, task_type: AITaskType, priority: AITaskPriority) -> str:
        """Select optimal AI model based on task type and priority"""
        model_selection = {
            AITaskType.STRATEGY_GENERATION: {
                AITaskPriority.CRITICAL: "gpt-4-1106-preview",
                AITaskPriority.HIGH: "gpt-4-1106-preview",
                AITaskPriority.NORMAL: "gpt-3.5-turbo-1106",
                AITaskPriority.LOW: "gpt-3.5-turbo-1106"
            },
            AITaskType.CONTENT_CREATION: {
                AITaskPriority.CRITICAL: "gpt-4-1106-preview",
                AITaskPriority.HIGH: "gpt-4-1106-preview", 
                AITaskPriority.NORMAL: "gpt-3.5-turbo-1106",
                AITaskPriority.LOW: "gpt-3.5-turbo-1106"
            },
            AITaskType.VIDEO_SCRIPTING: {
                AITaskPriority.CRITICAL: "gpt-4-1106-preview",
                AITaskPriority.HIGH: "gpt-4-1106-preview",
                AITaskPriority.NORMAL: "gpt-3.5-turbo-1106",
                AITaskPriority.LOW: "gpt-3.5-turbo-1106"
            },
            AITaskType.ANALYTICS_INSIGHTS: {
                AITaskPriority.CRITICAL: "gpt-4-1106-preview",
                AITaskPriority.HIGH: "gpt-3.5-turbo-1106",
                AITaskPriority.NORMAL: "gpt-3.5-turbo-1106",
                AITaskPriority.LOW: "gpt-3.5-turbo-1106"
            },
            AITaskType.CUSTOMER_MESSAGING: {
                AITaskPriority.CRITICAL: "gpt-4-1106-preview",
                AITaskPriority.HIGH: "gpt-3.5-turbo-1106",
                AITaskPriority.NORMAL: "gpt-3.5-turbo-1106",
                AITaskPriority.LOW: "gpt-3.5-turbo-1106"
            }
        }
        
        return model_selection.get(task_type, {}).get(priority, "gpt-3.5-turbo-1106")
    
    async def _get_business(self, business_id: str) -> Optional[Business]:
        """Get business by ID - placeholder for database query"""
        # This would connect to the MongoDB database
        # For now returning None to avoid database dependency
        return None
    
    async def _get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Get campaign by ID - placeholder for database query"""
        # This would connect to the MongoDB database
        return None
    
    async def _gather_performance_data(self, business_id: str, campaign_id: Optional[str] = None) -> Dict[str, Any]:
        """Gather performance data for analytics"""
        # Placeholder for gathering performance data from database
        return {
            "total_posts": 0,
            "avg_engagement_rate": 0.0,
            "platform_performance": {},
            "content_type_performance": {}
        }
    
    async def _log_ai_interaction(self, business_id: str, user_id: str, task_type: AITaskType,
                                prompt: str, response: str, cost: float, success: bool,
                                error: str = None):
        """Log AI interaction to database"""
        # This would create an AILog entry in MongoDB
        pass

class SafetyMonitor:
    """Safety monitoring and content validation"""
    
    async def validate_request(self, request: AITaskRequest, prompt_config: Dict[str, Any]):
        """Validate request for safety and compliance"""
        # Implement content safety checks
        pass

class PerformanceMonitor:
    """Performance monitoring and optimization"""
    
    async def log_request(self, task_id: str, attempt: int, success: bool, response: Optional[AIResponse], error: str = None):
        """Log request performance data"""
        # Implement performance tracking
        pass

class UsageTracker:
    """Track AI usage patterns and limits"""
    
    async def track_usage(self, business_id: str, response: AIResponse, cost: float):
        """Track usage statistics"""
        # Implement usage tracking
        pass