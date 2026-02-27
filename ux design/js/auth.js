// Authentication Manager with Google & LinkedIn OAuth
// Real credentials loaded from config.js (OAUTH_CONFIG global)

class AuthManager {
    constructor() {
        this.token = localStorage.getItem('auth_token') || null;
        try {
            this.user = JSON.parse(localStorage.getItem('user_info') || 'null');
        } catch (e) {
            this.user = null;
        }
    }

    // Initialize - call after DOM is ready
    init() {
        console.log('AuthManager initializing...');

        // Handle OAuth data in URL hash (from backend redirect)
        if (this.handleAuthHash()) return;

        // Handle OAuth callback (code in URL from provider redirect)
        if (this.handleOAuthCallback()) return;

        // If on login page and already authenticated, go to app
        if (this.token && this.user && window.location.pathname.includes('login.html')) {
            console.log('Already authenticated, redirecting to app');
            window.location.href = 'index.html';
            return;
        }

        // If on app page and NOT authenticated, go to login
        if (!this.token && !this.user
            && !window.location.pathname.includes('login.html')
            && !window.location.pathname.includes('test-auth.html')
            && !window.location.pathname.includes('login-sso.html')) {
            console.log('Not authenticated, redirecting to login');
            window.location.href = 'login.html';
            return;
        }

        console.log('Auth check passed, staying on page');
    }

    // Handle auth data passed in URL hash fragment from backend OAuth redirect
    handleAuthHash() {
        var hash = window.location.hash;
        if (!hash || hash.indexOf('auth_token=') === -1) return false;

        console.log('Auth data found in URL hash, storing...');
        var params = new URLSearchParams(hash.substring(1));
        var token = params.get('auth_token');
        var refreshToken = params.get('refresh_token');
        var userB64 = params.get('user');
        var bizB64 = params.get('business');

        if (!token || !userB64) return false;

        try {
            var userJson = atob(userB64.replace(/-/g, '+').replace(/_/g, '/'));
            var user = JSON.parse(userJson);
            var bizJson = bizB64 ? atob(bizB64.replace(/-/g, '+').replace(/_/g, '/')) : '{}';
            var biz = JSON.parse(bizJson);

            localStorage.setItem('auth_token', token);
            localStorage.setItem('refresh_token', refreshToken || '');
            localStorage.setItem('user_info', JSON.stringify(user));
            localStorage.setItem('user_profile', JSON.stringify(user));
            localStorage.setItem('business_profile', JSON.stringify(biz));

            this.token = token;
            this.user = user;

            // Clear the hash so it doesn't persist in URL
            window.history.replaceState({}, document.title, window.location.pathname);
            console.log('Auth data stored successfully for:', user.email || user.name);
            return true;
        } catch (e) {
            console.error('Failed to parse auth data from hash:', e);
            return false;
        }
    }

    // Handle OAuth callback - returns true if handling a callback
    handleOAuthCallback() {
        var params = new URLSearchParams(window.location.search);
        var code = params.get('code');
        var state = params.get('state');
        var error = params.get('error');

        if (error) {
            console.error('OAuth error:', error);
            showToast('Authentication failed: ' + error, 'error');
            window.history.replaceState({}, document.title, window.location.pathname);
            return true;
        }

        if (code) {
            console.log('OAuth callback detected, exchanging code via fetch...');
            showLoading();

            // Determine provider from state prefix
            var provider = 'google';
            if (state && state.startsWith('linkedin')) provider = 'linkedin';

            // Exchange code via fetch (stays on same origin so localStorage works)
            var base = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || 'http://localhost:8000';
            var self = this;

            // Clear URL params immediately
            window.history.replaceState({}, document.title, window.location.pathname);

            fetch(base + '/api/v1/auth/oauth/exchange', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ provider: provider, code: code })
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if (data.error) {
                    console.error('OAuth exchange error:', data.error, data.details || '');
                    showToast('Login failed: ' + data.error, 'error');
                    hideLoading();
                    return;
                }

                console.log('OAuth exchange successful, storing auth data...');
                localStorage.setItem('auth_token', data.token);
                localStorage.setItem('refresh_token', data.refreshToken || '');
                localStorage.setItem('user_info', JSON.stringify(data.user));
                localStorage.setItem('user_profile', JSON.stringify(data.user));
                localStorage.setItem('business_profile', JSON.stringify(data.business));

                self.token = data.token;
                self.user = data.user;

                showToast('Welcome, ' + (data.user.name || data.user.email) + '!', 'success');
                setTimeout(function() {
                    window.location.href = 'index.html';
                }, 800);
            })
            .catch(function(err) {
                console.error('OAuth exchange fetch error:', err);
                showToast('Authentication failed. Please try again.', 'error');
                hideLoading();
            });

            return true;
        }

        return false;
    }

    // Google OAuth - redirect to backend login endpoint
    signInWithGoogle() {
        console.log('Initiating Google OAuth via backend');
        showLoading();
        var base = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || 'http://localhost:8000';
        window.location.href = base + '/api/v1/auth/google/login';
    }

    // LinkedIn OAuth - redirect to backend login endpoint
    signInWithLinkedIn() {
        console.log('Initiating LinkedIn OAuth via backend');
        showLoading();
        var base = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || 'http://localhost:8000';
        window.location.href = base + '/api/v1/auth/linkedin/login';
    }

    // Email/Password sign in
    signInWithEmail(email, password) {
        showLoading();
        var self = this;
        var base = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || 'http://localhost:8000';
        fetch(base + '/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(function(response) {
            if (!response.ok) throw new Error('Invalid credentials');
            return response.json();
        })
        .then(function(data) {
            var d = data.data || data;
            self.setAuthData(
                { access_token: d.token || d.access_token, refresh_token: d.refreshToken || d.refresh_token },
                d.user || { email: email },
                'email'
            );
            window.location.href = 'index.html';
        })
        .catch(function(error) {
            console.error('Email sign-in error:', error);
            showToast('Invalid email or password', 'error');
            hideLoading();
        });
    }

    // Store auth data in localStorage
    setAuthData(tokenData, userProfile, provider) {
        console.log('Storing auth data for provider:', provider);
        this.token = tokenData.access_token;
        this.user = Object.assign({}, userProfile, {
            provider: provider,
            lastLogin: new Date().toISOString()
        });

        localStorage.setItem('auth_token', this.token);
        localStorage.setItem('user_info', JSON.stringify(this.user));
        localStorage.setItem('refresh_token', tokenData.refresh_token || '');
        console.log('Auth data stored. User:', this.user.email || this.user.name);
    }

    // Sign out
    signOut() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_info');
        localStorage.removeItem('refresh_token');
        this.token = null;
        this.user = null;
        window.location.href = 'login.html';
    }

    isAuthenticated() {
        return !!(this.token && this.user);
    }

    getCurrentUser() {
        return this.user;
    }

    getUserProfile() {
        return this.user;
    }

    getBusinessProfile() {
        try {
            return JSON.parse(localStorage.getItem('business_profile') || 'null');
        } catch (e) {
            return null;
        }
    }

    getToken() {
        return this.token;
    }
}

// ============================================================
// Create global auth instance
// ============================================================
var auth = new AuthManager();

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    auth.init();
});

// ============================================================
// UI Helper Functions
// ============================================================

function showLoading() {
    var overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.remove('hidden');
}

function hideLoading() {
    var overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.add('hidden');
}

function showToast(message, type) {
    type = type || 'info';
    var toast = document.getElementById('toast');
    var toastMessage = document.getElementById('toastMessage');
    var toastIcon = document.getElementById('toastIcon');

    if (!toast || !toastMessage) {
        console.log(type.toUpperCase() + ': ' + message);
        return;
    }

    toastMessage.textContent = message;

    if (toastIcon) {
        if (type === 'success') {
            toastIcon.innerHTML = '<i class="fas fa-check-circle text-green-500"></i>';
        } else if (type === 'error') {
            toastIcon.innerHTML = '<i class="fas fa-exclamation-circle text-red-500"></i>';
        } else {
            toastIcon.innerHTML = '<i class="fas fa-info-circle text-blue-500"></i>';
        }
    }

    toast.classList.remove('hidden');
    setTimeout(function() { hideToast(); }, 3000);
}

function hideToast() {
    var toast = document.getElementById('toast');
    if (toast) toast.classList.add('hidden');
}

// ============================================================
// Button Click Handlers (called from onclick in HTML)
// ============================================================

function signInWithGoogle() {
    console.log('Google sign-in button clicked');
    try {
        auth.signInWithGoogle();
    } catch (error) {
        console.error('Google sign-in error:', error);
        showToast('Error signing in with Google', 'error');
    }
}

function signInWithLinkedIn() {
    console.log('LinkedIn sign-in button clicked');
    try {
        auth.signInWithLinkedIn();
    } catch (error) {
        console.error('LinkedIn sign-in error:', error);
        showToast('Error signing in with LinkedIn', 'error');
    }
}

function signUpWithGoogle() {
    console.log('Google sign-up button clicked');
    signInWithGoogle();
}

function signUpWithLinkedIn() {
    console.log('LinkedIn sign-up button clicked');
    signInWithLinkedIn();
}

function signInDemo() {
    console.log('Demo login button clicked');
    try {
        var demoUser = {
            id: 'demo_user_' + Date.now(),
            email: 'demo@marketing-command.com',
            name: 'Demo User',
            firstName: 'Demo',
            lastName: 'User',
            picture: 'https://picsum.photos/seed/demo/200/200.jpg',
            provider: 'demo'
        };

        var mockTokenData = {
            access_token: 'demo_access_token_' + Date.now(),
            refresh_token: 'demo_refresh_token_' + Date.now()
        };

        auth.setAuthData(mockTokenData, demoUser, 'demo');
        showToast('Demo login successful! Welcome to Omni Mind', 'success');

        setTimeout(function() {
            window.location.href = 'index.html';
        }, 1000);
    } catch (error) {
        console.error('Demo login error:', error);
        showToast('Demo login failed', 'error');
    }
}

function handleEmailSignIn(event) {
    event.preventDefault();
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    auth.signInWithEmail(email, password);
}

// ============================================================
// Sign Up Modal Functions
// ============================================================

function showSignUpModal() {
    var modal = document.getElementById('signUpModal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function hideSignUpModal() {
    var modal = document.getElementById('signUpModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

function handleSignUp(event) {
    event.preventDefault();
    showLoading();

    var firstName = event.target[0].value;
    var lastName = event.target[1].value;
    var email = event.target[2].value;
    var password = event.target[3].value;
    var company = event.target[4].value;
    var industry = event.target[5].value;

    var base = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || 'http://localhost:8000';

    fetch(base + '/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: email,
            password: password,
            name: firstName + ' ' + lastName,
            business: { name: company, industry: industry }
        })
    })
    .then(function(response) {
        if (!response.ok) throw new Error('Registration failed');
        return response.json();
    })
    .then(function(data) {
        var d = data.data || data;
        auth.setAuthData(
            { access_token: d.token || d.access_token, refresh_token: d.refreshToken || d.refresh_token },
            d.user || { email: email, name: firstName + ' ' + lastName },
            'email'
        );
        if (d.business) {
            localStorage.setItem('business_profile', JSON.stringify(d.business));
        }
        hideLoading();
        hideSignUpModal();
        showToast('Account created successfully!', 'success');
        setTimeout(function() {
            window.location.href = 'index.html';
        }, 1000);
    })
    .catch(function(error) {
        console.error('Registration error:', error);
        hideLoading();
        showToast('Registration failed. Please try again.', 'error');
    });
}

// Export for other files
window.auth = auth;
