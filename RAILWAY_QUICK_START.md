# Railway Quick Deploy Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Railway account ([railway.app](https://railway.app))
- GitHub account
- OpenAI/Gemini API keys

---

## One-Click Deploy Steps

### 1️⃣ Create Railway Project
```bash
# Option A: Via Railway Dashboard
1. Go to railway.app
2. Click "New Project" → "Empty Project"
3. Name: "ai-marketing-assistant"

# Option B: Via CLI
railway login
railway init
```

### 2️⃣ Add Databases
```bash
# In Railway Dashboard:
1. Click "+ New" → "Database" → "SQLite"
2. Click "+ New" → "Database" → "Redis"
```

### 3️⃣ Deploy Services

#### Backend API
```bash
# In Railway Dashboard:
1. "+ New" → "GitHub Repo" → Select your repo
2. Root Directory: `backend`
3. Add environment variables (see below)
4. Deploy
```

**Backend Environment Variables**:
```env
PORT=8000
ENVIRONMENT=production
SECRET_KEY=<generate-random-string>
DATABASE_URL=sqlite:///./aimarketing.db
REDIS_URL=${{Redis.REDIS_URL}}
OPENAI_API_KEY=<your-key>
GEMINI_API_KEY=<your-key>
FRONTEND_URL=<will-update-later>
```

#### LangChain AI Service
```bash
# In Railway Dashboard:
1. "+ New" → "GitHub Repo" → Select your repo
2. Root Directory: `langchain`
3. Add environment variables (see below)
4. Deploy
```

**LangChain Environment Variables**:
```env
PORT=8001
GEMINI_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
```

#### Frontend
```bash
# In Railway Dashboard:
1. "+ New" → "GitHub Repo" → Select your repo
2. Root Directory: `ux design`
3. Add environment variables (see below)
4. Deploy
```

**Frontend Environment Variables**:
```env
PORT=3000
```

### 4️⃣ Update Frontend Config
After all services are deployed, update `ux design/config.js`:
```javascript
const CONFIG = {
    API_BASE_URL: 'https://backend-api-production.up.railway.app',
    LANGCHAIN_URL: 'https://langchain-ai-service-production.up.railway.app'
};
```

Commit and push to trigger redeploy.

### 5️⃣ Update Backend CORS
Update backend `FRONTEND_URL` variable:
```env
FRONTEND_URL=https://frontend-production.up.railway.app
```

Click "Redeploy" on backend service.

---

## 🎉 Done!

Your URLs:
- **Frontend**: `https://frontend-production.up.railway.app`
- **Backend**: `https://backend-api-production.up.railway.app`
- **AI Service**: `https://langchain-ai-service-production.up.railway.app`

---

## 🔧 Helpful Commands

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# View logs
railway logs

# Open service
railway open

# Check status
railway status
```

---

## 💡 Tips

1. **Free Credits**: Railway gives $5 free credits
2. **Auto Deploy**: Push to Git = Auto deploy
3. **Custom Domain**: Add in Settings → Domains
4. **Monitoring**: Check Metrics tab for each service
5. **Logs**: Real-time logs in Deployments tab

---

## 📚 Full Guide

See [RAILWAY_DEPLOYMENT_GUIDE.md](./RAILWAY_DEPLOYMENT_GUIDE.md) for detailed instructions.
