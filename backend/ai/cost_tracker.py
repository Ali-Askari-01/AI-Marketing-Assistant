"""
Enhanced Cost Tracker Module
Comprehensive AI service usage and cost tracking with budget management and analytics
Designed according to AI Service Layer specifications
"""

from typing import Dict, Any, Optional, List, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import json
import logging

from core.config import settings
from core.errors import RateLimitError

logger = logging.getLogger(__name__)

# Define missing error class
class BudgetExceededError(Exception):
    """Budget exceeded error"""
    pass

# Define AIResponse locally since it's not in ai_client
@dataclass
class AIResponse:
    """AI response structure for cost tracking"""
    model: str
    input_tokens: int
    output_tokens: int
    tokens_used: int

class SubscriptionTier(str, Enum):
    """Subscription tier levels"""
    FREE = "free"
    PRO = "pro" 
    ENTERPRISE = "enterprise"

@dataclass
class UsageSnapshot:
    """Point-in-time usage snapshot"""
    timestamp: datetime
    business_id: str
    total_tokens: int
    total_cost: float
    requests_count: int
    model_usage: Dict[str, int] = field(default_factory=dict)
    task_type_usage: Dict[str, int] = field(default_factory=dict)

@dataclass
class BudgetAlert:
    """Budget alert configuration"""
    business_id: str
    alert_type: str  # "warning", "limit"
    threshold_percent: float  # e.g., 75.0 for 75%
    current_usage_percent: float
    triggered_at: datetime
    message: str

class EnhancedCostTracker:
    """Comprehensive cost tracking with budgets, alerts, and analytics"""
    
    def __init__(self):
        self.pricing = self._initialize_pricing()
        self.daily_limits = self._initialize_daily_limits()
        self.usage_cache: Dict[str, Dict] = {}  # business_id -> usage data
        self.budget_alerts: Dict[str, List[BudgetAlert]] = {}
        self.usage_history: List[UsageSnapshot] = []
        
        # Real-time tracking
        self.active_sessions: Dict[str, Dict] = {}  # session_id -> session data
        
        # Analytics cache
        self.analytics_cache: Dict[str, Dict] = {}
        self.cache_ttl = 300  # 5 minutes
    
    def _initialize_pricing(self) -> Dict[str, Dict[str, float]]:
        """Initialize comprehensive pricing for different AI models"""
        return {
            "gpt-4-1106-preview": {
                "input": 0.01,    # $0.01 per 1K tokens
                "output": 0.03,   # $0.03 per 1K tokens
                "per_1000": True
            },
            "gpt-4": {
                "input": 0.03,    # $0.03 per 1K tokens
                "output": 0.06,   # $0.06 per 1K tokens
                "per_1000": True
            },
            "gpt-3.5-turbo-1106": {
                "input": 0.001,   # $0.001 per 1K tokens
                "output": 0.002,  # $0.002 per 1K tokens
                "per_1000": True
            },
            "gpt-3.5-turbo": {
                "input": 0.0015,  # $0.0015 per 1K tokens
                "output": 0.002,  # $0.002 per 1K tokens
                "per_1000": True
            }
        }
    
    def _initialize_daily_limits(self) -> Dict[str, Dict[str, Any]]:
        """Initialize tier-based daily usage limits"""
        return {
            SubscriptionTier.FREE: {
                "daily_cost_limit": 10.0,     # $10 per day
                "daily_token_limit": 50000,    # 50K tokens per day
                "request_limit": 50,           # 50 requests per day
                "concurrent_requests": 2,      # 2 concurrent requests
                "priority": "low"
            },
            SubscriptionTier.PRO: {
                "daily_cost_limit": 100.0,    # $100 per day
                "daily_token_limit": 500000,   # 500K tokens per day
                "request_limit": 500,          # 500 requests per day
                "concurrent_requests": 10,     # 10 concurrent requests
                "priority": "normal"
            },
            SubscriptionTier.ENTERPRISE: {
                "daily_cost_limit": 1000.0,   # $1000 per day
                "daily_token_limit": 5000000,  # 5M tokens per day
                "request_limit": 5000,         # 5000 requests per day
                "concurrent_requests": 50,     # 50 concurrent requests
                "priority": "high"
            }
        }

    async def calculate_cost(self, response: AIResponse) -> float:
        """Calculate cost for an AI response with enhanced tracking"""
        try:
            model = response.model.lower()
            
            # Get pricing for model
            if model not in self.pricing:
                logger.warning(f"Unknown model {model}, using default GPT-3.5 pricing")
                model = "gpt-3.5-turbo"
            
            pricing = self.pricing[model]
            
            # Calculate token costs
            input_cost = (response.input_tokens / 1000.0) * pricing["input"]
            output_cost = (response.output_tokens / 1000.0) * pricing["output"]
            total_cost = input_cost + output_cost
            
            logger.debug(f"Cost calculation: {response.input_tokens} input + {response.output_tokens} output = ${total_cost:.6f}")
            
            return round(total_cost, 6)
            
        except Exception as e:
            logger.error(f"Cost calculation failed: {str(e)}")
            return 0.0
    
    async def track_usage(self, business_id: str, response: AIResponse, cost: float, 
                         task_type: str = "unknown") -> Dict[str, Any]:
        """Track usage with comprehensive metadata and budget checking"""
        try:
            # Initialize usage tracking for business
            if business_id not in self.usage_cache:
                self.usage_cache[business_id] = self._initialize_business_usage()
            
            business_usage = self.usage_cache[business_id]
            today = datetime.now().date().isoformat()
            
            # Initialize daily tracking
            if today not in business_usage["daily"]:
                business_usage["daily"][today] = self._initialize_daily_usage()
            
            daily_usage = business_usage["daily"][today]
            
            # Update usage counters
            daily_usage["total_cost"] += cost
            daily_usage["total_tokens"] += response.tokens_used
            daily_usage["request_count"] += 1
            
            # Track by model
            model = response.model
            if model not in daily_usage["models"]:
                daily_usage["models"][model] = {"cost": 0.0, "tokens": 0, "requests": 0}
            
            daily_usage["models"][model]["cost"] += cost
            daily_usage["models"][model]["tokens"] += response.tokens_used
            daily_usage["models"][model]["requests"] += 1
            
            # Track by task type
            if task_type not in daily_usage["task_types"]:
                daily_usage["task_types"][task_type] = {"cost": 0.0, "tokens": 0, "requests": 0}
            
            daily_usage["task_types"][task_type]["cost"] += cost
            daily_usage["task_types"][task_type]["tokens"] += response.tokens_used
            daily_usage["task_types"][task_type]["requests"] += 1
            
            # Update last activity
            daily_usage["last_activity"] = datetime.now().isoformat()
            
            # Create usage snapshot
            snapshot = UsageSnapshot(
                timestamp=datetime.now(),
                business_id=business_id,
                total_tokens=daily_usage["total_tokens"],
                total_cost=daily_usage["total_cost"],
                requests_count=daily_usage["request_count"],
                model_usage=daily_usage["models"].copy(),
                task_type_usage=daily_usage["task_types"].copy()
            )
            self.usage_history.append(snapshot)
            
            # Check budgets and limits
            await self._check_usage_limits(business_id, daily_usage)
            
            logger.info(f"Usage tracked for {business_id}: ${cost:.6f}, {response.tokens_used} tokens")
            
            return {
                "success": True,
                "cost_tracked": cost,
                "tokens_tracked": response.tokens_used,
                "daily_total_cost": daily_usage["total_cost"],
                "daily_total_tokens": daily_usage["total_tokens"],
                "remaining_budget": await self._get_remaining_budget(business_id)
            }
            
        except Exception as e:
            logger.error(f"Usage tracking failed for {business_id}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def check_budget_before_request(self, business_id: str, estimated_tokens: int = 1000) -> Dict[str, Any]:
        """Check if request is within budget before processing"""
        try:
            # Get or create business usage
            if business_id not in self.usage_cache:
                self.usage_cache[business_id] = self._initialize_business_usage()
            
            business_usage = self.usage_cache[business_id]
            today = datetime.now().date().isoformat()
            
            if today not in business_usage["daily"]:
                business_usage["daily"][today] = self._initialize_daily_usage()
            
            daily_usage = business_usage["daily"][today]
            
            # Get subscription tier (default to free for demo)
            tier = business_usage.get("subscription_tier", SubscriptionTier.FREE)
            limits = self.daily_limits[tier]
            
            # Estimate cost for request
            estimated_cost = await self._estimate_request_cost(estimated_tokens)
            
            # Check various limits
            checks = {
                "within_cost_limit": daily_usage["total_cost"] + estimated_cost <= limits["daily_cost_limit"],
                "within_token_limit": daily_usage["total_tokens"] + estimated_tokens <= limits["daily_token_limit"],
                "within_request_limit": daily_usage["request_count"] < limits["request_limit"],
                "estimated_cost": estimated_cost,
                "remaining_cost_budget": limits["daily_cost_limit"] - daily_usage["total_cost"],
                "remaining_token_budget": limits["daily_token_limit"] - daily_usage["total_tokens"],
                "remaining_requests": limits["request_limit"] - daily_usage["request_count"]
            }
            
            checks["can_proceed"] = all([
                checks["within_cost_limit"],
                checks["within_token_limit"],
                checks["within_request_limit"]
            ])
            
            if not checks["can_proceed"]:
                # Generate budget exceeded error
                exceeded_limits = []
                if not checks["within_cost_limit"]:
                    exceeded_limits.append("daily cost limit")
                if not checks["within_token_limit"]:
                    exceeded_limits.append("daily token limit")
                if not checks["within_request_limit"]:
                    exceeded_limits.append("daily request limit")
                
                raise BudgetExceededError(f"Exceeded: {', '.join(exceeded_limits)}")
            
            return checks
            
        except Exception as e:
            logger.error(f"Budget check failed for {business_id}: {str(e)}")
            if isinstance(e, BudgetExceededError):
                raise e
            return {"can_proceed": False, "error": str(e)}
    
    async def get_usage_analytics(self, business_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive usage analytics for a business"""
        try:
            # Check cache first
            cache_key = f"{business_id}_analytics_{days}"
            if cache_key in self.analytics_cache:
                cached = self.analytics_cache[cache_key]
                if (datetime.now() - cached["cached_at"]).seconds < self.cache_ttl:
                    return cached["data"]
            
            # Generate analytics
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            analytics = {
                "business_id": business_id,
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "totals": {
                    "total_cost": 0.0,
                    "total_tokens": 0,
                    "total_requests": 0
                },
                "daily_breakdown": {},
                "model_breakdown": {},
                "task_type_breakdown": {},
                "trends": {},
                "cost_efficiency": {},
                "recommendations": []
            }
            
            # Get business usage data
            if business_id in self.usage_cache:
                business_usage = self.usage_cache[business_id]
                
                # Process daily data within date range
                for date_str, daily_data in business_usage["daily"].items():
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                    
                    if start_date <= date_obj <= end_date:
                        analytics["daily_breakdown"][date_str] = daily_data.copy()
                        
                        # Update totals
                        analytics["totals"]["total_cost"] += daily_data["total_cost"]
                        analytics["totals"]["total_tokens"] += daily_data["total_tokens"]
                        analytics["totals"]["total_requests"] += daily_data["request_count"]
                        
                        # Aggregate model usage
                        for model, model_data in daily_data["models"].items():
                            if model not in analytics["model_breakdown"]:
                                analytics["model_breakdown"][model] = {"cost": 0.0, "tokens": 0, "requests": 0}
                            
                            analytics["model_breakdown"][model]["cost"] += model_data["cost"]
                            analytics["model_breakdown"][model]["tokens"] += model_data["tokens"]
                            analytics["model_breakdown"][model]["requests"] += model_data["requests"]
                        
                        # Aggregate task type usage
                        for task_type, task_data in daily_data["task_types"].items():
                            if task_type not in analytics["task_type_breakdown"]:
                                analytics["task_type_breakdown"][task_type] = {"cost": 0.0, "tokens": 0, "requests": 0}
                            
                            analytics["task_type_breakdown"][task_type]["cost"] += task_data["cost"]
                            analytics["task_type_breakdown"][task_type]["tokens"] += task_data["tokens"]
                            analytics["task_type_breakdown"][task_type]["requests"] += task_data["requests"]
            
            # Calculate trends and efficiency metrics
            analytics["trends"] = await self._calculate_trends(business_id, analytics["daily_breakdown"])
            analytics["cost_efficiency"] = await self._calculate_cost_efficiency(analytics)
            analytics["recommendations"] = await self._generate_usage_recommendations(business_id, analytics)
            
            # Cache results
            self.analytics_cache[cache_key] = {
                "data": analytics,
                "cached_at": datetime.now()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Analytics generation failed for {business_id}: {str(e)}")
            return {"error": str(e)}
    
    async def set_budget_alerts(self, business_id: str, alert_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Configure budget alerts for a business"""
        try:
            if business_id not in self.budget_alerts:
                self.budget_alerts[business_id] = []
            
            # Clear existing alerts
            self.budget_alerts[business_id] = []
            
            # Add new alerts
            for config in alert_configs:
                alert = BudgetAlert(
                    business_id=business_id,
                    alert_type=config["alert_type"],
                    threshold_percent=config["threshold_percent"],
                    current_usage_percent=0.0,
                    triggered_at=datetime.now(),
                    message=config.get("message", f"{config['alert_type']} alert at {config['threshold_percent']}%")
                )
                self.budget_alerts[business_id].append(alert)
            
            logger.info(f"Budget alerts configured for {business_id}: {len(alert_configs)} alerts")
            
            return {
                "success": True,
                "alerts_configured": len(alert_configs),
                "business_id": business_id
            }
            
        except Exception as e:
            logger.error(f"Budget alert configuration failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _initialize_business_usage(self) -> Dict[str, Any]:
        """Initialize usage tracking structure for a business"""
        return {
            "business_id": "",
            "subscription_tier": SubscriptionTier.FREE,
            "daily": {},  # date -> daily usage data
            "created_at": datetime.now().isoformat(),
            "last_reset": datetime.now().date().isoformat()
        }
    
    def _initialize_daily_usage(self) -> Dict[str, Any]:
        """Initialize daily usage tracking structure"""
        return {
            "total_cost": 0.0,
            "total_tokens": 0,
            "request_count": 0,
            "models": {},  # model -> usage data
            "task_types": {},  # task_type -> usage data
            "first_request": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
    
    async def _check_usage_limits(self, business_id: str, daily_usage: Dict[str, Any]):
        """Check usage limits and trigger alerts"""
        try:
            business_usage = self.usage_cache[business_id]
            tier = business_usage.get("subscription_tier", SubscriptionTier.FREE)
            limits = self.daily_limits[tier]
            
            # Calculate usage percentages
            cost_percent = (daily_usage["total_cost"] / limits["daily_cost_limit"]) * 100
            token_percent = (daily_usage["total_tokens"] / limits["daily_token_limit"]) * 100
            request_percent = (daily_usage["request_count"] / limits["request_limit"]) * 100
            
            # Check budget alerts
            if business_id in self.budget_alerts:
                for alert in self.budget_alerts[business_id]:
                    max_percent = max(cost_percent, token_percent, request_percent)
                    
                    if max_percent >= alert.threshold_percent and alert.current_usage_percent < alert.threshold_percent:
                        alert.current_usage_percent = max_percent
                        alert.triggered_at = datetime.now()
                        
                        logger.warning(f"Budget alert triggered for {business_id}: {alert.message} (Usage: {max_percent:.1f}%)")
                        
                        # Here you would send actual notifications (email, webhook, etc.)
                        await self._send_budget_alert(alert)
            
            # Check hard limits
            if cost_percent >= 100 or token_percent >= 100 or request_percent >= 100:
                raise RateLimitError(f"Daily limit exceeded for {business_id}")
                
        except Exception as e:
            logger.error(f"Usage limit check failed: {str(e)}")
            if isinstance(e, RateLimitError):
                raise e
    
    async def _estimate_request_cost(self, estimated_tokens: int, model: str = "gpt-3.5-turbo") -> float:
        """Estimate cost for a request"""
        if model not in self.pricing:
            model = "gpt-3.5-turbo"
        
        pricing = self.pricing[model]
        
        # Estimate input/output token split (rough approximation)
        input_tokens = int(estimated_tokens * 0.7)
        output_tokens = int(estimated_tokens * 0.3)
        
        input_cost = (input_tokens / 1000.0) * pricing["input"]
        output_cost = (output_tokens / 1000.0) * pricing["output"]
        
        return round(input_cost + output_cost, 6)
    
    async def _get_remaining_budget(self, business_id: str) -> Dict[str, float]:
        """Get remaining budget for a business"""
        if business_id not in self.usage_cache:
            return {"cost": 0.0, "tokens": 0, "requests": 0}
        
        business_usage = self.usage_cache[business_id]
        tier = business_usage.get("subscription_tier", SubscriptionTier.FREE)
        limits = self.daily_limits[tier]
        
        today = datetime.now().date().isoformat()
        daily_usage = business_usage["daily"].get(today, self._initialize_daily_usage())
        
        return {
            "cost": limits["daily_cost_limit"] - daily_usage["total_cost"],
            "tokens": limits["daily_token_limit"] - daily_usage["total_tokens"],
            "requests": limits["request_limit"] - daily_usage["request_count"]
        }
    
    async def _calculate_trends(self, business_id: str, daily_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate usage trends"""
        # Implement trend calculation logic
        return {
            "cost_trend": "stable",
            "token_trend": "increasing",
            "request_trend": "stable",
            "efficiency_trend": "improving"
        }
    
    async def _calculate_cost_efficiency(self, analytics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate cost efficiency metrics"""
        totals = analytics["totals"]
        
        if totals["total_requests"] > 0:
            avg_cost_per_request = totals["total_cost"] / totals["total_requests"]
            avg_tokens_per_request = totals["total_tokens"] / totals["total_requests"]
        else:
            avg_cost_per_request = 0.0
            avg_tokens_per_request = 0.0
        
        return {
            "avg_cost_per_request": round(avg_cost_per_request, 6),
            "avg_tokens_per_request": round(avg_tokens_per_request, 2),
            "cost_per_1k_tokens": round((totals["total_cost"] / max(totals["total_tokens"], 1)) * 1000, 6)
        }
    
    async def _generate_usage_recommendations(self, business_id: str, analytics: Dict[str, Any]) -> List[str]:
        """Generate usage optimization recommendations"""
        recommendations = []
        
        # Model usage recommendations
        model_breakdown = analytics["model_breakdown"]
        if model_breakdown:
            most_expensive_model = max(model_breakdown.items(), key=lambda x: x[1]["cost"])
            recommendations.append(f"Consider optimizing usage of {most_expensive_model[0]} which accounts for highest costs")
        
        # Token efficiency recommendations  
        efficiency = analytics["cost_efficiency"]
        if efficiency["avg_tokens_per_request"] > 2000:
            recommendations.append("Consider breaking down large requests to improve token efficiency")
        
        # General optimization
        recommendations.append("Monitor daily usage patterns to optimize request timing")
        
        return recommendations
    
    async def _send_budget_alert(self, alert: BudgetAlert):
        """Send budget alert notification (placeholder)"""
        # In a real implementation, this would send emails, webhooks, etc.
        logger.info(f"Budget alert sent: {alert.message}")

# Backward compatibility
CostTracker = EnhancedCostTracker

# Global cost tracker instance
cost_tracker = CostTracker()
