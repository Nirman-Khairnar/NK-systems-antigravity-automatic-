$ErrorActionPreference = "Stop"

Write-Host "Starting Auto-Sync to GitHub..." -ForegroundColor Cyan

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..."
    git init
}

# Add all files
Write-Host "Adding files..."
git add .

# Commit
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "Committing changes..."
try {
    git commit -m "Auto-sync: $timestamp"
} catch {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}

# Check for remote
$remote = git remote get-url origin 2>$null
if (-not $remote) {
    Write-Host "CRITICAL: No remote repository configured." -ForegroundColor Red
    Write-Host "Please run: git remote add origin <YOUR_GITHUB_REPO_URL>" -ForegroundColor Yellow
    exit 1
}

# Push
Write-Host "Pushing to GitHub..."
git push -u origin main

Write-Host "Sync Complete!" -ForegroundColor Green
