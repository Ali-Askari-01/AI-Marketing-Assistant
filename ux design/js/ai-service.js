/**
 * AI Service Integration Module - Fixed Version
 * Provides client-side interface to AI backend services
 */

// Helper function to get API configuration
function getAPIConfig() {
    return window.API || {
        BASE_URL: 'http://localhost:8000',
        ENDPOINTS: {
            ai: {
                campaignCalendar: '/api/v1/ai/strategy/campaign-calendar',
                kpiGenerator: '/api/v1/ai/strategy/kpi-generator',
                mediaMixOptimizer: '/api/v1/ai/strategy/media-mix-optimizer',
                textContent: '/api/v1/ai/content/text',
                visualContent: '/api/v1/ai/content/visual',
                videoContent: '/api/v1/ai/content/video',
                analytics: '/api/v1/ai/analytics/analyze',
                customerReply: '/api/v1/ai/messaging/reply',
                status: '/api/v1/ai/status',
                usage: '/api/v1/ai/usage',
                optimizationSuggestions: '/api/v1/ai/optimization-suggestions'
            }
        }
    };
}

// Helper function to get auth token
function getAuthToken() {
    return localStorage.getItem('token') || 'demo_token';
}

// Helper function to make API calls
async function apiCall(endpoint, method, body = null) {
    const API = getAPIConfig();
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAuthToken()}`
        }
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    const response = await fetch(`${API.BASE_URL}${endpoint}`, options);
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail?.message || error.message || 'API call failed');
    }
    
    const result = await response.json();
    return result.data || result;
}

const AIService = {
    // ==================== STRATEGY AI ====================
    
    /**
     * Generate AI-powered campaign calendar
     */
    async generateCampaignCalendar(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.campaignCalendar, 'POST', {
                business_id: params.business_id || params.businessId || 'demo',
                business_name: params.business_name || params.businessName || 'My Business',
                industry: params.industry || 'technology',
                brand_voice: params.brand_voice || params.brandVoice || 'professional',
                target_audience: params.target_audience || params.targetAudience || 'General audience',
                campaign_goal: params.campaign_goal || params.campaignGoal || 'Increase brand awareness',
                duration_days: params.duration_days || params.durationDays || 30,
                platforms: params.platforms || ['instagram', 'linkedin'],
                content_types: params.content_types || params.contentTypes || ['text', 'image', 'video']
            });
        } catch (error) {
            console.error('Campaign calendar generation error:', error);
            throw error;
        }
    },

    /**
     * Generate KPI recommendations
     */
    async generateKPIs(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.kpiGenerator, 'POST', {
                business_id: params.businessId || 'demo',
                business_name: params.businessName,
                industry: params.industry,
                campaign_goal: params.campaignGoal,
                target_audience: params.targetAudience,
                duration_days: params.durationDays || 30
            });
        } catch (error) {
            console.error('KPI generation error:', error);
            throw error;
        }
    },

    /**
     * Optimize media mix
     */
    async optimizeMediaMix(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.mediaMixOptimizer, 'POST', {
                business_id: params.businessId || 'demo',
                performance_data: params.performanceData || {},
                platform_performance: params.platformPerformance || {},
                content_type_performance: params.contentTypePerformance || {}
            });
        } catch (error) {
            console.error('Media mix optimization error:', error);
            throw error;
        }
    },

    // ==================== CONTENT AI ====================
    
    /**
     * Generate text content
     */
    async generateTextContent(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.textContent, 'POST', {
                business_id: params.business_id || params.businessId || 'demo',
                content_type: params.content_type || params.contentType || 'post',
                platform: params.platform || 'instagram',
                business_context: params.business_context || {
                    business_name: params.businessName,
                    industry: params.industry,
                    brand_voice: params.brandVoice || params.tone,
                    target_audience: params.targetAudience || []
                },
                tone: params.tone || 'professional',
                topic: params.topic || 'General post',
                keywords: params.keywords || [],
                optimization: params.optimization !== false
            });
        } catch (error) {
            console.error('Text content generation error:', error);
            throw error;
        }
    },

    /**
     * Generate visual content
     */
    async generateVisualContent(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.visualContent, 'POST', {
                business_id: params.business_id || params.businessId || 'demo',
                content_type: params.content_type || params.contentType || 'image',
                platform: params.platform || 'instagram',
                business_context: params.business_context || {
                    business_name: params.businessName,
                    industry: params.industry,
                    brand_voice: params.brandVoice,
                    target_audience: params.targetAudience || []
                },
                visual_style: params.visual_style || params.visualStyle || 'modern',
                color_scheme: params.color_scheme || params.colorScheme || [],
                design_elements: params.design_elements || params.designElements || [],
                optimization: params.optimization !== false
            });
        } catch (error) {
            console.error('Visual content generation error:', error);
            throw error;
        }
    },

    /**
     * Generate video content
     */
    async generateVideoContent(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.videoContent, 'POST', {
                business_id: params.business_id || params.businessId || 'demo',
                content_type: params.content_type || params.contentType || 'reel',
                platform: params.platform || 'instagram',
                business_context: params.business_context || {
                    business_name: params.businessName,
                    industry: params.industry,
                    brand_voice: params.brandVoice,
                    target_audience: params.targetAudience || []
                },
                video_length: params.video_length || params.videoLength || 30,
                script_structure: params.script_structure || params.scriptStructure || {},
                music_style: params.music_style || params.musicStyle || 'upbeat',
                optimization: params.optimization !== false
            });
        } catch (error) {
            console.error('Video content generation error:', error);
            throw error;
        }
    },

    // ==================== ANALYTICS AI ====================
    
    /**
     * Generate performance analytics
     */
    async generatePerformanceAnalytics(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.analytics, 'POST', {
                business_id: params.businessId || 'demo',
                period_start: params.periodStart,
                period_end: params.periodEnd,
                platforms: params.platforms || ['instagram', 'linkedin'],
                metrics: params.metrics || ['engagement_rate', 'reach', 'impressions']
            });
        } catch (error) {
            console.error('Performance analytics error:', error);
            throw error;
        }
    },

    /**
     * Get optimization suggestions
     */
    async getOptimizationSuggestions(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.optimizationSuggestions, 'POST', {
                business_id: params.businessId || 'demo',
                performance_data: params.performanceData || {},
                goals: params.goals || ['engagement']
            });
        } catch (error) {
            console.error('Optimization suggestions error:', error);
            throw error;
        }
    },

    // ==================== MESSAGING AI ====================
    
    /**
     * Generate customer reply
     */
    async generateCustomerReply(params) {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.customerReply, 'POST', {
                business_id: params.businessId || 'demo',
                customer_message: params.customerMessage,
                conversation_context: params.conversationContext || [],
                business_context: params.businessContext || {},
                tone: params.tone || 'professional'
            });
        } catch (error) {
            console.error('Customer reply generation error:', error);
            throw error;
        }
    },

    // ==================== UTILITY ====================
    
    /**
     * Get AI service status
     */
    async getStatus() {
        try {
            const API = getAPIConfig();
            return await apiCall(API.ENDPOINTS.ai.status, 'GET');
        } catch (error) {
            console.error('AI status check error:', error);
            throw error;
        }
    },

    /**
     * Get AI usage statistics
     */
    async getUsageStats(period = 'month') {
        try {
            const API = getAPIConfig();
            return await apiCall(`${API.ENDPOINTS.ai.usage}?period=${period}`, 'GET');
        } catch (error) {
            console.error('AI usage stats error:', error);
            throw error;
        }
    }
};

// Make AIService available globally
window.AIService = AIService;
