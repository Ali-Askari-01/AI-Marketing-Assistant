// AI Prompt Engine - Advanced AI Integration Architecture
// Implements the complete AI prompt architecture design
class AIPromptEngine {
    constructor() {
        this.systemPrompts = this.initializeSystemPrompts();
        this.contextBuilder = new ContextBuilder();
        this.outputValidator = new OutputValidator();
        this.memoryManager = new MemoryManager();
        this.costOptimizer = new CostOptimizer();
        this.safetyGuardrails = new SafetyGuardrails();
        this.retryHandler = new RetryHandler();
        this.promptTemplates = this.initializePromptTemplates();
    }

    initializeSystemPrompts() {
        return {
            strategy: `You are a senior marketing strategist with 15 years of experience in digital marketing, campaign planning, and growth analytics. You produce structured, actionable marketing strategies. Always respond in strict JSON format. Your expertise includes market research, content strategy, audience segmentation, and performance optimization. You analyze data-driven insights and create comprehensive marketing plans that drive measurable results.`,
            
            content: `You are a creative content specialist with deep expertise in social media marketing, copywriting, and visual storytelling. You generate engaging, platform-specific content that resonates with target audiences. Always respond in strict JSON format. You understand brand voice, audience psychology, and content performance optimization. Your content drives engagement and conversions while maintaining brand consistency.`,
            
            analytics: `You are a data-driven marketing analyst with expertise in performance metrics, A/B testing, and campaign optimization. You analyze complex marketing data and provide actionable insights. Always respond in strict JSON format. You identify trends, opportunities, and areas for improvement based on quantitative analysis. Your recommendations are data-backed and focused on ROI optimization.`,
            
            messaging: `You are a professional brand communication specialist with expertise in customer service, brand voice consistency, and relationship building. You provide helpful, accurate, and brand-aligned responses. Always respond in strict JSON format. You understand customer psychology, conflict resolution, and brand values. Your responses build trust and strengthen customer relationships.`
        };
    }

    initializePromptTemplates() {
        return {
            // Strategy AI Templates
            campaignCalendar: {
                system: this.systemPrompts.strategy,
                task: `Generate a 30-day content calendar for a marketing campaign. Consider the business context, target audience, and campaign goals. Create a structured calendar with daily content themes, platform allocations, and content types. Return valid JSON with the following structure:
                {
                    "campaign_calendar": [
                        {
                            "day": 1,
                            "theme": "string",
                            "content_type": "post|reel|story|carousel|video",
                            "platform": "instagram|linkedin|email|sms",
                            "objective": "string",
                            "key_message": "string"
                        }
                    ],
                    "weekly_themes": [
                        {
                            "week": 1,
                            "theme": "string",
                            "focus": "string",
                            "kpis": ["string"]
                        }
                    ],
                    "content_distribution": {
                        "instagram": 40,
                        "linkedin": 30,
                        "email": 20,
                        "sms": 10
                    }
                }`
            },

            kpiGenerator: {
                system: this.systemPrompts.strategy,
                task: `Generate comprehensive KPI recommendations for a marketing campaign. Based on the business context and campaign goals, provide measurable targets and benchmarks. Return valid JSON with the following structure:
                {
                    "primary_kpis": [
                        {
                            "name": "string",
                            "target": 0,
                            "unit": "string",
                            "measurement_method": "string",
                            "benchmark": 0
                        }
                    ],
                    "secondary_kpis": [
                        {
                            "name": "string",
                            "target": 0,
                            "unit": "string",
                            "importance": "high|medium|low"
                        }
                    ],
                    "success_metrics": {
                        "minimum_engagement_rate": 0,
                        "conversion_target": 0,
                        "brand_awareness_lift": 0
                    }
                }`
            },

            mediaMixOptimizer: {
                system: this.systemPrompts.analytics,
                task: `Analyze campaign performance data and optimize media mix for future campaigns. Based on past performance metrics, recommend optimal content type distribution. Return valid JSON with the following structure:
                {
                    "performance_analysis": {
                        "video_engagement_rate": 0,
                        "image_engagement_rate": 0,
                        "text_engagement_rate": 0,
                        "carousel_engagement_rate": 0
                    },
                    "recommended_mix": {
                        "video": 40,
                        "image": 30,
                        "carousel": 20,
                        "text": 10
                    },
                    "optimization_insights": [
                        {
                            "insight": "string",
                            "impact": "high|medium|low",
                            "action": "string"
                        }
                    ]
                }`
            },

            // Content AI Templates
            textGenerator: {
                system: this.systemPrompts.content,
                task: `Generate engaging social media content. Consider the brand voice, target audience, and platform requirements. Return valid JSON with the following structure:
                {
                    "content_type": "text",
                    "platform": "instagram|linkedin|email|sms",
                    "headline": "string",
                    "body": "string",
                    "cta": "string",
                    "hashtags": ["string"],
                    "predicted_engagement_score": 0,
                    "tone_analysis": "string",
                    "character_count": 0
                }`
            },

            visualGenerator: {
                system: this.systemPrompts.content,
                task: `Create visual content concepts for marketing materials. Design compelling visuals that align with brand identity and campaign goals. Return valid JSON with the following structure:
                {
                    "content_type": "visual",
                    "platform": "instagram|linkedin|email",
                    "headline_text": "string",
                    "subheading": "string",
                    "design_direction": {
                        "color_scheme": ["string"],
                        "visual_style": "string",
                        "mood": "string",
                        "composition": "string"
                    },
                    "image_generation_prompt": "string",
                    "cta_placement": "string",
                    "brand_elements": ["string"],
                    "predicted_engagement_score": 0
                }`
            },

            videoScriptGenerator: {
                system: this.systemPrompts.content,
                task: `Create engaging video scripts for social media platforms. Structure content for maximum engagement and brand impact. Return valid JSON with the following structure:
                {
                    "content_type": "video",
                    "platform": "instagram|linkedin|tiktok",
                    "duration_seconds": 30,
                    "script": {
                        "hook": {
                            "text": "string",
                            "duration": 5,
                            "visual_cue": "string"
                        },
                        "body": {
                            "text": "string",
                            "duration": 20,
                            "visual_cues": ["string"],
                            "key_points": ["string"]
                        },
                        "cta": {
                            "text": "string",
                            "duration": 5,
                            "visual_cue": "string"
                        }
                    },
                    "caption": "string",
                    "hashtags": ["string"],
                    "predicted_engagement_score": 0,
                    "production_notes": "string"
                }`
            },

            // Analytics AI Templates
            performanceAnalyzer: {
                system: this.systemPrompts.analytics,
                task: `Analyze campaign performance data and provide actionable insights. Identify trends, opportunities, and areas for improvement. Return valid JSON with the following structure:
                {
                    "performance_summary": {
                        "overall_score": 0,
                        "engagement_rate": 0,
                        "conversion_rate": 0,
                        "reach": 0
                    },
                    "top_performing_content": [
                        {
                            "type": "string",
                            "engagement_score": 0,
                            "key_factors": ["string"]
                        }
                    ],
                    "weak_segments": [
                        {
                            "area": "string",
                            "issues": ["string"],
                            "recommendations": ["string"]
                        }
                    ],
                    "optimization_opportunities": [
                        {
                            "opportunity": "string",
                            "potential_impact": "high|medium|low",
                            "effort_required": "high|medium|low"
                        }
                    ]
                }`
            },

            // Messaging AI Templates
            customerReply: {
                system: this.systemPrompts.messaging,
                task: `Generate a professional and helpful response to a customer inquiry. Consider brand voice, customer context, and business policies. Return valid JSON with the following structure:
                {
                    "response_type": "customer_reply",
                    "platform": "instagram|linkedin|email|sms",
                    "reply_text": "string",
                    "tone": "professional|friendly|empathetic",
                    "escalation_needed": false,
                    "follow_up_required": false,
                    "sentiment": "positive|neutral|negative",
                    "confidence_score": 0,
                    "next_action": "string"
                }`
            }
        };
    }

    async generatePrompt(promptType, context, options = {}) {
        try {
            // Step 1: Build context
            const enrichedContext = await this.contextBuilder.buildContext(context, promptType);
            
            // Step 2: Get prompt template
            const template = this.promptTemplates[promptType];
            if (!template) {
                throw new Error(`Unknown prompt type: ${promptType}`);
            }
            
            // Step 3: Apply safety guardrails
            const safeContext = this.safetyGuardrails.applyGuardrails(enrichedContext);
            
            // Step 4: Optimize for cost
            const optimizedContext = this.costOptimizer.optimizeContext(safeContext, promptType);
            
            // Step 5: Build final prompt
            const finalPrompt = this.buildFinalPrompt(template, optimizedContext);
            
            // Step 6: Store in memory
            await this.memoryManager.storeContext(promptType, optimizedContext);
            
            return {
                prompt: finalPrompt,
                context: optimizedContext,
                metadata: {
                    promptType,
                    tokenCount: this.estimateTokens(finalPrompt),
                    cost: this.costOptimizer.estimateCost(finalPrompt, promptType)
                }
            };
            
        } catch (error) {
            console.error('Error generating prompt:', error);
            throw new Error(`Prompt generation failed: ${error.message}`);
        }
    }

    buildFinalPrompt(template, context) {
        let prompt = template.system + '\n\n';
        
        // Add context injection
        if (context.business) {
            prompt += `BUSINESS CONTEXT:\n`;
            prompt += `Business Name: ${context.business.name}\n`;
            prompt += `Industry: ${context.business.industry}\n`;
            prompt += `Brand Voice: ${context.business.brand_voice}\n`;
            prompt += `Target Audience: ${JSON.stringify(context.business.target_audience)}\n`;
            prompt += `Campaign Goal: ${context.business.campaign_goal}\n`;
            
            if (context.business.past_performance) {
                prompt += `Past Performance: ${JSON.stringify(context.business.past_performance)}\n`;
            }
            prompt += '\n';
        }
        
        // Add campaign context if available
        if (context.campaign) {
            prompt += `CAMPAIGN CONTEXT:\n`;
            prompt += `Campaign Name: ${context.campaign.name}\n`;
            prompt += `Duration: ${context.campaign.duration_days} days\n`;
            prompt += `Media Mix: ${JSON.stringify(context.campaign.media_mix)}\n`;
            prompt += '\n';
        }
        
        // Add performance context if available
        if (context.performance) {
            prompt += `PERFORMANCE CONTEXT:\n`;
            prompt += `Recent Metrics: ${JSON.stringify(context.performance.recent_metrics)}\n`;
            prompt += `Top Performing Content: ${JSON.stringify(context.performance.top_performing)}\n`;
            prompt += '\n';
        }
        
        // Add conversation context for messaging
        if (context.conversation) {
            prompt += `CONVERSATION CONTEXT:\n`;
            prompt += `Last Messages: ${JSON.stringify(context.conversation.last_messages)}\n`;
            prompt += `Customer Sentiment: ${context.conversation.sentiment}\n`;
            prompt += '\n';
        }
        
        // Add task-specific prompt
        prompt += `TASK:\n${template.task}\n`;
        
        // Add output schema reminder
        prompt += `\nIMPORTANT: Return valid JSON only. No explanations or additional text.`;
        
        return prompt;
    }

    estimateTokens(text) {
        // Rough estimation: ~1 token per 4 characters
        return Math.ceil(text.length / 4);
    }

    async processAIResponse(promptType, aiResponse, originalContext) {
        try {
            // Step 1: Validate JSON structure
            const validatedResponse = await this.outputValidator.validate(promptType, aiResponse);
            
            // Step 2: Apply safety checks
            const safeResponse = this.safetyGuardrails.validateResponse(validatedResponse);
            
            // Step 3: Store in memory for learning
            await this.memoryManager.storeResponse(promptType, originalContext, safeResponse);
            
            // Step 4: Update cost tracking
            this.costOptimizer.trackUsage(promptType, safeResponse);
            
            return safeResponse;
            
        } catch (error) {
            console.error('Error processing AI response:', error);
            
            // Step 5: Retry if validation failed
            if (error.name === 'ValidationError') {
                return await this.retryHandler.retry(promptType, originalContext, error);
            }
            
            throw error;
        }
    }

    async generateContent(contentRequest) {
        const promptType = this.determineContentPromptType(contentRequest);
        const promptData = await this.generatePrompt(promptType, contentRequest);
        
        // Call AI service (mock for demo)
        const aiResponse = await this.callAIService(promptData);
        
        return await this.processAIResponse(promptType, aiResponse, contentRequest);
    }

    determineContentPromptType(request) {
        if (request.type === 'video') {
            return 'videoScriptGenerator';
        } else if (request.type === 'visual' || request.type === 'image') {
            return 'visualGenerator';
        } else {
            return 'textGenerator';
        }
    }

    async callAIService(promptData) {
        // Mock AI service for demo
        await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
        
        // Generate mock response based on prompt type
        const mockResponses = {
            campaignCalendar: {
                campaign_calendar: [
                    { day: 1, theme: "Introduction", content_type: "post", platform: "instagram", objective: "Brand awareness", key_message: "Welcome to our journey!" },
                    { day: 2, theme: "Product showcase", content_type: "reel", platform: "instagram", objective: "Product education", key_message: "Discover our amazing features!" },
                    { day: 3, theme: "Behind the scenes", content_type: "story", platform: "instagram", objective: "Authenticity", key_message: "See how we work!" }
                ],
                weekly_themes: [
                    { week: 1, theme: "Introduction", focus: "Brand awareness", kpis: ["reach", "impressions"] },
                    { week: 2, theme: "Product showcase", focus: "Education", kpis: ["engagement", "clicks"] }
                ],
                content_distribution: { instagram: 40, linkedin: 30, email: 20, sms: 10 }
            },
            textGenerator: {
                content_type: "text",
                platform: "instagram",
                headline: "Transform Your Marketing Today!",
                body: "Discover how AI-powered marketing can revolutionize your business strategy and drive unprecedented growth.",
                cta: "Start your free trial now!",
                hashtags: ["#AIMarketing", "#MarketingAutomation", "#BusinessGrowth"],
                predicted_engagement_score: 85,
                tone_analysis: "Professional yet approachable",
                character_count: 145
            },
            videoScriptGenerator: {
                content_type: "video",
                platform: "instagram",
                duration_seconds: 30,
                script: {
                    hook: { text: "Stop wasting time on manual marketing!", duration: 5, visual_cue: "Bold text overlay" },
                    body: { text: "Our AI platform creates, schedules, and optimizes your content automatically.", duration: 20, visual_cues: ["Screen recording", "Animation"], key_points: ["AI automation", "Time savings", "Better results"] },
                    cta: { text: "Try it free today!", duration: 5, visual_cue: "Button animation" }
                },
                caption: "Revolutionize your marketing with AI! 🚀 #AIMarketing #MarketingAutomation",
                hashtags: ["#AIMarketing", "#MarketingAutomation", "#BusinessGrowth"],
                predicted_engagement_score: 92,
                production_notes: "Use upbeat background music and dynamic transitions"
            },
            customerReply: {
                response_type: "customer_reply",
                platform: "instagram",
                reply_text: "Thank you for your interest! Our AI marketing platform starts at $99/month with a 14-day free trial. Would you like me to send you more information?",
                tone: "professional",
                escalation_needed: false,
                follow_up_required: true,
                sentiment: "positive",
                confidence_score: 0.95,
                next_action: "Send detailed pricing information"
            }
        };
        
        // Return appropriate mock response
        const promptType = promptData.metadata.promptType;
        return mockResponses[promptType] || { error: "Unknown prompt type" };
    }
}

// Context Builder - Handles context injection
class ContextBuilder {
    constructor() {
        this.contextCache = new Map();
    }

    async buildContext(rawContext, promptType) {
        // Build enriched context based on prompt type
        const enrichedContext = {
            ...rawContext,
            timestamp: new Date().toISOString(),
            promptType: promptType
        };

        // Add business context
        if (rawContext.business_id) {
            enrichedContext.business = await this.getBusinessContext(rawContext.business_id);
        }

        // Add campaign context
        if (rawContext.campaign_id) {
            enrichedContext.campaign = await this.getCampaignContext(rawContext.campaign_id);
        }

        // Add performance context
        if (rawContext.performance_data) {
            enrichedContext.performance = rawContext.performance_data;
        }

        // Add conversation context
        if (rawContext.conversation_id) {
            enrichedContext.conversation = await this.getConversationContext(rawContext.conversation_id);
        }

        return enrichedContext;
    }

    async getBusinessContext(businessId) {
        // Mock business context
        return {
            name: "TechFlow Solutions",
            industry: "Technology",
            brand_voice: "Professional but innovative",
            target_audience: {
                age_range: "25-45",
                interests: ["Technology", "Innovation", "Productivity"],
                location: "Global"
            },
            campaign_goal: "Increase brand awareness and lead generation",
            past_performance: {
                top_content_type: "video",
                avg_engagement_rate: 4.2,
                best_platform: "linkedin"
            }
        };
    }

    async getCampaignContext(campaignId) {
        // Mock campaign context
        return {
            name: "Q1 Product Launch",
            duration_days: 30,
            media_mix: {
                video: 40,
                image: 30,
                text: 20,
                carousel: 10
            },
            status: "active",
            start_date: new Date().toISOString()
        };
    }

    async getConversationContext(conversationId) {
        // Mock conversation context
        return {
            last_messages: [
                { text: "How much does your service cost?", timestamp: new Date().toISOString() },
                { text: "Thanks for the information!", timestamp: new Date().toISOString() }
            ],
            sentiment: "neutral",
            customer_profile: {
                previous_interactions: 3,
                sentiment_history: ["positive", "neutral", "positive"]
            }
        };
    }
}

// Output Validator - Validates AI responses
class OutputValidator {
    constructor() {
        this.schemas = this.initializeSchemas();
    }

    initializeSchemas() {
        return {
            campaignCalendar: {
                required: ["campaign_calendar", "weekly_themes", "content_distribution"],
                properties: {
                    campaign_calendar: { type: "array", items: { type: "object" } },
                    weekly_themes: { type: "array", items: { type: "object" } },
                    content_distribution: { type: "object" }
                }
            },
            textGenerator: {
                required: ["content_type", "platform", "headline", "body", "cta", "hashtags"],
                properties: {
                    content_type: { type: "string" },
                    platform: { type: "string" },
                    headline: { type: "string" },
                    body: { type: "string" },
                    cta: { type: "string" },
                    hashtags: { type: "array" },
                    predicted_engagement_score: { type: "number" }
                }
            },
            videoScriptGenerator: {
                required: ["content_type", "platform", "duration_seconds", "script", "caption"],
                properties: {
                    content_type: { type: "string" },
                    platform: { type: "string" },
                    duration_seconds: { type: "number" },
                    script: { type: "object" },
                    caption: { type: "string" },
                    predicted_engagement_score: { type: "number" }
                }
            },
            customerReply: {
                required: ["response_type", "platform", "reply_text", "tone"],
                properties: {
                    response_type: { type: "string" },
                    platform: { type: "string" },
                    reply_text: { type: "string" },
                    tone: { type: "string" },
                    escalation_needed: { type: "boolean" },
                    confidence_score: { type: "number" }
                }
            }
        };
    }

    async validate(promptType, response) {
        const schema = this.schemas[promptType];
        if (!schema) {
            throw new Error(`Unknown schema for prompt type: ${promptType}`);
        }

        // Check if response is valid JSON
        if (typeof response === 'string') {
            try {
                response = JSON.parse(response);
            } catch (error) {
                throw new ValidationError('Invalid JSON format');
            }
        }

        // Validate required fields
        for (const requiredField of schema.required) {
            if (!(requiredField in response)) {
                throw new ValidationError(`Missing required field: ${requiredField}`);
            }
        }

        // Validate data types
        this.validateTypes(response, schema.properties);

        // Validate business logic
        this.validateBusinessLogic(response, promptType);

        return response;
    }

    validateTypes(data, schema) {
        for (const [key, schemaProp] of Object.entries(schema)) {
            if (key in data) {
                const value = data[key];
                const expectedType = schemaProp.type;

                if (expectedType === "array" && !Array.isArray(value)) {
                    throw new ValidationError(`Field ${key} must be an array`);
                }
                if (expectedType === "object" && typeof value !== "object") {
                    throw new ValidationError(`Field ${key} must be an object`);
                }
                if (expectedType === "string" && typeof value !== "string") {
                    throw new ValidationError(`Field ${key} must be a string`);
                }
                if (expectedType === "number" && typeof value !== "number") {
                    throw new ValidationError(`Field ${key} must be a number`);
                }
                if (expectedType === "boolean" && typeof value !== "boolean") {
                    throw new ValidationError(`Field ${key} must be a boolean`);
                }
            }
        }
    }

    validateBusinessLogic(data, promptType) {
        switch (promptType) {
            case 'campaignCalendar':
                if (data.campaign_calendar.length !== 30) {
                    throw new ValidationError('Campaign calendar must have exactly 30 days');
                }
                break;
            case 'textGenerator':
                if (data.predicted_engagement_score < 0 || data.predicted_engagement_score > 100) {
                    throw new ValidationError('Engagement score must be between 0 and 100');
                }
                break;
            case 'videoScriptGenerator':
                if (data.duration_seconds < 15 || data.duration_seconds > 60) {
                    throw new ValidationError('Video duration must be between 15 and 60 seconds');
                }
                break;
            case 'customerReply':
                if (data.confidence_score < 0 || data.confidence_score > 1) {
                    throw new ValidationError('Confidence score must be between 0 and 1');
                }
                break;
        }
    }
}

// Memory Manager - Handles AI memory and learning
class MemoryManager {
    constructor() {
        this.shortTermMemory = new Map();
        this.campaignMemory = new Map();
        this.responseHistory = new Map();
    }

    async storeContext(promptType, context) {
        // Store in short-term memory (Redis-like)
        const key = `${promptType}_${Date.now()}`;
        this.shortTermMemory.set(key, {
            context,
            timestamp: Date.now(),
            promptType
        });

        // Clean up old entries (10 minutes)
        this.cleanupShortTermMemory();
    }

    async storeResponse(promptType, context, response) {
        // Store response for learning
        const key = `${promptType}_${context.business_id || 'global'}_${Date.now()}`;
        this.responseHistory.set(key, {
            context,
            response,
            timestamp: Date.now(),
            promptType
        });

        // Update campaign memory if applicable
        if (context.campaign_id) {
            this.updateCampaignMemory(context.campaign_id, response);
        }
    }

    updateCampaignMemory(campaignId, response) {
        if (!this.campaignMemory.has(campaignId)) {
            this.campaignMemory.set(campaignId, {
                responses: [],
                performance: {},
                learnings: []
            });
        }

        const campaignData = this.campaignMemory.get(campaignId);
        campaignData.responses.push(response);
        
        // Keep only last 50 responses
        if (campaignData.responses.length > 50) {
            campaignData.responses = campaignData.responses.slice(-50);
        }
    }

    cleanupShortTermMemory() {
        const now = Date.now();
        const tenMinutes = 10 * 60 * 1000;

        for (const [key, value] of this.shortTermMemory.entries()) {
            if (now - value.timestamp > tenMinutes) {
                this.shortTermMemory.delete(key);
            }
        }
    }

    async getContext(promptType, businessId) {
        // Retrieve relevant context from memory
        const recentContexts = Array.from(this.shortTermMemory.values())
            .filter(ctx => ctx.promptType === promptType && 
                          (ctx.context.business_id === businessId || !businessId))
            .sort((a, b) => b.timestamp - a.timestamp)
            .slice(0, 5);

        return recentContexts.map(ctx => ctx.context);
    }
}

// Cost Optimizer - Manages AI costs
class CostOptimizer {
    constructor() {
        this.modelPricing = {
            'gpt-4o': { input: 0.005, output: 0.015 },
            'gpt-4o-mini': { input: 0.00015, output: 0.0006 },
            'gpt-3.5-turbo': { input: 0.0005, output: 0.0015 }
        };
        
        this.usageTracking = new Map();
        this.responseCache = new Map();
    }

    optimizeContext(context, promptType) {
        // Use smaller model for simple tasks
        if (this.isSimpleTask(promptType)) {
            context.model = 'gpt-4o-mini';
        } else {
            context.model = 'gpt-4o';
        }

        // Truncate unnecessary history
        if (context.conversation && context.conversation.last_messages) {
            context.conversation.last_messages = context.conversation.last_messages.slice(-3);
        }

        // Remove redundant data
        context = this.removeRedundantData(context);

        return context;
    }

    isSimpleTask(promptType) {
        const simpleTasks = ['textGenerator', 'customerReply', 'kpiGenerator'];
        return simpleTasks.includes(promptType);
    }

    removeRedundantData(context) {
        // Remove duplicate or unnecessary data
        const cleaned = { ...context };

        // Remove empty arrays
        if (cleaned.conversation && cleaned.conversation.last_messages && cleaned.conversation.last_messages.length === 0) {
            delete cleaned.conversation.last_messages;
        }

        // Remove empty performance data
        if (cleaned.performance && Object.keys(cleaned.performance).length === 0) {
            delete cleaned.performance;
        }

        return cleaned;
    }

    estimateCost(prompt, promptType) {
        const model = this.getModelForPrompt(promptType);
        const tokenCount = this.estimateTokens(prompt);
        const pricing = this.modelPricing[model];

        // Estimate input cost (most tokens are input)
        const inputCost = (tokenCount * 0.8) * pricing.input;
        const outputCost = (tokenCount * 0.2) * pricing.output;

        return inputCost + outputCost;
    }

    getModelForPrompt(promptType) {
        if (this.isSimpleTask(promptType)) {
            return 'gpt-4o-mini';
        }
        return 'gpt-4o';
    }

    estimateTokens(text) {
        return Math.ceil(text.length / 4);
    }

    trackUsage(promptType, response) {
        const key = `${promptType}_${new Date().toISOString().split('T')[0]}`;
        
        if (!this.usageTracking.has(key)) {
            this.usageTracking.set(key, {
                count: 0,
                totalCost: 0,
                promptType
            });
        }

        const usage = this.usageTracking.get(key);
        usage.count++;
        usage.totalCost += this.estimateCost(JSON.stringify(response), promptType);
    }

    getUsageStats() {
        return Array.from(this.usageTracking.values());
    }
}

// Safety Guardrails - Ensures safe AI outputs
class SafetyGuardrails {
    constructor() {
        this.blockedWords = [
            'guarantee', 'promise', 'medical advice', 'financial advice', 
            'diagnosis', 'treatment', 'investment advice', 'legal advice'
        ];

        this.controversialTopics = [
            'politics', 'religion', 'controversial social issues'
        ];
    }

    applyGuardrails(context) {
        // Filter harmful inputs
        const safeContext = { ...context };

        // Remove blocked words from business context
        if (safeContext.business) {
            safeContext.business = this.filterText(safeContext.business);
        }

        // Remove controversial topics
        if (safeContext.business && safeContext.business.target_audience) {
            safeContext.business.target_audience.interests = 
                safeContext.business.target_audience.interests.filter(interest => 
                    !this.controversialTopics.some(topic => interest.toLowerCase().includes(topic.toLowerCase()))
                );
        }

        return safeContext;
    }

    validateResponse(response) {
        // Filter harmful outputs
        const safeResponse = this.filterText(response);

        // Add safety warnings if needed
        if (this.containsRiskyContent(safeResponse)) {
            safeResponse.safety_warning = "This content should be reviewed before publication";
        }

        return safeResponse;
    }

    filterText(obj) {
        if (typeof obj === 'string') {
            return this.filterString(obj);
        } else if (typeof obj === 'object' && obj !== null) {
            const filtered = {};
            for (const [key, value] of Object.entries(obj)) {
                filtered[key] = this.filterText(value);
            }
            return filtered;
        } else if (Array.isArray(obj)) {
            return obj.map(item => this.filterText(item));
        }
        return obj;
    }

    filterString(text) {
        let filtered = text;
        
        // Remove blocked words
        for (const word of this.blockedWords) {
            const regex = new RegExp(word, 'gi');
            filtered = filtered.replace(regex, '[REDACTED]');
        }

        return filtered;
    }

    containsRiskyContent(response) {
        const text = JSON.stringify(response).toLowerCase();
        
        // Check for risky content
        const riskyPatterns = [
            'guaranteed results',
            'promise success',
            'medical advice',
            'financial advice',
            'legal advice'
        ];

        return riskyPatterns.some(pattern => text.includes(pattern));
    }
}

// Retry Handler - Manages AI response retries
class RetryHandler {
    constructor() {
        this.maxRetries = 2;
        this.retryDelay = 1000; // 1 second
    }

    async retry(promptType, context, error) {
        console.log(`Retrying ${promptType} due to error: ${error.message}`);
        
        for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
            try {
                await new Promise(resolve => setTimeout(resolve, this.retryDelay * attempt));
                
                // Generate retry prompt
                const retryPrompt = this.generateRetryPrompt(promptType, context, error);
                
                // Call AI service again
                const aiResponse = await this.callAIService(retryPrompt);
                
                // Validate response
                const validator = new OutputValidator();
                return await validator.validate(promptType, aiResponse);
                
            } catch (retryError) {
                console.log(`Retry attempt ${attempt} failed: ${retryError.message}`);
                
                if (attempt === this.maxRetries) {
                    throw new Error(`Max retries exceeded for ${promptType}: ${retryError.message}`);
                }
            }
        }
    }

    generateRetryPrompt(promptType, context, error) {
        return {
            ...context,
            retry_instruction: `Your previous response was not valid JSON. Fix it and return correct structure only. Error: ${error.message}`,
            retry_attempt: true
        };
    }

    async callAIService(promptData) {
        // Mock AI service call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Generate a valid response for retry
        const validResponses = {
            campaignCalendar: {
                campaign_calendar: Array.from({ length: 30 }, (_, i) => ({
                    day: i + 1,
                    theme: "Default theme",
                    content_type: "post",
                    platform: "instagram",
                    objective: "Engagement",
                    key_message: "Default message"
                })),
                weekly_themes: [
                    { week: 1, theme: "Default", focus: "Awareness", kpis: ["reach"] },
                    { week: 2, theme: "Default", focus: "Conversion", kpis: ["clicks"] }
                ],
                content_distribution: { instagram: 40, linkedin: 30, email: 20, sms: 10 }
            },
            textGenerator: {
                content_type: "text",
                platform: "instagram",
                headline: "Default Headline",
                body: "Default body text for retry.",
                cta: "Learn more",
                hashtags: ["#default", "#retry"],
                predicted_engagement_score: 75,
                tone_analysis: "Neutral",
                character_count: 100
            }
        };

        return validResponses[promptType] || { error: "Retry failed" };
    }
}

// Custom error class
class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValidationError';
    }
}

// Export for use in the application
window.AIPromptEngine = AIPromptEngine;

// Initialize the AI prompt engine
window.aiPromptEngine = new AIPromptEngine();
