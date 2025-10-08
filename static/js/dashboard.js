// Protect page
if (!requireAuth()) {
    throw new Error('Not authenticated');
}

// Display user name
const user = getCurrentUser();
document.getElementById('userName').textContent = user.full_name;

// Upload zone handling
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');

uploadZone.addEventListener('click', () => {
    fileInput.click();
});

// Drag and drop
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

// Handle file upload
async function handleFileUpload(file) {
    // Validate file type
    const allowedTypes = ['application/pdf', 'text/plain'];
    if (!allowedTypes.includes(file.type)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid File Type',
            text: 'Please upload a PDF or TXT file'
        });
        return;
    }
    
    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        Swal.fire({
            icon: 'error',
            title: 'File Too Large',
            text: 'File size should not exceed 16MB'
        });
        return;
    }
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    
    // Show loading
    Swal.fire({
        title: 'Analyzing Document...',
        html: 'This may take a few moments<br><div class="spinner-border text-primary mt-3" role="status"></div>',
        allowOutsideClick: false,
        showConfirmButton: false
    });
    
    try {
        const response = await fetchWithAuth(`${API_URL}/api/documents/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            Swal.fire({
                icon: 'success',
                title: 'Success!',
                text: 'Document analyzed successfully',
                timer: 1500,
                showConfirmButton: false
            }).then(() => {
                // Reload documents
                loadDocuments();
                loadStats();
                fileInput.value = '';
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Upload Failed',
                text: data.error || 'Could not upload document'
            });
        }
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'An error occurred during upload'
        });
    }
}

// Load documents
async function loadDocuments() {
    try {
        const response = await fetchWithAuth(`${API_URL}/api/documents`);
        const data = await response.json();
        
        if (response.ok) {
            displayDocuments(data.documents);
        }
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

// Display documents
function displayDocuments(documents) {
    const container = document.getElementById('documentsContainer');
    
    if (documents.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-file-alt"></i>
                <h5>No documents yet</h5>
                <p>Upload your first document to get started!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = documents.map(doc => createDocumentCard(doc)).join('');
}

// Create document card
function createDocumentCard(doc) {
    const analysis = doc.analysis;
    
    if (!analysis) {
        return `
            <div class="card document-card fade-in">
                <div class="card-body">
                    <h5><i class="fas fa-file-${doc.file_type === 'pdf' ? 'pdf' : 'alt'}"></i> ${doc.filename}</h5>
                    <p class="text-muted">Uploaded: ${formatDate(doc.uploaded_at)}</p>
                    <p class="text-warning">Analysis pending or failed</p>
                    <button class="btn btn-danger btn-sm" onclick="deleteDocument(${doc.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        `;
    }
    
    const keyPoints = JSON.parse(analysis.key_points || '[]');
    const sentimentClass = `sentiment-${analysis.sentiment}`;
    
    return `
        <div class="card document-card fade-in mb-3">
            <div class="document-header">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <div class="document-icon">
                            <i class="fas fa-file-${doc.file_type === 'pdf' ? 'pdf' : 'alt'}"></i>
                        </div>
                        <h4 class="mb-2">${doc.filename}</h4>
                        <p class="mb-0"><i class="fas fa-calendar me-2"></i>${formatDate(doc.uploaded_at)}</p>
                        <p class="mb-0"><i class="fas fa-file-alt me-2"></i>${formatFileSize(doc.file_size)}</p>
                    </div>
                    <div class="col-md-4 text-end">
                        <span class="sentiment-badge ${sentimentClass}">
                            ${analysis.sentiment.toUpperCase()}
                            ${analysis.sentiment === 'positive' ? '😊' : analysis.sentiment === 'negative' ? '😞' : '😐'}
                        </span>
                        <p class="mt-2 mb-0">Score: ${analysis.sentiment_score}</p>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12 mb-3">
                        <h6><i class="fas fa-align-left me-2"></i>Summary</h6>
                        <p>${analysis.summary}</p>
                    </div>
                    
                    ${keyPoints.length > 0 ? `
                    <div class="col-md-12 mb-3">
                        <h6><i class="fas fa-list-ul me-2"></i>Key Points</h6>
                        <ul class="key-points-list">
                            ${keyPoints.map(point => `<li>${point}</li>`).join('')}
                        </ul>
                    </div>
                    ` : ''}
                    
                    <div class="col-md-12">
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-info">
                                <i class="fas fa-font me-1"></i>${analysis.word_count} words
                            </span>
                            <button class="btn btn-danger btn-sm" onclick="deleteDocument(${doc.id})">
                                <i class="fas fa-trash me-1"></i>Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Delete document
async function deleteDocument(docId) {
    const result = await Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#6366f1',
        confirmButtonText: 'Yes, delete it!'
    });
    
    if (result.isConfirmed) {
        try {
            const response = await fetchWithAuth(`${API_URL}/api/documents/${docId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Deleted!',
                    text: 'Document has been deleted.',
                    timer: 1500,
                    showConfirmButton: false
                }).then(() => {
                    loadDocuments();
                    loadStats();
                });
            } else {
                const data = await response.json();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.error || 'Could not delete document'
                });
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'An error occurred'
            });
        }
    }
}

// Load stats
async function loadStats() {
    try {
        const response = await fetchWithAuth(`${API_URL}/api/documents`);
        const data = await response.json();
        
        if (response.ok) {
            const documents = data.documents;
            const total = documents.length;
            let positive = 0, negative = 0, neutral = 0;
            
            documents.forEach(doc => {
                if (doc.analysis) {
                    if (doc.analysis.sentiment === 'positive') positive++;
                    else if (doc.analysis.sentiment === 'negative') negative++;
                    else neutral++;
                }
            });
            
            document.getElementById('totalDocs').textContent = total;
            document.getElementById('positiveDocs').textContent = positive;
            document.getElementById('neutralDocs').textContent = neutral;
            document.getElementById('negativeDocs').textContent = negative;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Initial load
loadDocuments();
loadStats();
