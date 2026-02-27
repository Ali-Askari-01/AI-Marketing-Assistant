"""
AI Client Module
Handles communication with OpenAI API
Updated for new OpenAI SDK and proper error handling
"""

import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from core.config import settings
from core.errors import AIServiceError
import json

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIClient:
    """AI client for OpenAI API communication"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.default_model = settings.DEFAULT_AI_MODEL
        self.fallback_model = settings.FALLBACK_AI_MODEL
        self.timeout = settings.AI_TIMEOUT_SECONDS
        self.max_retries = settings.AI_MAX_RETRIES
        self.client = None
        
        # Initialize OpenAI client if API key is available
        if self.api_key and OPENAI_AVAILABLE:
            self.client = AsyncOpenAI(api_key=self.api_key)
        elif not OPENAI_AVAILABLE:
            print("Warning: OpenAI package not installed. Running in demo mode.")
        elif not self.api_key:
            print("Warning: No OpenAI API key provided. Running in demo mode.")
    
    async def generate_response(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate AI response with retry logic"""
        model = model or self.default_model
        
        for attempt in range(self.max_retries):
            try:
                # Check if we're in demo mode
                if not self.client:
                    return self._create_mock_response(prompt, model)
                
                # Prepare messages
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                # Prepare request parameters
                request_params = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                }
                
                # Add max tokens if specified
                if max_tokens:
                    request_params["max_tokens"] = max_tokens
                
                # Add response format for structured output (GPT-4 and newer)
                if response_format and model in ["gpt-4o-mini", "gpt-4", "gpt-4-turbo"]:
                    request_params["response_format"] = response_format
                
                # Make API call
                start_time = datetime.now(timezone.utc)
                response = await self.client.chat.completions.create(**request_params)
                end_time = datetime.now(timezone.utc)
                
                # Extract response data
                content = response.choices[0].message.content
                
                return {
                    "success": True,
                    "content": content,
                    "model": model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    "response_time_ms": int((end_time - start_time).total_seconds() * 1000),
                    "attempt": attempt + 1
                }
                
            except Exception as e:
                error_message = str(e)
                
                # Handle rate limits
                if "rate limit" in error_message.lower():
                    if attempt == self.max_retries - 1:
                        raise AIServiceError(f"Rate limit exceeded after {self.max_retries} attempts")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                    
                # Handle timeouts
                elif "timeout" in error_message.lower():
                    if attempt == self.max_retries - 1:
                        raise AIServiceError(f"Request timeout after {self.max_retries} attempts")
                    await asyncio.sleep(1)
                    continue
                
                # For other errors, try fallback model on last attempt
                elif attempt == self.max_retries - 1 and model != self.fallback_model:
                    model = self.fallback_model
                    continue
                    
                else:
                    raise AIServiceError(f"AI API error: {error_message}")
        
    
    async def generate_json_response(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.3,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate JSON response with schema validation"""
        try:
            # Prepare JSON schema
            json_schema = schema or {
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "success": {"type": "boolean"}
                },
                "required": ["content", "success"]
            }
            
            response_format = {
                "type": "json_schema",
                "json_schema": json_schema
            }
            
            # Generate response
            result = await self.generate_response(
                prompt=prompt,
                model=model,
                temperature=temperature,
                system_prompt=system_prompt,
                response_format=response_format
            )
            
            # Parse JSON response
            if result["success"]:
                try:
                    content = result["content"]
                    if isinstance(content, str):
                        parsed_content = json.loads(content)
                        return {
                            **result,
                            "parsed_content": parsed_content
                        }
                    else:
                        return result
                except json.JSONDecodeError as e:
                    raise AIServiceError(f"Failed to parse JSON response: {str(e)}")
            
            return result
            
        except AIServiceError:
            raise
        except Exception as e:
            raise AIServiceError(f"Failed to generate JSON response: {str(e)}")
    
    async def generate_structured_response(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.3,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate structured response with schema validation"""
        try:
            # Add JSON formatting instruction to prompt
            json_prompt = f"""
{prompt}

IMPORTANT: Respond with valid JSON only. No explanations or additional text.
"""
            
            # Generate JSON response
            return await self.generate_json_response(
                prompt=json_prompt,
                model=model,
                temperature=temperature,
                system_prompt=system_prompt,
                schema=schema
            )
            
        except AIServiceError:
            raise
        except Exception as e:
            raise AIServiceError(f"Failed to generate structured response: {str(e)}")
    
    def _create_mock_response(self, prompt: str, model: str) -> Dict[str, Any]:
        """Create mock response for demo mode"""
        import uuid
        
        # Simple mock response based on prompt content
        if "strategy" in prompt.lower() or "campaign" in prompt.lower():
            content = json.dumps({
                "campaign_name": "New Marketing Campaign",
                "duration_days": 30,
                "main_themes": ["Brand Awareness", "Product Launch", "Customer Engagement"],
                "weekly_schedule": {
                    "week_1": {"posts": 3, "theme": "Brand Awareness"},
                    "week_2": {"posts": 4, "theme": "Product Features"},
                    "week_3": {"posts": 3, "theme": "Customer Stories"},
                    "week_4": {"posts": 4, "theme": "Call to Action"}
                },
                "kpis": {
                    "target_reach": 10000,
                    "target_engagement_rate": 3.5,
                    "target_conversions": 100
                }
            })
        elif "content" in prompt.lower():
            content = json.dumps({
                "content": "🚀 Revolutionize your business with AI! Our cutting-edge solutions help you automate processes, boost efficiency, and drive growth. Ready to transform your future? #AI #Innovation #BusinessGrowth",
                "hashtags": ["#AI", "#Innovation", "#BusinessGrowth", "#Productivity"],
                "platform": "instagram",
                "content_type": "post"
            })
        else:
            content = f"Mock AI response for {model} model. Prompt: {prompt[:100]}..."
        
        return {
            "success": True,
            "content": content,
            "model": model,
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(content.split()) if isinstance(content, str) else 50,
                "total_tokens": len(prompt.split()) + (len(content.split()) if isinstance(content, str) else 50)
            },
            "response_time_ms": 500,
            "attempt": 1
        }
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get AI service status"""
        return {
            "status": "available" if self.client else "demo_mode",
            "api_key_configured": bool(self.api_key),
            "openai_available": OPENAI_AVAILABLE,
            "default_model": self.default_model,
            "fallback_model": self.fallback_model,
            "max_retries": self.max_retries,
            "timeout": self.timeout
        }
    
    def get_cost_estimate(self, prompt_tokens: int, completion_tokens: int, model: str) -> float:
        """Estimate cost for API call"""
        # Pricing per 1M tokens (approximate)
        pricing = {
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
        }
        
        model_pricing = pricing.get(model, pricing["gpt-4o"])
        
        input_cost = (prompt_tokens / 1000000) * model_pricing["input"]
        output_cost = (completion_tokens / 1000000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return bool(self.api_key) or settings.DEBUG


# Global AI client instance
ai_client = AIClient()
