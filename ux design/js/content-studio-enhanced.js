/**
 * Enhanced Content Studio Module
 * Simplified: Social Captions, Email Drafts, SMS Text, Post Ideas
 */

const ContentStudio = {
    currentContent: {
        id: null,
        platform: 'instagram',
        contentType: 'caption',
        title: '',
        caption: '',
        media: null,
        hashtags: [],
        scheduledTime: null,
        status: 'draft'
    },

    savedDrafts: [],
    publishedPosts: [],

    init() {
        this.loadSavedContent();
        this.setupEventListeners();
    },

    loadSavedContent() {
        this.savedDrafts = JSON.parse(localStorage.getItem('contentDrafts') || '[]');
        this.publishedPosts = JSON.parse(localStorage.getItem('publishedPosts') || '[]');
    },

    setupEventListeners() {
        console.log('Content Studio ready – Caption / Email / SMS / Post Ideas');
    },

    /* ─── VOICE INPUT (browser Speech Recognition) ──────────────── */
    _recognition: null,
    startVoiceInput() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            if (window.app) window.app.showToast('Speech recognition not supported in this browser. Use Chrome.', 'error');
            return;
        }
        const btn = document.getElementById('voiceInputBtn');
        const status = document.getElementById('voiceInputStatus');

        if (this._recognition) {
            this._recognition.stop();
            this._recognition = null;
            if (btn) { btn.classList.remove('bg-red-500', 'text-white'); btn.classList.add('bg-red-50', 'text-red-600'); }
            if (status) status.classList.add('hidden');
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        this._recognition = recognition;

        if (btn) { btn.classList.remove('bg-red-50', 'text-red-600'); btn.classList.add('bg-red-500', 'text-white'); }
        if (status) status.classList.remove('hidden');

        let finalTranscript = '';
        recognition.onresult = (e) => {
            let interim = '';
            for (let i = e.resultIndex; i < e.results.length; i++) {
                if (e.results[i].isFinal) finalTranscript += e.results[i][0].transcript + ' ';
                else interim += e.results[i][0].transcript;
            }
            const field = document.getElementById('captionText');
            if (field) field.value = finalTranscript + interim;
        };
        recognition.onerror = () => {
            this._recognition = null;
            if (btn) { btn.classList.remove('bg-red-500', 'text-white'); btn.classList.add('bg-red-50', 'text-red-600'); }
            if (status) status.classList.add('hidden');
            if (window.app) window.app.showToast('Voice input stopped', 'info');
        };
        recognition.onend = () => {
            this._recognition = null;
            if (btn) { btn.classList.remove('bg-red-500', 'text-white'); btn.classList.add('bg-red-50', 'text-red-600'); }
            if (status) status.classList.add('hidden');
        };
        recognition.start();
        if (window.app) window.app.showToast('Listening... Speak now!', 'success');
    },

    /* ─── FILE IMPORT (.txt, .md, .csv) ─────────────────────────── */
    handleFileImport(input) {
        const file = input.files && input.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            const field = document.getElementById('captionText');
            if (field) field.value = e.target.result;
            if (window.app) window.app.showToast(`Imported "${file.name}"`, 'success');
        };
        reader.readAsText(file);
        input.value = '';
    },

    /* ─── AUDIO FILE IMPORT (upload → AssemblyAI transcribe) ────── */
    async handleAudioImport(input) {
        const file = input.files && input.files[0];
        if (!file) return;

        const field = document.getElementById('captionText');
        if (field) field.value = '⏳ Transcribing audio...';
        if (window.app) window.app.showLoading();

        try {
            const formData = new FormData();
            formData.append('file', file);
            const baseUrl = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';
            const resp = await fetch(`${baseUrl}/api/v1/ai/voice-to-campaign`, { method: 'POST', body: formData });
            if (!resp.ok) throw new Error('Transcription failed');
            const result = await resp.json();
            const transcript = result.data?.transcript || result.data?.text || '';
            if (field) field.value = transcript;
            if (window.app) { window.app.hideLoading(); window.app.showToast('Audio transcribed!', 'success'); }
        } catch (err) {
            if (field) field.value = '';
            if (window.app) { window.app.hideLoading(); window.app.showToast('Audio transcription failed: ' + err.message, 'error'); }
        }
        input.value = '';
    },

    /* ─── TTS: Read AI content aloud ────────────────────────────── */
    speakText(text) {
        if (!text) return;
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.rate = 1.0;
        utter.pitch = 1.0;
        window.speechSynthesis.speak(utter);
        if (window.app) window.app.showToast('Playing audio...', 'info');
    },

    /* ─── INPUT TOOLBAR HTML (reusable for all forms) ────────── */
    _inputToolbar() {
        return `
            <div class="flex items-center gap-2 mb-2 p-2.5 rounded-lg" style="background:#0d1220;border:1px solid rgba(255,255,255,.06);">
                <button class="flex items-center gap-1 px-2.5 py-1.5 text-[11px] font-medium rounded-lg transition" style="background:rgba(239,68,68,.1);color:#f87171;border:1px solid rgba(239,68,68,.2);" onclick="ContentStudio.startVoiceInput()" id="voiceInputBtn" title="Speak your content">
                    <i class="fas fa-microphone"></i> <span class="hidden sm:inline">Voice</span>
                </button>
                <button class="flex items-center gap-1 px-2.5 py-1.5 text-[11px] font-medium rounded-lg transition" style="background:rgba(59,130,246,.1);color:#60a5fa;border:1px solid rgba(59,130,246,.2);" onclick="document.getElementById('importFileInput').click()" title="Import text file">
                    <i class="fas fa-file-import"></i> <span class="hidden sm:inline">Import</span>
                </button>
                <button class="flex items-center gap-1 px-2.5 py-1.5 text-[11px] font-medium rounded-lg transition" style="background:rgba(139,92,246,.1);color:#a78bfa;border:1px solid rgba(139,92,246,.2);" onclick="document.getElementById('importAudioInput').click()" title="Upload audio file to transcribe">
                    <i class="fas fa-file-audio"></i> <span class="hidden sm:inline">Audio</span>
                </button>
                <input type="file" id="importFileInput" accept=".txt,.md,.csv,.doc,.docx" class="hidden" onchange="ContentStudio.handleFileImport(this)">
                <input type="file" id="importAudioInput" accept="audio/*" class="hidden" onchange="ContentStudio.handleAudioImport(this)">
                <div id="voiceInputStatus" class="ml-auto text-[10px] hidden" style="color:#5f6680;">
                    <i class="fas fa-circle text-red-500 animate-pulse"></i> Listening...
                </div>
            </div>`;
    },

    /* ─── AI ANALYZE PANEL (shown below textarea) ──────────────── */
    _aiAnalyzePanel() {
        return `
            <div class="mt-4 mb-4 p-4 rounded-xl" style="background:linear-gradient(135deg,rgba(99,102,241,.06),rgba(6,182,212,.04));border:1px solid rgba(99,102,241,.12);">
                <div class="flex items-center gap-2 mb-3">
                    <div class="w-7 h-7 rounded-lg flex items-center justify-center" style="background:linear-gradient(135deg,#6366f1,#06b6d4);">
                        <i class="fas fa-brain text-white text-xs"></i>
                    </div>
                    <span class="text-sm font-bold" style="color:#e8eaed;">AI Content Analyzer</span>
                    <span class="text-[10px] px-2 py-0.5 rounded-full" style="background:rgba(16,185,129,.1);color:#34d399;border:1px solid rgba(16,185,129,.2);">Trend-Aware</span>
                </div>
                <p class="text-xs mb-3" style="color:#9aa0b0;">Enter your project details above (text, voice, or file), then let AI generate captions, hashtags, insights & upload recommendations.</p>
                <div class="flex flex-wrap gap-2">
                    <button class="flex items-center gap-1.5 px-3.5 py-2.5 text-xs font-semibold rounded-lg transition" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;box-shadow:0 2px 12px rgba(99,102,241,.3);" onclick="ContentStudio.aiAnalyzeAndGenerate()">
                        <i class="fas fa-magic"></i> AI Analyze & Generate
                    </button>
                    <button class="flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg transition" style="background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.2);" onclick="ContentStudio.optimizeHashtags()">
                        <i class="fas fa-hashtag"></i> Optimize Hashtags
                    </button>
                    <button class="flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg transition" style="background:rgba(245,158,11,.1);color:#fbbf24;border:1px solid rgba(245,158,11,.2);" onclick="ContentStudio.analyzeContentWithAI()">
                        <i class="fas fa-chart-bar"></i> Score & Insights
                    </button>
                </div>
                <div id="aiAnalyzeResults" class="mt-3"></div>
            </div>`;
    },

    /**
     * Switch content type and update form
     */
    switchContentType(type) {
        this.currentContent.contentType = type;

        document.querySelectorAll('.content-type-btn').forEach(btn => {
            btn.style.background = 'transparent';
            btn.style.color = '#9aa0b0';
            btn.style.boxShadow = 'none';

            if (btn.dataset.type === type) {
                btn.style.background = 'rgba(99,102,241,.15)';
                btn.style.color = '#818cf8';
                btn.style.boxShadow = '0 1px 3px rgba(0,0,0,.2)';
            }
        });

        this.renderContentForm(type);
    },

    renderContentForm(type) {
        const container = document.getElementById('contentFormContainer');
        if (!container) return;

        let html = '';
        switch (type) {
            case 'caption':  html = this.getCaptionForm(); break;
            case 'email':    html = this.getEmailForm();   break;
            case 'sms':      html = this.getSmsForm();     break;
            case 'post_idea':html = this.getPostIdeaForm();break;
            default:         html = this.getCaptionForm();
        }
        container.innerHTML = html;

        if (window.app && window.app.showToast) {
            const labels = { caption: 'Caption', email: 'Email Draft', sms: 'SMS Text', post_idea: 'Post Idea' };
            window.app.showToast(`Switched to ${labels[type] || type} mode`);
        }
    },

    /* ─── CAPTION FORM ─────────────────────────────────────────────── */
    getCaptionForm() {
        return `
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Platform</label>
                <select id="captionPlatform" class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);">
                    <option value="instagram">Instagram</option>
                    <option value="linkedin">LinkedIn</option>
                    <option value="twitter">Twitter / X</option>
                    <option value="facebook">Facebook</option>
                    <option value="tiktok">TikTok</option>
                </select>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Your Content / Project Details</label>
                ${this._inputToolbar()}
                <textarea class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" rows="6" id="captionText" placeholder="Type, speak, or import your content / project details. AI will analyze and generate optimized captions, hashtags, and recommendations..."></textarea>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Tone</label>
                <div class="flex flex-wrap gap-2">
                    <button class="px-3 py-2 rounded-lg text-sm font-medium" style="background:rgba(99,102,241,.15);color:#818cf8;border:1px solid rgba(99,102,241,.2);" onclick="ContentStudio.setTone('professional')">Professional</button>
                    <button class="px-3 py-2 rounded-lg text-sm" style="background:rgba(255,255,255,.03);color:#9aa0b0;border:1px solid rgba(255,255,255,.08);" onclick="ContentStudio.setTone('casual')">Casual</button>
                    <button class="px-3 py-2 rounded-lg text-sm" style="background:rgba(255,255,255,.03);color:#9aa0b0;border:1px solid rgba(255,255,255,.08);" onclick="ContentStudio.setTone('funny')">Funny</button>
                    <button class="px-3 py-2 rounded-lg text-sm" style="background:rgba(255,255,255,.03);color:#9aa0b0;border:1px solid rgba(255,255,255,.08);" onclick="ContentStudio.setTone('inspiring')">Inspiring</button>
                    <button class="px-3 py-2 rounded-lg text-sm" style="background:rgba(255,255,255,.03);color:#9aa0b0;border:1px solid rgba(255,255,255,.08);" onclick="ContentStudio.setTone('viral')">Viral</button>
                </div>
            </div>
            ${this._aiAnalyzePanel()}
            <div class="mb-6">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Hashtags</label>
                <div class="flex flex-wrap gap-2 mb-3" id="hashtagsContainer">
                    <span class="px-3 py-1 rounded-full text-sm" style="background:rgba(99,102,241,.12);color:#818cf8;">#Marketing</span>
                    <span class="px-3 py-1 rounded-full text-sm" style="background:rgba(99,102,241,.12);color:#818cf8;">#Innovation</span>
                </div>
            </div>
            ${this._actionButtons()}
        `;
    },

    /* ─── EMAIL FORM ───────────────────────────────────────────────── */
    getEmailForm() {
        return `
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Subject Line</label>
                <input type="text" id="emailSubject" class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" placeholder="Enter email subject..." value="🎉 You're Invited: Exclusive Launch Event">
            </div>
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Preview Text</label>
                <input type="text" id="emailPreview" class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" placeholder="Brief preview shown in inbox..." value="Be the first to experience our new product">
            </div>
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Email Body</label>
                ${this._inputToolbar()}
                <textarea class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" rows="10" id="captionText" placeholder="Type, speak, or import your email content...">Hi [First Name],

We're thrilled to announce the launch of our newest product!

Here's what you can expect:
• Feature 1 – Save time with AI-powered automation
• Feature 2 – Beautiful analytics dashboard  
• Feature 3 – Multi-platform content creation

Click below to get early access with 30% off.

[CTA Button: Get Early Access]

Best regards,
The Team</textarea>
            </div>
            ${this._aiAnalyzePanel()}
            <div class="mb-6 p-3 rounded-lg" style="background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.12);">
                <div class="flex items-center gap-2 mb-1">
                    <i class="fas fa-info-circle" style="color:#60a5fa;"></i>
                    <span class="text-xs font-bold" style="color:#60a5fa;">EMAIL TIPS</span>
                </div>
                <p class="text-xs" style="color:#9aa0b0;">Keep subject under 50 chars. Personalize with [First Name]. Include one clear CTA.</p>
            </div>
            ${this._actionButtons()}
        `;
    },

    /* ─── SMS FORM ─────────────────────────────────────────────────── */
    getSmsForm() {
        return `
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">SMS Message</label>
                ${this._inputToolbar()}
                <textarea class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" rows="4" id="captionText" placeholder="Type, speak, or import your SMS text (160 chars)..." maxlength="320" oninput="ContentStudio.updateCharCount()">🔥 Flash Sale! 30% off everything for the next 24 hours. Use code FLASH30 at checkout. Shop now: https://example.com/sale</textarea>
                <div class="flex justify-between mt-2">
                    <span id="smsCharCount" class="text-xs" style="color:#5f6680;">0 / 160 characters</span>
                    <span id="smsSegments" class="text-xs" style="color:#5f6680;">1 segment</span>
                </div>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Link (optional)</label>
                <input type="url" id="smsLink" class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" placeholder="https://...">
            </div>
            ${this._aiAnalyzePanel()}
            <div class="mb-6 p-3 rounded-lg" style="background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.12);">
                <div class="flex items-center gap-2 mb-1">
                    <i class="fas fa-exclamation-triangle" style="color:#fbbf24;"></i>
                    <span class="text-xs font-bold" style="color:#fbbf24;">SMS BEST PRACTICES</span>
                </div>
                <p class="text-xs" style="color:#9aa0b0;">Keep under 160 chars for 1 segment. Include a clear CTA and opt-out info for compliance.</p>
            </div>
            ${this._actionButtons()}
        `;
    },

    /* ─── POST IDEA FORM ───────────────────────────────────────────── */
    getPostIdeaForm() {
        return `
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Topic / Theme</label>
                <input type="text" id="ideaTopic" class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" placeholder="e.g., Product launch, Industry tips, Behind the scenes..." value="">
            </div>
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Target Platform</label>
                <select id="ideaPlatform" class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);">
                    <option value="instagram">Instagram</option>
                    <option value="linkedin">LinkedIn</option>
                    <option value="twitter">Twitter / X</option>
                    <option value="tiktok">TikTok</option>
                    <option value="all">All Platforms</option>
                </select>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Generated Ideas</label>
                <div id="generatedIdeas" class="space-y-3">
                    <div class="p-3 rounded-lg" style="background:rgba(139,92,246,.06);border:1px solid rgba(139,92,246,.12);">
                        <p class="text-xs italic" style="color:#9aa0b0;">Click "Generate Ideas" to get AI-powered post ideas</p>
                    </div>
                </div>
            </div>
            <div class="mb-4">
                <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Notes</label>
                <textarea class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" rows="4" id="captionText" placeholder="Add any notes or refine the idea..."></textarea>
            </div>
            <div class="flex flex-col sm:flex-row gap-3">
                <button class="btn btn-primary flex-1" onclick="ContentStudio.generatePostIdeas()">
                    <i class="fas fa-lightbulb"></i> Generate Ideas
                </button>
                <button class="btn btn-secondary flex-1" onclick="ContentStudio.saveDraft()">
                    <i class="fas fa-save"></i> Save Draft
                </button>
            </div>
        `;
    },

    /* ─── SHARED ACTION BUTTONS ────────────────────────────────────── */
    _actionButtons() {
        return `
            <div class="flex flex-col sm:flex-row gap-3">
                <button class="btn btn-secondary flex-1" onclick="ContentStudio.regenerateContent()">
                    <i class="fas fa-sync"></i> Regenerate
                </button>
                <button class="btn btn-primary flex-1" onclick="ContentStudio.saveDraft()">
                    <i class="fas fa-save"></i> Save Draft
                </button>
                <button class="btn btn-success flex-1" onclick="ContentStudio.scheduleContent()">
                    <i class="fas fa-paper-plane"></i> Schedule
                </button>
            </div>
        `;
    },

    /* ─── UTILITY METHODS ──────────────────────────────────────────── */

    setTone(tone) {
        this.currentContent.tone = tone;
        document.querySelectorAll('[onclick^="ContentStudio.setTone"]').forEach(b => {
            b.style.background = 'transparent';
            b.style.color = '#9aa0b0';
            b.style.borderColor = 'rgba(255,255,255,.08)';
        });
        event.target.style.background = 'rgba(99,102,241,.15)';
        event.target.style.color = '#818cf8';
        event.target.style.borderColor = 'rgba(99,102,241,.3)';
    },

    updateCharCount() {
        const text = document.getElementById('captionText')?.value || '';
        const countEl = document.getElementById('smsCharCount');
        const segEl = document.getElementById('smsSegments');
        if (countEl) countEl.textContent = `${text.length} / 160 characters`;
        if (segEl) segEl.textContent = `${Math.ceil(text.length / 160) || 1} segment${text.length > 160 ? 's' : ''}`;
    },

    async generatePostIdeas() {
        const topic = document.getElementById('ideaTopic')?.value || 'marketing';
        const platform = document.getElementById('ideaPlatform')?.value || 'instagram';
        const container = document.getElementById('generatedIdeas');
        if (!container) return;

        container.innerHTML = '<div class="p-3 rounded-lg text-center" style="background:rgba(255,255,255,.02);"><i class="fas fa-spinner fa-spin" style="color:#818cf8;"></i> <span style="color:#9aa0b0;">Generating ideas...</span></div>';

        try {
            // Try Gemini agent first
            const resp = await fetch(`${window.CONFIG.API.BASE_URL}/api/v1/agent/content-ideas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic, platform, count: 5 })
            });
            const data = await resp.json();
            const ideas = data?.data?.ideas || data?.ideas || [];

            if (ideas.length) {
                container.innerHTML = ideas.map((idea, i) => `
                    <div class="p-3 rounded-lg cursor-pointer transition" style="background:rgba(139,92,246,.06);border:1px solid rgba(139,92,246,.1);" onmouseover="this.style.borderColor='rgba(139,92,246,.3)'" onmouseout="this.style.borderColor='rgba(139,92,246,.1)'" onclick="ContentStudio.useIdea(${i})">
                        <div class="flex items-center gap-2 mb-1">
                            <span class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold" style="background:linear-gradient(135deg,#8b5cf6,#6366f1);color:#fff;">${i + 1}</span>
                            <span class="text-sm font-semibold" style="color:#e8eaed;">${typeof idea === 'string' ? idea : idea.title || idea}</span>
                        </div>
                        ${typeof idea === 'object' && idea.description ? `<p class="text-xs ml-8" style="color:#9aa0b0;">${idea.description}</p>` : ''}
                    </div>
                `).join('');
            } else {
                throw new Error('No ideas returned');
            }
        } catch (e) {
            // Fallback ideas
            const fallback = [
                `Share a behind-the-scenes look at your ${topic} process`,
                `Post a customer success story related to ${topic}`,
                `Create a "Did you know?" fact about ${topic}`,
                `Share 3 quick tips about ${topic} for beginners`,
                `Ask your audience: "What's your biggest challenge with ${topic}?"`,
            ];
            container.innerHTML = fallback.map((idea, i) => `
                <div class="p-3 rounded-lg cursor-pointer transition" style="background:rgba(139,92,246,.06);border:1px solid rgba(139,92,246,.1);" onmouseover="this.style.borderColor='rgba(139,92,246,.3)'" onmouseout="this.style.borderColor='rgba(139,92,246,.1)'" onclick="document.getElementById('captionText').value='${idea.replace(/'/g, "\\'")}'; window.app?.showToast('Idea selected!')">
                    <div class="flex items-center gap-2">
                        <span class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold" style="background:linear-gradient(135deg,#8b5cf6,#6366f1);color:#fff;">${i + 1}</span>
                        <span class="text-sm" style="color:#e8eaed;">${idea}</span>
                    </div>
                </div>
            `).join('');
        }
    },

    useIdea(index) {
        const ideas = document.querySelectorAll('#generatedIdeas > div');
        if (ideas[index]) {
            const text = ideas[index].querySelector('.text-sm.font-semibold')?.textContent || ideas[index].textContent.trim();
            const captionField = document.getElementById('captionText');
            if (captionField) captionField.value = text;
            if (window.app) window.app.showToast('Idea selected! Edit and refine it.', 'success');
        }
    },

    async importMedia() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                this.currentContent.media = file;
                if (window.app) window.app.showToast(`Imported ${file.name}`, 'success');
            }
        };
        input.click();
    },

    async saveDraft() {
        try {
            const draftData = {
                ...this.currentContent,
                id: this.currentContent.id || `draft_${Date.now()}`,
                title: document.getElementById('emailSubject')?.value || document.getElementById('ideaTopic')?.value || `${this.currentContent.contentType} content`,
                caption: document.getElementById('captionText')?.value || '',
                updatedAt: new Date().toISOString(),
                status: 'draft'
            };

            const drafts = JSON.parse(localStorage.getItem('contentDrafts') || '[]');
            const idx = drafts.findIndex(d => d.id === draftData.id);
            if (idx >= 0) drafts[idx] = draftData; else drafts.push(draftData);

            localStorage.setItem('contentDrafts', JSON.stringify(drafts));
            this.currentContent = draftData;
            this.savedDrafts = drafts;

            if (window.app) window.app.showToast('Draft saved!', 'success');
        } catch (error) {
            console.error('Save draft error:', error);
            if (window.app) window.app.showToast('Failed to save draft', 'error');
        }
    },

    async regenerateContent() {
        try {
            if (window.app) window.app.showLoading();

            const type = this.currentContent.contentType;
            const content = document.getElementById('captionText')?.value || 'our latest product';
            const platform = this.currentContent?.platform || 'instagram';

            const resp = await fetch(`${window.CONFIG.API.BASE_URL}/api/v1/ai/generate-captions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content: `Generate a ${type} for a marketing campaign about: ${content}`,
                    platforms: [platform],
                    tone: 'engaging',
                    niche: 'general marketing'
                })
            });
            const data = await resp.json();
            const captions = data?.data?.captions || [];
            const answer = captions[0]?.text || data?.data?.answer || '';

            if (answer) {
                const field = document.getElementById('captionText');
                if (field) field.value = answer;
            }

            // Also update hashtags if returned
            const hashtags = data?.data?.hashtags || [];
            if (hashtags.length) {
                this.currentContent.hashtags = hashtags;
                this.updateHashtagsUI(hashtags);
            }

            if (window.app) {
                window.app.hideLoading();
                window.app.showToast('Content regenerated with AI!', 'success');
            }
        } catch (error) {
            if (window.app) window.app.hideLoading();
            console.error('Regenerate error:', error);
            if (window.app) window.app.showToast('Regeneration failed: ' + error.message, 'error');
        }
    },

    async scheduleContent() {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4';
        modal.innerHTML = `
            <div class="rounded-2xl p-6 max-w-md w-full" style="background:#131825;border:1px solid rgba(255,255,255,.08);">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold" style="color:#e8eaed;">Schedule Content</h3>
                    <button onclick="this.closest('.fixed').remove()" style="color:#5f6680;" onmouseover="this.style.color='#e8eaed'" onmouseout="this.style.color='#5f6680'"><i class="fas fa-times"></i></button>
                </div>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Date</label>
                        <input type="date" id="scheduleDate" class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" value="${new Date().toISOString().split('T')[0]}">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2" style="color:#c4c8d4;">Time</label>
                        <input type="time" id="scheduleTime" class="w-full px-4 py-3 rounded-lg" style="background:#0d1220;color:#e8eaed;border:1px solid rgba(255,255,255,.08);" value="10:00">
                    </div>
                    <div class="flex gap-3 pt-4">
                        <button onclick="this.closest('.fixed').remove()" class="btn btn-secondary flex-1">Cancel</button>
                        <button onclick="ContentStudio.confirmSchedule()" class="btn btn-primary flex-1"><i class="fas fa-calendar-check"></i> Schedule</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    async confirmSchedule() {
        const d = document.getElementById('scheduleDate');
        const t = document.getElementById('scheduleTime');
        if (d && t) {
            const scheduledTime = `${d.value}T${t.value}:00`;
            this.currentContent.scheduledTime = scheduledTime;
            this.currentContent.status = 'scheduled';
            await this.saveDraft();
            document.querySelector('.fixed.inset-0')?.remove();
            if (window.app) window.app.showToast(`Scheduled for ${new Date(scheduledTime).toLocaleString()}`, 'success');
        }
    },

    async optimizeHashtags() {
        try {
            if (window.app) window.app.showLoading();

            // Use new AI hashtag optimizer
            const topic = document.getElementById('captionText')?.value || 'marketing';
            const platform = this.currentContent?.platform || 'instagram';
            const resp = await fetch(`${window.CONFIG.API.BASE_URL}/api/v1/ai/optimize-hashtags`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: topic, platform, niche: 'general marketing', count: 10 })
            });
            const data = await resp.json();
            const hashtags = data?.data?.hashtags || data?.hashtags || ['#marketing', '#ai', '#growth', '#digital', '#content'];

            this.currentContent.hashtags = hashtags;
            this.updateHashtagsUI(hashtags);

            if (window.app) {
                window.app.hideLoading();
                window.app.showToast('Hashtags optimized with AI!', 'success');
            }
        } catch (error) {
            if (window.app) window.app.hideLoading();
            const fallback = ['#marketing', '#digitalmarketing', '#socialmedia', '#growth', '#ai'];
            this.updateHashtagsUI(fallback);
        }
    },

    updateHashtagsUI(hashtags) {
        const container = document.getElementById('hashtagsContainer');
        if (container) {
            container.innerHTML = hashtags.map(tag =>
                `<span class="px-3 py-1 rounded-full text-sm" style="background:rgba(99,102,241,.12);color:#818cf8;">${tag.startsWith('#') ? tag : '#' + tag}</span>`
            ).join('');
        }
    },

    generateOptimizedVersion() {
        this.regenerateContent();
    },

    /* ─── AI FULL ANALYZE & GENERATE (main CTA) ────────────────── */
    async aiAnalyzeAndGenerate() {
        const textEl = document.getElementById('captionText');
        const resultsContainer = document.getElementById('aiAnalyzeResults');
        if (!textEl || !resultsContainer) return;

        const content = textEl.value.trim();
        if (!content) {
            resultsContainer.innerHTML = `<div class="p-3 rounded-lg text-center" style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.15);"><i class="fas fa-exclamation-triangle" style="color:#fbbf24;"></i><p class="text-xs mt-1" style="color:#fbbf24;">Please enter your project details first (type, speak, or import a file).</p></div>`;
            return;
        }

        const platform = document.getElementById('captionPlatform')?.value || this.currentContent?.platform || 'instagram';
        const tone = this.currentContent?.tone || 'engaging';

        resultsContainer.innerHTML = `<div class="p-4 text-center"><div class="inline-flex items-center gap-2"><i class="fas fa-brain text-lg animate-pulse" style="color:#818cf8;"></i><span class="text-sm font-medium" style="color:#9aa0b0;">AI is analyzing your content and generating recommendations...</span></div></div>`;

        try {
            const baseUrl = (window.CONFIG?.API?.BASE_URL) || 'http://localhost:8000';

            // Fire captions + analysis in parallel
            const [captionsResp, analysisResp] = await Promise.all([
                fetch(`${baseUrl}/api/v1/ai/generate-captions`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content, platforms: [platform], tone, niche: 'general marketing' })
                }),
                fetch(`${baseUrl}/api/v1/ai/analyze-post`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content, platform })
                })
            ]);

            const captionsData = await captionsResp.json();
            const analysisData = await analysisResp.json();

            const captions = captionsData?.data?.captions || [];
            const hashtags = captionsData?.data?.hashtags || [];
            const tips = captionsData?.data?.engagement_tips || [];
            const bestTime = captionsData?.data?.best_posting_time || '';
            const hooks = captionsData?.data?.trending_hooks || [];
            const insight = captionsData?.data?.content_insight || '';

            const analysis = analysisData?.data || {};
            const score = analysis.score || analysis.quality_score || 0;
            const strengths = analysis.strengths || [];
            const weaknesses = analysis.weaknesses || [];
            const improved = analysis.improved_caption || analysis.improved_version || '';

            // Update hashtags in the form
            if (hashtags.length) {
                this.currentContent.hashtags = hashtags;
                this.updateHashtagsUI(hashtags);
            }

            const scoreColor = score >= 80 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444';
            const scoreLabel = score >= 80 ? 'Excellent' : score >= 50 ? 'Good' : 'Needs Work';

            resultsContainer.innerHTML = `
                <div class="space-y-3 mt-3">
                    <!-- Score -->
                    <div class="flex items-center gap-4 p-3 rounded-xl" style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);">
                        <div class="text-center">
                            <div class="text-2xl font-black" style="color:${scoreColor};">${score}</div>
                            <div class="text-[10px] font-bold" style="color:${scoreColor};">${scoreLabel}</div>
                        </div>
                        <div class="flex-1">
                            <div class="w-full h-2 rounded-full" style="background:rgba(255,255,255,.06);">
                                <div class="h-2 rounded-full transition-all" style="width:${score}%;background:${scoreColor};"></div>
                            </div>
                            <p class="text-[10px] mt-1" style="color:#5f6680;">Content Quality Score</p>
                        </div>
                        ${bestTime ? `<div class="text-right"><div class="text-[10px] font-bold" style="color:#fbbf24;"><i class="fas fa-clock mr-1"></i>Best Time</div><div class="text-xs font-semibold" style="color:#e8eaed;">${bestTime}</div></div>` : ''}
                    </div>

                    <!-- AI Caption Variations -->
                    ${captions.length ? `
                    <div>
                        <div class="text-xs font-bold mb-2" style="color:#818cf8;"><i class="fas fa-magic mr-1"></i>AI-GENERATED CAPTIONS</div>
                        <div class="space-y-2">
                            ${captions.map((cap, i) => {
                                const styles = [{icon:'fa-briefcase',color:'#818cf8',label:'Formal'},{icon:'fa-smile',color:'#06b6d4',label:'Casual'},{icon:'fa-fire',color:'#f59e0b',label:'Viral'}];
                                const s = styles[i % 3];
                                const capText = typeof cap === 'string' ? cap : cap.text || cap.caption || '';
                                return `<div class="p-3 rounded-lg cursor-pointer transition" style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);" onclick="document.getElementById('captionText').value=this.querySelector('.cap-text').textContent; if(window.app)app.showToast('Caption applied!','success');" onmouseover="this.style.borderColor='rgba(99,102,241,.3)'" onmouseout="this.style.borderColor='rgba(255,255,255,.05)'">
                                    <div class="flex items-center gap-2 mb-1">
                                        <i class="fas ${s.icon} text-[10px]" style="color:${s.color};"></i>
                                        <span class="text-[10px] font-bold" style="color:${s.color};">${s.label}</span>
                                        <span class="ml-auto text-[10px]" style="color:#5f6680;">Click to use</span>
                                    </div>
                                    <p class="cap-text text-xs leading-relaxed" style="color:#c4c8d4;">${capText}</p>
                                </div>`;
                            }).join('')}
                        </div>
                    </div>` : ''}

                    <!-- Trending Hashtags -->
                    ${hashtags.length ? `
                    <div>
                        <div class="text-xs font-bold mb-2" style="color:#22d3ee;"><i class="fas fa-hashtag mr-1"></i>TRENDING HASHTAGS</div>
                        <div class="flex flex-wrap gap-1.5">
                            ${hashtags.map(h => `<span class="px-2.5 py-1 rounded-full text-[11px] font-medium cursor-pointer transition" style="background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.15);" onclick="navigator.clipboard.writeText('${h}');if(window.app)app.showToast('Copied!','success');">${h.startsWith('#')?h:'#'+h}</span>`).join('')}
                        </div>
                    </div>` : ''}

                    <!-- Trending Hooks -->
                    ${hooks.length ? `
                    <div>
                        <div class="text-xs font-bold mb-2" style="color:#a78bfa;"><i class="fas fa-bolt mr-1"></i>TRENDING HOOKS</div>
                        <div class="space-y-1">
                            ${hooks.slice(0,3).map(h => `<div class="flex items-center gap-2 p-2 rounded-lg cursor-pointer" style="background:rgba(139,92,246,.06);border:1px solid rgba(139,92,246,.1);" onclick="const t=document.getElementById('captionText');if(t){t.value='${h.replace(/'/g,"\\'").replace(/\n/g,' ')}\\n\\n'+t.value;if(window.app)app.showToast('Hook added!','success');}"><i class="fas fa-arrow-right text-[10px]" style="color:#a78bfa;"></i><span class="text-xs" style="color:#c4c8d4;">${h}</span></div>`).join('')}
                        </div>
                    </div>` : ''}

                    <!-- Engagement Tips -->
                    ${tips.length ? `
                    <div>
                        <div class="text-xs font-bold mb-2" style="color:#34d399;"><i class="fas fa-lightbulb mr-1"></i>ENGAGEMENT TIPS</div>
                        <div class="space-y-1">
                            ${tips.map(t => `<div class="flex items-start gap-2 text-xs" style="color:#9aa0b0;"><i class="fas fa-check-circle mt-0.5" style="color:#34d399;"></i>${t}</div>`).join('')}
                        </div>
                    </div>` : ''}

                    <!-- Strengths & Weaknesses -->
                    ${strengths.length || weaknesses.length ? `
                    <div class="grid grid-cols-2 gap-3">
                        ${strengths.length ? `<div class="p-3 rounded-lg" style="background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.1);">
                            <div class="text-[10px] font-bold mb-1" style="color:#34d399;">STRENGTHS</div>
                            ${strengths.slice(0,3).map(s => `<p class="text-[10px] mb-0.5" style="color:#9aa0b0;"><i class="fas fa-plus text-[8px] mr-1" style="color:#34d399;"></i>${s}</p>`).join('')}
                        </div>`:''}
                        ${weaknesses.length ? `<div class="p-3 rounded-lg" style="background:rgba(245,158,11,.05);border:1px solid rgba(245,158,11,.1);">
                            <div class="text-[10px] font-bold mb-1" style="color:#fbbf24;">IMPROVE</div>
                            ${weaknesses.slice(0,3).map(w => `<p class="text-[10px] mb-0.5" style="color:#9aa0b0;"><i class="fas fa-arrow-up text-[8px] mr-1" style="color:#fbbf24;"></i>${w}</p>`).join('')}
                        </div>`:''}
                    </div>` : ''}

                    <!-- Improved Version -->
                    ${improved ? `
                    <div class="p-3 rounded-lg" style="background:linear-gradient(135deg,rgba(99,102,241,.06),rgba(139,92,246,.04));border:1px solid rgba(99,102,241,.15);">
                        <div class="flex items-center justify-between mb-2">
                            <div class="text-[10px] font-bold" style="color:#818cf8;"><i class="fas fa-wand-magic-sparkles mr-1"></i>AI-IMPROVED VERSION</div>
                            <button class="text-[10px] font-bold px-2 py-0.5 rounded" style="background:rgba(99,102,241,.15);color:#818cf8;" onclick="document.getElementById('captionText').value=this.closest('div').querySelector('.improved-text').textContent;if(window.app)app.showToast('Applied!','success');">Apply</button>
                        </div>
                        <p class="improved-text text-xs italic leading-relaxed" style="color:#c4c8d4;">${improved}</p>
                    </div>` : ''}

                    <!-- Content Insight -->
                    ${insight ? `<div class="p-2 rounded-lg text-center" style="background:rgba(99,102,241,.04);border:1px solid rgba(99,102,241,.08);"><p class="text-[10px]" style="color:#9aa0b0;"><i class="fas fa-info-circle mr-1" style="color:#818cf8;"></i>${insight}</p></div>` : ''}
                </div>
            `;

            if (window.app) window.app.showToast('AI analysis complete!', 'success');
        } catch (err) {
            console.error('[ContentStudio] AI analyze error:', err);
            resultsContainer.innerHTML = `<div class="p-3 rounded-lg" style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.1);"><p class="text-xs" style="color:#f87171;"><i class="fas fa-exclamation-triangle mr-1"></i>AI analysis failed: ${err.message}. Please try again.</p></div>`;
        }
    },

    /**
     * AI-powered content analysis: sends content text to Gemini for
     * quality scoring, tone analysis, engagement prediction, and improvement suggestions.
     */
    async analyzeContentWithAI() {
        const textEl = document.getElementById('captionText');
        const container = document.getElementById('aiContentAnalysis');
        if (!textEl || !container) return;

        const content = textEl.value.trim();
        if (!content) {
            container.innerHTML = `
                <div class="p-3 rounded-lg text-center" style="background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.12);">
                    <i class="fas fa-exclamation-triangle" style="color:#fbbf24;"></i>
                    <p class="text-xs mt-1" style="color:#fbbf24;">Please enter some content first</p>
                </div>`;
            return;
        }

        container.innerHTML = `
            <div class="p-4 text-center animate-pulse">
                <i class="fas fa-brain text-2xl mb-2" style="color:#818cf8;"></i>
                <p class="text-xs" style="color:#9aa0b0;">AI is analyzing your content...</p>
            </div>`;

        try {
            const baseUrl = (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL)
                ? window.CONFIG.API.BASE_URL : 'http://localhost:8000';
            const resp = await fetch(`${baseUrl}/api/v1/ai/analyze-post`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content,
                    content_text: content,
                    content_type: this.currentContent?.contentType || 'caption',
                    platform: this.currentContent?.platform || 'instagram'
                })
            });

            if (!resp.ok) throw new Error('Analysis failed');
            const result = await resp.json();
            const analysis = result.data || {};

            const qualityScore = analysis.quality_score || 0;
            const engRate = analysis.predicted_engagement_rate || '0%';
            const tone = analysis.tone_analysis || {};
            const tonePrimary = tone.primary || tone.primary_tone || '';
            const toneSecondary = tone.secondary || [];
            const strengths = analysis.strengths || [];
            const weaknesses = analysis.weaknesses || [];
            const improved = analysis.improved_version || '';
            const hashSuggestions = analysis.hashtag_suggestions || [];
            const bestTime = analysis.best_posting_time || '';
            const visualRec = analysis.visual_recommendation || '';

            const scoreColor = qualityScore >= 80 ? 'green' : qualityScore >= 50 ? 'yellow' : 'red';

            // Build a TTS summary
            const ttsSummary = [
                `Quality score: ${qualityScore} out of 100.`,
                tonePrimary ? `Tone: ${tonePrimary}.` : '',
                `Predicted engagement: ${engRate}.`,
                strengths.length ? `Strengths: ${strengths.slice(0,2).join('. ')}.` : '',
                weaknesses.length ? `Areas to improve: ${weaknesses.slice(0,2).join('. ')}.` : '',
            ].filter(Boolean).join(' ');

            const scoreHexColor = qualityScore >= 80 ? '#10b981' : qualityScore >= 50 ? '#f59e0b' : '#ef4444';
            const scoreLbl = qualityScore >= 80 ? 'Excellent' : qualityScore >= 50 ? 'Good' : 'Needs Work';

            container.innerHTML = `
                <!-- TTS Button -->
                <div class="flex items-center justify-between mb-2">
                    <span class="text-[10px] font-bold uppercase" style="color:#5f6680;">AI Analysis Results</span>
                    <button class="flex items-center gap-1 px-2 py-1 text-[10px] font-medium rounded-full transition" style="background:rgba(99,102,241,.1);color:#818cf8;border:1px solid rgba(99,102,241,.15);" onclick="ContentStudio.speakText(\`${ttsSummary.replace(/`/g, "'")}\`)" title="Listen to analysis">
                        <i class="fas fa-volume-up"></i> Listen
                    </button>
                </div>

                <!-- Quality Score -->
                <div class="p-3 rounded-lg" style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);">
                    <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-2">
                            <i class="fas fa-star" style="color:${scoreHexColor};"></i>
                            <span class="text-xs font-bold" style="color:${scoreHexColor};">${scoreLbl}</span>
                        </div>
                        <span class="text-xl font-black" style="color:${scoreHexColor};">${qualityScore}/100</span>
                    </div>
                    <div class="w-full rounded-full h-2" style="background:rgba(255,255,255,.06);">
                        <div class="h-2 rounded-full transition-all" style="width:${qualityScore}%;background:${scoreHexColor};"></div>
                    </div>
                </div>

                <!-- Predicted Engagement -->
                <div class="p-3 rounded-lg" style="background:rgba(139,92,246,.06);border:1px solid rgba(139,92,246,.12);">
                    <div class="flex items-center gap-2 mb-1">
                        <i class="fas fa-chart-line" style="color:#a78bfa;"></i>
                        <span class="text-xs font-bold" style="color:#a78bfa;">PREDICTED ENGAGEMENT</span>
                    </div>
                    <span class="text-lg font-bold" style="color:#c4b5fd;">${engRate}</span>
                </div>

                <!-- Tone Analysis -->
                ${tonePrimary ? `
                <div class="p-3 rounded-lg" style="background:rgba(6,182,212,.06);border:1px solid rgba(6,182,212,.12);">
                    <div class="flex items-center gap-2 mb-1">
                        <i class="fas fa-theater-masks" style="color:#22d3ee;"></i>
                        <span class="text-xs font-bold" style="color:#22d3ee;">TONE</span>
                    </div>
                    <div class="flex flex-wrap gap-1">
                        <span class="px-2 py-0.5 rounded-full text-xs font-medium" style="background:rgba(6,182,212,.12);color:#22d3ee;">${tonePrimary}</span>
                        ${toneSecondary.map(t => `<span class="px-2 py-0.5 rounded-full text-xs" style="background:rgba(6,182,212,.08);color:#67e8f9;">${t}</span>`).join('')}
                    </div>
                    ${tone.clarity ? `<div class="mt-1 text-[10px]" style="color:#5f6680;">Clarity: ${tone.clarity}/100 • CTA: ${tone.call_to_action_strength || 0}/100</div>` : ''}
                </div>` : ''}

                <!-- Strengths -->
                ${strengths.length ? `
                <div class="p-3 rounded-lg" style="background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.12);">
                    <div class="flex items-center gap-2 mb-2">
                        <i class="fas fa-check-circle" style="color:#34d399;"></i>
                        <span class="text-xs font-bold" style="color:#34d399;">STRENGTHS</span>
                    </div>
                    ${strengths.slice(0,3).map(s => `<p class="text-xs flex items-start gap-1" style="color:#9aa0b0;"><i class="fas fa-plus mt-0.5 text-[8px]" style="color:#34d399;"></i> ${s}</p>`).join('')}
                </div>` : ''}

                <!-- Weaknesses -->
                ${weaknesses.length ? `
                <div class="p-3 rounded-lg" style="background:rgba(245,158,11,.05);border:1px solid rgba(245,158,11,.12);">
                    <div class="flex items-center gap-2 mb-2">
                        <i class="fas fa-exclamation-circle" style="color:#fbbf24;"></i>
                        <span class="text-xs font-bold" style="color:#fbbf24;">IMPROVEMENTS</span>
                    </div>
                    ${weaknesses.slice(0,3).map(w => `<p class="text-xs flex items-start gap-1" style="color:#9aa0b0;"><i class="fas fa-arrow-up mt-0.5 text-[8px]" style="color:#fbbf24;"></i> ${w}</p>`).join('')}
                </div>` : ''}

                <!-- AI-Improved Version -->
                ${improved ? `
                <div class="p-3 rounded-lg" style="background:linear-gradient(135deg,rgba(99,102,241,.06),rgba(139,92,246,.04));border:1px solid rgba(99,102,241,.15);">
                    <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-2">
                            <i class="fas fa-magic" style="color:#818cf8;"></i>
                            <span class="text-xs font-bold" style="color:#818cf8;">AI-IMPROVED VERSION</span>
                        </div>
                        <button class="flex items-center gap-1 px-1.5 py-0.5 text-[10px] rounded-full transition" style="background:rgba(99,102,241,.12);color:#818cf8;" onclick="ContentStudio.speakText(\`${improved.replace(/`/g, "'").replace(/\\/g, '\\\\').substring(0, 500)}\`)" title="Listen to improved version">
                            <i class="fas fa-volume-up"></i>
                        </button>
                    </div>
                    <p class="text-xs mb-2 italic" style="color:#c4c8d4;">"${improved.substring(0, 200)}${improved.length > 200 ? '...' : ''}"</p>
                    <button class="text-xs font-bold" style="color:#818cf8;" onclick="document.getElementById('captionText').value=\`${improved.replace(/`/g, "'").replace(/\\/g, '\\\\')}\`; if(window.app)window.app.showToast('Applied AI version','success');">
                        <i class="fas fa-check mr-1"></i> Apply AI Version
                    </button>
                </div>` : ''}

                <!-- Best Time & Hashtags -->
                ${bestTime ? `
                <div class="p-2 rounded-lg" style="background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.12);">
                    <div class="flex items-center gap-2">
                        <i class="fas fa-clock text-xs" style="color:#fbbf24;"></i>
                        <span class="text-[10px] font-bold" style="color:#fbbf24;">BEST TIME: ${bestTime}</span>
                    </div>
                </div>` : ''}

                ${hashSuggestions.length ? `
                <div class="p-2 rounded-lg" style="background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.12);">
                    <div class="flex items-center gap-1 mb-1">
                        <i class="fas fa-hashtag text-xs" style="color:#818cf8;"></i>
                        <span class="text-[10px] font-bold" style="color:#818cf8;">SUGGESTED HASHTAGS</span>
                    </div>
                    <div class="flex flex-wrap gap-1">
                        ${hashSuggestions.slice(0,5).map(h => `<span class="px-1.5 py-0.5 rounded text-[10px]" style="background:rgba(99,102,241,.12);color:#818cf8;">${h}</span>`).join('')}
                    </div>
                </div>` : ''}
            `;

            if (window.app) window.app.showToast('Content analyzed by AI', 'success');
        } catch (err) {
            console.warn('[ContentStudio] AI analysis error:', err);
            container.innerHTML = `
                <div class="p-3 rounded-lg" style="background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.12);">
                    <div class="flex items-center gap-2 mb-2">
                        <i class="fas fa-check-circle" style="color:#34d399;"></i>
                        <span class="text-xs font-bold" style="color:#34d399;">HOOK STRENGTH</span>
                    </div>
                    <p class="text-xs" style="color:#9aa0b0;">Strong opener with engagement potential</p>
                </div>
                <div class="p-3 rounded-lg" style="background:rgba(99,102,241,.05);border:1px solid rgba(99,102,241,.12);">
                    <div class="flex items-center gap-2 mb-2">
                        <i class="fas fa-lightbulb" style="color:#818cf8;"></i>
                        <span class="text-xs font-bold" style="color:#818cf8;">SUGGESTION</span>
                    </div>
                    <p class="text-xs" style="color:#9aa0b0;">Add a question to boost engagement</p>
                </div>`;
        }
    }
};

window.ContentStudio = ContentStudio;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ContentStudio.init());
} else {
    ContentStudio.init();
}
