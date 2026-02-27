/**
 * Frontend Configuration for Omni Mind - AI Marketing
 * Contains API endpoints, environment settings, and application constants
 */

// Detect environment: Use Railway URL in production, localhost in development
const IS_PRODUCTION = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';

// ⚠️ IMPORTANT: After deploying to Railway, replace with your actual backend URL
// Example: 'https://backend-api-production.up.railway.app'
const RAILWAY_BACKEND_URL = '';  // Set this to your Railway backend URL

// API Configuration
window.CONFIG = {
    // Backend API Configuration
    API: {
        BASE_URL: RAILWAY_BACKEND_URL || (IS_PRODUCTION ? window.location.origin : 'http://localhost:8000'),
        VERSION: 'v1',
        TIMEOUT: 30000, // 30 seconds
        
        // Endpoints
        ENDPOINTS: {
            // Authentication
            AUTH: {
                REGISTER: '/api/v1/auth/register',
                LOGIN: '/api/v1/auth/login',
                LOGOUT: '/api/v1/auth/logout',
                ME: '/api/v1/auth/me',
                REFRESH: '/api/v1/auth/refresh',
                RESET_PASSWORD: '/api/v1/auth/reset-password'
            },
            
            // Business Management
            BUSINESS: {
                LIST: '/api/v1/business',
                CREATE: '/api/v1/business',
                GET: '/api/v1/business/{id}',
                UPDATE: '/api/v1/business/{id}',
                DELETE: '/api/v1/business/{id}',
                ANALYTICS: '/api/v1/business/{id}/analytics'
            },
            
            // Campaign Management
            CAMPAIGN: {
                LIST: '/api/v1/campaign',
                CREATE: '/api/v1/campaign',
                GET: '/api/v1/campaign/{id}',
                UPDATE: '/api/v1/campaign/{id}',
                DELETE: '/api/v1/campaign/{id}',
                GENERATE_STRATEGY: '/api/v1/campaign/generate-strategy',
                ANALYTICS: '/api/v1/campaign/{id}/analytics'
            },
            
            // Content Management
            CONTENT: {
                LIST: '/api/v1/content',
                CREATE: '/api/v1/content',
                GET: '/api/v1/content/{id}',
                UPDATE: '/api/v1/content/{id}',
                DELETE: '/api/v1/content/{id}',
                GENERATE: '/api/v1/content/generate',
                PUBLISH: '/api/v1/content/{id}/publish',
                SCHEDULE: '/api/v1/content/{id}/schedule'
            },
            
            // Analytics
            ANALYTICS: {
                OVERVIEW: '/api/v1/analytics/overview',
                PERFORMANCE: '/api/v1/analytics/performance',
                INSIGHTS: '/api/v1/analytics/insights',
                REPORTS: '/api/v1/analytics/reports'
            },
            
            // Messaging
            MESSAGING: {
                INBOX: '/api/v1/messaging/inbox',
                SEND: '/api/v1/messaging/send',
                REPLY: '/api/v1/messaging/reply',
                MARK_READ: '/api/v1/messaging/{id}/read',
                SUGGESTIONS: '/api/v1/messaging/ai-suggestions'
            },
            
            // AI Services
            AI: {
                // Strategy AI
                CAMPAIGN_CALENDAR: '/api/v1/ai/strategy/campaign-calendar',
                KPI_GENERATOR: '/api/v1/ai/strategy/kpi-generator',
                MEDIA_MIX_OPTIMIZER: '/api/v1/ai/strategy/media-mix-optimizer',
                
                // Content AI
                TEXT_CONTENT: '/api/v1/ai/content/text',
                VISUAL_CONTENT: '/api/v1/ai/content/visual',
                
                // Analytics AI (Gemini-powered)
                ANALYTICS: '/api/v1/ai/analytics/analyze',
                AI_ENGAGEMENT: '/api/v1/ai-analytics/engagement',
                AI_COMPARE_POSTS: '/api/v1/ai-analytics/compare-posts',
                AI_RECOMMENDATIONS: '/api/v1/ai-analytics/recommendations',
                
                // Messaging AI
                CUSTOMER_REPLY: '/api/v1/ai/messaging/reply',
                
                // AI Agent (Gemini)
                AGENT_STATUS: '/api/v1/agent/status',
                AGENT_ASK: '/api/v1/agent/ask',
                AGENT_HASHTAGS: '/api/v1/agent/generate-hashtags',
                AGENT_IDEAS: '/api/v1/agent/content-ideas',
                
                // AI Service Status
                STATUS: '/api/v1/ai/status',
                USAGE: '/api/v1/ai/usage',
                OPTIMIZATION_SUGGESTIONS: '/api/v1/ai/optimization-suggestions'
            }
        }
    },
    
    // Application Settings
    APP: {
        NAME: 'Omni Mind',
        VERSION: '1.0.0',
        DEBUG: true,
        
        // UI Settings
        UI: {
            THEME: 'light',
            ANIMATIONS_ENABLED: true,
            NOTIFICATIONS_ENABLED: true,
            AUTO_SAVE_INTERVAL: 30000, // 30 seconds
        },
        
        // Feature Flags
        FEATURES: {
            AI_CONTENT_GENERATION: true,
            CAMPAIGN_ANALYTICS: true,
            MULTI_PLATFORM_PUBLISHING: true,
            REAL_TIME_NOTIFICATIONS: true,
            ADVANCED_SCHEDULING: true
        }
    },
    
    // Local Storage Keys
    STORAGE_KEYS: {
        ACCESS_TOKEN: 'ai_marketing_access_token',
        REFRESH_TOKEN: 'ai_marketing_refresh_token',
        USER_DATA: 'ai_marketing_user_data',
        SELECTED_BUSINESS: 'ai_marketing_selected_business',
        THEME: 'ai_marketing_theme',
        SETTINGS: 'ai_marketing_settings'
    },
    
    // Default Values
    DEFAULTS: {
        PAGINATION: {
            PAGE_SIZE: 20,
            MAX_PAGE_SIZE: 100
        },
        
        CONTENT: {
            AUTO_SAVE_DELAY: 2000,
            MAX_TITLE_LENGTH: 200,
            MAX_CONTENT_LENGTH: 4000
        },
        
        CAMPAIGN: {
            DEFAULT_DURATION_DAYS: 30,
            MIN_DURATION_DAYS: 7,
            MAX_DURATION_DAYS: 365
        }
    },
    
    // Validation Rules
    VALIDATION: {
        EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        PASSWORD_MIN_LENGTH: 8,
        BUSINESS_NAME_MIN_LENGTH: 2,
        CAMPAIGN_NAME_MIN_LENGTH: 3
    },
    
    // Social Media Platforms
    PLATFORMS: [
        { id: 'instagram', name: 'Instagram', icon: 'fab fa-instagram', color: '#E4405F' },
        { id: 'linkedin', name: 'LinkedIn', icon: 'fab fa-linkedin', color: '#0077B5' },
        { id: 'twitter', name: 'Twitter', icon: 'fab fa-twitter', color: '#1DA1F2' },
        { id: 'tiktok', name: 'TikTok', icon: 'fab fa-tiktok', color: '#000000' },
        { id: 'youtube', name: 'YouTube', icon: 'fab fa-youtube', color: '#FF0000' },
        { id: 'email', name: 'Email', icon: 'fas fa-envelope', color: '#6B46C1' },
        { id: 'sms', name: 'SMS', icon: 'fas fa-sms', color: '#10B981' }
    ],
    
    // Content Types
    CONTENT_TYPES: [
        { id: 'caption', name: 'Social Caption', icon: 'fas fa-comment-dots' },
        { id: 'email', name: 'Email Draft', icon: 'fas fa-envelope' },
        { id: 'sms', name: 'SMS Text', icon: 'fas fa-sms' },
        { id: 'post_idea', name: 'Post Idea', icon: 'fas fa-lightbulb' }
    ],
    
    // Campaign Status Options
    CAMPAIGN_STATUS: [
        { value: 'draft', label: 'Draft', color: 'gray' },
        { value: 'active', label: 'Active', color: 'green' },
        { value: 'paused', label: 'Paused', color: 'yellow' },
        { value: 'completed', label: 'Completed', color: 'blue' },
        { value: 'archived', label: 'Archived', color: 'gray' }
    ],
    
    // Content Status Options
    CONTENT_STATUS: [
        { value: 'draft', label: 'Draft', color: 'gray' },
        { value: 'review', label: 'In Review', color: 'yellow' },
        { value: 'approved', label: 'Approved', color: 'green' },
        { value: 'scheduled', label: 'Scheduled', color: 'blue' },
        { value: 'publishing', label: 'Publishing', color: 'purple' },
        { value: 'published', label: 'Published', color: 'green' },
        { value: 'failed', label: 'Failed', color: 'red' },
        { value: 'archived', label: 'Archived', color: 'gray' }
    ]
};

// Utility Functions
window.CONFIG.UTILS = {
    // Build complete API URL
    buildApiUrl: function(endpoint, params = {}) {
        let url = this.API.BASE_URL + endpoint;
        
        // Replace path parameters
        for (const [key, value] of Object.entries(params)) {
            url = url.replace(`{${key}}`, encodeURIComponent(value));
        }
        
        return url;
    },
    
    // Get platform configuration
    getPlatform: function(platformId) {
        return this.PLATFORMS.find(p => p.id === platformId);
    },
    
    // Get content type configuration
    getContentType: function(typeId) {
        return this.CONTENT_TYPES.find(t => t.id === typeId);
    },
    
    // Get status configuration
    getStatus: function(statusValue, type = 'campaign') {
        const statuses = type === 'campaign' ? this.CAMPAIGN_STATUS : this.CONTENT_STATUS;
        return statuses.find(s => s.value === statusValue);
    },
    
    // Validate email
    isValidEmail: function(email) {
        return this.VALIDATION.EMAIL_REGEX.test(email);
    },
    
    // Format date
    formatDate: function(dateString) {
        return new Date(dateString).toLocaleDateString();
    },
    
    // Format datetime
    formatDateTime: function(dateString) {
        return new Date(dateString).toLocaleString();
    }
};

// Environment-specific overrides
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Development environment
    window.CONFIG.APP.DEBUG = true;
} else {
    // Production environment
    window.CONFIG.APP.DEBUG = false;
    // BASE_URL stays '' (empty) so requests go to same origin (Railway single-service)
}

console.log('🔧 Configuration loaded:', window.CONFIG.APP.DEBUG ? window.CONFIG : 'Production mode');