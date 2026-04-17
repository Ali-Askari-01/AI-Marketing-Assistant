"""
Core Error Handling Module
Centralized error definitions and error response formatting
"""

from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from .config import settings

class BaseError(Exception):
    """Base error class for all custom errors"""
    
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(BaseError):
    """Validation error for invalid input data"""
    
    def __init__(self, message: str, field: str = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details or {"field": field} if field else {}
        )

class AuthenticationError(BaseError):
    """Authentication error for failed authentication"""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details or {}
        )

class AuthorizationError(BaseError):
    """Authorization error for insufficient permissions"""
    
    def __init__(self, message: str = "Access denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
            details=details or {}
        )

class NotFoundError(BaseError):
    """Not found error for missing resources"""
    
    def __init__(self, resource: str = "Resource", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"{resource} not found",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details or {}
        )

class ConflictError(BaseError):
    """Conflict error for resource conflicts"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=status.HTTP_409_CONFLICT,
            details=details or {}
        )

class RateLimitError(BaseError):
    """Rate limit error for too many requests"""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details or {}
        )

class AIServiceError(BaseError):
    """AI service error for AI-related failures"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="AI_SERVICE_ERROR",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details or {}
        )

class DatabaseError(BaseError):
    """Database error for database-related failures"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details or {}
        )

class BusinessNotFoundError(NotFoundError):
    """Business not found error"""
    
    def __init__(self, business_id: str = None, details: Optional[Dict[str, Any]] = None):
        message = f"Business {business_id} not found" if business_id else "Business not found"
        super().__init__(resource="Business", details=details or {"business_id": business_id} if business_id else {})
        self.message = message

class UserNotFoundError(NotFoundError):
    """User not found error"""
    
    def __init__(self, user_id: str = None, details: Optional[Dict[str, Any]] = None):
        message = f"User {user_id} not found" if user_id else "User not found"
        super().__init__(resource="User", details=details or {"user_id": user_id} if user_id else {})
        self.message = message

class BusinessOwnershipError(AuthorizationError):
    """Business ownership error"""
    
    def __init__(self, message: str = "You do not own this business", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, details=details)

class BusinessLogicError(BaseError):
    """Business logic validation error"""
    
    def __init__(self, message: str, error_code: str = "BUSINESS_LOGIC_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=error_code,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details or {}
        )

class ErrorHandler:
    """Centralized error handler"""
    
    @staticmethod
    def create_error_response(error: BaseError) -> JSONResponse:
        """Create standardized error response"""
        response_data = {
            "success": False,
            "error": {
                "code": error.code,
                "message": error.message,
                "details": error.details
            }
        }
        
        if settings.DEBUG:
            response_data["error"]["debug"] = {
                "status_code": error.status_code,
                "type": error.__class__.__name__
            }
        
        return JSONResponse(
            status_code=error.status_code,
            content=response_data
        )
    
    @staticmethod
    def handle_validation_error(exc: Exception) -> JSONResponse:
        """Handle validation errors"""
        return ErrorHandler.create_error_response(
            ValidationError(str(exc), details={"exception": str(exc)})
        )
    
    @staticmethod
    def handle_authentication_error(exc: Exception) -> JSONResponse:
        """Handle authentication errors"""
        return ErrorHandler.create_error_response(
            AuthenticationError(str(exc))
        )
    
    @staticmethod
    def handle_authorization_error(exc: Exception) -> JSONResponse:
        """Handle authorization errors"""
        return ErrorHandler.create_error_response(
            AuthorizationError(str(exc))
        )
    
    @staticmethod
    def handle_not_found_error(exc: Exception) -> JSONResponse:
        """Handle not found errors"""
        return ErrorHandler.create_error_response(
            NotFoundError(str(exc))
        )
    
    @staticmethod
    def handle_conflict_error(exc: Exception) -> JSONResponse:
        """Handle conflict errors"""
        return ErrorHandler.create_error_response(
            ConflictError(str(exc))
        )
    
    @staticmethod
    def handle_rate_limit_error(exc: Exception) -> JSONResponse:
        """Handle rate limit errors"""
        return ErrorHandler.create_error_response(
            RateLimitError(str(exc))
        )
    
    @staticmethod
    def handle_ai_service_error(exc: Exception) -> JSONResponse:
        """Handle AI service errors"""
        return ErrorHandler.create_error_response(
            AIServiceError(str(exc))
        )
    
    @staticmethod
    def handle_database_error(exc: Exception) -> JSONResponse:
        """Handle database errors"""
        return ErrorHandler.create_error_response(
            DatabaseError(str(exc))
        )
    
    @staticmethod
    def handle_general_error(exc: Exception) -> JSONResponse:
        """Handle general/unexpected errors"""
        return ErrorHandler.create_error_response(
            BaseError(
                message="An unexpected error occurred",
                code="INTERNAL_ERROR",
                details={"exception": str(exc)} if settings.DEBUG else {}
            )
        )

# Global error handler instance
error_handler = ErrorHandler()

# Helper function for validation errors
def raise_validation_error(message: str, field: str = None, details: Optional[Dict[str, Any]] = None):
    """Helper function to raise validation errors"""
    raise ValidationError(message=message, field=field, details=details)
