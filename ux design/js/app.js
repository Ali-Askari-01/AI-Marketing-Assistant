// Views HTML Templates
const views = {
    home: `
        <div class="min-h-screen view-enter" style="background:#0a0e17;">
            <!-- Hero Section with Animated Grid -->
            <div class="px-4 py-10 sm:py-16 relative">
                <div class="hero-grid-bg"></div>
                <div class="max-w-4xl mx-auto text-center relative z-10">
                    <!-- Personalized Greeting -->
                    <div class="time-icon" id="heroTimeIcon">
                        <span id="heroTimeEmoji"></span>
                    </div>
                    <h1 class="text-3xl sm:text-4xl font-bold mb-2" style="color:#ffffff;" id="heroGreeting">
                        Good morning, John
                    </h1>
                    <p class="text-base mb-6 max-w-lg mx-auto" style="color:#5f6680;" id="heroMotivation">
                        Your campaigns are performing well. Let's keep the momentum going.
                    </p>

                    <!-- Streak Banner -->
                    <div class="streak-banner max-w-md mx-auto mb-8">
                        <span class="streak-fire">&#128293;</span>
                        <div class="flex-1 text-left">
                            <p class="text-sm font-bold" style="color:#fbbf24;">5-day streak!</p>
                            <p class="text-xs" style="color:#9aa0b0;">You've logged in 5 days in a row. Keep it up!</p>
                        </div>
                        <div class="pulse-dot flex-shrink-0"></div>
                    </div>
                    
                    <!-- Clear CTA Buttons -->
                    <div class="flex flex-col sm:flex-row gap-3 justify-center mb-12">
                        <button class="px-6 py-3 text-white font-medium rounded-lg transition-all" style="background:linear-gradient(135deg,#6366f1,#8b5cf6); box-shadow:0 4px 15px rgba(99,102,241,0.35);" onclick="app.loadView('strategy')">
                            <i class="fas fa-rocket mr-2"></i> Start Campaign
                        </button>
                        <button class="px-6 py-3 font-medium rounded-lg transition-colors" style="background:rgba(255,255,255,0.04); color:#e8eaed; border:1px solid rgba(255,255,255,0.08);" onclick="app.loadView('analytics')">
                            <i class="fas fa-chart-line mr-2"></i> Analytics
                        </button>
                        <button class="px-6 py-3 font-medium rounded-lg transition-colors" style="background:rgba(255,255,255,0.04); color:#e8eaed; border:1px solid rgba(255,255,255,0.08);" onclick="app.loadView('content')">
                            <i class="fas fa-pen-fancy mr-2"></i> Create Content
                        </button>
                    </div>
                </div>
            </div>
                    
            <!-- Marketing Health Score & Key Metrics -->
            <div class="px-4 pb-12">
                <div class="max-w-6xl mx-auto">
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                        <!-- Marketing Health Score -->
                        <div class="p-6 rounded-xl" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                            <h3 class="text-lg font-semibold mb-6" style="color:#fff;">Marketing Health</h3>
                            <div class="flex flex-col items-center">
                                <div class="health-score relative">
                                    <svg viewBox="0 0 200 200" class="health-score-circle w-32 h-32">
                                        <defs>
                                            <linearGradient id="healthGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                                <stop offset="0%" style="stop-color:#6366f1"/>
                                                <stop offset="100%" style="stop-color:#06b6d4"/>
                                            </linearGradient>
                                        </defs>
                                        <circle cx="100" cy="100" r="90" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="12"/>
                                        <circle cx="100" cy="100" r="90" class="health-score-progress" fill="none" stroke="url(#healthGradient)" stroke-width="12" stroke-dasharray="478" stroke-dashoffset="120" stroke-linecap="round"/>
                                    </svg>
                                    <div class="health-score-text absolute inset-0 flex flex-col items-center justify-center">
                                        <div class="health-score-number text-3xl font-bold" style="color:#ffffff;">75</div>
                                        <div class="text-sm font-semibold" style="color:#9aa0b0;">Good</div>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-6 space-y-3">
                                <div class="flex justify-between text-sm">
                                    <span style="color:#9aa0b0;">Consistency</span>
                                    <span class="font-semibold" style="color:#e8eaed;">92%</span>
                                </div>
                                <div class="flex justify-between text-sm">
                                    <span style="color:#9aa0b0;">Engagement</span>
                                    <span class="font-semibold" style="color:#e8eaed;">68%</span>
                                </div>
                                <div class="flex justify-between text-sm">
                                    <span style="color:#9aa0b0;">Diversity</span>
                                    <span class="font-semibold" style="color:#e8eaed;">81%</span>
                                </div>
                            </div>
                        </div>

                        <!-- Key Metrics Grid -->
                        <div class="lg:col-span-2">
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
                                <div class="text-center p-4 rounded-xl" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                                    <div class="text-3xl font-bold mb-1" style="color:#818cf8;">87%</div>
                                    <div class="text-sm" style="color:#9aa0b0;">Time Saved</div>
                                </div>
                                <div class="text-center p-4 rounded-xl" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                                    <div class="text-3xl font-bold mb-1" style="color:#06b6d4;">3.2x</div>
                                    <div class="text-sm" style="color:#9aa0b0;">Engagement</div>
                                </div>
                                <div class="text-center p-4 rounded-xl" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                                    <div class="text-3xl font-bold mb-1" style="color:#8b5cf6;">5</div>
                                    <div class="text-sm" style="color:#9aa0b0;">Platforms</div>
                                </div>
                                <div class="text-center p-4 rounded-xl" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                                    <div class="text-3xl font-bold mb-1" style="color:#f59e0b;">24/7</div>
                                    <div class="text-sm" style="color:#9aa0b0;">AI Assistant</div>
                                </div>
                            </div>
                            
                            <!-- Today's Tasks -->
                            <div>
                                <h3 class="text-lg font-semibold mb-4" style="color:#ffffff;">Today's Tasks</h3>
                                <div class="space-y-3">
                                    <div class="flex items-center gap-4 p-4 rounded-xl cursor-pointer transition" style="background:rgba(249,115,22,0.08); border:1px solid rgba(249,115,22,0.2);">
                                        <div class="w-10 h-10 rounded-lg flex items-center justify-center text-white flex-shrink-0" style="background:#f97316;">
                                            <i class="fas fa-exclamation"></i>
                                        </div>
                                        <div class="flex-1">
                                            <p class="font-semibold" style="color:#e8eaed;">3 drafts need approval</p>
                                            <p class="text-sm" style="color:#9aa0b0;">Content Studio</p>
                                        </div>
                                        <button class="font-semibold text-sm flex-shrink-0" style="color:#fb923c;">
                                            Review â†’
                                        </button>
                                    </div>
                                    <div class="flex items-center gap-4 p-4 rounded-xl cursor-pointer transition" style="background:rgba(59,130,246,0.08); border:1px solid rgba(59,130,246,0.2);">
                                        <div class="w-10 h-10 rounded-lg flex items-center justify-center text-white flex-shrink-0" style="background:#3b82f6;">
                                            <i class="fas fa-calendar"></i>
                                        </div>
                                        <div class="flex-1">
                                            <p class="font-semibold" style="color:#e8eaed;">2 posts scheduled</p>
                                            <p class="text-sm" style="color:#9aa0b0;">Campaign Calendar</p>
                                        </div>
                                        <button class="font-semibold text-sm flex-shrink-0" style="color:#60a5fa;">
                                            View â†’
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features - Interactive Glow Cards -->
            <div class="px-4 pb-12" style="background:#0f1419;">
                <div class="max-w-6xl mx-auto pt-12">
                    <h2 class="text-2xl font-bold text-center mb-2" style="color:#ffffff;">Everything You Need</h2>
                    <p class="text-center text-sm mb-8" style="color:#5f6680;">Click any card to jump right in</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div class="glow-card p-6 rounded-xl cursor-pointer" style="background:#131825; border:1px solid rgba(255,255,255,0.06);" onclick="app.loadView('strategy')">
                            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4 glow-card-icon" style="background:rgba(99,102,241,0.12); color:#818cf8;">
                                <i class="fas fa-brain text-xl"></i>
                            </div>
                            <h3 class="text-lg font-semibold mb-2" style="color:#e8eaed;">AI Strategy</h3>
                            <p class="text-sm" style="color:#9aa0b0;">Generate 30-day campaigns with weekly themes and KPIs.</p>
                        </div>

                        <div class="glow-card p-6 rounded-xl cursor-pointer" style="background:#131825; border:1px solid rgba(255,255,255,0.06);" onclick="app.loadView('content')">
                            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4 glow-card-icon" style="background:rgba(139,92,246,0.12); color:#a78bfa;">
                                <i class="fas fa-pen-fancy text-xl"></i>
                            </div>
                            <h3 class="text-lg font-semibold mb-2" style="color:#e8eaed;">Content Creation</h3>
                            <p class="text-sm" style="color:#9aa0b0;">Create platform-specific posts with AI optimization.</p>
                        </div>

                        <div class="glow-card p-6 rounded-xl cursor-pointer" style="background:#131825; border:1px solid rgba(255,255,255,0.06);" onclick="app.loadView('calendar')">
                            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4 glow-card-icon" style="background:rgba(245,158,11,0.12); color:#fbbf24;">
                                <i class="fas fa-calendar-alt text-xl"></i>
                            </div>
                            <h3 class="text-lg font-semibold mb-2" style="color:#e8eaed;">Smart Calendar</h3>
                            <p class="text-sm" style="color:#9aa0b0;">Visual scheduling with drag-and-drop timing optimization.</p>
                        </div>

                        <div class="glow-card p-6 rounded-xl cursor-pointer" style="background:#131825; border:1px solid rgba(255,255,255,0.06);" onclick="app.loadView('analytics')">
                            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4 glow-card-icon" style="background:rgba(16,185,129,0.12); color:#34d399;">
                                <i class="fas fa-chart-line text-xl"></i>
                            </div>
                            <h3 class="text-lg font-semibold mb-2" style="color:#e8eaed;">Analytics</h3>
                            <p class="text-sm" style="color:#9aa0b0;">Real-time insights and AI recommendations.</p>
                        </div>

                        <div class="glow-card p-6 rounded-xl cursor-pointer" style="background:#131825; border:1px solid rgba(255,255,255,0.06);" onclick="app.loadView('inbox')">
                            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4 glow-card-icon" style="background:rgba(59,130,246,0.12); color:#60a5fa;">
                                <i class="fas fa-inbox text-xl"></i>
                            </div>
                            <h3 class="text-lg font-semibold mb-2" style="color:#e8eaed;">Communication</h3>
                            <p class="text-sm" style="color:#9aa0b0;">Unified inbox with AI replies and engagement.</p>
                        </div>

                        <div class="glow-card p-6 rounded-xl cursor-pointer" style="background:#131825; border:1px solid rgba(255,255,255,0.06);" onclick="app.loadView('settings')">
                            <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4 glow-card-icon" style="background:rgba(236,72,153,0.12); color:#f472b6;">
                                <i class="fas fa-rocket text-xl"></i>
                            </div>
                            <h3 class="text-lg font-semibold mb-2" style="color:#e8eaed;">All-in-One</h3>
                            <p class="text-sm" style="color:#9aa0b0;">Complete platform that saves time and drives results.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Activity -->
            <div class="px-4 pb-12">
                <div class="max-w-6xl mx-auto">
                    <h2 class="text-2xl font-bold text-center mb-8" style="color:#ffffff;">Recent Activity</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="p-4 rounded-lg" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="w-10 h-10 rounded-full flex items-center justify-center" style="background:rgba(16,185,129,0.12);">
                                    <i class="fas fa-check" style="color:#34d399;"></i>
                                </div>
                                <div>
                                    <p class="font-semibold" style="color:#e8eaed;">Campaign Completed</p>
                                    <p class="text-xs" style="color:#5f6680;">2 hours ago</p>
                                </div>
                            </div>
                            <p class="text-sm" style="color:#9aa0b0;">"Product Launch" finished with 15 posts</p>
                        </div>
                        
                        <div class="p-4 rounded-lg" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="w-10 h-10 rounded-full flex items-center justify-center" style="background:rgba(59,130,246,0.12);">
                                    <i class="fas fa-chart-line" style="color:#60a5fa;"></i>
                                </div>
                                <div>
                                    <p class="font-semibold" style="color:#e8eaed;">Report Generated</p>
                                    <p class="text-xs" style="color:#5f6680;">5 hours ago</p>
                                </div>
                            </div>
                            <p class="text-sm" style="color:#9aa0b0;">Weekly report shows 23% engagement increase</p>
                        </div>
                        
                        <div class="p-4 rounded-lg" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="w-10 h-10 rounded-full flex items-center justify-center" style="background:rgba(139,92,246,0.12);">
                                    <i class="fas fa-magic" style="color:#a78bfa;"></i>
                                </div>
                                <div>
                                    <p class="font-semibold" style="color:#e8eaed;">Content Created</p>
                                    <p class="text-xs" style="color:#5f6680;">1 day ago</p>
                                </div>
                            </div>
                            <p class="text-sm" style="color:#9aa0b0;">AI generated 12 new posts ready for review</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    strategy: `
        <div class="p-4 sm:p-6 md:p-8 max-w-6xl mx-auto view-enter" style="background:#0a0e17;">
            <div class="mb-6 md:mb-8">
                <h1 class="text-2xl sm:text-3xl font-bold mb-2" style="color:#ffffff;">Create Campaign Strategy</h1>
                <p class="text-sm sm:text-base" style="color:#9aa0b0;">Let AI generate a data-driven marketing plan tailored to your business</p>
            </div>

            <div id="wizardContainer" class="p-6 sm:p-8 rounded-2xl" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                <!-- Progress Bar -->
                <div class="mb-8">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-2">
                            <div class="wizard-step-indicator w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" data-step="1" style="background:#6366f1; color:#fff;">1</div>
                            <span class="text-sm font-medium hidden sm:inline" style="color:#e8eaed;">Business</span>
                        </div>
                        <div class="flex-1 h-1 mx-3 rounded-full" style="background:rgba(255,255,255,0.06);">
                            <div id="progressBar" class="h-1 rounded-full transition-all duration-500" style="width:25%; background:linear-gradient(90deg,#6366f1,#06b6d4);"></div>
                        </div>
                        <div class="flex items-center gap-2">
                            <div class="wizard-step-indicator w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" data-step="2" style="background:rgba(255,255,255,0.06); color:#5f6680;">2</div>
                            <span class="text-sm font-medium hidden sm:inline" style="color:#5f6680;">Goals</span>
                        </div>
                        <div class="flex-1 h-1 mx-3 rounded-full" style="background:rgba(255,255,255,0.06);"></div>
                        <div class="flex items-center gap-2">
                            <div class="wizard-step-indicator w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" data-step="3" style="background:rgba(255,255,255,0.06); color:#5f6680;">3</div>
                            <span class="text-sm font-medium hidden sm:inline" style="color:#5f6680;">Generate</span>
                        </div>
                        <div class="flex-1 h-1 mx-3 rounded-full" style="background:rgba(255,255,255,0.06);"></div>
                        <div class="flex items-center gap-2">
                            <div class="wizard-step-indicator w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" data-step="4" style="background:rgba(255,255,255,0.06); color:#5f6680;">4</div>
                            <span class="text-sm font-medium hidden sm:inline" style="color:#5f6680;">Review</span>
                        </div>
                    </div>
                </div>

                <!-- Step 1: Business Context -->
                <div id="step1" class="wizard-step">
                    <div class="mb-8">
                        <div class="flex items-center gap-3 mb-3">
                            <div class="w-11 h-11 rounded-xl flex items-center justify-center" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);">
                                <i class="fas fa-building text-white"></i>
                            </div>
                            <div>
                                <h2 class="text-xl font-bold" style="color:#ffffff;">Business Context</h2>
                                <p class="text-sm" style="color:#9aa0b0;">Tell us about your business and goals</p>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Business Name <span style="color:#ef4444;">*</span></label>
                                <input type="text" id="businessName" class="strat-input w-full px-4 py-3 rounded-lg text-sm" placeholder="e.g., TechFlow Solutions">
                            </div>
                            <div>
                                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Industry <span style="color:#ef4444;">*</span></label>
                                <select id="industry" class="strat-input w-full px-4 py-3 rounded-lg text-sm">
                                    <option value="">Select your industry</option>
                                    <option value="technology">SaaS / Technology</option>
                                    <option value="ecommerce">E-commerce</option>
                                    <option value="consulting">Consulting</option>
                                    <option value="healthcare">Healthcare</option>
                                    <option value="education">Education</option>
                                    <option value="fitness">Fitness & Wellness</option>
                                    <option value="food">Food & Beverage</option>
                                    <option value="fashion">Fashion & Beauty</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Target Audience</label>
                                <input type="text" id="targetAudience" class="strat-input w-full px-4 py-3 rounded-lg text-sm" placeholder="e.g., B2B founders, 25-40 age">
                            </div>
                        </div>

                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Brand Tone</label>
                                <div class="grid grid-cols-2 gap-3">
                                    <button class="tone-option active" data-tone="professional">
                                        <i class="fas fa-briefcase"></i>
                                        <span>Professional</span>
                                    </button>
                                    <button class="tone-option" data-tone="friendly">
                                        <i class="fas fa-smile"></i>
                                        <span>Friendly</span>
                                    </button>
                                    <button class="tone-option" data-tone="bold">
                                        <i class="fas fa-rocket"></i>
                                        <span>Bold</span>
                                    </button>
                                    <button class="tone-option" data-tone="inspirational">
                                        <i class="fas fa-lightbulb"></i>
                                        <span>Inspirational</span>
                                    </button>
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Monthly Budget</label>
                                <select id="budget" class="strat-input w-full px-4 py-3 rounded-lg text-sm">
                                    <option value="">Select budget range</option>
                                    <option value="$0 - $500">$0 - $500</option>
                                    <option value="$500 - $2,000">$500 - $2,000</option>
                                    <option value="$2,000 - $5,000">$2,000 - $5,000</option>
                                    <option value="$5,000 - $10,000">$5,000 - $10,000</option>
                                    <option value="$10,000+">$10,000+</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Primary Goal <span style="color:#ef4444;">*</span></label>
                                <select id="goal" class="strat-input w-full px-4 py-3 rounded-lg text-sm">
                                    <option value="">Select your primary goal</option>
                                    <option value="awareness">Brand Awareness</option>
                                    <option value="engagement">Engagement & Community</option>
                                    <option value="leads">Lead Generation</option>
                                    <option value="sales">Sales & Conversions</option>
                                    <option value="retention">Customer Retention</option>
                                    <option value="growth">Audience Growth</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="mt-8 flex justify-between items-center">
                        <p class="text-xs" style="color:#5f6680;"><span style="color:#ef4444;">*</span> Required fields</p>
                        <button onclick="app.validateAndNext(2)" class="btn btn-primary">
                            Continue <i class="fas fa-arrow-right ml-2"></i>
                        </button>
                    </div>
                </div>

                <!-- Step 2: Campaign Goals -->
                <div id="step2" class="wizard-step hidden">
                    <div class="mb-8">
                        <div class="flex items-center gap-3 mb-3">
                            <div class="w-11 h-11 rounded-xl flex items-center justify-center" style="background:linear-gradient(135deg,#06b6d4,#22d3ee);">
                                <i class="fas fa-bullseye text-white"></i>
                            </div>
                            <div>
                                <h2 class="text-xl font-bold" style="color:#ffffff;">Campaign Goals</h2>
                                <p class="text-sm" style="color:#9aa0b0;">Define your campaign objectives and success metrics</p>
                            </div>
                        </div>
                    </div>

                    <div class="space-y-6">
                        <div>
                            <label class="block text-sm font-semibold mb-3" style="color:#c4c8d4;">Campaign Duration</label>
                            <div class="grid grid-cols-3 gap-3">
                                <button class="duration-option" data-duration="7">
                                    <span class="text-lg font-bold" style="color:#e8eaed;">7</span>
                                    <span class="text-sm" style="color:#9aa0b0;">Days</span>
                                </button>
                                <button class="duration-option active" data-duration="30">
                                    <span class="text-lg font-bold" style="color:#e8eaed;">30</span>
                                    <span class="text-sm" style="color:#9aa0b0;">Days</span>
                                </button>
                                <button class="duration-option" data-duration="90">
                                    <span class="text-lg font-bold" style="color:#e8eaed;">90</span>
                                    <span class="text-sm" style="color:#9aa0b0;">Days</span>
                                </button>
                            </div>
                        </div>

                        <div>
                            <label class="block text-sm font-semibold mb-3" style="color:#c4c8d4;">Key Performance Indicators</label>
                            <div class="grid grid-cols-2 gap-3">
                                <label class="strat-check flex items-center gap-3 p-3 rounded-lg cursor-pointer">
                                    <input type="checkbox" class="w-4 h-4 accent-indigo-500" checked>
                                    <span class="text-sm" style="color:#c4c8d4;">Reach & Impressions</span>
                                </label>
                                <label class="strat-check flex items-center gap-3 p-3 rounded-lg cursor-pointer">
                                    <input type="checkbox" class="w-4 h-4 accent-indigo-500" checked>
                                    <span class="text-sm" style="color:#c4c8d4;">Engagement Rate</span>
                                </label>
                                <label class="strat-check flex items-center gap-3 p-3 rounded-lg cursor-pointer">
                                    <input type="checkbox" class="w-4 h-4 accent-indigo-500">
                                    <span class="text-sm" style="color:#c4c8d4;">Click-Through Rate</span>
                                </label>
                                <label class="strat-check flex items-center gap-3 p-3 rounded-lg cursor-pointer">
                                    <input type="checkbox" class="w-4 h-4 accent-indigo-500">
                                    <span class="text-sm" style="color:#c4c8d4;">Conversion Rate</span>
                                </label>
                            </div>
                        </div>

                        <div>
                            <label class="block text-sm font-semibold mb-3" style="color:#c4c8d4;">Target Platforms</label>
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                                <label class="strat-check flex items-center gap-2 p-3 rounded-lg cursor-pointer">
                                    <i class="fab fa-instagram text-pink-400"></i>
                                    <span class="text-sm" style="color:#c4c8d4;">Instagram</span>
                                    <input type="checkbox" class="w-4 h-4 accent-indigo-500 ml-auto" checked>
                                </label>
                                <label class="strat-check flex items-center gap-2 p-3 rounded-lg cursor-pointer">
                                    <i class="fab fa-linkedin text-blue-400"></i>
                                    <span class="text-sm" style="color:#c4c8d4;">LinkedIn</span>
                                    <input type="checkbox" class="w-4 h-4 accent-indigo-500 ml-auto">
                                </label>
                                <label class="strat-check flex items-center gap-2 p-3 rounded-lg cursor-pointer">
                                    <i class="fas fa-envelope" style="color:#818cf8;"></i>
                                    <span class="text-sm" style="color:#c4c8d4;">Email</span>
                                    <input type="checkbox" class="w-4 h-4 accent-indigo-500 ml-auto" checked>
                                </label>
                                <label class="strat-check flex items-center gap-2 p-3 rounded-lg cursor-pointer">
                                    <i class="fas fa-sms text-green-400"></i>
                                    <span class="text-sm" style="color:#c4c8d4;">SMS</span>
                                    <input type="checkbox" class="w-4 h-4 accent-indigo-500 ml-auto">
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="mt-8 flex justify-between">
                        <button onclick="app.showStep(1)" class="btn btn-secondary">
                            <i class="fas fa-arrow-left mr-2"></i> Back
                        </button>
                        <button onclick="app.generateCampaignStrategy()" class="btn btn-primary">
                            <i class="fas fa-wand-magic-sparkles mr-2"></i> Generate Strategy
                        </button>
                    </div>
                </div>

                <!-- Step 3: AI Generating -->
                <div id="step3" class="wizard-step hidden">
                    <div class="text-center py-12">
                        <div class="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse" style="background:linear-gradient(135deg,#6366f1,#06b6d4); box-shadow:0 0 40px rgba(99,102,241,0.35);">
                            <i class="fas fa-brain text-white text-3xl"></i>
                        </div>
                        <h2 class="text-2xl font-bold mb-3" style="color:#ffffff;">AI is crafting your strategy...</h2>
                        <p class="mb-8" style="color:#9aa0b0;">Analyzing your inputs and building a custom campaign</p>

                        <div id="generationProgress" class="max-w-md mx-auto space-y-3 text-left">
                            <div id="progress1" class="flex items-center gap-3 p-3 rounded-lg" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                                <i class="fas fa-spinner fa-spin" style="color:#6366f1;"></i>
                                <span class="text-sm" style="color:#9aa0b0;">Analyzing business context...</span>
                            </div>
                            <div id="progress2" class="flex items-center gap-3 p-3 rounded-lg opacity-40" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                                <i class="fas fa-circle text-xs" style="color:#5f6680;"></i>
                                <span class="text-sm" style="color:#5f6680;">Generating campaign calendar...</span>
                            </div>
                            <div id="progress3" class="flex items-center gap-3 p-3 rounded-lg opacity-40" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                                <i class="fas fa-circle text-xs" style="color:#5f6680;"></i>
                                <span class="text-sm" style="color:#5f6680;">Creating weekly themes...</span>
                            </div>
                            <div id="progress4" class="flex items-center gap-3 p-3 rounded-lg opacity-40" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                                <i class="fas fa-circle text-xs" style="color:#5f6680;"></i>
                                <span class="text-sm" style="color:#5f6680;">Defining KPIs & benchmarks...</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Step 4: Review Strategy (dynamically filled by renderStrategyReview) -->
                <div id="step4" class="wizard-step hidden">
                    <div class="text-center py-12" style="color:#9aa0b0;">
                        <i class="fas fa-spinner fa-spin text-2xl mb-4" style="color:#6366f1;"></i>
                        <p>Loading strategy results...</p>
                    </div>
                </div>
            </div>
        </div>

        <style>
            .strat-input {
                background: #0d1220;
                border: 1px solid rgba(255,255,255,0.08);
                color: #e8eaed;
                transition: border-color 0.2s, box-shadow 0.2s;
            }
            .strat-input:focus {
                outline: none;
                border-color: #6366f1;
                box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
            }
            .strat-input::placeholder { color: #5f6680; }
            .strat-input option { background: #131825; color: #e8eaed; }
            .strat-input.input-error { border-color: #ef4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.15); }
            .strat-check {
                background: #0d1220;
                border: 1px solid rgba(255,255,255,0.08);
                transition: all 0.2s;
            }
            .strat-check:hover { border-color: rgba(99,102,241,0.3); background: #1a2033; }
            .tone-option {
                display: flex; flex-direction: column; align-items: center; gap: 8px;
                padding: 16px; border: 2px solid rgba(255,255,255,0.08); border-radius: 12px;
                background: #131825; cursor: pointer; transition: all 0.2s; color: #9aa0b0;
            }
            .tone-option:hover { border-color: rgba(99,102,241,0.3); background: #1a2033; }
            .tone-option.active { border-color: #6366f1; background: rgba(99,102,241,0.1); }
            .tone-option i { font-size: 24px; color: #5f6680; }
            .tone-option.active i { color: #818cf8; }
            .tone-option span { font-size: 14px; font-weight: 600; color: #c4c8d4; }
            .duration-option {
                display: flex; flex-direction: column; align-items: center; padding: 16px;
                border: 2px solid rgba(255,255,255,0.08); border-radius: 12px;
                background: #131825; cursor: pointer; transition: all 0.2s; color: #9aa0b0;
            }
            .duration-option:hover { border-color: rgba(99,102,241,0.3); background: #1a2033; }
            .duration-option.active { border-color: #6366f1; background: rgba(99,102,241,0.1); }
        </style>
    `,

    content: `
        <div class="p-4 sm:p-6 md:p-8 max-w-7xl mx-auto fade-in">
            <div class="mb-6 md:mb-8">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">AI Content Studio</h1>
                        <p class="text-sm sm:text-base text-gray-600">Create platform-optimized content with AI</p>
                    </div>
                    <div class="flex items-center gap-3">
                        <button class="btn btn-primary">
                            <i class="fas fa-plus"></i> Create New Content
                        </button>
                        <button class="btn btn-secondary">
                            <i class="fas fa-upload"></i> Import Media
                        </button>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
                <!-- Content List -->
                <div class="lg:col-span-3">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="text-sm font-bold text-gray-900">Content Calendar</h3>
                            <button class="text-sm text-teal-600 hover:text-teal-700" onclick="app.refreshContentCalendar()">
                                <i class="fas fa-sync"></i>
                            </button>
                        </div>
                        <div id="contentCalendarList" class="space-y-2">
                            <!-- Dynamically populated from saved drafts -->
                            <div class="p-3 text-center text-gray-400 text-xs">Loading drafts...</div>
                        </div>
                    </div>

                    <!-- Quick Actions -->
                    <div class="card mt-4">
                        <div class="card-header">
                            <h3 class="text-sm font-bold text-gray-900">Quick Actions</h3>
                        </div>
                        <div class="p-4 space-y-3">
                            <button class="w-full btn btn-secondary text-left" onclick="app.generateWeekContent()">
                                <i class="fas fa-magic mr-2"></i> Generate Week's Content
                            </button>
                            <button class="w-full btn btn-secondary text-left" onclick="app.loadView('posts')">
                                <i class="fas fa-copy mr-2"></i> View All Posts
                            </button>
                            <button class="w-full btn btn-secondary text-left" onclick="app.showToast('Batch scheduling coming soon!')">
                                <i class="fas fa-calendar mr-2"></i> Batch Schedule
                            </button>
                        </div>
                    </div>

                    <!-- Voice-to-Campaign (AssemblyAI) -->
                    <div class="card mt-4">
                        <div class="card-header">
                            <h3 class="text-sm font-bold text-gray-900">
                                <i class="fas fa-microphone text-red-500"></i> Voice to Campaign
                            </h3>
                        </div>
                        <div class="p-4">
                            <p class="text-xs text-gray-500 mb-3">Upload an audio file and AI will create a campaign brief from your voice.</p>
                            <input type="file" id="voiceFileInput" accept="audio/*" class="hidden" onchange="app.handleVoiceToCampaign(this)">
                            <button class="w-full btn btn-secondary text-left" onclick="document.getElementById('voiceFileInput').click()">
                                <i class="fas fa-upload mr-2"></i> Upload Audio File
                            </button>
                            <div id="voiceCampaignResult" class="mt-3 hidden"></div>
                        </div>
                    </div>
                </div>

                <!-- Main Editor -->
                <div class="lg:col-span-6">
                    <div class="card">
                        <div class="card-header">
                            <div class="flex items-center justify-between">
                                <h3 class="card-title">Product Launch Caption</h3>
                                <div class="flex items-center gap-2">
                                    <span class="status-pill status-draft">
                                        <i class="fas fa-circle"></i> Draft
                                    </span>
                                    <button class="text-sm text-teal-600 hover:text-teal-700">
                                        <i class="fas fa-ellipsis-v"></i>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Content Type Selector -->
                        <div class="mb-4">
                            <div class="flex gap-2 p-1 rounded-lg" id="contentTypeSelector" style="background:#0f1419;">
                                <button class="content-type-btn px-3 py-2 shadow-sm rounded text-sm font-medium" data-type="caption" onclick="ContentStudio.switchContentType('caption')" style="background:#1a2033; color:#e8eaed;"><i class="fas fa-comment-dots mr-1"></i> Caption</button>
                                <button class="content-type-btn px-3 py-2 text-sm font-medium text-gray-600" data-type="email" onclick="ContentStudio.switchContentType('email')"><i class="fas fa-envelope mr-1"></i> Email</button>
                                <button class="content-type-btn px-3 py-2 text-sm font-medium text-gray-600" data-type="sms" onclick="ContentStudio.switchContentType('sms')"><i class="fas fa-sms mr-1"></i> SMS</button>
                                <button class="content-type-btn px-3 py-2 text-sm font-medium text-gray-600" data-type="post_idea" onclick="ContentStudio.switchContentType('post_idea')"><i class="fas fa-lightbulb mr-1"></i> Ideas</button>
                            </div>
                        </div>

                        <!-- Dynamic Content Form Container -->
                        <div id="contentFormContainer">
                            <!-- Content form will be dynamically loaded here -->
                        </div>
                    </div>
                </div>

                <!-- AI Optimization Panel -->
                <div class="lg:col-span-3">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="text-sm font-bold text-gray-900">
                                <i class="fas fa-magic text-purple-500"></i> AI Content Assistant
                            </h3>
                        </div>

                        <!-- AI Content Analysis (Dynamic) -->
                        <div class="mb-6">
                            <h4 class="text-sm font-semibold text-gray-900 mb-3">
                                <i class="fas fa-brain text-purple-500"></i> AI Content Analysis
                            </h4>
                            <div id="aiContentAnalysis" class="space-y-3">
                                <div class="p-3 bg-gray-50 border border-gray-200 rounded-lg text-center">
                                    <i class="fas fa-pen-fancy text-gray-400 mb-2"></i>
                                    <p class="text-xs text-gray-500">Start typing content to get AI analysis</p>
                                </div>
                            </div>
                            <button class="mt-3 w-full text-xs text-center text-purple-600 font-bold hover:text-purple-700 py-2 bg-purple-50 rounded-lg" onclick="ContentStudio.analyzeContentWithAI()">
                                <i class="fas fa-brain mr-1"></i> Analyze Content Now
                            </button>
                        </div>

                        <!-- Performance Forecast -->
                        <div class="mb-4">
                            <h4 class="text-xs font-semibold text-gray-900 mb-2">Performance Forecast</h4>
                            <div class="p-3 bg-purple-50 border border-purple-200 rounded-lg">
                                <div class="flex items-center gap-2 mb-2">
                                    <i class="fas fa-chart-line text-purple-600 text-xs"></i>
                                    <span class="text-[10px] font-bold text-purple-700">PREDICTED PERFORMANCE</span>
                                </div>
                                <div class="space-y-1.5">
                                    <div class="flex justify-between text-xs">
                                        <span class="text-gray-600">Engagement Rate</span>
                                        <span class="font-semibold text-green-600">6.2%</span>
                                    </div>
                                    <div class="flex justify-between text-xs">
                                        <span class="text-gray-600">Reach</span>
                                        <span class="font-semibold text-blue-600">12.5K</span>
                                    </div>
                                    <div class="flex justify-between text-xs">
                                        <span class="text-gray-600">Click-Through</span>
                                        <span class="font-semibold text-purple-600">3.1%</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Visual Optimization -->
                        <div class="mb-4">
                            <h4 class="text-xs font-semibold text-gray-900 mb-2">Visual Optimization</h4>
                            <div class="space-y-2">
                                <!-- Thumbnail -->
                                <div class="p-2 bg-orange-50 border border-orange-200 rounded-lg">
                                    <div class="flex items-center gap-2 mb-1">
                                        <i class="fas fa-palette text-orange-600 text-xs"></i>
                                        <span class="text-[10px] font-bold text-orange-700">THUMBNAIL</span>
                                    </div>
                                    <div id="thumbnailPreview" class="w-full h-24 bg-gray-200 rounded flex items-center justify-center overflow-hidden">
                                        <i class="fas fa-image text-gray-400"></i>
                                    </div>
                                    <button class="text-[10px] text-orange-600 font-semibold hover:text-orange-700 mt-1" onclick="app.generateThumbnail()">
                                        <i class="fas fa-magic mr-1"></i> Generate thumbnail
                                    </button>
                                </div>

                                <!-- Text Styles -->
                                <div class="p-2 bg-pink-50 border border-pink-200 rounded-lg">
                                    <div class="flex items-center gap-2 mb-1">
                                        <i class="fas fa-text-height text-pink-600 text-xs"></i>
                                        <span class="text-[10px] font-bold text-pink-700">TEXT STYLES</span>
                                    </div>
                                    <div class="grid grid-cols-2 gap-1">
                                        <button class="px-2 py-1 bg-white border border-gray-200 rounded text-[10px] hover:bg-pink-100" onclick="app.applyTextStyle('bold')"><b>Bold</b></button>
                                        <button class="px-2 py-1 bg-white border border-gray-200 rounded text-[10px] hover:bg-pink-100" onclick="app.applyTextStyle('italic')"><i>Italic</i></button>
                                        <button class="px-2 py-1 bg-white border border-gray-200 rounded text-[10px] hover:bg-pink-100" onclick="app.applyTextStyle('uppercase')">UPPER</button>
                                        <button class="px-2 py-1 bg-white border border-gray-200 rounded text-[10px] hover:bg-pink-100" onclick="app.applyTextStyle('hashtags')"> #Tags</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Generate Options -->
                        <div class="space-y-2">
                            <button class="btn btn-primary w-full text-xs py-2" onclick="ContentStudio.generateOptimizedVersion()">
                                <i class="fas fa-magic mr-1"></i> Generate Optimized Version
                            </button>
                            <button class="btn btn-secondary w-full text-xs py-2" onclick="app.translateContent('spanish')">
                                <i class="fas fa-language mr-1"></i> Translate to Spanish
                            </button>
                            <button class="btn btn-secondary w-full text-xs py-2" onclick="app.adaptForMobile()">
                                <i class="fas fa-mobile-alt mr-1"></i> Adapt for Mobile
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,

    calendar: `
        <div class="p-4 sm:p-6 md:p-8 max-w-7xl mx-auto fade-in">
            <div class="mb-6 md:mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">Campaign Calendar</h1>
                    <p class="text-sm sm:text-base text-gray-600">Schedule and manage your content across all platforms</p>
                </div>
                <div class="flex items-center gap-3">
                    <button class="btn btn-secondary" onclick="app.loadView('strategy')">
                        <i class="fas fa-plus"></i> Create Campaign
                    </button>
                    <div class="flex bg-gray-100 rounded-lg p-1">
                        <button class="px-3 py-1 bg-white rounded text-sm font-medium">Month</button>
                        <button class="px-3 py-1 text-sm font-medium text-gray-600">Week</button>
                        <button class="px-3 py-1 text-sm font-medium text-gray-600">Day</button>
                    </div>
                </div>
            </div>

            <!-- Campaign Overview -->
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-6">
                <div class="card">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-900">Active Campaign</h3>
                        <span class="status-pill status-active">Active</span>
                    </div>
                    <h4 class="font-bold text-gray-900 mb-2">30-Day Brand Awareness</h4>
                    <div class="space-y-3">
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-600">Progress</span>
                            <span class="font-semibold text-gray-900">12/30 days</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-teal-500 h-2 rounded-full" style="width: 40%"></div>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-600">Published</span>
                            <span class="font-semibold text-green-600">8 posts</span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-600">Scheduled</span>
                            <span class="font-semibold text-blue-600">4 posts</span>
                        </div>
                    </div>
                </div>
                
                <div class="lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="metric-card">
                        <div class="metric-label">This Week</div>
                        <div class="metric-value">7 posts</div>
                        <div class="metric-change positive">
                            <i class="fas fa-arrow-up"></i>
                            <span>2 more than last week</span>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Engagement Rate</div>
                        <div class="metric-value">4.2%</div>
                        <div class="metric-change positive">
                            <i class="fas fa-arrow-up"></i>
                            <span>+0.8%</span>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Total Reach</div>
                        <div class="metric-value">8.5K</div>
                        <div class="metric-change positive">
                            <i class="fas fa-arrow-up"></i>
                            <span>+15%</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Calendar View -->
            <div class="card">
                <div class="card-header">
                    <div class="flex items-center justify-between">
                        <h3 class="card-title" id="calendarMonthTitle">Loading...</h3>
                        <div class="flex items-center gap-2">
                            <button class="text-sm text-teal-600 font-semibold hover:text-teal-700" onclick="app.calendarPrevMonth()">
                                <i class="fas fa-chevron-left"></i>
                            </button>
                            <button class="text-sm text-teal-600 font-semibold hover:text-teal-700 px-2" onclick="app.calendarToday()">Today</button>
                            <button class="text-sm text-teal-600 font-semibold hover:text-teal-700" onclick="app.calendarNextMonth()">
                                <i class="fas fa-chevron-right"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="p-4">
                    <div class="grid grid-cols-7 gap-px text-center text-xs font-bold text-gray-500 mb-1">
                        <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
                    </div>
                    <div id="calendarGrid" class="grid grid-cols-7 gap-px bg-gray-200 rounded-lg overflow-hidden">
                        <!-- JS populates -->
                    </div>
                </div>
            </div>
        </div>
    `,

    analytics: `
        <div class="p-4 sm:p-6 md:p-8 max-w-7xl mx-auto fade-in">
            <div class="mb-6 md:mb-8">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2"><i class="fas fa-brain text-purple-500"></i> AI Analytics Dashboard</h1>
                        <p class="text-sm sm:text-base text-gray-600">AI-powered insights, engagement analysis & smart recommendations</p>
                    </div>
                    <div class="flex items-center gap-3">
                        <button class="btn btn-secondary" onclick="AnalyticsDashboard.refresh()">
                            <i class="fas fa-sync"></i> Refresh
                        </button>
                        <button class="btn btn-primary" onclick="AnalyticsDashboard.loadAIAnalysis()">
                            <i class="fas fa-robot"></i> AI Analysis
                        </button>
                    </div>
                </div>
            </div>

            <!-- AI Analysis Banner -->
            <div id="aiAnalysisBanner" class="hidden mb-6 p-4 bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl">
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 bg-indigo-500 rounded-full flex items-center justify-center text-white flex-shrink-0">
                        <i class="fas fa-brain"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-indigo-900 mb-1">AI Performance Analysis</h4>
                        <p id="aiAnalysisText" class="text-sm text-gray-700"></p>
                    </div>
                </div>
            </div>

            <!-- Health Score & Key Metrics -->
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 sm:gap-6 mb-6 md:mb-8">
                <div class="card lg:col-span-1">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-sm font-bold text-gray-700">Marketing Health</h3>
                        <span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-bold">AI Score</span>
                    </div>
                    <div class="health-score" style="width:150px;height:150px;">
                        <svg viewBox="0 0 200 200" class="health-score-circle">
                            <defs>
                                <linearGradient id="healthGradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" style="stop-color:#6366f1"/>
                                    <stop offset="100%" style="stop-color:#06b6d4"/>
                                </linearGradient>
                            </defs>
                            <circle cx="100" cy="100" r="90" class="health-score-bg"/>
                            <circle cx="100" cy="100" r="90" class="health-score-progress" stroke-dasharray="478" stroke-dashoffset="105" stroke="url(#healthGradient2)"/>
                        </svg>
                        <div class="health-score-text">
                            <div class="health-score-number" id="healthScoreNum" style="font-size:36px;">78</div>
                            <div class="text-xs text-gray-500 font-semibold">Good</div>
                        </div>
                    </div>
                    <div class="mt-4 space-y-2">
                        <div class="flex justify-between text-xs">
                            <span class="text-gray-600">Consistency</span>
                            <span class="font-semibold text-green-600">85%</span>
                        </div>
                        <div class="flex justify-between text-xs">
                            <span class="text-gray-600">Engagement</span>
                            <span class="font-semibold text-green-600">78%</span>
                        </div>
                        <div class="flex justify-between text-xs">
                            <span class="text-gray-600">Growth</span>
                            <span class="font-semibold text-yellow-600">62%</span>
                        </div>
                        <div class="flex justify-between text-xs">
                            <span class="text-gray-600">Content Quality</span>
                            <span class="font-semibold text-green-600">82%</span>
                        </div>
                    </div>
                </div>

                <div class="lg:col-span-3">
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
                        <div class="metric-card">
                            <div class="metric-label">Total Reach</div>
                            <div class="metric-value" id="metricReach">15.2K</div>
                            <div class="metric-change positive"><i class="fas fa-arrow-up"></i><span>+18% from last month</span></div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Engagement Rate</div>
                            <div class="metric-value" id="metricER">5.1%</div>
                            <div class="metric-change positive"><i class="fas fa-arrow-up"></i><span>+0.8% from last month</span></div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">New Followers</div>
                            <div class="metric-value" id="metricFollowers">+412</div>
                            <div class="metric-change positive"><i class="fas fa-arrow-up"></i><span>+25% from last month</span></div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Click-Through Rate</div>
                            <div class="metric-value" id="metricCTR">2.5%</div>
                            <div class="metric-change positive"><i class="fas fa-arrow-up"></i><span>+0.3%</span></div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Email Open Rate</div>
                            <div class="metric-value">26%</div>
                            <div class="metric-change positive"><i class="fas fa-arrow-up"></i><span>+5%</span></div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">SMS CTR</div>
                            <div class="metric-value">14%</div>
                            <div class="metric-change positive"><i class="fas fa-arrow-up"></i><span>+8%</span></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Charts Row -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 md:mb-8">
                <!-- Weekly Reach & Engagement Chart -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-chart-line text-teal-500"></i> Weekly Reach & Engagement</h3>
                    </div>
                    <div style="height:280px; position:relative;">
                        <canvas id="reachEngagementChart"></canvas>
                    </div>
                </div>
                <!-- Content Type Performance Chart -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-chart-pie text-purple-500"></i> Content Type Performance</h3>
                    </div>
                    <div style="height:280px; position:relative;">
                        <canvas id="contentTypeChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Platform Performance Chart + Follower Growth -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 md:mb-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-chart-bar text-blue-500"></i> Platform Engagement Rates</h3>
                    </div>
                    <div style="height:280px; position:relative;">
                        <canvas id="platformChart"></canvas>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-users text-green-500"></i> Follower Growth Trend</h3>
                    </div>
                    <div style="height:280px; position:relative;">
                        <canvas id="followerChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- AI Recommendations -->
            <div class="card mb-6 md:mb-8">
                <div class="card-header">
                    <h3 class="card-title"><i class="fas fa-magic text-purple-500"></i> AI Next-Action Recommendations</h3>
                    <button class="text-sm text-teal-600 font-semibold hover:text-teal-700" onclick="AnalyticsDashboard.loadRecommendations()">
                        <i class="fas fa-sync"></i> Refresh with AI
                    </button>
                </div>
                <div id="aiRecommendations" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div class="p-4 bg-gradient-to-br from-teal-50 to-green-50 border border-teal-200 rounded-xl">
                        <div class="flex items-center gap-2 mb-3">
                            <i class="fas fa-spinner fa-spin text-teal-600 text-lg"></i>
                            <span class="text-xs font-bold text-teal-700">LOADING</span>
                        </div>
                        <h4 class="font-bold text-gray-900 mb-2">Loading AI recommendations...</h4>
                        <p class="text-sm text-gray-600 mb-3">AI is analyzing your data to give personalized advice.</p>
                    </div>
                </div>
            </div>

            <!-- AI Ask Box -->
            <div class="card mb-6 md:mb-8">
                <div class="card-header">
                    <h3 class="card-title"><i class="fas fa-robot text-indigo-500"></i> Ask AI About Your Performance</h3>
                </div>
                <div class="flex gap-3">
                    <input type="text" id="aiAnalyticsQuestion" class="flex-1 px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-teal-500" placeholder="e.g., Why did engagement drop last week? What content should I post next?" onkeypress="if(event.key==='Enter') AnalyticsDashboard.askAI()">
                    <button class="btn btn-primary" onclick="AnalyticsDashboard.askAI()">
                        <i class="fas fa-paper-plane"></i> Ask
                    </button>
                </div>
                <div id="aiAnalyticsAnswer" class="mt-4 hidden">
                    <div class="p-4 bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl">
                        <div class="flex items-center gap-2 mb-2">
                            <i class="fas fa-brain text-indigo-600"></i>
                            <span class="text-xs font-bold text-indigo-700">AI INSIGHT</span>
                        </div>
                        <p id="aiAnalyticsAnswerText" class="text-sm text-gray-700"></p>
                    </div>
                </div>
            </div>

            <!-- Post Comparison with AI analysis -->
            <div class="card mb-6 md:mb-8">
                <div class="card-header">
                    <h3 class="card-title"><i class="fas fa-chart-bar text-blue-500"></i> Post Performance Comparison</h3>
                    <button class="text-sm text-teal-600 font-semibold hover:text-teal-700" onclick="AnalyticsDashboard.loadPostComparison()">
                        <i class="fas fa-robot"></i> AI Compare
                    </button>
                </div>
                <div id="aiPostComparison" class="hidden mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <div class="flex items-center gap-2 mb-1">
                        <i class="fas fa-brain text-blue-600"></i>
                        <span class="text-xs font-bold text-blue-700">AI COMPARISON</span>
                    </div>
                    <p id="aiPostComparisonText" class="text-sm text-gray-700"></p>
                </div>
                <div style="height:260px; position:relative;">
                    <canvas id="postComparisonChart"></canvas>
                </div>
            </div>

            <!-- AI-Powered Suggestions for improvement -->
            <div class="card mb-6 md:mb-8">
                <div class="card-header">
                    <h3 class="card-title"><i class="fas fa-lightbulb text-yellow-500"></i> AI Improvement Suggestions</h3>
                    <button class="text-sm text-teal-600 font-semibold hover:text-teal-700" onclick="AnalyticsDashboard.loadAISuggestions()">
                        <i class="fas fa-sync"></i> Generate
                    </button>
                </div>
                <div id="analyticsAiSuggestions" class="space-y-3">
                    <div class="text-center py-6 text-gray-500">
                        <i class="fas fa-lightbulb text-3xl text-yellow-400 mb-2"></i>
                        <p class="text-sm">Click "Generate" to get AI-powered improvement suggestions</p>
                    </div>
                </div>
            </div>
        </div>
    `,

    inbox: `
        <div class="p-4 sm:p-6 md:p-8 max-w-7xl mx-auto fade-in" id="inboxRoot">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <div>
                    <h1 class="text-2xl sm:text-3xl font-bold" style="color:#e8eaed;">AI Communication Hub</h1>
                    <p class="text-sm mt-1" style="color:#5f6680;">Manage all customer conversations with AI-powered replies</p>
                </div>
                <div class="flex items-center gap-3">
                    <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg" style="background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.15);">
                        <i class="fas fa-envelope text-xs" style="color:#818cf8;"></i>
                        <span class="text-xs font-bold" style="color:#818cf8;" id="inboxUnreadBadge">0 unread</span>
                    </div>
                    <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg" style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.12);">
                        <i class="fas fa-robot text-xs" style="color:#34d399;"></i>
                        <span class="text-xs font-bold" style="color:#34d399;">AI Active</span>
                    </div>
                </div>
            </div>

            <!-- Stats Bar -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6" id="inboxStats">
                <div class="p-3 rounded-xl" style="background:#131825;border:1px solid rgba(255,255,255,.05);">
                    <div class="text-lg font-bold" style="color:#818cf8;" id="statTotal">0</div>
                    <div class="text-[10px]" style="color:#5f6680;">Total Messages</div>
                </div>
                <div class="p-3 rounded-xl" style="background:#131825;border:1px solid rgba(255,255,255,.05);">
                    <div class="text-lg font-bold" style="color:#f59e0b;" id="statUnread">0</div>
                    <div class="text-[10px]" style="color:#5f6680;">Unread</div>
                </div>
                <div class="p-3 rounded-xl" style="background:#131825;border:1px solid rgba(255,255,255,.05);">
                    <div class="text-lg font-bold" style="color:#34d399;" id="statAvgTime">12 min</div>
                    <div class="text-[10px]" style="color:#5f6680;">Avg Response</div>
                </div>
                <div class="p-3 rounded-xl" style="background:#131825;border:1px solid rgba(255,255,255,.05);">
                    <div class="text-lg font-bold" style="color:#06b6d4;" id="statAiReplies">8</div>
                    <div class="text-[10px]" style="color:#5f6680;">AI Replies Today</div>
                </div>
            </div>

            <!-- Filters -->
            <div class="flex flex-wrap items-center gap-2 mb-4">
                <button class="inbox-filter-btn active" data-filter="all" onclick="app.filterInbox('all')">All</button>
                <button class="inbox-filter-btn" data-filter="instagram" onclick="app.filterInbox('instagram')"><i class="fab fa-instagram mr-1"></i>Instagram</button>
                <button class="inbox-filter-btn" data-filter="email" onclick="app.filterInbox('email')"><i class="fas fa-envelope mr-1"></i>Email</button>
                <button class="inbox-filter-btn" data-filter="linkedin" onclick="app.filterInbox('linkedin')"><i class="fab fa-linkedin mr-1"></i>LinkedIn</button>
                <button class="inbox-filter-btn" data-filter="sms" onclick="app.filterInbox('sms')"><i class="fas fa-sms mr-1"></i>SMS</button>
                <button class="inbox-filter-btn" data-filter="twitter" onclick="app.filterInbox('twitter')"><i class="fab fa-twitter mr-1"></i>Twitter</button>
                <div class="flex-1"></div>
                <input type="text" id="inboxSearch" placeholder="Search conversations..." class="px-3 py-1.5 rounded-lg text-xs" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);min-width:180px;" oninput="app.searchInbox(this.value)">
            </div>

            <!-- Main Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
                <!-- Thread List -->
                <div class="lg:col-span-4">
                    <div class="rounded-xl overflow-hidden" style="background:#131825;border:1px solid rgba(255,255,255,.05);">
                        <div id="threadList" class="divide-y" style="border-color:rgba(255,255,255,.04); max-height:65vh; overflow-y:auto;">
                            <div class="p-6 text-center"><i class="fas fa-spinner fa-spin" style="color:#818cf8;"></i><p class="text-xs mt-2" style="color:#5f6680;">Loading conversations...</p></div>
                        </div>
                    </div>
                </div>

                <!-- Conversation Thread -->
                <div class="lg:col-span-5">
                    <div class="rounded-xl flex flex-col" style="background:#131825;border:1px solid rgba(255,255,255,.05); min-height:65vh;" id="conversationPanel">
                        <div class="flex-1 flex items-center justify-center p-8">
                            <div class="text-center">
                                <i class="fas fa-comments text-4xl mb-3" style="color:#1e2538;"></i>
                                <p class="text-sm font-medium" style="color:#5f6680;">Select a conversation</p>
                                <p class="text-xs mt-1" style="color:#3a3f52;">Click any thread on the left to view messages</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- AI Assistant Sidebar -->
                <div class="lg:col-span-3">
                    <div class="rounded-xl p-4 space-y-4" style="background:#131825;border:1px solid rgba(255,255,255,.05);" id="aiAssistPanel">
                        <div class="flex items-center gap-2 mb-1">
                            <div class="w-7 h-7 rounded-lg flex items-center justify-center" style="background:linear-gradient(135deg,#8b5cf6,#6366f1);">
                                <i class="fas fa-robot text-white text-xs"></i>
                            </div>
                            <span class="text-sm font-bold" style="color:#e8eaed;">AI Assistant</span>
                        </div>
                        <div class="p-3 rounded-lg" style="background:rgba(139,92,246,.06);border:1px solid rgba(139,92,246,.1);">
                            <p class="text-xs" style="color:#9aa0b0;"><i class="fas fa-info-circle mr-1" style="color:#a78bfa;"></i>Select a conversation to get AI-powered reply suggestions, sentiment analysis, and smart actions.</p>
                        </div>
                        <div id="aiSuggestions"></div>
                        <div class="p-3 rounded-lg" style="background:rgba(6,182,212,.05);border:1px solid rgba(6,182,212,.1);">
                            <div class="text-[10px] font-bold mb-2" style="color:#22d3ee;">QUICK ACTIONS</div>
                            <div class="space-y-1.5">
                                <button class="w-full text-left flex items-center gap-2 px-2 py-1.5 rounded text-xs transition" style="color:#c4c8d4;" onmouseover="this.style.background='rgba(255,255,255,.03)'" onmouseout="this.style.background='transparent'" onclick="app.loadView('content')"><i class="fas fa-pen-fancy text-[10px]" style="color:#818cf8;"></i>Create Content</button>
                                <button class="w-full text-left flex items-center gap-2 px-2 py-1.5 rounded text-xs transition" style="color:#c4c8d4;" onmouseover="this.style.background='rgba(255,255,255,.03)'" onmouseout="this.style.background='transparent'" onclick="app.loadView('strategy')"><i class="fas fa-lightbulb text-[10px]" style="color:#f59e0b;"></i>New Strategy</button>
                                <button class="w-full text-left flex items-center gap-2 px-2 py-1.5 rounded text-xs transition" style="color:#c4c8d4;" onmouseover="this.style.background='rgba(255,255,255,.03)'" onmouseout="this.style.background='transparent'" onclick="app.loadView('analytics')"><i class="fas fa-chart-bar text-[10px]" style="color:#34d399;"></i>View Analytics</button>
                                <button class="w-full text-left flex items-center gap-2 px-2 py-1.5 rounded text-xs transition" style="color:#c4c8d4;" onmouseover="this.style.background='rgba(255,255,255,.03)'" onmouseout="this.style.background='transparent'" onclick="app.loadView('calendar')"><i class="fas fa-calendar text-[10px]" style="color:#ec4899;"></i>Content Calendar</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,

    settings: `
        <div class="p-4 sm:p-6 md:p-8 max-w-4xl mx-auto fade-in">
            <div class="mb-6 md:mb-8">
                <h1 class="text-2xl sm:text-3xl font-bold mb-2" style="color:#e8eaed;">Settings</h1>
                <p class="text-sm sm:text-base" style="color:#9aa0b0;">Manage your account and business profile</p>
            </div>

            <div class="space-y-4 sm:space-y-6">
                <!-- User Profile Card -->
                <div class="rounded-xl p-6" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                    <div class="flex items-center gap-3 mb-4" style="border-bottom:1px solid rgba(255,255,255,0.06); padding-bottom:12px;">
                        <i class="fas fa-user" style="color:#818cf8;"></i>
                        <h3 class="font-semibold text-lg" style="color:#e8eaed;">Your Profile</h3>
                        <span id="settingsProviderBadge" class="ml-auto text-xs px-2 py-1 rounded-full" style="background:rgba(99,102,241,0.15); color:#818cf8;"></span>
                    </div>
                    <div class="flex items-center gap-4 mb-6">
                        <div id="settingsAvatar" class="w-16 h-16 rounded-full flex items-center justify-center text-white text-xl font-semibold flex-shrink-0" style="background:linear-gradient(135deg, #8b5cf6, #ec4899);"></div>
                        <div>
                            <p id="settingsDisplayName" class="font-semibold text-lg" style="color:#e8eaed;"></p>
                            <p id="settingsDisplayEmail" class="text-sm" style="color:#9aa0b0;"></p>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-semibold mb-2" style="color:#e8eaed;">First Name</label>
                            <input type="text" id="profileFirstName" class="w-full px-4 py-3 rounded-lg text-sm" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.1); color:#e8eaed;">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold mb-2" style="color:#e8eaed;">Last Name</label>
                            <input type="text" id="profileLastName" class="w-full px-4 py-3 rounded-lg text-sm" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.1); color:#e8eaed;">
                        </div>
                        <div class="sm:col-span-2">
                            <label class="block text-sm font-semibold mb-2" style="color:#e8eaed;">Email</label>
                            <input type="email" id="profileEmail" class="w-full px-4 py-3 rounded-lg text-sm" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.1); color:#9aa0b0;" readonly>
                        </div>
                    </div>
                </div>

                <!-- Business Profile Card -->
                <div class="rounded-xl p-6" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                    <div class="flex items-center gap-3 mb-4" style="border-bottom:1px solid rgba(255,255,255,0.06); padding-bottom:12px;">
                        <i class="fas fa-briefcase" style="color:#34d399;"></i>
                        <h3 class="font-semibold text-lg" style="color:#e8eaed;">Business Profile</h3>
                    </div>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-semibold mb-2" style="color:#e8eaed;">Business Name</label>
                            <input type="text" id="bizName" class="w-full px-4 py-3 rounded-lg text-sm" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.1); color:#e8eaed;">
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-semibold mb-2" style="color:#e8eaed;">Industry</label>
                                <select id="bizIndustry" class="w-full px-4 py-3 rounded-lg text-sm" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.1); color:#e8eaed;">
                                    <option value="Technology">Technology / SaaS</option>
                                    <option value="E-commerce">E-commerce</option>
                                    <option value="Healthcare">Healthcare</option>
                                    <option value="Education">Education</option>
                                    <option value="Finance">Finance</option>
                                    <option value="Real Estate">Real Estate</option>
                                    <option value="Food & Beverage">Food & Beverage</option>
                                    <option value="Consulting">Consulting</option>
                                    <option value="Marketing">Marketing Agency</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm font-semibold mb-2" style="color:#e8eaed;">Brand Voice</label>
                                <select id="bizVoice" class="w-full px-4 py-3 rounded-lg text-sm" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.1); color:#e8eaed;">
                                    <option value="Professional">Professional</option>
                                    <option value="Casual">Casual & Friendly</option>
                                    <option value="Bold">Bold & Direct</option>
                                    <option value="Inspirational">Inspirational</option>
                                    <option value="Humorous">Humorous</option>
                                    <option value="Technical">Technical / Expert</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold mb-2" style="color:#e8eaed;">Target Audience</label>
                            <input type="text" id="bizAudience" placeholder="e.g. B2B founders, Tech professionals 25-45" class="w-full px-4 py-3 rounded-lg text-sm" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.1); color:#e8eaed;">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold mb-2" style="color:#e8eaed;">Primary Goals</label>
                            <div id="bizGoals" class="flex flex-wrap gap-2">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Connected Platforms -->
                <div class="rounded-xl p-6" style="background:#131825; border:1px solid rgba(255,255,255,0.06);">
                    <div class="flex items-center gap-3 mb-4" style="border-bottom:1px solid rgba(255,255,255,0.06); padding-bottom:12px;">
                        <i class="fas fa-plug" style="color:#f59e0b;"></i>
                        <h3 class="font-semibold text-lg" style="color:#e8eaed;">Connected Platforms</h3>
                    </div>
                    <div class="space-y-3">
                        <div class="flex items-center justify-between p-4 rounded-lg" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.06);">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-lg flex items-center justify-center text-white" style="background:#E4405F;"><i class="fab fa-instagram"></i></div>
                                <div><p class="font-semibold text-sm" style="color:#e8eaed;">Instagram</p><p class="text-xs" style="color:#5f6680;">Not connected</p></div>
                            </div>
                            <button class="px-3 py-1.5 rounded-lg text-xs font-semibold" style="background:rgba(99,102,241,0.15); color:#818cf8;">Connect</button>
                        </div>
                        <div class="flex items-center justify-between p-4 rounded-lg" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.06);">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-lg flex items-center justify-center text-white" style="background:#0A66C2;"><i class="fab fa-linkedin"></i></div>
                                <div><p class="font-semibold text-sm" style="color:#e8eaed;">LinkedIn</p><p class="text-xs" style="color:#5f6680;">Not connected</p></div>
                            </div>
                            <button class="px-3 py-1.5 rounded-lg text-xs font-semibold" style="background:rgba(99,102,241,0.15); color:#818cf8;">Connect</button>
                        </div>
                        <div class="flex items-center justify-between p-4 rounded-lg" style="background:#0a0e17; border:1px solid rgba(255,255,255,0.06);">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-lg flex items-center justify-center text-white" style="background:#25D366;"><i class="fab fa-whatsapp"></i></div>
                                <div><p class="font-semibold text-sm" style="color:#e8eaed;">WhatsApp Business</p><p class="text-xs" style="color:#5f6680;">Not connected</p></div>
                            </div>
                            <button class="px-3 py-1.5 rounded-lg text-xs font-semibold" style="background:rgba(99,102,241,0.15); color:#818cf8;">Connect</button>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex justify-between items-center">
                    <button class="px-4 py-2.5 rounded-lg text-sm font-semibold transition" style="background:rgba(239,68,68,0.1); color:#f87171; border:1px solid rgba(239,68,68,0.2);" onclick="app.signOut()">
                        <i class="fas fa-sign-out-alt mr-2"></i>Sign Out
                    </button>
                    <div class="flex gap-3">
                        <button class="px-4 py-2.5 rounded-lg text-sm font-semibold" style="background:rgba(255,255,255,0.06); color:#e8eaed;" onclick="app.showTechArchitecture()">
                            <i class="fas fa-microchip mr-2"></i>Architecture
                        </button>
                        <button class="px-5 py-2.5 rounded-lg text-sm font-semibold text-white" style="background:linear-gradient(135deg, #6366f1, #8b5cf6);" onclick="app.saveProfileSettings()">
                            <i class="fas fa-save mr-2"></i>Save Changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `
};

// Application State & Logic
const app = {
    currentView: 'home',
    wizardStep: 1,
    isMobileMenuOpen: false,
    get isDemoMode() {
        // Auto-detect: demo mode only when logged in with demo provider
        if (window.auth && window.auth.isAuthenticated()) {
            var u = window.auth.getCurrentUser();
            return u && u.provider === 'demo';
        }
        return false;
    },
    user: null,
    businessProfile: null,
    
    // Make views accessible
    get views() {
        return views;
    },

    init() {
        console.log('App initializing...');
        console.log('Available views:', Object.keys(this.views));

        // Restore last campaign from localStorage
        try {
            const stored = JSON.parse(localStorage.getItem('campaigns') || '[]');
            if (stored.length) this.currentCampaign = stored[stored.length - 1];
        } catch(e) { /* ignore */ }
        
        // Initialize AI prompt engine if available
        if (window.aiPromptEngine) {
            console.log('AI Prompt Engine initialized');
        } else {
            console.log('AI Prompt Engine not available - using fallback');
        }
        
        // Initialize infrastructure if available
        if (window.infrastructure) {
            console.log('Infrastructure initialized');
        } else {
            console.log('Infrastructure not available - using fallback');
        }
        
        // Initialize with smooth loading
        this.showLoading();
        
        // Load initial data
        this.loadInitialData().then(() => {
            this.loadView('home');
            this.setupEventListeners();
            this.setupResponsive();
            this.hideLoading();
            console.log('App initialization complete');
        }).catch(error => {
            console.error('Failed to load initial data:', error);
            this.hideLoading();
            this.showToast('Failed to load some features', 'error');
        });
    },

    async loadInitialData() {
        try {
            // Load user profile if authenticated
            if (auth.isAuthenticated()) {
                await this.loadUserProfile();
                await this.loadBusinessProfile();
                await this.loadRecentCampaigns();
                await this.loadRecentActivity();
            }
        } catch (error) {
            console.error('Error loading initial data:', error);
            // Continue with demo data if API fails
        }
    },

    async loadUserProfile() {
        try {
            // 1. Try real user from auth (Google/LinkedIn/Email login)
            if (window.auth && window.auth.isAuthenticated() && window.auth.getUserProfile()) {
                const authUser = window.auth.getUserProfile();
                this.user = {
                    id: authUser.id || authUser.email,
                    email: authUser.email || '',
                    name: authUser.name || authUser.firstName || 'User',
                    full_name: authUser.name || ((authUser.firstName || '') + ' ' + (authUser.lastName || '')).trim() || 'User',
                    firstName: authUser.firstName || (authUser.name ? authUser.name.split(' ')[0] : 'User'),
                    lastName: authUser.lastName || (authUser.name ? authUser.name.split(' ').slice(1).join(' ') : ''),
                    picture: authUser.picture || '',
                    provider: authUser.provider || 'unknown',
                    role: 'admin',
                    is_active: true,
                    created_at: authUser.createdAt || new Date().toISOString(),
                    updated_at: authUser.lastLogin || new Date().toISOString()
                };
                this.updateUserProfileUI();
                console.log('Using real user profile:', this.user.email, '(provider:', this.user.provider + ')');
                return;
            }

            // 2. Fallback demo data only if truly not authenticated
            this.user = {
                id: 'demo_user_1',
                email: 'demo@aimarketing.ai',
                name: 'Demo User',
                full_name: 'Demo User',
                firstName: 'Demo',
                lastName: 'User',
                picture: '',
                provider: 'demo',
                role: 'admin',
                is_active: true,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString()
            };
            this.updateUserProfileUI();
            console.log('Using demo user profile');
        } catch (error) {
            console.error('Failed to load user profile:', error);
        }
    },

    async loadBusinessProfile() {
        try {
            // 1. Try stored business profile from OAuth login
            if (window.auth && window.auth.getBusinessProfile()) {
                const biz = window.auth.getBusinessProfile();
                this.businessProfile = {
                    id: biz.id || '',
                    business_name: biz.name || biz.business_name || (this.user ? this.user.firstName + "'s Business" : 'My Business'),
                    industry: biz.industry || 'Technology',
                    brand_voice: biz.brand_voice || 'Professional',
                    primary_goals: biz.primary_goals || ['Brand Awareness'],
                    target_audience: biz.target_audience || [{ segment_name: 'General', age_range: '25-45', interests: ['Technology'] }],
                    plan: biz.plan || 'free'
                };
                console.log('Using stored business profile:', this.businessProfile.business_name);
                return;
            }

            // 2. Try loading from localStorage directly
            try {
                const stored = JSON.parse(localStorage.getItem('business_profile') || 'null');
                if (stored) {
                    this.businessProfile = {
                        id: stored.id || '',
                        business_name: stored.name || stored.business_name || 'My Business',
                        industry: stored.industry || 'Technology',
                        brand_voice: stored.brand_voice || 'Professional',
                        primary_goals: stored.primary_goals || ['Brand Awareness'],
                        target_audience: stored.target_audience || [],
                        plan: stored.plan || 'free'
                    };
                    return;
                }
            } catch(e) {}

            // 3. Default for new users
            const firstName = this.user ? this.user.firstName : 'My';
            this.businessProfile = {
                business_name: firstName + "'s Business",
                industry: 'Technology',
                brand_voice: 'Professional',
                primary_goals: ['Brand Awareness'],
                target_audience: [{ segment_name: 'General', age_range: '25-45', interests: ['Technology'] }]
            };
        } catch (error) {
            console.error('Failed to load business profile:', error);
            this.businessProfile = { business_name: 'My Business', industry: 'Technology', brand_voice: 'Professional', primary_goals: ['Brand Awareness'], target_audience: [] };
        }
    },

    async loadRecentCampaigns() {
        try {
            // For demo, we'll use mock data
            this.campaigns = [
                {
                    _id: "1",
                    name: "Q1 Product Launch",
                    goal: "Generate 500 qualified leads",
                    status: "active",
                    start_date: new Date().toISOString(),
                    end_date: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString()
                },
                {
                    _id: "2",
                    name: "Brand Awareness Campaign",
                    goal: "Increase social media presence",
                    status: "draft",
                    start_date: new Date().toISOString(),
                    end_date: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000).toISOString()
                }
            ];
        } catch (error) {
            console.error('Failed to load campaigns:', error);
        }
    },

    async loadRecentActivity() {
        try {
            // For demo, we'll use mock data
            this.recentActivity = [
                {
                    type: 'campaign_completed',
                    title: 'Product Launch Campaign',
                    description: 'Campaign finished with 15 posts published',
                    timestamp: '2 hours ago',
                    icon: 'fa-check',
                    color: 'green'
                },
                {
                    type: 'report_generated',
                    title: 'Weekly Analytics Report',
                    description: 'Shows 23% engagement increase',
                    timestamp: '5 hours ago',
                    icon: 'fa-chart-line',
                    color: 'blue'
                },
                {
                    type: 'content_created',
                    title: 'AI Content Generated',
                    description: '12 new posts ready for review',
                    timestamp: '1 day ago',
                    icon: 'fa-magic',
                    color: 'purple'
                }
            ];
        } catch (error) {
            console.error('Failed to load activity:', error);
        }
    },

    updateUserProfileUI() {
        if (!this.user) return;

        const displayName = this.user.name || this.user.full_name || this.user.email || 'User';
        const firstName = displayName.split(' ')[0];
        const email = this.user.email || '';
        const picture = this.user.picture || '';
        const initials = displayName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();

        // Update user info in navigation
        const userName = document.getElementById('userName');
        if (userName) {
            userName.textContent = displayName;
        }

        // Update sidebar user section
        const sidebarAvatar = document.getElementById('sidebarAvatar');
        const sidebarName = document.getElementById('sidebarName');
        const sidebarEmail = document.getElementById('sidebarEmail');

        if (sidebarAvatar) {
            if (picture) {
                sidebarAvatar.innerHTML = `<img src="${picture}" alt="${firstName}" class="w-10 h-10 rounded-full object-cover">`;
            } else {
                sidebarAvatar.textContent = initials;
            }
        }
        if (sidebarName) sidebarName.textContent = displayName;
        if (sidebarEmail) sidebarEmail.textContent = email;

        // Update greeting in home view
        const greetingElement = document.querySelector('.text-4xl');
        if (greetingElement) {
            greetingElement.textContent = `Welcome back, ${firstName}!`;
        }

        // Update demo mode indicator
        const demoIndicator = document.querySelector('[data-demo-indicator]');
        if (demoIndicator) {
            if (this.isDemoMode) {
                demoIndicator.classList.remove('hidden');
            } else {
                demoIndicator.classList.add('hidden');
            }
        }
    },

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const view = e.currentTarget.getAttribute('data-view');
                this.loadView(view);
                // Close mobile menu after navigation
                if (window.innerWidth < 1024) {
                    this.closeMobileMenu();
                }
            });
        });

        // Mobile Menu Toggle
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');
        const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
        
        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }
        
        if (mobileMenuOverlay) {
            mobileMenuOverlay.addEventListener('click', () => {
                this.closeMobileMenu();
            });
        }

        // Command Palette
        document.getElementById('searchBtn').addEventListener('click', () => {
            this.toggleCommandPalette();
        });

        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                this.toggleCommandPalette();
            }
            if (e.key === 'Escape') {
                document.getElementById('commandPalette').classList.add('hidden');
                this.closeMobileMenu();
            }
        });

        // Command Items
        document.querySelectorAll('.command-item').forEach(item => {
            item.addEventListener('click', () => {
                const action = item.getAttribute('data-action');
                this.handleCommand(action);
            });
        });

        // Tone options
        document.addEventListener('click', (e) => {
            if (e.target.closest('.tone-option')) {
                document.querySelectorAll('.tone-option').forEach(opt => opt.classList.remove('active'));
                e.target.closest('.tone-option').classList.add('active');
            }
        });

        // Duration options
        document.addEventListener('click', (e) => {
            if (e.target.closest('.duration-option')) {
                document.querySelectorAll('.duration-option').forEach(opt => opt.classList.remove('active'));
                e.target.closest('.duration-option').classList.add('active');
            }
        });

        // Setup content studio event listeners with delegation
        this.setupContentStudioListeners();
    },

    setupContentStudioListeners() {
        // Use event delegation for dynamically loaded content
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('button');
            if (!btn) return;

            const btnText = btn.textContent.trim();
            const btnIcon = btn.querySelector('i')?.className || '';

            // Create New Content button
            if (btnText.includes('Create New Content') || btnIcon.includes('fa-plus')) {
                if (this.currentView === 'content') {
                    this.createNewContent();
                }
            }

            // Import Media button
            if (btnText.includes('Import Media') || btnIcon.includes('fa-upload')) {
                if (this.currentView === 'content') {
                    this.importMedia();
                }
            }

            // Save Draft button
            if (btnText.includes('Save Draft') || btnIcon.includes('fa-save')) {
                if (this.currentView === 'content') {
                    this.saveDraft();
                }
            }

            // Regenerate button
            if (btnText.includes('Regenerate') && btnIcon.includes('fa-sync')) {
                if (this.currentView === 'content') {
                    this.regenerateContent();
                }
            }

            // Schedule button
            if (btnText.includes('Schedule') && btnIcon.includes('fa-paper-plane')) {
                if (this.currentView === 'content') {
                    this.scheduleContent();
                }
            }

            // Optimize hashtags
            if (btnText.includes('Optimize hashtags') || btnText.includes('Optimize script')) {
                if (this.currentView === 'content') {
                    this.optimizeHashtags();
                }
            }

            // AI Content Assistant buttons
            if (btnText.includes('Generate Optimized Version')) {
                if (this.currentView === 'content') {
                    this.generateContentFromAI();
                }
            }
        });

        // Platform tab switching
        document.addEventListener('click', (e) => {
            const tab = e.target.closest('.tab[data-platform]');
            if (tab && this.currentView === 'content') {
                const platform = tab.dataset.platform;
                this.switchPlatform(platform);
            }
        });

        // Content type switching
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.flex.gap-2.p-1.bg-gray-100 button');
            if (btn && this.currentView === 'content') {
                const contentType = btn.textContent.trim().toLowerCase();
                this.switchContentType(contentType);
            }
        });
    },

    setupResponsive() {
        // Handle window resize
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                // Close mobile menu on desktop
                if (window.innerWidth >= 1024) {
                    this.closeMobileMenu();
                }
            }, 250);
        });
    },

    toggleMobileMenu() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('mobileMenuOverlay');
        
        this.isMobileMenuOpen = !this.isMobileMenuOpen;
        
        if (this.isMobileMenuOpen) {
            sidebar.classList.add('mobile-open');
            overlay.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        } else {
            this.closeMobileMenu();
        }
    },

    closeMobileMenu() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('mobileMenuOverlay');
        
        this.isMobileMenuOpen = false;
        sidebar.classList.remove('mobile-open');
        overlay.classList.add('hidden');
        document.body.style.overflow = '';
    },

    toggleCommandPalette() {
        const palette = document.getElementById('commandPalette');
        palette.classList.toggle('hidden');
        if (!palette.classList.contains('hidden')) {
            document.getElementById('commandInput').focus();
        }
    },

    handleCommand(action) {
        document.getElementById('commandPalette').classList.add('hidden');
        switch(action) {
            case 'new-campaign':
                this.loadView('strategy');
                break;
            case 'generate-post':
                this.loadView('content');
                break;
            case 'view-analytics':
                this.loadView('analytics');
                break;
            case 'open-inbox':
                this.loadView('inbox');
                break;
            case 'view-dashboard':
                this.loadView('dashboard');
                break;
        }
    },

    // Real-time Notifications System
    initNotifications() {
        // Create notification container
        const notificationContainer = document.createElement('div');
        notificationContainer.id = 'notificationContainer';
        notificationContainer.className = 'fixed top-4 right-4 z-50 space-y-2';
        document.body.appendChild(notificationContainer);

        // Sample notifications
        this.showNotification('New message from Sarah Kim', 'message');
        this.showNotification('Campaign performance up 23%', 'success');
        this.showNotification('3 posts scheduled for today', 'info');
    },

    showNotification(message, type = 'info') {
        const container = document.getElementById('notificationContainer');
        if (!container) return;

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icons = {
            message: 'fas fa-envelope',
            success: 'fas fa-check-circle',
            warning: 'fas fa-exclamation-triangle',
            error: 'fas fa-times-circle',
            info: 'fas fa-info-circle'
        };

        const colors = {
            message: 'bg-blue-500',
            success: 'bg-green-500',
            warning: 'bg-yellow-500',
            error: 'bg-red-500',
            info: 'bg-gray-500'
        };

        notification.innerHTML = `
            <div class="flex items-center gap-3 p-4 bg-white rounded-lg shadow-lg border border-gray-200 min-w-80">
                <div class="w-10 h-10 ${colors[type]} rounded-full flex items-center justify-center text-white">
                    <i class="${icons[type]}"></i>
                </div>
                <div class="flex-1">
                    <p class="text-sm font-semibold text-gray-900">${message}</p>
                    <p class="text-xs text-gray-500">Just now</p>
                </div>
                <button class="text-gray-400 hover:text-gray-600">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        container.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);

        // Manual close
        notification.querySelector('button').addEventListener('click', () => {
            notification.remove();
        });
    },

    // Task Management System
    initTaskSystem() {
        // Create task panel
        const taskPanel = document.createElement('div');
        taskPanel.id = 'taskPanel';
        taskPanel.className = 'fixed bottom-4 right-4 bg-white rounded-lg shadow-xl border border-gray-200 p-4 w-80 z-40';
        taskPanel.innerHTML = `
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-sm font-bold text-gray-900">Today's Tasks</h3>
                <button class="text-gray-400 hover:text-gray-600">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="space-y-3">
                <div class="task-item">
                    <div class="flex items-center gap-3">
                        <input type="checkbox" class="w-4 h-4 text-teal-600">
                        <div class="flex-1">
                            <p class="text-sm font-medium text-gray-900">Review 3 pending posts</p>
                            <p class="text-xs text-gray-500">Due in 2 hours</p>
                        </div>
                        <span class="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded">Pending</span>
                    </div>
                </div>
                <div class="task-item">
                    <div class="flex items-center gap-3">
                        <input type="checkbox" class="w-4 h-4 text-teal-600">
                        <div class="flex-1">
                            <p class="text-sm font-medium text-gray-900">Schedule Instagram posts</p>
                            <p class="text-xs text-gray-500">Due today</p>
                        </div>
                        <span class="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">Urgent</span>
                    </div>
                </div>
                <div class="task-item">
                    <div class="flex items-center gap-3">
                        <input type="checkbox" class="w-4 h-4 text-teal-600" checked>
                        <div class="flex-1">
                            <p class="text-sm font-medium text-gray-900 line-through">Generate weekly report</p>
                            <p class="text-xs text-gray-500">Completed</p>
                        </div>
                        <span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">Done</span>
                    </div>
                </div>
            </div>
            <div class="mt-4 pt-4 border-t border-gray-200">
                <button class="w-full btn btn-secondary text-sm">
                    <i class="fas fa-plus"></i> Add Task
                </button>
            </div>
        `;

        document.body.appendChild(taskPanel);

        // Toggle panel
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'taskToggle';
        toggleBtn.className = 'fixed bottom-4 right-4 bg-teal-500 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg z-30';
        toggleBtn.innerHTML = '<i class="fas fa-tasks"></i>';
        document.body.appendChild(toggleBtn);

        toggleBtn.addEventListener('click', () => {
            taskPanel.classList.toggle('hidden');
        });

        taskPanel.querySelector('button').addEventListener('click', () => {
            taskPanel.classList.add('hidden');
        });
    },

    // Marketing Health Score Visualization
    initHealthScore() {
        const healthScoreElement = document.querySelector('.health-score');
        if (!healthScoreElement) return;

        // Animate health score
        let currentScore = 0;
        const targetScore = 75;
        const increment = targetScore / 50;

        const animateScore = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(animateScore);
            }
            
            const scoreNumber = healthScoreElement.querySelector('.health-score-number');
            if (scoreNumber) {
                scoreNumber.textContent = Math.round(currentScore);
            }
        }, 30);

        // Interactive health score
        healthScoreElement.addEventListener('click', () => {
            this.showHealthScoreDetails();
        });
    },

    showHealthScoreDetails() {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold text-gray-900">Marketing Health Score</h3>
                    <button class="text-gray-400 hover:text-gray-600">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <span class="text-gray-600">Overall Score</span>
                        <span class="text-2xl font-bold text-green-600">75/100</span>
                    </div>
                    <div class="space-y-3">
                        <div>
                            <div class="flex justify-between text-sm mb-1">
                                <span>Consistency</span>
                                <span class="font-semibold text-green-600">85%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-green-500 h-2 rounded-full" style="width: 85%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between text-sm mb-1">
                                <span>Engagement</span>
                                <span class="font-semibold text-green-600">78%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-green-500 h-2 rounded-full" style="width: 78%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between text-sm mb-1">
                                <span>Growth</span>
                                <span class="font-semibold text-yellow-600">62%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-yellow-500 h-2 rounded-full" style="width: 62%"></div>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between text-sm mb-1">
                                <span>Content Quality</span>
                                <span class="font-semibold text-green-600">82%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-green-500 h-2 rounded-full" style="width: 82%"></div>
                            </div>
                        </div>
                    </div>
                    <div class="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <p class="text-sm text-blue-700">
                            <strong>Recommendation:</strong> Focus on growth metrics to improve overall score.
                        </p>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.closest('button')) {
                modal.remove();
            }
        });
    },

    async approveStrategy() {
        // approveStrategy is called from step 4 to finalize
        try {
            // Save campaign from current strategy
            const stratData = this.getStrategyData();
            const campaign = {
                _id: 'camp_' + Date.now(),
                name: (this.currentStrategy && this.currentStrategy.campaign_name) || stratData.businessName + ' Campaign',
                industry: stratData.industry,
                platforms: stratData.platforms,
                duration: stratData.duration,
                startDate: new Date().toISOString(),
                strategy: this.currentStrategy || {},
                status: 'active',
                createdAt: new Date().toISOString()
            };
            this.currentCampaign = campaign;

            // Also save this.currentStrategy approval date for calendar
            if (this.currentStrategy) {
                this.currentStrategy._approvedDate = new Date().toISOString();
            }

            // Persist in localStorage
            const campaigns = JSON.parse(localStorage.getItem('campaigns') || '[]');
            campaigns.push(campaign);
            localStorage.setItem('campaigns', JSON.stringify(campaigns));
            localStorage.setItem('activeCampaign', JSON.stringify(campaign));

            // Also persist to backend (fire and forget — don't block on failure)
            const baseUrl = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || 'http://localhost:8000';
            fetch(`${baseUrl}/api/v1/campaigns`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: campaign.name,
                    business_id: 'demo',
                    platforms: campaign.platforms,
                    duration_days: parseInt(campaign.duration) || 30,
                    strategy: campaign.strategy,
                    status: 'active',
                })
            }).catch(e => console.warn('Backend campaign save skipped:', e));

            this.showToast('Strategy approved! Campaign created. Redirecting to content creation...', 'success');
            setTimeout(() => this.loadView('content'), 1500);
        } catch (error) {
            console.error('Error approving strategy:', error);
            this.showToast('Failed to approve strategy');
        }
    },

    async generateCampaignStrategy() {
        try {
            // Get strategy data from wizard (prefer cached data if form fields empty)
            let strategyData = this.getStrategyData();
            
            // If form fields return defaults, use lastStrategyData from previous generation
            if (strategyData.businessName === 'My Business' && this._lastStrategyData) {
                strategyData = this._lastStrategyData;
            }
            
            // Validate required fields
            if (!strategyData.businessName || strategyData.businessName === '' || strategyData.businessName === 'My Business') {
                this.showToast('Please enter your business name');
                this.showStep(1);
                return;
            }

            // Cache for regenerate
            this._lastStrategyData = { ...strategyData };
            
            // Show step 3 (generating animation)
            this.showStep(3);
            
            // Animate progress indicators
            const progressSteps = ['progress1', 'progress2', 'progress3', 'progress4'];
            for (let i = 0; i < progressSteps.length; i++) {
                await new Promise(r => setTimeout(r, 800));
                const el = document.getElementById(progressSteps[i]);
                if (el) {
                    el.style.opacity = '1';
                    const icon = el.querySelector('i');
                    const span = el.querySelector('span');
                    if (icon) { icon.className = 'fas fa-spinner fa-spin'; icon.style.color = '#818cf8'; }
                    if (span) { span.style.color = '#e8eaed'; span.style.fontWeight = '500'; }
                    if (i > 0) {
                        const prev = document.getElementById(progressSteps[i - 1]);
                        if (prev) {
                            const prevIcon = prev.querySelector('i');
                            if (prevIcon) { prevIcon.className = 'fas fa-check-circle'; prevIcon.style.color = '#10b981'; }
                        }
                    }
                }
            }

            const baseUrl = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || 'http://localhost:8000';
            
            // Try the agent endpoint first (most reliable)
            let strategy = null;
            try {
                const response = await fetch(`${baseUrl}/api/v1/agent/generate-strategy`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        business_name: strategyData.businessName,
                        industry: strategyData.industry || 'technology',
                        target_audience: strategyData.targetAudience || 'General audience',
                        brand_voice: strategyData.brandVoice || 'professional',
                        campaign_goal: strategyData.goal || 'Increase brand awareness',
                        duration_days: parseInt(strategyData.duration) || 30,
                        platforms: strategyData.platforms.length > 0 ? strategyData.platforms : ['instagram', 'linkedin'],
                        budget: strategyData.budget || null,
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    strategy = (data.data && data.data.strategy) || data.strategy || data.data;
                }
            } catch (e) {
                console.warn('Agent strategy endpoint failed, trying campaign endpoint:', e);
            }

            // Fallback to campaign endpoint
            if (!strategy) {
                try {
                    const response2 = await fetch(`${baseUrl}/api/v1/campaign/generate-strategy`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            business_name: strategyData.businessName,
                            industry: strategyData.industry || 'technology',
                            target_audience: strategyData.targetAudience || 'General audience',
                            brand_voice: strategyData.brandVoice || 'professional',
                            campaign_goal: strategyData.goal || 'Increase brand awareness',
                            duration_days: parseInt(strategyData.duration) || 30,
                            platforms: strategyData.platforms.length > 0 ? strategyData.platforms : ['instagram', 'linkedin'],
                            budget: strategyData.budget || null,
                        })
                    });
                    if (response2.ok) {
                        const data2 = await response2.json();
                        strategy = (data2.data && data2.data.strategy) || data2.strategy || data2.data;
                    }
                } catch (e2) {
                    console.warn('Campaign strategy endpoint also failed:', e2);
                }
            }
            
            // If both endpoints failed, generate a smart local fallback
            if (!strategy) {
                console.warn('Both API endpoints failed — generating local fallback strategy');
                strategy = this._generateFallbackStrategy(strategyData);
            }

            // Mark last progress step as complete
            const lastProgress = document.getElementById('progress4');
            if (lastProgress) {
                const lastIcon = lastProgress.querySelector('i');
                if (lastIcon) { lastIcon.className = 'fas fa-check-circle'; lastIcon.style.color = '#10b981'; }
            }
            
            await new Promise(r => setTimeout(r, 600));
            
            // Store the strategy
            this.currentStrategy = strategy;
            
            // Render Step 4 dynamically
            this.renderStrategyReview(strategy, strategyData);
            
            // Show step 4
            this.showStep(4);
            this.showToast(strategy._isFallback ? 'Offline strategy generated (AI unavailable)' : 'Campaign strategy generated successfully!', strategy._isFallback ? 'warning' : 'success');
            
        } catch (error) {
            console.error('Error generating strategy:', error);
            // Even on total error, try the fallback
            try {
                const fallback = this._generateFallbackStrategy(this._lastStrategyData || {});
                this.currentStrategy = fallback;
                this.renderStrategyReview(fallback, this._lastStrategyData || {});
                this.showStep(4);
                this.showToast('Offline strategy generated (AI unavailable)', 'warning');
            } catch (e2) {
                this.showStep(2);
                this.showToast('Strategy generation failed. Please try again.');
            }
        }
    },

    _generateFallbackStrategy(formData) {
        const biz = formData.businessName || 'Your Business';
        const ind = formData.industry || 'technology';
        const goal = formData.goal || 'awareness';
        const dur = parseInt(formData.duration) || 30;
        const plats = (formData.platforms && formData.platforms.length > 0) ? formData.platforms : ['instagram', 'linkedin'];
        const voice = formData.brandVoice || 'professional';
        const weeks = Math.ceil(dur / 7);

        const goalThemes = {
            awareness: ['Brand Story Launch', 'Community Building', 'Value Showcase', 'Thought Leadership', 'Viral Moments'],
            engagement: ['Conversation Starters', 'Interactive Content', 'User Spotlights', 'Behind-the-Scenes', 'Engagement Challenges'],
            leads: ['Problem-Solution', 'Social Proof', 'Lead Magnets', 'Case Studies', 'Conversion Push'],
            sales: ['Product Highlights', 'Customer Success', 'Limited Offers', 'Trust Building', 'Launch Event'],
        };
        const themes = goalThemes[goal] || goalThemes.awareness;

        // Content templates per goal per day-of-week
        const dailyTemplates = {
            awareness: [
                { title: 'Brand Story Post', type: 'carousel', tips: 'Use storytelling to humanize the brand', best_time: '10:00 AM' },
                { title: 'Industry Insight', type: 'text', tips: 'Share a surprising statistic or trend', best_time: '12:30 PM' },
                { title: 'Behind-the-Scenes Reel', type: 'video', tips: 'Show authenticity — imperfect is relatable', best_time: '6:00 PM' },
                { title: 'Quotes & Motivation', type: 'image', tips: 'Use brand colours and clean fonts', best_time: '8:00 AM' },
                { title: 'Educational Infographic', type: 'infographic', tips: 'Keep text under 30 words per slide', best_time: '11:00 AM' },
                { title: 'Community Spotlight', type: 'story', tips: 'Tag featured members for extra reach', best_time: '3:00 PM' },
                { title: 'Week Recap & Preview', type: 'carousel', tips: 'Tease next week to build anticipation', best_time: '5:00 PM' },
            ],
            engagement: [
                { title: 'Poll / This-or-That', type: 'story', tips: 'Use 2-option polls for maximum taps', best_time: '9:00 AM' },
                { title: 'Ask Me Anything', type: 'text', tips: 'Respond to every comment within 30 min', best_time: '12:00 PM' },
                { title: 'User-Generated Content', type: 'image', tips: 'Credit the creator prominently', best_time: '2:00 PM' },
                { title: 'Live Q&A or Demo', type: 'live', tips: 'Promote 24h before to build audience', best_time: '7:00 PM' },
                { title: 'Challenge / Trend', type: 'video', tips: 'Add your unique spin to a trending format', best_time: '10:00 AM' },
                { title: 'Meme / Rel content', type: 'image', tips: 'Humor boosts shares — keep it on-brand', best_time: '1:00 PM' },
                { title: 'Engagement Recap', type: 'carousel', tips: 'Celebrate top comments and contributors', best_time: '4:00 PM' },
            ],
            leads: [
                { title: 'Problem Statement Post', type: 'text', tips: 'Describe the pain point vividly', best_time: '9:00 AM' },
                { title: 'Solution Teaser', type: 'carousel', tips: 'Reveal just enough to spark curiosity', best_time: '11:00 AM' },
                { title: 'Free Resource / Lead Magnet', type: 'image', tips: 'Use a clear CTA — link in bio', best_time: '1:00 PM' },
                { title: 'Testimonial / Case Study', type: 'video', tips: 'Include specific numbers and outcomes', best_time: '3:00 PM' },
                { title: 'How-to Guide', type: 'carousel', tips: 'Actionable steps get saved & shared', best_time: '10:00 AM' },
                { title: 'FAQ Buster', type: 'text', tips: 'Answer the #1 question you get from DMs', best_time: '12:00 PM' },
                { title: 'Soft CTA & Value Recap', type: 'story', tips: 'Summarize the week and offer a next step', best_time: '5:00 PM' },
            ],
            sales: [
                { title: 'Product Feature Highlight', type: 'image', tips: 'Focus on ONE benefit per post', best_time: '10:00 AM' },
                { title: 'Customer Success Story', type: 'video', tips: 'Real faces build more trust than graphics', best_time: '12:00 PM' },
                { title: 'Limited-Time Offer', type: 'image', tips: 'Add urgency — countdown or deadline', best_time: '2:00 PM' },
                { title: 'Comparison / Why Us', type: 'carousel', tips: 'Be factual, not bashing competitors', best_time: '11:00 AM' },
                { title: 'Unboxing / Demo', type: 'video', tips: 'Show the product in real-world use', best_time: '6:00 PM' },
                { title: 'Social Proof Roundup', type: 'carousel', tips: 'Screenshot DMs & reviews (with consent)', best_time: '1:00 PM' },
                { title: 'Flash Sale / Final CTA', type: 'story', tips: 'Last-chance energy — clear link & deadline', best_time: '7:00 PM' },
            ],
        };
        const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

        const weeklyThemes = [];
        for (let w = 0; w < weeks; w++) {
            const tpls = dailyTemplates[goal] || dailyTemplates.awareness;
            const daily_plan = dayNames.map((dayName, idx) => {
                const t = tpls[idx % tpls.length];
                return {
                    day: dayName,
                    platform: plats[idx % plats.length],
                    title: `${t.title} — ${themes[w % themes.length]}`,
                    description: `Create a ${t.type} for ${plats[idx % plats.length]} that ${t.title.toLowerCase()}. Align with this week's ${themes[w % themes.length].toLowerCase()} theme to drive ${goal}.`,
                    tips: t.tips,
                    best_time: t.best_time,
                };
            });

            weeklyThemes.push({
                week: w + 1,
                theme: themes[w % themes.length],
                description: `Week ${w + 1}: Focus on ${themes[w % themes.length].toLowerCase()} to drive ${goal}. Daily content planned across ${plats.join(', ')}.`,
                content_types: plats.map(p => `${p} post`),
                daily_plan,
            });
        }

        const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        const calendar = [];
        for (let w = 0; w < Math.min(weeks, 4); w++) {
            days.forEach((day, idx) => {
                if (calendar.length < 28) {
                    const t = (dailyTemplates[goal] || dailyTemplates.awareness)[idx % 7];
                    calendar.push({
                        day: day,
                        platform: plats[idx % plats.length],
                        content_type: t.type,
                        title: t.title,
                        description: `${themes[w % themes.length]} — ${t.title} for ${plats[idx % plats.length]}`,
                        best_time: t.best_time,
                    });
                }
            });
        }

        return {
            _isFallback: true,
            campaign_name: `${biz} ${goal.charAt(0).toUpperCase() + goal.slice(1)} Campaign`,
            campaign_summary: `A ${dur}-day ${voice} marketing campaign for ${biz} in the ${ind} industry, focused on ${goal}. This strategy covers ${plats.join(', ')} with weekly themed content.`,
            weekly_themes: weeklyThemes,
            content_calendar: calendar,
            kpis: {
                target_reach: '10,000+',
                engagement_rate: '4-6%',
                content_pieces: String(weeks * 5),
                follower_growth: '+15%',
            },
            recommendations: [
                `Post consistently at peak hours (10 AM & 7 PM) on ${plats.join(' and ')}.`,
                `Use a mix of educational and entertaining content to build engagement.`,
                `Track weekly KPIs and adjust themes based on audience response.`,
                `Engage with comments within 1 hour to boost algorithm visibility.`,
                `Repurpose top-performing content across ${plats.length > 1 ? 'platforms' : 'formats'}.`,
            ],
        };
    },

    renderStrategyReview(strategy, formData) {
        const step4 = document.getElementById('step4');
        if (!step4 || !strategy) return;

        const campaignName = strategy.campaign_name || `${formData.goal || 'Brand Awareness'} Campaign`;
        const summary = strategy.campaign_summary || 'AI-generated marketing campaign strategy.';
        const weeklyThemes = strategy.weekly_themes || [];
        const kpis = strategy.kpis || {};
        const calendar = strategy.content_calendar || [];
        const recommendations = strategy.recommendations || [];
        const duration = formData.duration || 30;

        // Dark-themed week colors (border accent + label color)
        const themeColors = [
            { border: 'border-indigo-500/30', label: 'color:#818cf8', accent: '#6366f1' },
            { border: 'border-cyan-500/30', label: 'color:#22d3ee', accent: '#06b6d4' },
            { border: 'border-amber-500/30', label: 'color:#fbbf24', accent: '#f59e0b' },
            { border: 'border-emerald-500/30', label: 'color:#34d399', accent: '#10b981' },
            { border: 'border-pink-500/30', label: 'color:#f472b6', accent: '#ec4899' },
        ];

        const platformIcons = {
            instagram: '<i class="fab fa-instagram text-pink-400"></i>',
            linkedin: '<i class="fab fa-linkedin text-blue-400"></i>',
            email: '<i class="fas fa-envelope" style="color:#818cf8;"></i>',
            sms: '<i class="fas fa-sms text-green-400"></i>',
            tiktok: '<i class="fab fa-tiktok" style="color:#e8eaed;"></i>',
            twitter: '<i class="fab fa-twitter text-blue-400"></i>',
        };

        const weeklyHTML = weeklyThemes.length > 0
            ? weeklyThemes.map((w, i) => {
                const c = themeColors[i % themeColors.length];
                const dailyPlan = w.daily_plan || [];

                const dailyPlanHTML = dailyPlan.length > 0
                    ? `<div class="mt-3">
                        <button class="w-full flex items-center justify-between text-xs font-bold uppercase tracking-wide py-1 transition" style="color:#9aa0b0;" onclick="this.nextElementSibling.classList.toggle('hidden'); this.querySelector('i').classList.toggle('fa-chevron-down'); this.querySelector('i').classList.toggle('fa-chevron-up');">
                            <span>Daily Plan (${dailyPlan.length} days)</span>
                            <i class="fas fa-chevron-down text-[10px]"></i>
                        </button>
                        <div class="hidden space-y-2 mt-2">
                        ${dailyPlan.map(d => `
                            <div class="flex items-start gap-2 p-2 rounded-lg" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04);">
                                <span class="px-2 py-0.5 text-[10px] font-bold rounded whitespace-nowrap" style="background:rgba(99,102,241,0.15); color:#818cf8;">${d.day || '?'}</span>
                                <div class="flex-1 min-w-0">
                                    <div class="flex items-center gap-1">
                                        ${platformIcons[(d.platform||'').toLowerCase()] || ''} 
                                        <span class="text-xs font-semibold truncate" style="color:#e8eaed;">${d.title || ''}</span>
                                    </div>
                                    <p class="text-[10px] mt-0.5" style="color:#9aa0b0;">${d.description || ''}</p>
                                    ${d.tips ? `<p class="text-[10px] italic mt-0.5" style="color:#06b6d4;">tip: ${d.tips}</p>` : ''}
                                </div>
                                <span class="text-[10px] whitespace-nowrap" style="color:#5f6680;">${d.best_time || ''}</span>
                            </div>
                        `).join('')}
                        </div>
                    </div>`
                    : '';

                return `<div class="p-4 rounded-xl" style="background:#0d1220; border:1px solid ${c.accent}33;">
                    <div class="text-xs font-bold mb-2" style="${c.label}">WEEK ${w.week || i + 1}</div>
                    <p class="text-sm font-semibold" style="color:#e8eaed;">${w.theme || 'Theme'}</p>
                    <p class="text-xs mt-1" style="color:#9aa0b0;">${w.description || ''}</p>
                    ${w.goal ? `<p class="text-xs mt-1 italic" style="color:#5f6680;">Goal: ${w.goal}</p>` : ''}
                    ${dailyPlanHTML}
                </div>`;
            }).join('')
            : `<div class="col-span-4 text-center py-4" style="color:#5f6680;">Themes included in calendar below</div>`;

        const kpiCards = Object.entries(kpis).length > 0
            ? Object.entries(kpis).slice(0, 6).map(([key, val]) => {
                const label = key.replace(/_/g, ' ').replace(/target /i, '').replace(/\b\w/g, l => l.toUpperCase());
                return `<div class="p-4 rounded-xl" style="background:#0d1220; border:1px solid rgba(255,255,255,0.06);">
                    <div class="text-2xl font-bold mb-1" style="color:#818cf8;">${val}</div>
                    <div class="text-sm" style="color:#9aa0b0;">${label}</div>
                </div>`;
            }).join('')
            : `<div class="p-4 rounded-xl" style="background:#0d1220; border:1px solid rgba(255,255,255,0.06);">
                <div class="text-2xl font-bold mb-1" style="color:#818cf8;">15K</div>
                <div class="text-sm" style="color:#9aa0b0;">Target Reach</div>
            </div>`;

        const calendarHTML = calendar.length > 0
            ? `<div class="overflow-x-auto"><table class="w-full text-sm">
                <thead><tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
                    <th class="px-3 py-2 text-left text-xs font-bold" style="color:#5f6680;">Day</th>
                    <th class="px-3 py-2 text-left text-xs font-bold" style="color:#5f6680;">Platform</th>
                    <th class="px-3 py-2 text-left text-xs font-bold" style="color:#5f6680;">Type</th>
                    <th class="px-3 py-2 text-left text-xs font-bold" style="color:#5f6680;">Title</th>
                    <th class="px-3 py-2 text-left text-xs font-bold" style="color:#5f6680;">Time</th>
                </tr></thead>
                <tbody>${calendar.slice(0, 7).map((c, i) => {
                    return `<tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                        <td class="px-3 py-2 font-medium" style="color:#c4c8d4;">Day ${c.day || '?'}</td>
                        <td class="px-3 py-2" style="color:#c4c8d4;">${platformIcons[(c.platform||'').toLowerCase()] || ''} ${c.platform || ''}</td>
                        <td class="px-3 py-2"><span class="px-2 py-1 text-xs rounded" style="background:rgba(99,102,241,0.15); color:#818cf8;">${c.content_type || c.type || ''}</span></td>
                        <td class="px-3 py-2" style="color:#e8eaed;">${c.title || c.description || ''}</td>
                        <td class="px-3 py-2" style="color:#5f6680;">${c.best_time || ''}</td>
                    </tr>`;
                }).join('')}${calendar.length > 7 ? calendar.slice(7).map((c, i) => {
                    return `<tr class="calendar-hidden-row" style="border-bottom:1px solid rgba(255,255,255,0.03); display:none;">
                        <td class="px-3 py-2 font-medium" style="color:#c4c8d4;">Day ${c.day || '?'}</td>
                        <td class="px-3 py-2" style="color:#c4c8d4;">${platformIcons[(c.platform||'').toLowerCase()] || ''} ${c.platform || ''}</td>
                        <td class="px-3 py-2"><span class="px-2 py-1 text-xs rounded" style="background:rgba(99,102,241,0.15); color:#818cf8;">${c.content_type || c.type || ''}</span></td>
                        <td class="px-3 py-2" style="color:#e8eaed;">${c.title || c.description || ''}</td>
                        <td class="px-3 py-2" style="color:#5f6680;">${c.best_time || ''}</td>
                    </tr>`;
                }).join('') : ''}</tbody>
            </table></div>
            ${calendar.length > 7 ? `<button id="calendarExpandBtn" onclick="app.expandCalendarRows()" class="w-full mt-2 py-2 text-xs font-semibold rounded-lg cursor-pointer transition" style="background:rgba(99,102,241,0.08); color:#818cf8; border:1px solid rgba(99,102,241,0.15);" onmouseover="this.style.background='rgba(99,102,241,0.15)'" onmouseout="this.style.background='rgba(99,102,241,0.08)'"><i class="fas fa-chevron-down mr-1"></i> + ${calendar.length - 7} more entries</button>` : ''}`
            : '<p class="text-center py-4" style="color:#5f6680;">Calendar details included in the strategy above</p>';

        const recsHTML = recommendations.length > 0
            ? `<ul class="space-y-2">${recommendations.map(r => 
                `<li class="flex items-start gap-2"><i class="fas fa-check-circle mt-0.5" style="color:#06b6d4;"></i><span class="text-sm" style="color:#c4c8d4;">${r}</span></li>`
            ).join('')}</ul>`
            : '';

        step4.innerHTML = `
            <div class="mb-8">
                <div class="flex items-center justify-between mb-4 flex-wrap gap-3">
                    <div class="flex items-center gap-3">
                        <div class="w-12 h-12 rounded-xl flex items-center justify-center" style="background:linear-gradient(135deg,#10b981,#34d399);">
                            <i class="fas fa-check text-white text-lg"></i>
                        </div>
                        <div>
                            <h2 class="text-xl sm:text-2xl font-bold" style="color:#ffffff;">${campaignName}</h2>
                            <p class="text-sm" style="color:#9aa0b0;">${duration}-Day ${formData.goal || 'Brand Awareness'} Campaign</p>
                        </div>
                    </div>
                    <button onclick="app.generateCampaignStrategy()" class="btn btn-secondary">
                        <i class="fas fa-sync mr-1"></i> Regenerate
                    </button>
                </div>
                <p class="mt-2" style="color:#9aa0b0;">${summary}</p>
            </div>

            <!-- Weekly Themes with Daily Plans -->
            <div class="mb-8">
                <h3 class="font-bold mb-4" style="color:#e8eaed;"><i class="fas fa-calendar-week mr-2" style="color:#6366f1;"></i>Weekly Themes & Daily Plans</h3>
                <div class="grid grid-cols-1 ${weeklyThemes.length <= 2 ? 'lg:grid-cols-' + weeklyThemes.length : 'lg:grid-cols-2'} gap-4">
                    ${weeklyHTML}
                </div>
            </div>

            <!-- KPIs -->
            <div class="mb-8">
                <h3 class="font-bold mb-4" style="color:#e8eaed;"><i class="fas fa-chart-line mr-2" style="color:#06b6d4;"></i>Success Metrics & KPIs</h3>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                    ${kpiCards}
                </div>
            </div>

            <!-- Content Calendar -->
            <div class="mb-8">
                <h3 class="font-bold mb-4" style="color:#e8eaed;"><i class="fas fa-table mr-2" style="color:#8b5cf6;"></i>Content Calendar Preview</h3>
                <div class="rounded-xl p-4" style="background:#0d1220; border:1px solid rgba(255,255,255,0.06);">
                    ${calendarHTML}
                </div>
            </div>

            <!-- Recommendations -->
            ${recommendations.length > 0 ? `
            <div class="mb-8">
                <h3 class="font-bold mb-4" style="color:#e8eaed;"><i class="fas fa-lightbulb mr-2" style="color:#fbbf24;"></i>AI Recommendations</h3>
                <div class="rounded-xl p-4" style="background:rgba(251,191,36,0.04); border:1px solid rgba(251,191,36,0.15);">
                    ${recsHTML}
                </div>
            </div>` : ''}

            <div class="mt-8 flex flex-col sm:flex-row justify-between gap-3">
                <button onclick="app.showStep(2)" class="btn btn-secondary">
                    <i class="fas fa-arrow-left mr-1"></i> Back
                </button>
                <div class="flex flex-col sm:flex-row gap-3">
                    <button onclick="app.generateCampaignStrategy()" class="btn btn-secondary">
                        <i class="fas fa-edit mr-1"></i> Refine Strategy
                    </button>
                    <button onclick="app.approveStrategy()" class="btn btn-primary">
                        <i class="fas fa-check mr-1"></i> Approve & Continue
                    </button>
                </div>
            </div>
        `;
    },

    getStrategyData() {
        // Collect data from wizard form
        return {
            businessName: document.getElementById('businessName')?.value || 'My Business',
            industry: document.getElementById('industry')?.value || 'technology',
            targetAudience: document.getElementById('targetAudience')?.value || 'General Audience',
            brandVoice: document.querySelector('.tone-option.active')?.dataset.tone || 'professional',
            budget: document.getElementById('budget')?.value || '$500 - $2,000',
            goal: document.getElementById('goal')?.value || 'awareness',
            duration: document.querySelector('.duration-option.active')?.dataset.duration || '30',
            platforms: Array.from(document.querySelectorAll('#step2 input[type="checkbox"]:checked'))
                .map(cb => cb.closest('label')?.textContent.trim().toLowerCase() || '')
                .filter(p => p)
        };
    },

    validateAndNext(targetStep) {
        const currentStep = this.wizardStep || 1;

        if (currentStep === 1) {
            const biz = document.getElementById('businessName');
            const ind = document.getElementById('industry');
            const goal = document.getElementById('goal');
            let valid = true;

            [biz, ind, goal].forEach(el => {
                if (el) el.style.borderColor = 'rgba(255,255,255,0.08)';
            });

            if (!biz || !biz.value.trim() || biz.value.trim() === 'My Business') {
                if (biz) { biz.style.borderColor = '#ef4444'; biz.focus(); }
                this.showToast('Please enter your business name', 'error');
                valid = false;
            } else if (!ind || !ind.value.trim()) {
                if (ind) { ind.style.borderColor = '#ef4444'; ind.focus(); }
                this.showToast('Please enter your industry', 'error');
                valid = false;
            } else if (!goal || !goal.value) {
                if (goal) { goal.style.borderColor = '#ef4444'; goal.focus(); }
                this.showToast('Please select a campaign goal', 'error');
                valid = false;
            }

            if (!valid) return;
        }

        if (currentStep === 2) {
            const checked = document.querySelectorAll('#step2 input[type="checkbox"]:checked');
            if (checked.length === 0) {
                this.showToast('Select at least one platform', 'error');
                return;
            }
        }

        this.showStep(targetStep);
    },

    showStep(stepNumber) {
        // Hide all steps
        document.querySelectorAll('.wizard-step').forEach(step => {
            step.classList.add('hidden');
        });
        
        // Show target step with fade animation
        const targetStep = document.getElementById(`step${stepNumber}`);
        if (targetStep) {
            targetStep.classList.remove('hidden');
            targetStep.style.animation = 'fadeIn .3s ease';
        }
        
        // Update progress bar
        const progressPercent = (stepNumber / 4) * 100;
        const progressBar = document.getElementById('progressBar');
        if (progressBar) {
            progressBar.style.width = `${progressPercent}%`;
        }
        
        // Update step indicators (dark-theme: uses .wizard-step-indicator with data-step)
        document.querySelectorAll('.wizard-step-indicator').forEach(indicator => {
            const sNum = parseInt(indicator.dataset.step);
            if (sNum <= stepNumber) {
                indicator.style.background = '#6366f1';
                indicator.style.color = '#ffffff';
                indicator.style.borderColor = 'transparent';
            } else {
                indicator.style.background = 'rgba(255,255,255,0.06)';
                indicator.style.color = '#5f6680';
                indicator.style.borderColor = 'rgba(255,255,255,0.08)';
            }
        });

        // Update step label text colors
        document.querySelectorAll('.wizard-step-label').forEach(label => {
            const sNum = parseInt(label.dataset.step);
            if (sNum <= stepNumber) {
                label.style.color = '#e8eaed';
            } else {
                label.style.color = '#5f6680';
            }
        });
        
        this.wizardStep = stepNumber;
    },

    // Content Studio Functions
    currentContent: {
        platform: 'instagram',
        contentType: 'video',
        caption: '',
        script: {},
        media: null,
        hashtags: [],
        scheduledTime: null
    },

    async createNewContent() {
        // Reset current content
        this.currentContent = {
            platform: 'instagram',
            contentType: 'video',
            caption: '',
            script: {},
            media: null,
            hashtags: [],
            scheduledTime: null
        };
        
        this.showToast('New content created. Start editing!');
    },

    async importMedia() {
        // Create file input
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*,video/*';
        input.onchange = async (e) => {
            const file = e.target.files[0];
            if (file) {
                this.currentContent.media = file;
                this.showToast(`Imported ${file.name}`, 'success');
                // TODO: Upload to backend/cloud storage
            }
        };
        input.click();
    },

    switchPlatform(platform) {
        this.currentContent.platform = platform;
        
        // Update UI - remove active class from all tabs
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Add active class to clicked tab
        const activeTab = document.querySelector(`[data-platform="${platform}"]`);
        if (activeTab) {
            activeTab.classList.add('active');
        }
        
        this.showToast(`Switched to ${platform.charAt(0).toUpperCase() + platform.slice(1)}`);
    },

    switchContentType(type) {
        this.currentContent.contentType = type;
        
        // Update UI
        const buttons = document.querySelectorAll('.flex.gap-2.p-1.bg-gray-100 button');
        buttons.forEach(btn => {
            btn.classList.remove('bg-white', 'rounded', 'font-medium');
            btn.classList.add('text-gray-600');
            if (btn.textContent.trim().toLowerCase() === type) {
                btn.classList.add('bg-white', 'rounded', 'font-medium');
                btn.classList.remove('text-gray-600');
            }
        });
        
        this.showToast(`Switched to ${type.charAt(0).toUpperCase() + type.slice(1)}`);
    },

    async saveDraft() {
        try {
            // Collect current content data
            const draftData = {
                ...this.currentContent,
                caption: document.querySelector('textarea[placeholder="Main content..."]')?.value || '',
                updatedAt: new Date().toISOString()
            };
            
            // Save to localStorage for now
            const drafts = JSON.parse(localStorage.getItem('contentDrafts') || '[]');
            const draftIndex = drafts.findIndex(d => d.id === this.currentContent.id);
            
            if (draftIndex >= 0) {
                drafts[draftIndex] = draftData;
            } else {
                draftData.id = `draft_${Date.now()}`;
                drafts.push(draftData);
            }
            
            localStorage.setItem('contentDrafts', JSON.stringify(drafts));
            
            this.currentContent = draftData;
            this.showToast('Draft saved successfully!', 'success');
            
        } catch (error) {
            console.error('Error saving draft:', error);
            this.showToast('Failed to save draft', 'error');
        }
    },

    async regenerateContent() {
        try {
            this.showLoading();
            
            const contentType = this.currentContent.contentType;
            const platform = this.currentContent.platform;
            
            // Prepare AI request
            const request = {
                business_id: this.user?.id || 'demo_business_1',
                content_type: contentType,
                platform: platform,
                business_context: {
                    business_name: this.businessProfile?.business_name || 'My Business',
                    industry: this.businessProfile?.industry || 'technology',
                    brand_voice: this.businessProfile?.brand_voice || 'professional',
                    target_audience: this.businessProfile?.target_audience || []
                },
                tone: this.businessProfile?.brand_voice || 'professional',
                topic: 'Product showcase',
                optimization: true
            };
            
            // Call appropriate AI service based on content type
            let generatedContent;
            
            if (contentType === 'text') {
                generatedContent = await window.AIService.generateTextContent(request);
            } else if (contentType === 'image' || contentType === 'carousel') {
                generatedContent = await window.AIService.generateVisualContent(request);
            } else if (contentType === 'video' || contentType === 'story') {
                generatedContent = await window.AIService.generateVideoContent(request);
            }
            
            if (generatedContent) {
                // Update UI with generated content
                const captionField = document.querySelector('textarea[placeholder="Main content..."]');
                if (captionField && generatedContent.caption) {
                    captionField.value = generatedContent.caption;
                }
                
                // Update hashtags if available
                if (generatedContent.hashtags) {
                    this.currentContent.hashtags = generatedContent.hashtags;
                    this.updateHashtagsUI(generatedContent.hashtags);
                }
                
                this.hideLoading();
                this.showToast('Content regenerated successfully!', 'success');
            }
            
        } catch (error) {
            this.hideLoading();
            console.error('Error regenerating content:', error);
            this.showToast('Failed to regenerate content. Please try again.', 'error');
        }
    },

    updateHashtagsUI(hashtags) {
        const hashtagContainer = document.querySelector('.flex.flex-wrap.gap-2.mb-3');
        if (hashtagContainer) {
            hashtagContainer.innerHTML = hashtags.map(tag => 
                `<span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">${tag}</span>`
            ).join('');
        }
    },

    async scheduleContent() {
        // Show date/time picker modal
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
        modal.innerHTML = `
            <div class="bg-white rounded-2xl p-6 max-w-md w-full">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold text-gray-900">Schedule Content</h3>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">Date</label>
                        <input type="date" id="scheduleDate" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-teal-500" value="${new Date().toISOString().split('T')[0]}">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-2">Time</label>
                        <input type="time" id="scheduleTime" class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-teal-500" value="09:00">
                    </div>
                    <div class="flex gap-3 pt-4">
                        <button onclick="this.closest('.fixed').remove()" class="btn btn-secondary flex-1">
                            Cancel
                        </button>
                        <button onclick="app.confirmSchedule()" class="btn btn-primary flex-1">
                            <i class="fas fa-calendar-check"></i> Schedule
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    async confirmSchedule() {
        const dateInput = document.getElementById('scheduleDate');
        const timeInput = document.getElementById('scheduleTime');
        
        if (dateInput && timeInput) {
            const scheduledTime = `${dateInput.value}T${timeInput.value}:00`;
            this.currentContent.scheduledTime = scheduledTime;
            
            // Save to backend or localStorage
            await this.saveDraft();
            
            // Close modal
            document.querySelector('.fixed.inset-0').remove();
            
            this.showToast(`Content scheduled for ${new Date(scheduledTime).toLocaleString()}`, 'success');
        }
    },

    async optimizeHashtags() {
        try {
            this.showLoading();
            
            const request = {
                business_id: this.user?.id || 'demo_business_1',
                platform: this.currentContent.platform,
                content_type: this.currentContent.contentType,
                caption: document.querySelector('textarea[placeholder="Main content..."]')?.value || '',
                industry: this.businessProfile?.industry || 'technology'
            };
            
            // This would call an AI service to optimize hashtags
            // For now, let's use mock data
            const optimizedTags = [
                '#marketing', '#digitalmarketing', '#socialmedia', 
                '#contentcreator', '#businessgrowth', '#ai', 
                '#innovation', '#entrepreneur', '#success', '#trending'
            ];
            
            this.currentContent.hashtags = optimizedTags;
            this.updateHashtagsUI(optimizedTags);
            
            this.hideLoading();
            this.showToast('Hashtags optimized!', 'success');
            
        } catch (error) {
            this.hideLoading();
            console.error('Error optimizing hashtags:', error);
            this.showToast('Failed to optimize hashtags', 'error');
        }
    },

    async generateContentFromAI() {
        try {
            this.showLoading();
            
            // Use AI service to generate complete content
            await this.regenerateContent();
            
        } catch (error) {
            this.hideLoading();
            console.error('Error generating AI content:', error);
            this.showToast('Failed to generate content', 'error');
        }
    },

    // Content Generation Functions
    async generateContent(contentRequest) {
        try {
            this.showLoading();
            
            const content = await window.apiContract.generateContent(contentRequest);
            
            this.hideLoading();
            this.showToast('Content generated successfully!', 'success');
            
            return content;
        } catch (error) {
            this.hideLoading();
            console.error('Error generating content:', error);
            this.showToast('Failed to generate content. Please try again.', 'error');
            return null;
        }
    },

    async generateWeekContent() {
        if (!this.currentCampaign) {
            this.showToast('No campaign yet — let\'s create a strategy first!', 'info');
            setTimeout(() => this.loadView('strategy'), 1000);
            return;
        }

        const contentRequest = {
            campaign_id: this.currentCampaign._id,
            type: 'text',
            platform: 'instagram',
            tone: this.businessProfile.brand_voice,
            themes: ['Product Focus', 'Behind the Scenes', 'Customer Stories'],
            quantity: 7 // One post per day for a week
        };

        const contents = [];
        
        for (let i = 0; i < 7; i++) {
            const content = await this.generateContent(contentRequest);
            if (content) {
                contents.push(content);
            }
        }

        this.showToast(`Generated ${contents.length} posts for the week!`, 'success');
        return contents;
    },

    /**
     * Voice-to-Campaign: Upload audio file → AssemblyAI transcription → Gemini campaign brief
     */
    async handleVoiceToCampaign(input) {
        const file = input.files && input.files[0];
        if (!file) return;

        const resultDiv = document.getElementById('voiceCampaignResult');
        if (resultDiv) {
            resultDiv.classList.remove('hidden');
            resultDiv.innerHTML = `
                <div class="p-3 bg-purple-50 border border-purple-200 rounded-lg animate-pulse text-center">
                    <i class="fas fa-spinner fa-spin text-purple-500 text-lg mb-2"></i>
                    <p class="text-xs text-purple-600 font-medium">Transcribing audio with AssemblyAI...</p>
                    <p class="text-xs text-gray-500 mt-1">Then generating campaign brief with Gemini</p>
                </div>`;
        }

        try {
            const formData = new FormData();
            formData.append('file', file);

            const baseUrl = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL)
                ? window.CONFIG.API.BASE_URL : 'http://localhost:8000';

            const resp = await fetch(`${baseUrl}/api/v1/ai/voice-to-campaign`, {
                method: 'POST',
                body: formData
            });

            if (!resp.ok) throw new Error('Voice processing failed');
            const result = await resp.json();
            const data = result.data || {};

            if (resultDiv) {
                resultDiv.innerHTML = `
                    <div class="space-y-2">
                        <div class="p-3 bg-green-50 border border-green-200 rounded-lg">
                            <div class="flex items-center gap-2 mb-1">
                                <i class="fas fa-check-circle text-green-500"></i>
                                <span class="text-xs font-bold text-green-700">TRANSCRIBED</span>
                            </div>
                            <p class="text-xs text-gray-600 italic">"${(data.transcript || '').substring(0, 150)}..."</p>
                        </div>
                        ${data.campaign_brief ? `
                        <div class="p-3 bg-purple-50 border border-purple-200 rounded-lg">
                            <div class="flex items-center justify-between mb-1">
                                <div class="flex items-center gap-2">
                                    <i class="fas fa-bullhorn text-purple-500"></i>
                                    <span class="text-xs font-bold text-purple-700">CAMPAIGN BRIEF</span>
                                </div>
                                <button class="flex items-center gap-1 px-1.5 py-0.5 text-[10px] bg-purple-100 text-purple-600 rounded-full hover:bg-purple-200" onclick="ContentStudio.speakText('${(typeof data.campaign_brief === 'string' ? data.campaign_brief : JSON.stringify(data.campaign_brief)).substring(0, 300).replace(/'/g, "\\'")}')">
                                    <i class="fas fa-volume-up"></i>
                                </button>
                            </div>
                            <p class="text-xs text-gray-700">${typeof data.campaign_brief === 'string' ? data.campaign_brief.substring(0, 300) : JSON.stringify(data.campaign_brief).substring(0, 300)}</p>
                        </div>` : ''}
                    </div>`;
            }
            this.showToast('Voice transcribed and campaign generated!', 'success');
        } catch (err) {
            console.warn('[Voice] Error:', err);
            if (resultDiv) {
                resultDiv.innerHTML = `
                    <div class="p-3 bg-red-50 border border-red-200 rounded-lg text-center">
                        <i class="fas fa-exclamation-triangle text-red-500"></i>
                        <p class="text-xs text-red-600">${err.message || 'Failed to process audio'}</p>
                    </div>`;
            }
            this.showToast('Voice processing failed', 'error');
        }

        // Reset file input
        input.value = '';
    },

    /**
     * Refresh the content calendar sidebar with saved drafts from localStorage
     */
    refreshContentCalendar() {
        const container = document.getElementById('contentCalendarList');
        if (!container) return;

        const drafts = JSON.parse(localStorage.getItem('contentDrafts') || '[]');
        const typeColors = {
            caption: { bg: 'bg-teal-50', border: 'border-teal-500', badge: 'bg-teal-100 text-teal-700', icon: 'fab fa-instagram text-pink-500' },
            email: { bg: 'bg-blue-50', border: 'border-blue-500', badge: 'bg-blue-100 text-blue-700', icon: 'fas fa-envelope text-red-500' },
            sms: { bg: 'bg-green-50', border: 'border-green-500', badge: 'bg-green-100 text-green-700', icon: 'fas fa-sms text-green-600' },
            post_idea: { bg: 'bg-purple-50', border: 'border-purple-500', badge: 'bg-purple-100 text-purple-700', icon: 'fas fa-lightbulb text-yellow-500' },
        };
        const statusLabels = {
            draft: '<span class="text-[10px] px-1.5 py-0.5 bg-gray-100 text-gray-600 rounded">Draft</span>',
            scheduled: '<span class="text-[10px] px-1.5 py-0.5 bg-yellow-100 text-yellow-700 rounded">Scheduled</span>',
            published: '<span class="text-[10px] px-1.5 py-0.5 bg-green-100 text-green-700 rounded">Published</span>',
        };

        if (drafts.length === 0) {
            container.innerHTML = `
                <div class="p-4 text-center">
                    <i class="fas fa-pen-fancy text-gray-300 text-2xl mb-2"></i>
                    <p class="text-xs text-gray-400">No drafts yet</p>
                    <p class="text-[10px] text-gray-400 mt-1">Create content and save as draft</p>
                </div>`;
            return;
        }

        container.innerHTML = drafts.slice(0, 10).map((draft, idx) => {
            const tc = typeColors[draft.contentType] || typeColors.caption;
            const date = draft.updatedAt ? new Date(draft.updatedAt).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }) : '';
            const status = statusLabels[draft.status] || statusLabels.draft;
            return `
                <div class="p-3 ${idx === 0 ? tc.bg + ' border-l-4 ' + tc.border : 'border border-gray-200'} rounded cursor-pointer hover:bg-gray-50 transition" onclick="app.loadDraftIntoEditor('${draft.id}')">
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-xs text-gray-500 font-semibold">${date}</span>
                        ${status}
                    </div>
                    <div class="text-sm font-semibold text-gray-900 truncate">${draft.title || 'Untitled'}</div>
                    <div class="flex items-center gap-2 mt-2">
                        <i class="${tc.icon}" style="font-size:12px"></i>
                        <span class="text-xs ${tc.badge} px-2 py-0.5 rounded">${draft.contentType || 'caption'}</span>
                        ${draft.status === 'draft' ? `
                            <button onclick="event.stopPropagation(); app.publishContent('${draft.id}')" class="ml-auto text-[10px] text-teal-600 hover:text-teal-700 font-bold"><i class="fas fa-paper-plane"></i> Publish</button>
                        ` : ''}
                        <button onclick="event.stopPropagation(); app.deleteDraft('${draft.id}')" class="text-[10px] text-red-400 hover:text-red-600"><i class="fas fa-trash"></i></button>
                    </div>
                </div>`;
        }).join('');
    },

    /**
     * Load a saved draft back into the editor
     */
    loadDraftIntoEditor(draftId) {
        const drafts = JSON.parse(localStorage.getItem('contentDrafts') || '[]');
        const draft = drafts.find(d => d.id === draftId);
        if (!draft) return;

        if (window.ContentStudio) {
            window.ContentStudio.currentContent = { ...draft };
            window.ContentStudio.switchContentType(draft.contentType || 'caption');

            // After form renders, populate the text
            setTimeout(() => {
                const textField = document.getElementById('captionText');
                if (textField && draft.caption) textField.value = draft.caption;
                const subjectField = document.getElementById('emailSubject');
                if (subjectField && draft.title) subjectField.value = draft.title;
                const topicField = document.getElementById('ideaTopic');
                if (topicField && draft.title) topicField.value = draft.title;
            }, 50);
        }
        this.showToast(`Loaded: ${draft.title || 'Draft'}`);
    },

    /**
     * Publish content (simulate pushing to platform)
     */
    publishContent(draftId) {
        const drafts = JSON.parse(localStorage.getItem('contentDrafts') || '[]');
        const idx = drafts.findIndex(d => d.id === draftId);
        if (idx === -1) return;

        drafts[idx].status = 'published';
        drafts[idx].publishedAt = new Date().toISOString();
        localStorage.setItem('contentDrafts', JSON.stringify(drafts));

        // Also add to published posts
        const published = JSON.parse(localStorage.getItem('publishedPosts') || '[]');
        published.push(drafts[idx]);
        localStorage.setItem('publishedPosts', JSON.stringify(published));

        this.refreshContentCalendar();
        this.showToast(`Published "${drafts[idx].title}" to ${drafts[idx].platform || 'platform'}!`, 'success');
    },

    /**
     * Delete a draft
     */
    deleteDraft(draftId) {
        let drafts = JSON.parse(localStorage.getItem('contentDrafts') || '[]');
        drafts = drafts.filter(d => d.id !== draftId);
        localStorage.setItem('contentDrafts', JSON.stringify(drafts));
        this.refreshContentCalendar();
        this.showToast('Draft deleted');
    },

    /* ═══════════════════════════════════════════════════════════════
     *  THUMBNAIL GENERATION (Canvas-based)
     * ═════════════════════════════════════════════════════════════ */
    generateThumbnail() {
        const text = document.getElementById('captionText')?.value || 'Your Content Here';
        const preview = document.getElementById('thumbnailPreview');
        if (!preview) return;

        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 200;
        const ctx = canvas.getContext('2d');

        // Gradient background
        const grad = ctx.createLinearGradient(0, 0, 400, 200);
        const palettes = [
            ['#667eea', '#764ba2'],
            ['#f093fb', '#f5576c'],
            ['#4facfe', '#00f2fe'],
            ['#43e97b', '#38f9d7'],
            ['#fa709a', '#fee140'],
            ['#a18cd1', '#fbc2eb']
        ];
        const pal = palettes[Math.floor(Math.random() * palettes.length)];
        grad.addColorStop(0, pal[0]);
        grad.addColorStop(1, pal[1]);
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, 400, 200);

        // Decorative shapes
        ctx.globalAlpha = 0.15;
        ctx.fillStyle = '#fff';
        ctx.beginPath(); ctx.arc(320, 40, 60, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(80, 160, 40, 0, Math.PI * 2); ctx.fill();
        ctx.globalAlpha = 1;

        // Text
        const shortText = text.substring(0, 60) + (text.length > 60 ? '...' : '');
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 20px Inter, Arial, sans-serif';
        ctx.textAlign = 'center';
        ctx.shadowColor = 'rgba(0,0,0,0.3)';
        ctx.shadowBlur = 4;
        // Word wrap
        const words = shortText.split(' ');
        let lines = [];
        let line = '';
        for (const word of words) {
            const test = line + word + ' ';
            if (ctx.measureText(test).width > 340 && line) { lines.push(line.trim()); line = word + ' '; }
            else line = test;
        }
        lines.push(line.trim());
        const startY = 100 - (lines.length - 1) * 14;
        lines.forEach((l, i) => ctx.fillText(l, 200, startY + i * 28));

        // Branding
        ctx.shadowBlur = 0;
        ctx.font = '12px Inter, Arial, sans-serif';
        ctx.globalAlpha = 0.7;
        ctx.fillText('Omni Mind', 200, 185);
        ctx.globalAlpha = 1;

        preview.innerHTML = '';
        const img = new Image();
        img.src = canvas.toDataURL('image/png');
        img.className = 'w-full h-full object-cover rounded';
        preview.appendChild(img);

        // Also allow download
        const link = document.createElement('a');
        link.download = 'thumbnail.png';
        link.href = canvas.toDataURL('image/png');
        link.className = 'text-[10px] text-orange-600 font-semibold hover:text-orange-700 block mt-1 text-center';
        link.innerHTML = '<i class="fas fa-download mr-1"></i> Download';
        preview.parentElement.appendChild(link);

        this.showToast('Thumbnail generated!', 'success');
    },

    /* ═══════════════════════════════════════════════════════════════
     *  TEXT STYLE HELPERS
     * ═════════════════════════════════════════════════════════════ */
    applyTextStyle(style) {
        const field = document.getElementById('captionText');
        if (!field) return;
        let text = field.value;

        switch (style) {
            case 'bold':
                // Unicode bold (works on social media)
                text = text.replace(/([A-Za-z])/g, (m) => {
                    const c = m.charCodeAt(0);
                    if (c >= 65 && c <= 90) return String.fromCodePoint(c - 65 + 0x1D400);
                    if (c >= 97 && c <= 122) return String.fromCodePoint(c - 97 + 0x1D41A);
                    return m;
                });
                break;
            case 'italic':
                text = text.replace(/([A-Za-z])/g, (m) => {
                    const c = m.charCodeAt(0);
                    if (c >= 65 && c <= 90) return String.fromCodePoint(c - 65 + 0x1D434);
                    if (c >= 97 && c <= 122) return String.fromCodePoint(c - 97 + 0x1D44E);
                    return m;
                });
                break;
            case 'uppercase':
                text = text.toUpperCase();
                break;
            case 'hashtags':
                // Auto-generate hashtags from keywords
                const words = text.replace(/[^a-zA-Z0-9\s]/g, '').split(/\s+/).filter(w => w.length > 3);
                const tags = [...new Set(words)].slice(0, 5).map(w => '#' + w.charAt(0).toUpperCase() + w.slice(1).toLowerCase());
                text = text + '\n\n' + tags.join(' ');
                break;
        }
        field.value = text;
        this.showToast(`Applied ${style} style`, 'success');
    },

    /* ═══════════════════════════════════════════════════════════════
     *  TRANSLATE CONTENT (via Gemini)
     * ═════════════════════════════════════════════════════════════ */
    async translateContent(language) {
        const field = document.getElementById('captionText');
        if (!field || !field.value.trim()) { this.showToast('Enter content first', 'error'); return; }

        this.showLoading();
        try {
            const baseUrl = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            const resp = await fetch(`${baseUrl}/api/v1/agent/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: `Translate the following marketing content to ${language}. Keep emojis, hashtags, and formatting. Only return the translated text, no explanation:\n\n${field.value}`
                })
            });
            const data = await resp.json();
            const answer = data?.data?.answer || data?.answer || '';
            if (answer) {
                field.value = answer;
                this.showToast(`Translated to ${language}!`, 'success');
            } else {
                this.showToast('Translation returned empty', 'error');
            }
        } catch (err) {
            this.showToast('Translation failed: ' + err.message, 'error');
        }
        this.hideLoading();
    },

    /* ═══════════════════════════════════════════════════════════════
     *  ADAPT FOR MOBILE (via Gemini)
     * ═════════════════════════════════════════════════════════════ */
    async adaptForMobile() {
        const field = document.getElementById('captionText');
        if (!field || !field.value.trim()) { this.showToast('Enter content first', 'error'); return; }

        this.showLoading();
        try {
            const baseUrl = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            const resp = await fetch(`${baseUrl}/api/v1/agent/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: `Adapt the following marketing content for mobile viewing. Make it shorter, punchier, use line breaks for readability, keep emojis. Only return the adapted text:\n\n${field.value}`
                })
            });
            const data = await resp.json();
            const answer = data?.data?.answer || data?.answer || '';
            if (answer) {
                field.value = answer;
                this.showToast('Adapted for mobile!', 'success');
            }
        } catch (err) {
            this.showToast('Adaptation failed: ' + err.message, 'error');
        }
        this.hideLoading();
    },

    async optimizeContent(contentId, optimizationType) {
        try {
            this.showLoading();
            
            const optimizationData = {
                optimization_type: optimizationType,
                target_platform: 'instagram',
                target_engagement: 8.0
            };
            
            const optimizedContent = await window.apiContract.demoGenerateContent(optimizationData);
            
            this.hideLoading();
            this.showToast('Content optimized successfully!', 'success');
            
            return optimizedContent;
        } catch (error) {
            this.hideLoading();
            console.error('Error optimizing content:', error);
            this.showToast('Failed to optimize content. Please try again.', 'error');
            return null;
        }
    },

    // Analytics Functions
    async simulateAnalytics(contentId) {
        try {
            const analytics = await window.apiContract.simulateAnalytics({ content_id: contentId });
            
            // Update UI with simulated metrics
            this.updateContentMetrics(contentId, analytics);
            
            return analytics;
        } catch (error) {
            console.error('Error simulating analytics:', error);
            // Fallback to mock data
            return this.getMockAnalytics(contentId);
        }
    },

    getMockAnalytics(contentId) {
        return {
            content_id: contentId,
            platform: 'instagram',
            metrics: {
                views: Math.floor(Math.random() * 10000) + 1000,
                likes: Math.floor(Math.random() * 1000) + 100,
                comments: Math.floor(Math.random() * 100) + 10,
                shares: Math.floor(Math.random() * 50) + 5,
                watch_time_seconds: Math.floor(Math.random() * 3000) + 300
            },
            engagement_score: Math.floor(Math.random() * 30) + 70,
            recorded_at: new Date().toISOString()
        };
    },

    updateContentMetrics(contentId, analytics) {
        // Update the content item in the UI with new metrics
        const contentElement = document.querySelector(`[data-content-id="${contentId}"]`);
        if (contentElement) {
            const metricsElement = contentElement.querySelector('.content-metrics');
            if (metricsElement) {
                metricsElement.innerHTML = `
                    <div class="flex items-center gap-4 text-xs text-gray-600">
                        <span><i class="fas fa-heart text-red-500"></i> ${analytics.metrics.likes}</span>
                        <span><i class="fas fa-comment text-blue-500"></i> ${analytics.metrics.comments}</span>
                        <span><i class="fas fa-share text-green-500"></i> ${analytics.metrics.shares}</span>
                    </div>
                    <div class="text-xs text-gray-500">ER: ${analytics.engagement_score}%</div>
                `;
            }
        }
    },

    // Messaging Functions
    async getAIMessageReply(messageId) {
        try {
            const reply = await window.apiContract.generateAIReply({ business_id: 'demo_business_1', customer_message: 'How can I help?' });
            return reply;
        } catch (error) {
            console.error('Error getting AI reply:', error);
            return this.getMockAIReply();
        }
    },

    getMockAIReply() {
        const replies = [
            "Thank you for your interest! Our team will get back to you shortly.",
            "Great question! Let me help you with that.",
            "I'd be happy to provide more information about our services.",
            "That's a fantastic point! Let me address that for you.",
            "I appreciate your message! Here's what I can tell you..."
        ];
        
        return replies[Math.floor(Math.random() * replies.length)];
    },

    // Utility Functions
    showLoading() {
        try {
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                overlay.classList.remove('hidden');
            } else {
                console.warn('Loading overlay element not found');
            }
        } catch (error) {
            console.error('Error showing loading overlay:', error);
        }
    },

    hideLoading() {
        try {
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                overlay.classList.add('hidden');
            } else {
                console.warn('Loading overlay element not found');
            }
        } catch (error) {
            console.error('Error hiding loading overlay:', error);
        }
    },

    // ─── Calendar rendering ───
    _calendarDate: new Date(),

    renderCalendar() {
        const d = this._calendarDate;
        const year = d.getFullYear();
        const month = d.getMonth();
        const today = new Date();

        // Title
        const titleEl = document.getElementById('calendarMonthTitle');
        if (titleEl) titleEl.textContent = d.toLocaleString('default', { month: 'long', year: 'numeric' });

        const grid = document.getElementById('calendarGrid');
        if (!grid) return;
        grid.innerHTML = '';

        const firstDay = new Date(year, month, 1).getDay(); // 0=Sun
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Load campaigns from localStorage
        const campaigns = JSON.parse(localStorage.getItem('campaigns') || '[]');
        const drafts = JSON.parse(localStorage.getItem('contentDrafts') || '[]');

        // Build map: "YYYY-MM-DD" → [{label,color}]
        const eventMap = {};
        campaigns.forEach(c => {
            if (c.startDate) {
                const key = c.startDate.slice(0, 10);
                if (!eventMap[key]) eventMap[key] = [];
                eventMap[key].push({ label: c.name || 'Campaign', color: 'bg-teal-500' });
            }
        });
        drafts.forEach(dr => {
            if (dr.scheduledDate) {
                const key = new Date(dr.scheduledDate).toISOString().slice(0, 10);
                if (!eventMap[key]) eventMap[key] = [];
                eventMap[key].push({ label: dr.platform || 'Draft', color: 'bg-purple-500' });
            }
        });

        // Also map strategy daily plans
        if (this.currentStrategy && this.currentStrategy.weekly_themes) {
            const start = this.currentStrategy._approvedDate ? new Date(this.currentStrategy._approvedDate) : new Date();
            this.currentStrategy.weekly_themes.forEach((wk, wi) => {
                (wk.daily_plan || []).forEach((dp, di) => {
                    const dd = new Date(start);
                    dd.setDate(dd.getDate() + wi * 7 + di);
                    const key = dd.toISOString().slice(0, 10);
                    if (!eventMap[key]) eventMap[key] = [];
                    eventMap[key].push({ label: dp.title || dp.platform || 'Plan', color: 'bg-indigo-500' });
                });
            });
        }

        // Blanks before first day
        for (let i = 0; i < firstDay; i++) {
            const blank = document.createElement('div');
            blank.className = 'min-h-[80px]';
            blank.style.cssText = 'background:rgba(255,255,255,0.02);';
            grid.appendChild(blank);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const cell = document.createElement('div');
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const isToday = (today.getFullYear() === year && today.getMonth() === month && today.getDate() === day);
            cell.className = `min-h-[80px] p-1 calendar-day cursor-pointer transition relative`;
            cell.style.cssText = isToday 
                ? 'background:rgba(99,102,241,0.15); border:1px solid rgba(99,102,241,0.4); border-radius:8px;'
                : 'background:#131825; border:1px solid rgba(255,255,255,0.04); border-radius:8px;';
            cell.dataset.date = dateStr;

            const dayNum = document.createElement('div');
            dayNum.className = 'text-xs font-bold mb-1';
            dayNum.style.color = isToday ? '#818cf8' : '#c4c8d4';
            dayNum.textContent = day;
            cell.appendChild(dayNum);

            // Events
            const events = eventMap[dateStr] || [];
            const evWrap = document.createElement('div');
            evWrap.className = 'space-y-0.5';
            events.slice(0, 3).forEach(ev => {
                const tag = document.createElement('div');
                tag.className = `${ev.color} text-white text-[9px] rounded px-1 py-px truncate`;
                tag.textContent = ev.label;
                evWrap.appendChild(tag);
            });
            if (events.length > 3) {
                const more = document.createElement('div');
                more.className = 'text-[9px] text-gray-400';
                more.textContent = `+${events.length - 3} more`;
                evWrap.appendChild(more);
            }
            cell.appendChild(evWrap);
            grid.appendChild(cell);
        }

        // Trailing blanks
        const total = firstDay + daysInMonth;
        const trailing = (7 - (total % 7)) % 7;
        for (let i = 0; i < trailing; i++) {
            const blank = document.createElement('div');
            blank.className = 'min-h-[80px]';
            blank.style.cssText = 'background:rgba(255,255,255,0.02);';
            grid.appendChild(blank);
        }

        // Re-init drag-drop
        this.initCalendarDragDrop();
    },

    calendarPrevMonth() {
        this._calendarDate.setMonth(this._calendarDate.getMonth() - 1);
        this.renderCalendar();
    },
    calendarNextMonth() {
        this._calendarDate.setMonth(this._calendarDate.getMonth() + 1);
        this.renderCalendar();
    },
    calendarToday() {
        this._calendarDate = new Date();
        this.renderCalendar();
    },

    initCalendarDragDrop() {
        const calendarDays = document.querySelectorAll('.calendar-day');
        const contentItems = document.querySelectorAll('.content-item');
        
        // Add drag event listeners to content items
        contentItems.forEach(item => {
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/html', e.target.innerHTML);
                e.target.classList.add('dragging');
            });
            
            item.addEventListener('dragend', (e) => {
                e.target.classList.remove('dragging');
            });
        });
        
        // Add drop event listeners to calendar days
        calendarDays.forEach(day => {
            day.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                day.classList.add('drag-over');
            });
            
            day.addEventListener('dragleave', (e) => {
                day.classList.remove('drag-over');
            });
            
            day.addEventListener('drop', (e) => {
                e.preventDefault();
                day.classList.remove('drag-over');
                
                const draggedContent = e.dataTransfer.getData('text/html');
                const spaceDiv = day.querySelector('.space-y-1');
                
                if (spaceDiv) {
                    const newContent = document.createElement('div');
                    newContent.className = 'content-item';
                    newContent.setAttribute('draggable', 'true');
                    newContent.innerHTML = draggedContent;
                    spaceDiv.appendChild(newContent);
                    
                    // Re-initialize drag events for new element
                    this.initCalendarDragDrop();
                    
                    this.showToast('Content rescheduled successfully', 'success');
                }
            });
        });
    },

    showContentDetails(contentType, date) {
        const detailsDiv = document.getElementById('contentDetails');
        if (!detailsDiv) return;
        
        const contentDetails = {
            instagram: {
                title: 'Instagram Post',
                caption: 'Transform your business with AI-powered marketing! ðŸš€',
                hashtags: ['#marketing', '#AI', '#businessgrowth', '#innovation'],
                engagement: '2.3K likes, 145 comments',
                status: 'Scheduled'
            },
            linkedin: {
                title: 'LinkedIn Article',
                caption: 'How AI is revolutionizing small business marketing strategies in 2024...',
                hashtags: ['#business', '#AI', '#marketing', '#strategy'],
                engagement: '542 views, 28 likes',
                status: 'Published'
            },
            email: {
                title: 'Email Newsletter',
                caption: 'Weekly marketing insights and tips for your business...',
                hashtags: ['#newsletter', '#marketing', '#tips'],
                engagement: '45% open rate, 12% CTR',
                status: 'Draft'
            },
            video: {
                title: 'Video Content',
                caption: 'Behind the scenes: How we create marketing campaigns...',
                hashtags: ['#video', '#marketing', '#behindthescenes'],
                engagement: '8.9K views, 234 comments',
                status: 'Scheduled'
            },
            image: {
                title: 'Image Post',
                caption: 'Marketing statistics that will blow your mind! ðŸ“Š',
                hashtags: ['#marketing', '#stats', '#data'],
                engagement: '1.2K likes, 89 shares',
                status: 'Published'
            }
        };
        
        const details = contentDetails[contentType] || contentDetails.instagram;
        
        detailsDiv.innerHTML = `
            <div class="space-y-4">
                <div class="flex items-center justify-between">
                    <h4 class="text-lg font-bold text-gray-900">${details.title}</h4>
                    <span class="status-pill status-${details.status.toLowerCase()}">${details.status}</span>
                </div>
                
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Caption</label>
                    <p class="text-gray-700 bg-gray-50 p-3 rounded-lg">${details.caption}</p>
                </div>
                
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Hashtags</label>
                    <div class="flex flex-wrap gap-2">
                        ${details.hashtags.map(tag => `<span class="px-2 py-1 bg-gray-100 text-gray-700 rounded text-sm">${tag}</span>`).join('')}
                    </div>
                </div>
                
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Performance</label>
                    <p class="text-gray-600">${details.engagement}</p>
                </div>
                
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Scheduled for</label>
                    <p class="text-gray-600">${date}</p>
                </div>
                
                <div class="flex gap-3 pt-4">
                    <button class="btn btn-secondary">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn btn-secondary">
                        <i class="fas fa-copy"></i> Duplicate
                    </button>
                    <button class="btn btn-danger">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        `;
    },

    loadView(viewName) {
        const viewContainer = document.getElementById('viewContainer');
        if (!viewContainer) {
            console.error('View container not found!');
            return;
        }
        
        console.log(`Loading view: ${viewName}`);
        console.log('View content available:', !!this.views[viewName]);
        
        // Set current view
        this.currentView = viewName;
        
        viewContainer.innerHTML = this.views[viewName] || '<div class="text-center py-8">View not found</div>';
        
        console.log('View loaded successfully');
        
        // Re-initialize view-specific functionality
        if (viewName === 'home') {
            setTimeout(() => {
                this.updateHeroGreeting();
                this.animateCounters();
                this.updateStreak();
                // Load proactive AI insights for health score & anomalies
                if (window.AIChatPanel) AIChatPanel.loadInsights();
            }, 80);
        }

        if (viewName === 'calendar') {
            setTimeout(() => {
                this.renderCalendar();
            }, 100);
        }
        
        // Initialize strategy wizard if on strategy view
        if (viewName === 'strategy') {
            setTimeout(() => {
                // Make sure step 1 is shown
                this.showStep(1);
            }, 100);
        }
        
        // Initialize analytics charts if on analytics view
        if (viewName === 'analytics') {
            setTimeout(() => {
                if (window.AnalyticsDashboard) {
                    window.AnalyticsDashboard.initCharts();
                }
            }, 150);
        }
        
        // Initialize content studio if on content view
        if (viewName === 'content') {
            setTimeout(() => {
                if (window.ContentStudio) {
                    window.ContentStudio.renderContentForm('caption');
                }
                this.refreshContentCalendar();
                // Inject Social Publisher panel (FB/IG/Email + AI Captions)
                if (window.SocialPublisher) {
                    SocialPublisher.injectPublishPanel();
                }
            }, 100);
        }

        // Initialize inbox
        if (viewName === 'inbox') {
            setTimeout(() => this.initInbox(), 80);
        }

        // Initialize settings with user data
        if (viewName === 'settings') {
            setTimeout(() => this.populateSettingsView(), 80);
        }
        
        // Update active navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        const activeNav = document.querySelector(`[data-view="${viewName}"]`);
        if (activeNav) {
            activeNav.classList.add('active');
        }
    },

    showToast(message) {
        const toast = document.createElement('div');
        toast.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;background:#1e293b;border:1px solid #334155;color:#e2e8f0;padding:12px 20px;border-radius:12px;display:flex;align-items:center;gap:10px;box-shadow:0 8px 24px rgba(0,0,0,.4);animation:fadeIn .3s ease';
        toast.innerHTML = `
            <i class="fas fa-check-circle" style="color:#34d399;font-size:1.15rem"></i>
            <span style="font-weight:600">${message}</span>
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity .3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 2700);
    },

    updateUserProfile() {
        // Delegate to unified updateUserProfileUI which uses new sidebar IDs
        this.updateUserProfileUI();
    },

    populateSettingsView() {
        const user = this.user || {};
        const biz = this.businessProfile || {};

        // Provider badge
        const badge = document.getElementById('settingsProviderBadge');
        if (badge) {
            const p = user.provider || 'unknown';
            const icons = { google: 'fab fa-google', linkedin: 'fab fa-linkedin', email: 'fas fa-envelope', demo: 'fas fa-flask' };
            const colors = { google: '#ea4335', linkedin: '#0A66C2', email: '#818cf8', demo: '#fbbf24' };
            badge.innerHTML = `<i class="${icons[p] || 'fas fa-user'}" style="margin-right:4px;"></i>${p.charAt(0).toUpperCase() + p.slice(1)}`;
            badge.style.color = colors[p] || '#818cf8';
        }

        // Avatar
        const av = document.getElementById('settingsAvatar');
        if (av) {
            if (user.picture) {
                av.innerHTML = `<img src="${user.picture}" class="w-16 h-16 rounded-full object-cover" alt="">`;
            } else {
                const initials = (user.name || user.email || 'U').split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
                av.textContent = initials;
            }
        }

        // Display name/email
        const dn = document.getElementById('settingsDisplayName');
        if (dn) dn.textContent = user.name || user.full_name || 'User';
        const de = document.getElementById('settingsDisplayEmail');
        if (de) de.textContent = user.email || '';

        // Form fields
        const fn = document.getElementById('profileFirstName');
        if (fn) fn.value = user.firstName || (user.name ? user.name.split(' ')[0] : '');
        const ln = document.getElementById('profileLastName');
        if (ln) ln.value = user.lastName || (user.name ? user.name.split(' ').slice(1).join(' ') : '');
        const em = document.getElementById('profileEmail');
        if (em) em.value = user.email || '';

        // Business fields
        const bn = document.getElementById('bizName');
        if (bn) bn.value = biz.business_name || biz.name || '';
        const bi = document.getElementById('bizIndustry');
        if (bi) bi.value = biz.industry || 'Technology';
        const bv = document.getElementById('bizVoice');
        if (bv) bv.value = biz.brand_voice || 'Professional';
        const ba = document.getElementById('bizAudience');
        if (ba) {
            const aud = biz.target_audience;
            if (Array.isArray(aud) && aud.length && typeof aud[0] === 'object') {
                ba.value = aud[0].segment_name || '';
            } else if (typeof aud === 'string') {
                ba.value = aud;
            }
        }

        // Goals chips
        const goalsContainer = document.getElementById('bizGoals');
        if (goalsContainer) {
            const allGoals = ['Brand Awareness', 'Lead Generation', 'Engagement', 'Sales', 'Community', 'Thought Leadership'];
            const activeGoals = biz.primary_goals || [];
            goalsContainer.innerHTML = allGoals.map(g => {
                const isActive = activeGoals.includes(g);
                return `<button onclick="this.classList.toggle('active-goal'); this.dataset.selected = this.dataset.selected === 'true' ? 'false' : 'true'" 
                    data-goal="${g}" data-selected="${isActive}" 
                    class="px-3 py-1.5 rounded-full text-xs font-medium transition ${isActive ? 'active-goal' : ''}" 
                    style="background:${isActive ? 'rgba(99,102,241,0.2)' : 'rgba(255,255,255,0.04)'}; color:${isActive ? '#818cf8' : '#9aa0b0'}; border:1px solid ${isActive ? 'rgba(99,102,241,0.3)' : 'rgba(255,255,255,0.08)'};">
                    ${g}
                </button>`;
            }).join('');
        }
    },

    saveProfileSettings() {
        // Gather form values
        const firstName = (document.getElementById('profileFirstName') || {}).value || '';
        const lastName = (document.getElementById('profileLastName') || {}).value || '';
        const name = (firstName + ' ' + lastName).trim();

        // Update user object
        if (this.user) {
            this.user.firstName = firstName;
            this.user.lastName = lastName;
            this.user.name = name;
            this.user.full_name = name;
            // Persist to localStorage
            localStorage.setItem('user_info', JSON.stringify(this.user));
            localStorage.setItem('user_profile', JSON.stringify(this.user));
            this.updateUserProfileUI();
        }

        // Update business profile
        const bizName = (document.getElementById('bizName') || {}).value || '';
        const bizIndustry = (document.getElementById('bizIndustry') || {}).value || 'Technology';
        const bizVoice = (document.getElementById('bizVoice') || {}).value || 'Professional';
        const bizAudience = (document.getElementById('bizAudience') || {}).value || '';

        // Collect selected goals
        const goalBtns = document.querySelectorAll('#bizGoals button[data-selected="true"]');
        const goals = Array.from(goalBtns).map(b => b.dataset.goal);

        this.businessProfile = {
            ...(this.businessProfile || {}),
            business_name: bizName,
            industry: bizIndustry,
            brand_voice: bizVoice,
            primary_goals: goals.length ? goals : ['Brand Awareness'],
            target_audience: bizAudience ? [{ segment_name: bizAudience, age_range: '', interests: [] }] : []
        };
        localStorage.setItem('business_profile', JSON.stringify(this.businessProfile));

        this.showToast('Profile saved successfully!', 'success');
    },

    showTechArchitecture() {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
        modal.innerHTML = `
            <div class="bg-white rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
                <div class="sticky top-0 bg-white border-b border-gray-200 p-6">
                    <div class="flex items-center justify-between">
                        <h2 class="text-2xl font-bold text-gray-900">Technical Architecture</h2>
                        <button class="text-gray-400 hover:text-gray-600">
                            <i class="fas fa-times text-xl"></i>
                        </button>
                    </div>
                </div>
                
                <div class="p-6 space-y-8">
                    <!-- Layered Architecture -->
                    <div>
                        <h3 class="text-xl font-bold text-gray-900 mb-4">ðŸ—ï¸ 5-Layer Architecture</h3>
                        <div class="space-y-4">
                            <div class="border-l-4 border-teal-500 pl-4">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center">
                                        <span class="text-xs font-bold text-teal-700">1</span>
                                    </div>
                                    <h4 class="font-semibold text-gray-900">User Interface Layer</h4>
                                </div>
                                <p class="text-gray-600 ml-11">Web dashboard with React.js, Tailwind CSS, drag-and-drop UI</p>
                            </div>
                            <div class="border-l-4 border-blue-500 pl-4">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                                        <span class="text-xs font-bold text-blue-700">2</span>
                                    </div>
                                    <h4 class="font-semibold text-gray-900">Application & Orchestration Layer</h4>
                                </div>
                                <p class="text-gray-600 ml-11">Node.js/FastAPI, business logic, API orchestration, workflow management</p>
                            </div>
                            <div class="border-l-4 border-purple-500 pl-4">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                                        <span class="text-xs font-bold text-purple-700">3</span>
                                    </div>
                                    <h4 class="font-semibold text-gray-900">AI & Intelligence Layer</h4>
                                </div>
                                <p class="text-gray-600 ml-11">GPT-4.5/GPT-5 APIs, LangChain, Strategy AI, Content AI, Optimization AI</p>
                            </div>
                            <div class="border-l-4 border-orange-500 pl-4">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
                                        <span class="text-xs font-bold text-orange-700">4</span>
                                    </div>
                                    <h4 class="font-semibold text-gray-900">Data Layer</h4>
                                </div>
                                <p class="text-gray-600 ml-11">PostgreSQL, MongoDB, Redis, AWS S3 for scalable data storage</p>
                            </div>
                            <div class="border-l-4 border-green-500 pl-4">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                                        <span class="text-xs font-bold text-green-700">5</span>
                                    </div>
                                    <h4 class="font-semibold text-gray-900">Integration & API Layer</h4>
                                </div>
                                <p class="text-gray-600 ml-11">Platform APIs, Email/SMS gateways, RESTful/GraphQL APIs</p>
                            </div>
                        </div>
                    </div>

                    <!-- Tech Stack -->
                    <div>
                        <h3 class="text-xl font-bold text-gray-900 mb-4">ðŸ’» Tech Stack</h3>
                        <div class="bg-gray-50 rounded-xl p-6">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <h4 class="font-semibold text-gray-900 mb-3">Frontend</h4>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm">React.js</span>
                                        <span class="px-3 py-1 bg-cyan-100 text-cyan-700 rounded text-sm">Tailwind CSS</span>
                                        <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">Framer Motion</span>
                                    </div>
                                </div>
                                <div>
                                    <h4 class="font-semibold text-gray-900 mb-3">Backend</h4>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-green-100 text-green-700 rounded text-sm">Node.js</span>
                                        <span class="px-3 py-1 bg-emerald-100 text-emerald-700 rounded text-sm">Express</span>
                                        <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm">FastAPI</span>
                                    </div>
                                </div>
                                <div>
                                    <h4 class="font-semibold text-gray-900 mb-3">AI</h4>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm">OpenAI GPT-4.5</span>
                                        <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded text-sm">LangChain</span>
                                    </div>
                                </div>
                                <div>
                                    <h4 class="font-semibold text-gray-900 mb-3">Database</h4>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm">PostgreSQL</span>
                                        <span class="px-3 py-1 bg-green-100 text-green-700 rounded text-sm">MongoDB</span>
                                        <span class="px-3 py-1 bg-red-100 text-red-700 rounded text-sm">Redis</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- MVP Considerations -->
                    <div>
                        <h3 class="text-xl font-bold text-gray-900 mb-4">ðŸš€ MVP Features</h3>
                        <div class="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
                            <ul class="space-y-2">
                                <li class="flex items-start gap-2">
                                    <i class="fas fa-check text-yellow-600 mt-1"></i>
                                    <span class="text-gray-700">Simulated external APIs for social media publishing</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <i class="fas fa-check text-yellow-600 mt-1"></i>
                                    <span class="text-gray-700">AI content generation via GPT API</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <i class="fas fa-check text-yellow-600 mt-1"></i>
                                    <span class="text-gray-700">Mock engagement data for analytics</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <i class="fas fa-check text-yellow-600 mt-1"></i>
                                    <span class="text-gray-700">Modular architecture for each epic</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.closest('button')) {
                modal.remove();
            }
        });
    },

    showHelp() {
        const existing = document.getElementById('helpModal');
        if (existing) { existing.remove(); return; }

        const modal = document.createElement('div');
        modal.id = 'helpModal';
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4';
        modal.style.cssText = 'background:rgba(0,0,0,.6);backdrop-filter:blur(8px)';
        modal.innerHTML = `
            <div class="rounded-2xl shadow-2xl max-w-2xl w-full max-h-[85vh] overflow-y-auto" style="background:#131825;border:1px solid rgba(99,102,241,.15);">
                <div class="p-6 flex items-center justify-between" style="border-bottom:1px solid rgba(255,255,255,.06);">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl flex items-center justify-center" style="background:linear-gradient(135deg,#6366f1,#06b6d4);"><i class="fas fa-question-circle text-white"></i></div>
                        <h2 class="text-xl font-bold" style="color:#fff;">Help & User Guide</h2>
                    </div>
                    <button onclick="document.getElementById('helpModal').remove()" style="color:#5f6680;" class="hover:text-white transition"><i class="fas fa-times text-xl"></i></button>
                </div>
                <div class="p-6 space-y-6">
                    <div>
                        <h3 class="font-bold mb-2" style="color:#e8eaed;"><i class="fas fa-route mr-2" style="color:#06b6d4;"></i>Getting Started</h3>
                        <ol class="list-decimal list-inside text-sm space-y-1.5" style="color:#9aa0b0;">
                            <li><strong style="color:#c4c8d4;">Strategy</strong> — Create a campaign strategy. Enter business details, select platforms, choose a duration, and generate an AI-powered plan.</li>
                            <li><strong style="color:#c4c8d4;">Approve Strategy</strong> — Review weekly themes & daily plans. Click "Approve & Continue" to activate.</li>
                            <li><strong style="color:#c4c8d4;">Content Studio</strong> — Create content (captions, emails, SMS) using AI. Use voice input, text, or file import.</li>
                            <li><strong style="color:#c4c8d4;">Calendar</strong> — View your content calendar with campaign events.</li>
                            <li><strong style="color:#c4c8d4;">Analytics</strong> — Monitor performance, ask AI questions, and get smart recommendations.</li>
                        </ol>
                    </div>
                    <div>
                        <h3 class="font-bold mb-2" style="color:#e8eaed;"><i class="fas fa-lightbulb mr-2" style="color:#fbbf24;"></i>Key Features</h3>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <div class="p-3 rounded-lg" style="background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.15);">
                                <p class="text-sm font-semibold" style="color:#818cf8;">🎯 AI Strategy Generator</p>
                                <p class="text-xs mt-1" style="color:#9aa0b0;">Creates weekly themes with detailed day-by-day plans tailored to your business.</p>
                            </div>
                            <div class="p-3 rounded-lg" style="background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.15);">
                                <p class="text-sm font-semibold" style="color:#22d3ee;">✍️ Content Studio</p>
                                <p class="text-xs mt-1" style="color:#9aa0b0;">Generate captions, emails, SMS campaigns with AI. Supports voice, text & file input.</p>
                            </div>
                            <div class="p-3 rounded-lg" style="background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.15);">
                                <p class="text-sm font-semibold" style="color:#a78bfa;">📅 Smart Calendar</p>
                                <p class="text-xs mt-1" style="color:#9aa0b0;">Full month calendar with campaign markers and scheduled posts.</p>
                            </div>
                            <div class="p-3 rounded-lg" style="background:rgba(236,72,153,.08);border:1px solid rgba(236,72,153,.15);">
                                <p class="text-sm font-semibold" style="color:#f472b6;">📱 Social Publishing</p>
                                <p class="text-xs mt-1" style="color:#9aa0b0;">Publish to Instagram & Facebook directly. Share via email too.</p>
                            </div>
                            <div class="p-3 rounded-lg" style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.15);">
                                <p class="text-sm font-semibold" style="color:#34d399;">🔊 Voice-to-Campaign</p>
                                <p class="text-xs mt-1" style="color:#9aa0b0;">Speak your idea or upload audio. AI transcribes and generates content.</p>
                            </div>
                            <div class="p-3 rounded-lg" style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.15);">
                                <p class="text-sm font-semibold" style="color:#fbbf24;">🤖 AI Analysis</p>
                                <p class="text-xs mt-1" style="color:#9aa0b0;">Get engagement score, trending hashtags, caption variants & posting recommendations.</p>
                            </div>
                        </div>
                    </div>
                    <div>
                        <h3 class="font-bold mb-2" style="color:#e8eaed;"><i class="fas fa-keyboard mr-2" style="color:#5f6680;"></i>Quick Tips</h3>
                        <ul class="text-sm space-y-1.5" style="color:#9aa0b0;">
                            <li>• Press <kbd class="px-1.5 py-0.5 rounded text-xs" style="background:rgba(255,255,255,.06);color:#818cf8;">Ctrl+K</kbd> to open the command palette.</li>
                            <li>• Click the <i class="fas fa-brain" style="color:#818cf8;"></i> FAB to chat with your AI assistant.</li>
                            <li>• Use <strong style="color:#c4c8d4;">Regenerate</strong> in strategy review to generate a new plan with the same settings.</li>
                            <li>• Expand <strong style="color:#c4c8d4;">Daily Plan</strong> in each week to see day-by-day details.</li>
                            <li>• The + button creates new content; bell shows notifications.</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
    },

    // ── Quick Create Modal (+ button) ──
    showQuickCreate() {
        const existing = document.getElementById('quickCreateModal');
        if (existing) { existing.remove(); return; }

        const modal = document.createElement('div');
        modal.id = 'quickCreateModal';
        modal.className = 'fixed inset-0 z-50 flex items-start justify-center pt-20 px-4';
        modal.style.cssText = 'background:rgba(0,0,0,.5);backdrop-filter:blur(6px)';
        modal.innerHTML = `
            <div class="w-full max-w-md rounded-2xl shadow-2xl overflow-hidden" style="background:#131825;border:1px solid rgba(99,102,241,.15);animation:fadeIn .2s ease;">
                <div class="p-5" style="border-bottom:1px solid rgba(255,255,255,.06);">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-bold" style="color:#fff;"><i class="fas fa-plus-circle mr-2" style="color:#818cf8;"></i>Quick Create</h3>
                        <button onclick="document.getElementById('quickCreateModal').remove()" style="color:#5f6680;" class="hover:text-white transition"><i class="fas fa-times"></i></button>
                    </div>
                </div>
                <div class="p-5 space-y-2">
                    <button onclick="document.getElementById('quickCreateModal').remove(); app.loadView('strategy')" class="w-full flex items-center gap-4 p-4 rounded-xl transition-all" style="background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.1);" onmouseover="this.style.background='rgba(99,102,241,.12)'" onmouseout="this.style.background='rgba(99,102,241,.06)'">
                        <div class="w-10 h-10 rounded-xl flex items-center justify-center" style="background:rgba(99,102,241,.15);"><i class="fas fa-rocket" style="color:#818cf8;"></i></div>
                        <div class="text-left"><p class="text-sm font-semibold" style="color:#e8eaed;">New Campaign</p><p class="text-xs" style="color:#5f6680;">Create an AI-powered marketing strategy</p></div>
                    </button>
                    <button onclick="document.getElementById('quickCreateModal').remove(); app.loadView('content')" class="w-full flex items-center gap-4 p-4 rounded-xl transition-all" style="background:rgba(6,182,212,.06);border:1px solid rgba(6,182,212,.1);" onmouseover="this.style.background='rgba(6,182,212,.12)'" onmouseout="this.style.background='rgba(6,182,212,.06)'">
                        <div class="w-10 h-10 rounded-xl flex items-center justify-center" style="background:rgba(6,182,212,.15);"><i class="fas fa-pen-fancy" style="color:#22d3ee;"></i></div>
                        <div class="text-left"><p class="text-sm font-semibold" style="color:#e8eaed;">New Content</p><p class="text-xs" style="color:#5f6680;">Write captions, emails, or SMS with AI</p></div>
                    </button>
                    <button onclick="document.getElementById('quickCreateModal').remove(); app.loadView('calendar')" class="w-full flex items-center gap-4 p-4 rounded-xl transition-all" style="background:rgba(139,92,246,.06);border:1px solid rgba(139,92,246,.1);" onmouseover="this.style.background='rgba(139,92,246,.12)'" onmouseout="this.style.background='rgba(139,92,246,.06)'">
                        <div class="w-10 h-10 rounded-xl flex items-center justify-center" style="background:rgba(139,92,246,.15);"><i class="fas fa-calendar-plus" style="color:#a78bfa;"></i></div>
                        <div class="text-left"><p class="text-sm font-semibold" style="color:#e8eaed;">Schedule Post</p><p class="text-xs" style="color:#5f6680;">Add content to your calendar</p></div>
                    </button>
                    <button onclick="document.getElementById('quickCreateModal').remove(); if(window.AIChatPanel)AIChatPanel.toggle();" class="w-full flex items-center gap-4 p-4 rounded-xl transition-all" style="background:rgba(236,72,153,.06);border:1px solid rgba(236,72,153,.1);" onmouseover="this.style.background='rgba(236,72,153,.12)'" onmouseout="this.style.background='rgba(236,72,153,.06)'">
                        <div class="w-10 h-10 rounded-xl flex items-center justify-center" style="background:rgba(236,72,153,.15);"><i class="fas fa-brain" style="color:#f472b6;"></i></div>
                        <div class="text-left"><p class="text-sm font-semibold" style="color:#e8eaed;">Ask AI</p><p class="text-xs" style="color:#5f6680;">Chat with your AI marketing assistant</p></div>
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
    },

    // ── Notification Panel (bell icon) ──
    showNotificationPanel() {
        const existing = document.getElementById('notifPanel');
        if (existing) { existing.remove(); return; }

        // Hide the red badge
        const badge = document.getElementById('notifBadge');
        if (badge) badge.style.display = 'none';

        const now = new Date();
        const timeAgo = (mins) => mins < 60 ? `${mins}m ago` : `${Math.floor(mins/60)}h ago`;

        const notifications = [
            { icon: 'fa-chart-line', color: '#10b981', bg: 'rgba(16,185,129,.12)', title: 'Campaign Performance Up 23%', desc: 'Your "Brand Awareness" campaign engagement rate increased significantly this week.', time: timeAgo(15) },
            { icon: 'fa-envelope', color: '#818cf8', bg: 'rgba(99,102,241,.12)', title: 'New Message from Sarah Kim', desc: 'Hey, can we review the December content calendar together?', time: timeAgo(42) },
            { icon: 'fa-calendar-check', color: '#06b6d4', bg: 'rgba(6,182,212,.12)', title: '3 Posts Scheduled for Today', desc: 'Instagram (10 AM), LinkedIn (12 PM), Email blast (3 PM)', time: timeAgo(90) },
            { icon: 'fa-brain', color: '#a78bfa', bg: 'rgba(139,92,246,.12)', title: 'AI Generated New Strategy', desc: 'Your 30-day plan is ready for review with daily action items.', time: timeAgo(180) },
            { icon: 'fa-fire', color: '#f59e0b', bg: 'rgba(245,158,11,.12)', title: 'Trending Topic Alert', desc: 'AI detected a trending topic in your niche. Create content now for maximum reach!', time: timeAgo(240) },
        ];

        const panel = document.createElement('div');
        panel.id = 'notifPanel';
        panel.className = 'fixed inset-0 z-50';
        panel.style.cssText = 'background:rgba(0,0,0,.4);backdrop-filter:blur(4px)';
        panel.innerHTML = `
            <div class="absolute top-16 right-4 w-96 max-w-[calc(100vw-2rem)] rounded-2xl shadow-2xl overflow-hidden" style="background:#131825;border:1px solid rgba(99,102,241,.15);animation:fadeIn .2s ease;">
                <div class="p-4 flex items-center justify-between" style="border-bottom:1px solid rgba(255,255,255,.06);">
                    <h3 class="text-sm font-bold" style="color:#fff;"><i class="fas fa-bell mr-2" style="color:#818cf8;"></i>Notifications</h3>
                    <div class="flex items-center gap-3">
                        <button onclick="document.querySelectorAll('#notifPanel .notif-item').forEach(n=>n.style.opacity='.5')" class="text-xs font-medium" style="color:#06b6d4;">Mark all read</button>
                        <button onclick="document.getElementById('notifPanel').remove()" style="color:#5f6680;" class="hover:text-white transition"><i class="fas fa-times"></i></button>
                    </div>
                </div>
                <div class="max-h-96 overflow-y-auto divide-y" style="border-color:rgba(255,255,255,.04);">
                    ${notifications.map(n => `
                        <div class="notif-item flex items-start gap-3 p-4 transition cursor-pointer" style="border-bottom:1px solid rgba(255,255,255,.03);" onmouseover="this.style.background='rgba(255,255,255,.03)'" onmouseout="this.style.background='transparent'">
                            <div class="w-9 h-9 rounded-lg flex-shrink-0 flex items-center justify-center" style="background:${n.bg};">
                                <i class="fas ${n.icon} text-sm" style="color:${n.color};"></i>
                            </div>
                            <div class="flex-1 min-w-0">
                                <p class="text-sm font-semibold" style="color:#e8eaed;">${n.title}</p>
                                <p class="text-xs mt-0.5 leading-relaxed" style="color:#9aa0b0;">${n.desc}</p>
                                <p class="text-[10px] mt-1" style="color:#5f6680;">${n.time}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="p-3 text-center" style="border-top:1px solid rgba(255,255,255,.06);">
                    <button onclick="document.getElementById('notifPanel').remove(); app.loadView('inbox')" class="text-xs font-semibold" style="color:#818cf8;">View All Notifications <i class="fas fa-arrow-right ml-1"></i></button>
                </div>
            </div>
        `;
        document.body.appendChild(panel);
        panel.addEventListener('click', (e) => { if (e.target === panel) panel.remove(); });
    },

    signOut() {
        auth.signOut();
    },

    // --- UI Enhancement Methods ---

    updateHeroGreeting() {
        const h = new Date().getHours();
        let greeting, emoji, motivation;
        const name = this.user?.name?.split(' ')[0] || 'there';
        
        if (h < 6) {
            greeting = `Burning the midnight oil, ${name}`;
            emoji = '\u{1F319}';
            motivation = 'Late-night ideas often become breakthrough campaigns.';
        } else if (h < 12) {
            greeting = `Good morning, ${name}`;
            emoji = '\u{2600}\u{FE0F}';
            motivation = 'Fresh day, fresh opportunities. What will you create?';
        } else if (h < 17) {
            greeting = `Good afternoon, ${name}`;
            emoji = '\u{1F31E}';
            motivation = 'Your campaigns are running strong. Keep the momentum going.';
        } else if (h < 21) {
            greeting = `Good evening, ${name}`;
            emoji = '\u{1F307}';
            motivation = 'Great time to review today\'s performance and plan ahead.';
        } else {
            greeting = `Winding down, ${name}`;
            emoji = '\u{1F303}';
            motivation = 'Quick recap of the day before you head out?';
        }

        const el = document.getElementById('heroGreeting');
        const emojiEl = document.getElementById('heroTimeEmoji');
        const motEl = document.getElementById('heroMotivation');
        if (el) el.textContent = greeting;
        if (emojiEl) emojiEl.textContent = emoji;
        if (motEl) motEl.textContent = motivation;
    },

    animateCounters() {
        const counters = [
            { selector: '.counter-time', target: 87, suffix: '%' },
            { selector: '.counter-engage', target: 3.2, suffix: 'x', decimal: true },
            { selector: '.counter-platforms', target: 5, suffix: '' },
        ];
        counters.forEach(c => {
            const el = document.querySelector(c.selector);
            if (!el) return;
            let current = 0;
            const step = c.target / 30;
            const interval = setInterval(() => {
                current += step;
                if (current >= c.target) {
                    current = c.target;
                    clearInterval(interval);
                }
                el.textContent = (c.decimal ? current.toFixed(1) : Math.round(current)) + c.suffix;
            }, 30);
        });
    },

    updateStreak() {
        const today = new Date().toDateString();
        let streak = JSON.parse(localStorage.getItem('loginStreak') || '{"count":0,"lastDate":""}');
        if (streak.lastDate !== today) {
            const yesterday = new Date(Date.now() - 86400000).toDateString();
            streak.count = (streak.lastDate === yesterday) ? streak.count + 1 : 1;
            streak.lastDate = today;
            localStorage.setItem('loginStreak', JSON.stringify(streak));
        }
        const streakBanner = document.querySelector('.streak-banner');
        if (streakBanner && streak.count > 0) {
            const countEl = streakBanner.querySelector('.streak-fire');
            const textEl = streakBanner.querySelector('p.text-sm');
            const subEl = streakBanner.querySelector('p.text-xs');
            if (textEl) textEl.textContent = `${streak.count}-day streak!`;
            if (subEl) subEl.textContent = streak.count >= 7
                ? `Incredible! ${streak.count} days straight. You're unstoppable!`
                : streak.count >= 3
                ? `You've logged in ${streak.count} days in a row. Keep it up!`
                : 'Welcome back! Start building your streak.';
        }
    },

    toggleAIHelper() {
        if (window.AIChatPanel) {
            AIChatPanel.toggle();
        }
    },

    /* ══════════════════════════════════════════════════════════════════
       INBOX — fully interactive, API-connected inbox
       ══════════════════════════════════════════════════════════════════ */
    _inboxThreads: [],
    _inboxFilter: 'all',
    _inboxActiveThread: null,

    async initInbox() {
        await Promise.all([this._loadInboxThreads(), this._loadInboxStats()]);
    },

    async _loadInboxStats() {
        try {
            const base = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            const r = await fetch(`${base}/api/v1/inbox/stats`);
            const d = await r.json();
            const s = d?.data || {};
            const el = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
            el('statTotal', s.total_messages || 0);
            el('statUnread', s.unread || 0);
            el('statAvgTime', s.avg_response_time || '—');
            el('statAiReplies', s.ai_replies_today || 0);
            el('inboxUnreadBadge', `${s.unread || 0} unread`);
            // Update sidebar badge
            const badge = document.querySelector('[data-view="inbox"] .badge');
            if (badge) badge.textContent = s.unread || 0;
        } catch (e) { console.warn('Inbox stats error', e); }
    },

    async _loadInboxThreads(platform, search) {
        try {
            const base = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            let url = `${base}/api/v1/inbox/threads?business_id=demo`;
            if (platform && platform !== 'all') url += `&platform=${platform}`;
            if (search) url += `&search=${encodeURIComponent(search)}`;
            const r = await fetch(url);
            const d = await r.json();
            this._inboxThreads = d?.data?.threads || [];
            this._renderThreadList();
        } catch (e) {
            console.warn('Inbox threads error', e);
            document.getElementById('threadList').innerHTML = '<div class="p-4 text-center text-xs" style="color:#f87171;">Failed to load conversations</div>';
        }
    },

    _platformMeta: {
        instagram: { icon: 'fab fa-instagram',  color: '#e1306c', gradient: 'from-purple-500 to-pink-500' },
        email:     { icon: 'fas fa-envelope',    color: '#818cf8', gradient: 'from-blue-500 to-cyan-500' },
        linkedin:  { icon: 'fab fa-linkedin',    color: '#0a66c2', gradient: 'from-blue-600 to-blue-400' },
        sms:       { icon: 'fas fa-sms',         color: '#34d399', gradient: 'from-green-500 to-teal-500' },
        twitter:   { icon: 'fab fa-twitter',     color: '#1da1f2', gradient: 'from-blue-400 to-cyan-400' },
    },

    _renderThreadList() {
        const el = document.getElementById('threadList');
        if (!el) return;
        if (!this._inboxThreads.length) {
            el.innerHTML = '<div class="p-6 text-center"><i class="fas fa-inbox text-2xl mb-2" style="color:#1e2538;"></i><p class="text-xs" style="color:#5f6680;">No conversations found</p></div>';
            return;
        }
        el.innerHTML = this._inboxThreads.map(t => {
            const pm = this._platformMeta[t.platform] || this._platformMeta.email;
            const initials = (t.customer_name || '??').split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
            const isActive = this._inboxActiveThread === t.thread_id;
            const timeAgo = this._timeAgo(t.last_time);
            const unread = t.unread_count > 0;
            const catColors = { 'Product Inquiry': '#06b6d4', 'Technical': '#a78bfa', 'Business': '#3b82f6', 'Support': '#34d399', 'Feedback': '#f59e0b', 'Pricing': '#ec4899' };
            const catColor = catColors[t.category] || '#5f6680';

            return `<div class="p-3 cursor-pointer transition-all" style="background:${isActive ? 'rgba(99,102,241,.08)' : 'transparent'};border-left:3px solid ${isActive ? '#6366f1' : 'transparent'};" onmouseover="if(!${isActive})this.style.background='rgba(255,255,255,.02)'" onmouseout="if(!${isActive})this.style.background='transparent'" onclick="app.openThread('${t.thread_id}')">
                <div class="flex items-start gap-3">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold text-xs flex-shrink-0 bg-gradient-to-br ${pm.gradient}">
                        ${initials}
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center justify-between">
                            <span class="text-sm font-semibold truncate" style="color:${unread ? '#e8eaed' : '#9aa0b0'};">${t.customer_name}</span>
                            <span class="text-[10px] flex-shrink-0 ml-2" style="color:#5f6680;">${timeAgo}</span>
                        </div>
                        <div class="flex items-center gap-1.5 mt-0.5">
                            <i class="${pm.icon} text-[10px]" style="color:${pm.color};"></i>
                            <span class="text-[10px]" style="color:#5f6680;">${t.platform}</span>
                            ${t.is_flagged ? '<i class="fas fa-flag text-[8px]" style="color:#f59e0b;"></i>' : ''}
                            ${unread ? `<span class="w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-bold text-white ml-auto" style="background:#6366f1;">${t.unread_count}</span>` : ''}
                        </div>
                        <p class="text-xs truncate mt-1" style="color:${unread ? '#c4c8d4' : '#5f6680'};">${t.last_message}</p>
                        ${t.category ? `<span class="inline-block mt-1.5 px-2 py-0.5 rounded text-[10px] font-medium" style="background:${catColor}15;color:${catColor};">${t.category}</span>` : ''}
                    </div>
                </div>
            </div>`;
        }).join('');
    },

    async openThread(threadId) {
        this._inboxActiveThread = threadId;
        this._renderThreadList(); // update active highlight
        const panel = document.getElementById('conversationPanel');
        if (!panel) return;
        panel.innerHTML = '<div class="flex-1 flex items-center justify-center"><i class="fas fa-spinner fa-spin text-lg" style="color:#818cf8;"></i></div>';

        try {
            const base = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            const r = await fetch(`${base}/api/v1/inbox/threads/${threadId}`);
            const d = await r.json();
            const thread = d?.data || {};
            const msgs = thread.messages || [];
            const pm = this._platformMeta[thread.platform] || this._platformMeta.email;
            const initials = (thread.customer_name || '??').split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();

            panel.innerHTML = `
                <!-- Header -->
                <div class="p-4" style="border-bottom:1px solid rgba(255,255,255,.05);">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold text-sm bg-gradient-to-br ${pm.gradient}">${initials}</div>
                            <div>
                                <p class="font-semibold text-sm" style="color:#e8eaed;">${thread.customer_name}</p>
                                <div class="flex items-center gap-2 mt-0.5">
                                    <i class="${pm.icon} text-[10px]" style="color:${pm.color};"></i>
                                    <span class="text-[10px]" style="color:#5f6680;">${thread.platform} • ${thread.customer_email || ''}</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex items-center gap-1">
                            <button class="w-7 h-7 rounded-lg flex items-center justify-center transition" style="color:#5f6680;" onmouseover="this.style.background='rgba(255,255,255,.05)'" onmouseout="this.style.background='transparent'" onclick="app.toggleThreadFlag('${threadId}')" title="Flag"><i class="fas fa-flag text-xs"></i></button>
                            <button class="w-7 h-7 rounded-lg flex items-center justify-center transition" style="color:#5f6680;" onmouseover="this.style.background='rgba(255,255,255,.05)'" onmouseout="this.style.background='transparent'" onclick="app.archiveThread('${threadId}')" title="Archive"><i class="fas fa-archive text-xs"></i></button>
                        </div>
                    </div>
                    ${thread.category ? `<div class="mt-2 flex items-center gap-2 px-2 py-1 rounded-lg" style="background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.1);"><i class="fas fa-tag text-[10px]" style="color:#818cf8;"></i><span class="text-[10px]" style="color:#818cf8;">Category: <strong>${thread.category}</strong></span></div>` : ''}
                </div>

                <!-- Messages -->
                <div class="flex-1 p-4 space-y-3 overflow-y-auto" id="messagesList" style="max-height:45vh;">
                    ${msgs.map(m => {
                        const isInbound = m.direction === 'inbound';
                        const time = new Date(m.sent_at).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
                        if (isInbound) {
                            return `<div class="flex gap-2.5">
                                <div class="w-7 h-7 rounded-full flex items-center justify-center text-white font-semibold text-[10px] flex-shrink-0 bg-gradient-to-br ${pm.gradient}">${initials}</div>
                                <div>
                                    <div class="px-3.5 py-2.5 rounded-2xl rounded-tl-none max-w-xs" style="background:#1a1f2e;">
                                        <p class="text-xs leading-relaxed" style="color:#c4c8d4;">${m.content}</p>
                                    </div>
                                    <span class="text-[10px] mt-0.5 block" style="color:#3a3f52;">${time}</span>
                                </div>
                            </div>`;
                        } else {
                            return `<div class="flex gap-2.5 justify-end">
                                <div>
                                    <div class="px-3.5 py-2.5 rounded-2xl rounded-tr-none max-w-xs" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);">
                                        <p class="text-xs leading-relaxed text-white">${m.content}</p>
                                    </div>
                                    <span class="text-[10px] mt-0.5 block text-right" style="color:#3a3f52;">${time}</span>
                                </div>
                            </div>`;
                        }
                    }).join('')}
                </div>

                <!-- Input -->
                <div class="p-3" style="border-top:1px solid rgba(255,255,255,.05);">
                    <div class="flex gap-2">
                        <input type="text" id="inboxReplyInput" placeholder="Type your reply..." class="flex-1 px-3 py-2.5 rounded-lg text-xs" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" onkeydown="if(event.key==='Enter')app.sendInboxReply('${threadId}')">
                        <button class="px-3 py-2 rounded-lg text-xs font-semibold" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;" onclick="app.sendInboxReply('${threadId}')"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>
            `;

            // Scroll to bottom
            const ml = document.getElementById('messagesList');
            if (ml) ml.scrollTop = ml.scrollHeight;

            // Load AI suggestions
            this._loadAiSuggestions(threadId);
            // Refresh stats (read status changed)
            this._loadInboxStats();
        } catch (e) {
            console.error('Open thread error', e);
            panel.innerHTML = '<div class="flex-1 flex items-center justify-center"><p class="text-xs" style="color:#f87171;">Failed to load conversation</p></div>';
        }
    },

    async sendInboxReply(threadId) {
        const input = document.getElementById('inboxReplyInput');
        if (!input) return;
        const content = input.value.trim();
        if (!content) return;
        input.value = '';

        try {
            const base = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            await fetch(`${base}/api/v1/inbox/threads/${threadId}/reply`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content }),
            });
            // Re-open thread to show new message
            await this.openThread(threadId);
            await this._loadInboxThreads(this._inboxFilter === 'all' ? undefined : this._inboxFilter);
            this.showToast('Reply sent!', 'success');
        } catch (e) {
            this.showToast('Failed to send reply', 'error');
        }
    },

    async _loadAiSuggestions(threadId) {
        const el = document.getElementById('aiSuggestions');
        if (!el) return;
        el.innerHTML = '<div class="p-3 text-center"><i class="fas fa-brain animate-pulse" style="color:#a78bfa;"></i><p class="text-[10px] mt-1" style="color:#5f6680;">AI generating suggestions...</p></div>';

        try {
            const base = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            const r = await fetch(`${base}/api/v1/inbox/threads/${threadId}/ai-suggest`, { method: 'POST' });
            const d = await r.json();
            const suggestions = d?.data?.suggestions || [];
            const toneIcons = { friendly: 'fa-smile', professional: 'fa-briefcase', empathetic: 'fa-heart' };
            const toneColors = { friendly: '#34d399', professional: '#818cf8', empathetic: '#f472b6' };

            el.innerHTML = `
                <div class="text-[10px] font-bold mb-2" style="color:#a78bfa;"><i class="fas fa-magic mr-1"></i>AI SUGGESTED REPLIES</div>
                <div class="space-y-2">
                    ${suggestions.map((s, i) => `
                        <div class="p-2.5 rounded-lg cursor-pointer transition" style="background:rgba(139,92,246,.04);border:1px solid rgba(139,92,246,.08);" onmouseover="this.style.borderColor='rgba(139,92,246,.25)'" onmouseout="this.style.borderColor='rgba(139,92,246,.08)'" onclick="document.getElementById('inboxReplyInput').value=this.querySelector('.suggestion-text').textContent;app.showToast('Suggestion applied!')">
                            <div class="flex items-center gap-1.5 mb-1">
                                <i class="fas ${toneIcons[s.tone] || 'fa-comment'} text-[10px]" style="color:${toneColors[s.tone] || '#818cf8'};"></i>
                                <span class="text-[10px] font-bold" style="color:${toneColors[s.tone] || '#818cf8'};">${(s.tone||'reply').toUpperCase()}</span>
                                <span class="ml-auto text-[8px] px-1.5 py-0.5 rounded-full" style="background:rgba(99,102,241,.1);color:#818cf8;">${Math.round((s.confidence||0.85)*100)}%</span>
                            </div>
                            <p class="suggestion-text text-[11px] leading-relaxed" style="color:#c4c8d4;">${s.reply}</p>
                            <button class="text-[10px] font-semibold mt-1.5" style="color:#818cf8;"><i class="fas fa-paper-plane mr-1"></i>Use this reply</button>
                        </div>
                    `).join('')}
                </div>
            `;
        } catch (e) {
            el.innerHTML = '<div class="p-2 text-[10px]" style="color:#5f6680;">AI suggestions unavailable</div>';
        }
    },

    /* ── Strategy calendar expand ── */
    expandCalendarRows() {
        const rows = document.querySelectorAll('.calendar-hidden-row');
        const btn = document.getElementById('calendarExpandBtn');
        if (!rows.length) return;
        const hidden = rows[0].style.display === 'none';
        rows.forEach(r => r.style.display = hidden ? '' : 'none');
        if (btn) {
            btn.innerHTML = hidden
                ? '<i class="fas fa-chevron-up mr-1"></i> Show less'
                : `<i class="fas fa-chevron-down mr-1"></i> + ${rows.length} more entries`;
        }
    },

    filterInbox(platform) {
        this._inboxFilter = platform;
        document.querySelectorAll('.inbox-filter-btn').forEach(b => {
            b.classList.remove('active');
            if (b.dataset.filter === platform) b.classList.add('active');
        });
        this._loadInboxThreads(platform === 'all' ? undefined : platform);
    },

    searchInbox(query) {
        clearTimeout(this._inboxSearchTimer);
        this._inboxSearchTimer = setTimeout(() => {
            const platform = this._inboxFilter === 'all' ? undefined : this._inboxFilter;
            this._loadInboxThreads(platform, query || undefined);
        }, 300);
    },

    async toggleThreadFlag(threadId) {
        try {
            const base = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            const thread = this._inboxThreads.find(t => t.thread_id === threadId);
            await fetch(`${base}/api/v1/inbox/threads/${threadId}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ is_flagged: !(thread?.is_flagged) }),
            });
            await this._loadInboxThreads(this._inboxFilter === 'all' ? undefined : this._inboxFilter);
            this.showToast('Thread updated');
        } catch (e) { this.showToast('Update failed', 'error'); }
    },

    async archiveThread(threadId) {
        try {
            const base = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            await fetch(`${base}/api/v1/inbox/threads/${threadId}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ is_archived: true }),
            });
            this._inboxActiveThread = null;
            document.getElementById('conversationPanel').innerHTML = '<div class="flex-1 flex items-center justify-center p-8"><div class="text-center"><i class="fas fa-archive text-3xl mb-2" style="color:#34d399;"></i><p class="text-sm" style="color:#5f6680;">Thread archived</p></div></div>';
            await this._loadInboxThreads(this._inboxFilter === 'all' ? undefined : this._inboxFilter);
            await this._loadInboxStats();
            this.showToast('Conversation archived');
        } catch (e) { this.showToast('Archive failed', 'error'); }
    },

    _timeAgo(iso) {
        if (!iso) return '';
        const diff = (Date.now() - new Date(iso).getTime()) / 1000;
        if (diff < 60) return 'just now';
        if (diff < 3600) return `${Math.floor(diff/60)}m`;
        if (diff < 86400) return `${Math.floor(diff/3600)}h`;
        return `${Math.floor(diff/86400)}d`;
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // AuthManager already handles authentication redirects in its init() method
    // Just initialize the app if we reach this point
    app.init();
    app.updateUserProfile();
});
