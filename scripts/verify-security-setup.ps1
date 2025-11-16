# Security Setup Verification Script for Iterum Culinary App
# This script verifies that all security features are properly configured

param(
    [string]$Repository = "Iterum-Foods/iterum-chef-notebook",
    [string]$Organization = "Iterum-Foods",
    [switch]$Detailed
)

Write-Host "🔍 Security Setup Verification for Iterum Culinary App" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""

# Check if GitHub CLI is installed
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghInstalled) {
    Write-Host "❌ GitHub CLI (gh) not found. Cannot verify setup automatically." -ForegroundColor Red
    Write-Host "   Please install GitHub CLI: https://cli.github.com/" -ForegroundColor Yellow
    exit 1
}

# Check authentication
$authStatus = gh auth status 2>&1
if ($authStatus -match "not logged in") {
    Write-Host "❌ Not authenticated with GitHub CLI. Run: gh auth login" -ForegroundColor Red
    exit 1
}

Write-Host "✅ GitHub CLI authenticated" -ForegroundColor Green
Write-Host ""

# Verification results
$results = @{
    Secrets = @{}
    Teams = @{}
    Repository = @{}
    SecurityFeatures = @{}
    Workflows = @{}
}

# Function to check if a secret exists
function Test-GitHubSecret {
    param([string]$SecretName)
    try {
        $secrets = gh secret list --repo $Repository 2>$null
        return $secrets -match $SecretName
    } catch {
        return $false
    }
}

# Function to check if a team exists
function Test-GitHubTeam {
    param([string]$TeamName)
    try {
        $teams = gh api orgs/$Organization/teams 2>$null | ConvertFrom-Json
        return $teams.name -contains $TeamName
    } catch {
        return $false
    }
}

# Function to check repository settings
function Get-RepositoryInfo {
    try {
        $repo = gh api repos/$Repository 2>$null | ConvertFrom-Json
        return $repo
    } catch {
        return $null
    }
}

# Function to check if a workflow exists
function Test-WorkflowExists {
    param([string]$WorkflowName)
    try {
        $workflows = gh api repos/$Repository/actions/workflows 2>$null | ConvertFrom-Json
        return $workflows.workflows.name -contains $WorkflowName
    } catch {
        return $false
    }
}

Write-Host "🔐 Checking GitHub Secrets..." -ForegroundColor Cyan
$secrets = @("SNYK_TOKEN", "SLACK_WEBHOOK_URL")
foreach ($secret in $secrets) {
    $exists = Test-GitHubSecret -SecretName $secret
    $results.Secrets[$secret] = $exists
    if ($exists) {
        Write-Host "   ✅ $secret - Configured" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $secret - Not configured" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "👥 Checking GitHub Teams..." -ForegroundColor Cyan
$teams = @("security-team", "maintainers", "backend-team", "frontend-team", "devops-team")
foreach ($team in $teams) {
    $exists = Test-GitHubTeam -TeamName $team
    $results.Teams[$team] = $exists
    if ($exists) {
        Write-Host "   ✅ $team - Exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $team - Not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📁 Checking Repository..." -ForegroundColor Cyan
$repo = Get-RepositoryInfo
if ($repo) {
    $results.Repository["Accessible"] = $true
    $results.Repository["Visibility"] = $repo.visibility
    $results.Repository["Private"] = $repo.private
    Write-Host "   ✅ Repository accessible" -ForegroundColor Green
    Write-Host "   📊 Visibility: $($repo.visibility)" -ForegroundColor White
    Write-Host "   🔒 Private: $($repo.private)" -ForegroundColor White
} else {
    $results.Repository["Accessible"] = $false
    Write-Host "   ❌ Cannot access repository" -ForegroundColor Red
}

Write-Host ""
Write-Host "⚙️  Checking GitHub Workflows..." -ForegroundColor Cyan
$workflows = @("CI/CD Pipeline - Iterum Culinary App", "Deploy Iterum Culinary App", "Automated Dependency Updates", "Comprehensive Security Scan")
foreach ($workflow in $workflows) {
    $exists = Test-WorkflowExists -WorkflowName $workflow
    $results.Workflows[$workflow] = $exists
    if ($exists) {
        Write-Host "   ✅ $workflow - Exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $workflow - Not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📋 Checking Security Files..." -ForegroundColor Cyan
$securityFiles = @("SECURITY.md", "CODEOWNERS", ".github/dependabot.yml", "SECURITY_IMPLEMENTATION_SUMMARY.md")
foreach ($file in $securityFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file - Exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file - Not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📊 Verification Summary" -ForegroundColor Yellow
Write-Host "======================" -ForegroundColor Yellow

# Calculate scores
$totalChecks = 0
$passedChecks = 0

# Secrets
$totalChecks += $results.Secrets.Count
$passedChecks += ($results.Secrets.Values | Where-Object { $_ -eq $true }).Count

# Teams
$totalChecks += $results.Teams.Count
$passedChecks += ($results.Teams.Values | Where-Object { $_ -eq $true }).Count

# Repository
$totalChecks += 1
if ($results.Repository["Accessible"]) { $passedChecks += 1 }

# Workflows
$totalChecks += $results.Workflows.Count
$passedChecks += ($results.Workflows.Values | Where-Object { $_ -eq $true }).Count

# Security files
$totalChecks += $securityFiles.Count
$passedChecks += ($securityFiles | Where-Object { Test-Path $_ }).Count

$score = if ($totalChecks -gt 0) { [math]::Round(($passedChecks / $totalChecks) * 100, 1) } else { 0 }

Write-Host "Overall Score: $passedChecks/$totalChecks ($score%)" -ForegroundColor $(if ($score -ge 80) { "Green" } elseif ($score -ge 60) { "Yellow" } else { "Red" })

Write-Host ""
if ($score -ge 80) {
    Write-Host "🎉 Excellent! Your security setup is well configured." -ForegroundColor Green
} elseif ($score -ge 60) {
    Write-Host "⚠️  Good progress, but some improvements needed." -ForegroundColor Yellow
} else {
    Write-Host "❌ Security setup needs significant work." -ForegroundColor Red
}

Write-Host ""

# Detailed recommendations
if ($Detailed) {
    Write-Host "📋 Detailed Recommendations:" -ForegroundColor Cyan
    Write-Host "============================" -ForegroundColor Cyan
    
    # Secrets recommendations
    $missingSecrets = $results.Secrets.GetEnumerator() | Where-Object { $_.Value -eq $false }
    if ($missingSecrets) {
        Write-Host ""
        Write-Host "🔐 Missing Secrets:" -ForegroundColor Yellow
        foreach ($secret in $missingSecrets) {
            Write-Host "   - $($secret.Key): Add to repository settings" -ForegroundColor White
        }
    }
    
    # Teams recommendations
    $missingTeams = $results.Teams.GetEnumerator() | Where-Object { $_.Value -eq $false }
    if ($missingTeams) {
        Write-Host ""
        Write-Host "👥 Missing Teams:" -ForegroundColor Yellow
        foreach ($team in $missingTeams) {
            Write-Host "   - $($team.Key): Create in organization settings" -ForegroundColor White
        }
    }
    
    # Workflows recommendations
    $missingWorkflows = $results.Workflows.GetEnumerator() | Where-Object { $_.Value -eq $false }
    if ($missingWorkflows) {
        Write-Host ""
        Write-Host "⚙️  Missing Workflows:" -ForegroundColor Yellow
        foreach ($workflow in $missingWorkflows) {
            Write-Host "   - $($workflow.Key): Check workflow files" -ForegroundColor White
        }
    }
}

Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host "==============" -ForegroundColor Cyan
Write-Host "1. Review the setup guide: GITHUB_SECURITY_SETUP.md" -ForegroundColor White
Write-Host "2. Configure missing secrets and teams" -ForegroundColor White
Write-Host "3. Enable security features in repository settings" -ForegroundColor White
Write-Host "4. Test security workflows with a pull request" -ForegroundColor White
Write-Host "5. Run this verification script again" -ForegroundColor White

Write-Host ""
Write-Host "🔗 Useful Links:" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan
Write-Host "Repository Settings: https://github.com/$Repository/settings" -ForegroundColor White
Write-Host "Security Settings: https://github.com/$Repository/settings/security" -ForegroundColor White
Write-Host "Teams: https://github.com/$Organization/teams" -ForegroundColor White
Write-Host "Actions: https://github.com/$Repository/actions" -ForegroundColor White

Write-Host ""
Write-Host "✅ Verification complete!" -ForegroundColor Green
