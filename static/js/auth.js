// Check if user is already authenticated on auth pages
function checkAuthOnAuthPage() {
    if (isAuthenticated()) {
        const user = getCurrentUser();
        if (user.is_admin) {
            window.location.href = 'admin.html';
        } else {
            window.location.href = 'dashboard.html';
        }
    }
}

// Protect authenticated pages
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Protect admin pages
function requireAdmin() {
    if (!isAuthenticated() || !isAdmin()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}
