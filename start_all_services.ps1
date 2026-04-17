# Start all services for AI Marketing Command Center
# Run this script to start Frontend, Backend, and Gemini AI Agent

Write-Host "🚀 Starting AI Marketing Command Center..." -ForegroundColor Cyan
Write-Host "=" * 60

# Start Frontend (Port 8000)
Write-Host "`n📱 Starting Frontend on port 8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\SIKANDAR\Desktop\Hackathon\ux design'; python -m http.server 8000"

Start-Sleep -Seconds 2

# Start Main Backend (Port 8003)
Write-Host "⚙️  Starting Main Backend on port 8003..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\SIKANDAR\Desktop\Hackathon\backend'; c:\Users\SIKANDAR\Desktop\Hackathon\.venv\Scripts\python.exe main.py"

Start-Sleep -Seconds 3

# Start Gemini AI Agent (Port 8004)
Write-Host "🤖 Starting Gemini AI Agent on port 8004..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\SIKANDAR\Desktop\Hackathon\langchain'; c:\Users\SIKANDAR\Desktop\Hackathon\.venv\Scripts\python.exe api_gemini.py"

Write-Host "`n⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "`n✅ All services started!" -ForegroundColor Green
Write-Host "`nService URLs:" -ForegroundColor Cyan
Write-Host "  Frontend:        http://localhost:8000" -ForegroundColor White
Write-Host "  Main Backend:    http://localhost:8003" -ForegroundColor White
Write-Host "  API Docs:        http://localhost:8003/docs" -ForegroundColor White
Write-Host "  Gemini Agent:    http://localhost:8004" -ForegroundColor White
Write-Host "  Agent Docs:      http://localhost:8004/docs" -ForegroundColor White

Write-Host "`n🌐 Opening browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
Start-Process "http://localhost:8000"

Write-Host "`n✨ AI Marketing Command Center is ready!" -ForegroundColor Green
Write-Host "   Press any key to check service health..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Health checks
Write-Host "`n🏥 Running health checks..." -ForegroundColor Cyan

try {
    $frontendHealth = curl http://localhost:8000 -UseBasicParsing -TimeoutSec 2
    Write-Host "  ✅ Frontend: OK (Status: $($frontendHealth.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Frontend: Not responding" -ForegroundColor Red
}

try {
    $backendHealth = curl http://localhost:8003/health -UseBasicParsing -TimeoutSec 2
    Write-Host "  ✅ Main Backend: OK (Status: $($backendHealth.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Main Backend: Not responding" -ForegroundColor Red
}

try {
    $agentHealth = curl http://localhost:8004/health -UseBasicParsing -TimeoutSec 2
    Write-Host "  ✅ Gemini Agent: OK (Status: $($agentHealth.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Gemini Agent: Not responding (may still be starting)" -ForegroundColor Yellow
}

Write-Host "`n📝 Note:" -ForegroundColor Yellow
Write-Host "   - Three PowerShell windows will remain open for each service"
Write-Host "   - Close those windows to stop the services"
Write-Host "   - Check GEMINI_AGENT_INTEGRATION_COMPLETE.md for documentation"

Write-Host "`n🎉 Happy marketing! 🚀" -ForegroundColor Magenta
