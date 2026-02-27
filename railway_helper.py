"""
Railway Deployment Helper Script
Generates secure keys and validates environment setup
"""

import secrets
import os
import sys

def generate_secret_key():
    """Generate a secure SECRET_KEY for backend"""
    return secrets.token_urlsafe(32)

def generate_api_token():
    """Generate a secure API token"""
    return secrets.token_urlsafe(48)

def check_env_vars():
    """Check if required environment variables are set"""
    required_vars = [
        'OPENAI_API_KEY',
        'GEMINI_API_KEY',
        'SECRET_KEY',
        'MONGODB_URL',
        'REDIS_URL'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    return missing

def print_deployment_info():
    """Print deployment information"""
    print("=" * 60)
    print("🚀 Railway Deployment Helper")
    print("=" * 60)
    print()
    
    print("📋 Generated Secure Keys:")
    print("-" * 60)
    print(f"SECRET_KEY (Backend):")
    print(f"  {generate_secret_key()}")
    print()
    print(f"API_TOKEN (Optional):")
    print(f"  {generate_api_token()}")
    print()
    
    print("=" * 60)
    print("📝 Required API Keys:")
    print("-" * 60)
    print()
    print("1. OpenAI API Key")
    print("   Get it from: https://platform.openai.com/api-keys")
    print()
    print("2. Google Gemini API Key")
    print("   Get it from: https://makersuite.google.com/app/apikey")
    print()
    print("3. SerpAPI Key (Optional - for web search)")
    print("   Get it from: https://serpapi.com/")
    print()
    
    print("=" * 60)
    print("🔧 Railway Setup Steps:")
    print("-" * 60)
    print()
    print("1. Create Railway project")
    print("2. Add MongoDB plugin")
    print("3. Add Redis plugin")
    print("4. Deploy backend service (root: backend)")
    print("5. Deploy langchain service (root: langchain)")
    print("6. Deploy frontend service (root: ux design)")
    print("7. Update FRONTEND_URL in backend env vars")
    print("8. Update config.js with backend URLs")
    print()
    
    print("=" * 60)
    print("✅ Deployment Checklist:")
    print("-" * 60)
    print()
    print("[ ] Railway account created")
    print("[ ] GitHub repo connected")
    print("[ ] MongoDB plugin added")
    print("[ ] Redis plugin added")
    print("[ ] OpenAI API key obtained")
    print("[ ] Gemini API key obtained")
    print("[ ] SECRET_KEY generated and set")
    print("[ ] Backend service deployed")
    print("[ ] LangChain service deployed")
    print("[ ] Frontend service deployed")
    print("[ ] FRONTEND_URL updated in backend")
    print("[ ] config.js updated with API URLs")
    print("[ ] All services tested and working")
    print()
    
    print("=" * 60)
    print("📖 Full Documentation:")
    print("-" * 60)
    print("  - RAILWAY_DEPLOYMENT_GUIDE.md (Complete guide)")
    print("  - RAILWAY_QUICK_START.md (Quick reference)")
    print("  - .env.railway.template (Environment variables)")
    print()

if __name__ == "__main__":
    print_deployment_info()
    
    # Check if running in environment with vars
    if "--check" in sys.argv:
        print("=" * 60)
        print("🔍 Environment Variables Check:")
        print("-" * 60)
        missing = check_env_vars()
        if missing:
            print("❌ Missing required variables:")
            for var in missing:
                print(f"   - {var}")
        else:
            print("✅ All required variables are set!")
        print()
