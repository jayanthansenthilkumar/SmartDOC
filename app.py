import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Document, Analysis
from utils import allowed_file, analyze_document
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Initialize database and create admin user
with app.app_context():
    db.create_all()
    
    # Create admin user if not exists
    admin = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
    if not admin:
        admin = User(
            email=app.config['ADMIN_EMAIL'],
            full_name='Admin User',
            is_admin=True
        )
        admin.set_password(app.config['ADMIN_PASSWORD'])
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created: {app.config['ADMIN_EMAIL']}")


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('static', 'index.html')


# ==================== AUTH ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not all(k in data for k in ['email', 'password', 'full_name']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            full_name=data['full_name'],
            is_admin=False
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== DOCUMENT ROUTES ====================

@app.route('/api/documents/upload', methods=['POST'])
@jwt_required()
def upload_document():
    """Upload and analyze a document"""
    try:
        user_id = get_jwt_identity()
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            return jsonify({'error': 'Invalid file type. Only PDF and TXT files are allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{user_id}_{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Get file info
        file_type = filename.rsplit('.', 1)[1].lower()
        file_size = os.path.getsize(file_path)
        
        # Create document record
        document = Document(
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            user_id=user_id
        )
        db.session.add(document)
        db.session.commit()
        
        # Analyze document
        try:
            analysis_results = analyze_document(file_path, file_type)
            
            # Create analysis record
            analysis = Analysis(
                document_id=document.id,
                extracted_text=analysis_results['extracted_text'][:10000],  # Store first 10k chars
                summary=analysis_results['summary'],
                key_points=analysis_results['key_points'],
                sentiment=analysis_results['sentiment'],
                sentiment_score=analysis_results['sentiment_score'],
                word_count=analysis_results['word_count']
            )
            db.session.add(analysis)
            db.session.commit()
            
            return jsonify({
                'message': 'Document uploaded and analyzed successfully',
                'document': document.to_dict()
            }), 201
            
        except Exception as e:
            # If analysis fails, still keep the document but return error
            return jsonify({
                'error': f'Document uploaded but analysis failed: {str(e)}',
                'document': document.to_dict()
            }), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents', methods=['GET'])
@jwt_required()
def get_documents():
    """Get all documents for current user"""
    try:
        user_id = get_jwt_identity()
        documents = Document.query.filter_by(user_id=user_id).order_by(Document.uploaded_at.desc()).all()
        
        return jsonify({
            'documents': [doc.to_dict() for doc in documents]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents/<int:doc_id>', methods=['GET'])
@jwt_required()
def get_document(doc_id):
    """Get a specific document"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        document = Document.query.get(doc_id)
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Check if user owns the document or is admin
        if document.user_id != user_id and not user.is_admin:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'document': document.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
@jwt_required()
def delete_document(doc_id):
    """Delete a document"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        document = Document.query.get(doc_id)
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Check if user owns the document or is admin
        if document.user_id != user_id and not user.is_admin:
            return jsonify({'error': 'Access denied'}), 403
        
        # Delete file from disk
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({'message': 'Document deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== ADMIN ROUTES ====================

@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        users = User.query.all()
        return jsonify({
            'users': [u.to_dict() for u in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/documents', methods=['GET'])
@jwt_required()
def get_all_documents():
    """Get all documents (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        documents = Document.query.order_by(Document.uploaded_at.desc()).all()
        return jsonify({
            'documents': [doc.to_dict() for doc in documents]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get system statistics (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        total_users = User.query.count()
        total_documents = Document.query.count()
        total_analyses = Analysis.query.count()
        
        # Sentiment breakdown
        positive_docs = Analysis.query.filter_by(sentiment='positive').count()
        negative_docs = Analysis.query.filter_by(sentiment='negative').count()
        neutral_docs = Analysis.query.filter_by(sentiment='neutral').count()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'total_documents': total_documents,
                'total_analyses': total_analyses,
                'sentiment_breakdown': {
                    'positive': positive_docs,
                    'negative': negative_docs,
                    'neutral': neutral_docs
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete a user (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prevent deleting yourself
        if user.id == current_user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        # Delete user's documents from disk
        for doc in user.documents:
            if os.path.exists(doc.file_path):
                os.remove(doc.file_path)
        
        # Delete user (cascade will delete documents and analyses)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
