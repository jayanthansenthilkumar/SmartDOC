# 🎯 INSTALLATION & RUNNING GUIDE

## 📋 Current Status

✅ Virtual environment created
✅ Flask and core dependencies installed
✅ Project structure complete
✅ Database models ready
✅ Frontend files ready
✅ Uploads directory created

## ⚠️ IMPORTANT - Complete Installation

You still need to install the AI/NLP libraries. You have two options:

### Option A: Quick Test (Without AI Features)

Run the app now to test the interface and basic upload:

```powershell
python app.py
```

Then open: http://localhost:5000

**Note:** Document analysis will show fallback messages until you install the AI models.

### Option B: Full Installation (With AI Features) - RECOMMENDED

Install the AI libraries now:

```powershell
# Install spaCy (REQUIRED for key points extraction)
pip install spacy
python -m spacy download en_core_web_sm

# Install Transformers for AI summarization (Large download ~2GB)
pip install transformers torch sentencepiece
```

This will take 10-15 minutes to download (~2GB total).

After installation, run:

```powershell
python app.py
```

---

## 🚀 Running the Application

### Step 1: Ensure Virtual Environment is Active

You should see `(venv)` in your PowerShell prompt. If not:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 2: Start the Server

```powershell
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
 * Debugger is active!
```

### Step 3: Open Your Browser

Navigate to: **http://localhost:5000**

---

## 🔑 First Login

**Admin Credentials:**
- Email: `admin@smartdoc.com`
- Password: `admin123`

**Or create a new user:**
- Click "Register here" on the login page
- Fill in your details
- Start uploading documents!

---

## 📤 Testing Document Upload

1. **Login** to the dashboard
2. **Click** the upload zone or drag & drop
3. **Upload** the sample file: `sample_document.txt`
4. **Wait** for analysis (30-60 seconds first time)
5. **View** the results!

---

## 🎨 What You'll See

### Login Page
- Beautiful gradient background
- Clean login form
- Link to registration

### User Dashboard
- Statistics cards (total docs, sentiment breakdown)
- Drag & drop upload zone
- Document cards with:
  - Summary
  - Key points
  - Sentiment analysis
  - Word count

### Admin Dashboard (login as admin)
- System statistics
- User management table
- All documents overview
- Analytics charts

---

## 🐛 Troubleshooting

### Error: "Port 5000 already in use"
Edit `app.py`, line at the bottom:
```python
app.run(debug=True, port=5001)  # Change to 5001
```

### Error: "ModuleNotFoundError: No module named 'spacy'"
Install spaCy:
```powershell
pip install spacy
python -m spacy download en_core_web_sm
```

### Error: "ModuleNotFoundError: No module named 'transformers'"
You can run without transformers (basic features work), or install:
```powershell
pip install transformers torch
```

### Database Issues
Delete the database and restart:
```powershell
Remove-Item smartdoc.db -ErrorAction SilentlyContinue
python app.py
```

---

## 📊 Features to Test

✅ User Registration
✅ User Login
✅ Admin Login
✅ Document Upload (drag & drop)
✅ Document Analysis
✅ View Summaries
✅ View Key Points
✅ Sentiment Analysis
✅ Delete Documents
✅ Admin - View Users
✅ Admin - View All Documents
✅ Admin - System Statistics
✅ Admin - Delete Users
✅ SweetAlert Notifications

---

## 🎯 Next Steps

1. **Install AI models** (if not done)
2. **Run the application**
3. **Test all features**
4. **Customize if needed** (colors, text, etc.)
5. **Prepare for demo**

---

## 📞 Quick Commands Reference

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install AI models (if needed)
pip install spacy transformers torch sentencepiece
python -m spacy download en_core_web_sm

# Run the application
python app.py

# Deactivate virtual environment (when done)
deactivate
```

---

## ✨ You're Ready!

Everything is set up and ready to go. Just install the AI models and run the app!

**Good luck with your hackathon! 🏆**
