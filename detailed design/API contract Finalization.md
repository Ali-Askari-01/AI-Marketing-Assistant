We will define:

Standard response structure

Standard error structure

Auth endpoints

Business endpoints

Campaign endpoints

Content endpoints

Analytics endpoints

Messaging endpoints

No implementation yet. Only contract.

🧱 2.1 GLOBAL RESPONSE FORMAT (MANDATORY)

Every success response must follow:

{
  "success": true,
  "data": { ... },
  "meta": { ... } // optional
}

Every error response:

{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}

We NEVER return raw exceptions.

🔐 2.2 AUTH API
1️⃣ Register

POST /api/v1/auth/register

Request:

{
  "email": "user@example.com",
  "password": "string_min_8"
}

Response:

{
  "success": true,
  "data": {
    "user_id": "uuid",
    "access_token": "jwt_token"
  }
}

Errors:

EMAIL_ALREADY_EXISTS

INVALID_PASSWORD

2️⃣ Login

POST /api/v1/auth/login

Request:

{
  "email": "user@example.com",
  "password": "string"
}

Response:

{
  "success": true,
  "data": {
    "user_id": "uuid",
    "access_token": "jwt_token"
  }
}

Errors:

INVALID_CREDENTIALS

🏢 2.3 BUSINESS API
3️⃣ Create Business

POST /api/v1/business

Request:

{
  "name": "FitLife Gym",
  "industry": "Fitness",
  "target_audience": "Young professionals",
  "brand_tone": "Motivational",
  "primary_goal": "Lead Generation"
}

Response:

{
  "success": true,
  "data": {
    "business_id": "uuid",
    "created_at": "timestamp"
  }
}
4️⃣ Get All Businesses

GET /api/v1/business

Response:

{
  "success": true,
  "data": [
    {
      "business_id": "uuid",
      "name": "FitLife Gym",
      "industry": "Fitness"
    }
  ]
}
📅 2.4 CAMPAIGN API
5️⃣ Generate Campaign Strategy (AI)

POST /api/v1/campaign/generate

Request:

{
  "business_id": "uuid",
  "duration_days": 30
}

Response:

{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "calendar": [
      {
        "day": 1,
        "theme": "Transformation Story",
        "content_type": "Reel"
      }
    ]
  }
}

Errors:

BUSINESS_NOT_FOUND

AI_GENERATION_FAILED

6️⃣ Get Campaign Details

GET /api/v1/campaign/{campaign_id}

Response:

{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "business_id": "uuid",
    "calendar": [...],
    "created_at": "timestamp"
  }
}
✍ 2.5 CONTENT API
7️⃣ Generate Content (AI)

POST /api/v1/content/generate

Request:

{
  "campaign_id": "uuid",
  "day": 1,
  "content_type": "Reel"
}

Response:

{
  "success": true,
  "data": {
    "content_id": "uuid",
    "caption": "Your transformation starts today...",
    "hashtags": ["#fitness", "#gym"],
    "script": "Hook... Body... CTA...",
    "estimated_engagement_score": 82
  }
}

Errors:

CAMPAIGN_NOT_FOUND

INVALID_CONTENT_TYPE

AI_GENERATION_FAILED

8️⃣ Schedule Content

POST /api/v1/content/schedule

Request:

{
  "content_id": "uuid",
  "scheduled_at": "timestamp"
}

Response:

{
  "success": true,
  "data": {
    "status": "scheduled"
  }
}
📊 2.6 ANALYTICS API
9️⃣ Get Business Analytics

GET /api/v1/analytics/{business_id}

Response:

{
  "success": true,
  "data": {
    "health_score": 78,
    "engagement_rate": 4.2,
    "top_content_type": "Reel",
    "recommendations": [
      "Post more video content",
      "Increase CTA strength"
    ]
  }
}
💬 2.7 MESSAGING API
🔟 Generate Reply Suggestion (AI)

POST /api/v1/message/reply

Request:

{
  "business_id": "uuid",
  "customer_message": "How much is membership?"
}

Response:

{
  "success": true,
  "data": {
    "suggested_reply": "Thanks for reaching out! Our membership starts at..."
  }
}
🔒 2.8 AUTHORIZATION RULES

Every endpoint except auth must:

Require JWT

Validate business ownership

Return 403 if user does not own resource

📏 2.9 STATUS CODE POLICY

200 → Success
201 → Resource Created
400 → Validation Error
401 → Unauthorized
403 → Forbidden
404 → Not Found
429 → Rate Limited
500 → Internal Error

No random codes.