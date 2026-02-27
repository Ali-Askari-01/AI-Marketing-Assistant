🚀 ITERATION 6 — BACKGROUND JOBS & PERFORMANCE LAYER

Even though we’re using synchronous AI for hackathon purposes, we still need a performance & reliability plan. This ensures the app doesn’t freeze, times out, or fail during demos or multi-user scenarios.

🧱 6.1 OBJECTIVES

Prevent AI calls from freezing the backend

Set timeouts for long-running AI requests

Ensure frontend loading states are clear

Prepare groundwork for future async/background workers

Optimize DB queries for speed

⚡ 6.2 AI REQUEST PERFORMANCE STRATEGY
1️⃣ Timeout Handling

Max AI request time: 20 seconds

If AI exceeds this → return standardized error: AI_GENERATION_FAILED

Frontend shows: “AI is taking longer than expected. Try again or refresh.”

2️⃣ Async Execution (Hackathon-Friendly)

Even synchronous AI can be wrapped in async FastAPI routes

Example:

@app.post("/content/generate")
async def generate_content_endpoint(payload: ContentRequest):
    # Call AI in async function
    content = await ai_service.generate_content_async(payload)
    return {"success": True, "data": content}

Prevents backend from blocking multiple requests

3️⃣ Retry Logic

Already defined in Iteration 4 AI layer

Max retries: 2

If all retries fail → return standardized error

🏃 6.3 FUTURE BACKGROUND JOB SETUP

Optional for production SaaS / post-hackathon:

Use Redis + Celery / RQ to queue AI tasks

Route creates job → returns job_id

Worker executes AI task → updates DB

Frontend polls /job/{id} for status

Benefit: scaling multiple users simultaneously without blocking

🗄 6.4 DATABASE OPTIMIZATION

Index foreign keys: user_id, business_id, campaign_id, content_id

Add index on status in content table for fast retrieval of scheduled/published posts

Optional: cache heavy analytics queries in Redis

📊 6.5 ANALYTICS PERFORMANCE

Precompute engagement scores when content is generated

For multi-day campaigns: batch analytics computation offline

Store computed metrics in analytics table

Avoid computing on-the-fly for every frontend request

💻 6.6 FRONTEND PERFORMANCE CONSIDERATIONS

Show loading spinner during AI generation

Disable duplicate submissions

Timeout feedback: “Still generating…” after 15 seconds

Optional: show estimated wait time

✅ 6.7 DELIVERABLES FOR ITERATION 6

AI calls protected by timeouts

Async routes prevent server blocking

Retry logic applied from AI layer

DB indexes applied for speed

Frontend loading and error handling integrated

Background jobs blueprint ready for future expansion