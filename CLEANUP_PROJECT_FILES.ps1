# Iterum Culinary App - Cleanup Script
# Moves files from other projects to archive folders

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Iterum App Cleanup - Moving Other Projects" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$rootDir = Get-Location

# Create archive folders if they don't exist
$archivesPath = Join-Path $rootDir "archive-other-projects"
if (!(Test-Path $archivesPath)) {
    New-Item -ItemType Directory -Path $archivesPath | Out-Null
}

# USTA Files
$ustaArchive = Join-Path $archivesPath "usta-files"
if (!(Test-Path $ustaArchive)) {
    New-Item -ItemType Directory -Path $ustaArchive | Out-Null
}

# Find and move USTA files from root
Get-ChildItem -Path $rootDir -File | Where-Object { 
    $_.Name -match "usta|USTA" -and 
    $_.Name -match "\.(bat|json|txt|md|html)$" 
} | ForEach-Object {
    Write-Host "Moving: $($_.Name)" -ForegroundColor Yellow
    Move-Item -Path $_.FullName -Destination $ustaArchive -Force
}

# Old Test Files
$testArchive = Join-Path $archivesPath "old-test-files"
if (!(Test-Path $testArchive)) {
    New-Item -ItemType Directory -Path $testArchive | Out-Null
}

# Move old test and demo HTML files
Get-ChildItem -Path $rootDir -File | Where-Object { 
    ($_.Name -match "^test_|^demo_|^debug_" -or $_.Name -like "*demo*") -and
    $_.LastWriteTime -lt (Get-Date).AddDays(-30)
} | ForEach-Object {
    Write-Host "Moving: $($_.Name)" -ForegroundColor Yellow
    Move-Item -Path $_.FullName -Destination $testArchive -Force
}

# Old documentation
$docArchive = Join-Path $archivesPath "old-docs"
if (!(Test-Path $docArchive)) {
    New-Item -ItemType Directory -Path $docArchive | Out-Null
}

# Move very old documentation files (older than 60 days)
Get-ChildItem -Path $rootDir -File | Where-Object { 
    $_.Name -match "\.md$" -and
    $_.LastWriteTime -lt (Get-Date).AddDays(-60)
} | ForEach-Object {
    Write-Host "Moving: $($_.Name)" -ForegroundColor Yellow
    Move-Item -Path $_.FullName -Destination $docArchive -Force
}

Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Files moved to: $archivesPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

