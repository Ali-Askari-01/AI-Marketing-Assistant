"""
Authentication Routes
Implements the API contract for authentication endpoints
Updated for SQLite with SQLAlchemy ORM
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import uuid

from contracts.api_contract import (
    APIContract, ErrorCode, RegisterRequest, LoginRequest, AuthResponse,
    RequestContext, ValidationRules, get_status_code
)
from core.security import security_manager
from models.database import UserRepository as SQLiteUserRepo
from core.config import settings


def _get_db():
    """Get the SQLite database manager singleton."""
    from main import sqlite_db
    return sqlite_db

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=Dict[str, Any])
async def register(request: Request, user_data: RegisterRequest) -> Dict[str, Any]:
    """Register new user"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id)
    
    try:
        # Validate request
        if not ValidationRules.validate_email(user_data.email):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("email", "Invalid email format")
            )
        
        if not ValidationRules.validate_password(user_data.password):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("password", "Password must be at least 8 characters with uppercase, lowercase, and digit")
            )
        
        # Check if user already exists
        db = _get_db()
        with db.get_session() as session:
            repo = SQLiteUserRepo(session)
            existing_user = repo.get_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=409,
                    detail=APIContract.error_response(
                        ErrorCode.EMAIL_ALREADY_EXISTS,
                        "Email already registered"
                    )
                )
        
            # Create user
            password_hash = security_manager.hash_password(user_data.password)
            full_name = user_data.full_name or user_data.email.split("@")[0]
            user = repo.create(
                {
                    "email": user_data.email.lower(),
                    "password_hash": password_hash,
                    "full_name": full_name,
                    "first_name": full_name.split()[0] if full_name else "",
                    "last_name": " ".join(full_name.split()[1:]) if full_name else "",
                    "is_active": True,
                    "is_verified": False,
                    "provider": "email",
                    "timezone": "UTC",
                    "language": "en",
                }
            )
        
            # Generate tokens
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "provider": "email"
            }
        
        access_token = security_manager.create_access_token(token_data)
        refresh_token = security_manager.create_refresh_token(token_data)
        
        response_data = {
            "user_id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/login", response_model=Dict[str, Any])
async def login(request: Request, login_data: LoginRequest) -> Dict[str, Any]:
    """Login user"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id)
    
    try:
        # Validate request
        if not ValidationRules.validate_email(login_data.email):
            raise HTTPException(
                status_code=400,
                detail=APIContract.validation_error_response("email", "Invalid email format")
            )
        
        # Get user
        db = _get_db()
        with db.get_session() as session:
            repo = SQLiteUserRepo(session)
            user = repo.get_by_email(login_data.email)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail=APIContract.error_response(
                        ErrorCode.INVALID_CREDENTIALS,
                        "Invalid email or password"
                    )
                )
        
            # Check if user is active
            if not user.is_active:
                raise HTTPException(
                    status_code=401,
                    detail=APIContract.error_response(
                        ErrorCode.ACCOUNT_DISABLED,
                        "Account is disabled"
                    )
                )
        
            # Verify password
            if not security_manager.verify_password(login_data.password, user.password_hash):
                raise HTTPException(
                    status_code=401,
                    detail=APIContract.error_response(
                        ErrorCode.INVALID_CREDENTIALS,
                        "Invalid email or password"
                    )
                )
        
            # Update login stats
            repo.update_login_stats(user.id)

            # Generate tokens
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "provider": "email"
            }
        
            access_token = security_manager.create_access_token(token_data)
            refresh_token = security_manager.create_refresh_token(token_data)
        
            response_data = {
                "user_id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_profile(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get current user profile"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id)
    
    try:
        # Verify token
        payload = security_manager.verify_token(credentials.credentials)
        context.user_id = payload.get("sub")
        
        # Get user
        db = _get_db()
        with db.get_session() as session:
            repo = SQLiteUserRepo(session)
            user = repo.get_by_id(context.user_id)
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail=APIContract.error_response(
                        ErrorCode.NOT_FOUND,
                        "User not found"
                    )
                )
        
            response_data = {
                "user_id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "is_verified": user.is_verified,
                "plan": user.subscription_plan,
                "timezone": user.timezone,
                "language": user.language,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/refresh", response_model=Dict[str, Any])
async def refresh_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Refresh access token"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id)
    
    try:
        # Verify token
        payload = security_manager.verify_token(credentials.credentials)
        
        # Check if it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail=APIContract.error_response(
                    ErrorCode.INVALID_TOKEN,
                    "Invalid token type"
                )
            )
        
        # Generate new access token
        token_data = {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "provider": payload.get("provider")
        }
        
        access_token = security_manager.create_access_token(token_data)
        refresh_token = security_manager.create_refresh_token(token_data)
        
        response_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
        return APIContract.success_response(
            response_data,
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )

@router.post("/signout", response_model=Dict[str, Any])
async def signout(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Sign out user"""
    request_id = str(uuid.uuid4())
    context = RequestContext(request_id)
    
    try:
        # Verify token
        payload = security_manager.verify_token(credentials.credentials)
        
        # In a real implementation, you would invalidate the token here
        # For now, just return success
        
        return APIContract.success_response(
            {"message": "Successfully signed out"},
            meta=context.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=APIContract.internal_error_response(str(e))
        )
