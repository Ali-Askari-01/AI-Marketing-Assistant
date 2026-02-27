// API Integration Layer - Connects frontend to FastAPI backend
class MarketingAPI {
    constructor() {
        this.baseURL = 'http://localhost:8003/api'; // FastAPI backend
        this.token = localStorage.getItem('auth_token');
    }

    // Auth APIs
    async register(userData) {
        const response = await fetch(`${this.baseURL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        return response.json();
    }

    async login(credentials) {
        const response = await fetch(`${this.baseURL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentials)
        });
        const data = await response.json();
        if (data.access_token) {
            this.token = data.access_token;
            localStorage.setItem('auth_token', this.token);
        }
        return data;
    }

    async getMe() {
        const response = await fetch(`${this.baseURL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    // Business APIs
    async createBusiness(businessData) {
        const response = await fetch(`${this.baseURL}/business/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(businessData)
        });
        return response.json();
    }

    async getBusiness(id) {
        const response = await fetch(`${this.baseURL}/business/${id}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async updateBusiness(id, businessData) {
        const response = await fetch(`${this.baseURL}/business/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(businessData)
        });
        return response.json();
    }

    // Campaign APIs
    async createCampaign(campaignData) {
        const response = await fetch(`${this.baseURL}/campaign/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(campaignData)
        });
        return response.json();
    }

    async getCampaign(id) {
        const response = await fetch(`${this.baseURL}/campaign/${id}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async getCampaigns(businessId) {
        const response = await fetch(`${this.baseURL}/campaign?business_id=${businessId}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async updateCampaign(id, campaignData) {
        const response = await fetch(`${this.baseURL}/campaign/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(campaignData)
        });
        return response.json();
    }

    async deleteCampaign(id) {
        const response = await fetch(`${this.baseURL}/campaign/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    // Strategy AI APIs
    async generateCalendar(strategyData) {
        try {
            // Use AI prompt engine for better prompts
            const promptData = await window.aiPromptEngine.generatePrompt('campaignCalendar', strategyData);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('campaignCalendar', aiResponse, strategyData);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error generating calendar:', error);
            throw error;
        }
    }

    async suggestSegments(businessData) {
        try {
            const promptData = await window.aiPromptEngine.generatePrompt('kpiGenerator', businessData);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('kpiGenerator', aiResponse, businessData);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error suggesting segments:', error);
            throw error;
        }
    }

    async suggestKPIs(campaignData) {
        try {
            const promptData = await window.aiPromptEngine.generatePrompt('kpiGenerator', campaignData);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('kpiGenerator', aiResponse, campaignData);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error suggesting KPIs:', error);
            throw error;
        }
    }

    async optimizeCampaign(campaignId) {
        try {
            const campaignData = { campaign_id: campaignId };
            const promptData = await window.aiPromptEngine.generatePrompt('mediaMixOptimizer', campaignData);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('mediaMixOptimizer', aiResponse, campaignData);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error optimizing campaign:', error);
            throw error;
        }
    }

    // Content APIs
    async generateContent(contentRequest) {
        try {
            // Use AI prompt engine for content generation
            const promptData = await window.aiPromptEngine.generatePrompt('textGenerator', contentRequest);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('textGenerator', aiResponse, contentRequest);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error generating content:', error);
            throw error;
        }
    }

    async generateVisualContent(visualRequest) {
        try {
            const promptData = await window.aiPromptEngine.generatePrompt('visualGenerator', visualRequest);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('visualGenerator', aiResponse, visualRequest);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error generating visual content:', error);
            throw error;
        }
    }

    async generateVideoScript(videoRequest) {
        try {
            const promptData = await window.aiPromptEngine.generatePrompt('videoScriptGenerator', videoRequest);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('videoScriptGenerator', aiResponse, videoRequest);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error generating video script:', error);
            throw error;
        }
    }

    async optimizeContent(id, optimizationData) {
        try {
            const contentRequest = { content_id: id, ...optimizationData };
            const promptData = await window.aiPromptEngine.generatePrompt('performanceAnalyzer', contentRequest);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('performanceAnalyzer', aiResponse, contentRequest);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error optimizing content:', error);
            throw error;
        }
    }

    async getContent(id) {
        const response = await fetch(`${this.baseURL}/content/${id}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async getCampaignContent(campaignId) {
        const response = await fetch(`${this.baseURL}/content?campaign_id=${campaignId}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async updateContent(id, contentData) {
        const response = await fetch(`${this.baseURL}/content/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(contentData)
        });
        return response.json();
    }

    // Publishing APIs
    async scheduleContent(id, scheduleData) {
        const response = await fetch(`${this.baseURL}/content/${id}/schedule`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(scheduleData)
        });
        return response.json();
    }

    async publishContent(id) {
        const response = await fetch(`${this.baseURL}/content/${id}/publish`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async getCampaignCalendar(campaignId) {
        const response = await fetch(`${this.baseURL}/calendar/${campaignId}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    // Analytics APIs
    async simulateAnalytics(contentId) {
        const response = await fetch(`${this.baseURL}/analytics/simulate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({ content_id: contentId })
        });
        return response.json();
    }

    async getContentAnalytics(contentId) {
        const response = await fetch(`${this.baseURL}/analytics/content/${contentId}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async getCampaignAnalytics(campaignId) {
        const response = await fetch(`${this.baseURL}/analytics/campaign/${campaignId}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async getHealthScore(campaignId) {
        const response = await fetch(`${this.baseURL}/analytics/health-score/${campaignId}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    // Messaging APIs
    async getMessages(businessId) {
        const response = await fetch(`${this.baseURL}/messages?business_id=${businessId}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async simulateMessages() {
        const response = await fetch(`${this.baseURL}/messages/simulate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }

    async getAIMessageReply(messageId) {
        try {
            const messageData = { message_id: messageId };
            const promptData = await window.aiPromptEngine.generatePrompt('customerReply', messageData);
            const aiResponse = await this.callAI(promptData);
            const validatedResponse = await window.aiPromptEngine.processAIResponse('customerReply', aiResponse, messageData);
            
            return validatedResponse;
        } catch (error) {
            console.error('Error getting AI reply:', error);
            throw error;
        }
    },

    async markMessageReplied(messageId) {
        const response = await fetch(`${this.baseURL}/messages/${messageId}/mark-replied`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    },

    async publishContent(id) {
        const response = await fetch(`${this.baseURL}/content/${id}/publish`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    },

    // AI Service Integration
    async callAI(promptData) {
        try {
            // For demo, use the AI prompt engine's mock service
            return await window.aiPromptEngine.callAIService(promptData);
        } catch (error) {
            console.error('Error calling AI service:', error);
            throw error;
        }
    },

    // Utility methods
    async handleAPIError(response) {
        if (response.status === 401) {
            // Token expired, redirect to login
            localStorage.removeItem('auth_token');
            window.location.href = 'login.html';
            return;
        }
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        
        return response.json();
    },

    async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`,
                ...options.headers
            }
        };

        const response = await fetch(`${this.baseURL}${url}`, {
            ...defaultOptions,
            ...options
        });

        return this.handleAPIError(response);
    }
}

// Export for use in the app
const api = new MarketingAPI();
