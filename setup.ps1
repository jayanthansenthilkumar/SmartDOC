# SmartDoc Setup Script for Windows PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SmartDoc Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed. Please install Python 3.8 or higher." -ForegroundColor Red
    exit
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "`nInstalling Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Download spaCy model
Write-Host "`nDownloading spaCy language model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm

# Create uploads directory
Write-Host "`nCreating uploads directory..." -ForegroundColor Yellow
if (!(Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads"
    Write-Host "✓ Uploads directory created" -ForegroundColor Green
} else {
    Write-Host "✓ Uploads directory already exists" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nTo run the application:" -ForegroundColor Yellow
Write-Host "  1. Ensure virtual environment is activated" -ForegroundColor White
Write-Host "  2. Run: python app.py" -ForegroundColor White
Write-Host "  3. Open browser at: http://localhost:5000" -ForegroundColor White
Write-Host "`nDefault Admin Login:" -ForegroundColor Yellow
Write-Host "  Email: admin@smartdoc.com" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host "`n⚠️  Remember to change admin password after first login!" -ForegroundColor Red
Write-Host ""
