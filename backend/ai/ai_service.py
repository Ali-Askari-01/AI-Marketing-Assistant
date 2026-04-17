"""
AI Service Layer
Orchestrates AI operations with proper abstraction and error handling
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from core.config import settings
from core.errors import AIServiceError, ValidationError
from ai.ai_client import ai_client
from ai.prompt_builder import prompt_builder
from ai.schema_validator import schema_validator
from ai.cost_tracker import cost_tracker
import json

class AIService:
    """AI service orchestrator"""
    
    def __init__(self):
        self.ai_client = ai_client
        self.prompt_builder = prompt_builder
        self.schema_validator = schema_validator
        self.cost_tracker = cost_tracker
        self.service_types = ["strategy", "content", "analytics", "messaging"]
    
    async def generate_strategy(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI strategy for campaigns"""
        strategy_type = request_data.get("strategy_type", "campaign_calendar")
        
        if strategy_type == "campaign_calendar":
            return await self._generate_campaign_calendar(request_data)
        elif strategy_type == "kpi_generator":
            return await self._generate_kpis(request_data)
        elif strategy_type == "media_mix_optimizer":
            return await self._optimize_media_mix(request_data)
        else:
            raise AIServiceError(f"Unknown strategy type: {strategy_type}")
    
    async def _generate_campaign_calendar(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate campaign calendar"""
        try:
            # Build prompt
            prompt = self.prompt_builder.build_prompt("strategy", "campaign_calendar", request_data)
            
            # Determine model based on complexity
            model = self._select_model("strategy", request_data)
            
            # Generate response
            start_time = datetime.utcnow()
            response = await self.ai_client.generate_structured_response(
                prompt=prompt,
                model=model,
                temperature=0.3,
                system_prompt=self.prompt_builder.system_prompts["strategy"],
                schema=self._get_strategy_schema()
            )
            
            # Calculate response time
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Validate response
            validated_response = self.schema_validator.validate_response("campaign_calendar", response.get("parsed_content", response.get("content", {})))
            
            # Track usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "strategy",
                "model_used": model,
                "prompt_template": "campaign_calendar",
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms,
                "success": response.get("success", False),
                "error_message": None if response.get("success") else "AI generation failed"
            })
            
            # Format response
            return {
                "success": True,
                "data": validated_response,
                "model": model,
                "response_time_ms": response_time_ms,
                "cost_estimate": self.cost_tracker.calculate_cost(
                    model,
                    response.get("usage", {}).get("prompt_tokens", 0),
                    response.get("usage", {}).get("completion_tokens", 0)
                )
            }
            
        except ValidationError as e:
            # Track failed usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "strategy",
                "model_used": model,
                "prompt_template": "campaign_calendar",
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "response_time_ms": 0,
                "success": False,
                "error_message": str(e)
            })
            raise AIServiceError(f"Strategy validation failed: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Strategy generation failed: {str(e)}")
    
    async def _generate_kpis(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate KPI recommendations"""
        try:
            # Build prompt
            prompt = self.prompt_builder.build_prompt("strategy", "kpi_generator", request_data)
            
            # Generate response
            model = self._select_model("strategy", request_data)
            start_time = datetime.utcnow()
            response = await self.ai_client.generate_structured_response(
                prompt=prompt,
                model=model,
                temperature=0.2,
                system_prompt=self.prompt_builder.system_prompts["strategy"]
            )
            
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            validated_response = response.get("parsed_content", response.get("content", {}))
            
            # Track usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "strategy",
                "model_used": model,
                "prompt_template": "kpi_generator",
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms,
                "success": response.get("success", False)
            })
            
            return {
                "success": True,
                "data": validated_response,
                "model": model,
                "response_time_ms": response_time_ms,
                "cost_estimate": self.cost_tracker.calculate_cost(
                    model,
                    response.get("usage", {}).get("prompt_tokens", 0),
                    response.get("usage", {}).get("completion_tokens", 0)
                )
            }
        except Exception as e:
            raise AIServiceError(f"KPI generation failed: {str(e)}")
    
    async def _optimize_media_mix(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize media mix based on performance data"""
        try:
            # Build prompt
            prompt = self.prompt_builder.build_prompt("strategy", "media_mix_optimizer", request_data)
            
            # Generate response
            model = self._select_model("analytics", request_data)
            start_time = datetime.utcnow()
            response = await self.ai_client.generate_structured_response(
                prompt=prompt,
                model=model,
                temperature=0.3,
                system_prompt=self.prompt_builder.system_prompts["analytics"]
            )
            
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            validated_response = response.get("parsed_content", response.get("content", {}))
            
            # Track usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "analytics",
                "model_used": model,
                "prompt_template": "media_mix_optimizer",
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms,
                "success": response.get("success", False)
            })
            
            return {
                "success": True,
                "data": validated_response,
                "model": model,
                "response_time_ms": response_time_ms,
                "cost_estimate": self.cost_tracker.calculate_cost(
                    model,
                    response.get("usage", {}).get("prompt_tokens", 0),
                    response.get("usage", {}).get("completion_tokens", 0)
                )
            }
        except Exception as e:
            raise AIServiceError(f"Media mix optimization failed: {str(e)}")
    
    async def generate_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI content"""
        content_type = request_data.get("content_type", "text")
        
        if content_type == "text":
            return await self._generate_text_content(request_data)
        elif content_type == "visual":
            return await self._generate_visual_content(request_data)
        elif content_type == "video":
            return await self._generate_video_content(request_data)
        else:
            raise AIServiceError(f"Unknown content type: {content_type}")
    
    async def _generate_text_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate text content"""
        try:
            # Build prompt
            prompt = self.prompt_builder.build_prompt("content", "text_generator", request_data)
            
            # Determine model based on content type
            model = self._select_model("content", request_data)
            
            # Generate response
            start_time = datetime.utcnow()
            response = await self.ai_client.generate_structured_response(
                prompt=prompt,
                model=model,
                temperature=0.7,
                system_prompt=self.prompt_builder.system_prompts["content"],
                schema=self._get_content_schema("text")
            )
            
            # Calculate response time
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Validate response
            validated_response = self.schema_validator.validate_response("content_generator", response.get("parsed_content", response.get("content", {})))
            
            # Track usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "content",
                "model_used": model,
                "prompt_template": "text_generator",
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms,
                "success": response.get("success", False),
                "error_message": None if response.get("success") else "Content generation failed"
            })
            
            # Format response
            return {
                "success": True,
                "data": validated_response,
                "model": model,
                "response_time_ms": response_time_ms,
                "cost_estimate": self.cost_tracker.calculate_cost(
                    model,
                    response.get("usage", {}).get("prompt_tokens", 0),
                    response.get("usage", {}).get("completion_tokens", 0)
                )
            }
            
        except ValidationError as e:
            # Track failed usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "content",
                "model_used": model,
                "prompt_template": "text_generator",
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "response_time_ms": 0,
                "success": False,
                "error_message": str(e)
            })
            raise AIServiceError(f"Content validation failed: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Content generation failed: {str(e)}")
    
    async def _generate_visual_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual content concept"""
        try:
            # Build prompt
            prompt = self.prompt_builder.build_prompt("content", "visual_generator", request_data)
            
            model = self._select_model("content", request_data)
            start_time = datetime.utcnow()
            response = await self.ai_client.generate_structured_response(
                prompt=prompt,
                model=model,
                temperature=0.8,
                system_prompt=self.prompt_builder.system_prompts["content"],
                schema=self._get_content_schema("visual")
            )
            
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            validated_response = response.get("parsed_content", response.get("content", {}))
            
            # Track usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "content",
                "model_used": model,
                "prompt_template": "visual_generator",
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms,
                "success": response.get("success", False)
            })
            
            return {
                "success": True,
                "data": validated_response,
                "model": model,
                "response_time_ms": response_time_ms,
                "cost_estimate": self.cost_tracker.calculate_cost(
                    model,
                    response.get("usage", {}).get("prompt_tokens", 0),
                    response.get("usage", {}).get("completion_tokens", 0)
                )
            }
        except Exception as e:
            raise AIServiceError(f"Visual content generation failed: {str(e)}")
    
    async def _generate_video_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate video script"""
        try:
            # Build prompt
            prompt = self.prompt_builder.build_prompt("content", "video_script_generator", request_data)
            
            model = self._select_model("content", request_data)
            start_time = datetime.utcnow()
            response = await self.ai_client.generate_structured_response(
                prompt=prompt,
                model=model,
                temperature=0.75,
                system_prompt=self.prompt_builder.system_prompts["content"],
                schema=self._get_content_schema("video")
            )
            
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            validated_response = response.get("parsed_content", response.get("content", {}))
            
            # Track usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "content",
                "model_used": model,
                "prompt_template": "video_script_generator",
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms,
                "success": response.get("success", False)
            })
            
            return {
                "success": True,
                "data": validated_response,
                "model": model,
                "response_time_ms": response_time_ms,
                "cost_estimate": self.cost_tracker.calculate_cost(
                    model,
                    response.get("usage", {}).get("prompt_tokens", 0),
                    response.get("usage", {}).get("completion_tokens", 0)
                )
            }
        except Exception as e:
            raise AIServiceError(f"Video script generation failed: {str(e)}")
    
    async def generate_analytics(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI analytics insights"""
        try:
            # Build prompt
            prompt = self.prompt_builder.build_analytics_prompt(request_data)
            
            # Determine model based on complexity
            model = self._select_model("analytics", request_data)
            
            # Generate response
            start_time = datetime.utcnow()
            response = await self.ai_client.generate_structured_response(
                prompt=prompt,
                model=model,
                temperature=0.3,
                system_prompt=self.prompt_builder.system_prompts["analytics"],
                schema=self._get_analytics_schema()
            )
            
            # Calculate response time
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Validate response
            validated_response = self.schema_validator.validate_response("analytics_analyzer", response.get("parsed_content", response.get("content", {})))
            
            # Track usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "analytics",
                "model_used": model,
                "prompt_template": "performance_analyzer",
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms,
                "success": response.get("success", False),
                "error_message": None if response.get("success") else "Analytics generation failed"
            })
            
            # Format response
            return {
                "success": True,
                "data": validated_response,
                "model": model,
                "response_time_ms": response_time_ms,
                "cost_estimate": self.cost_tracker.calculate_cost(
                    model,
                    response.get("usage", {}).get("prompt_tokens", 0),
                    response.get("usage", {}).get("completion_tokens", 0)
                )
            }
            
        except ValidationError as e:
            # Track failed usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "analytics",
                "model_used": model,
                "prompt_template": "performance_analyzer",
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "response_time_ms": 0,
                "success": False,
                "error_message": str(e)
            })
            raise AIServiceError(f"Analytics validation failed: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Analytics generation failed: {str(e)}")
    
    async def generate_message_reply(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI message reply"""
        try:
            # Build prompt
            prompt = self.prompt_builder.build_messaging_prompt(request_data)
            
            # Determine model based on complexity
            model = self._select_model("messaging", request_data)
            
            # Generate response
            start_time = datetime.utcnow()
            response = await self.ai_client.generate_structured_response(
                prompt=prompt,
                model=model,
                temperature=0.5,
                system_prompt=self.prompt_builder.system_prompts["messaging"],
                schema=self._get_messaging_schema()
            )
            
            # Calculate response time
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Validate response
            validated_response = self.schema_validator.validate_response("customer_reply", response.get("parsed_content", response.get("content", {})))
            
            # Track usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "messaging",
                "model_used": model,
                "prompt_template": "customer_reply",
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "response_time_ms": response_time_ms,
                "success": response.get("success", False),
                "error_message": None if response.get("success") else "Message generation failed"
            })
            
            # Format response
            return {
                "success": True,
                "data": validated_response,
                "model": model,
                "response_time_ms": response_time_ms,
                "cost_estimate": self.cost_tracker.calculate_cost(
                    model,
                    response.get("usage", {}).get("prompt_tokens", 0),
                    response.get("usage", {}).get("completion_tokens", 0)
                )
            }
            
        except ValidationError as e:
            # Track failed usage
            self.cost_tracker.track_usage({
                "business_id": request_data.get("business_id"),
                "user_id": request_data.get("user_id"),
                "service_type": "messaging",
                "model_used": model,
                "prompt_template": "customer_reply",
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "response_time_ms": 0,
                "success": False,
                "error_message": str(e)
            })
            raise AIServiceError(f"Message validation failed: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Message generation failed: {str(e)}")
    
    def _select_model(self, service_type: str, request_data: Dict[str, Any]) -> str:
        """Select appropriate AI model based on service type and complexity"""
        # Default models for each service type
        default_models = {
            "strategy": settings.OPENAI_MODEL_STRATEGY,
            "content": settings.OPENAI_MODEL_CONTENT,
            "analytics": settings.OPENAI_MODEL_STRATEGY,
            "messaging": settings.OPENAI_MODEL_CONTENT
        }
        
        model = default_models.get(service_type, settings.OPENAI_MODEL_STRATEGY)
        
        # Override with specific model if requested
        if "model" in request_data:
            model = request_data["model"]
        
        # Use cheaper model for simple content generation
        if service_type == "content" and request_data.get("complexity", "medium") == "simple":
            model = settings.OPENAI_MODEL_CONTENT
        
        return model
    
    def _get_strategy_schema(self) -> Dict[str, Any]:
        """Get schema for strategy generation"""
        return {
            "type": "object",
            "properties": {
                "campaign_calendar": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "theme": {"type": "string"},
                            "content_type": {"type": "string"},
                            "platform": {"type": "string"},
                            "objective": {"type": "string"},
                            "key_message": {"type": "string"}
                        }
                    }
                },
                "weekly_themes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "week": {"type": "integer"},
                            "theme": {"type": "string"},
                            "focus": {"type": "string"},
                            "kpis": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "content_distribution": {
                    "type": "object",
                    "properties": {
                        "instagram": {"type": "integer"},
                        "linkedin": {"type": "integer"},
                        "email": {"type": "integer"},
                        "sms": {"type": "integer"}
                    }
                }
            },
            "required": ["campaign_calendar", "weekly_themes", "content_distribution"]
        }
    
    def _get_content_schema(self, content_type: str) -> Dict[str, Any]:
        """Get schema for content generation"""
        base_schema = {
            "type": "object",
            "properties": {
                "content_type": {"type": "string"},
                "platform": {"type": "string"},
                "headline": {"type": "string"},
                "body": {"type": "string"},
                "cta": {"type": "string"},
                "hashtags": {"type": "array", "items": {"type": "string"}},
                "predicted_engagement_score": {"type": "number"}
            },
            "required": ["content_type", "platform", "headline", "body", "cta", "hashtags", "predicted_engagement_score"]
        }
        
        # Add content-type specific fields
        if content_type == "visual":
            base_schema["properties"].update({
                "visual_description": {"type": "string"},
                "design_direction": {"type": "object"},
                "image_generation_prompt": {"type": "string"}
            })
        elif content_type == "video":
            base_schema["properties"].update({
                "script": {"type": "object"},
                "duration_seconds": {"type": "integer"},
                "production_notes": {"type": "string"}
            })
        
        return base_schema
    
    def _get_analytics_schema(self) -> Dict[str, Any]:
        """Get schema for analytics generation"""
        return {
            "type": "object",
            "properties": {
                "performance_summary": {
                    "type": "object",
                    "properties": {
                        "overall_score": {"type": "number"},
                        "engagement_rate": {"type": "number"},
                        "conversion_rate": {"type": "number"},
                        "reach": {"type": "integer"}
                    }
                },
                "top_performing_content": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "engagement_score": {"type": "number"},
                            "key_factors": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "weak_segments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "area": {"type": "string"},
                            "issues": {"type": "array", "items": {"type": "string"}},
                            "recommendations": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "optimization_opportunities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "opportunity": {"type": "string"},
                            "potential_impact": {"type": "string"},
                            "effort_required": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["performance_summary", "top_performing_content", "weak_segments", "optimization_opportunities"]
        }
    
    def _get_messaging_schema(self) -> Dict[str, Any]:
        """Get schema for message generation"""
        return {
            "type": "object",
            "properties": {
                "response_type": {"type": "string"},
                "platform": {"type": "string"},
                "reply_text": {"type": "string"},
                "tone": {"type": "string"},
                "escalation_needed": {"type": "boolean"},
                "follow_up_required": {"type": "boolean"},
                "sentiment": {"type": "string"},
                "confidence_score": {"type": "number"},
                "next_action": {"type": "string"}
            },
            "required": ["response_type", "platform", "reply_text", "tone", "escalation_needed", "follow_up_required", "sentiment", "confidence_score", "next_action"]
        }
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get AI service status"""
        try:
            # Check AI client availability
            ai_available = self.ai_client.is_available()
            
            # Get model info
            model_info = await self.ai_client.get_model_info(settings.OPENAI_MODEL_STRATEGY)
            
            # Get recent usage
            daily_usage = self.cost_tracker.get_daily_usage()
            
            return {
                "status": "healthy" if ai_available else "unhealthy",
                "ai_client_available": ai_available,
                "current_model": settings.OPENAI_MODEL_STRATEGY,
                "model_info": model_info,
                "daily_usage": daily_usage,
                "supported_services": self.service_types,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_usage_statistics(self, period: str = "daily") -> Dict[str, Any]:
        """Get usage statistics"""
        try:
            if period == "daily":
                return self.cost_tracker.get_daily_usage()
            elif period == "weekly":
                return self.cost_tracker.get_weekly_usage()
            elif period == "monthly":
                return self.cost_tracker.get_monthly_usage()
            else:
                raise ValidationError(f"Invalid period: {period}")
                
        except Exception as e:
            raise AIServiceError(f"Failed to get usage statistics: {str(e)}")
    
    async def get_cost_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """Get cost optimization suggestions"""
        try:
            return self.cost_tracker.get_cost_optimization_suggestions()
        except Exception as e:
            raise AIServiceError(f"Failed to get optimization suggestions: {str(e)}")

# Global AI service instance
ai_service = AIService()
