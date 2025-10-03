# GitHub Security Setup Script for Iterum Culinary App
# This script helps configure GitHub security features and provides setup guidance

param(
    [string]$Repository = "Iterum-Foods/iterum-chef-notebook",
    [string]$Organization = "Iterum-Foods",
    [switch]$Help
)

if ($Help) {
    Write-Host @"
GitHub Security Setup Script

This script provides guidance and automation for setting up GitHub security features
for the Iterum Culinary App.

Usage:
    .\setup-github-security.ps1 [options]

Options:
    -Repository <repo>    GitHub repository (default: Iterum-Foods/iterum-chef-notebook)
    -Organization <org>   GitHub organization (default: Iterum-Foods)
    -Help                Show this help message

Examples:
    .\setup-github-security.ps1
    .\setup-github-security.ps1 -Repository "MyOrg/MyRepo"
    .\setup-github-security.ps1 -Help

"@
    exit 0
}

Write-Host "🔐 GitHub Security Setup for Iterum Culinary App" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""

# Check if GitHub CLI is installed
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghInstalled) {
    Write-Host "⚠️  GitHub CLI (gh) not found. Please install it for automated setup." -ForegroundColor Yellow
    Write-Host "   Download from: https://cli.github.com/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 Manual Setup Required:" -ForegroundColor Cyan
    Write-Host "   1. Follow the guide in GITHUB_SECURITY_SETUP.md" -ForegroundColor White
    Write-Host "   2. Configure secrets manually in GitHub repository settings" -ForegroundColor White
    Write-Host "   3. Set up security teams and enable security features" -ForegroundColor White
    exit 1
}

# Check if user is authenticated with GitHub CLI
$authStatus = gh auth status 2>&1
if ($authStatus -match "not logged in") {
    Write-Host "🔑 Please authenticate with GitHub CLI first:" -ForegroundColor Yellow
    Write-Host "   Run: gh auth login" -ForegroundColor White
    exit 1
}

Write-Host "✅ GitHub CLI authenticated" -ForegroundColor Green
Write-Host ""

# Function to check if a secret exists
function Test-GitHubSecret {
    param([string]$SecretName)
    $secrets = gh secret list --repo $Repository 2>$null
    return $secrets -match $SecretName
}

# Function to check if a team exists
function Test-GitHubTeam {
    param([string]$TeamName)
    $teams = gh api orgs/$Organization/teams 2>$null | ConvertFrom-Json
    return $teams.name -contains $TeamName
}

# Function to check repository settings
function Test-RepositorySetting {
    param([string]$Setting)
    $repo = gh api repos/$Repository 2>$null | ConvertFrom-Json
    return $repo.$Setting
}

Write-Host "🔍 Checking current configuration..." -ForegroundColor Cyan
Write-Host ""

# Check secrets
Write-Host "📋 Checking GitHub Secrets:" -ForegroundColor Yellow
$secrets = @("SNYK_TOKEN", "SLACK_WEBHOOK_URL")
foreach ($secret in $secrets) {
    if (Test-GitHubSecret -SecretName $secret) {
        Write-Host "   ✅ $secret - Configured" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $secret - Not configured" -ForegroundColor Red
    }
}

Write-Host ""

# Check teams
Write-Host "👥 Checking GitHub Teams:" -ForegroundColor Yellow
$teams = @("security-team", "maintainers", "backend-team", "frontend-team", "devops-team")
foreach ($team in $teams) {
    if (Test-GitHubTeam -TeamName $team) {
        Write-Host "   ✅ $team - Exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $team - Not found" -ForegroundColor Red
    }
}

Write-Host ""

# Check repository settings
Write-Host "⚙️  Checking Repository Settings:" -ForegroundColor Yellow
$repo = gh api repos/$Repository 2>$null | ConvertFrom-Json
if ($repo) {
    Write-Host "   ✅ Repository accessible" -ForegroundColor Green
    Write-Host "   📊 Visibility: $($repo.visibility)" -ForegroundColor White
    Write-Host "   🔒 Private: $($repo.private)" -ForegroundColor White
} else {
    Write-Host "   ❌ Cannot access repository" -ForegroundColor Red
}

Write-Host ""

# Provide setup guidance
Write-Host "📋 Setup Instructions:" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. 🔐 Configure GitHub Secrets:" -ForegroundColor Yellow
Write-Host "   Go to: https://github.com/$Repository/settings/secrets/actions" -ForegroundColor White
Write-Host "   Add the following secrets:" -ForegroundColor White
Write-Host "   - SNYK_TOKEN: Get from https://snyk.io (Account Settings → API Token)" -ForegroundColor White
Write-Host "   - SLACK_WEBHOOK_URL: Get from Slack (Apps → Incoming Webhooks)" -ForegroundColor White
Write-Host ""

Write-Host "2. 👥 Create Security Teams:" -ForegroundColor Yellow
Write-Host "   Go to: https://github.com/$Organization/teams" -ForegroundColor White
Write-Host "   Create teams: security-team, maintainers, backend-team, frontend-team, devops-team" -ForegroundColor White
Write-Host ""

Write-Host "3. 🛡️  Enable Security Features:" -ForegroundColor Yellow
Write-Host "   Go to: https://github.com/$Repository/settings/security" -ForegroundColor White
Write-Host "   Enable: Dependabot alerts, Code scanning, Security advisories" -ForegroundColor White
Write-Host ""

Write-Host "4. 🔒 Configure Branch Protection:" -ForegroundColor Yellow
Write-Host "   Go to: https://github.com/$Repository/settings/branches" -ForegroundColor White
Write-Host "   Add protection rules for 'main' branch" -ForegroundColor White
Write-Host ""

Write-Host "5. 📚 Read Complete Guide:" -ForegroundColor Yellow
Write-Host "   See: GITHUB_SECURITY_SETUP.md for detailed instructions" -ForegroundColor White
Write-Host ""

# Offer to open URLs
$openUrls = Read-Host "Would you like to open the GitHub repository settings in your browser? (y/n)"
if ($openUrls -eq "y" -or $openUrls -eq "Y") {
    Write-Host "🌐 Opening GitHub repository settings..." -ForegroundColor Green
    
    # Open repository settings
    Start-Process "https://github.com/$Repository/settings"
    
    # Wait a moment
    Start-Sleep 2
    
    # Open security settings
    Start-Process "https://github.com/$Repository/settings/security"
    
    # Wait a moment
    Start-Sleep 2
    
    # Open teams page
    Start-Process "https://github.com/$Organization/teams"
    
    Write-Host "✅ Opened GitHub settings in your browser" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Setup guidance complete!" -ForegroundColor Green
Write-Host "Follow the instructions above to complete the security setup." -ForegroundColor White
Write-Host ""
Write-Host "📞 Need help? Create an issue in the repository or contact the security team." -ForegroundColor Cyan
