/**
 * Debug and Development Utilities
 * Provides debugging tools and development helpers
 */

window.Debug = {
    // Debug state
    enabled: window.CONFIG?.APP?.DEBUG || false,
    
    // Logging utilities
    log: function(message, data = null) {
        if (this.enabled) {
            const timestamp = new Date().toISOString();
            console.log(`[${timestamp}] ${message}`, data || '');
        }
    },
    
    error: function(message, error = null) {
        if (this.enabled) {
            const timestamp = new Date().toISOString();
            console.error(`[${timestamp}] ERROR: ${message}`, error || '');
        }
    },
    
    warn: function(message, data = null) {
        if (this.enabled) {
            const timestamp = new Date().toISOString();
            console.warn(`[${timestamp}] WARNING: ${message}`, data || '');
        }
    },
    
    // API request debugging
    logApiRequest: function(method, url, data = null) {
        if (this.enabled) {
            console.group(`🌐 API ${method.toUpperCase()} ${url}`);
            if (data) {
                console.log('Request Data:', data);
            }
            console.groupEnd();
        }
    },
    
    logApiResponse: function(method, url, response, duration = null) {
        if (this.enabled) {
            const status = response.ok ? '✅' : '❌';
            console.group(`${status} API ${method.toUpperCase()} ${url}${duration ? ` (${duration}ms)` : ''}`);
            console.log('Response:', response);
            console.groupEnd();
        }
    },
    
    // Performance monitoring
    measurePerformance: function(name, fn) {
        if (this.enabled) {
            const start = performance.now();
            const result = fn();
            const end = performance.now();
            console.log(`⚡ Performance: ${name} took ${end - start} ms`);
            return result;
        } else {
            return fn();
        }
    },
    
    // Local storage debugging
    inspectStorage: function() {
        if (this.enabled) {
            console.group('📦 Local Storage Contents');
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                const value = localStorage.getItem(key);
                try {
                    console.log(key, JSON.parse(value));
                } catch (e) {
                    console.log(key, value);
                }
            }
            console.groupEnd();
        }
    },
    
    // Clear all app-related storage
    clearAppStorage: function() {
        if (this.enabled) {
            const keys = Object.values(window.CONFIG?.STORAGE_KEYS || {});
            keys.forEach(key => {
                localStorage.removeItem(key);
                console.log(`🗑️ Cleared storage key: ${key}`);
            });
            console.log('✨ App storage cleared');
        }
    },
    
    // Test API connectivity
    testApi: async function() {
        if (!this.enabled) return;
        
        console.group('🔍 API Connectivity Test');
        
        try {
            const baseUrl = window.CONFIG?.API?.BASE_URL || 'http://localhost:8000';
            const response = await fetch(`${baseUrl}/health`);
            
            if (response.ok) {
                console.log('✅ API is reachable');
                const data = await response.json();
                console.log('Health data:', data);
            } else {
                console.log('❌ API returned error:', response.status);
            }
        } catch (error) {
            console.log('❌ API is not reachable:', error.message);
        }
        
        console.groupEnd();
    },
    
    // Mock data generators
    mockData: {
        user: function() {
            return {
                id: 'mock-user-id',
                email: 'demo@example.com',
                full_name: 'Demo User',
                is_verified: true,
                plan: 'pro'
            };
        },
        
        business: function() {
            return {
                id: 'mock-business-id',
                name: 'Demo Business',
                industry: 'Technology',
                description: 'A demo business for testing',
                target_audience: 'Young professionals',
                brand_voice: 'Professional and friendly'
            };
        },
        
        campaign: function() {
            return {
                id: 'mock-campaign-id',
                name: 'Summer Launch Campaign',
                description: 'Product launch for summer season',
                status: 'active',
                platforms: ['instagram', 'linkedin'],
                start_date: new Date().toISOString(),
                end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
            };
        },
        
        content: function() {
            return {
                id: 'mock-content-id',
                title: 'Demo Post',
                content: 'This is a demo post content for testing purposes. #demo #testing',
                platform: 'instagram',
                content_type: 'post',
                status: 'draft',
                hashtags: ['demo', 'testing']
            };
        }
    },
    
    // Feature toggles for development
    features: {
        enableMockMode: function() {
            localStorage.setItem('debug_mock_mode', 'true');
            console.log('🎭 Mock mode enabled - API calls will return mock data');
        },
        
        disableMockMode: function() {
            localStorage.removeItem('debug_mock_mode');
            console.log('🌐 Mock mode disabled - API calls will hit real backend');
        },
        
        isMockMode: function() {
            return localStorage.getItem('debug_mock_mode') === 'true';
        }
    },
    
    // Component state inspector
    inspectComponent: function(componentName) {
        if (this.enabled) {
            console.group(`🔍 Component State: ${componentName}`);
            // This would be populated by individual components
            console.log('Component inspection not implemented yet');
            console.groupEnd();
        }
    },
    
    // Authentication debugging
    auth: {
        inspectToken: function() {
            const token = localStorage.getItem(window.CONFIG?.STORAGE_KEYS?.ACCESS_TOKEN);
            if (!token) {
                console.log('❌ No access token found');
                return;
            }
            
            try {
                const parts = token.split('.');
                const payload = JSON.parse(atob(parts[1]));
                console.group('🔐 JWT Token Analysis');
                console.log('Payload:', payload);
                console.log('Expires:', new Date(payload.exp * 1000));
                console.log('Valid:', payload.exp > Date.now() / 1000);
                console.groupEnd();
            } catch (error) {
                console.log('❌ Invalid token format:', error.message);
            }
        },
        
        simulateLogin: function() {
            const mockUser = window.Debug.mockData.user();
            localStorage.setItem(window.CONFIG?.STORAGE_KEYS?.USER_DATA, JSON.stringify(mockUser));
            localStorage.setItem(window.CONFIG?.STORAGE_KEYS?.ACCESS_TOKEN, 'mock-access-token');
            console.log('🎭 Simulated login with mock user:', mockUser);
        },
        
        simulateLogout: function() {
            localStorage.removeItem(window.CONFIG?.STORAGE_KEYS?.USER_DATA);
            localStorage.removeItem(window.CONFIG?.STORAGE_KEYS?.ACCESS_TOKEN);
            localStorage.removeItem(window.CONFIG?.STORAGE_KEYS?.REFRESH_TOKEN);
            console.log('👋 Simulated logout');
        }
    }
};

// Expose debug tools globally in development
if (window.Debug.enabled) {
    window.debug = window.Debug;
    
    // Add some helpful shortcuts
    window.clearStorage = () => window.Debug.clearAppStorage();
    window.testAPI = () => window.Debug.testApi();
    window.mockLogin = () => window.Debug.auth.simulateLogin();
    window.mockLogout = () => window.Debug.auth.simulateLogout();
    
    console.log('🛠️ Debug tools loaded. Available commands:');
    console.log('  - debug.*      : All debug utilities');
    console.log('  - clearStorage : Clear app storage');
    console.log('  - testAPI      : Test API connectivity');
    console.log('  - mockLogin    : Simulate login');
    console.log('  - mockLogout   : Simulate logout');
}

// Initialize debug features
if (window.Debug.enabled) {
    // Test API connectivity on load
    setTimeout(() => {
        window.Debug.testApi();
    }, 1000);
    
    // Log application startup
    window.Debug.log('Application started in debug mode');
}