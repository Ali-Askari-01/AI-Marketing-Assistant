/**
 * AI Chat Panel — Hybrid Intelligence Frontend
 * ═════════════════════════════════════════════
 * Slide-out chat drawer that talks to /api/v1/ai/chat
 * (Gemini primary, Rule-based fallback).
 * Also loads proactive insights from /api/v1/insights/proactive.
 */

const AIChatPanel = {
    isOpen: false,
    messages: [],
    isLoading: false,
    baseUrl: (window.CONFIG && window.CONFIG.API && window.CONFIG.API.BASE_URL) || 'http://localhost:8003',

    // ── Render the panel HTML (injected once) ──────────────────────
    inject() {
        if (document.getElementById('aiChatDrawer')) return;

        const drawer = document.createElement('div');
        drawer.id = 'aiChatDrawer';
        drawer.className = 'fixed inset-y-0 right-0 z-50 flex transition-transform duration-300 translate-x-full';
        drawer.style.cssText = 'width:400px; max-width:92vw;';
        drawer.innerHTML = `
            <!-- Backdrop -->
            <div class="ai-chat-backdrop fixed inset-0 bg-black/40 backdrop-blur-sm hidden" onclick="AIChatPanel.close()"></div>

            <!-- Panel -->
            <div class="relative ml-auto h-full flex flex-col" style="background:#0f1321; border-left:1px solid rgba(99,102,241,0.2); width:400px; max-width:92vw;">

                <!-- Header -->
                <div class="flex items-center justify-between px-5 py-4" style="border-bottom:1px solid rgba(255,255,255,0.06); background:linear-gradient(135deg,rgba(99,102,241,0.08),rgba(6,182,212,0.06));">
                    <div class="flex items-center gap-3">
                        <div class="w-9 h-9 rounded-xl flex items-center justify-center" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);">
                            <i class="fas fa-brain text-white text-sm"></i>
                        </div>
                        <div>
                            <h3 class="text-sm font-bold" style="color:#e8eaed;">AI Strategist</h3>
                            <div class="flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block"></span>
                                <span class="text-xs" style="color:#9aa0b0;">Gemini + Rules Engine</span>
                            </div>
                        </div>
                    </div>
                    <button onclick="AIChatPanel.close()" class="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-white/5 transition-colors" style="color:#5f6680;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>

                <!-- Insights Banner (auto-populated) -->
                <div id="aiChatInsights" class="px-4 py-3 hidden" style="border-bottom:1px solid rgba(255,255,255,0.04); background:rgba(99,102,241,0.04);">
                    <div class="flex items-center gap-2 mb-1">
                        <i class="fas fa-lightbulb text-xs" style="color:#f59e0b;"></i>
                        <span class="text-xs font-semibold" style="color:#fbbf24;">PROACTIVE INSIGHT</span>
                    </div>
                    <p id="aiChatInsightText" class="text-xs leading-relaxed" style="color:#9aa0b0;"></p>
                </div>

                <!-- Messages -->
                <div id="aiChatMessages" class="flex-1 overflow-y-auto px-4 py-4 space-y-4" style="scrollbar-width:thin; scrollbar-color:rgba(255,255,255,0.08) transparent;">
                    <!-- Welcome message -->
                    <div class="flex gap-3">
                        <div class="w-7 h-7 rounded-lg flex-shrink-0 flex items-center justify-center mt-0.5" style="background:linear-gradient(135deg,#6366f1,#06b6d4);">
                            <i class="fas fa-robot text-white text-xs"></i>
                        </div>
                        <div class="flex-1 p-3 rounded-xl text-sm leading-relaxed" style="background:rgba(255,255,255,0.04); color:#c8ccd8; border:1px solid rgba(255,255,255,0.04);">
                            <p class="font-semibold mb-1" style="color:#e8eaed;">Hey! I'm your AI Marketing Strategist.</p>
                            <p>I analyse your <strong>live business data</strong> and give data-backed advice. Ask me anything:</p>
                            <div class="mt-2 space-y-1">
                                <button onclick="AIChatPanel.sendQuick('What\\'s my engagement rate?')" class="block w-full text-left px-3 py-1.5 rounded-lg text-xs transition-colors hover:bg-white/5" style="color:#818cf8;">→ What's my engagement rate?</button>
                                <button onclick="AIChatPanel.sendQuick('Which platform performs best?')" class="block w-full text-left px-3 py-1.5 rounded-lg text-xs transition-colors hover:bg-white/5" style="color:#818cf8;">→ Which platform performs best?</button>
                                <button onclick="AIChatPanel.sendQuick('Give me tips to improve my marketing')" class="block w-full text-left px-3 py-1.5 rounded-lg text-xs transition-colors hover:bg-white/5" style="color:#818cf8;">→ Tips to improve my marketing</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Input -->
                <div class="px-4 py-3" style="border-top:1px solid rgba(255,255,255,0.06); background:rgba(0,0,0,0.2);">
                    <div class="flex gap-2">
                        <input id="aiChatInput" type="text" placeholder="Ask about your campaigns, content, analytics..."
                            class="flex-1 px-4 py-2.5 rounded-xl text-sm outline-none transition-all"
                            style="background:rgba(255,255,255,0.05); color:#e8eaed; border:1px solid rgba(255,255,255,0.08);"
                            onfocus="this.style.borderColor='rgba(99,102,241,0.4)'"
                            onblur="this.style.borderColor='rgba(255,255,255,0.08)'"
                            onkeypress="if(event.key==='Enter') AIChatPanel.send()">
                        <button onclick="AIChatPanel.send()" class="w-10 h-10 rounded-xl flex items-center justify-center transition-all"
                            style="background:linear-gradient(135deg,#6366f1,#8b5cf6); color:white;"
                            id="aiChatSendBtn">
                            <i class="fas fa-paper-plane text-sm"></i>
                        </button>
                    </div>
                    <div class="flex items-center justify-between mt-2">
                        <span class="text-xs" style="color:#5f6680;" id="aiChatSource">Powered by Gemini + Rules Engine</span>
                        <button onclick="AIChatPanel.clearChat()" class="text-xs hover:underline" style="color:#5f6680;">Clear</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(drawer);

        // Load proactive insights
        this.loadInsights();
    },

    // ── Open / Close ───────────────────────────────────────────────
    toggle() {
        this.isOpen ? this.close() : this.open();
    },

    open() {
        this.inject();
        const drawer = document.getElementById('aiChatDrawer');
        const backdrop = drawer.querySelector('.ai-chat-backdrop');
        drawer.classList.remove('translate-x-full');
        backdrop.classList.remove('hidden');
        this.isOpen = true;
        setTimeout(() => {
            const input = document.getElementById('aiChatInput');
            if (input) input.focus();
        }, 300);
    },

    close() {
        const drawer = document.getElementById('aiChatDrawer');
        if (!drawer) return;
        const backdrop = drawer.querySelector('.ai-chat-backdrop');
        drawer.classList.add('translate-x-full');
        backdrop.classList.add('hidden');
        this.isOpen = false;
    },

    // ── Send message ───────────────────────────────────────────────
    sendQuick(text) {
        const input = document.getElementById('aiChatInput');
        if (input) input.value = text;
        this.send();
    },

    async send() {
        const input = document.getElementById('aiChatInput');
        const question = (input && input.value || '').trim();
        if (!question || this.isLoading) return;

        input.value = '';
        this.isLoading = true;

        // Show user message
        this._appendMsg('user', question);

        // Show typing indicator
        const typingId = this._appendMsg('ai', '<i class="fas fa-circle-notch fa-spin" style="color:#818cf8;"></i> Analysing your data...');

        try {
            const res = await fetch(`${this.baseUrl}/api/v1/ai/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question }),
            });
            const data = await res.json();
            const answer = (data.data && data.data.answer) || 'Sorry, I couldn\'t generate a response.';
            const source = (data.data && data.data.source) || 'unknown';

            // Replace typing with answer
            this._replaceMsg(typingId, 'ai', this._formatMd(answer));

            // Update source label
            const srcEl = document.getElementById('aiChatSource');
            if (srcEl) {
                srcEl.textContent = source === 'gemini'
                    ? '✦ Answered via Gemini AI'
                    : '⚡ Answered via Rules Engine (offline)';
            }
        } catch (err) {
            this._replaceMsg(typingId, 'ai', '<span style="color:#f87171;">Network error — please check your backend is running on port 8003.</span>');
        }

        this.isLoading = false;
    },

    // ── Load proactive insights ────────────────────────────────────
    async loadInsights() {
        try {
            const res = await fetch(`${this.baseUrl}/api/v1/insights/proactive`);
            const data = await res.json();
            if (data.success && data.data) {
                const insights = data.data;
                const banner = document.getElementById('aiChatInsights');
                const text = document.getElementById('aiChatInsightText');
                if (!banner || !text) return;

                // Pick the first anomaly or advice to show
                let msg = '';
                if (insights.anomalies && insights.anomalies.length > 0) {
                    msg = insights.anomalies[0].message;
                } else if (insights.advice && insights.advice.length > 0) {
                    msg = insights.advice[0].message;
                }
                if (msg) {
                    text.innerHTML = this._formatMd(msg);
                    banner.classList.remove('hidden');
                }

                // Also update home health score if visible
                this._updateHomeHealth(insights.health);

                // Store for later
                this._insights = insights;
            }
        } catch (e) {
            console.warn('[AIChatPanel] Could not load proactive insights:', e);
        }
    },

    _updateHomeHealth(health) {
        if (!health) return;
        const scoreEl = document.querySelector('.health-score-number');
        const gradeEl = scoreEl && scoreEl.nextElementSibling;
        if (scoreEl) scoreEl.textContent = health.score;
        if (gradeEl) gradeEl.textContent = health.grade;

        // Update SVG circle (dasharray=478, offset = 478 * (1 - score/100))
        const circle = document.querySelector('.health-score-progress');
        if (circle) {
            const offset = 478 * (1 - health.score / 100);
            circle.setAttribute('stroke-dashoffset', offset.toFixed(0));
        }

        // Update breakdown rows (Consistency, Engagement, Diversity)
        const bd = health.breakdown || {};
        const mapping = [
            { label: 'Consistency', value: (bd.consistency || 0) * 4 },
            { label: 'Engagement', value: (bd.engagement || 0) * 4 },
            { label: 'Diversity',  value: ((bd.content_volume || 0) + (bd.reach || 0)) * 2 }
        ];
        const rows = document.querySelectorAll('.health-score ~ .mt-6 .flex.justify-between');
        mapping.forEach((m, i) => {
            if (rows[i]) {
                const valEl = rows[i].querySelector('.font-semibold');
                if (valEl) valEl.textContent = Math.round(m.value) + '%';
            }
        });
    },

    // ── DOM helpers ────────────────────────────────────────────────
    _msgCounter: 0,

    _appendMsg(role, html) {
        const container = document.getElementById('aiChatMessages');
        if (!container) return null;

        const id = `ai-msg-${++this._msgCounter}`;
        const isUser = role === 'user';

        const wrapper = document.createElement('div');
        wrapper.id = id;
        wrapper.className = `flex gap-3 ${isUser ? 'justify-end' : ''}`;
        wrapper.style.animation = 'fadeIn .25s ease';

        if (isUser) {
            wrapper.innerHTML = `
                <div class="max-w-[85%] px-4 py-2.5 rounded-xl text-sm" style="background:linear-gradient(135deg,#6366f1,#8b5cf6); color:white;">
                    ${this._esc(html)}
                </div>
            `;
        } else {
            wrapper.innerHTML = `
                <div class="w-7 h-7 rounded-lg flex-shrink-0 flex items-center justify-center mt-0.5" style="background:linear-gradient(135deg,#6366f1,#06b6d4);">
                    <i class="fas fa-robot text-white text-xs"></i>
                </div>
                <div class="flex-1 p-3 rounded-xl text-sm leading-relaxed" style="background:rgba(255,255,255,0.04); color:#c8ccd8; border:1px solid rgba(255,255,255,0.04);">
                    ${html}
                </div>
            `;
        }

        container.appendChild(wrapper);
        container.scrollTop = container.scrollHeight;
        return id;
    },

    _replaceMsg(id, role, html) {
        const el = document.getElementById(id);
        if (!el) return;
        const bubble = role === 'user'
            ? el.querySelector('div[style*="gradient"]')
            : el.querySelector('.flex-1');
        if (bubble) bubble.innerHTML = html;

        const container = document.getElementById('aiChatMessages');
        if (container) container.scrollTop = container.scrollHeight;
    },

    clearChat() {
        const container = document.getElementById('aiChatMessages');
        if (!container) return;
        // Keep the welcome message (first child)
        while (container.children.length > 1) {
            container.removeChild(container.lastChild);
        }
        this.messages = [];
    },

    _esc(str) {
        const d = document.createElement('div');
        d.textContent = str;
        return d.innerHTML;
    },

    _formatMd(text) {
        // Lightweight markdown: bold, bullets, line breaks
        return text
            .replace(/\*\*(.+?)\*\*/g, '<strong style="color:#e8eaed;">$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/^[•\-]\s+/gm, '<span style="color:#818cf8;">●</span> ')
            .replace(/\n/g, '<br>');
    },
};

// Expose globally
window.AIChatPanel = AIChatPanel;
