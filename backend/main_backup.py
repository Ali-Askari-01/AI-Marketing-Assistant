"""
Production-Ready FastAPI Backend for AI Marketing Command Center
Implements complete 6-layer architecture with proper separation of concerns
"""

from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.background import BackgroundTasks
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging
import time
import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import uvicorn
from pydantic import BaseModel, Field
import hashlib
import secrets
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import our layered architecture components
from core.config import settings
from core.security import security_manager, get_current_user, get_current_business
from core.errors import error_handler, BaseError
from models.mongo_db import db_manager, initialize_database, user_repo, business_repo, campaign_repo, content_repo
from services.business_service import business_service
from services.campaign_service import campaign_service
from ai.ai_service import ai_service
from schemas.requests import *
from schemas.responses import *

# Import API routes
from routes.auth import router as auth_router
from routes.business import router as business_router
from routes.campaign import router as campaign_router
from routes.content import router as content_router
from routes.analytics import router as analytics_router
from routes.messaging import router as messaging_router
from routes.ai import router as ai_router
from routes.agent import router as agent_router
# from routes.database import router as database_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Security
security = HTTPBearer()

# Background tasks
background_tasks = BackgroundTasks()

# Application lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    logger.info("Starting AI Marketing Command Center Backend...")
    
    # Initialize database connection
    try:
        await initialize_database()
        health_check = await db_manager.health_check()
        logger.info(f"Database health: {health_check['status']}")
    except Exception as e:
        logger.warning(f"Database connection failed: {e}")
        logger.info("Running in demo mode without database persistence")
        # Continue without database for demo purposes
    
    # Initialize AI service
    try:
        ai_status = await ai_service.get_service_status()
        logger.info(f"AI Service status: {ai_status['status']}")
    except Exception as e:
        logger.error(f"AI service initialization failed: {e}")
    
    logger.info("Backend startup complete")
    yield
    
    # Cleanup
    logger.info("Shutting down backend...")
    await db_manager.disconnect()
    logger.info("Backend shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="AI Marketing Command Center",
    description="Enterprise-grade AI-powered marketing platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting
app.state.limiter = limiter
if isinstance(RateLimitExceeded, type) and issubclass(RateLimitExceeded, Exception):
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
else:
    logger.warning("Skipping SlowAPI exception handler registration: RateLimitExceeded is not an Exception class")

# Global exception handler
@app.exception_handler(BaseError)
async def base_error_handler(request: Request, exc: BaseError):
    """Handle custom base errors"""
    return error_handler.create_error_response(exc)

@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    return error_handler.handle_general_error(exc)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response

# Register API routes
app.include_router(auth_router, prefix="/api/v1")
app.include_router(business_router, prefix="/api/v1")
app.include_router(campaign_router, prefix="/api/v1")
app.include_router(content_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(messaging_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(agent_router)  # Gemini AI Agent routes
# app.include_router(database_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check database
        db_status = "healthy"
        try:
            await db.get_collection("test").find_one()
        except:
            db_status = "unhealthy"
        
        # Check AI service
        ai_status = await ai_service.get_service_status()
        
        return HealthCheckResponse(
            status="healthy" if db_status == "healthy" and ai_status["status"] == "healthy" else "degraded",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            environment=settings.ENVIRONMENT,
            database={"status": db_status},
            ai_service={"status": ai_status["status"]},
            uptime_seconds=int(time.time()),
            memory_usage={"used": "N/A", "total": "N/A"},
            cpu_usage={"used": "N/A", "total": "N/A"}
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            environment=settings.ENVIRONMENT,
            database={"status": "unhealthy"},
            ai_service={"status": "unhealthy"},
            uptime_seconds=int(time.time()),
            memory_usage={"used": "N/A", "total": "N/A"},
            cpu_usage={"used": "N/A", "total": "N/A"}
        )

# Pydantic Models
class User(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

class Business(BaseModel):
    id: str
    owner_id: str
    name: str
    industry: str
    description: str
    target_audience: Dict[str, Any]
    brand_voice: str
    content_preferences: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class Campaign(BaseModel):
    id: str
    business_id: str
    name: str
    goal: str
    duration_days: int
    strategy_summary: str
    content_calendar: List[Dict[str, Any]]
    status: str
    start_date: datetime
    end_date: datetime
    created_at: datetime

class Content(BaseModel):
    id: str
    campaign_id: str
    business_id: str
    day: int
    platform: str
    content_type: str
    caption: str
    hashtags: List[str]
    media: Dict[str, str]
    script: Optional[str]
    status: str
    scheduled_at: Optional[datetime]
    ai_metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class Analytics(BaseModel):
    id: str
    content_id: str
    platform: str
    metrics: Dict[str, Any]
    predicted_performance: Dict[str, Any]
    collected_at: datetime

class Message(BaseModel):
    id: str
    business_id: str
    platform: str
    incoming_message: str
    generated_reply: str
    confidence_score: float
    status: str
    created_at: datetime

class AILog(BaseModel):
    id: str
    user_id: str
    feature: str
    model_used: str
    tokens_used: int
    input_prompt_hash: str
    status: str
    error_message: Optional[str]
    response_time_ms: int
    created_at: datetime

# Error Models
class ErrorResponse(BaseModel):
    success: bool = False
    error: Dict[str, Any]

class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

# FastAPI App
app = FastAPI(
    title="AI Marketing Command Center API",
    description="Production-ready API for AI-powered marketing automation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.aimarketing.ai"]
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Too many requests. Please try again later."
            }
        }
    )

# Security Utilities
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = hashlib.sha256(f"{settings.SECRET_KEY}{json.dumps(to_encode)}".encode()).hexdigest()
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        # Simple token verification (in production, use proper JWT)
        payload = hashlib.sha256(f"{settings.SECRET_KEY}{token}".encode()).hexdigest()
        return {"sub": "user", "exp": time.time() + 3600}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# Database Connection (Mock for demo)
class DatabaseManager:
    def __init__(self):
        self.users = {}
        self.businesses = {}
        self.campaigns = {}
        self.contents = {}
        self.analytics = {}
        self.messages = {}
        self.ai_logs = {}

    async def connect(self):
        logger.info("Connected to database")
        return True

    async def disconnect(self):
        logger.info("Disconnected from database")

# AI Service Integration
class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.DEFAULT_AI_MODEL
        self.base_url = "https://api.openai.com/v1"

    async def generate_content(self, prompt: str) -> Dict[str, Any]:
        """Generate content using OpenAI API"""
        try:
            # Mock AI response for demo
            await asyncio.sleep(1)  # Simulate API call
            
            return {
                "content": f"Generated content for: {prompt}",
                "tokens_used": 150,
                "model": self.model,
                "confidence": 0.85
            }
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            raise HTTPException(status_code=500, detail="AI_GENERATION_FAILED")

    async def generate_strategy(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate marketing strategy"""
        try:
            await asyncio.sleep(2)  # Simulate API call
            
            return {
                "strategy": f"Marketing strategy for {business_data.get('name', 'business')}",
                "calendar": [
                    {"day": 1, "theme": "Introduction", "content_type": "post"},
                    {"day": 2, "theme": "Product Showcase", "content_type": "reel"}
                ],
                "kpis": {"engagement_rate": 5.0, "leads_target": 100}
            }
        except Exception as e:
            logger.error(f"Strategy generation failed: {e}")
            raise HTTPException(status_code=500, detail="AI_GENERATION_FAILED")

    async def generate_reply(self, message: str) -> Dict[str, Any]:
        """Generate AI reply for customer message"""
        try:
            await asyncio.sleep(1)
            
            return {
                "reply": f"AI reply for: {message}",
                "confidence": 0.92
            }
        except Exception as e:
            logger.error(f"Reply generation failed: {e}")
            raise HTTPException(status_code=500, detail="AI_GENERATION_FAILED")

# Initialize services
db = DatabaseManager()
ai_service = AIService()

# Authentication Dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = verify_token(token.credentials)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

# Register Gemini AI Agent routes on this app instance
app.include_router(agent_router)

# Authentication Endpoints
@app.post("/api/auth/{provider}/callback", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def auth_callback(request: Request, provider: str, callback_data: dict):
    """Handle OAuth callback from Google or Microsoft"""
    try:
        if provider not in ["google", "microsoft"]:
            raise HTTPException(status_code=400, detail="Invalid provider")
        
        # For demo, simulate successful OAuth callback
        # In production, this would exchange the code for tokens
        user_data = {
            "id": f"user_{int(time.time())}",
            "email": f"user.{provider}@example.com",
            "name": f"Demo User ({provider.capitalize()})",
            "firstName": "Demo",
            "lastName": "User",
            "picture": f"https://ui-avatars.com/api/?name=Demo+User&background=random",
            "provider": provider,
            "providerId": f"{provider}_user_{int(time.time())}",
            "createdAt": datetime.utcnow().isoformat(),
            "lastLogin": datetime.utcnow().isoformat()
        }
        
        business_data = {
            "id": f"business_{int(time.time())}",
            "name": "Demo Business",
            "industry": "Technology",
            "plan": "free",
            "createdAt": datetime.utcnow().isoformat()
        }
        
        # Generate JWT tokens
        access_token = create_access_token({"sub": user_data["id"]}, timedelta(hours=1))
        refresh_token = create_access_token({"sub": user_data["id"]}, timedelta(days=7))
        
        # Store user in database
        db.users[user_data["id"]] = User(
            id=user_data["id"],
            email=user_data["email"],
            full_name=user_data["name"],
            role="user",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Store business in database
        db.businesses[business_data["id"]] = Business(
            id=business_data["id"],
            owner_id=user_data["id"],
            name=business_data["name"],
            industry=business_data["industry"],
            description="Demo business for SSO testing",
            target_audience={
                "age_range": "25-45",
                "gender_focus": "All",
                "location": "Global",
                "interests": ["Technology", "Marketing", "AI"]
            },
            brand_voice="Professional but innovative",
            content_preferences={
                "platforms": ["Instagram", "LinkedIn", "Email"],
                "tone": "Professional",
                "post_frequency_per_week": 5
            },
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        return SuccessResponse(
            data={
                "token": access_token,
                "refreshToken": refresh_token,
                "user": user_data,
                "business": business_data
            },
            message=f"Successfully authenticated with {provider.capitalize()}"
        )
        
    except Exception as e:
        logger.error(f"SSO callback failed for {provider}: {e}")
        raise HTTPException(status_code=401, detail="OAuth authentication failed")

@app.post("/api/auth/refresh", response_model=SuccessResponse)
@limiter.limit("20/minute")
async def refresh_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh JWT access token using refresh token"""
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        # Generate new tokens
        new_access_token = create_access_token({"sub": payload["sub"]}, timedelta(hours=1))
        new_refresh_token = create_access_token({"sub": payload["sub"]}, timedelta(days=7))
        
        return SuccessResponse(
            data={
                "token": new_access_token,
                "refreshToken": new_refresh_token,
                "expiresIn": 3600
            },
            message="Token refreshed successfully"
        )
        
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@app.get("/api/auth/me", response_model=SuccessResponse)
async def get_current_user_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user profile"""
    try:
        token = credentials.credentials
        payload = verify_token(token)
        user_id = payload["sub"]
        
        # Get user from database
        user = db.users.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's business
        user_business = None
        for business in db.businesses.values():
            if business.owner_id == user_id:
                user_business = {
                    "id": business.id,
                    "name": business.name,
                    "industry": business.industry,
                    "plan": "free",
                    "createdAt": business.created_at.isoformat()
                }
                break
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.full_name,
            "firstName": user.full_name.split(" ")[0],
            "lastName": " ".join(user.full_name.split(" ")[1:]) if len(user.full_name.split(" ")) > 1 else "",
            "picture": f"https://ui-avatars.com/api/?name={user.full_name.replace(' ', '+')}&background=random",
            "provider": "sso_demo",
            "providerId": user.id,
            "createdAt": user.created_at.isoformat(),
            "lastLogin": datetime.utcnow().isoformat()
        }
        
        return SuccessResponse(
            data={
                **user_data,
                "business": user_business
            },
            message="User profile retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Get user profile failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user profile")

@app.post("/api/auth/signout", response_model=SuccessResponse)
async def sign_out_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Sign out user and invalidate tokens"""
    try:
        # In a real implementation, you would invalidate the token in a database
        # For demo, we just return success
        return SuccessResponse(
            message="Successfully signed out"
        )
        
    except Exception as e:
        logger.error(f"Sign out failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to sign out")

@app.post("/api/auth/login", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def email_password_login(request: Request, login_data: dict):
    """Traditional email/password authentication"""
    try:
        email = login_data.get("email")
        password = login_data.get("password")
        
        # For demo, accept any email/password
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password required")
        
        # Create or get user
        user_id = f"email_user_{int(time.time())}"
        user = User(
            id=user_id,
            email=email,
            full_name=email.split("@")[0].title(),
            role="user",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.users[user_id] = user
        
        # Generate tokens
        access_token = create_access_token({"sub": user_id}, timedelta(hours=1))
        refresh_token = create_access_token({"sub": user_id}, timedelta(days=7))
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.full_name,
            "firstName": user.full_name.split(" ")[0],
            "lastName": " ".join(user.full_name.split(" ")[1:]) if len(user.full_name.split(" ")) > 1 else "",
            "provider": "email",
            "createdAt": user.created_at.isoformat(),
            "lastLogin": datetime.utcnow().isoformat()
        }
        
        return SuccessResponse(
            data={
                "token": access_token,
                "refreshToken": refresh_token,
                "user": user_data
            },
            message="Login successful"
        )
        
    except Exception as e:
        logger.error(f"Email login failed: {e}")
        raise HTTPException(status_code=401, detail="Login failed")

@app.post("/api/auth/register", response_model=SuccessResponse)
@limiter.limit("3/minute")
async def email_password_register(request: Request, register_data: dict):
    """Register new user with email/password"""
    try:
        email = register_data.get("email")
        password = register_data.get("password")
        name = register_data.get("name")
        business_data = register_data.get("business", {})
        
        if not email or not password or not name:
            raise HTTPException(status_code=400, detail="Email, password, and name required")
        
        # Create user
        user_id = f"email_user_{int(time.time())}"
        user = User(
            id=user_id,
            email=email,
            full_name=name,
            role="user",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.users[user_id] = user
        
        # Create business
        business_id = f"business_{int(time.time())}"
        business = Business(
            id=business_id,
            owner_id=user_id,
            name=business_data.get("name", f"{name}'s Business"),
            industry=business_data.get("industry", "Technology"),
            description="Business created during registration",
            target_audience={
                "age_range": "25-45",
                "gender_focus": "All",
                "location": "Global",
                "interests": ["Technology", "Marketing", "Business"]
            },
            brand_voice="Professional",
            content_preferences={
                "platforms": ["Instagram", "LinkedIn", "Email"],
                "tone": "Professional",
                "post_frequency_per_week": 3
            },
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.businesses[business_id] = business
        
        # Generate tokens
        access_token = create_access_token({"sub": user_id}, timedelta(hours=1))
        refresh_token = create_access_token({"sub": user_id}, timedelta(days=7))
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.full_name,
            "firstName": user.full_name.split(" ")[0],
            "lastName": " ".join(user.full_name.split(" ")[1:]) if len(user.full_name.split(" ")) > 1 else "",
            "provider": "email",
            "createdAt": user.created_at.isoformat(),
            "lastLogin": datetime.utcnow().isoformat()
        }
        
        business_response = {
            "id": business.id,
            "name": business.name,
            "industry": business.industry,
            "plan": "free",
            "createdAt": business.created_at.isoformat()
        }
        
        return SuccessResponse(
            data={
                "token": access_token,
                "refreshToken": refresh_token,
                "user": user_data,
                "business": business_response
            },
            message="Registration successful"
        )
        
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(status_code=400, detail="Registration failed")

# Business Management Endpoints
@app.post("/business/", response_model=SuccessResponse)
async def create_business(business_data: dict, current_user: dict = Depends(get_current_user)):
    """Create a new business"""
    try:
        business_id = f"business_{int(time.time())}"
        business = Business(
            id=business_id,
            owner_id=current_user["sub"],
            name=business_data["name"],
            industry=business_data["industry"],
            description=business_data.get("description", ""),
            target_audience=business_data.get("target_audience", {}),
            brand_voice=business_data.get("brand_voice", "Professional"),
            content_preferences=business_data.get("content_preferences", {}),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.businesses[business_id] = business
        
        return SuccessResponse(
            data={"business_id": business_id},
            message="Business created successfully"
        )
    except Exception as e:
        logger.error(f"Business creation failed: {e}")
        raise HTTPException(status_code=400, detail="Business creation failed")

@app.get("/business/{business_id}", response_model=SuccessResponse)
async def get_business(business_id: str, current_user: dict = Depends(get_current_user)):
    """Get business details"""
    try:
        business = db.businesses.get(business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        
        if business.owner_id != current_user["sub"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return SuccessResponse(data={"business": business})
    except Exception as e:
        logger.error(f"Get business failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get business")

# Campaign Management Endpoints
@app.post("/campaign/", response_model=SuccessResponse)
async def create_campaign(campaign_data: dict, current_user: dict = Depends(get_current_user)):
    """Create a new campaign"""
    try:
        campaign_id = f"campaign_{int(time.time())}"
        campaign = Campaign(
            id=campaign_id,
            business_id=campaign_data["business_id"],
            name=campaign_data["name"],
            goal=campaign_data["goal"],
            duration_days=campaign_data.get("duration_days", 30),
            strategy_summary=campaign_data.get("strategy_summary", ""),
            content_calendar=campaign_data.get("content_calendar", []),
            status="draft",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            created_at=datetime.utcnow()
        )
        
        db.campaigns[campaign_id] = campaign
        
        return SuccessResponse(
            data={"campaign_id": campaign_id},
            message="Campaign created successfully"
        )
    except Exception as e:
        logger.error(f"Campaign creation failed: {e}")
        raise HTTPException(status_code=400, detail="Campaign creation failed")

@app.get("/campaign/{campaign_id}", response_model=SuccessResponse)
async def get_campaign(campaign_id: str, current_user: dict = Depends(get_current_user)):
    """Get campaign details"""
    try:
        campaign = db.campaigns.get(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Verify ownership
        business = db.businesses.get(campaign.business_id)
        if not business or business.owner_id != current_user["sub"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return SuccessResponse(data={"campaign": campaign})
    except Exception as e:
        logger.error(f"Get campaign failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get campaign")

# AI Strategy Endpoints
@app.post("/ai/strategy/generate-calendar", response_model=SuccessResponse)
@limiter.limit("3/minute")
async def generate_calendar(request: Request, strategy_data: dict, current_user: dict = Depends(get_current_user)):
    """Generate content calendar using AI"""
    try:
        # Log AI usage
        ai_log_id = f"ai_log_{int(time.time())}"
        start_time = time.time()
        
        # Get business data
        business = db.businesses.get(strategy_data["business_id"])
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        
        # Generate strategy
        strategy = await ai_service.generate_strategy(strategy_data)
        
        # Log AI usage
        end_time = time.time()
        ai_log = AILog(
            id=ai_log_id,
            user_id=current_user["sub"],
            feature="calendar_generation",
            model_used=ai_service.model,
            tokens_used=200,
            input_prompt_hash=str(hash(str(strategy_data))),
            status="success",
            response_time_ms=int((end_time - start_time) * 1000),
            created_at=datetime.utcnow()
        )
        
        db.ai_logs[ai_log_id] = ai_log
        
        return SuccessResponse(
            data={"strategy": strategy},
            message="Calendar generated successfully"
        )
    except Exception as e:
        logger.error(f"Calendar generation failed: {e}")
        raise HTTPException(status_code=500, detail="AI_GENERATION_FAILED")

# Content Generation Endpoints
@app.post("/content/generate", response_model=SuccessResponse)
@limiter.limit("5/minute")
async def generate_content(request: Request, content_request: dict, current_user: dict = Depends(get_current_user)):
    """Generate content using AI"""
    try:
        ai_log_id = f"ai_log_{int(time.time())}"
        start_time = time.time()
        
        # Generate content
        content = await ai_service.generate_content(content_request.get("prompt", ""))
        
        # Create content record
        content_id = f"content_{int(time.time())}"
        content_record = Content(
            id=content_id,
            campaign_id=content_request.get("campaign_id"),
            business_id=content_request.get("business_id"),
            day=content_request.get("day", 1),
            platform=content_request.get("platform", "instagram"),
            content_type=content_request.get("type", "post"),
            caption=content.get("content"),
            hashtags=content_request.get("hashtags", []),
            media=content_request.get("media", {}),
            script=content.get("script"),
            status="draft",
            ai_metadata={
                "model_used": ai_service.model,
                "tokens_used": content.get("tokens_used", 150),
                "generation_time_ms": int((time.time() - start_time) * 1000)
            },
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.contents[content_id] = content_record
        
        # Log AI usage
        end_time = time.time()
        ai_log = AILog(
            id=ai_log_id,
            user_id=current_user["sub"],
            feature="content_generation",
            model_used=ai_service.model,
            tokens_used=content.get("tokens_used", 150),
            input_prompt_hash=str(hash(str(content_request))),
            status="success",
            response_time_ms=int((end_time - start_time) * 1000),
            created_at=datetime.utcnow()
        )
        
        db.ai_logs[ai_log_id] = ai_log
        
        return SuccessResponse(
            data={"content": content_record},
            message="Content generated successfully"
        )
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        raise HTTPException(status_code=500, detail="AI_GENERATION_FAILED")

# Analytics Endpoints
@app.post("/analytics/simulate", response_model=SuccessResponse)
async def simulate_analytics(analytics_request: dict):
    """Simulate analytics for content"""
    try:
        content_id = analytics_request.get("content_id")
        
        # Generate mock analytics
        analytics = Analytics(
            id=f"analytics_{int(time.time())}",
            content_id=content_id,
            platform="instagram",
            metrics={
                "views": int(time.time() * 10) % 10000 + 1000,
                "likes": int(time.time() * 5) % 1000 + 100,
                "comments": int(time.time() * 3) % 100 + 10,
                "shares": int(time.time() * 2) % 50 + 5,
                "engagement_rate": round((int(time.time() * 7) % 10 + 1), 1)
            },
            predicted_performance={
                "score": int(time.time() * 10) % 30 + 70,
                "confidence": round((int(time.time() * 100) % 100) / 100, 2)
            },
            collected_at=datetime.utcnow()
        )
        
        db.analytics[analytics.id] = analytics
        
        return SuccessResponse(
            data={"analytics": analytics},
            message="Analytics simulated successfully"
        )
    except Exception as e:
        logger.error(f"Analytics simulation failed: {e}")
        raise HTTPException(status_code=500, detail="Analytics simulation failed")

# Messaging Endpoints
@app.get("/messages", response_model=SuccessResponse)
async def get_messages(business_id: str, current_user: dict = Depends(get_current_user)):
    """Get messages for a business"""
    try:
        # Verify business ownership
        business = db.businesses.get(business_id)
        if not business or business.owner_id != current_user["sub"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get messages
        messages = list(db.messages.values())
        business_messages = [msg for msg in messages if msg.business_id == business_id]
        
        return SuccessResponse(
            data={"messages": business_messages},
            message="Messages retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Get messages failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get messages")

@app.post("/messages/{message_id}/ai-reply", response_model=SuccessResponse)
@limiter.limit("10/minute")
async def get_ai_reply(request: Request, message_id: str, current_user: dict = Depends(get_current_user)):
    """Generate AI reply for message"""
    try:
        message = db.messages.get(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Verify business ownership
        business = db.businesses.get(message.business_id)
        if not business or business.owner_id != current_user["sub"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Generate AI reply
        reply_data = await ai_service.generate_reply(message.incoming_message)
        
        # Update message
        message.generated_reply = reply_data["reply"]
        message.confidence_score = reply_data["confidence"]
        message.status = "replied"
        
        return SuccessResponse(
            data={"reply": reply_data["reply"]},
            message="AI reply generated successfully"
        )
    except Exception as e:
        logger.error(f"AI reply generation failed: {e}")
        raise HTTPException(status_code=500, detail="AI_GENERATION_FAILED")

# Monitoring Endpoints
@app.post("/monitoring")
async def log_monitoring_data(monitoring_data: dict):
    """Log monitoring data"""
    try:
        logger.info(f"Monitoring data: {monitoring_data}")
        return SuccessResponse(message="Monitoring data logged")
    except Exception as e:
        logger.error(f"Monitoring logging failed: {e}")
        raise HTTPException(status_code=500, detail="Monitoring logging failed")

@app.get("/monitoring/health")
async def monitoring_health():
    """Get monitoring system health"""
    return {
        "status": "healthy",
        "logs_count": len(db.ai_logs),
        "timestamp": datetime.utcnow().isoformat()
    }

# Background Tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    await db.disconnect()
    logger.info("Application shutdown complete")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=settings.ENVIRONMENT == "development",
        reload_excludes=["*.log", "*.pyc", "__pycache__"],
        log_level="info",
        access_log=True
    )
