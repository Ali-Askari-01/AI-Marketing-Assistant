🚀 ITERATION 3 — DATABASE SCHEMA FINALIZATION (SQLite)

Since SQLite is document-based, we must design:

🔹 Proper document boundaries

🔹 References vs Embedding strategy

🔹 Indexing strategy

🔹 Scalability consideration

🔹 AI logs separation

🔹 Analytics modeling

🧠 DATABASE DESIGN PRINCIPLES (For Your AI Marketing SaaS)
We will use:

Reference pattern for large entities (User → Business → Campaign → Content)

Embedding pattern for small frequently-read objects (AI metadata inside content)

Separate AI logs collection for monitoring

Analytics decoupled from content

📦 COLLECTION STRUCTURE OVERVIEW

You will have these collections:

users

businesses

campaigns

contents

analytics

messages

ai_logs

scheduled_jobs (optional for future async)

1️⃣ USERS COLLECTION
Collection: users
{
  "_id": ObjectId,
  "email": "founder@email.com",
  "password_hash": "hashed_password",
  "full_name": "Ali Askari",
  "role": "owner", 
  "is_active": true,
  "created_at": ISODate,
  "updated_at": ISODate
}
Indexes:

unique index on email

index on created_at

Notes:

No business embedded (user may own multiple businesses)

Lightweight document

2️⃣ BUSINESSES COLLECTION
Collection: businesses
{
  "_id": ObjectId,
  "owner_id": ObjectId,   // reference to users
  "name": "Ali Fitness Studio",
  "industry": "Fitness",
  "description": "Gym focused on weight loss",
  "target_audience": {
      "age_range": "18-35",
      "gender_focus": "All",
      "location": "Karachi",
      "interests": ["Fitness", "Diet", "Weight Loss"]
  },
  "brand_voice": "Motivational, Energetic",
  "content_preferences": {
      "platforms": ["Instagram", "TikTok"],
      "tone": "Friendly",
      "post_frequency_per_week": 4
  },
  "created_at": ISODate,
  "updated_at": ISODate
}
Indexes:

index on owner_id

compound index on industry + created_at

3️⃣ CAMPAIGNS COLLECTION
Collection: campaigns
{
  "_id": ObjectId,
  "business_id": ObjectId,
  "name": "30 Day Fitness Transformation",
  "goal": "Increase membership signups",
  "duration_days": 30,
  "strategy_summary": "Content focused on transformation journeys",
  "content_calendar": [
    {
      "day": 1,
      "content_type": "Reel",
      "theme": "Before/After"
    }
  ],
  "status": "active", 
  "start_date": ISODate,
  "end_date": ISODate,
  "created_at": ISODate
}
Why embed content_calendar?

It's relatively small

Frequently read together

Reduces joins

Indexes:

index on business_id

index on status

4️⃣ CONTENTS COLLECTION
Collection: contents

This is the core collection.

{
  "_id": ObjectId,
  "campaign_id": ObjectId,
  "business_id": ObjectId,
  "day": 1,
  "platform": "Instagram",
  "content_type": "Reel",
  "caption": "Your transformation starts today 💪",
  "hashtags": ["#fitness", "#weightloss"],
  "media": {
      "image_url": "https://...",
      "video_url": "https://...",
      "thumbnail_url": "https://..."
  },
  "script": "Scene 1: Show gym intro...",
  "status": "draft",   // draft | approved | scheduled | published
  "scheduled_at": ISODate,
  "ai_metadata": {
      "model_used": "gpt-4o",
      "tokens_used": 850,
      "generation_time_ms": 2300
  },
  "created_at": ISODate,
  "updated_at": ISODate
}
Why separate collection?

Content grows very large

Can scale independently

Queryable by status

Enables analytics linking

Indexes:

index on campaign_id

index on business_id

index on status

index on scheduled_at

5️⃣ ANALYTICS COLLECTION

Separate from content for scalability.

{
  "_id": ObjectId,
  "content_id": ObjectId,
  "platform": "Instagram",
  "metrics": {
      "likes": 1200,
      "comments": 85,
      "shares": 42,
      "views": 5500,
      "engagement_rate": 4.5
  },
  "predicted_performance": {
      "score": 82,
      "confidence": 0.76
  },
  "collected_at": ISODate
}
Indexes:

index on content_id

index on collected_at

6️⃣ MESSAGES COLLECTION (AI Auto Reply)
{
  "_id": ObjectId,
  "business_id": ObjectId,
  "platform": "Instagram",
  "incoming_message": "What are your charges?",
  "generated_reply": "Our monthly package starts at...",
  "confidence_score": 0.92,
  "status": "sent",
  "created_at": ISODate
}
7️⃣ AI_LOGS COLLECTION (CRITICAL)

Keep AI monitoring separate.

{
  "_id": ObjectId,
  "user_id": ObjectId,
  "feature": "campaign_generation",
  "model_used": "gpt-4o",
  "tokens_used": 1520,
  "input_prompt_hash": "abc123hash",
  "status": "success",
  "error_message": null,
  "response_time_ms": 3120,
  "created_at": ISODate
}
Indexes:

index on user_id

index on feature

index on created_at

index on status

🔥 EMBEDDING VS REFERENCING STRATEGY SUMMARY
Entity	Strategy	Reason
Target Audience	Embedded	Small, fixed
Content Calendar	Embedded	Always read with campaign
Media URLs	Embedded	Small
Analytics	Referenced	Large, grows
AI Logs	Separate	Monitoring
Content	Separate	Heavy & scalable
📈 SCALABILITY DESIGN

Your system will scale like this:

Content grows → separate collection

Analytics grows → separate collection

AI logs grow → separate collection

Businesses isolated via owner_id

SQLite handles horizontal scaling easily later.

🛡 DATA VALIDATION STRATEGY

Use:

Pydantic models in FastAPI

JSON schema validation

Enum types for:

status

platform

content_type

⚡ FUTURE READY EXTENSIONS

You can later add:

vector_embeddings collection (for semantic search)

billing collection

subscription_plans

notifications collection

🎯 ADVANCED SCHEMA FEATURES & IMPLEMENTATION

## 🔥 ADVANCED SQLite FEATURES

### 1️⃣ AGGREGATION PIPELINE OPTIMIZATIONS

```javascript
// Campaign Performance Analytics
db.contents.aggregate([
  { $match: { campaign_id: ObjectId("...") } },
  { $lookup: { 
      from: "analytics", 
      localField: "_id", 
      foreignField: "content_id", 
      as: "performance" 
  }},
  { $group: {
      _id: "$platform",
      total_content: { $sum: 1 },
      avg_engagement: { $avg: "$performance.engagement" },
      best_performing: { $max: "$performance.engagement" }
  }}
])

// AI Cost Analysis by Business
db.ai_logs.aggregate([
  { $match: { created_at: { $gte: new Date("2026-01-01") } } },
  { $group: {
      _id: { business_id: "$business_id", feature: "$feature" },
      total_tokens: { $sum: "$tokens_used" },
      total_cost: { $sum: "$cost_usd" },
      avg_response_time: { $avg: "$response_time_ms" }
  }},
  { $sort: { total_cost: -1 } }
])
```

### 2️⃣ COMPOUND INDEXING STRATEGY

```javascript
// High-performance indexes
db.contents.createIndex({ 
    "business_id": 1, 
    "status": 1, 
    "scheduled_date": 1 
})

db.analytics.createIndex({ 
    "business_id": 1, 
    "date": -1, 
    "platform": 1 
})

db.ai_logs.createIndex({ 
    "user_id": 1, 
    "created_at": -1, 
    "feature": 1 
})

// Text search indexes
db.contents.createIndex({ 
    "text_content": "text", 
    "caption": "text",
    "hashtags": "text" 
})
```

### 3️⃣ CHANGE STREAMS FOR REAL-TIME UPDATES

```javascript
// Real-time campaign monitoring
db.contents.watch([
  { $match: { "fullDocument.status": "published" } }
]).on('change', (change) => {
  // Trigger analytics collection
  // Update dashboard metrics
  // Send notifications
})
```

## 🚀 REPOSITORY PATTERN IMPLEMENTATION

### Base Repository Interface
```python
class BaseRepository:
    async def create(self, data: dict) -> str
    async def get_by_id(self, id: str) -> Optional[dict]
    async def update(self, id: str, data: dict) -> bool
    async def delete(self, id: str) -> bool
    async def find(self, query: dict, limit: int = 100) -> List[dict]
    async def count(self, query: dict) -> int
    async def aggregate(self, pipeline: List[dict]) -> List[dict]
```

### Specialized Repositories
```python
class CampaignRepository(BaseRepository):
    async def get_active_campaigns(self, business_id: str)
    async def get_performance_summary(self, campaign_id: str)
    async def archive_old_campaigns(self, days: int = 90)
    
class ContentRepository(BaseRepository):
    async def get_scheduled_content(self, date_range: tuple)
    async def publish_content(self, content_id: str)
    async def get_content_by_platform(self, business_id: str, platform: str)
    
class AnalyticsRepository(BaseRepository):
    async def record_engagement(self, content_id: str, metrics: dict)
    async def get_business_insights(self, business_id: str, period: str)
    async def compare_campaign_performance(self, campaign_ids: List[str])
```

## 📊 ADVANCED ANALYTICS SCHEMA

### Enhanced Analytics Collection
```javascript
{
  "_id": ObjectId,
  "content_id": ObjectId,
  "business_id": ObjectId,
  "campaign_id": ObjectId,
  "date": ISODate,
  "platform": "instagram",
  
  // Core Metrics
  "metrics": {
    "impressions": 5420,
    "reach": 4180,
    "engagement": 425,
    "likes": 380,
    "comments": 32,
    "shares": 13,
    "saves": 67,
    "clicks": 89,
    "profile_visits": 23,
    "website_clicks": 15
  },
  
  // Advanced Analytics
  "audience_insights": {
    "top_locations": ["Karachi", "Lahore", "Islamabad"],
    "age_groups": {
      "18-24": 0.35,
      "25-34": 0.45,
      "35-44": 0.20
    },
    "gender_split": {
      "male": 0.52,
      "female": 0.48
    },
    "peak_engagement_hours": [19, 20, 21]
  },
  
  // AI Predictions
  "ai_insights": {
    "performance_score": 8.4,
    "trending_probability": 0.73,
    "optimal_posting_time": "19:30",
    "content_suggestions": [
      "Add more user-generated content",
      "Include trending hashtags: #fitnessjourney"
    ],
    "competitor_comparison": {
      "vs_industry_average": 1.34,
      "performance_percentile": 78
    }
  },
  
  // Attribution & ROI
  "attribution": {
    "direct_conversions": 3,
    "assisted_conversions": 7,
    "revenue_generated": 850.0,
    "cost_per_acquisition": 28.33,
    "roi_percentage": 240
  },
  
  "created_at": ISODate,
  "updated_at": ISODate
}
```

## 🔄 WORKFLOW & STATE MANAGEMENT

### Campaign Lifecycle States
```javascript
{
  "campaign_states": {
    "draft": ["active", "archived"],
    "active": ["paused", "completed", "archived"],
    "paused": ["active", "completed", "archived"],
    "completed": ["archived", "reactivated"],
    "archived": ["reactivated"]
  }
}

// State transition validation
function validateStateTransition(currentState, newState) {
  const allowedStates = campaign_states[currentState] || []
  return allowedStates.includes(newState)
}
```

### Content Publishing Pipeline
```javascript
{
  "content_pipeline": [
    "draft",           // AI generated or manually created
    "review",          // Human review required
    "approved",        // Ready for scheduling
    "scheduled",       // Queued for publication
    "publishing",      // Currently being published
    "published",       // Live on platform
    "archived"         // Moved to archive
  ]
}
```

## 🛡️ DATA VALIDATION & CONSTRAINTS

### Schema Validators
```javascript
// Business profile validator
{
  $jsonSchema: {
    bsonType: "object",
    required: ["owner_id", "name", "industry"],
    properties: {
      industry: {
        enum: ["Technology", "Healthcare", "Fitness", "Retail", "Education", "Food", "Travel", "Finance"]
      },
      plan: {
        enum: ["free", "pro", "enterprise"]
      },
      content_preferences: {
        bsonType: "object",
        properties: {
          platforms: {
            bsonType: "array",
            items: {
              enum: ["instagram", "linkedin", "twitter", "tiktok", "youtube", "email", "sms"]
            }
          }
        }
      }
    }
  }
}

// Content validator
{
  $jsonSchema: {
    bsonType: "object",
    required: ["campaign_id", "business_id", "content_type", "platform"],
    properties: {
      content_type: {
        enum: ["post", "story", "reel", "carousel", "video", "live", "email", "sms"]
      },
      platform: {
        enum: ["instagram", "linkedin", "twitter", "tiktok", "youtube", "email", "sms"]
      },
      status: {
        enum: ["draft", "review", "approved", "scheduled", "published", "failed", "archived"]
      }
    }
  }
}
```

## 🔍 SEARCH & DISCOVERY FEATURES

### Full-Text Search Implementation
```javascript
// Content search index
db.contents.createIndex({
  "text_content": "text",
  "hashtags": "text", 
  "title": "text"
}, {
  weights: {
    "title": 10,
    "text_content": 5,
    "hashtags": 1
  }
})

// Search campaigns by content
db.contents.find({
  $text: {
    $search: "fitness transformation weight loss",
    $caseSensitive: false
  }
})
```

### Vector Embeddings for Semantic Search
```javascript
// Future: Add vector embeddings collection
{
  "_id": ObjectId,
  "content_id": ObjectId,
  "embedding_vector": [0.123, -0.456, 0.789, ...], // 1536 dimensions
  "embedding_model": "text-embedding-ada-002",
  "created_at": ISODate
}

// Vector similarity search
db.embeddings.aggregate([
  {
    $vectorSearch: {
      queryVector: [0.1, 0.2, 0.3, ...],
      path: "embedding_vector",
      numCandidates: 100,
      limit: 10,
      index: "vector_index"
    }
  }
])
```

## 📈 PERFORMANCE OPTIMIZATION

### Query Optimization Patterns
```javascript
// Use projection to reduce bandwidth
db.contents.find(
  { business_id: ObjectId("...") },
  { _id: 1, title: 1, status: 1, created_at: 1 }
)

// Use aggregation for complex queries
db.campaigns.aggregate([
  { $match: { business_id: ObjectId("...") } },
  { $lookup: {
      from: "contents",
      localField: "_id",
      foreignField: "campaign_id",
      as: "content_count",
      pipeline: [{ $count: "total" }]
  }},
  { $addFields: {
      content_count: { $arrayElemAt: ["$content_count.total", 0] }
  }}
])
```

### Caching Strategy
```javascript
// Redis caching patterns
{
  "user_sessions": "user:{user_id}:session",
  "business_cache": "business:{business_id}:profile",
  "campaign_stats": "campaign:{campaign_id}:stats:24h",
  "content_schedule": "schedule:{business_id}:{date}",
  "ai_rate_limits": "ai:ratelimit:{user_id}:{feature}"
}
```

## 🔄 DATA LIFECYCLE MANAGEMENT

### Automated Data Archival
```javascript
// Archive old content after 1 year
db.contents.updateMany(
  { 
    created_at: { $lt: new Date(Date.now() - 365*24*60*60*1000) },
    status: "published"
  },
  { 
    $set: { 
      status: "archived",
      archived_at: new Date()
    }
  }
)

// Move analytics to cold storage after 6 months
db.analytics.find({
  created_at: { $lt: new Date(Date.now() - 180*24*60*60*1000) }
}).forEach(doc => {
  db.analytics_archive.insertOne(doc)
  db.analytics.deleteOne({ _id: doc._id })
})
```

## 🚨 BACKUP & DISASTER RECOVERY

### Backup Strategy
```bash
# Daily automated backups
sqlitedump --uri="SQLite://..." --db=aimarketing --out=/backups/$(date +%Y%m%d)

# Point-in-time recovery setup
sqlited --replSet=rs0 --oplogSize=1024

# Cross-region replication
rs.add("backup-server:27017")
```

### Data Recovery Procedures
```javascript
// Restore deleted campaign
db.campaigns_trash.findOne({ original_id: ObjectId("...") })

// Rollback content changes
db.contents.findOne({ _id: ObjectId("..."), version: "previous" })

// Audit trail query
db.audit_logs.find({
  entity_type: "campaign",
  entity_id: ObjectId("..."),
  action: { $in: ["update", "delete"] }
}).sort({ timestamp: -1 })
```

🎯 FINAL ARCHITECTURAL VALIDATION

This SQLite schema is:

✅ Fully normalized where required
✅ Optimized for reads
✅ AI monitoring ready
✅ Content heavy friendly
✅ Hackathon + production ready
✅ Supports image + video generation
✅ Async-ready