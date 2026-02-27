# Automated API Contract Tests

> Updated: Feb 2026 — aligned with running backend endpoints

## Test Environment

| Setting       | Value                                      |
| ------------- | ------------------------------------------ |
| Backend URL   | `http://localhost:8003`                    |
| API Base      | `/api/v1`                                  |
| Business ID   | `demo`                                     |
| Auth          | Bearer token (JWT) where required          |
| Runner        | PowerShell `Invoke-WebRequest` / curl       |

---

## 1 · Health & System Endpoints

### 1.1 Root / Docs
| # | Method | URL            | Expected Status | Assertion                        |
|---|--------|----------------|-----------------|----------------------------------|
| 1 | GET    | `/`            | 200             | Returns HTML landing page        |
| 2 | GET    | `/docs`        | 200             | FastAPI Swagger UI loads          |
| 3 | GET    | `/health`      | 200             | `{ "status": "healthy" }`        |

---

## 2 · Authentication Endpoints

### 2.1 Login / Register
| # | Method | URL                  | Body                                                   | Expected | Assertion                              |
|---|--------|----------------------|--------------------------------------------------------|----------|----------------------------------------|
| 4 | POST   | `/api/v1/auth/login` | `{ "email":"admin@demo.com","password":"demo123" }`    | 200      | Returns `access_token` string          |
| 5 | POST   | `/api/v1/auth/login` | Missing password                                       | 422      | Validation error                       |
| 6 | POST   | `/api/v1/auth/register` | `{ "email":"new@test.com","password":"Test12345","name":"Tester" }` | 200/201 | Returns user object or token |

### 2.2 SSO Endpoints
| # | Method | URL                           | Expected | Assertion                              |
|---|--------|-------------------------------|----------|----------------------------------------|
| 7 | GET    | `/api/v1/sso/google/login`    | 200/302  | Returns OAuth URL or redirect          |
| 8 | GET    | `/api/v1/sso/facebook/login`  | 200/302  | Returns OAuth URL or redirect          |

---

## 3 · AI Endpoints

### 3.1 Caption Generation
| # | Method | URL                              | Body                                                       | Expected | Assertion                      |
|---|--------|----------------------------------|------------------------------------------------------------|----------|-------------------------------|
| 9 | POST   | `/api/v1/ai/generate-captions`   | `{ "topic":"Summer Sale", "platform":"instagram" }`        | 200      | Returns `captions` array       |
| 10| POST   | `/api/v1/ai/generate-captions`   | `{}`  (missing topic)                                      | 422      | Validation error               |

### 3.2 Hashtag Optimization
| # | Method | URL                              | Body                                                       | Expected | Assertion                      |
|---|--------|----------------------------------|------------------------------------------------------------|----------|-------------------------------|
| 11| POST   | `/api/v1/ai/optimize-hashtags`   | `{ "topic":"fitness", "platform":"instagram" }`            | 200      | Returns hashtag suggestions    |

### 3.3 Post Analysis
| # | Method | URL                          | Body                                                           | Expected | Assertion                      |
|---|--------|------------------------------|----------------------------------------------------------------|----------|-------------------------------|
| 12| POST   | `/api/v1/ai/analyze-post`    | `{ "content":"Check out our new product!", "platform":"instagram" }` | 200 | Returns analysis object        |

### 3.4 Strategy Agent
| # | Method | URL                                  | Body                                                       | Expected | Assertion                             |
|---|--------|--------------------------------------|------------------------------------------------------------|----------|--------------------------------------|
| 13| POST   | `/api/v1/agent/generate-strategy`    | `{ "business_type":"SaaS", "goals":["brand awareness"] }`  | 200      | Returns strategy with `daily_plan`    |
| 14| POST   | `/api/v1/campaign/generate-strategy` | `{ "business_type":"ecommerce", "goals":["sales"] }`       | 200      | Returns strategy object               |

### 3.5 AI Chat / Ask
| # | Method | URL                    | Body                                                   | Expected | Assertion                      |
|---|--------|------------------------|--------------------------------------------------------|----------|-------------------------------|
| 15| POST   | `/api/v1/agent/ask`    | `{ "question":"How do I improve Instagram engagement?" }` | 200   | Non-empty response text        |

---

## 4 · Inbox / Messaging Endpoints

### 4.1 Thread Listing
| # | Method | URL                                             | Expected | Assertion                                          |
|---|--------|------------------------------------------------|----------|----------------------------------------------------|
| 16| GET    | `/api/v1/inbox/threads?business_id=demo`        | 200      | Returns `threads` array with >= 5 items             |
| 17| GET    | `/api/v1/inbox/threads?business_id=demo&platform=instagram` | 200 | All threads have `platform == "instagram"`  |
| 18| GET    | `/api/v1/inbox/threads?business_id=demo&search=Sarah` | 200 | At least 1 thread with "Sarah" in customer_name    |

### 4.2 Thread Detail
| # | Method | URL                                          | Expected | Assertion                                          |
|---|--------|---------------------------------------------|----------|----------------------------------------------------|
| 19| GET    | `/api/v1/inbox/threads/thread_sarah`         | 200      | Returns `messages` array, `customer_name == "Sarah Kim"` |
| 20| GET    | `/api/v1/inbox/threads/nonexistent_id`       | 404      | Error response                                      |

### 4.3 Send Reply
| # | Method | URL                                          | Body                           | Expected | Assertion                        |
|---|--------|---------------------------------------------|--------------------------------|----------|----------------------------------|
| 21| POST   | `/api/v1/inbox/threads/thread_sarah/reply`   | `{ "content":"Thanks!" }`      | 200      | Returns sent message object       |
| 22| POST   | `/api/v1/inbox/threads/thread_sarah/reply`   | `{}`                           | 422      | Validation error (missing content)|

### 4.4 AI Reply Suggestions
| # | Method | URL                                              | Expected | Assertion                                    |
|---|--------|--------------------------------------------------|----------|----------------------------------------------|
| 23| POST   | `/api/v1/inbox/threads/thread_sarah/ai-suggest`  | 200      | Returns `suggestions` array with >= 1 item     |

### 4.5 Thread Update (Archive/Flag)
| # | Method | URL                                          | Body                          | Expected | Assertion                        |
|---|--------|---------------------------------------------|-------------------------------|----------|----------------------------------|
| 24| PATCH  | `/api/v1/inbox/threads/thread_sarah`         | `{ "is_flagged": true }`       | 200      | Thread updated                    |
| 25| PATCH  | `/api/v1/inbox/threads/thread_mike`          | `{ "is_archived": true }`      | 200      | Thread archived                   |

### 4.6 Inbox Stats
| # | Method | URL                          | Expected | Assertion                                          |
|---|--------|------------------------------|----------|----------------------------------------------------|
| 26| GET    | `/api/v1/inbox/stats`        | 200      | `total_messages > 0`, has `by_platform` object      |

---

## 5 · Social Publishing Endpoints

| # | Method | URL                                      | Body / Params                                      | Expected | Assertion                      |
|---|--------|------------------------------------------|----------------------------------------------------|----------|-------------------------------|
| 27| GET    | `/api/v1/social/accounts`                | —                                                   | 200      | Returns array of social accounts |
| 28| POST   | `/api/v1/social/publish`                 | `{ "platform":"instagram", "content":"test" }`      | 200      | Returns publish result          |
| 29| GET    | `/api/v1/social/post-history`            | —                                                   | 200      | Returns post history array      |

---

## 6 · Campaign & Content Endpoints

| # | Method | URL                              | Body                                                       | Expected | Assertion                      |
|---|--------|----------------------------------|------------------------------------------------------------|----------|-------------------------------|
| 30| GET    | `/api/v1/campaigns`              | —                                                          | 200      | Returns campaigns list          |
| 31| POST   | `/api/v1/campaigns`              | `{ "name":"Test Campaign", "platform":"instagram" }`       | 200/201  | Campaign created                |
| 32| GET    | `/api/v1/content/library`        | —                                                          | 200      | Returns content array           |

---

## 7 · Analytics Endpoints

| # | Method | URL                                      | Expected | Assertion                              |
|---|--------|------------------------------------------|----------|----------------------------------------|
| 33| GET    | `/api/v1/analytics/dashboard`            | 200      | Returns analytics summary object        |
| 34| GET    | `/api/v1/analytics/engagement`           | 200      | Returns engagement metrics              |

---

## 8 · File Upload Endpoints

| # | Method | URL                      | Body                    | Expected | Assertion                      |
|---|--------|--------------------------|-------------------------|----------|-------------------------------|
| 35| POST   | `/api/v1/upload`         | Multipart form (image)  | 200      | Returns file URL               |

---

## 9 · Error & Edge Case Tests

| # | Test                                | URL                              | Expected | Assertion                      |
|---|-------------------------------------|----------------------------------|----------|-------------------------------|
| 36| Unknown endpoint                   | `/api/v1/nonexistent`            | 404      | Not found error                 |
| 37| Wrong HTTP method                  | PUT `/api/v1/inbox/stats`        | 405      | Method not allowed              |
| 38| Invalid JSON body                  | POST `/api/v1/ai/generate-captions` with `{bad` | 422 | JSON parse error         |
| 39| CORS headers present               | OPTIONS `/api/v1/inbox/threads`  | 200      | `Access-Control-Allow-Origin` header exists |

---

## Response Format Contract

All successful responses must follow:
```json
{
  "success": true,
  "data": { ... },
  "message": "Human-readable message"
}
```

All error responses must follow:
```json
{
  "success": false,
  "error": "error_code",
  "message": "Human-readable error",
  "details": { ... }
}
```

---

## Execution Script

See `test-runner.ps1` in the same directory for the automated PowerShell test runner.
