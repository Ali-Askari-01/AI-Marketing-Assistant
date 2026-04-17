"""
Prompt Builder Module
Builds and manages prompts for AI services
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from core.config import settings
import json

class PromptBuilder:
    """Prompt builder for AI services"""
    
    def __init__(self):
        self.system_prompts = self._initialize_system_prompts()
        self.prompt_templates = self._initialize_prompt_templates()
    
    def _initialize_system_prompts(self) -> Dict[str, str]:
        """Initialize system prompts for different AI services"""
        return {
            "strategy": """You are a senior marketing strategist with 15 years of experience in digital marketing, campaign planning, and growth analytics. You produce structured, actionable marketing strategies. Always respond in strict JSON format. Your expertise includes market research, content strategy, audience segmentation, and performance optimization. You analyze data-driven insights and create comprehensive marketing plans that drive measurable results.""",
            
            "content": """You are a creative content specialist with deep expertise in social media marketing, copywriting, and visual storytelling. You generate engaging, platform-specific content that resonates with target audiences. Always respond in strict JSON format. You understand brand voice, audience psychology, and content performance optimization. Your content drives engagement and conversions while maintaining brand consistency.""",
            
            "analytics": """You are a data-driven marketing analyst with expertise in performance metrics, A/B testing, and campaign optimization. You analyze complex marketing data and provide actionable insights. Always respond in strict JSON format. You identify trends, opportunities, and areas for improvement based on quantitative analysis. Your recommendations are data-backed and focused on ROI optimization.""",
            
            "messaging": """You are a professional brand communication specialist with expertise in customer service, brand voice consistency, and relationship building. You provide helpful, accurate, and brand-aligned responses. Always respond in strict JSON format. You understand customer psychology, conflict resolution, and brand values. Your responses build trust and strengthen customer relationships."""
        }
    
    def _initialize_prompt_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize prompt templates for different AI services"""
        return {
            "strategy": {
                "campaign_calendar": {
                    "system": self.system_prompts["strategy"],
                    "task": """Generate a {duration_days}-day content calendar for a marketing campaign.

BUSINESS CONTEXT:
Business: {business_name}
Industry: {industry}
Brand Voice: {brand_voice}
Target Audience: {target_audience}
Campaign Goal: {campaign_goal}

REQUIREMENTS:
- Create a structured calendar with daily content themes
- Distribute content across platforms: {platforms}
- Use content types: {content_types}
- Align content with campaign goal
- Balance content distribution appropriately
- Include weekly themes and KPI targets

Return valid JSON with the following structure:
{{
  "campaign_calendar": [
    {{
      "day": 1,
      "theme": "string",
      "content_type": "post|reel|story|carousel|video",
      "platform": "instagram|linkedin|email|sms",
      "objective": "string",
      "key_message": "string"
    }}
  ],
  "weekly_themes": [
    {{
      "week": 1,
      "theme": "string",
      "focus": "string",
      "kpis": ["string"]
    }}
  ],
  "content_distribution": {{
    "instagram": 40,
    "linkedin": 30,
    "email": 20,
    "sms": 10
  }},
  "recommendations": [
    {{
      "area": "string",
      "suggestion": "string",
      "expected_impact": "high|medium|low"
    }}
  ]
}}""",
                    "variables": ["business_name", "industry", "brand_voice", "target_audience", "campaign_goal", "duration_days", "platforms", "content_types"]
                },
                "kpi_generator": {
                    "system": self.system_prompts["strategy"],
                    "task": """Generate comprehensive KPI recommendations for a marketing campaign.

BUSINESS CONTEXT:
Business: {business_name}
Industry: {industry}
Campaign Goal: {campaign_goal}
Target Audience: {target_audience}
Campaign Duration: {duration_days} days

REQUIREMENTS:
- Define measurable primary KPIs aligned with campaign goal
- Include secondary KPIs for holistic measurement
- Provide realistic targets based on industry benchmarks
- Include measurement methods for each KPI
- Define success thresholds

Return valid JSON with the following structure:
{{
  "primary_kpis": [
    {{
      "name": "string",
      "target": 0,
      "unit": "string",
      "measurement_method": "string",
      "benchmark": 0,
      "priority": "critical|high|medium"
    }}
  ],
  "secondary_kpis": [
    {{
      "name": "string",
      "target": 0,
      "unit": "string",
      "importance": "high|medium|low"
    }}
  ],
  "success_metrics": {{
    "minimum_engagement_rate": 0,
    "conversion_target": 0,
    "brand_awareness_lift": 0,
    "roi_target": 0
  }},
  "measurement_plan": {{
    "tracking_frequency": "daily|weekly|monthly",
    "reporting_schedule": "string",
    "tools_required": ["string"]
  }}
}}""",
                    "variables": ["business_name", "industry", "campaign_goal", "target_audience", "duration_days"]
                },
                "media_mix_optimizer": {
                    "system": self.system_prompts["analytics"],
                    "task": """Analyze campaign performance data and optimize media mix for future campaigns.

PERFORMANCE DATA:
{performance_data}

PLATFORM PERFORMANCE:
{platform_performance}

CONTENT TYPE PERFORMANCE:
{content_type_performance}

REQUIREMENTS:
- Analyze engagement rates by content type
- Identify top performing content formats
- Recommend optimal content mix based on data
- Provide actionable optimization insights
- Consider platform-specific performance

Return valid JSON with the following structure:
{{
  "performance_analysis": {{
    "video_engagement_rate": 0,
    "image_engagement_rate": 0,
    "text_engagement_rate": 0,
    "carousel_engagement_rate": 0,
    "story_engagement_rate": 0
  }},
  "recommended_mix": {{
    "video": 40,
    "image": 30,
    "carousel": 20,
    "text": 10,
    "story": 0
  }},
  "optimization_insights": [
    {{
      "insight": "string",
      "impact": "high|medium|low",
      "action": "string",
      "expected_improvement": "string"
    }}
  ],
  "platform_recommendations": {{
    "instagram": {{"content_types": ["video", "carousel"], "posting_frequency": "2x daily"}},
    "linkedin": {{"content_types": ["text", "image"], "posting_frequency": "1x daily"}},
    "email": {{"content_types": ["text"], "sending_frequency": "2x weekly"}},
    "sms": {{"content_types": ["text"], "sending_frequency": "1x weekly"}}
  }}
}}""",
                    "variables": ["performance_data", "platform_performance", "content_type_performance"]
                }
            },
            "content": {
                "text_generator": {
                    "system": self.system_prompts["content"],
                    "task": """Generate engaging social media content for {platform}.

BUSINESS CONTEXT:
Business: {business_name}
Industry: {industry}
Brand Voice: {brand_voice}
Target Audience: {target_audience}

CONTENT REQUIREMENTS:
Topic: {content_topic}
Platform: {platform}
Tone: {tone}
Length: {length}

PLATFORM-SPECIFIC GUIDELINES:
{platform_guidelines}

REQUIREMENTS:
- Create compelling headline and body copy
- Include clear call-to-action
- Generate relevant hashtags (if applicable)
- Match brand voice and tone
- Optimize for platform best practices
- Limit to {character_limit} characters

Return valid JSON with the following structure:
{{
  "content_type": "text",
  "platform": "{platform}",
  "headline": "string",
  "body": "string",
  "cta": "string",
  "hashtags": ["string"],
  "emojis": ["string"],
  "predicted_engagement_score": 0,
  "tone_analysis": "string",
  "character_count": 0,
  "optimization_notes": ["string"],
  "alternative_versions": [
    {{
      "version": "string",
      "body": "string",
      "use_case": "string"
    }}
  ]
}}""",
                    "variables": ["business_name", "industry", "brand_voice", "target_audience", "content_topic", "platform", "tone", "length", "platform_guidelines", "character_limit"]
                },
                "visual_generator": {
                    "system": self.system_prompts["content"],
                    "task": """Create visual content concept for {platform}.

BUSINESS CONTEXT:
Business: {business_name}
Industry: {industry}
Brand Colors: {brand_colors}
Brand Guidelines: {brand_guidelines}
Target Audience: {target_audience}

VISUAL REQUIREMENTS:
Topic: {visual_topic}
Platform: {platform}
Visual Style: {visual_style}

REQUIREMENTS:
- Create compelling headline and subheading
- Define color scheme using brand colors
- Provide detailed image generation prompt for DALL-E
- Specify design direction and mood
- Include CTA placement recommendation
- Ensure brand consistency

Return valid JSON with the following structure:
{{
  "content_type": "visual",
  "platform": "{platform}",
  "headline_text": "string",
  "subheading": "string",
  "design_direction": {{
    "color_scheme": ["string"],
    "visual_style": "string",
    "mood": "string",
    "composition": "string",
    "typography": "string"
  }},
  "image_generation_prompt": "string",
  "cta_placement": "string",
  "brand_elements": ["string"],
  "predicted_engagement_score": 0,
  "layout_suggestions": {{
    "primary_focus": "string",
    "text_placement": "string",
    "visual_hierarchy": "string"
  }},
  "alternative_concepts": [
    {{
      "concept": "string",
      "description": "string",
      "use_case": "string"
    }}
  ]
}}""",
                    "variables": ["business_name", "industry", "brand_colors", "brand_guidelines", "target_audience", "visual_topic", "platform", "visual_style"]
                },
                "video_script_generator": {
                    "system": self.system_prompts["content"],
                    "task": """Create an engaging {duration_seconds}-second video script for {platform}.

BUSINESS CONTEXT:
Business: {business_name}
Industry: {industry}
Brand Voice: {brand_voice}
Target Audience: {target_audience}

VIDEO REQUIREMENTS:
Topic: {video_topic}
Platform: {platform}
Duration: {duration_seconds} seconds
Script Style: {script_style}

REQUIREMENTS:
- Structure: Hook (5s) → Body (20s) → CTA (5s)
- Include voiceover script for each section
- Provide visual cues and scene descriptions
- Add caption text for accessibility
- Include hashtag recommendations
- Ensure platform-optimized formatting

Return valid JSON with the following structure:
{{
  "content_type": "video",
  "platform": "{platform}",
  "duration_seconds": {duration_seconds},
  "script": {{
    "hook": {{
      "text": "string",
      "duration": 5,
      "visual_cue": "string",
      "audio_note": "string"
    }},
    "body": {{
      "text": "string",
      "duration": 20,
      "visual_cues": ["string"],
      "key_points": ["string"],
      "transitions": ["string"]
    }},
    "cta": {{
      "text": "string",
      "duration": 5,
      "visual_cue": "string",
      "action": "string"
    }}
  }},
  "caption": "string",
  "hashtags": ["string"],
  "predicted_engagement_score": 0,
  "production_notes": "string",
  "music_suggestions": ["string"],
  "shot_list": [
    {{
      "shot_number": 1,
      "description": "string",
      "duration": 0,
      "camera_angle": "string"
    }}
  ]
}}""",
                    "variables": ["business_name", "industry", "brand_voice", "target_audience", "video_topic", "platform", "duration_seconds", "script_style"]
                }
            },
            "analytics": {
                "performance_analyzer": {
                    "system": self.system_prompts["analytics"],
                    "task": """Analyze campaign performance data and provide actionable insights.

PERFORMANCE DATA:
{performance_data}

PLATFORM PERFORMANCE:
{platform_performance}

CONTENT TYPE PERFORMANCE:
{content_type_performance}

TIME PERIOD:
{time_period}

CAMPAIGN GOALS:
{campaign_goals}

REQUIREMENTS:
- Calculate overall performance score
- Identify top performing content types
- Highlight weak segments with specific issues
- Provide data-driven optimization opportunities
- Recommend priority actions based on impact vs effort
- Compare performance against campaign goals

Return valid JSON with the following structure:
{{
  "performance_summary": {{
    "overall_score": 0,
    "engagement_rate": 0,
    "conversion_rate": 0,
    "reach": 0,
    "impressions": 0,
    "goal_achievement": 0
  }},
  "top_performing_content": [
    {{
      "type": "string",
      "engagement_score": 0,
      "key_factors": ["string"],
      "sample_content_id": "string"
    }}
  ],
  "weak_segments": [
    {{
      "area": "string",
      "current_performance": 0,
      "issues": ["string"],
      "recommendations": ["string"],
      "priority": "high|medium|low"
    }}
  ],
  "optimization_opportunities": [
    {{
      "opportunity": "string",
      "potential_impact": "high|medium|low",
      "effort_required": "high|medium|low",
      "implementation_steps": ["string"],
      "expected_improvement": "string"
    }}
  ],
  "trend_analysis": {{
    "engagement_trend": "increasing|stable|decreasing",
    "best_posting_times": ["string"],
    "audience_growth_rate": 0,
    "content_saturation": "low|medium|high"
  }},
  "competitive_insights": {{
    "industry_benchmark_comparison": "above|at|below",
    "unique_strengths": ["string"],
    "improvement_areas": ["string"]
  }}
}}""",
                    "variables": ["performance_data", "platform_performance", "content_type_performance", "time_period", "campaign_goals"]
                }
            },
            "messaging": {
                "customer_reply": {
                    "system": self.system_prompts["messaging"],
                    "task": """Generate a professional and helpful response to a customer inquiry.

BUSINESS CONTEXT:
Business: {business_name}
Brand Voice: {brand_voice}
Industry: {industry}

CUSTOMER MESSAGE:
{customer_message}

CONVERSATION HISTORY:
{conversation_history}

PLATFORM:
{platform}

CUSTOMER PROFILE:
{customer_profile}

REQUIREMENTS:
- Respond with appropriate brand voice
- Address customer concerns professionally
- Stay within brand guidelines and policies
- Determine if escalation is needed
- Identify required follow-up actions
- Maintain positive customer sentiment

CONSTRAINTS:
- Never provide medical advice
- Never guarantee business growth or returns
- Avoid controversial topics
- Do not promise discounts unless authorized
- If unsure, recommend escalation

Return valid JSON with the following structure:
{{
  "response_type": "customer_reply",
  "platform": "{platform}",
  "reply_text": "string",
  "tone": "professional|friendly|empathetic|apologetic",
  "escalation_needed": false,
  "escalation_reason": "string",
  "follow_up_required": false,
  "follow_up_action": "string",
  "sentiment": "positive|neutral|negative",
  "confidence_score": 0,
  "next_action": "string",
  "suggested_tags": ["string"],
  "internal_notes": "string",
  "alternative_responses": [
    {{
      "tone": "string",
      "text": "string",
      "use_case": "string"
    }}
  ]
}}""",
                    "variables": ["business_name", "brand_voice", "industry", "customer_message", "conversation_history", "platform", "customer_profile"]
                }
            }
        }
    
    def build_prompt(
        self, 
        service_type: str, 
        template_name: str, 
        variables: Dict[str, Any]
    ) -> str:
        """Build a complete prompt with system prompt, context, and task"""
        try:
            # Get template
            template = self.prompt_templates.get(service_type, {}).get(template_name)
            if not template:
                raise ValueError(f"Template not found: {service_type}.{template_name}")
            
            # Get system prompt
            system_prompt = template["system"]
            
            # Get task template
            task_template = template["task"]
            
            # Inject variables into task template
            task_prompt = self._inject_variables(task_template, variables, template.get("variables", []))
            
            # Combine system prompt and task prompt
            full_prompt = f"{system_prompt}\n\n{task_prompt}"
            
            return full_prompt
            
        except Exception as e:
            raise ValueError(f"Failed to build prompt: {str(e)}")
    
    def _inject_variables(
        self, 
        template: str, 
        variables: Dict[str, Any], 
        allowed_variables: List[str]
    ) -> str:
        """Inject variables into prompt template"""
        try:
            # Format context for injection
            context = self._format_context(variables, allowed_variables)
            
            # Replace variables in template
            formatted_prompt = template.format(**context)
            
            return formatted_prompt
            
        except KeyError as e:
            raise ValueError(f"Missing variable in template: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to inject variables: {str(e)}")
    
    def _format_context(self, variables: Dict[str, Any], allowed_variables: List[str]) -> Dict[str, Any]:
        """Format variables for prompt injection with intelligent defaults"""
        context = {}
        
        # Default values for common variables
        defaults = {
            "business_name": "Your Business",
            "industry": "General",
            "brand_voice": "Professional and friendly",
            "target_audience": "General audience",
            "campaign_goal": "Increase engagement",
            "duration_days": "30",
            "platforms": "Instagram, LinkedIn",
            "content_types": "posts, reels, stories",
            "platform": "instagram",
            "tone": "engaging",
            "length": "medium",
            "character_limit": "150",
            "platform_guidelines": "Platform best practices apply",
            "brand_colors": "Brand colors",
            "brand_guidelines": "Follow brand guidelines",
            "visual_style": "modern and clean",
            "visual_topic": "promotional content",
            "content_topic": "general marketing content",
            "duration_seconds": "30",
            "script_style": "conversational",
            "video_topic": "promotional video",
            "performance_data": "{}",
            "platform_performance": "{}",
            "content_type_performance": "{}",
            "time_period": "last 30 days",
            "campaign_goals": "engagement and growth",
            "customer_message": "",
            "conversation_history": "No previous messages",
            "customer_profile": "{}"
        }
        
        for var in allowed_variables:
            if var in variables and variables[var] is not None:
                # Convert complex objects to JSON strings
                if isinstance(variables[var], (dict, list)):
                    context[var] = json.dumps(variables[var], indent=2)
                else:
                    context[var] = str(variables[var])
            else:
                # Use default value
                context[var] = defaults.get(var, f"[{var.upper()}_NOT_PROVIDED]")
        
        return context
    
    def build_strategy_prompt(self, variables: Dict[str, Any]) -> str:
        """Build strategy generation prompt"""
        return self.build_prompt("strategy", "campaign_calendar", variables)
    
    def build_content_prompt(self, content_type: str, variables: Dict[str, Any]) -> str:
        """Build content generation prompt"""
        return self.build_prompt("content", f"{content_type}_generator", variables)
    
    def build_analytics_prompt(self, variables: Dict[str, Any]) -> str:
        """Build analytics prompt"""
        return self.build_prompt("analytics", "performance_analyzer", variables)
    
    def build_messaging_prompt(self, variables: Dict[str, Any]) -> str:
        """Build messaging prompt"""
        return self.build_prompt("messaging", "customer_reply", variables)
    
    def add_context_block(self, prompt: str, context: Dict[str, Any]) -> str:
        """Add context block to prompt"""
        context_lines = []
        
        if "business_context" in context:
            business = context["business_context"]
            context_lines.extend([
                "BUSINESS CONTEXT:",
                f"Business Name: {business.get('name', 'Unknown')}",
                f"Industry: {business.get('industry', 'Unknown')}",
                f"Brand Voice: {business.get('brand_voice', 'Professional')}",
                f"Target Audience: {business.get('target_audience', {})}",
                f"Primary Goals: {business.get('primary_goals', [])}",
                ""
            ])
        
        if "campaign_context" in context:
            campaign = context["campaign_context"]
            context_lines.extend([
                "CAMPAIGN CONTEXT:",
                f"Campaign Name: {campaign.get('name', 'Unknown')}",
                f"Duration: {campaign.get('duration_days', 30)} days",
                f"Status: {campaign.get('status', 'Unknown')}",
                f"Primary Goal: {campaign.get('primary_goal', 'Unknown')}",
                f"Start Date: {campaign.get('start_date', 'Unknown')}",
                ""
            ])
        
        if "performance_data" in context:
            performance = context["performance_data"]
            context_lines.extend([
                "PERFORMANCE DATA:",
                f"Recent Metrics: {performance.get('recent_metrics', {})}",
                f"Top Performing Content: {performance.get('top_performing', [])}",
                f"Platform Performance: {performance.get('platform_performance', {})}",
                ""
            ])
        
        if "conversation_context" in context:
            conversation = context["conversation_context"]
            context_lines.extend([
                "CONVERSATION CONTEXT:",
                f"Last Messages: {conversation.get('last_messages', [])}",
                f"Customer Sentiment: {conversation.get('sentiment', 'neutral')}",
                f"Customer Profile: {conversation.get('customer_profile', {})}",
                ""
            ])
        
        # Add context block to prompt
        if context_lines:
            context_block = "\n".join(context_lines)
            return f"{prompt}\n\n{context_block}"
        
        return prompt
    
    def add_constraints(self, prompt: str, constraints: List[str]) -> str:
        """Add constraints to prompt"""
        if constraints:
            constraint_text = "\n".join([f"- {constraint}" for constraint in constraints])
            return f"{prompt}\n\nCONSTRAINTS:\n{constraint_text}"
        return prompt
    
    def add_json_schema(self, prompt: str, schema: Dict[str, Any]) -> str:
        """Add JSON schema requirements to prompt"""
        schema_text = json.dumps(schema, indent=2)
        return f"{prompt}\n\nJSON SCHEMA:\n{schema_text}\n\nIMPORTANT: Return valid JSON that matches the schema exactly."
    
    def add_brand_voice(self, prompt: str, brand_voice: str) -> str:
        """Add brand voice instructions to prompt"""
        return f"{prompt}\n\nBRAND VOICE: {brand_voice}"
    
    def add_tone_instructions(self, prompt: str, tone: str) -> str:
        """Add tone instructions to prompt"""
        return f"{prompt}\n\nTONE: {tone}"
    
    def add_length_instructions(self, prompt: str, length: str) -> str:
        """Add length instructions to prompt"""
        length_guidelines = {
            "short": "Keep the response concise and to the point (under 100 words)",
            "medium": "Provide a balanced response (100-300 words)",
            "long": "Provide a comprehensive response (300-500 words)"
        }
        return f"{prompt}\n\nLENGTH: {length_guidelines.get(length, length_guidelines['medium'])}"
    
    def add_platform_specifics(self, prompt: str, platform: str) -> str:
        """Add platform-specific instructions to prompt"""
        platform_guidelines = {
            "instagram": "Focus on visual content, hashtags, and engaging captions. Use emojis appropriately.",
            "linkedin": "Focus on professional tone, industry insights, and business value. Use formal language.",
            "email": "Focus on clear subject lines, personalization, and call-to-action. Use professional formatting.",
            "sms": "Focus on concise messages, clear calls-to-action, and urgent tone. Keep under 160 characters."
        }
        return f"{prompt}\n\nPLATFORM SPECIFICS: {platform_guidelines.get(platform, 'General content guidelines.')}"
    
    def get_prompt_template_info(self, service_type: str, template_name: str) -> Dict[str, Any]:
        """Get information about a prompt template"""
        template = self.prompt_templates.get(service_type, {}).get(template_name)
        if not template:
            return {}
        
        return {
            "service_type": service_type,
            "template_name": template_name,
            "system_prompt": template["system"],
            "task_template": template["task"],
            "variables": template.get("variables", [])
        }
    
    def list_available_templates(self, service_type: Optional[str] = None) -> Dict[str, List[str]]:
        """List available prompt templates"""
        if service_type:
            return {
                service_type: list(self.prompt_templates.get(service_type, {}).keys())
            }
        
        return {
            service: list(templates.keys()) for service, templates in self.prompt_templates.items()
        }

# Global prompt builder instance
prompt_builder = PromptBuilder()
