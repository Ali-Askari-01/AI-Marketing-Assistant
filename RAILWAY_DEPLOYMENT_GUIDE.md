# Railway Deployment Guide - AI Marketing Command Center

## 📋 Overview

This guide walks you through deploying your AI Marketing Command Center on Railway. We'll deploy 3 services:

1. **Backend API** (FastAPI) - Port 8000
2. **LangChain AI Service** - Port 8001
3. **Frontend** (Static Site) - Port 3000

Plus 2 managed databases:
- **MongoDB** (Railway Plugin)
- **Redis** (Railway Plugin)

---

## 🚀 Step-by-Step Deployment

### **Part 1: Initial Setup**

#### 1.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Verify your account

#### 1.2 Install Railway CLI (Optional)
```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Verify installation
railway --version
```

---

### **Part 2: Create Railway Project**

#### 2.1 Create New Project
1. Click **"New Project"**
2. Select **"Empty Project"**
3. Name it: `ai-marketing-command-center`

---

### **Part 3: Add Databases**

#### 3.1 Add MongoDB
1. In your project, click **"+ New"**
2. Select **"Database"** → **"Add MongoDB"**
3. Wait for provisioning (1-2 minutes)
4. Note: Connection string will be automatically available as `MONGO_URL`

#### 3.2 Add Redis
1. Click **"+ New"** again
2. Select **"Database"** → **"Add Redis"**
3. Wait for provisioning
4. Note: Connection string will be available as `REDIS_URL`

---

### **Part 4: Deploy Backend API**

#### 4.1 Create Backend Service
1. Click **"+ New"** → **"GitHub Repo"**
2. Select your `AI-Marketing-Assistant` repository
3. Choose **"Add Service"**
4. Name: `backend-api`

#### 4.2 Configure Backend Service
1. Click on the backend service
2. Go to **"Settings"** tab
3. Set **Root Directory**: `backend`
4. Deploy command should auto-detect from `Procfile`

#### 4.3 Set Environment Variables
Go to **"Variables"** tab and add:

```env
# Required Variables
PORT=8000
ENVIRONMENT=production
SECRET_KEY=<generate-a-secure-random-string-here>

# Database (Auto-filled by Railway plugins)
MONGODB_URL=${{MongoDB.MONGO_URL}}
REDIS_URL=${{Redis.REDIS_URL}}

# AI API Keys (Add your own)
OPENAI_API_KEY=<your-openai-api-key>
GEMINI_API_KEY=<your-gemini-api-key>

# Frontend URL (Will update after frontend deployment)
FRONTEND_URL=<will-add-after-frontend-deployment>

# Optional
LOG_LEVEL=INFO
```

**Generate SECRET_KEY**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 4.4 Deploy Backend
1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Check **"Deployments"** tab for status
4. Once deployed, note the **public URL** (e.g., `https://backend-api-production.up.railway.app`)

---

### **Part 5: Deploy LangChain AI Service**

#### 5.1 Create AI Service
1. Click **"+ New"** → **"GitHub Repo"**
2. Select same repository
3. Choose **"Add Service"**
4. Name: `langchain-ai-service`

#### 5.2 Configure AI Service
1. Go to **"Settings"**
2. Set **Root Directory**: `langchain`
3. Procfile should auto-detect

#### 5.3 Set Environment Variables
Go to **"Variables"** tab:

```env
PORT=8001
GEMINI_API_KEY=<your-gemini-api-key>
OPENAI_API_KEY=<your-openai-api-key>
SERPAPI_API_KEY=<your-serpapi-key-optional>
```

#### 5.4 Deploy AI Service
1. Click **"Deploy"**
2. Wait for build completion
3. Note the **public URL** (e.g., `https://langchain-ai-service-production.up.railway.app`)

---

### **Part 6: Deploy Frontend**

#### 6.1 Create Frontend Service
1. Click **"+ New"** → **"GitHub Repo"**
2. Select same repository
3. Choose **"Add Service"**
4. Name: `frontend`

#### 6.2 Configure Frontend
1. Go to **"Settings"**
2. Set **Root Directory**: `ux design`
3. Procfile should detect Python server

#### 6.3 Update Frontend Config
**IMPORTANT**: Before deploying, update your frontend config:

Edit `ux design/config.js`:
```javascript
const CONFIG = {
    API_BASE_URL: 'https://backend-api-production.up.railway.app',
    LANGCHAIN_URL: 'https://langchain-ai-service-production.up.railway.app',
    // ... rest of config
};
```

#### 6.4 Set Environment Variables
```env
PORT=3000
```

#### 6.5 Deploy Frontend
1. Click **"Deploy"**
2. Note the **public URL** (e.g., `https://frontend-production.up.railway.app`)

---

### **Part 7: Final Configuration**

#### 7.1 Update Backend CORS
Go back to **Backend Service** → **Variables** and update:
```env
FRONTEND_URL=https://frontend-production.up.railway.app
```

Click **"Redeploy"** on backend service.

#### 7.2 Enable Public Networking
For each service:
1. Go to **"Settings"**
2. Scroll to **"Networking"**
3. Click **"Generate Domain"** if not auto-generated

---

## 🔒 Security Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Add all API keys to environment variables
- [ ] Enable Railway's **"Private Networking"** for internal services
- [ ] Set up **"Health Checks"** for each service
- [ ] Configure CORS properly in backend
- [ ] Never commit `.env` files to Git

---

## 📊 Monitoring & Logs

### View Logs
1. Click on any service
2. Go to **"Deployments"** tab
3. Click on latest deployment
4. View real-time logs

### Monitor Resources
- Railway provides CPU, Memory, and Network metrics
- Check **"Metrics"** tab in each service

---

## 💰 Cost Estimation

**Railway Pricing** (as of 2024):
- **Hobby Plan**: $5/month + $0.000231/GB-hour
- **Pro Plan**: $20/month + usage

**Estimated Monthly Cost**:
- 3 Services (Backend, AI, Frontend): ~$10-15/month
- MongoDB + Redis: ~$5-10/month
- **Total**: ~$20-30/month for small-medium traffic

**Free Trial**: Railway offers $5 free credits to start.

---

## 🐛 Troubleshooting

### Build Fails
- Check **"Build Logs"** in Deployments tab
- Verify `requirements.txt` is correct
- Ensure Python version compatibility

### Service Won't Start
- Check **"Deploy Logs"**
- Verify environment variables are set
- Check PORT is set correctly

### Database Connection Issues
- Verify MongoDB and Redis plugins are running
- Check connection string variables: `${{MongoDB.MONGO_URL}}`
- Test connection from backend logs

### CORS Errors
- Update `FRONTEND_URL` in backend variables
- Check CORS middleware in `main.py`
- Ensure frontend URL is correct

---

## 🔄 CI/CD - Auto Deploy

Railway automatically deploys on Git push:

1. Go to **Service Settings**
2. Enable **"Auto Deploy"**
3. Select branch (e.g., `main` or `production`)
4. Every push triggers redeployment

---

## 📦 Alternative: Deploy with Railway CLI

```bash
# Login
railway login

# Link to project
railway link

# Deploy backend
cd backend
railway up

# Deploy langchain
cd ../langchain
railway up

# Deploy frontend
cd ../ux-design
railway up
```

---

## 🌐 Custom Domain (Optional)

1. Go to **Frontend Service** → **"Settings"**
2. Scroll to **"Domains"**
3. Click **"Custom Domain"**
4. Add your domain (e.g., `app.yourdomain.com`)
5. Update DNS records as instructed

---

## 📝 Environment Variables Reference

### Backend Service
```env
PORT=8000
ENVIRONMENT=production
SECRET_KEY=<random-secure-string>
MONGODB_URL=${{MongoDB.MONGO_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
OPENAI_API_KEY=<your-key>
GEMINI_API_KEY=<your-key>
FRONTEND_URL=<frontend-railway-url>
LOG_LEVEL=INFO
```

### LangChain Service
```env
PORT=8001
GEMINI_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
SERPAPI_API_KEY=<optional>
```

### Frontend Service
```env
PORT=3000
```

---

## ✅ Post-Deployment Checklist

- [ ] All 3 services are deployed and running
- [ ] MongoDB connected successfully
- [ ] Redis connected successfully
- [ ] Frontend loads correctly
- [ ] Backend API responds to health check
- [ ] AI service generates responses
- [ ] CORS is properly configured
- [ ] Environment variables are set
- [ ] Public URLs are accessible
- [ ] Auto-deploy is enabled

---

## 🎉 You're Live!

Your AI Marketing Command Center is now deployed on Railway!

**Access your app**:
- Frontend: `https://frontend-production.up.railway.app`
- Backend API: `https://backend-api-production.up.railway.app`
- AI Service: `https://langchain-ai-service-production.up.railway.app`

**Next Steps**:
1. Test all features
2. Set up monitoring
3. Configure custom domain
4. Enable backups for databases
5. Set up error tracking (Sentry)

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord Community](https://discord.gg/railway)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [MongoDB Atlas Alternative](https://www.mongodb.com/cloud/atlas) (if needed)

---

**Need Help?** Check Railway logs or contact support at [Railway Help](https://help.railway.app).
