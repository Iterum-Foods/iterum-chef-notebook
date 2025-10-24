# Quick Security Setup Script for Iterum Culinary App
# This script provides a streamlined setup process for GitHub security features

param(
    [string]$Repository = "Iterum-Foods/iterum-chef-notebook",
    [string]$Organization = "Iterum-Foods",
    [switch]$SkipPrompts
)

Write-Host "🚀 Quick Security Setup for Iterum Culinary App" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Check prerequisites
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghInstalled) {
    Write-Host "❌ GitHub CLI (gh) not found." -ForegroundColor Red
    Write-Host "   Please install GitHub CLI: https://cli.github.com/" -ForegroundColor Yellow
    Write-Host "   Then run: gh auth login" -ForegroundColor Yellow
    exit 1
}

$authStatus = gh auth status 2>&1
if ($authStatus -match "not logged in") {
    Write-Host "❌ Not authenticated with GitHub CLI." -ForegroundColor Red
    Write-Host "   Run: gh auth login" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ GitHub CLI authenticated" -ForegroundColor Green
Write-Host ""

# Function to prompt user
function Get-UserInput {
    param(
        [string]$Message,
        [string]$Default = "",
        [switch]$Required
    )
    
    if ($SkipPrompts -and $Default) {
        return $Default
    }
    
    do {
        $input = Read-Host $Message
        if (-not $input -and $Default) {
            $input = $Default
        }
        if ($Required -and -not $input) {
            Write-Host "This field is required. Please enter a value." -ForegroundColor Red
        }
    } while ($Required -and -not $input)
    
    return $input
}

# Function to open URL in browser
function Open-URL {
    param([string]$URL, [string]$Description)
    Write-Host "🌐 Opening $Description..." -ForegroundColor Green
    Start-Process $URL
    Start-Sleep 2
}

Write-Host "📋 This script will help you set up GitHub security features." -ForegroundColor Cyan
Write-Host ""

# Step 1: Secrets Configuration
Write-Host "🔐 Step 1: Configure GitHub Secrets" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

$configureSecrets = Get-UserInput "Do you want to configure GitHub secrets now? (y/n)" "y"
if ($configureSecrets -eq "y" -or $configureSecrets -eq "Y") {
    Write-Host ""
    Write-Host "📝 You need to add the following secrets to your repository:" -ForegroundColor White
    Write-Host "   1. SNYK_TOKEN - For security vulnerability scanning" -ForegroundColor White
    Write-Host "   2. SLACK_WEBHOOK_URL - For security notifications (optional)" -ForegroundColor White
    Write-Host ""
    
    $openSecrets = Get-UserInput "Open GitHub secrets page in browser? (y/n)" "y"
    if ($openSecrets -eq "y" -or $openSecrets -eq "Y") {
        Open-URL "https://github.com/$Repository/settings/secrets/actions" "GitHub Secrets page"
    }
    
    Write-Host ""
    Write-Host "📚 How to get SNYK_TOKEN:" -ForegroundColor Cyan
    Write-Host "   1. Go to https://snyk.io and sign up/login" -ForegroundColor White
    Write-Host "   2. Navigate to Account Settings → API Token" -ForegroundColor White
    Write-Host "   3. Copy your API token" -ForegroundColor White
    Write-Host "   4. Add it as SNYK_TOKEN secret in GitHub" -ForegroundColor White
    Write-Host ""
    
    $openSnyk = Get-UserInput "Open Snyk.io in browser? (y/n)" "n"
    if ($openSnyk -eq "y" -or $openSnyk -eq "Y") {
        Open-URL "https://snyk.io" "Snyk.io"
    }
}

Write-Host ""

# Step 2: Teams Configuration
Write-Host "👥 Step 2: Create Security Teams" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

$configureTeams = Get-UserInput "Do you want to create security teams now? (y/n)" "y"
if ($configureTeams -eq "y" -or $configureTeams -eq "Y") {
    Write-Host ""
    Write-Host "📝 You need to create the following teams:" -ForegroundColor White
    Write-Host "   - security-team (required)" -ForegroundColor White
    Write-Host "   - maintainers (recommended)" -ForegroundColor White
    Write-Host "   - backend-team (optional)" -ForegroundColor White
    Write-Host "   - frontend-team (optional)" -ForegroundColor White
    Write-Host "   - devops-team (optional)" -ForegroundColor White
    Write-Host ""
    
    $openTeams = Get-UserInput "Open GitHub teams page in browser? (y/n)" "y"
    if ($openTeams -eq "y" -or $openTeams -eq "Y") {
        Open-URL "https://github.com/$Organization/teams" "GitHub Teams page"
    }
}

Write-Host ""

# Step 3: Security Features
Write-Host "🛡️  Step 3: Enable Security Features" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

$enableSecurity = Get-UserInput "Do you want to enable security features now? (y/n)" "y"
if ($enableSecurity -eq "y" -or $enableSecurity -eq "Y") {
    Write-Host ""
    Write-Host "📝 Enable the following security features:" -ForegroundColor White
    Write-Host "   1. Dependabot alerts" -ForegroundColor White
    Write-Host "   2. Code scanning (CodeQL)" -ForegroundColor White
    Write-Host "   3. Security advisories" -ForegroundColor White
    Write-Host "   4. Branch protection rules" -ForegroundColor White
    Write-Host ""
    
    $openSecurity = Get-UserInput "Open GitHub security settings in browser? (y/n)" "y"
    if ($openSecurity -eq "y" -or $openSecurity -eq "Y") {
        Open-URL "https://github.com/$Repository/settings/security" "GitHub Security settings"
    }
    
    Write-Host ""
    Write-Host "📚 Security Features Guide:" -ForegroundColor Cyan
    Write-Host "   1. Dependabot alerts: Monitor dependencies for vulnerabilities" -ForegroundColor White
    Write-Host "   2. Code scanning: Static analysis for security issues" -ForegroundColor White
    Write-Host "   3. Security advisories: Coordinate vulnerability disclosures" -ForegroundColor White
    Write-Host "   4. Branch protection: Require reviews and status checks" -ForegroundColor White
}

Write-Host ""

# Step 4: Verification
Write-Host "🔍 Step 4: Verify Setup" -ForegroundColor Yellow
Write-Host "=======================" -ForegroundColor Yellow

$verifySetup = Get-UserInput "Do you want to verify the setup now? (y/n)" "y"
if ($verifySetup -eq "y" -or $verifySetup -eq "Y") {
    Write-Host ""
    Write-Host "🔍 Running verification..." -ForegroundColor Green
    
    # Run verification script
    $verifyScript = ".\scripts\verify-security-setup.ps1"
    if (Test-Path $verifyScript) {
        & $verifyScript -Repository $Repository -Organization $Organization
    } else {
        Write-Host "⚠️  Verification script not found. Please run it manually." -ForegroundColor Yellow
    }
}

Write-Host ""

# Step 5: Test Workflow
Write-Host "🧪 Step 5: Test Security Workflows" -ForegroundColor Yellow
Write-Host "===================================" -ForegroundColor Yellow

$testWorkflow = Get-UserInput "Do you want to test security workflows now? (y/n)" "n"
if ($testWorkflow -eq "y" -or $testWorkflow -eq "Y") {
    Write-Host ""
    Write-Host "📝 To test security workflows:" -ForegroundColor White
    Write-Host "   1. Create a test branch: git checkout -b test-security-setup" -ForegroundColor White
    Write-Host "   2. Make a small change and push: git push origin test-security-setup" -ForegroundColor White
    Write-Host "   3. Create a pull request" -ForegroundColor White
    Write-Host "   4. Check the Actions tab for security scans" -ForegroundColor White
    Write-Host "   5. Verify security team is notified for review" -ForegroundColor White
    Write-Host ""
    
    $openActions = Get-UserInput "Open GitHub Actions page in browser? (y/n)" "n"
    if ($openActions -eq "y" -or $openActions -eq "Y") {
        Open-URL "https://github.com/$Repository/actions" "GitHub Actions page"
    }
}

Write-Host ""

# Summary
Write-Host "📋 Setup Summary" -ForegroundColor Green
Write-Host "===============" -ForegroundColor Green
Write-Host ""
Write-Host "✅ GitHub CLI authenticated" -ForegroundColor Green
Write-Host "✅ Security setup guidance provided" -ForegroundColor Green
Write-Host "✅ GitHub pages opened (if requested)" -ForegroundColor Green
Write-Host ""

Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host "==============" -ForegroundColor Cyan
Write-Host "1. Complete the manual configuration steps above" -ForegroundColor White
Write-Host "2. Run verification script: .\scripts\verify-security-setup.ps1" -ForegroundColor White
Write-Host "3. Test security workflows with a pull request" -ForegroundColor White
Write-Host "4. Review security documentation: GITHUB_SECURITY_SETUP.md" -ForegroundColor White
Write-Host ""

Write-Host "🔗 Useful Links:" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan
Write-Host "Repository: https://github.com/$Repository" -ForegroundColor White
Write-Host "Settings: https://github.com/$Repository/settings" -ForegroundColor White
Write-Host "Security: https://github.com/$Repository/settings/security" -ForegroundColor White
Write-Host "Actions: https://github.com/$Repository/actions" -ForegroundColor White
Write-Host "Teams: https://github.com/$Organization/teams" -ForegroundColor White

Write-Host ""
Write-Host "🎉 Quick setup complete!" -ForegroundColor Green
Write-Host "Follow the steps above to complete your security configuration." -ForegroundColor White
