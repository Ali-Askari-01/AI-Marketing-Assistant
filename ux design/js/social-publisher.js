/**
 * Social Publisher + AI Caption Engine
 * ═══════════════════════════════════════════════════════
 * Integrates Facebook Pages, Instagram Business, and Email
 * via Meta App "Softwa Desig" (ID 122100895335285764)
 *
 * Also provides AI-powered caption generation with trending
 * hashtags, engagement tips, and multi-style variations.
 */

const SocialPublisher = {
    // ── State ──────────────────────────────────────────────────────
    connected: false,
    accounts: { pages: [], instagram_accounts: [] },
    baseUrl: (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8003',
    _panelInjected: false,

    // ── Theme tokens ───────────────────────────────────────────────
    colors: {
        bg: '#0a0e17', card: '#131825', cardAlt: '#0f1321',
        border: 'rgba(255,255,255,0.06)',
        primary: '#6366f1', accent: '#06b6d4',
        text: '#e8eaed', muted: '#9aa0b0', dim: '#5f6680',
        fb: '#1877F2', ig: '#E4405F', email: '#8b5cf6',
    },

    // ═══════════════════════════════════════════════════════════════
    // INIT — called once on DOM ready
    // ═══════════════════════════════════════════════════════════════
    init() {
        this.checkConnection();
        // Listen for OAuth popup callback
        window.addEventListener('message', (e) => {
            if (e.data && e.data.success !== undefined) {
                this._handleOAuthResult(e.data);
            }
        });
    },

    // ═══════════════════════════════════════════════════════════════
    // CONNECTION — Meta/Facebook OAuth
    // ═══════════════════════════════════════════════════════════════
    async checkConnection() {
        try {
            const res = await fetch(`${this.baseUrl}/api/v1/social/accounts`);
            const data = await res.json();
            if (data.success && data.data) {
                this.connected = data.data.connected || false;
                this.accounts = data.data;
                this._updateConnectUI();
            }
        } catch (e) {
            console.warn('[SocialPublisher] Connection check failed:', e);
        }
    },

    async connectMeta() {
        try {
            const res = await fetch(`${this.baseUrl}/api/v1/social/meta/oauth-url`);
            const data = await res.json();
            if (data.success && data.data?.oauth_url) {
                // Open OAuth popup
                const w = 600, h = 700;
                const left = (screen.width - w) / 2;
                const top = (screen.height - h) / 2;
                window.open(data.data.oauth_url, 'meta_oauth',
                    `width=${w},height=${h},left=${left},top=${top},toolbar=no,menubar=no`);
                if (window.app) window.app.showToast('Connecting to Facebook & Instagram...', 'info');
            }
        } catch (e) {
            console.error('[SocialPublisher] OAuth URL fetch failed:', e);
            if (window.app) window.app.showToast('Failed to start connection', 'error');
        }
    },

    _handleOAuthResult(result) {
        if (result.success) {
            this.connected = true;
            this.accounts = {
                pages: result.pages || [],
                instagram_accounts: result.instagram_accounts || [],
            };
            this._updateConnectUI();
            if (window.app) window.app.showToast('Facebook & Instagram connected!', 'success');
        } else {
            if (window.app) window.app.showToast('Connection failed: ' + (result.error || 'Unknown'), 'error');
        }
    },

    async disconnect() {
        try {
            await fetch(`${this.baseUrl}/api/v1/social/disconnect`, { method: 'POST' });
            this.connected = false;
            this.accounts = { pages: [], instagram_accounts: [] };
            this._updateConnectUI();
            if (window.app) window.app.showToast('Accounts disconnected', 'info');
        } catch (e) { console.error(e); }
    },

    // ═══════════════════════════════════════════════════════════════
    // PUBLISH — Post to FB / IG / Email
    // ═══════════════════════════════════════════════════════════════
    async publish(platform, options = {}) {
        const caption = options.caption || document.getElementById('captionText')?.value || '';
        if (!caption.trim()) {
            if (window.app) window.app.showToast('Please enter content first', 'error');
            return;
        }

        if (window.app) window.app.showLoading?.();
        try {
            const body = {
                platform,
                message: caption,
                caption: caption,
                image_url: options.image_url || '',
                link: options.link || '',
                page_id: options.page_id || '',
                ig_account_id: options.ig_account_id || '',
                to_email: options.to_email || '',
                subject: options.subject || 'Check this out!',
            };

            const res = await fetch(`${this.baseUrl}/api/v1/social/publish`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            const data = await res.json();

            if (window.app) window.app.hideLoading?.();
            if (data.success && data.data?.published) {
                if (window.app) window.app.showToast(`Published to ${platform}!`, 'success');
                return data.data;
            } else {
                const errMsg = data.data?.results?.[0]?.error || 'Publish failed';
                if (window.app) window.app.showToast(errMsg, 'error');
                return data.data;
            }
        } catch (e) {
            if (window.app) { window.app.hideLoading?.(); window.app.showToast('Publish error: ' + e.message, 'error'); }
        }
    },

    async sendEmail(to, subject, body) {
        try {
            const res = await fetch(`${this.baseUrl}/api/v1/social/email`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ to_email: to, subject, body }),
            });
            const data = await res.json();
            if (data.data?.method === 'mailto') {
                // Open mailto link in new tab
                window.open(data.data.mailto_link, '_blank');
                if (window.app) window.app.showToast('Opening email client...', 'info');
            } else if (data.data?.success) {
                if (window.app) window.app.showToast('Email sent!', 'success');
            }
            return data.data;
        } catch (e) {
            if (window.app) window.app.showToast('Email failed', 'error');
        }
    },

    // ═══════════════════════════════════════════════════════════════
    // AI CAPTIONS — Trend-Aware Generation
    // ═══════════════════════════════════════════════════════════════
    async generateCaptions(content, options = {}) {
        if (!content?.trim()) {
            if (window.app) window.app.showToast('Enter content or describe your post first', 'error');
            return null;
        }

        try {
            const res = await fetch(`${this.baseUrl}/api/v1/ai/generate-captions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content,
                    platforms: options.platforms || ['instagram', 'facebook'],
                    tone: options.tone || 'engaging',
                    niche: options.niche || 'general marketing',
                    image_description: options.image_description || '',
                }),
            });
            const data = await res.json();
            return data.data || null;
        } catch (e) {
            console.error('[SocialPublisher] Caption generation failed:', e);
            return null;
        }
    },

    async optimizeHashtags(content, options = {}) {
        try {
            const res = await fetch(`${this.baseUrl}/api/v1/ai/optimize-hashtags`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content,
                    platform: options.platform || 'instagram',
                    niche: options.niche || 'general marketing',
                    count: options.count || 15,
                }),
            });
            const data = await res.json();
            return data.data || null;
        } catch (e) { return null; }
    },

    async analyzePost(content, platform = 'instagram') {
        try {
            const res = await fetch(`${this.baseUrl}/api/v1/ai/analyze-post`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content, platform }),
            });
            const data = await res.json();
            return data.data || null;
        } catch (e) { return null; }
    },

    // ═══════════════════════════════════════════════════════════════
    // UI — Inject Publish Panel into Content Studio
    // ═══════════════════════════════════════════════════════════════
    injectPublishPanel() {
        if (this._panelInjected) return;
        const col = document.querySelector('#contentFormContainer')?.closest('.lg\\:col-span-6');
        if (!col) return;

        const panel = document.createElement('div');
        panel.id = 'socialPublishPanel';
        panel.className = 'mt-4 rounded-xl p-4';
        panel.style.cssText = `background:${this.colors.card}; border:1px solid ${this.colors.border};`;
        panel.innerHTML = this._publishPanelHTML();
        col.appendChild(panel);
        this._panelInjected = true;
    },

    _publishPanelHTML() {
        const c = this.colors;
        return `
        <!-- Connect / Publish Section -->
        <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-bold flex items-center gap-2" style="color:${c.text};">
                <i class="fas fa-share-alt" style="color:${c.primary};"></i> Publish & Share
            </h3>
            <div id="socialConnectStatus" class="text-[10px] font-medium px-2 py-0.5 rounded-full"
                 style="background:${this.connected ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)'}; color:${this.connected ? '#10b981' : '#ef4444'};">
                ${this.connected ? '● Connected' : '○ Not connected'}
            </div>
        </div>

        <!-- Account Connection -->
        <div id="socialConnectSection" class="mb-4">
            ${this.connected ? this._connectedAccountsHTML() : `
            <button onclick="SocialPublisher.connectMeta()" class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-semibold text-white transition hover:opacity-90"
                    style="background:linear-gradient(135deg, ${c.fb}, ${c.ig});">
                <i class="fab fa-facebook"></i> <i class="fab fa-instagram"></i>
                Connect Facebook & Instagram
            </button>
            <p class="text-[10px] mt-1.5 text-center" style="color:${c.dim};">
                Connect via Meta to publish directly to your pages
            </p>`}
        </div>

        <!-- Publish Buttons -->
        <div class="grid grid-cols-3 gap-2 mb-3">
            <button onclick="SocialPublisher._publishFromUI('facebook')" class="flex flex-col items-center gap-1 py-2.5 rounded-lg text-xs font-medium transition hover:opacity-90"
                    style="background:rgba(24,119,242,0.12); color:${c.fb}; border:1px solid rgba(24,119,242,0.25);">
                <i class="fab fa-facebook text-base"></i> Facebook
            </button>
            <button onclick="SocialPublisher._publishFromUI('instagram')" class="flex flex-col items-center gap-1 py-2.5 rounded-lg text-xs font-medium transition hover:opacity-90"
                    style="background:rgba(228,64,95,0.12); color:${c.ig}; border:1px solid rgba(228,64,95,0.25);">
                <i class="fab fa-instagram text-base"></i> Instagram
            </button>
            <button onclick="SocialPublisher._showEmailModal()" class="flex flex-col items-center gap-1 py-2.5 rounded-lg text-xs font-medium transition hover:opacity-90"
                    style="background:rgba(139,92,246,0.12); color:${c.email}; border:1px solid rgba(139,92,246,0.25);">
                <i class="fas fa-envelope text-base"></i> Email
            </button>
        </div>

        <!-- AI Caption Generator -->
        <div class="pt-3" style="border-top:1px solid ${c.border};">
            <div class="flex items-center justify-between mb-2">
                <h4 class="text-xs font-bold flex items-center gap-1.5" style="color:${c.text};">
                    <i class="fas fa-sparkles" style="color:${c.accent};"></i> AI Caption Generator
                </h4>
                <span id="captionSource" class="text-[9px] px-1.5 py-0.5 rounded" style="background:rgba(99,102,241,0.15); color:${c.primary}; display:none;"></span>
            </div>

            <!-- Niche / Tone selectors -->
            <div class="grid grid-cols-2 gap-2 mb-2">
                <select id="captionNiche" class="text-[11px] py-1.5 px-2 rounded-lg" style="background:${c.cardAlt}; color:${c.text}; border:1px solid ${c.border};">
                    <option value="general marketing">General Marketing</option>
                    <option value="technology">Technology</option>
                    <option value="fashion">Fashion</option>
                    <option value="food">Food & Beverage</option>
                    <option value="fitness">Fitness</option>
                    <option value="business">Business</option>
                </select>
                <select id="captionTone" class="text-[11px] py-1.5 px-2 rounded-lg" style="background:${c.cardAlt}; color:${c.text}; border:1px solid ${c.border};">
                    <option value="engaging">Engaging</option>
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                    <option value="funny">Funny</option>
                    <option value="inspiring">Inspiring</option>
                    <option value="educational">Educational</option>
                </select>
            </div>

            <button onclick="SocialPublisher._generateFromUI()" id="aiCaptionBtn"
                    class="w-full flex items-center justify-center gap-2 py-2 rounded-lg text-xs font-semibold transition hover:opacity-90"
                    style="background:linear-gradient(135deg, ${c.primary}, ${c.accent}); color:#fff;">
                <i class="fas fa-wand-magic-sparkles"></i> Generate AI Captions & Hashtags
            </button>

            <!-- Results container -->
            <div id="aiCaptionResults" class="mt-3 hidden space-y-2"></div>
        </div>
        `;
    },

    _connectedAccountsHTML() {
        const c = this.colors;
        const pages = this.accounts.pages || [];
        const igs = this.accounts.instagram_accounts || [];
        let html = '<div class="space-y-1.5">';

        pages.forEach(p => {
            html += `<div class="flex items-center gap-2 py-1.5 px-2 rounded-lg" style="background:rgba(24,119,242,0.08);">
                <i class="fab fa-facebook" style="color:${c.fb};"></i>
                <span class="text-xs font-medium" style="color:${c.text};">${p.name}</span>
                <span class="text-[9px] ml-auto" style="color:${c.dim};">Page</span>
            </div>`;
        });
        igs.forEach(ig => {
            html += `<div class="flex items-center gap-2 py-1.5 px-2 rounded-lg" style="background:rgba(228,64,95,0.08);">
                <i class="fab fa-instagram" style="color:${c.ig};"></i>
                <span class="text-xs font-medium" style="color:${c.text};">@${ig.username || ig.id}</span>
                <span class="text-[9px] ml-auto" style="color:${c.dim};">Business</span>
            </div>`;
        });

        if (!pages.length && !igs.length) {
            html += `<p class="text-[10px] text-center py-2" style="color:${c.dim};">Connected but no pages found. Check Meta settings.</p>`;
        }

        html += `<button onclick="SocialPublisher.disconnect()" class="w-full text-[10px] text-center py-1 mt-1 rounded" style="color:#ef4444; background:rgba(239,68,68,0.08);">
            <i class="fas fa-unlink mr-1"></i> Disconnect
        </button></div>`;
        return html;
    },

    _updateConnectUI() {
        const status = document.getElementById('socialConnectStatus');
        const section = document.getElementById('socialConnectSection');
        if (status) {
            status.style.background = this.connected ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)';
            status.style.color = this.connected ? '#10b981' : '#ef4444';
            status.textContent = this.connected ? '● Connected' : '○ Not connected';
        }
        if (section) {
            section.innerHTML = this.connected ? this._connectedAccountsHTML() : `
                <button onclick="SocialPublisher.connectMeta()" class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-semibold text-white transition hover:opacity-90"
                        style="background:linear-gradient(135deg, ${this.colors.fb}, ${this.colors.ig});">
                    <i class="fab fa-facebook"></i> <i class="fab fa-instagram"></i>
                    Connect Facebook & Instagram
                </button>`;
        }
    },

    // ═══════════════════════════════════════════════════════════════
    // UI ACTIONS — triggered by buttons
    // ═══════════════════════════════════════════════════════════════
    _publishFromUI(platform) {
        if (!this.connected && platform !== 'email') {
            if (window.app) window.app.showToast('Please connect your account first', 'error');
            this.connectMeta();
            return;
        }
        const caption = document.getElementById('captionText')?.value || '';
        // For IG, we need an image — prompt user
        if (platform === 'instagram') {
            this._showImagePrompt(caption);
            return;
        }
        this.publish(platform, { caption });
    },

    _showImagePrompt(caption) {
        const c = this.colors;
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 z-[9999] flex items-center justify-center p-4';
        modal.style.background = 'rgba(0,0,0,0.7)';
        modal.innerHTML = `
            <div class="rounded-xl p-5 max-w-md w-full" style="background:${c.card}; border:1px solid ${c.border};">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-bold" style="color:${c.text};">
                        <i class="fab fa-instagram mr-1" style="color:${c.ig};"></i> Instagram Post
                    </h3>
                    <button onclick="this.closest('.fixed').remove()" style="color:${c.dim};"><i class="fas fa-times"></i></button>
                </div>
                <p class="text-xs mb-3" style="color:${c.muted};">Instagram requires a public image URL:</p>
                <input type="url" id="igImageUrl" placeholder="https://example.com/image.jpg"
                       class="w-full px-3 py-2 rounded-lg text-sm mb-3"
                       style="background:${c.cardAlt}; color:${c.text}; border:1px solid ${c.border};">
                <div class="flex gap-2">
                    <button onclick="this.closest('.fixed').remove()" class="flex-1 py-2 rounded-lg text-xs font-medium"
                            style="background:${c.cardAlt}; color:${c.muted};">Cancel</button>
                    <button onclick="SocialPublisher._publishIG()" class="flex-1 py-2 rounded-lg text-xs font-semibold text-white"
                            style="background:${c.ig};">Publish</button>
                </div>
            </div>`;
        document.body.appendChild(modal);
    },

    _publishIG() {
        const url = document.getElementById('igImageUrl')?.value || '';
        const caption = document.getElementById('captionText')?.value || '';
        document.querySelector('.fixed.inset-0.z-\\[9999\\]')?.remove();
        if (!url) {
            if (window.app) window.app.showToast('Image URL is required for Instagram', 'error');
            return;
        }
        this.publish('instagram', { caption, image_url: url });
    },

    _showEmailModal() {
        const c = this.colors;
        const caption = document.getElementById('captionText')?.value || '';
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 z-[9999] flex items-center justify-center p-4';
        modal.style.background = 'rgba(0,0,0,0.7)';
        modal.innerHTML = `
            <div class="rounded-xl p-5 max-w-md w-full" style="background:${c.card}; border:1px solid ${c.border};">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-bold" style="color:${c.text};">
                        <i class="fas fa-envelope mr-1" style="color:${c.email};"></i> Share via Email
                    </h3>
                    <button onclick="this.closest('.fixed').remove()" style="color:${c.dim};"><i class="fas fa-times"></i></button>
                </div>
                <div class="space-y-3">
                    <div>
                        <label class="block text-[10px] font-semibold mb-1" style="color:${c.muted};">Recipient Email</label>
                        <input type="email" id="emailTo" placeholder="recipient@example.com"
                               class="w-full px-3 py-2 rounded-lg text-sm"
                               style="background:${c.cardAlt}; color:${c.text}; border:1px solid ${c.border};">
                    </div>
                    <div>
                        <label class="block text-[10px] font-semibold mb-1" style="color:${c.muted};">Subject</label>
                        <input type="text" id="emailSubjectLine" value="Check out this content!"
                               class="w-full px-3 py-2 rounded-lg text-sm"
                               style="background:${c.cardAlt}; color:${c.text}; border:1px solid ${c.border};">
                    </div>
                    <div>
                        <label class="block text-[10px] font-semibold mb-1" style="color:${c.muted};">Message</label>
                        <textarea id="emailBody" rows="4" class="w-full px-3 py-2 rounded-lg text-sm"
                                  style="background:${c.cardAlt}; color:${c.text}; border:1px solid ${c.border};">${caption}</textarea>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="this.closest('.fixed').remove()" class="flex-1 py-2 rounded-lg text-xs font-medium"
                                style="background:${c.cardAlt}; color:${c.muted};">Cancel</button>
                        <button onclick="SocialPublisher._sendEmailFromModal()" class="flex-1 py-2 rounded-lg text-xs font-semibold text-white"
                                style="background:${c.email};">Send Email</button>
                    </div>
                </div>
            </div>`;
        document.body.appendChild(modal);
    },

    _sendEmailFromModal() {
        const to = document.getElementById('emailTo')?.value;
        const subject = document.getElementById('emailSubjectLine')?.value;
        const body = document.getElementById('emailBody')?.value;
        document.querySelector('.fixed.inset-0.z-\\[9999\\]')?.remove();
        if (!to) {
            if (window.app) window.app.showToast('Please enter recipient email', 'error');
            return;
        }
        this.sendEmail(to, subject, body);
    },

    // ═══════════════════════════════════════════════════════════════
    // AI CAPTION UI — Generate & Display
    // ═══════════════════════════════════════════════════════════════
    async _generateFromUI() {
        const content = document.getElementById('captionText')?.value || '';
        const niche = document.getElementById('captionNiche')?.value || 'general marketing';
        const tone = document.getElementById('captionTone')?.value || 'engaging';
        const btn = document.getElementById('aiCaptionBtn');
        const results = document.getElementById('aiCaptionResults');
        if (!results) return;

        if (!content.trim()) {
            if (window.app) window.app.showToast('Enter content or a topic to generate captions', 'error');
            return;
        }

        // Loading state
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating with AI...';
        }
        results.classList.remove('hidden');
        results.innerHTML = `<div class="text-center py-4"><i class="fas fa-spinner fa-spin text-lg" style="color:${this.colors.accent};"></i><p class="text-[10px] mt-2" style="color:${this.colors.muted};">AI is analyzing trends & generating captions...</p></div>`;

        const data = await this.generateCaptions(content, {
            platforms: ['instagram', 'facebook'],
            tone, niche,
        });

        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Generate AI Captions & Hashtags';
        }

        if (!data) {
            results.innerHTML = `<p class="text-xs text-center py-2" style="color:#ef4444;">Generation failed. Try again.</p>`;
            return;
        }

        // Show source badge
        const srcEl = document.getElementById('captionSource');
        if (srcEl) {
            srcEl.textContent = data.source === 'gemini' ? '✦ Gemini AI' : '⚙ Rules Engine';
            srcEl.style.display = 'inline-block';
        }

        this._renderCaptionResults(data, results);
    },

    _renderCaptionResults(data, container) {
        const c = this.colors;
        const captions = data.captions || [];
        const hashtags = data.hashtags || [];
        const tips = data.engagement_tips || [];
        const insight = data.content_insight || '';
        const bestTime = data.best_posting_time || '';
        const hooks = data.trending_hooks || [];

        let html = '';

        // Caption variations
        const styleIcons = { formal: 'fa-briefcase', casual: 'fa-mug-hot', viral: 'fa-fire' };
        const styleColors = { formal: c.primary, casual: c.accent, viral: '#f59e0b' };

        captions.forEach((cap, i) => {
            const icon = styleIcons[cap.style] || 'fa-pen';
            const color = styleColors[cap.style] || c.primary;
            html += `
            <div class="rounded-lg p-3 cursor-pointer transition hover:opacity-80" style="background:${c.cardAlt}; border:1px solid ${c.border};"
                 onclick="SocialPublisher._useCaption(${i})">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold uppercase flex items-center gap-1" style="color:${color};">
                        <i class="fas ${icon}"></i> ${cap.style}
                    </span>
                    <button class="text-[9px] px-1.5 py-0.5 rounded font-medium" style="background:rgba(99,102,241,0.15); color:${c.primary};"
                            onclick="event.stopPropagation(); SocialPublisher._useCaption(${i})">
                        <i class="fas fa-check mr-0.5"></i> Use
                    </button>
                </div>
                <p class="text-[11px] leading-relaxed whitespace-pre-line" style="color:${c.text};" id="aiCaption_${i}">${this._escapeHtml(cap.text)}</p>
            </div>`;
        });

        // Hashtags
        if (hashtags.length) {
            html += `<div class="rounded-lg p-3" style="background:${c.cardAlt}; border:1px solid ${c.border};">
                <div class="flex items-center justify-between mb-1.5">
                    <span class="text-[10px] font-bold" style="color:${c.accent};"><i class="fas fa-hashtag mr-1"></i> TRENDING HASHTAGS</span>
                    <button class="text-[9px] px-1.5 py-0.5 rounded font-medium" style="background:rgba(6,182,212,0.15); color:${c.accent};"
                            onclick="SocialPublisher._copyHashtags()">
                        <i class="fas fa-copy mr-0.5"></i> Copy All
                    </button>
                </div>
                <div class="flex flex-wrap gap-1" id="aiHashtagsContainer">
                    ${hashtags.map(t => `<span class="px-2 py-0.5 rounded-full text-[10px] font-medium" style="background:rgba(6,182,212,0.1); color:${c.accent};">${t}</span>`).join('')}
                </div>
            </div>`;
        }

        // Engagement Tips + Insight
        if (tips.length || insight) {
            html += `<div class="rounded-lg p-3" style="background:${c.cardAlt}; border:1px solid ${c.border};">
                <span class="text-[10px] font-bold" style="color:#10b981;"><i class="fas fa-lightbulb mr-1"></i> INSIGHTS</span>`;
            if (insight) {
                html += `<p class="text-[11px] mt-1 mb-1.5" style="color:${c.text};">${this._escapeHtml(insight)}</p>`;
            }
            if (bestTime) {
                html += `<p class="text-[10px] mb-1" style="color:${c.muted};"><i class="fas fa-clock mr-1"></i> Best time: <strong style="color:${c.text};">${bestTime}</strong></p>`;
            }
            tips.forEach(tip => {
                html += `<p class="text-[10px] flex items-start gap-1 mt-1" style="color:${c.muted};"><i class="fas fa-check-circle mt-0.5" style="color:#10b981;"></i> ${this._escapeHtml(tip)}</p>`;
            });
            html += `</div>`;
        }

        // Trending Hooks
        if (hooks.length) {
            html += `<div class="rounded-lg p-3" style="background:${c.cardAlt}; border:1px solid ${c.border};">
                <span class="text-[10px] font-bold" style="color:#f59e0b;"><i class="fas fa-bolt mr-1"></i> TRENDING HOOKS</span>
                <div class="mt-1.5 space-y-1">
                    ${hooks.map(h => `<p class="text-[10px] cursor-pointer hover:underline" style="color:${c.text};" onclick="SocialPublisher._insertHook(this)">${this._escapeHtml(h)}</p>`).join('')}
                </div>
            </div>`;
        }

        container.innerHTML = html;
        this._lastCaptions = data;
    },

    _useCaption(index) {
        const el = document.getElementById(`aiCaption_${index}`);
        if (!el) return;
        const field = document.getElementById('captionText');
        if (field) {
            field.value = el.textContent;
            if (window.app) window.app.showToast('Caption applied!', 'success');
        }
        // Also update hashtags in ContentStudio if available
        if (this._lastCaptions?.hashtags && window.ContentStudio) {
            ContentStudio.updateHashtagsUI(this._lastCaptions.hashtags);
        }
    },

    _copyHashtags() {
        const tags = this._lastCaptions?.hashtags || [];
        if (!tags.length) return;
        const text = tags.join(' ');
        navigator.clipboard?.writeText(text).then(() => {
            if (window.app) window.app.showToast('Hashtags copied!', 'success');
        }).catch(() => {
            // Fallback: select text
            const field = document.getElementById('captionText');
            if (field) {
                const current = field.value;
                field.value = current + '\n\n' + text;
                if (window.app) window.app.showToast('Hashtags appended to caption', 'success');
            }
        });
    },

    _insertHook(el) {
        const hook = el?.textContent || '';
        const field = document.getElementById('captionText');
        if (field && hook) {
            field.value = hook + '\n\n' + field.value;
            if (window.app) window.app.showToast('Hook inserted at top!', 'success');
        }
    },

    _escapeHtml(str) {
        const d = document.createElement('div');
        d.textContent = str;
        return d.innerHTML;
    },

    _lastCaptions: null,
};

// ── Auto-init ──────────────────────────────────────────────────────────
window.SocialPublisher = SocialPublisher;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => SocialPublisher.init());
} else {
    SocialPublisher.init();
}
