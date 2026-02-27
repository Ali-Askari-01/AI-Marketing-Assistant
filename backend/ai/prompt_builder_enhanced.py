"""
AI Prompt Builder Module
Implements the 4-layer prompt architecture with context injection and structured output enforcement
Designed according to AI Prompt Architecture Design specifications
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from models.mongodb_models import Business, Campaign, Content, Platform, ContentType
import json

class PromptBuilder:
    """Advanced prompt builder with context injection and structured templates"""
    
    def __init__(self):
        self.system_prompts = {
            "strategy": self._get_strategy_system_prompt(),
            "content": self._get_content_system_prompt(),
            "video": self._get_video_system_prompt(),
            "analytics": self._get_analytics_system_prompt(),
            "messaging": self._get_messaging_system_prompt()
        }
        
        # Output schemas for validation
        self.output_schemas = {
            "campaign_calendar": self._get_campaign_calendar_schema(),
            "content_generation": self._get_content_generation_schema(),
            "video_script": self._get_video_script_schema(),
            "analytics_insights": self._get_analytics_insights_schema(),
            "message_reply": self._get_message_reply_schema()
        }
    
    # === LAYER 1: SYSTEM PROMPTS (ROLE DEFINITION) ===
    
    def _get_strategy_system_prompt(self) -> str:
        return """
You are a senior marketing strategist with 15 years of experience in digital marketing, 
campaign planning, and growth analytics. You produce structured, actionable marketing strategies 
based on business context and industry best practices.

Always respond in strict JSON format matching the provided schema.
Focus on ROI-driven recommendations and measurable outcomes.
Consider platform-specific content requirements and audience behavior patterns.
"""
    
    def _get_content_system_prompt(self) -> str:
        return """
You are an expert content creator and copywriter specializing in social media marketing.
You create engaging, platform-optimized content that drives engagement and conversions.

Always respond in strict JSON format.
Ensure content aligns with brand voice and campaign objectives.
Optimize for platform-specific algorithms and user behavior.
Include relevant hashtags and calls-to-action.
"""
    
    def _get_video_system_prompt(self) -> str:
        return """
You are a professional video content strategist and scriptwriter.
You create compelling video scripts optimized for short-form social media content.

Always respond in strict JSON format.
Structure scripts with strong hooks, engaging body content, and clear CTAs.
Consider visual storytelling and platform-specific video requirements.
"""
    
    def _get_analytics_system_prompt(self) -> str:
        return """
You are a data analyst specializing in marketing performance analytics.
You provide actionable insights based on campaign data and performance metrics.

Always respond in strict JSON format.
Focus on trends, opportunities, and specific recommendations for improvement.
Base insights on statistical significance and industry benchmarks.
"""
    
    def _get_messaging_system_prompt(self) -> str:
        return """
You are a professional customer service representative and brand voice specialist.
You create helpful, brand-aligned responses to customer messages.

Always respond in strict JSON format.
Maintain business professionalism while being helpful and personable.
Never promise discounts or make commitments without authorization.
Escalate complex issues appropriately.
"""
    
    # === LAYER 2: CONTEXT INJECTION ===
    
    def _build_business_context(self, business: Business) -> str:
        """Build business context for AI prompts"""
        context = f"""
BUSINESS CONTEXT:
Business Name: {business.profile.name}
Industry: {business.profile.industry}
Description: {business.profile.description or 'Not provided'}
Target Audience: {business.profile.target_audience or 'General audience'}
Brand Voice: {business.profile.brand_voice or 'Professional'}
Website: {business.profile.website or 'Not provided'}

SOCIAL MEDIA PRESENCE:
Instagram: {business.social_accounts.instagram_handle or 'Not connected'}
LinkedIn: {business.social_accounts.linkedin_page or 'Not connected'}
Twitter: {business.social_accounts.twitter_handle or 'Not connected'}
TikTok: {business.social_accounts.tiktok_handle or 'Not connected'}
YouTube: {business.social_accounts.youtube_channel or 'Not connected'}

AI PREFERENCES:
{json.dumps(business.ai_preferences, indent=2) if business.ai_preferences else 'Default settings'}
"""
        return context
    
    def _build_campaign_context(self, campaign: Campaign) -> str:
        """Build campaign context for AI prompts"""
        context = f"""
CAMPAIGN CONTEXT:
Campaign Name: {campaign.name}
Description: {campaign.description or 'Not provided'}
Status: {campaign.status}
Platforms: {', '.join(campaign.platforms)}
Start Date: {campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else 'Not set'}
End Date: {campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else 'Not set'}
Total Posts: {campaign.total_posts}
Published Posts: {campaign.published_posts}

TARGET METRICS:
Target Reach: {campaign.target_reach or 'Not set'}
Target Engagement: {campaign.target_engagement or 'Not set'}%
Budget: ${campaign.budget or 'Not set'}

AI STRATEGY:
{json.dumps(campaign.ai_strategy, indent=2) if campaign.ai_strategy else 'Not generated yet'}
"""
        return context
    
    def _get_performance_context(self, content_list: List[Content]) -> str:
        """Build performance context from past content"""
        if not content_list:
            return "PERFORMANCE CONTEXT:\nNo past performance data available."
        
        # Calculate basic performance metrics
        total_content = len(content_list)
        platform_breakdown = {}
        type_breakdown = {}
        avg_performance = {}
        
        for content in content_list:
            # Platform breakdown
            platform = content.platform
            platform_breakdown[platform] = platform_breakdown.get(platform, 0) + 1
            
            # Type breakdown  
            content_type = content.content_type
            type_breakdown[content_type] = type_breakdown.get(content_type, 0) + 1
            
            # Performance data (if available)
            if content.performance:
                for metric in ['views', 'likes', 'comments', 'shares']:
                    if hasattr(content.performance, metric):
                        value = getattr(content.performance, metric)
                        if metric not in avg_performance:
                            avg_performance[metric] = []
                        avg_performance[metric].append(value)
        
        # Calculate averages
        for metric, values in avg_performance.items():
            avg_performance[metric] = sum(values) / len(values) if values else 0
        
        context = f"""
PERFORMANCE CONTEXT:
Total Content Pieces: {total_content}

Platform Distribution:
{json.dumps(platform_breakdown, indent=2)}

Content Type Distribution:
{json.dumps(type_breakdown, indent=2)}

Average Performance Metrics:
{json.dumps(avg_performance, indent=2)}
"""
        return context
    
    # === LAYER 3: TASK-SPECIFIC PROMPT BUILDERS ===
    
    def build_strategy_prompt(self, business: Business, campaign_goal: str, duration_days: int = 30, platforms: List[str] = None) -> Dict[str, Any]:
        """Build campaign strategy generation prompt"""
        business_context = self._build_business_context(business)
        platforms = platforms or ["instagram", "linkedin"] 
        
        task_prompt = f"""
TASK: Generate a comprehensive {duration_days}-day marketing campaign strategy.

CAMPAIGN REQUIREMENTS:
Goal: {campaign_goal}
Duration: {duration_days} days
Platforms: {', '.join(platforms)}

Please create a detailed campaign calendar that includes:
1. Weekly themes and messaging strategies
2. Daily content recommendations with specific types
3. Platform-specific posting schedules
4. KPI targets and success metrics
5. Content mix recommendations (video, image, text ratios)

{business_context}

IMPORTANT: Return a valid JSON response matching the campaign_calendar schema.
Focus on actionable, measurable recommendations that align with the business context.
"""
        
        return {
            "system_prompt": self.system_prompts["strategy"],
            "user_prompt": task_prompt,
            "schema_type": "campaign_calendar",
            "temperature": 0.3,
            "max_tokens": 2000
        }
    
    def build_content_prompt(self, business: Business, campaign: Campaign, content_type: str, platform: str, theme: str = None) -> Dict[str, Any]:
        """Build content generation prompt"""
        business_context = self._build_business_context(business)
        campaign_context = self._build_campaign_context(campaign)
        
        platform_specs = {
            "instagram": "Instagram post (max 2,200 characters, include 5-10 relevant hashtags)",
            "linkedin": "LinkedIn post (max 3,000 characters, professional tone, include 2-5 hashtags)",
            "twitter": "Twitter post (max 280 characters, include 1-3 hashtags)",
            "tiktok": "TikTok caption (engaging, trendy, include 3-7 hashtags)",
            "youtube": "YouTube description (detailed, SEO-optimized, include relevant tags)"
        }
        
        content_type_specs = {
            "post": "Regular social media post with caption",
            "story": "Story content (engaging, time-sensitive)",
            "reel": "Short-form video content with high engagement potential",
            "carousel": "Multi-slide content with educational or storytelling value",
            "video": "Video content with script and visual descriptions"
        }
        
        task_prompt = f"""
TASK: Generate {content_type_specs.get(content_type, content_type)} for {platform_specs.get(platform, platform)}.

CONTENT REQUIREMENTS:
Platform: {platform.title()}
Content Type: {content_type_specs.get(content_type, content_type)}
Theme: {theme or 'Aligned with campaign goals'}

{business_context}

{campaign_context}

Please create content that:
1. Matches the brand voice and personality
2. Aligns with the campaign goals and theme
3. Is optimized for the specific platform
4. Includes appropriate calls-to-action
5. Incorporates relevant hashtags
6. Has high engagement potential

IMPORTANT: Return a valid JSON response matching the content_generation schema.
Include title, main content, hashtags, CTA, and platform-specific optimizations.
"""
        
        return {
            "system_prompt": self.system_prompts["content"],
            "user_prompt": task_prompt,
            "schema_type": "content_generation",
            "temperature": 0.7,
            "max_tokens": 1500
        }
    
    def build_video_script_prompt(self, business: Business, campaign: Campaign, video_type: str = "reel", duration: int = 30) -> Dict[str, Any]:
        """Build video script generation prompt"""
        business_context = self._build_business_context(business)
        campaign_context = self._build_campaign_context(campaign)
        
        video_structures = {
            15: "Hook (3s) → Value (9s) → CTA (3s)",
            30: "Hook (5s) → Body (20s) → CTA (5s)",
            60: "Hook (8s) → Problem (15s) → Solution (25s) → CTA (12s)"
        }
        
        structure = video_structures.get(duration, video_structures[30])
        
        task_prompt = f"""
TASK: Create a {duration}-second {video_type} script for social media.

VIDEO REQUIREMENTS:
Duration: {duration} seconds
Structure: {structure}
Style: Engaging, authentic, brand-aligned

{business_context}

{campaign_context}

Please create a video script that includes:
1. Compelling hook to grab attention immediately
2. Valuable content that delivers on the hook promise
3. Clear call-to-action
4. Scene-by-scene visual descriptions
5. Voiceover/caption text
6. Engagement elements (questions, challenges, etc.)

IMPORTANT: Return a valid JSON response matching the video_script schema.
Make it platform-optimized and highly engaging.
"""
        
        return {
            "system_prompt": self.system_prompts["video"],
            "user_prompt": task_prompt,
            "schema_type": "video_script",
            "temperature": 0.6,
            "max_tokens": 1200
        }
    
    def build_analytics_prompt(self, business: Business, campaign: Campaign, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build analytics insights generation prompt"""
        business_context = self._build_business_context(business)
        campaign_context = self._build_campaign_context(campaign)
        
        task_prompt = f"""
TASK: Analyze campaign performance data and provide actionable insights.

PERFORMANCE DATA:
{json.dumps(performance_data, indent=2)}

{business_context}

{campaign_context}

Please analyze the data and provide:
1. Key performance highlights
2. Areas of concern or underperformance
3. Specific recommendations for improvement
4. Content type and platform optimization suggestions
5. Audience engagement insights
6. Projected improvements with recommended changes

IMPORTANT: Return a valid JSON response matching the analytics_insights schema.
Focus on actionable, data-driven recommendations.
"""
        
        return {
            "system_prompt": self.system_prompts["analytics"],
            "user_prompt": task_prompt,
            "schema_type": "analytics_insights",
            "temperature": 0.2,
            "max_tokens": 1500
        }
    
    def build_messaging_prompt(self, business: Business, customer_message: str, context_messages: List[Dict] = None) -> Dict[str, Any]:
        """Build customer message reply prompt"""
        business_context = self._build_business_context(business)
        
        context_str = ""
        if context_messages:
            context_str = "CONVERSATION HISTORY:\n"
            for msg in context_messages[-3:]:  # Last 3 messages for context
                context_str += f"Customer: {msg.get('customer_message', '')}\n"
                context_str += f"Response: {msg.get('response', '')}\n\n"
        
        task_prompt = f"""
TASK: Generate a professional, helpful response to a customer message.

CUSTOMER MESSAGE:
"{customer_message}"

{context_str}

{business_context}

Guidelines for response:
1. Be helpful and professional
2. Maintain the brand voice
3. Address the customer's concern directly
4. Do not promise discounts or make unauthorized commitments
5. Escalate to human agent if necessary
6. Keep response concise but complete
7. Include next steps if applicable

IMPORTANT: Return a valid JSON response matching the message_reply schema.
"""
        
        return {
            "system_prompt": self.system_prompts["messaging"],
            "user_prompt": task_prompt,
            "schema_type": "message_reply", 
            "temperature": 0.4,
            "max_tokens": 800
        }
    
    # === LAYER 4: OUTPUT SCHEMA DEFINITIONS ===
    
    def _get_campaign_calendar_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "campaign_overview": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "duration_days": {"type": "integer"},
                        "primary_goal": {"type": "string"},
                        "target_platforms": {"type": "array", "items": {"type": "string"}},
                        "estimated_reach": {"type": "integer"},
                        "estimated_engagement_rate": {"type": "number"}
                    },
                    "required": ["name", "duration_days", "primary_goal", "target_platforms"]
                },
                "weekly_themes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "week": {"type": "integer"},
                            "theme": {"type": "string"},
                            "focus": {"type": "string"},
                            "key_message": {"type": "string"},
                            "content_goals": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["week", "theme", "focus", "key_message"]
                    }
                },
                "daily_calendar": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "date": {"type": "string"},
                            "theme": {"type": "string"},
                            "platform": {"type": "string"},
                            "content_type": {"type": "string"},
                            "content_focus": {"type": "string"},
                            "suggested_timing": {"type": "string"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"]}
                        },
                        "required": ["day", "theme", "platform", "content_type"]
                    }
                },
                "kpis": {
                    "type": "object",
                    "properties": {
                        "primary_metrics": {"type": "array", "items": {"type": "string"}},
                        "target_reach": {"type": "integer"},
                        "target_engagement_rate": {"type": "number"},
                        "target_conversions": {"type": "integer"},
                        "measurement_frequency": {"type": "string"}
                    }
                },
                "content_mix": {
                    "type": "object",
                    "properties": {
                        "video_percentage": {"type": "integer"},
                        "image_percentage": {"type": "integer"},
                        "text_percentage": {"type": "integer"},
                        "carousel_percentage": {"type": "integer"}
                    }
                }
            },
            "required": ["campaign_overview", "weekly_themes", "daily_calendar", "kpis"]
        }
    
    def _get_content_generation_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "main_text": {"type": "string"},
                        "caption": {"type": "string"},
                        "platform": {"type": "string"},
                        "content_type": {"type": "string"},
                        "tone": {"type": "string"},
                        "word_count": {"type": "integer"}
                    },
                    "required": ["title", "main_text", "platform", "content_type"]
                },
                "hashtags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "maxItems": 10
                },
                "call_to_action": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "type": {"type": "string"},
                        "urgency": {"type": "string", "enum": ["low", "medium", "high"]}
                    },
                    "required": ["text", "type"]
                },
                "visual_suggestions": {
                    "type": "object",
                    "properties": {
                        "image_description": {"type": "string"},
                        "color_scheme": {"type": "array", "items": {"type": "string"}},
                        "style_notes": {"type": "string"},
                        "text_overlay": {"type": "string"}
                    }
                },
                "engagement_factors": {
                    "type": "object",
                    "properties": {
                        "hook_strength": {"type": "integer", "minimum": 1, "maximum": 10},
                        "value_delivery": {"type": "integer", "minimum": 1, "maximum": 10},
                        "shareability": {"type": "integer", "minimum": 1, "maximum": 10},
                        "predicted_engagement_rate": {"type": "number"}
                    }
                },
                "optimization_notes": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["content", "hashtags", "call_to_action"]
        }
    
    def _get_video_script_schema(self) -> Dict[str, Any]:
        return {
            "type": "object", 
            "properties": {
                "video_overview": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "duration_seconds": {"type": "integer"},
                        "style": {"type": "string"},
                        "primary_goal": {"type": "string"},
                        "target_emotion": {"type": "string"}
                    },
                    "required": ["title", "duration_seconds", "style"]
                },
                "script_segments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "segment": {"type": "string", "enum": ["hook", "body", "cta"]},
                            "start_time": {"type": "integer"},
                            "end_time": {"type": "integer"},
                            "voiceover": {"type": "string"},
                            "visual_description": {"type": "string"},
                            "text_overlay": {"type": "string"},
                            "notes": {"type": "string"}
                        },
                        "required": ["segment", "start_time", "end_time", "voiceover", "visual_description"]
                    }
                },
                "production_notes": {
                    "type": "object",
                    "properties": {
                        "equipment_needed": {"type": "array", "items": {"type": "string"}},
                        "location_requirements": {"type": "string"},
                        "lighting_setup": {"type": "string"},
                        "editing_notes": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "hashtags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "maxItems": 10
                },
                "caption_text": {"type": "string"},
                "engagement_hooks": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "success_metrics": {
                    "type": "object",
                    "properties": {
                        "target_completion_rate": {"type": "number"},
                        "target_shares": {"type": "integer"},
                        "target_comments": {"type": "integer"},
                        "virality_potential": {"type": "string", "enum": ["low", "medium", "high"]}
                    }
                }
            },
            "required": ["video_overview", "script_segments", "hashtags", "caption_text"]
        }
    
    def _get_analytics_insights_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "performance_summary": {
                    "type": "object",
                    "properties": {
                        "overall_score": {"type": "integer", "minimum": 0, "maximum": 100},
                        "trend_direction": {"type": "string", "enum": ["improving", "declining", "stable"]},
                        "key_achievements": {"type": "array", "items": {"type": "string"}},
                        "primary_concerns": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["overall_score", "trend_direction"]
                },
                "platform_insights": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "platform": {"type": "string"},
                            "performance_rating": {"type": "string", "enum": ["excellent", "good", "average", "poor"]},
                            "best_performing_content": {"type": "string"},
                            "engagement_rate": {"type": "number"},
                            "reach_performance": {"type": "string"},
                            "recommendations": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["platform", "performance_rating", "recommendations"]
                    }
                },
                "content_analysis": {
                    "type": "object",
                    "properties": {
                        "top_performing_types": {"type": "array", "items": {"type": "string"}},
                        "underperforming_types": {"type": "array", "items": {"type": "string"}},
                        "optimal_posting_times": {"type": "object"},
                        "content_fatigue_signals": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "audience_insights": {
                    "type": "object",
                    "properties": {
                        "engagement_patterns": {"type": "array", "items": {"type": "string"}},
                        "demographic_performance": {"type": "object"},
                        "interest_alignment": {"type": "string"},
                        "growth_opportunities": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "actionable_recommendations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "recommendation": {"type": "string"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                            "expected_impact": {"type": "string"},
                            "implementation_difficulty": {"type": "string", "enum": ["easy", "moderate", "difficult"]},
                            "timeline": {"type": "string"}
                        },
                        "required": ["recommendation", "priority", "expected_impact"]
                    }
                },
                "forecast": {
                    "type": "object",
                    "properties": {
                        "next_30_days": {"type": "string"},
                        "growth_projection": {"type": "number"},
                        "risk_factors": {"type": "array", "items": {"type": "string"}},
                        "confidence_level": {"type": "string", "enum": ["high", "medium", "low"]}
                    }
                }
            },
            "required": ["performance_summary", "platform_insights", "actionable_recommendations"]
        }
    
    def _get_message_reply_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "response": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "tone": {"type": "string"},
                        "intent_addressed": {"type": "string"},
                        "word_count": {"type": "integer"}
                    },
                    "required": ["message", "tone", "intent_addressed"]
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "customer_intent": {"type": "string"},
                        "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
                        "urgency": {"type": "string", "enum": ["low", "medium", "high"]},
                        "category": {"type": "string"},
                        "escalation_needed": {"type": "boolean"}
                    },
                    "required": ["customer_intent", "sentiment", "urgency", "escalation_needed"]
                },
                "suggested_actions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                            "department": {"type": "string"}
                        },
                        "required": ["action", "priority"]
                    }
                },
                "alternatives": {
                    "type": "array",
                    "items": {"type": "string"},
                    "maxItems": 3
                },
                "follow_up": {
                    "type": "object",
                    "properties": {
                        "recommended": {"type": "boolean"},
                        "timeline": {"type": "string"},
                        "method": {"type": "string"}
                    }
                }
            },
            "required": ["response", "analysis"]
        }

# Global prompt builder instance
prompt_builder = PromptBuilder()