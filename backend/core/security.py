"""
Core Security Module
Centralized security functions for authentication, authorization, and validation
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings

# Security instance
security = HTTPBearer()

class SecurityManager:
    """Centralized security management"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "iss": settings.APP_NAME,
            "aud": f"{settings.APP_NAME}-users"
        })
        
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "iss": settings.APP_NAME,
            "aud": f"{settings.APP_NAME}-users",
            "type": "refresh"
        })
        
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM],
                audience=f"{settings.APP_NAME}-users",
                issuer=settings.APP_NAME
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        import bcrypt
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def validate_business_ownership(user_id: str, business_id: str, db) -> bool:
        """Validate that user owns the business"""
        # This would be implemented with actual database queries
        # For now, return True for demo
        return True
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        import re
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\';()&+]', '', input_string)
        return sanitized.strip()

# Global security manager instance
security_manager = SecurityManager()

# Dependency functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = security_manager.verify_token(token)
    return payload

async def get_current_business(current_user: Dict[str, Any] = Depends(get_current_user)) -> str:
    """Get current business ID from authenticated user"""
    # This would fetch the business ID from the database
    # For now, return a demo business ID
    return "demo_business_id"

# Rate limiting decorator
def rate_limit(max_requests: int, window_minutes: int = 1):
    """Rate limiting decorator"""
    def decorator(func):
        # This would be implemented with Redis or in-memory storage
        # For now, just pass through
        return func
    return decorator

# Standalone helper functions for backwards compatibility
def validate_business_ownership(user_id: str, business_id: str, db=None) -> bool:
    """Validate that user owns the business - wrapper for SecurityManager method"""
    return security_manager.validate_business_ownership(user_id, business_id, db)
