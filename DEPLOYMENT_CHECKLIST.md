# Railway Deployment Checklist

Use this checklist to track your deployment progress.

## 📋 Pre-Deployment

- [ ] Railway account created at [railway.app](https://railway.app)
- [ ] GitHub repository connected to Railway
- [ ] OpenAI API key obtained from [platform.openai.com](https://platform.openai.com/api-keys)
- [ ] Google Gemini API key obtained from [makersuite.google.com](https://makersuite.google.com/app/apikey)
- [ ] SECRET_KEY generated (run `python railway_helper.py`)

## 🗄️ Database Setup

- [ ] SQLite embedded (no external DB needed)
- [ ] Redis plugin added to Railway project
- [ ] Both databases are provisioned and running
- [ ] Connection strings verified in Railway dashboard

## 🔧 Backend Service

- [ ] Backend service created in Railway
- [ ] Root directory set to `backend`
- [ ] Environment variables configured:
  - [ ] `PORT=8000`
  - [ ] `ENVIRONMENT=production`
  - [ ] `SECRET_KEY=<generated>`
  - [ ] `DATABASE_URL=sqlite:///./aimarketing.db`
  - [ ] `REDIS_URL=${{Redis.REDIS_URL}}`
  - [ ] `OPENAI_API_KEY=<your-key>`
  - [ ] `GEMINI_API_KEY=<your-key>`
  - [ ] `LOG_LEVEL=INFO`
- [ ] Backend deployed successfully
- [ ] Backend health check accessible: `<backend-url>/health`
- [ ] Backend public URL noted: `___________________________`

## 🤖 LangChain AI Service

- [ ] LangChain service created in Railway
- [ ] Root directory set to `langchain`
- [ ] Environment variables configured:
  - [ ] `PORT=8001`
  - [ ] `GEMINI_API_KEY=<your-key>`
  - [ ] `OPENAI_API_KEY=<your-key>`
- [ ] LangChain service deployed successfully
- [ ] LangChain public URL noted: `___________________________`

## 🎨 Frontend Service

- [ ] Frontend service created in Railway
- [ ] Root directory set to `ux design`
- [ ] Environment variables configured:
  - [ ] `PORT=3000`
- [ ] Frontend deployed successfully
- [ ] Frontend public URL noted: `___________________________`

## 🔄 Cross-Service Configuration

- [ ] Updated `ux design/config.js` with backend URLs:
  - [ ] `API_BASE_URL` set to backend URL
  - [ ] `LANGCHAIN_URL` set to langchain URL
- [ ] Committed and pushed config.js changes
- [ ] Frontend redeployed with new config
- [ ] Updated backend `FRONTEND_URL` variable to frontend URL
- [ ] Backend redeployed with new CORS settings

## ✅ Testing

- [ ] Frontend loads successfully
- [ ] Backend API responds to requests
- [ ] AI service generates responses
- [ ] No CORS errors in browser console
- [ ] Database connections working (check backend logs)
- [ ] Redis cache working
- [ ] User registration works
- [ ] User login works
- [ ] Campaign creation works
- [ ] Content generation works
- [ ] Analytics dashboard loads

## 🚀 Post-Deployment

- [ ] Auto-deploy enabled for each service
- [ ] Health checks configured
- [ ] Monitoring set up in Railway dashboard
- [ ] Custom domain configured (if applicable)
- [ ] SSL/HTTPS verified
- [ ] Error tracking configured (optional: Sentry)
- [ ] Backup strategy for databases
- [ ] Documentation updated with live URLs

## 📝 URLs Reference

Fill in your deployed URLs:

```
Frontend:  https://_________________________________
Backend:   https://_________________________________
LangChain: https://_________________________________
SQLite:   (internal) ${{SQLite embedded}}
Redis:     (internal) ${{Redis.REDIS_URL}}
```

## 🆘 Troubleshooting

If something doesn't work:

1. **Check Logs**: Railway Dashboard → Service → Deployments → Latest → Logs
2. **Verify Environment Variables**: Railway Dashboard → Service → Variables
3. **Check Health Endpoints**: 
   - Backend: `<backend-url>/health`
   - Should return JSON status
4. **CORS Issues**: 
   - Ensure `FRONTEND_URL` is set in backend
   - Check allowed origins in `main.py`
5. **Database Connection**: 
   - Check SQLite and Redis are running
   - Verify connection string format

## 📞 Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project GitHub Issues: [Your repo issues]

---

**Deployment Date**: _______________  
**Deployed By**: _______________  
**Environment**: Production  
**Platform**: Railway
