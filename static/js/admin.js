// Protect admin page
if (!requireAdmin()) {
    throw new Error('Not authorized');
}

// Display user name
const user = getCurrentUser();
document.getElementById('userName').textContent = user.full_name;

// Sidebar toggle
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.querySelector('.sidebar');
const mainContent = document.querySelector('.main-content');

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
});

// Navigation
const navLinks = document.querySelectorAll('.nav-link');
const contentSections = document.querySelectorAll('.content-section');

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = link.getAttribute('data-section');
        
        // Update active link
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Show target section
        contentSections.forEach(section => {
            section.classList.remove('active');
        });
        
        const targetSection = document.getElementById(target + 'Section');
        if (targetSection) {
            targetSection.classList.add('active');
        }
    });
});

// Load all data
loadStats();
loadUsers();
loadDocuments();

// Load statistics
async function loadStats() {
    try {
        const response = await fetchWithAuth(`${API_URL}/api/admin/stats`);
        const data = await response.json();
        
        if (response.ok) {
            const stats = data.stats;
            
            // Update stat cards
            document.getElementById('totalUsers').textContent = stats.total_users;
            document.getElementById('totalDocs').textContent = stats.total_documents;
            document.getElementById('totalAnalyses').textContent = stats.total_analyses;
            document.getElementById('positiveDocs').textContent = stats.sentiment_breakdown.positive;
            
            // Update user count badge
            document.getElementById('userCount').textContent = `${stats.total_users} users`;
            
            // Update document count badge
            document.getElementById('docCount').textContent = `${stats.total_documents} documents`;
            
            // Update sentiment progress bars
            const total = stats.total_documents || 1; // Avoid division by zero
            const positivePercent = Math.round((stats.sentiment_breakdown.positive / total) * 100);
            const neutralPercent = Math.round((stats.sentiment_breakdown.neutral / total) * 100);
            const negativePercent = Math.round((stats.sentiment_breakdown.negative / total) * 100);
            
            document.getElementById('positiveBar').style.width = positivePercent + '%';
            document.getElementById('positiveBar').textContent = `${stats.sentiment_breakdown.positive} (${positivePercent}%)`;
            
            document.getElementById('neutralBar').style.width = neutralPercent + '%';
            document.getElementById('neutralBar').textContent = `${stats.sentiment_breakdown.neutral} (${neutralPercent}%)`;
            
            document.getElementById('negativeBar').style.width = negativePercent + '%';
            document.getElementById('negativeBar').textContent = `${stats.sentiment_breakdown.negative} (${negativePercent}%)`;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load users
async function loadUsers() {
    try {
        const response = await fetchWithAuth(`${API_URL}/api/admin/users`);
        const data = await response.json();
        
        if (response.ok) {
            displayUsers(data.users);
        }
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

// Display users
function displayUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No users found</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.id}</td>
            <td>${user.full_name}</td>
            <td>${user.email}</td>
            <td>
                ${user.is_admin 
                    ? '<span class="badge bg-danger">Admin</span>' 
                    : '<span class="badge bg-primary">User</span>'}
            </td>
            <td>${formatDate(user.created_at)}</td>
            <td>
                ${!user.is_admin 
                    ? `<button class="btn btn-danger btn-sm" onclick="deleteUser(${user.id})">
                        <i class="fas fa-trash"></i>
                    </button>` 
                    : '<span class="text-muted">Protected</span>'}
            </td>
        </tr>
    `).join('');
}

// Load documents
async function loadDocuments() {
    try {
        const response = await fetchWithAuth(`${API_URL}/api/admin/documents`);
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
    const tbody = document.getElementById('documentsTableBody');
    
    if (documents.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">No documents found</td></tr>';
        return;
    }
    
    tbody.innerHTML = documents.map(doc => {
        const sentiment = doc.analysis ? doc.analysis.sentiment : 'N/A';
        const sentimentBadge = sentiment === 'positive' 
            ? '<span class="badge bg-success">Positive</span>'
            : sentiment === 'negative'
            ? '<span class="badge bg-danger">Negative</span>'
            : sentiment === 'neutral'
            ? '<span class="badge bg-warning">Neutral</span>'
            : '<span class="badge bg-secondary">N/A</span>';
        
        // Get user info
        const userName = doc.user ? doc.user.full_name : `User ${doc.user_id}`;
        
        return `
            <tr>
                <td>${doc.id}</td>
                <td>
                    <i class="fas fa-file-${doc.file_type === 'pdf' ? 'pdf text-danger' : 'alt text-primary'} me-2"></i>
                    ${doc.filename}
                </td>
                <td>${userName}</td>
                <td><span class="badge bg-info">${doc.file_type.toUpperCase()}</span></td>
                <td>${formatFileSize(doc.file_size)}</td>
                <td>${sentimentBadge}</td>
                <td>${formatDate(doc.uploaded_at)}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="deleteDocument(${doc.id})" title="Delete Document">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Delete user
async function deleteUser(userId) {
    const result = await Swal.fire({
        title: 'Delete User?',
        text: "This will delete the user and all their documents!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#6366f1',
        confirmButtonText: 'Yes, delete user!'
    });
    
    if (result.isConfirmed) {
        try {
            const response = await fetchWithAuth(`${API_URL}/api/admin/users/${userId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Deleted!',
                    text: 'User has been deleted.',
                    timer: 1500,
                    showConfirmButton: false
                }).then(() => {
                    loadUsers();
                    loadDocuments();
                    loadStats();
                });
            } else {
                const data = await response.json();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.error || 'Could not delete user'
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

// Delete document
async function deleteDocument(docId) {
    const result = await Swal.fire({
        title: 'Delete Document?',
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
