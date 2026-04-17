// API Contract Integration Layer - Connects frontend to new API contract
class MarketingAPIContract {
    constructor() {
        this.baseURL = ((window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || window.location.origin) + '/api/v1';
        this.token = localStorage.getItem('auth_token');
        this.requestId = this.generateRequestId();
    }

    generateRequestId() {
        return 'req_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Standard request method with error handling
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`,
                'X-Request-ID': this.generateRequestId(),
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            const data = await response.json();

            // Handle API contract responses
            if (data.success === false) {
                throw new Error(data.error?.message || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth APIs - Updated to new contract
    async register(userData) {
        const response = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        
        if (response.data?.access_token) {
            this.token = response.data.access_token;
            localStorage.setItem('auth_token', this.token);
        }
        
        return response.data;
    }

    async login(credentials) {
        const response = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
        
        if (response.data?.access_token) {
            this.token = response.data.access_token;
            localStorage.setItem('auth_token', this.token);
        }
        
        return response.data;
    }

    async getMe() {
        const response = await this.request('/auth/me');
        return response.data;
    }

    async refreshToken() {
        const response = await this.request('/auth/refresh', {
            method: 'POST',
            body: JSON.stringify({})
        });
        
        if (response.data?.access_token) {
            this.token = response.data.access_token;
            localStorage.setItem('auth_token', this.token);
        }
        
        return response.data;
    }

    async signout() {
        const response = await this.request('/auth/signout', {
            method: 'POST'
        });
        
        localStorage.removeItem('auth_token');
        this.token = null;
        
        return response.data;
    }

    // Business APIs - Updated to new contract
    async createBusiness(businessData) {
        const response = await this.request('/business', {
            method: 'POST',
            body: JSON.stringify(businessData)
        });
        return response.data;
    }

    async getAllBusinesses() {
        const response = await this.request('/business');
        return response.data;
    }

    async getBusiness(businessId) {
        const response = await this.request(`/business/${businessId}`);
        return response.data;
    }

    async updateBusiness(businessId, businessData) {
        const response = await this.request(`/business/${businessId}`, {
            method: 'PUT',
            body: JSON.stringify(businessData)
        });
        return response.data;
    }

    async deleteBusiness(businessId) {
        const response = await this.request(`/business/${businessId}`, {
            method: 'DELETE'
        });
        return response.data;
    }

    async getBusinessAnalytics(businessId) {
        const response = await this.request(`/business/${businessId}/analytics`);
        return response.data;
    }

    // Campaign APIs - Updated to new contract
    async generateCampaignStrategy(campaignData) {
        const response = await this.request('/campaign/generate', {
            method: 'POST',
            body: JSON.stringify(campaignData)
        });
        return response.data;
    }

    async getCampaign(campaignId) {
        const response = await this.request(`/campaign/${campaignId}`);
        return response.data;
    }

    async getCampaigns(businessId) {
        const response = await this.request(`/campaign?business_id=${businessId}`);
        return response.data;
    }

    async updateCampaign(campaignId, campaignData) {
        const response = await this.request(`/campaign/${campaignId}`, {
            method: 'PUT',
            body: JSON.stringify(campaignData)
        });
        return response.data;
    }

    async deleteCampaign(campaignId) {
        const response = await this.request(`/campaign/${campaignId}`, {
            method: 'DELETE'
        });
        return response.data;
    }

    async activateCampaign(campaignId) {
        const response = await this.request(`/campaign/${campaignId}/activate`, {
            method: 'POST'
        });
        return response.data;
    }

    async pauseCampaign(campaignId) {
        const response = await this.request(`/campaign/${campaignId}/pause`, {
            method: 'POST'
        });
        return response.data;
    }

    async completeCampaign(campaignId) {
        const response = await this.request(`/campaign/${campaignId}/complete`, {
            method: 'POST'
        });
        return response.data;
    }

    async generateAIStrategy(campaignId) {
        const response = await this.request(`/campaign/${campaignId}/generate-ai-strategy`, {
            method: 'POST'
        });
        return response.data;
    }

    async getCampaignAnalytics(campaignId) {
        const response = await this.request(`/analytics/campaign/${campaignId}`);
        return response.data;
    }

    // Content APIs - Updated to new contract
    async generateContent(contentData) {
        const response = await this.request('/content/generate', {
            method: 'POST',
            body: JSON.stringify(contentData)
        });
        return response.data;
    }

    async getContent(contentId) {
        const response = await this.request(`/content/${contentId}`);
        return response.data;
    }

    async listContent(campaignId, businessId) {
        let endpoint = '/content';
        const params = [];
        
        if (campaignId) params.push(`campaign_id=${campaignId}`);
        if (businessId) params.push(`business_id=${businessId}`);
        
        if (params.length > 0) {
            endpoint += '?' + params.join('&');
        }
        
        const response = await this.request(endpoint);
        return response.data;
    }

    async updateContent(contentId, contentData) {
        const response = await this.request(`/content/${contentId}`, {
            method: 'PUT',
            body: JSON.stringify(contentData)
        });
        return response.data;
    }

    async scheduleContent(scheduleData) {
        const response = await this.request('/content/schedule', {
            method: 'POST',
            body: JSON.stringify(scheduleData)
        });
        return response.data;
    }

    async publishContent(contentId) {
        const response = await this.request(`/content/${contentId}/publish`, {
            method: 'POST'
        });
        return response.data;
    }

    async deleteContent(contentId) {
        const response = await this.request(`/content/${contentId}`, {
            method: 'DELETE'
        });
        return response.data;
    }

    async getContentAnalytics(contentId) {
        const response = await this.request(`/analytics/content/${contentId}`);
        return response.data;
    }

    // Analytics APIs - Updated to new contract
    async getBusinessAnalytics(businessId, dateFrom, dateTo) {
        let endpoint = `/analytics/${businessId}`;
        const params = [];
        
        if (dateFrom) params.push(`date_from=${dateFrom}`);
        if (dateTo) params.push(`date_to=${dateTo}`);
        
        if (params.length > 0) {
            endpoint += '?' + params.join('&');
        }
        
        const response = await this.request(endpoint);
        return response.data;
    }

    async getHealthScore(campaignId) {
        const response = await this.request(`/analytics/health-score/${campaignId}`);
        return response.data;
    }

    async simulateAnalytics(simulationData) {
        const response = await this.request('/analytics/simulate', {
            method: 'POST',
            body: JSON.stringify(simulationData)
        });
        return response.data;
    }

    // Messaging APIs - Updated to new contract
    async getMessages(businessId, platform, status, limit = 50, offset = 0) {
        let endpoint = '/messages';
        const params = [];
        
        if (businessId) params.push(`business_id=${businessId}`);
        if (platform) params.push(`platform=${platform}`);
        if (status) params.push(`status=${status}`);
        params.push(`limit=${limit}`);
        params.push(`offset=${offset}`);
        
        if (params.length > 0) {
            endpoint += '?' + params.join('&');
        }
        
        const response = await this.request(endpoint);
        return response.data;
    }

    async generateAIReply(replyData) {
        const response = await this.request('/message/reply', {
            method: 'POST',
            body: JSON.stringify(replyData)
        });
        return response.data;
    }

    async markMessageReplied(messageId, replyData = {}) {
        const response = await this.request(`/message/${messageId}/mark-replied`, {
            method: 'POST',
            body: JSON.stringify(replyData)
        });
        return response.data;
    }

    async getMessageThread(messageId) {
        const response = await this.request(`/message/${messageId}/thread`);
        return response.data;
    }

    async escalateMessage(messageId, escalationData) {
        const response = await this.request(`/message/${messageId}/escalate`, {
            method: 'POST',
            body: JSON.stringify(escalationData)
        });
        return response.data;
    }

    async simulateMessages(simulationData) {
        const response = await this.request('/messages/simulate', {
            method: 'POST',
            body: JSON.stringify(simulationData)
        });
        return response.data;
    }

    async getMessagingStats(businessId, dateFrom, dateTo) {
        let endpoint = '/messages/stats';
        const params = [];
        
        if (businessId) params.push(`business_id=${businessId}`);
        if (dateFrom) params.push(`date_from=${dateFrom}`);
        if (dateTo) params.push(`date_to=${dateTo}`);
        
        if (params.length > 0) {
            endpoint += '?' + params.join('&');
        }
        
        const response = await this.request(endpoint);
        return response.data;
    }

    // Health check
    async getHealthStatus() {
        const response = await this.request('/health');
        return response.data;
    }

    // Utility methods
    handleAPIError(error) {
        if (error.message?.includes('401') || error.message?.includes('Unauthorized')) {
            localStorage.removeItem('auth_token');
            this.token = null;
            window.location.href = 'login.html';
            return;
        }
        
        if (error.message?.includes('403') || error.message?.includes('Forbidden')) {
            alert('Access denied. You do not have permission to perform this action.');
            return;
        }
        
        if (error.message?.includes('429') || error.message?.includes('Rate limited')) {
            alert('Too many requests. Please try again later.');
            return;
        }
        
        if (error.message?.includes('500') || error.message?.includes('Internal error')) {
            alert('Server error. Please try again later.');
            return;
        }
        
        if (error.message?.includes('503') || error.message?.includes('Service unavailable')) {
            alert('Service temporarily unavailable. Please try again later.');
            return;
        }
        
        // Generic error handling
        console.error('API Error:', error);
        alert(error.message || 'An error occurred. Please try again.');
    }

    // Demo mode methods for testing
    async demoRegister(userData) {
        // Simulate successful registration
        return {
            user_id: 'demo_user_' + Date.now(),
            access_token: 'demo_token_' + Date.now(),
            refresh_token: 'demo_refresh_' + Date.now(),
            expires_in: 3600
        };
    }

    async demoLogin(credentials) {
        // Simulate successful login
        return {
            user_id: 'demo_user_' + Date.now(),
            access_token: 'demo_token_' + Date.now(),
            refresh_token: 'demo_refresh_' + Date.now(),
            expires_in: 3600
        };
    }

    async demoGetMe() {
        // Simulate user data
        return {
            user_id: 'demo_user_' + Date.now(),
            email: 'demo@example.com',
            full_name: 'Demo User',
            first_name: 'Demo',
            last_name: 'User',
            picture: null,
            provider: 'demo',
            is_active: true,
            created_at: new Date().toISOString(),
            last_login: new Date().toISOString()
        };
    }

    async demoCreateBusiness(businessData) {
        // Simulate business creation
        return {
            business_id: 'demo_business_' + Date.now(),
            created_at: new Date().toISOString()
        };
    }

    async demoGenerateCampaignStrategy(campaignData) {
        // Simulate AI strategy generation
        return {
            campaign_id: 'demo_campaign_' + Date.now(),
            calendar: [
                {
                    day: 1,
                    theme: "Brand Introduction",
                    content_type: "image",
                    platform: "instagram",
                    objective: "Brand awareness",
                    key_message: "Welcome to our brand!"
                },
                {
                    day: 2,
                    theme: "Product Showcase",
                    content_type: "reel",
                    platform: "instagram",
                    objective: "Product education",
                    key_message: "Discover our amazing products!"
                }
            ],
            weekly_themes: [
                {
                    week: 1,
                    theme: "Brand Building",
                    focus: "Introduction and awareness",
                    kpis: ["engagement", "reach"]
                }
            ],
            content_distribution: {
                instagram: 60,
                linkedin: 25,
                email: 10,
                sms: 5
            },
            created_at: new Date().toISOString()
        };
    }

    async demoGenerateContent(contentData) {
        // Simulate content generation
        return {
            content_id: 'demo_content_' + Date.now(),
            caption: "Amazing content generated by AI! 🚀",
            hashtags: ["#marketing", "#ai", "#innovation"],
            script: {
                hook: "Did you know...",
                body: "Our amazing solution helps you...",
                cta: "Try it now!"
            },
            visual_description: "Modern, clean design with vibrant colors",
            estimated_engagement_score: 85,
            tone_analysis: "Professional and engaging",
            character_count: 150,
            content_type: contentData.content_type,
            platform: contentData.platform || "instagram"
        };
    }

    async demoGenerateAIReply(replyData) {
        // Simulate AI reply generation
        return {
            suggested_reply: "Thank you for your message! I'd be happy to help you with that. Let me get back to you shortly.",
            response_type: "customer_reply",
            platform: replyData.platform || "instagram",
            tone: "professional",
            escalation_needed: false,
            follow_up_required: false,
            sentiment: "neutral",
            confidence_score: 0.85,
            next_action: "Wait for customer response"
        };
    }

    async demoGetBusinessAnalytics(businessId) {
        // Simulate analytics data
        return {
            health_score: 78,
            engagement_rate: 4.2,
            top_content_type: "Reel",
            recommendations: [
                "Post more video content to increase engagement",
                "Increase CTA strength in posts",
                "Optimize posting times for better reach"
            ],
            metrics: {
                total_impressions: 125000,
                total_engagement: 5250,
                total_clicks: 875,
                total_conversions: 45,
                total_posts: 25,
                average_engagement_rate: 4.2,
                average_ctr: 0.7,
                conversion_rate: 3.6
            },
            platform_performance: {
                instagram: { impressions: 75000, engagement: 3500, engagement_rate: 4.7 },
                linkedin: { impressions: 35000, engagement: 1400, engagement_rate: 4.0 },
                email: { impressions: 15000, engagement: 350, engagement_rate: 2.3 }
            }
        };
    }

    async demoGetMessages(businessId) {
        // Simulate messages data
        return {
            messages: [
                {
                    id: "demo_msg_1",
                    business_id: businessId,
                    platform: "instagram",
                    sender_name: "Sarah Johnson",
                    sender_type: "customer",
                    message_text: "How much is your monthly membership?",
                    message_type: "inquiry",
                    status: "pending",
                    priority: "normal",
                    received_at: new Date().toISOString(),
                    ai_suggested_reply: "Thanks for your interest! Our monthly membership starts at $29...",
                    ai_sentiment: "neutral",
                    ai_category: "pricing_inquiry"
                },
                {
                    id: "demo_msg_2",
                    business_id: businessId,
                    platform: "instagram",
                    sender_name: "Mike Chen",
                    sender_type: "customer",
                    message_text: "Do you offer personal training?",
                    message_type: "inquiry",
                    status: "replied",
                    priority: "normal",
                    received_at: new Date(Date.now() - 3600000).toISOString(),
                    ai_suggested_reply: "Yes! We offer personal training with certified trainers...",
                    ai_sentiment: "neutral",
                    ai_category: "service_inquiry"
                }
            ],
            pagination: {
                total: 2,
                limit: 50,
                offset: 0,
                has_next: false
            }
        };
    }
}

// Create global API instance
window.apiContract = new MarketingAPIContract();

// Export for use in the app
const api = window.apiContract;
