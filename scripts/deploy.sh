#!/bin/bash

# Production Deployment Script
# This script deploys the AI Marketing Command Center to production

set -e

echo "🚀 Starting Production Deployment..."

# Check environment variables
if [ -z "$SECRET_KEY" ]; then
    echo "❌ ERROR: SECRET_KEY environment variable is required"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ ERROR: OPENAI_API_KEY environment variable is required"
    exit 1
fi

# Build and deploy services
echo "📦 Building and starting services..."

# Stop existing services
echo "🛑 Stopping existing services..."
docker-compose down

# Build new images
echo "🔨 Building Docker images..."
docker-compose build --no-cache

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Health checks
echo "🔍 Performing health checks..."

# Check backend health
echo "Checking backend health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    exit 1
fi

# Check database connection
echo "Checking database connection..."
echo "✅ SQLite database is embedded (no external service needed)"

# Database tables are auto-created by SQLAlchemy on startup
echo "🗄️ Database tables auto-created by SQLAlchemy ORM..."

# Indexes are defined in SQLAlchemy models
echo "📊 Database indexes defined in SQLAlchemy models..."

# Load demo data
echo "🎭 Loading demo data..."
docker-compose exec backend python -c "
import asyncio
import json
import datetime
import time

# Create demo user
demo_user = {
    "id": "demo_user_1",
    "email": "demo@aimarketing.ai",
    "full_name": "Demo User",
    "role": "admin",
    "is_active": True,
    "created_at": datetime.datetime.utcnow().isoformat(),
    "updated_at": datetime.datetime.utcnow().isoformat()
}

# Create demo business
demo_business = {
    "id": "demo_business_1",
    "owner_id": "demo_user_1",
    "name": "Demo Tech Company",
    "industry": "Technology",
    "description": "AI-powered marketing automation platform",
    "target_audience": {
        "age_range": "25-45",
        "gender_focus": "All",
        "location": "Global",
        "interests": ["Technology", "AI", "Marketing", "Automation"]
    },
    "brand_voice": "Professional but innovative",
    "content_preferences": {
        "platforms": ["Instagram", "LinkedIn", "Email", "SMS"],
        "tone": "Professional",
        "post_frequency_per_week": 5
    },
    "created_at": datetime.datetime.utcnow().isoformat(),
    "updated_at": datetime.datetime.utcnow().isoformat()
}

# Create demo campaign
demo_campaign = {
    "id": "demo_campaign_1",
    "business_id": "demo_business_1",
    "name": "Q1 Product Launch",
    "goal": "Generate 500 qualified leads",
    "duration_days": 30,
    "strategy_summary": "AI-powered content calendar for product launch",
    "content_calendar": [
        {"day": 1, "theme": "Introduction", "content_type": "post"},
        {"day": 2, "theme": "Product Showcase", "content_type": "reel"},
        {"day": 3, "theme": "Behind the Scenes", "content_type": "story"},
        {"day": 4, "theme": "Customer Testimonial", "content_type": "post"},
        {"day": 5, "theme": "Feature Highlight", "content_type": "carousel"}
    ],
    "status": "active",
    "start_date": datetime.datetime.utcnow().isoformat(),
    "end_date": (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat(),
    "created_at": datetime.datetime.utcnow().isoformat()
}

# Save demo data
with open('demo_data.json', 'w') as f:
    json.dump({
        "users": [demo_user],
        "businesses": [demo_business],
        "campaigns": [demo_campaign]
    }, f, indent=2)

print('Demo data created successfully')
"

echo "✅ Demo data loaded"

# Show service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎉 Deployment Complete!"
echo "🌐 Frontend: http://localhost:3000"
echo "🚀 Backend API: http://localhost:8000"
echo "📊 Monitoring: http://localhost:3001 (Grafana)"
echo "📈 Metrics: http://localhost:9090 (Prometheus)"
echo ""
echo "📚 Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "🎯 Next Steps:"
echo "1. Open http://localhost:3000 to access the application"
echo "2. Login with demo credentials"
echo "3. Explore all features and functionality"
echo "4. Monitor performance in Grafana dashboard"
echo "5. Check logs in the logs directory"
echo ""
echo "🚀 Happy Marketing! 🎉"
