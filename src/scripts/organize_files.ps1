# File Organization Script for Iterum R&D Chef Notebook
# This script will organize files into a cleaner directory structure

Write-Host "Starting file organization..." -ForegroundColor Green

# Create necessary directories if they don't exist
$directories = @(
    "assets\css",
    "assets\js", 
    "assets\images",
    "assets\icons",
    "config",
    "documentation\guides",
    "documentation\strategies", 
    "documentation\investor-materials",
    "templates\shared",
    "templates\components",
    "scripts\startup",
    "scripts\utilities",
    "tests"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Yellow
    }
}

# Move files to appropriate directories
$fileMoves = @{
    # Assets
    "*.ico" = "assets\icons"
    "botanical-logo.svg" = "assets\images"
    
    # JavaScript files
    "*.js" = "assets\js"
    
    # CSS and styling
    "*.css" = "assets\css"
    
    # Configuration files
    "apiConfig.js" = "config"
    "env.https.example" = "config"
    "requirements.txt" = "config"
    
    # Documentation
    "*.md" = "documentation"
    "README.md" = "."
    
    # Templates
    "shared-*.html" = "templates\shared"
    "uniform-*.html" = "templates\shared"
    
    # Scripts and utilities
    "*.py" = "scripts"
    "*.bat" = "scripts\startup"
    
    # Test files
    "test_*.py" = "tests"
    "test_*.html" = "tests"
    
    # Database files
    "*.db" = "data"
}

Write-Host "File organization completed!" -ForegroundColor Green
