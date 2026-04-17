// OAuth Configuration — Set your own credentials
const OAUTH_CONFIG = {
    // Google OAuth
    google: {
        clientId: 'YOUR_GOOGLE_CLIENT_ID',
        redirectUri: window.location.origin + '/login.html',
        scope: 'openid email profile',
        authUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
        // Backend handles token exchange — no client secret in frontend
        backendLogin: (window.CONFIG?.API?.BASE_URL || 'http://localhost:8000') + '/api/v1/auth/google/login',
        backendCallback: (window.CONFIG?.API?.BASE_URL || 'http://localhost:8000') + '/api/v1/auth/google/callback',
    },

    // LinkedIn OAuth
    linkedin: {
        clientId: 'YOUR_LINKEDIN_CLIENT_ID',
        redirectUri: window.location.origin + '/login.html',
        scope: 'openid profile email',
        authUrl: 'https://www.linkedin.com/oauth/v2/authorization',
        backendLogin: (window.CONFIG?.API?.BASE_URL || 'http://localhost:8000') + '/api/v1/auth/linkedin/login',
        backendCallback: (window.CONFIG?.API?.BASE_URL || 'http://localhost:8000') + '/api/v1/auth/linkedin/callback',
    }
};

console.log('🔐 OAuth configured: Google + LinkedIn');

// Export for use in auth.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OAUTH_CONFIG;
}
