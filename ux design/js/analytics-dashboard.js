/**
 * AI Analytics Dashboard Module
 * Handles AI-powered engagement analytics, post comparison, recommendations, and Chart.js graphs
 */
const AnalyticsDashboard = {
    isLoading: false,
    baseUrl: '',
    charts: {},

    init() {
        this.baseUrl = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL)
            ? window.CONFIG.API.BASE_URL
            : 'http://localhost:8003';
        console.log('[AnalyticsDashboard] Initialized with baseUrl:', this.baseUrl);
    },

    getEndpoint(path) {
        return this.baseUrl + path;
    },

    // ============ CHART.JS INITIALIZATION ============

    /**
     * Initialize all Chart.js charts when analytics view loads
     */
    initCharts() {
        console.log('[AnalyticsDashboard] Initializing charts...');
        // Destroy existing charts to prevent duplicates
        Object.values(this.charts).forEach(c => { if (c && c.destroy) c.destroy(); });
        this.charts = {};

        // Initialize default charts immediately (fast)
        this.initReachEngagementChart();
        this.initContentTypeChart();
        this.initPlatformChart();
        this.initFollowerChart();
        this.initPostComparisonChart();

        // Then ask AI to analyze and potentially override with better viz
        this.loadAIDrivenVisualization();
        this.loadRecommendations();
        this.loadAIAnalysis();
        this.loadProactiveInsights();
        this.loadSmartSuggestions('viewing_dashboard');
    },

    /**
     * AI-DRIVEN VISUALIZATION: Gemini decides chart types and presentation
     */
    async loadAIDrivenVisualization() {
        try {
            const engData = await this.fetchEngagement();
            if (!engData) return;

            const metrics = engData.data || engData;
            this.updateEngagementUI(engData);

            const response = await fetch(this.getEndpoint('/api/v1/ai/visualize'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ metrics, context: 'marketing_dashboard' })
            });

            if (!response.ok) return;
            const result = await response.json();
            const viz = result.data;
            if (!viz || !viz.charts) return;

            console.log('[AnalyticsDashboard] AI decided visualization:', viz.charts.length, 'charts');

            // Update health score from AI
            if (viz.health_score) {
                const healthNum = document.getElementById('healthScoreNum');
                if (healthNum) healthNum.textContent = viz.health_score;
            }

            // Update AI analysis banner
            if (viz.executive_summary) {
                const banner = document.getElementById('aiAnalysisBanner');
                const textEl = document.getElementById('aiAnalysisText');
                if (banner && textEl) {
                    banner.classList.remove('hidden');
                    textEl.innerHTML = this.formatAIResponse(viz.executive_summary);
                }
            }

            // Render AI-decided charts
            this.renderAICharts(viz.charts);

            // Render proactive alerts
            if (viz.proactive_alerts) {
                this.renderProactiveAlerts(viz.proactive_alerts);
            }

            // Update recommendations if AI provided them
            if (viz.recommendations && viz.recommendations.length) {
                this.renderAIRecommendations(viz.recommendations);
            }
        } catch (err) {
            console.warn('[AnalyticsDashboard] AI visualization fallback:', err);
        }
    },

    /**
     * Render charts as decided by AI
     */
    renderAICharts(aiCharts) {
        if (!aiCharts || !aiCharts.length) return;

        // Map AI chart IDs to existing canvas IDs where possible
        const canvasMap = {
            'weekly_trend': 'reachEngagementChart',
            'content_mix': 'contentTypeChart',
            'platform_comparison': 'platformChart',
            'follower_growth': 'followerChart',
            'post_comparison': 'postComparisonChart',
        };

        aiCharts.forEach((chartConfig, index) => {
            let canvasId = canvasMap[chartConfig.id];
            
            // If no matching canvas, try to use an existing one by index
            if (!canvasId) {
                const fallbacks = ['reachEngagementChart', 'contentTypeChart', 'platformChart', 'followerChart', 'postComparisonChart'];
                canvasId = fallbacks[index] || fallbacks[0];
            }

            const ctx = document.getElementById(canvasId);
            if (!ctx) return;

            // Destroy existing chart on this canvas
            const chartKey = canvasId.replace('Chart', '');
            if (this.charts[chartKey]) {
                this.charts[chartKey].destroy();
            }

            // Build Chart.js config from AI response
            const chartData = chartConfig.data || {};
            const datasets = (chartData.datasets || []).map(ds => {
                const dataset = { ...ds };
                // Ensure proper types
                if (typeof dataset.fill === 'undefined' && chartConfig.type === 'line') dataset.fill = true;
                if (!dataset.tension && chartConfig.type === 'line') dataset.tension = 0.4;
                if (!dataset.borderWidth && chartConfig.type !== 'line') dataset.borderWidth = 2;
                if (chartConfig.type === 'bar' && !dataset.borderRadius) dataset.borderRadius = 6;
                if (chartConfig.type === 'radar') {
                    dataset.pointRadius = dataset.pointRadius || 4;
                    dataset.pointHoverRadius = dataset.pointHoverRadius || 6;
                }
                return dataset;
            });

            const options = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top', labels: { usePointStyle: true, padding: 12, color: 'rgba(255,255,255,0.7)' } },
                    ...(chartConfig.options?.plugins || {})
                },
                ...(chartConfig.type === 'doughnut' || chartConfig.type === 'pie' ? { cutout: '55%' } : {}),
                ...(chartConfig.type === 'radar' ? { scales: { r: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: 'rgba(255,255,255,0.5)' } } } } : {}),
                ...(chartConfig.type === 'bar' || chartConfig.type === 'line' ? {
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: 'rgba(255,255,255,0.5)' } },
                        x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.5)' } }
                    }
                } : {}),
            };

            // Update the card header to show AI-chosen title + chart type reason
            const card = ctx.closest('.card');
            if (card) {
                const titleEl = card.querySelector('.card-title');
                if (titleEl && chartConfig.title) {
                    titleEl.innerHTML = `<i class="fas fa-brain text-purple-500"></i> ${chartConfig.title}`;
                }
                // Add small badge showing why AI chose this type
                if (chartConfig.reason) {
                    let reasonBadge = card.querySelector('.ai-reason-badge');
                    if (!reasonBadge) {
                        reasonBadge = document.createElement('span');
                        reasonBadge.className = 'ai-reason-badge text-xs text-purple-500 italic block mt-1';
                        const header = card.querySelector('.card-header');
                        if (header) header.appendChild(reasonBadge);
                    }
                    reasonBadge.textContent = `AI: ${chartConfig.reason}`;
                }
            }

            try {
                this.charts[chartKey] = new Chart(ctx, {
                    type: chartConfig.type || 'bar',
                    data: { labels: chartData.labels || [], datasets },
                    options
                });
            } catch (e) {
                console.warn(`[AnalyticsDashboard] Failed to render AI chart ${chartConfig.id}:`, e);
            }
        });
    },

    /**
     * Render proactive alerts from AI
     */
    renderProactiveAlerts(alerts) {
        const banner = document.getElementById('aiAnalysisBanner');
        if (!banner || !alerts.length) return;

        const alertColors = {
            'success': 'bg-green-50 border-green-200 text-green-800',
            'warning': 'bg-yellow-50 border-yellow-200 text-yellow-800',
            'info': 'bg-blue-50 border-blue-200 text-blue-800',
            'opportunity': 'bg-purple-50 border-purple-200 text-purple-800',
        };
        const alertIcons = {
            'success': 'fa-check-circle text-green-500',
            'warning': 'fa-exclamation-triangle text-yellow-500',
            'info': 'fa-info-circle text-blue-500',
            'opportunity': 'fa-rocket text-purple-500',
        };

        const alertsHtml = alerts.map(a => `
            <div class="flex items-start gap-2 p-2 rounded-lg ${alertColors[a.type] || alertColors.info} border text-sm mt-2">
                <i class="fas ${alertIcons[a.type] || alertIcons.info} mt-0.5"></i>
                <div><strong>${a.message}</strong>${a.action ? ` → <em>${a.action}</em>` : ''}</div>
            </div>
        `).join('');

        // Append after the AI analysis text
        const textEl = document.getElementById('aiAnalysisText');
        if (textEl) {
            textEl.innerHTML += alertsHtml;
        }
    },

    /**
     * Render AI-structured recommendations
     */
    renderAIRecommendations(recs) {
        const container = document.getElementById('aiRecommendations');
        if (!container || !recs.length) return;

        const priorityColors = {
            'high': { bg: 'from-red-50 to-orange-50', border: 'border-red-200', icon: 'text-red-600', label: 'text-red-700 bg-red-100' },
            'medium': { bg: 'from-blue-50 to-purple-50', border: 'border-blue-200', icon: 'text-blue-600', label: 'text-blue-700 bg-blue-100' },
            'low': { bg: 'from-green-50 to-teal-50', border: 'border-green-200', icon: 'text-green-600', label: 'text-green-700 bg-green-100' },
        };
        const catIcons = {
            'content': 'fa-pen-fancy', 'timing': 'fa-clock', 'platform': 'fa-share-nodes',
            'engagement': 'fa-heart', 'growth': 'fa-chart-line', 'email': 'fa-envelope',
            'sms': 'fa-sms',
        };

        container.innerHTML = recs.slice(0, 4).map(rec => {
            const c = priorityColors[rec.priority] || priorityColors.medium;
            const icon = catIcons[rec.category] || 'fa-lightbulb';
            return `
                <div class="p-4 bg-gradient-to-br ${c.bg} ${c.border} border rounded-xl">
                    <div class="flex items-center gap-2 mb-3">
                        <i class="fas ${icon} ${c.icon} text-lg"></i>
                        <span class="text-xs font-bold ${c.label} px-2 py-0.5 rounded-full">${(rec.priority || 'medium').toUpperCase()}</span>
                    </div>
                    <h4 class="font-bold text-gray-900 mb-2">${rec.title || 'Recommendation'}</h4>
                    <p class="text-sm text-gray-600 mb-3">${rec.description || ''}</p>
                    ${rec.expected_impact ? `<span class="text-xs ${c.icon} font-semibold">Expected: ${rec.expected_impact}</span>` : ''}
                </div>`;
        }).join('');
    },

    /**
     * Load AI proactive insights (tips, alerts, milestones)
     */
    async loadProactiveInsights() {
        try {
            const response = await fetch(this.getEndpoint('/api/v1/ai/proactive-insights'));
            if (!response.ok) return;
            const result = await response.json();
            const insights = result.data?.insights || [];
            if (!insights.length) return;

            // Create proactive insights bar if not exists
            let container = document.getElementById('proactiveInsights');
            if (!container) {
                const mainContent = document.querySelector('.max-w-7xl');
                if (!mainContent) return;
                container = document.createElement('div');
                container.id = 'proactiveInsights';
                container.className = 'mb-6 space-y-2';
                // Insert after the AI analysis banner
                const banner = document.getElementById('aiAnalysisBanner');
                if (banner && banner.nextSibling) {
                    banner.parentNode.insertBefore(container, banner.nextSibling);
                } else {
                    mainContent.insertBefore(container, mainContent.children[1]);
                }
            }

            const urgencyColors = {
                'high': 'border-l-red-500 bg-red-50',
                'medium': 'border-l-yellow-500 bg-yellow-50',
                'low': 'border-l-blue-500 bg-blue-50',
            };
            const typeIcons = {
                'tip': 'fa-lightbulb text-yellow-500',
                'alert': 'fa-bell text-red-500',
                'opportunity': 'fa-rocket text-purple-500',
                'milestone': 'fa-trophy text-green-500',
            };

            container.innerHTML = `
                <div class="flex items-center gap-2 mb-2">
                    <i class="fas fa-bolt text-amber-500"></i>
                    <span class="text-sm font-bold text-gray-700">AI Proactive Insights</span>
                </div>
            ` + insights.slice(0, 5).map(item => `
                <div class="flex items-start gap-3 p-3 border-l-4 ${urgencyColors[item.urgency] || 'border-l-blue-500 bg-blue-50'} rounded-r-lg">
                    <i class="fas ${item.icon || typeIcons[item.type] || 'fa-info-circle text-blue-500'} text-lg mt-0.5"></i>
                    <div>
                        <span class="font-bold text-gray-900 text-sm">${item.title}</span>
                        <p class="text-xs text-gray-600 mt-0.5">${item.message}</p>
                    </div>
                </div>
            `).join('');
        } catch (err) {
            console.warn('[AnalyticsDashboard] Proactive insights error:', err);
        }
    },

    /**
     * Context-aware smart suggestions
     */
    async loadSmartSuggestions(action, data = {}) {
        try {
            const response = await fetch(this.getEndpoint('/api/v1/ai/smart-suggest'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action, view: 'analytics', data })
            });
            if (!response.ok) return;
            const result = await response.json();
            const suggestions = result.data?.suggestions || [];
            if (!suggestions.length) return;

            // Show as a floating suggestion badge
            let badge = document.getElementById('smartSuggestBadge');
            if (!badge) {
                badge = document.createElement('div');
                badge.id = 'smartSuggestBadge';
                badge.className = 'fixed bottom-6 right-6 max-w-sm bg-white border border-purple-200 shadow-2xl rounded-2xl p-4 z-50 transition-all duration-300';
                document.body.appendChild(badge);
            }

            badge.innerHTML = `
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center gap-2">
                        <div class="w-8 h-8 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-full flex items-center justify-center">
                            <i class="fas fa-robot text-white text-sm"></i>
                        </div>
                        <span class="text-sm font-bold text-gray-900">AI Suggestions</span>
                    </div>
                    <button onclick="document.getElementById('smartSuggestBadge').remove()" class="text-gray-400 hover:text-gray-600"><i class="fas fa-times"></i></button>
                </div>
                ${suggestions.slice(0, 3).map(s => `
                    <div class="flex items-start gap-2 mb-2 p-2 bg-purple-50 rounded-lg">
                        <i class="fas fa-chevron-right text-purple-500 text-xs mt-1"></i>
                        <div>
                            <p class="text-xs font-semibold text-gray-800">${s.tip}</p>
                            ${s.action ? `<span class="text-xs text-purple-600 cursor-pointer hover:underline">${s.action}</span>` : ''}
                        </div>
                    </div>
                `).join('')}
            `;

            // Auto-hide after 15 seconds
            setTimeout(() => { if (badge) badge.style.opacity = '0'; }, 15000);
            setTimeout(() => { if (badge && badge.parentNode) badge.remove(); }, 15500);
        } catch (err) {
            console.warn('[AnalyticsDashboard] Smart suggest error:', err);
        }
    },

    initReachEngagementChart() {
        const ctx = document.getElementById('reachEngagementChart');
        if (!ctx) return;
        this.charts.reachEngagement = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
                datasets: [
                    {
                        label: 'Reach',
                        data: [8200, 9100, 11000, 10500, 13200, 15200],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.15)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    },
                    {
                        label: 'Engagement',
                        data: [420, 510, 680, 590, 780, 850],
                        borderColor: '#06b6d4',
                        backgroundColor: 'rgba(6, 182, 212, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top', labels: { usePointStyle: true, padding: 15, color: 'rgba(255,255,255,0.7)' } }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: 'rgba(255,255,255,0.5)' } },
                    x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.5)' } }
                }
            }
        });
    },

    initContentTypeChart() {
        const ctx = document.getElementById('contentTypeChart');
        if (!ctx) return;
        this.charts.contentType = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Captions', 'Email Drafts', 'SMS Texts', 'Post Ideas'],
                datasets: [{
                    data: [42, 28, 18, 12],
                    backgroundColor: ['#6366f1', '#8b5cf6', '#06b6d4', '#ec4899'],
                    borderWidth: 3,
                    borderColor: '#131825',
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { usePointStyle: true, padding: 12, font: { size: 12 }, color: 'rgba(255,255,255,0.7)' } }
                },
                cutout: '60%'
            }
        });
    },

    initPlatformChart() {
        const ctx = document.getElementById('platformChart');
        if (!ctx) return;
        this.charts.platform = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Instagram', 'LinkedIn', 'Email', 'SMS'],
                datasets: [{
                    label: 'Engagement Rate %',
                    data: [5.8, 4.2, 3.6, 2.8],
                    backgroundColor: [
                        'rgba(236, 72, 153, 0.8)',
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(6, 182, 212, 0.8)'
                    ],
                    borderColor: ['#ec4899', '#3b82f6', '#ef4444', '#06b6d4'],
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true, max: 8, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: 'rgba(255,255,255,0.5)', callback: v => v + '%' } },
                    x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.5)' } }
                }
            }
        });
    },

    initFollowerChart() {
        const ctx = document.getElementById('followerChart');
        if (!ctx) return;
        this.charts.follower = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Followers',
                    data: [1200, 1380, 1520, 1690, 1850, 2262],
                    borderColor: '#22c55e',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 5,
                    pointBackgroundColor: '#22c55e',
                    pointBorderColor: '#131825',
                    pointBorderWidth: 2,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: false, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: 'rgba(255,255,255,0.5)' } },
                    x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.5)' } }
                }
            }
        });
    },

    initPostComparisonChart() {
        const ctx = document.getElementById('postComparisonChart');
        if (!ctx) return;
        this.charts.postComparison = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Product Launch', 'Newsletter', 'Flash Sale SMS', '5 Tips Post'],
                datasets: [
                    {
                        label: 'Likes/Opens',
                        data: [1240, 342, 156, 892],
                        backgroundColor: 'rgba(239, 68, 68, 0.7)',
                        borderRadius: 4
                    },
                    {
                        label: 'Comments/Clicks',
                        data: [186, 0, 23, 67],
                        backgroundColor: 'rgba(59, 130, 246, 0.7)',
                        borderRadius: 4
                    },
                    {
                        label: 'Shares/Conversions',
                        data: [92, 3, 23, 45],
                        backgroundColor: 'rgba(34, 197, 94, 0.7)',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top', labels: { usePointStyle: true, padding: 12, color: 'rgba(255,255,255,0.7)' } }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: 'rgba(255,255,255,0.5)' } },
                    x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.5)' } }
                }
            }
        });
    },

    // ============ AI ANALYSIS ============

    /**
     * Load full AI analysis of all marketing data
     */
    async loadAIAnalysis() {
        const banner = document.getElementById('aiAnalysisBanner');
        const textEl = document.getElementById('aiAnalysisText');
        if (!banner || !textEl) return;

        banner.classList.remove('hidden');
        textEl.innerHTML = '<i class="fas fa-spinner fa-spin text-indigo-500"></i> AI is analyzing your marketing performance...';

        try {
            const response = await fetch(this.getEndpoint('/api/v1/agent/ask'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: 'Analyze this marketing dashboard data and give a brief executive summary with 3 key findings: Total Reach 15.2K (+18%), Engagement Rate 5.1% (+0.8%), New Followers +412 (+25%), CTR 2.5% (+0.3%), Email Open Rate 26% (+5%), SMS CTR 14% (+8%). Instagram ER 5.8%, LinkedIn ER 4.2%. Top post: Product launch caption (7.2% ER, 1240 likes). Content mix: Captions 42%, Email 28%, SMS 18%, Post Ideas 12%.',
                    context: 'marketing_analytics_executive_summary'
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            const answer = (data.data && data.data.answer) || data.response || data.answer || '';
            textEl.innerHTML = this.formatAIResponse(answer || this.getDefaultAnalysis());
        } catch (err) {
            console.error('[AnalyticsDashboard] loadAIAnalysis error:', err);
            textEl.innerHTML = this.formatAIResponse(this.getDefaultAnalysis());
        }
    },

    getDefaultAnalysis() {
        return '**Executive Summary:** Your marketing performance is strong with positive growth across all channels. **Key Finding 1:** Instagram leads with 5.8% engagement rate - 2x industry average. Product launches drive highest interaction. **Key Finding 2:** Email open rate of 26% is above the 21% industry benchmark. Consider increasing email frequency. **Key Finding 3:** SMS shows the fastest growth (+8% CTR) indicating untapped potential. Recommend expanding SMS campaigns with personalized flash sale content.';
    },

    /**
     * Load AI post comparison analysis
     */
    async loadPostComparison() {
        const container = document.getElementById('aiPostComparison');
        const textEl = document.getElementById('aiPostComparisonText');
        if (!container || !textEl) return;

        container.classList.remove('hidden');
        textEl.innerHTML = '<i class="fas fa-spinner fa-spin text-blue-500"></i> AI comparing posts...';

        try {
            const response = await fetch(this.getEndpoint('/api/v1/agent/ask'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: 'Compare these 4 marketing posts and tell me which strategy works best and why: 1) Instagram product launch caption: 7.2% ER, 1240 likes, 186 comments, 92 shares. 2) Weekly email newsletter: 28% open rate, 342 clicks, 3 unsubscribes. 3) Flash sale SMS: 14% CTR, 890 delivered, 156 clicks, 23 conversions. 4) LinkedIn "5 tips" post: 5.9% ER, 892 likes, 67 comments, 45 shares. Give brief analysis.',
                    context: 'post_comparison_analysis'
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            const answer = (data.data && data.data.answer) || data.response || data.answer || '';
            textEl.innerHTML = this.formatAIResponse(answer || 'The Instagram product launch caption leads with 7.2% engagement rate. SMS shows best conversion rate at 2.6%. Recommend combining high-engagement social content with SMS follow-ups for maximum ROI.');
        } catch (err) {
            textEl.innerHTML = this.formatAIResponse('The Instagram product launch caption leads with 7.2% engagement rate. SMS shows best conversion rate at 2.6%. Recommend combining high-engagement social content with SMS follow-ups for maximum ROI.');
        }
    },

    /**
     * Load AI improvement suggestions
     */
    async loadAISuggestions() {
        const container = document.getElementById('analyticsAiSuggestions');
        if (!container) return;

        container.innerHTML = `<div class="text-center py-6"><i class="fas fa-spinner fa-spin text-2xl text-yellow-500"></i><p class="text-sm text-gray-500 mt-2">AI is generating improvement suggestions...</p></div>`;

        try {
            const response = await fetch(this.getEndpoint('/api/v1/agent/ask'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: 'Based on this marketing data (Reach 15.2K, ER 5.1%, Followers +412, CTR 2.5%, Email OR 26%, SMS CTR 14%), give me exactly 5 specific improvement suggestions. For each, provide: 1) A clear title, 2) A brief description (1-2 sentences), 3) Expected impact. Format as numbered list.',
                    context: 'improvement_suggestions'
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            const answer = (data.data && data.data.answer) || data.response || data.answer || '';
            this.renderSuggestions(container, answer);
        } catch (err) {
            console.error('[AnalyticsDashboard] loadAISuggestions error:', err);
            this.renderDefaultSuggestions(container);
        }
    },

    renderSuggestions(container, text) {
        if (!text) { this.renderDefaultSuggestions(container); return; }

        const lines = text.split('\n').filter(l => l.trim());
        const suggestions = [];
        let current = null;

        lines.forEach(line => {
            const trimmed = line.trim();
            if (trimmed.match(/^\d+[\.\)]/)) {
                if (current) suggestions.push(current);
                current = { title: trimmed.replace(/^\d+[\.\)]\s*/, '').replace(/\*\*/g, ''), body: '' };
            } else if (current) {
                current.body += trimmed.replace(/\*\*/g, '') + ' ';
            }
        });
        if (current) suggestions.push(current);

        if (suggestions.length === 0) { this.renderDefaultSuggestions(container); return; }

        const icons = ['fa-rocket', 'fa-clock', 'fa-bullseye', 'fa-envelope', 'fa-chart-line'];
        const colors = ['text-purple-500', 'text-teal-500', 'text-blue-500', 'text-orange-500', 'text-green-500'];
        const bgColors = ['bg-purple-50', 'bg-teal-50', 'bg-blue-50', 'bg-orange-50', 'bg-green-50'];

        container.innerHTML = suggestions.slice(0, 5).map((s, i) => `
            <div class="p-4 ${bgColors[i % bgColors.length]} rounded-xl border border-gray-100 flex items-start gap-3">
                <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center flex-shrink-0 shadow-sm">
                    <i class="fas ${icons[i % icons.length]} ${colors[i % colors.length]}"></i>
                </div>
                <div>
                    <h4 class="font-bold text-gray-900 mb-1">${s.title}</h4>
                    <p class="text-sm text-gray-600">${s.body.trim()}</p>
                </div>
            </div>
        `).join('');
    },

    renderDefaultSuggestions(container) {
        const defaults = [
            { icon: 'fa-rocket', color: 'text-purple-500', bg: 'bg-purple-50', title: 'Increase Video Content', body: 'Video posts get 2.5x more engagement than static images. Try Reels and short-form videos for Instagram and LinkedIn.' },
            { icon: 'fa-clock', color: 'text-teal-500', bg: 'bg-teal-50', title: 'Optimize Posting Schedule', body: 'Post at 10 AM on weekdays and 11 AM on weekends. Your audience is most active during these windows.' },
            { icon: 'fa-bullseye', color: 'text-blue-500', bg: 'bg-blue-50', title: 'A/B Test Email Subject Lines', body: 'Run A/B tests on email subjects to boost open rates by 15-20%. Test urgency vs. curiosity-driven headlines.' },
            { icon: 'fa-envelope', color: 'text-orange-500', bg: 'bg-orange-50', title: 'Expand SMS Campaigns', body: 'SMS CTR at 14% shows strong potential. Add personalized flash sale sequences and abandoned cart reminders.' },
            { icon: 'fa-chart-line', color: 'text-green-500', bg: 'bg-green-50', title: 'Cross-Channel Attribution', body: 'Track how social posts drive email signups and SMS opt-ins for a unified view of customer journey.' }
        ];

        container.innerHTML = defaults.map(d => `
            <div class="p-4 ${d.bg} rounded-xl border border-gray-100 flex items-start gap-3">
                <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center flex-shrink-0 shadow-sm">
                    <i class="fas ${d.icon} ${d.color}"></i>
                </div>
                <div>
                    <h4 class="font-bold text-gray-900 mb-1">${d.title}</h4>
                    <p class="text-sm text-gray-600">${d.body}</p>
                </div>
            </div>
        `).join('');
    },

    // ============ UPDATE CHARTS WITH LIVE DATA ============

    /**
     * Update charts with data from API
     */
    updateChartsWithData(data) {
        const metrics = data.data || data;

        // Update reach/engagement chart
        if (this.charts.reachEngagement && metrics.weekly_data) {
            const wd = metrics.weekly_data;
            this.charts.reachEngagement.data.labels = wd.map(w => w.week || w.label);
            this.charts.reachEngagement.data.datasets[0].data = wd.map(w => w.reach);
            this.charts.reachEngagement.data.datasets[1].data = wd.map(w => w.engagement);
            this.charts.reachEngagement.update();
        }

        // Update content type chart
        if (this.charts.contentType && metrics.content_performance) {
            const cp = metrics.content_performance;
            this.charts.contentType.data.labels = cp.map(c => c.type || c.name);
            this.charts.contentType.data.datasets[0].data = cp.map(c => c.count || c.percentage);
            this.charts.contentType.update();
        }

        // Show AI analysis if available
        if (metrics.ai_analysis) {
            const banner = document.getElementById('aiAnalysisBanner');
            const textEl = document.getElementById('aiAnalysisText');
            if (banner && textEl) {
                banner.classList.remove('hidden');
                textEl.innerHTML = this.formatAIResponse(metrics.ai_analysis);
            }
        }
    },

    // ============ REFRESH ALL ============

    /**
     * Refresh all analytics data from AI backend
     */
    async refresh() {
        if (this.isLoading) return;
        this.isLoading = true;
        this.showNotification('Refreshing analytics with AI...', 'info');

        try {
            const [engagement, recommendations] = await Promise.allSettled([
                this.fetchEngagement(),
                this.fetchRecommendations()
            ]);

            if (engagement.status === 'fulfilled' && engagement.value) {
                this.updateEngagementUI(engagement.value);
                this.updateChartsWithData(engagement.value);
            }
            if (recommendations.status === 'fulfilled' && recommendations.value) {
                this.updateRecommendationsUI(recommendations.value);
            }

            // Also reload AI analysis
            this.loadAIAnalysis();

            this.showNotification('Analytics refreshed with AI insights!', 'success');
        } catch (err) {
            console.error('[AnalyticsDashboard] Refresh error:', err);
            this.showNotification('Could not refresh analytics. Using cached data.', 'warning');
        } finally {
            this.isLoading = false;
        }
    },

    // ============ ASK AI ============

    /**
     * Ask AI a question about analytics/performance
     */
    async askAI() {
        const input = document.getElementById('aiAnalyticsQuestion');
        const answerBox = document.getElementById('aiAnalyticsAnswer');
        const answerText = document.getElementById('aiAnalyticsAnswerText');

        if (!input || !answerBox || !answerText) {
            console.error('[AnalyticsDashboard] askAI: Missing DOM elements');
            return;
        }

        const question = input.value.trim();
        if (!question) {
            this.showNotification('Please type a question first.', 'warning');
            input.focus();
            return;
        }

        answerBox.classList.remove('hidden');
        answerText.innerHTML = '<i class="fas fa-spinner fa-spin text-indigo-500"></i> AI is thinking...';

        try {
            // Use contextual AI chat endpoint (RAG-lite: injects live DB data into prompt)
            const response = await fetch(this.getEndpoint('/api/v1/ai/chat'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: `As a marketing analytics expert, analyze this question about our marketing performance: ${question}`,
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            const answer = (data.data && data.data.answer) || data.response || data.answer || data.result || 'No insights available.';
            const source = (data.data && data.data.source) || '';
            answerText.innerHTML = this.formatAIResponse(answer) +
                (source ? `<div class="mt-2 text-xs" style="color:#5f6680;">Answered via ${source === 'gemini' ? 'Gemini AI' : 'Rules Engine'}</div>` : '');
        } catch (err) {
            console.error('[AnalyticsDashboard] askAI error:', err);
            answerText.innerHTML = this.getFallbackAnswer(question);
        }
    },

    // ============ RECOMMENDATIONS ============

    /**
     * Load fresh AI recommendations
     */
    async loadRecommendations() {
        const container = document.getElementById('aiRecommendations');
        if (!container) return;

        container.innerHTML = `
            <div class="col-span-3 text-center py-8">
                <i class="fas fa-spinner fa-spin text-2xl text-teal-500"></i>
                <p class="text-sm text-gray-500 mt-2">AI is generating personalized recommendations...</p>
            </div>`;

        try {
            const data = await this.fetchRecommendations();
            if (data && (data.data && data.data.recommendations || data.recommendations)) {
                this.updateRecommendationsUI(data);
            } else {
                const response = await fetch(this.getEndpoint('/api/v1/agent/ask'), {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question: 'Give me 3 specific marketing recommendations for improving engagement. Format each with a title, description, and expected impact percentage. Focus on social media captions, email campaigns, and SMS marketing.',
                        context: 'marketing_recommendations'
                    })
                });

                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const agentData = await response.json();
                this.renderAgentRecommendations(container, (agentData.data && agentData.data.answer) || agentData.response || agentData.answer || '');
            }
        } catch (err) {
            console.error('[AnalyticsDashboard] loadRecommendations error:', err);
            this.renderDefaultRecommendations(container);
        }
    },

    // ============ DATA FETCHING ============

    async fetchEngagement() {
        try {
            const response = await fetch(this.getEndpoint('/api/v1/ai-analytics/engagement'), {
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) return null;
            return await response.json();
        } catch { return null; }
    },

    async fetchRecommendations() {
        try {
            const response = await fetch(this.getEndpoint('/api/v1/ai-analytics/recommendations'), {
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) return null;
            return await response.json();
        } catch { return null; }
    },

    // ============ UI UPDATES ============

    updateEngagementUI(data) {
        const metrics = data.data || data.metrics || data;
        const healthNum = document.getElementById('healthScoreNum');
        if (healthNum && metrics.health_score) healthNum.textContent = metrics.health_score;

        const updates = {
            'metricReach': metrics.total_reach || metrics.reach,
            'metricER': metrics.engagement_rate,
            'metricFollowers': metrics.new_followers,
            'metricCTR': metrics.click_through_rate || metrics.ctr
        };

        Object.entries(updates).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el && value !== undefined) {
                el.textContent = typeof value === 'number'
                    ? (value > 1000 ? (value / 1000).toFixed(1) + 'K' : value.toString())
                    : value;
            }
        });
    },

    updateRecommendationsUI(data) {
        const container = document.getElementById('aiRecommendations');
        const recs = (data.data && data.data.recommendations) || data.recommendations;
        if (!container || !recs) return;

        const colors = [
            { bg: 'from-teal-50 to-green-50', border: 'border-teal-200', icon: 'text-teal-600', label: 'text-teal-700', impact: 'text-teal-600' },
            { bg: 'from-blue-50 to-purple-50', border: 'border-blue-200', icon: 'text-blue-600', label: 'text-blue-700', impact: 'text-blue-600' },
            { bg: 'from-orange-50 to-red-50', border: 'border-orange-200', icon: 'text-orange-600', label: 'text-orange-700', impact: 'text-orange-600' }
        ];
        const icons = ['fa-clock', 'fa-chart-line', 'fa-envelope'];
        const priorities = ['HIGH PRIORITY', 'HIGH PRIORITY', 'MEDIUM'];

        container.innerHTML = recs.slice(0, 3).map((rec, i) => {
            const c = colors[i % colors.length];
            return `
                <div class="p-4 bg-gradient-to-br ${c.bg} ${c.border} border rounded-xl">
                    <div class="flex items-center gap-2 mb-3">
                        <i class="fas ${icons[i % icons.length]} ${c.icon} text-lg"></i>
                        <span class="text-xs font-bold ${c.label}">${priorities[i % priorities.length]}</span>
                    </div>
                    <h4 class="font-bold text-gray-900 mb-2">${rec.title || rec.action || 'Recommendation'}</h4>
                    <p class="text-sm text-gray-600 mb-3">${rec.description || rec.reason || ''}</p>
                    <span class="text-xs ${c.impact} font-semibold">Expected: ${rec.impact || rec.expected_impact || '+15% improvement'}</span>
                </div>`;
        }).join('');
    },

    renderAgentRecommendations(container, text) {
        const lines = text.split('\n').filter(l => l.trim());
        const cards = [];
        let current = null;

        lines.forEach(line => {
            const trimmed = line.trim();
            if (trimmed.match(/^\d+[\.\)]/)) {
                if (current) cards.push(current);
                current = { title: trimmed.replace(/^\d+[\.\)]\s*/, '').replace(/\*\*/g, ''), description: '' };
            } else if (current) {
                current.description += trimmed.replace(/\*\*/g, '') + ' ';
            }
        });
        if (current) cards.push(current);

        if (cards.length === 0) { this.renderDefaultRecommendations(container); return; }

        const colors = [
            { bg: 'from-teal-50 to-green-50', border: 'border-teal-200', icon: 'text-teal-600', label: 'text-teal-700' },
            { bg: 'from-blue-50 to-purple-50', border: 'border-blue-200', icon: 'text-blue-600', label: 'text-blue-700' },
            { bg: 'from-orange-50 to-red-50', border: 'border-orange-200', icon: 'text-orange-600', label: 'text-orange-700' }
        ];
        const icons = ['fa-clock', 'fa-chart-line', 'fa-envelope'];

        container.innerHTML = cards.slice(0, 3).map((card, i) => {
            const c = colors[i % colors.length];
            return `
                <div class="p-4 bg-gradient-to-br ${c.bg} ${c.border} border rounded-xl">
                    <div class="flex items-center gap-2 mb-3">
                        <i class="fas ${icons[i % icons.length]} ${c.icon} text-lg"></i>
                        <span class="text-xs font-bold ${c.label}">AI RECOMMENDATION</span>
                    </div>
                    <h4 class="font-bold text-gray-900 mb-2">${card.title}</h4>
                    <p class="text-sm text-gray-600">${card.description.trim()}</p>
                </div>`;
        }).join('');
    },

    renderDefaultRecommendations(container) {
        container.innerHTML = `
            <div class="p-4 bg-gradient-to-br from-teal-50 to-green-50 border border-teal-200 rounded-xl">
                <div class="flex items-center gap-2 mb-3">
                    <i class="fas fa-clock text-teal-600 text-lg"></i>
                    <span class="text-xs font-bold text-teal-700">HIGH PRIORITY</span>
                </div>
                <h4 class="font-bold text-gray-900 mb-2">Post at 10 AM for better reach</h4>
                <p class="text-sm text-gray-600 mb-3">Your audience is most active 10-11 AM. Schedule content during this window.</p>
                <span class="text-xs text-teal-600 font-semibold">Expected: +24% reach</span>
            </div>
            <div class="p-4 bg-gradient-to-br from-blue-50 to-purple-50 border border-blue-200 rounded-xl">
                <div class="flex items-center gap-2 mb-3">
                    <i class="fas fa-question-circle text-blue-600 text-lg"></i>
                    <span class="text-xs font-bold text-blue-700">HIGH PRIORITY</span>
                </div>
                <h4 class="font-bold text-gray-900 mb-2">Add questions to captions</h4>
                <p class="text-sm text-gray-600 mb-3">Question-based captions get 18% more comments than statements.</p>
                <span class="text-xs text-blue-600 font-semibold">Expected: +18% comments</span>
            </div>
            <div class="p-4 bg-gradient-to-br from-orange-50 to-red-50 border border-orange-200 rounded-xl">
                <div class="flex items-center gap-2 mb-3">
                    <i class="fas fa-envelope text-orange-600 text-lg"></i>
                    <span class="text-xs font-bold text-orange-700">MEDIUM</span>
                </div>
                <h4 class="font-bold text-gray-900 mb-2">Personalize email subjects</h4>
                <p class="text-sm text-gray-600 mb-3">Personalized subjects increase open rate by 22% on average.</p>
                <span class="text-xs text-orange-600 font-semibold">Expected: +22% open rate</span>
            </div>`;
    },

    // ============ HELPERS ============

    formatAIResponse(text) {
        if (!text) return 'No insights available.';
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n\n/g, '</p><p class="mt-2">')
            .replace(/\n/g, '<br>')
            .replace(/^/, '<p>')
            .replace(/$/, '</p>');
    },

    getFallbackAnswer(question) {
        const q = question.toLowerCase();
        if (q.includes('engagement') || q.includes('drop')) {
            return '<p>Based on typical patterns: Engagement fluctuations are normal. Consider diversifying post times, using more interactive formats like questions in captions, and ensuring consistent posting frequency. Email subject line A/B testing can also improve open rates by 15-20%.</p>';
        }
        if (q.includes('post') || q.includes('caption') || q.includes('what should')) {
            return '<p>Try posting educational content (tips, how-tos) on weekdays and engaging/fun content on weekends. Captions with questions generate 18% more comments. Pair social posts with follow-up email campaigns for maximum reach.</p>';
        }
        if (q.includes('email') || q.includes('open rate')) {
            return '<p>To improve email performance: Personalize subject lines (22% lift), send Tuesdays/Thursdays at 10 AM, keep subject under 50 chars, and use preview text effectively. Segment your list by engagement level.</p>';
        }
        if (q.includes('sms') || q.includes('text')) {
            return '<p>SMS best practices: Keep under 160 chars, include clear CTA, use personalization, send during business hours. Flash sale SMS with urgency words see 14-18% higher CTR.</p>';
        }
        return '<p>I recommend analyzing your top-performing content types (captions, emails, SMS) and doubling down on what works. Focus on consistent posting times and A/B testing different approaches.</p>';
    },

    showNotification(message, type = 'info') {
        const colors = { success: 'bg-green-500', error: 'bg-red-500', warning: 'bg-yellow-500', info: 'bg-blue-500' };
        const existing = document.getElementById('analytics-notification');
        if (existing) existing.remove();

        const notification = document.createElement('div');
        notification.id = 'analytics-notification';
        notification.className = `fixed top-4 right-4 ${colors[type] || colors.info} text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-opacity duration-300`;
        notification.innerHTML = `<i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i> ${message}`;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => AnalyticsDashboard.init());
} else {
    AnalyticsDashboard.init();
}

// Expose globally
window.AnalyticsDashboard = AnalyticsDashboard;
