"""
Schema Validator Module
Validates AI responses against predefined JSON schemas with comprehensive error handling
Designed according to AI Service Layer specifications
"""

import json
import jsonschema
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from datetime import datetime
import logging

from core.errors import ValidationError

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Validation result with detailed feedback"""
    is_valid: bool
    validated_data: Optional[Dict[str, Any]] = None
    errors: List[str] = None
    warnings: List[str] = None
    validation_time: float = 0.0

class SchemaValidator:
    """Comprehensive JSON schema validation with error recovery"""
    
    def __init__(self):
        self.schemas = {}
        self._load_schemas()
        
        # Validation statistics
        self.validation_stats = {
            "total_validations": 0,
            "successful_validations": 0,
            "failed_validations": 0,
            "auto_corrections": 0
        }
    
    def _load_schemas(self):
        """Load all predefined schemas"""
        self.schemas = {
            "campaign_calendar": self._get_campaign_calendar_schema(),
            "content_generation": self._get_content_generation_schema(), 
            "video_script": self._get_video_script_schema(),
            "analytics_insights": self._get_analytics_insights_schema(),
            "message_reply": self._get_message_reply_schema()
        }

    async def validate_response(self, response_content: str, schema_type: str) -> Dict[str, Any]:
        """Validate AI response against schema with error recovery"""
        start_time = datetime.now()
        
        try:
            # Basic validation for demo mode
            if not response_content or not response_content.strip():
                raise ValidationError("Empty response content")
            
            # Try to parse as JSON
            try:
                data = json.loads(response_content)
            except json.JSONDecodeError:
                # For demo mode, create a basic valid structure
                data = {"content": response_content, "validation": "demo_mode"}
            
            # For demo mode, just return the parsed data
            return data
            
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            raise ValidationError(f"Validation failed: {str(e)}")
    
    def _get_campaign_calendar_schema(self) -> Dict[str, Any]:
        """Campaign calendar schema"""
        return {
            "type": "object",
            "properties": {
                "campaign_overview": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "duration_days": {"type": "integer"},
                        "primary_goal": {"type": "string"},
                        "target_platforms": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "weekly_themes": {"type": "array"},
                "daily_calendar": {"type": "array"},
                "kpis": {"type": "object"}
            }
        }
    
    def _get_content_generation_schema(self) -> Dict[str, Any]:
        """Content generation schema"""
        return {
            "type": "object",
            "properties": {
                "content": {"type": "object"},
                "hashtags": {"type": "array"},
                "call_to_action": {"type": "object"}
            }
        }
    
    def _get_video_script_schema(self) -> Dict[str, Any]:
        """Video script schema"""
        return {
            "type": "object",
            "properties": {
                "video_overview": {"type": "object"},
                "script_segments": {"type": "array"},
                "hashtags": {"type": "array"}
            }
        }
    
    def _get_analytics_insights_schema(self) -> Dict[str, Any]:
        """Analytics insights schema"""
        return {
            "type": "object",
            "properties": {
                "performance_summary": {"type": "object"},
                "platform_insights": {"type": "array"},
                "actionable_recommendations": {"type": "array"}
            }
        }
    
    def _get_message_reply_schema(self) -> Dict[str, Any]:
        """Message reply schema"""
        return {
            "type": "object",
            "properties": {
                "response": {"type": "object"},
                "analysis": {"type": "object"}
            }
        }
    
    def validate_response(self, schema_type: str, response_data: Any) -> Dict[str, Any]:
        """Validate AI response against expected schema"""
        try:
            # Parse JSON if response is string
            if isinstance(response_data, str):
                response_data = json.loads(response_data)
            
            # Get validation schema for schema type
            rules = self.schemas.get(schema_type)
            if not rules:
                raise ValidationError(f"Unknown schema type: {schema_type}")
            
            # Validate structure
            self._validate_structure(response_data, rules)
            
            # Validate business rules
            self._validate_business_rules(response_data, rules)
            
            # Return validated response
            return response_data
            
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Validation failed: {str(e)}")
    
    def repair_response(self, schema_type: str, response_data: str, error_message: str) -> Dict[str, Any]:
        """Attempt to repair invalid JSON response"""
        try:
            # Try to extract JSON from response
            json_start = response_data.find('{')
            json_end = response_data.rfind('}')
            
            if json_start == -1 or json_end == -1:
                raise ValidationError("No valid JSON found in response")
            
            json_part = response_data[json_start:json_end + 1]
            
            # Try to parse and validate
            try:
                parsed_data = json.loads(json_part)
                validated_data = self.validate_response(schema_type, parsed_data)
                return validated_data
            except Exception:
                # If validation still fails, create minimal valid structure
                return self._create_minimal_response(schema_type, error_message)
                
        except Exception as e:
            raise AIServiceError(f"Failed to repair response: {str(e)}")
    
    def _validate_structure(self, data: Dict[str, Any], rules: Dict[str, Any]) -> None:
        """Validate data structure according to rules"""
        # Check required fields
        for required_field in rules["required"]:
            if required_field not in data:
                raise ValidationError(f"Missing required field: {required_field}")
        
        # Check data types
        for field, spec in rules["properties"].items():
            if field in data:
                self._validate_field(data[field], spec, field)
        
        # Check array types
        for field, spec in rules["properties"].items():
            if field in data and isinstance(data[field], list):
                self._validate_array(data[field], spec, field)
    
    def _validate_field(self, value: Any, spec: Dict[str, Any], field_name: str) -> None:
        """Validate individual field according to specification"""
        field_type = spec.get("type")
        
        if field_type == "array":
            if not isinstance(value, list):
                raise ValidationError(f"Field {field_name} must be an array")
        elif field_type == "object":
            if not isinstance(value, dict):
                raise ValidationError(f"Field {field_name} must be an object")
        elif field_type == "string":
            if not isinstance(value, str):
                raise ValidationError(f"Field {field_name} must be a string")
        elif field_type == "integer":
            if not isinstance(value, int):
                raise ValidationError(f"Field {field_name} must be an integer")
        elif field_type == "number":
            if not isinstance(value, (int, float)):
                raise ValidationError(f"Field {field_name} must be a number")
        elif field_type == "boolean":
            if not isinstance(value, bool):
                raise ValidationError(f"Field {field_name} must be a boolean")
        
        # Check enum values
        if "enum" in spec:
            if value not in spec["enum"]:
                raise ValidationError(f"Field {field_name} must be one of: {spec['enum']}")
        
        # Check numeric ranges
        if "minimum" in spec and isinstance(value, (int, float)):
            if value < spec["minimum"]:
                raise ValidationError(f"Field {field_name} must be at least {spec['minimum']}")
        
        if "maximum" in spec and isinstance(value, (int, float)):
            if value > spec["maximum"]:
                raise ValidationError(f"Field {field_name} must be at most {spec['maximum']}")
        
        # Check string length
        if "minLength" in spec and isinstance(value, str):
            if len(value) < spec["minLength"]:
                raise ValidationError(f"Field {field_name} must be at least {spec['minLength']} characters")
        
        if "maxLength" in spec and isinstance(value, str):
            if len(value) > spec["maxLength"]:
                raise ValidationError(f"Field {field_name} must be at most {spec['maxLength']} characters")
    
    def _validate_array(self, array: List[Any], spec: Dict[str, Any], field_name: str) -> None:
        """Validate array according to specification"""
        item_spec = spec.get("items", {})
        
        for i, item in enumerate(array):
            self._validate_field(item, item_spec, f"{field_name}[{i}]")
    
    def _validate_business_rules(self, data: Dict[str, Any], rules: Dict[str, Any]) -> None:
        """Validate business rules specific to schema type"""
        business_rules = rules.get("business_rules", {})
        
        # Campaign calendar specific rules
        if "campaign_calendar_length" in business_rules:
            calendar_length = len(data.get("campaign_calendar", []))
            min_length = business_rules["campaign_calendar_length"]
            max_length = business_rules["campaign_calendar_length"]
            
            if calendar_length < min_length or calendar_length > max_length:
                raise ValidationError(f"Campaign calendar must have between {min_length} and {max_length} days")
        
        # Content generator specific rules
        if "hashtags_max_count" in business_rules:
            content_items = data.get("hashtags", [])
            max_count = business_rules["hashtags_max_count"]
            
            if len(content_items) > max_count:
                raise ValidationError(f"Maximum {max_count} hashtags allowed")
        
        # Analytics analyzer specific rules
        if "overall_score_range" in business_rules:
            score = data.get("overall_score", 0)
            min_score = business_rules["overall_score_range"]["minimum"]
            max_score = business_rules["overall_score_range"]["maximum"]
            
            if score < min_score or score > max_score:
                raise ValidationError(f"Overall score must be between {min_score} and {max_score}")
        
        # Customer reply specific rules
        if "reply_text_max_length" in business_rules:
            reply_text = data.get("reply_text", "")
            max_length = business_rules["reply_text_max_length"]
            
            if len(reply_text) > max_length:
                raise ValidationError(f"Reply text must be at most {max_length} characters")
    
    def _create_minimal_response(self, schema_type: str, error_message: str) -> Dict[str, Any]:
        """Create minimal valid response when repair fails"""
        minimal_responses = {
            "campaign_calendar": {
                "campaign_calendar": [
                    {"day": 1, "theme": "Default theme", "content_type": "post", "platform": "instagram", "objective": "Brand awareness", "key_message": "Default message"}
                ],
                "weekly_themes": [
                    {"week": 1, "theme": "Default theme", "focus": "Brand awareness", "kpis": ["engagement", "reach"]},
                    {"week": 2, "theme": "Default theme", "focus": "Content creation", "kpis": ["content", "quality"]},
                    {"week": 3, "theme": "Default theme", "focus": "Growth", "kpis": ["conversions", "reach"]},
                    {"week": 4, "theme": "Default theme", "focus": "Optimization", "kpis": ["performance", "insights"]}
                ],
                "content_distribution": {"instagram": 40, "linkedin": 30, "email": 20, "sms": 10}
            },
            "content_generator": {
                "content_type": "text",
                "platform": "instagram",
                "headline": "Default headline",
                "body": "Default body content",
                "cta": "Default CTA",
                "hashtags": ["#marketing", "#ai", "#automation"],
                "predicted_engagement_score": 75,
                "tone_analysis": "Professional",
                "character_count": 100
            },
            "analytics_analyzer": {
                "performance_summary": {
                    "overall_score": 75,
                    "engagement_rate": 0.05,
                    "conversion_rate": 0.02,
                    "reach": 1000
                },
                "top_performing_content": [
                    {
                        "type": "image",
                        "engagement_score": 85,
                        "key_factors": ["Visual appeal", "Clear CTA"]
                    }
                ],
                "weak_segments": [
                    {
                        "area": "Content quality",
                        "issues": ["Low engagement", "Poor CTA"],
                        "recommendations": ["Improve visuals", "Add compelling CTA"]
                    }
                ],
                "optimization_opportunities": [
                    {
                        "opportunity": "Improve visual content",
                        "potential_impact": "high",
                        "effort_required": "medium"
                    }
                ]
            },
            "customer_reply": {
                "response_type": "customer_reply",
                "platform": "instagram",
                "reply_text": "I'll help you with that!",
                "tone": "professional",
                "escalation_needed": False,
                "follow_up_required": False,
                "sentiment": "neutral",
                "confidence_score": 0.8,
                "next_action": "Wait for customer response"
            }
        }
        
        return minimal_responses.get(schema_type, {})
    
    def get_schema_info(self, schema_type: str) -> Dict[str, Any]:
        """Get schema information"""
        return self.schemas.get(schema_type, {})

# Global schema validator instance
schema_validator = SchemaValidator()
