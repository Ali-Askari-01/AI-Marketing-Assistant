"""
Simple FastAPI Health Check Server
For testing and demonstration purposes
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Marketing Command Center API",
    version="1.0.0",
    description="AI-powered marketing automation platform"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, be more specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str = ""

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Marketing Command Center API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Marketing Command Center",
        "version": "1.0.0"
    }

@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "success": True,
        "data": {
            "api_status": "operational",
            "database_status": "demo_mode",
            "ai_status": "demo_mode"
        }
    }

# Mock auth endpoints for frontend testing
@app.post("/api/v1/auth/login")
async def mock_login(request_data: LoginRequest):
    """Mock login endpoint"""
    return {
        "success": True,
        "data": {
            "user_id": "mock-user-id",
            "email": request_data.email,
            "full_name": "Demo User",
            "access_token": "mock-jwt-token",
            "refresh_token": "mock-refresh-token",
            "expires_in": 3600
        }
    }

@app.post("/api/v1/auth/register") 
async def mock_register(request_data: RegisterRequest):
    """Mock register endpoint"""
    return {
        "success": True,
        "data": {
            "user_id": "mock-user-id",
            "email": request_data.email, 
            "full_name": request_data.full_name or "Demo User",
            "access_token": "mock-jwt-token",
            "refresh_token": "mock-refresh-token",
            "expires_in": 3600
        }
    }

@app.get("/api/v1/auth/me")
async def mock_user_profile():
    """Mock user profile endpoint"""
    return {
        "success": True,
        "data": {
            "user_id": "mock-user-id",
            "email": "demo@example.com",
            "full_name": "Demo User",
            "is_verified": True,
            "plan": "pro"
        }
    }

# Mock business endpoints
@app.get("/api/v1/business")
async def mock_list_businesses():
    """Mock list businesses"""
    return {
        "success": True,
        "data": [
            {
                "id": "mock-business-1",
                "name": "Demo Business", 
                "industry": "Technology",
                "description": "A demo business for testing"
            }
        ]
    }

@app.post("/api/v1/business")
async def mock_create_business(business_data: dict):
    """Mock create business"""
    return {
        "success": True,
        "data": {
            "id": "mock-business-id",
            "name": business_data.get("name", "New Business"),
            "industry": business_data.get("industry", "Technology"),
            "description": business_data.get("description", "")
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)