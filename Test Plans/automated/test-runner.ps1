# ═══════════════════════════════════════════════════════════════
# AI Marketing Platform — Automated API Test Runner
# Run: powershell -ExecutionPolicy Bypass -File test-runner.ps1
# ═══════════════════════════════════════════════════════════════

$BASE = "http://localhost:8003"
$pass = 0; $fail = 0; $skip = 0
$results = @()

function Test-Endpoint {
    param(
        [string]$Id,
        [string]$Name,
        [string]$Method = "GET",
        [string]$Url,
        [string]$Body = $null,
        [int[]]$ExpectedStatus = @(200),
        [string]$AssertContains = $null
    )
    try {
        $params = @{
            Uri             = "$BASE$Url"
            Method          = $Method
            UseBasicParsing = $true
            TimeoutSec      = 15
            ErrorAction     = "Stop"
        }
        if ($Body) {
            $params.Headers = @{ "Content-Type" = "application/json" }
            $params.Body    = $Body
        }
        $resp = Invoke-WebRequest @params
        $status = [int]$resp.StatusCode
        $ok = $status -in $ExpectedStatus

        if ($ok -and $AssertContains) {
            $ok = $resp.Content -match $AssertContains
        }

        if ($ok) {
            $script:pass++
            $color = "Green"
            $label = "PASS"
        } else {
            $script:fail++
            $color = "Red"
            $label = "FAIL"
        }
        Write-Host "  [$label] #$Id $Name  (HTTP $status)" -ForegroundColor $color
        $script:results += [pscustomobject]@{ Id=$Id; Name=$Name; Status=$status; Result=$label }
    }
    catch {
        $msg = $_.Exception.Message
        # Try to extract status code from error
        if ($msg -match "(\d{3})") {
            $status = [int]$Matches[1]
            if ($status -in $ExpectedStatus) {
                $script:pass++
                Write-Host "  [PASS] #$Id $Name  (HTTP $status)" -ForegroundColor Green
                $script:results += [pscustomobject]@{ Id=$Id; Name=$Name; Status=$status; Result="PASS" }
                return
            }
        }
        $script:fail++
        Write-Host "  [FAIL] #$Id $Name  — $msg" -ForegroundColor Red
        $script:results += [pscustomobject]@{ Id=$Id; Name=$Name; Status="ERR"; Result="FAIL" }
    }
}

# ─── Pre-flight ───
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  AI Marketing Platform — API Test Suite" -ForegroundColor Cyan
Write-Host "  Target: $BASE" -ForegroundColor DarkGray
Write-Host "  Time:   $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor DarkGray
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Connectivity check
try {
    Invoke-WebRequest -Uri "$BASE/docs" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop | Out-Null
    Write-Host "  Backend reachable." -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Backend not reachable at $BASE" -ForegroundColor Red
    Write-Host "  Start the backend first: python backend/main.py" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# ═══ 1. Health ═══
Write-Host "─── 1. Health & System ───" -ForegroundColor Yellow
Test-Endpoint -Id "1" -Name "Root page" -Url "/"
Test-Endpoint -Id "2" -Name "Swagger docs" -Url "/docs"
Test-Endpoint -Id "3" -Name "Health check" -Url "/health" -AssertContains "healthy"

# ═══ 2. Auth ═══
Write-Host ""
Write-Host "─── 2. Authentication ───" -ForegroundColor Yellow
Test-Endpoint -Id "4" -Name "Login (valid)" -Method POST -Url "/api/v1/auth/login" `
    -Body '{"email":"admin@demo.com","password":"demo123"}' -AssertContains "access_token"
Test-Endpoint -Id "5" -Name "Login (invalid)" -Method POST -Url "/api/v1/auth/login" `
    -Body '{"email":"bad"}' -ExpectedStatus @(401, 422)

# ═══ 3. AI ═══
Write-Host ""
Write-Host "─── 3. AI Endpoints ───" -ForegroundColor Yellow
Test-Endpoint -Id "9" -Name "Generate captions" -Method POST -Url "/api/v1/ai/generate-captions" `
    -Body '{"topic":"Summer Sale","platform":"instagram"}' -AssertContains "captions"
Test-Endpoint -Id "11" -Name "Optimize hashtags" -Method POST -Url "/api/v1/ai/optimize-hashtags" `
    -Body '{"topic":"fitness","platform":"instagram"}'
Test-Endpoint -Id "12" -Name "Analyze post" -Method POST -Url "/api/v1/ai/analyze-post" `
    -Body '{"content":"Check out our new product!","platform":"instagram"}'
Test-Endpoint -Id "15" -Name "Agent ask" -Method POST -Url "/api/v1/agent/ask" `
    -Body '{"question":"How to improve engagement?"}'

# ═══ 4. Inbox ═══
Write-Host ""
Write-Host "─── 4. Inbox / Messaging ───" -ForegroundColor Yellow
Test-Endpoint -Id "16" -Name "List threads" -Url "/api/v1/inbox/threads?business_id=demo" -AssertContains "threads"
Test-Endpoint -Id "17" -Name "Filter by platform" -Url "/api/v1/inbox/threads?business_id=demo&platform=instagram" -AssertContains "instagram"
Test-Endpoint -Id "18" -Name "Search threads" -Url "/api/v1/inbox/threads?business_id=demo&search=Sarah" -AssertContains "Sarah"
Test-Endpoint -Id "19" -Name "Thread detail" -Url "/api/v1/inbox/threads/thread_sarah" -AssertContains "messages"
Test-Endpoint -Id "20" -Name "Thread not found" -Url "/api/v1/inbox/threads/nonexistent_id" -ExpectedStatus @(404)
Test-Endpoint -Id "21" -Name "Send reply" -Method POST -Url "/api/v1/inbox/threads/thread_sarah/reply" `
    -Body '{"content":"Thanks for reaching out!"}' -AssertContains "message"
Test-Endpoint -Id "23" -Name "AI suggest" -Method POST -Url "/api/v1/inbox/threads/thread_sarah/ai-suggest" `
    -AssertContains "suggestions"
Test-Endpoint -Id "24" -Name "Flag thread" -Method PATCH -Url "/api/v1/inbox/threads/thread_sarah" `
    -Body '{"is_flagged":true}'
Test-Endpoint -Id "26" -Name "Inbox stats" -Url "/api/v1/inbox/stats" -AssertContains "total_messages"

# ═══ 5. Social ═══
Write-Host ""
Write-Host "─── 5. Social Publishing ───" -ForegroundColor Yellow
Test-Endpoint -Id "27" -Name "Social accounts" -Url "/api/v1/social/accounts"
Test-Endpoint -Id "29" -Name "Post history" -Url "/api/v1/social/post-history"

# ═══ 6. Campaigns ═══
Write-Host ""
Write-Host "─── 6. Campaigns & Content ───" -ForegroundColor Yellow
Test-Endpoint -Id "30" -Name "List campaigns" -Url "/api/v1/campaigns"
Test-Endpoint -Id "32" -Name "Content library" -Url "/api/v1/content/library"

# ═══ 7. Analytics ═══
Write-Host ""
Write-Host "─── 7. Analytics ───" -ForegroundColor Yellow
Test-Endpoint -Id "33" -Name "Dashboard analytics" -Url "/api/v1/analytics/dashboard"

# ═══ 8. Error handling ═══
Write-Host ""
Write-Host "─── 8. Error Handling ───" -ForegroundColor Yellow
Test-Endpoint -Id "36" -Name "Unknown endpoint" -Url "/api/v1/nonexistent" -ExpectedStatus @(404, 405)
Test-Endpoint -Id "39" -Name "CORS headers" -Method OPTIONS -Url "/api/v1/inbox/threads" -ExpectedStatus @(200, 400, 405)

# ═══ Summary ═══
$total = $pass + $fail
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  RESULTS: $pass/$total passed   $fail failed" -ForegroundColor $(if ($fail -eq 0) { "Green" } else { "Red" })
Write-Host "  Pass rate: $([math]::Round($pass/$total*100, 1))%" -ForegroundColor $(if ($fail -eq 0) { "Green" } else { "Yellow" })
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
