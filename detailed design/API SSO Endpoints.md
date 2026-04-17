# 🔗 SSO API Endpoints Specification

## Overview
This document defines the backend API endpoints required to support Google and Microsoft SSO authentication in the AI Marketing Command Center.

## 🛡️ Authentication Architecture

### Flow Summary
1. Frontend initiates OAuth flow with provider
2. Provider redirects to callback with authorization code
3. Backend exchanges code for access token
4. Backend fetches user profile from provider
5. Backend creates/updates user in database
6. Backend generates JWT token for frontend
7. Frontend stores JWT and user profile

## 📡 API Endpoints

### 1. OAuth Callback Handler

#### POST `/api/auth/{provider}/callback`
Handles OAuth callback from Google or Microsoft

**Parameters:**
- `provider` (path): "google" or "microsoft"

**Request Body:**
```json
{
  "code": "authorization_code_from_provider",
  "state": "csrf_state_token"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "token": "jwt_access_token",
    "refreshToken": "jwt_refresh_token",
    "user": {
      "id": "user_uuid",
      "email": "user@example.com",
      "name": "John Doe",
      "firstName": "John",
      "lastName": "Doe",
      "picture": "https://profile.url/photo.jpg",
      "provider": "google|microsoft",
      "providerId": "provider_user_id",
      "createdAt": "2024-01-01T00:00:00Z",
      "lastLogin": "2024-01-01T00:00:00Z"
    },
    "business": {
      "id": "business_uuid",
      "name": "Business Name",
      "industry": "Technology",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  }
}
```

**Error Responses:**
```json
// 400 Bad Request
{
  "success": false,
  "error": {
    "code": "INVALID_CODE",
    "message": "Authorization code is invalid or expired"
  }
}

// 401 Unauthorized  
{
  "success": false,
  "error": {
    "code": "OAUTH_FAILED",
    "message": "Failed to authenticate with provider"
  }
}

// 500 Internal Server Error
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Server error during authentication"
  }
}
```

### 2. Token Refresh

#### POST `/api/auth/refresh`
Refreshes JWT access token using refresh token

**Request Headers:**
```
Authorization: Bearer {refresh_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "token": "new_jwt_access_token",
    "refreshToken": "new_jwt_refresh_token",
    "expiresIn": 3600
  }
}
```

### 3. User Profile

#### GET `/api/auth/me`
Get current user profile

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "user_uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "firstName": "John",
    "lastName": "Doe",
    "picture": "https://profile.url/photo.jpg",
    "provider": "google|microsoft",
    "providerId": "provider_user_id",
    "createdAt": "2024-01-01T00:00:00Z",
    "lastLogin": "2024-01-01T00:00:00Z",
    "business": {
      "id": "business_uuid",
      "name": "Business Name",
      "industry": "Technology",
      "plan": "free|pro|enterprise",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 4. Sign Out

#### POST `/api/auth/signout`
Sign out user and invalidate tokens

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully signed out"
}
```

### 5. Email/Password Authentication (Fallback)

#### POST `/api/auth/login`
Traditional email/password authentication

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "user_password"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "token": "jwt_access_token",
    "refreshToken": "jwt_refresh_token",
    "user": {
      "id": "user_uuid",
      "email": "user@example.com",
      "name": "John Doe",
      "firstName": "John",
      "lastName": "Doe",
      "provider": "email",
      "createdAt": "2024-01-01T00:00:00Z",
      "lastLogin": "2024-01-01T00:00:00Z"
    }
  }
}
```

#### POST `/api/auth/register`
Register new user with email/password

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe",
  "business": {
    "name": "Business Name",
    "industry": "Technology"
  }
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "token": "jwt_access_token",
    "refreshToken": "jwt_refresh_token",
    "user": {
      "id": "user_uuid",
      "email": "user@example.com",
      "name": "John Doe",
      "firstName": "John",
      "lastName": "Doe",
      "provider": "email",
      "createdAt": "2024-01-01T00:00:00Z",
      "lastLogin": "2024-01-01T00:00:00Z"
    },
    "business": {
      "id": "business_uuid",
      "name": "Business Name",
      "industry": "Technology",
      "plan": "free",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  }
}
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    picture TEXT,
    provider VARCHAR(20) NOT NULL, -- 'google', 'microsoft', 'email'
    provider_id VARCHAR(255),
    password_hash VARCHAR(255), -- Only for email provider
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Businesses Table
```sql
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    plan VARCHAR(20) DEFAULT 'free', -- 'free', 'pro', 'enterprise'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Refresh Tokens Table
```sql
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 Security Implementation

### JWT Token Structure
```json
{
  "sub": "user_uuid",
  "email": "user@example.com",
  "provider": "google|microsoft|email",
  "businessId": "business_uuid",
  "iat": 1640995200,
  "exp": 1640998800,
  "iss": "ai-marketing-command-center",
  "aud": "ai-marketing-command-center-users"
}
```

### Security Headers
```http
Access-Control-Allow-Origin: https://yourdomain.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Rate Limiting
```python
# Recommended rate limits
RATE_LIMITS = {
    "/api/auth/login": "5/minute",
    "/api/auth/register": "3/minute", 
    "/api/auth/*/callback": "10/minute",
    "/api/auth/refresh": "20/minute"
}
```

## 🐍 Python Implementation (FastAPI Example)

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import httpx
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

# OAuth Provider Configuration
OAUTH_CONFIG = {
    "google": {
        "token_url": "https://oauth2.googleapis.com/token",
        "profile_url": "https://www.googleapis.com/oauth2/v2/userinfo",
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    },
    "microsoft": {
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "profile_url": "https://graph.microsoft.com/v1.0/me",
        "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
        "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET"),
    }
}

@app.post("/api/auth/{provider}/callback")
async def auth_callback(provider: str, request: OAuthCallbackRequest):
    if provider not in OAUTH_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid provider")
    
    config = OAUTH_CONFIG[provider]
    
    # Exchange authorization code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            config["token_url"],
            data={
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "code": request.code,
                "grant_type": "authorization_code",
                "redirect_uri": f"{os.getenv('APP_URL')}/auth/{provider}/callback"
            }
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=401, detail="OAuth token exchange failed")
        
        token_data = token_response.json()
        
        # Get user profile
        profile_response = await client.get(
            config["profile_url"],
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        
        if profile_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to fetch user profile")
        
        profile_data = profile_response.json()
    
    # Create/update user in database
    user = await create_or_update_user(provider, profile_data)
    
    # Generate JWT tokens
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    
    return {
        "success": True,
        "data": {
            "token": access_token,
            "refreshToken": refresh_token,
            "user": user.dict(),
            "business": user.business.dict() if user.business else None
        }
    }

async def create_or_update_user(provider: str, profile_data: dict):
    # Implementation for user creation/update logic
    pass

def generate_access_token(user: User):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "provider": user.provider,
        "businessId": str(user.business_id) if user.business_id else None,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "iss": "ai-marketing-command-center",
        "aud": "ai-marketing-command-center-users"
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")

def generate_refresh_token(user: User):
    # Generate secure refresh token and store in database
    pass
```

## 🧪 Testing

### Test Cases

1. **Successful Google OAuth Flow**
2. **Successful Microsoft OAuth Flow**
3. **Invalid Authorization Code**
4. **Expired Authorization Code**
5. **Token Refresh Success**
6. **Token Refresh with Invalid Token**
7. **User Profile Retrieval**
8. **Sign Out Success**
9. **Email/Password Login Success**
10. **Email/Password Login Failure**

### Example Test (Python)

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_google_oauth_callback():
    response = client.post(
        "/api/auth/google/callback",
        json={
            "code": "valid_authorization_code",
            "state": "valid_state_token"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data["data"]
    assert "user" in data["data"]
    assert data["data"]["user"]["provider"] == "google"

def test_invalid_oauth_code():
    response = client.post(
        "/api/auth/google/callback",
        json={
            "code": "invalid_code",
            "state": "valid_state_token"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "OAUTH_FAILED"
```

## 📊 Monitoring & Logging

### Key Metrics
- Authentication success rate by provider
- Token refresh success/failure rate
- User registration vs login ratio
- Authentication error frequency
- Response time for auth endpoints

### Logging Format
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "INFO|WARN|ERROR",
  "event": "auth_callback|token_refresh|user_login",
  "provider": "google|microsoft|email",
  "userId": "user_uuid",
  "success": true|false,
  "errorCode": "ERROR_CODE",
  "responseTime": 150,
  "userAgent": "Mozilla/5.0...",
  "ipAddress": "192.168.1.1"
}
```

---

## 📝 Implementation Checklist

### Backend Development
- [ ] Set up OAuth provider credentials
- [ ] Implement token exchange logic
- [ ] Create user management system
- [ ] Add JWT token generation/validation
- [ ] Implement refresh token mechanism
- [ ] Add proper error handling
- [ ] Set up rate limiting
- [ ] Add comprehensive logging
- [ ] Write unit tests
- [ ] Configure security headers

### Security Review
- [ ] Validate all inputs
- [ ] Implement proper CORS
- [ ] Use HTTPS in production
- [ ] Secure token storage
- [ ] Implement rate limiting
- [ ] Add audit logging
- [ ] Test for common vulnerabilities
- [ ] Review OAuth implementation
- [ ] Validate JWT configuration

### Deployment
- [ ] Configure environment variables
- [ ] Set up database migrations
- [ ] Configure monitoring
- [ ] Test end-to-end flows
- [ ] Set up backup procedures
- [ ] Document API endpoints
- [ ] Create troubleshooting guide
- [ ] Plan disaster recovery
