# SmartDoc - AI-Powered Document Analyzer 🤖📄

An intelligent document analysis application that automatically extracts summaries, key points, and performs sentiment analysis on PDF and text documents using advanced NLP techniques.

## ✨ Features

- **🔐 Secure Authentication**: JWT-based user authentication with role-based access control
- **📄 Document Upload**: Support for PDF and TXT files (up to 16MB)
- **🤖 AI-Powered Analysis**:
  - Automatic text extraction from documents
  - Smart summarization using BART transformer model
  - Key points extraction using spaCy NLP
  - Sentiment analysis with confidence scores
- **📊 Beautiful Dashboard**: Modern, responsive UI with real-time statistics
- **👨‍💼 Admin Panel**: Complete user and document management
- **🎨 Sweet Alerts**: Elegant notifications and confirmations
- **💾 Persistent Storage**: SQLite database for all data

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database
- **Flask-JWT-Extended** - Authentication
- **spaCy** - NLP processing
- **Transformers (Hugging Face)** - Summarization & sentiment analysis
- **PyPDF2** - PDF text extraction
- **bcrypt** - Password hashing

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript (ES6+)** - Client-side logic
- **SweetAlert2** - Beautiful alerts
- **Font Awesome** - Icons

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone or Navigate to the Project Directory

```powershell
cd "c:\Users\jayan\OneDrive\Desktop\SmartDOC"
```

### 2. Create a Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you encounter an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Download spaCy Language Model

```powershell
python -m spacy download en_core_web_sm
```

### 6. Configure Environment Variables

Copy `.env.example` to `.env` and update with your settings:

```powershell
Copy-Item .env.example .env
```

Edit `.env` file and update:
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URI=sqlite:///smartdoc.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
ADMIN_EMAIL=admin@smartdoc.com
ADMIN_PASSWORD=admin123
```

### 7. Run the Application

```powershell
python app.py
```

The application will be available at: **http://localhost:5000**

## 📖 Usage

### Default Admin Credentials
- **Email**: admin@smartdoc.com
- **Password**: admin123

⚠️ **Important**: Change the admin password after first login!

### For Regular Users

1. **Register**: Go to http://localhost:5000 and click "Register here"
2. **Login**: Use your credentials to access the dashboard
3. **Upload Documents**: 
   - Drag & drop or click to browse
   - Supports PDF and TXT files (max 16MB)
4. **View Analysis**:
   - Summary of the document
   - Key points extracted
   - Sentiment analysis with score
   - Word count

### For Administrators

1. **Login** with admin credentials
2. **Access Admin Dashboard**: Automatically redirected
3. **Manage Users**: View and delete users
4. **Monitor Documents**: View all documents across users
5. **View Analytics**: System statistics and sentiment distribution

## 📁 Project Structure

```
SmartDOC/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── utils.py               # NLP and document processing utilities
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── static/               # Frontend files
│   ├── index.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── admin.html        # Admin dashboard
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       ├── config.js     # API configuration
│       ├── auth.js       # Authentication helpers
│       ├── dashboard.js  # Dashboard logic
│       └── admin.js      # Admin panel logic
└── uploads/              # Uploaded documents (created automatically)
```

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with 24-hour expiration
- **Role-Based Access**: Separate user and admin permissions
- **Input Validation**: Server-side and client-side validation
- **File Type Validation**: Only PDF and TXT files allowed
- **File Size Limits**: Maximum 16MB per file

## 🎨 UI Features

- **Modern Design**: Gradient backgrounds and smooth animations
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Cards**: Hover effects and transitions
- **Sweet Alerts**: Beautiful confirmation and notification dialogs
- **Loading Indicators**: Progress feedback during operations
- **Empty States**: Helpful messages when no data available

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Documents
- `POST /api/documents/upload` - Upload and analyze document
- `GET /api/documents` - Get user's documents
- `GET /api/documents/<id>` - Get specific document
- `DELETE /api/documents/<id>` - Delete document

### Admin (Admin Only)
- `GET /api/admin/users` - Get all users
- `GET /api/admin/documents` - Get all documents
- `GET /api/admin/stats` - Get system statistics
- `DELETE /api/admin/users/<id>` - Delete user

## 🧪 Testing the Application

1. **Register a new user**
2. **Upload a sample PDF or TXT file**
3. **View the analysis results**:
   - Check the summary quality
   - Review extracted key points
   - Verify sentiment analysis
4. **Test admin features** (login as admin):
   - View all users and documents
   - Check analytics dashboard
   - Test user deletion

## 🐛 Troubleshooting

### Model Download Issues
If transformers models fail to download automatically:
```powershell
# They will download on first use, ensure internet connection
```

### spaCy Model Not Found
```powershell
python -m spacy download en_core_web_sm
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Database Issues
Delete the database file and restart:
```powershell
Remove-Item smartdoc.db
python app.py
```

## 🚀 Deployment Tips

### For Production:

1. **Change Secret Keys**: Update all secret keys in `.env`
2. **Disable Debug Mode**: Set `debug=False` in `app.py`
3. **Use Production Database**: Consider PostgreSQL instead of SQLite
4. **Use HTTPS**: Enable SSL/TLS
5. **Set File Upload Limits**: Configure based on server capacity
6. **Use Production Server**: Deploy with Gunicorn or uWSGI

## 📝 Future Enhancements

- 📧 Email notifications
- 🔄 Document versioning
- 📑 Support for DOCX files
- 🌐 Multi-language support
- 📈 Advanced analytics and charts
- 🔍 Full-text search
- 💾 Cloud storage integration
- 🤝 Collaboration features

## 👨‍💻 Developer

Built with ❤️ for the Hackathon

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- Hugging Face for transformer models
- spaCy for NLP capabilities
- Bootstrap team for UI framework
- SweetAlert2 for beautiful alerts

---

**Happy Analyzing! 🎉**
