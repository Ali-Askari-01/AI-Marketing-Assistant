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
        'GEMINI_API_KEY',
        'SECRET_KEY',
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
    print("2. Deploy single service (backend serves frontend)")
    print("3. Set environment variables (SECRET_KEY, GEMINI_API_KEY)")
    print("4. Database is SQLite (embedded, no plugin needed)")
    print()
    
    print("=" * 60)
    print("✅ Deployment Checklist:")
    print("-" * 60)
    print()
    print("[ ] Railway account created")
    print("[ ] GitHub repo connected")
    print("[ ] Database: SQLite (embedded, no setup needed)")
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
