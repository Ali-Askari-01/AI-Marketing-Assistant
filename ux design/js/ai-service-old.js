/**
 * AI Service Integration Module
 * Provides client-side interface to AI backend services
 */

// Helper function to get API configuration
function getAPIConfig() {
    return window.API || {
        BASE_URL: 'http://localhost:8000',
        ENDPOINTS: {
            ai: {
                campaignCalendar: '/api/v1/ai/campaign-calendar',
                kpiGenerator: '/api/v1/ai/kpi-generator',
                mediaMixOptimizer: '/api/v1/ai/media-mix-optimizer',
                textContent: '/api/v1/ai/content/text',
                visualContent: '/api/v1/ai/content/visual',
                videoContent: '/api/v1/ai/content/video',
                analytics: '/api/v1/ai/analytics/performance',
                customerReply: '/api/v1/ai/messaging/reply',
                status: '/api/v1/ai/status',
                usage: '/api/v1/ai/usage',
                optimizationSuggestions: '/api/v1/ai/analytics/optimization-suggestions'
            }
        }
    };
}

// Helper function to get auth token
function getAuthToken() {
    return localStorage.getItem('token') || 'demo_token';
}

const AIService = {
    // ==================== STRATEGY AI ====================
    
    /**
     * Generate AI-powered campaign calendar
     * @param {Object} params - Calendar generation parameters
     * @returns {Promise<Object>} Campaign calendar
     */
    async generateCampaignCalendar(params) {
        try {
            const API = getAPIConfig();
            
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.campaignCalendar}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token') || 'demo_token'}`
                },
                body: JSON.stringify({
                    business_id: params.business_id || params.businessId || 'demo',
                    business_context: params.business_context || {
                        business_name: params.businessName || params.business_name,
                        industry: params.industry,
                        brand_voice: params.brandVoice || params.brand_voice,
                        target_audience: params.targetAudience || params.target_audience,
                        primary_goals: params.primary_goals || [params.campaignGoal || params.campaign_goal]
                    },
                    duration_days: params.duration_days || params.durationDays || 30,
                    platforms: params.platforms || ['instagram', 'linkedin'],
                    content_types: params.content_types || params.contentTypes || ['text', 'image', 'video'],
                    posting_frequency: params.posting_frequency || 'daily'
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail?.message || 'Campaign calendar generation failed');
            }

            const result = await response.json();
            return result.data || result;
        } catch (error) {
            console.error('Campaign calendar generation error:', error);
            throw error;
        }
    },

    /**
     * Generate KPI recommendations
     * @param {Object} params - KPI generation parameters
     * @returns {Promise<Object>} KPI recommendations
     */
    async generateKPIs(params) {
        try {
            const API = window.API || { 
                BASE_URL: 'http://localhost:8000', 
                ENDPOINTS: { ai: { kpiGenerator: '/api/v1/ai/kpi-generator' } } 
            };
            
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.kpiGenerator}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token') || 'demo_token'}`
                },
                body: JSON.stringify({
                    business_id: params.businessId || 'demo',
                    business_name: params.businessName,
                    industry: params.industry,
                    campaign_goal: params.campaignGoal,
                    target_audience: params.targetAudience,
                    duration_days: params.durationDays || 30
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail?.message || 'KPI generation failed');
            }

            const result = await response.json();
            return result.data || result;
        } catch (error) {
            console.error('KPI generation error:', error);
            throw error;
        }
    },

    /**
     * Optimize media mix based on performance
     * @param {Object} params - Optimization parameters
     * @returns {Promise<Object>} Media mix optimization
     */
    async optimizeMediaMix(params) {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.mediaMixOptimizer}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    business_id: params.businessId || 'demo',
                    performance_data: params.performanceData || {},
                    platform_performance: params.platformPerformance || {},
                    content_type_performance: params.contentTypePerformance || {}
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail?.message || 'Media mix optimization failed');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('Media mix optimization error:', error);
            throw error;
        }
    },

    // ==================== CONTENT AI ====================

    /**
     * Generate text content
     * @param {Object} params - Text content parameters
     * @returns {Promise<Object>} Generated text content
     */
    async generateTextContent(params) {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.textContent}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    business_id: params.businessId || 'demo',
                    business_name: params.businessName,
                    industry: params.industry,
                    brand_voice: params.brandVoice,
                    target_audience: params.targetAudience,
                    topic: params.topic,
                    platform: params.platform || 'instagram',
                    tone: params.tone || 'engaging',
                    length: params.length || 'medium',
                    character_limit: params.characterLimit || 150
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail?.message || 'Text content generation failed');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('Text content generation error:', error);
            throw error;
        }
    },

    /**
     * Generate visual content concept
     * @param {Object} params - Visual content parameters
     * @returns {Promise<Object>} Generated visual content concept
     */
    async generateVisualContent(params) {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.visualContent}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    business_id: params.businessId || 'demo',
                    business_name: params.businessName,
                    industry: params.industry,
                    brand_colors: params.brandColors || ['blue', 'white'],
                    brand_guidelines: params.brandGuidelines || 'Modern and clean',
                    target_audience: params.targetAudience,
                    topic: params.topic,
                    platform: params.platform || 'instagram',
                    visual_style: params.visualStyle || 'modern and clean'
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail?.message || 'Visual content generation failed');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('Visual content generation error:', error);
            throw error;
        }
    },

    /**
     * Generate video script
     * @param {Object} params - Video content parameters
     * @returns {Promise<Object>} Generated video script
     */
    async generateVideoScript(params) {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.videoContent}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    business_id: params.businessId || 'demo',
                    business_name: params.businessName,
                    industry: params.industry,
                    brand_voice: params.brandVoice,
                    target_audience: params.targetAudience,
                    topic: params.topic,
                    platform: params.platform || 'instagram',
                    duration_seconds: params.durationSeconds || 30,
                    script_style: params.scriptStyle || 'conversational'
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail?.message || 'Video script generation failed');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('Video script generation error:', error);
            throw error;
        }
    },

    // ==================== ANALYTICS AI ====================

    /**
     * Analyze campaign performance
     * @param {Object} params - Analytics parameters
     * @returns {Promise<Object>} Performance analytics
     */
    async analyzePerformance(params) {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.analytics}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    business_id: params.businessId || 'demo',
                    performance_data: params.performanceData || {},
                    platform_performance: params.platformPerformance || {},
                    content_type_performance: params.contentTypePerformance || {},
                    time_period: params.timePeriod || 'last 30 days',
                    campaign_goals: params.campaignGoals || 'engagement and growth'
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail?.message || 'Performance analysis failed');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('Performance analysis error:', error);
            throw error;
        }
    },

    // ==================== MESSAGING AI ====================

    /**
     * Generate customer reply
     * @param {Object} params - Reply generation parameters
     * @returns {Promise<Object>} Generated reply
     */
    async generateCustomerReply(params) {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.customerReply}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    business_id: params.businessId || 'demo',
                    business_name: params.businessName,
                    brand_voice: params.brandVoice,
                    industry: params.industry,
                    customer_message: params.customerMessage,
                    conversation_history: params.conversationHistory || 'No previous messages',
                    platform: params.platform || 'instagram',
                    customer_profile: params.customerProfile || {}
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail?.message || 'Reply generation failed');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('Reply generation error:', error);
            throw error;
        }
    },

    // ==================== AI SERVICE STATUS ====================

    /**
     * Get AI service status
     * @returns {Promise<Object>} AI service status
     */
    async getStatus() {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.status}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to get AI service status');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('AI status check error:', error);
            throw error;
        }
    },

    /**
     * Get AI usage statistics
     * @param {string} period - Usage period (daily/weekly/monthly)
     * @returns {Promise<Object>} Usage statistics
     */
    async getUsage(period = 'daily') {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.usage}?period=${period}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to get AI usage statistics');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('AI usage check error:', error);
            throw error;
        }
    },

    /**
     * Get cost optimization suggestions
     * @returns {Promise<Object>} Optimization suggestions
     */
    async getOptimizationSuggestions() {
        try {
            const response = await fetch(`${API.BASE_URL}${API.ENDPOINTS.ai.optimizationSuggestions}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to get optimization suggestions');
            }

            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('Optimization suggestions error:', error);
            throw error;
        }
    }
};

// Make AIService available globally
window.AIService = AIService;
