# Quick Start Guide - SmartDoc

Follow these steps to get SmartDoc up and running!

## Option 1: Automated Setup (Recommended)

Run the setup script in PowerShell:

```powershell
.\setup.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run the setup script again.

## Option 2: Manual Setup

### Step 1: Create Virtual Environment
```powershell
python -m venv venv
```

### Step 2: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Download spaCy Model
```powershell
python -m spacy download en_core_web_sm
```

### Step 5: Create Uploads Directory
```powershell
New-Item -ItemType Directory -Path uploads -Force
```

## Running the Application

```powershell
python app.py
```

Open your browser and navigate to: **http://localhost:5000**

## Default Login Credentials

**Admin Account:**
- Email: `admin@smartdoc.com`
- Password: `admin123`

**⚠️ IMPORTANT**: Change the admin password after first login!

## First Steps

1. **Login** with admin credentials
2. **Register** a new user account (or use admin)
3. **Upload** a sample PDF or TXT document
4. **View** the AI-generated analysis!

## Test Files

Try uploading:
- Any PDF document (research papers, articles, reports)
- Text files (.txt)
- Max file size: 16MB

## Features to Try

✅ Document upload and instant analysis
✅ View summary and key points
✅ Check sentiment analysis
✅ Admin dashboard (login as admin)
✅ User management
✅ Document analytics

## Troubleshooting

**Problem**: Port 5000 already in use
**Solution**: Edit `app.py` and change the port:
```python
app.run(debug=True, port=5001)
```

**Problem**: Models not downloading
**Solution**: Ensure you have internet connection. Models download on first use.

**Problem**: Database errors
**Solution**: Delete `smartdoc.db` and restart the application.

## Need Help?

Check the full README.md for detailed documentation and troubleshooting.

---

Happy Analyzing! 🚀
