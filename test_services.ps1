# Test script for all services
Write-Host "🧪 Testing AI Marketing Command Center Services" -ForegroundColor Cyan
Write-Host "=" * 70

# Test Frontend
Write-Host "`n📱 Testing Frontend (Port 8000)..." -ForegroundColor Yellow
try {
    $frontend = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 3
    if ($frontend.StatusCode -eq 200) {
        Write-Host "   ✅ Frontend is running" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Frontend is NOT running" -ForegroundColor Red
    Write-Host "   Start with: cd 'C:\Users\SIKANDAR\Desktop\Hackathon\ux design'; python -m http.server 8000" -ForegroundColor Gray
}

# Test Main Backend
Write-Host "`n⚙️  Testing Main Backend (Port 8003)..." -ForegroundColor Yellow
try {
    $backend = Invoke-WebRequest -Uri "http://localhost:8003/health" -UseBasicParsing -TimeoutSec 3
    if ($backend.StatusCode -eq 200) {
        Write-Host "   ✅ Main Backend is running" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Main Backend is NOT running" -ForegroundColor Red
    Write-Host "   Start with: cd C:\Users\SIKANDAR\Desktop\Hackathon\backend; c:\Users\SIKANDAR\Desktop\Hackathon\.venv\Scripts\python.exe main.py" -ForegroundColor Gray
}

# Test Gemini Agent
Write-Host "`n🤖 Testing Gemini AI Agent (Port 8004)..." -ForegroundColor Yellow
try {
    $agent = Invoke-WebRequest -Uri "http://localhost:8004/health" -UseBasicParsing -TimeoutSec 3
    if ($agent.StatusCode -eq 200) {
        Write-Host "   ✅ Gemini Agent is running" -ForegroundColor Green
        $agentData = $agent.Content | ConvertFrom-Json
        Write-Host "   Model: $($agentData.model)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️  Gemini Agent is NOT running" -ForegroundColor Yellow
    Write-Host "   Start with: cd C:\Users\SIKANDAR\Desktop\Hackathon\langchain; c:\Users\SIKANDAR\Desktop\Hackathon\.venv\Scripts\python.exe api_simple.py" -ForegroundColor Gray
}

# Test Agent Integration
Write-Host "`n🔗 Testing Agent Integration..." -ForegroundColor Yellow
try {
    $agentStatus = Invoke-WebRequest -Uri "http://localhost:8003/api/v1/agent/status" -UseBasicParsing -TimeoutSec 3
    $statusData = $agentStatus.Content | ConvertFrom-Json
    if ($statusData.data.available) {
        Write-Host "   ✅ Agent integration is working" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Agent is available but not connected" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Cannot test integration (backend may not be running)" -ForegroundColor Red
}

# Summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "📋 SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 70

Write-Host "`n🌐 URLs:" -ForegroundColor White
Write-Host "   Frontend:     http://localhost:8000" -ForegroundColor Gray
Write-Host "   Backend API:  http://localhost:8003" -ForegroundColor Gray
Write-Host "   API Docs:     http://localhost:8003/docs" -ForegroundColor Gray
Write-Host "   Gemini Agent: http://localhost:8004" -ForegroundColor Gray
Write-Host "   Agent Docs:   http://localhost:8004/docs" -ForegroundColor Gray

Write-Host "`n📖 Documentation:" -ForegroundColor White
Write-Host "   GEMINI_AGENT_INTEGRATION_COMPLETE.md" -ForegroundColor Gray

Write-Host "`n🚀 Quick Start:" -ForegroundColor White
Write-Host "   .\start_all_services.ps1" -ForegroundColor Gray

Write-Host ""
