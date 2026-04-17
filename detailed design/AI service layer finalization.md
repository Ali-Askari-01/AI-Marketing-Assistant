🚀 ITERATION 4 — AI SERVICE LAYER FINALIZATION (Deep, Production-Ready)

This layer is critical — it’s the “brain” of your marketing software. It must:

Handle all AI calls (strategy, content, multimedia, messaging)

Validate outputs against JSON schemas

Track costs/tokens

Retry intelligently if AI fails

Be fully isolated from routes

We will define:

1️⃣ Folder & Module Structure
2️⃣ Responsibilities
3️⃣ Input/Output schema rules
4️⃣ Prompt orchestration
5️⃣ Retry & error handling
6️⃣ Cost tracking
7️⃣ Sample flows

🗂 4.1 Folder & Module Structure
app/
 └── ai/
      ├── ai_client.py          # Handles direct calls to OpenAI
      ├── prompt_builder.py     # Builds prompts for each feature
      ├── validator.py          # Validates AI response JSON schema
      ├── retry_handler.py      # Retries AI calls intelligently
      ├── cost_tracker.py       # Tracks tokens, model used, estimated cost
      └── ai_service.py         # Orchestrator: exposes high-level functions

ai_service.py is the only module your routes will call.

No other route calls OpenAI directly.

🧠 4.2 Responsibilities
Module	Responsibility
ai_client.py	Low-level OpenAI API request/response handling
prompt_builder.py	Constructs feature-specific prompts (strategy, content, video, messaging)
validator.py	Ensures AI returns valid JSON; repairs or flags errors
retry_handler.py	Retries failed AI calls (timeout, malformed output, rate-limit)
cost_tracker.py	Logs tokens used, model, cost per call
ai_service.py	Orchestrates prompt building → AI call → validation → logging → return
4.3 Input/Output Schema Rules

Every AI call must define input and output schemas.

Example: Campaign Strategy Output Schema

{
  "campaign_id": "uuid",
  "calendar": [
    {
      "day": 1,
      "theme": "Transformation Story",
      "content_type": "Reel"
    }
  ]
}

Validator rules:

Required fields: campaign_id, calendar, day, theme, content_type

Types must match (string, int, enum)

Missing/invalid → Retry once with JSON repair, else fail

4.4 Prompt Orchestration (prompt_builder.py)

For each feature:

Feature	Prompt Example	Output Type
Strategy	“Generate 30-day content calendar for {industry} brand tone {tone}”	JSON calendar
Content	“Generate caption, hashtags, script for campaign day X”	JSON post
Video	“Generate hook, body, CTA for {theme} video”	JSON video script
Messaging	“Reply suggestion for customer message”	JSON text

Insert business context, campaign data, tone, CTA info

Enforce JSON response mode (OpenAI response_format={"type": "json"})

4.5 Retry & Error Handling (retry_handler.py)

Retry on:

Timeout

Empty response

Invalid JSON

5xx from AI provider

Max retries: 2–3

On failure:

Return standardized error: AI_GENERATION_FAILED

Log for debugging

4.6 Cost & Token Tracking (cost_tracker.py)

Track per request:

User / Business / Campaign / Content IDs

Model used

Tokens used

Estimated cost

Store in ai_logs table.

Optional for competition: just print to console or save in test DB.

4.7 Orchestration Flow (ai_service.py)

Example: Content Generation Flow

Route calls: ai_service.generate_content(business_id, campaign_id, day, content_type)

AI Service:

Builds prompt via prompt_builder.py

Calls ai_client.py (OpenAI)

Validates output via validator.py

If invalid → retry_handler.py

Logs tokens via cost_tracker.py

Returns validated JSON to route

Example Call:

from ai.ai_service import generate_content

content_json = generate_content(
    business_id="uuid",
    campaign_id="uuid",
    day=1,
    content_type="Reel"
)
# content_json now safe to save in DB
4.8 Safety / Production Considerations

Prompt Injection Protection: sanitize user inputs before sending to AI

Timeouts: AI client must timeout after 15–20 seconds

Async: optional for production, sync is OK for hackathon

Logging: always log AI outputs & errors

4.9 Notes for Multimedia Content

Image/video endpoints:

ai_service.generate_image(...) → returns image URL / base64

ai_service.generate_video_script(...) → returns script JSON

Treat image/video as content_type in content table

✅ Key Takeaways (Iteration 4)

Routes never call AI directly

JSON validation is mandatory

Retries handled systematically

Token/cost tracking logged

Prompt builder modular per feature

Multimedia content integrated