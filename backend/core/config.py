"""Core Configuration Module - Enhanced for System Architecture
Centralized configuration management with comprehensive settings"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from pathlib import Path

class Settings(BaseSettings):
    """Application Settings - Production Ready Configuration"""
    
    # Application Core
    APP_NAME: str = "Omni Mind"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    PORT: int = Field(default=8000, env="PORT")
    FRONTEND_URL: str = Field(default="http://localhost:3000", env="FRONTEND_URL")
    
    # Database Configuration (SQLite)
    DATABASE_URL: str = Field(default="sqlite:///./aimarketing.db", env="DATABASE_URL")
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Security Configuration
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production-must-be-at-least-32-chars", env="SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI Service Configuration
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(default="", env="ANTHROPIC_API_KEY")
    DEFAULT_AI_MODEL: str = "gpt-4o-mini"
    FALLBACK_AI_MODEL: str = "gpt-3.5-turbo"
    AI_TIMEOUT_SECONDS: int = 30
    AI_MAX_RETRIES: int = 3
    AI_REQUEST_DELAY: float = 0.5
    MAX_TOKENS_PER_REQUEST: int = 4000
    
    # Rate Limiting Configuration
    RATE_LIMIT_PER_MINUTE: int = 60
    AI_RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_BURST_SIZE: int = 10
    
    # Business Logic Limits
    MAX_BUSINESSES_PER_USER: int = 5
    MAX_CAMPAIGNS_PER_BUSINESS: int = 20
    MAX_CONTENT_PIECES_PER_CAMPAIGN: int = 50
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: List[str] = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"]
    UPLOAD_DIR: str = "uploads"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(default=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ])
    
    @property
    def get_allowed_origins(self) -> List[str]:
        """Get CORS allowed origins including FRONTEND_URL and Railway domain"""
        origins = self.ALLOWED_ORIGINS.copy()
        if self.FRONTEND_URL and self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)
        # Auto-add Railway domain if deployed there
        import os
        railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
        if railway_domain:
            for scheme in ("https://", "http://"):
                url = f"{scheme}{railway_domain}"
                if url not in origins:
                    origins.append(url)
        return origins
    
    # Monitoring and Performance
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    HEALTH_CHECK_TIMEOUT: float = 5.0
    
    # Cache Configuration (Future)
    CACHE_TTL_SECONDS: int = 300
    ENABLE_CACHING: bool = False
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Email Configuration (Optional)
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: Optional[int] = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_USE_TLS: bool = True
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_SECRET")
    MICROSOFT_CLIENT_ID: Optional[str] = Field(default=None, env="MICROSOFT_CLIENT_ID")
    MICROSOFT_CLIENT_SECRET: Optional[str] = Field(default=None, env="MICROSOFT_CLIENT_SECRET")
    OAUTH_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    
    # Background Job Configuration (Future)
    ENABLE_BACKGROUND_JOBS: bool = False
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND")
    
    # Content Generation Configuration
    CONTENT_GENERATION_TIMEOUT: int = 60  # seconds
    BATCH_SIZE_LIMIT: int = 10
    
    @validator('SECRET_KEY')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError('Secret key must be at least 32 characters long')
        return v
    
    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        if not v:
            raise ValueError('Database URL is required')
        return v
    
    def get_database_path(self) -> Optional[Path]:
        """Get the database file path for SQLite"""
        if self.DATABASE_URL.startswith('sqlite:///'):
            db_path = self.DATABASE_URL.replace('sqlite:///', '')
            if not db_path.startswith('/'):
                return Path.cwd() / db_path
            return Path(db_path)
        return None
    
    def ensure_directories(self):
        """Ensure required directories exist"""
        # Upload directory
        upload_path = Path(self.UPLOAD_DIR)
        upload_path.mkdir(exist_ok=True)
        
        # Database directory for SQLite
        db_path = self.get_database_path()
        if db_path:
            db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT.lower() == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT.lower() == 'development'
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

# Global settings instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()