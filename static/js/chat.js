/**
 * MediSense AI — Chatbot Engine & UI Logic
 * Handles all conversation flow, API calls, and dynamic UI updates.
 */

// ── State ───────────────────────────────────────────────────────────────────
const state = {
  mode: 'patient',
  collectedSymptoms: [],
  conversationHistory: [],
  allSymptoms: [],
  allDiseases: [],
  isTyping: false,
  typingTimeout: null
};

// ── Utility ──────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const now = () => new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

function md(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br/>');
}

function getSeverityColor(s) {
  if (s <= 3) return '#10b981';
  if (s <= 5) return '#f59e0b';
  if (s <= 7) return '#f97316';
  return '#ef4444';
}

function formatCost(cost) {
  if (!cost) return 'N/A';
  const fmt = n => '₹' + n.toLocaleString('en-IN');
  return `${fmt(cost.min)} – ${fmt(cost.max)} (avg ${fmt(cost.avg)})`;
}

function showToast(msg, type = 'info') {
  const colors = { info: 'var(--info)', success: 'var(--success)', error: 'var(--danger)', warn: 'var(--warning)' };
  const div = document.createElement('div');
  div.style.cssText = `
    position:fixed;bottom:24px;right:24px;z-index:9999;
    background:var(--bg-card2);border:1px solid ${colors[type]};
    padding:12px 20px;border-radius:12px;font-size:0.85rem;
    color:var(--text-primary);box-shadow:0 4px 20px rgba(0,0,0,0.4);
    animation:fadeInDown 0.3s ease;max-width:320px;
  `;
  div.textContent = msg;
  document.body.appendChild(div);
  setTimeout(() => div.remove(), 3500);
}

// ── API Calls ────────────────────────────────────────────────────────────────
async function apiFetch(url, options = {}) {
  try {
    const resp = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
      ...options
    });
    return await resp.json();
  } catch (e) {
    console.error('API Error:', e);
    return { error: 'Network error. Please check the server.' };
  }
}

async function loadSymptoms() {
  const data = await apiFetch('/api/symptoms');
  if (Array.isArray(data)) state.allSymptoms = data;
}

async function loadDiseases() {
  const data = await apiFetch('/api/diseases');
  if (Array.isArray(data)) {
    state.allDiseases = data;
    renderDiseaseList(data);
  }
}

async function checkStatus() {
  const data = await apiFetch('/api/status');
  if (data && !data.error) {
    $('status-text').textContent = `AI Online — ${data.accuracy || '97%'} Accuracy`;
    if (data.accuracy) $('stat-accuracy').textContent = data.accuracy;
  } else {
    $('status-text').textContent = 'Offline — Run server';
    $('nav-status').style.color = 'var(--danger)';
  }
}

// ── Chat Rendering ───────────────────────────────────────────────────────────
function appendMessage(role, content, time) {
  const wrap = $('chat-messages');
  const isBot = role === 'bot';
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = `
    <div class="msg-avatar">${isBot ? '🤖' : '🧑'}</div>
    <div>
      <div class="msg-bubble">${content}</div>
      <div class="msg-time">${time || now()}</div>
    </div>
  `;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
  return div;
}

function showTyping() {
  if (state.isTyping) return;
  state.isTyping = true;
  const wrap = $('chat-messages');
  const div = document.createElement('div');
  div.className = 'msg bot';
  div.id = 'typing-msg';
  div.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div class="typing-indicator">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>
  `;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
}

function hideTyping() {
  state.isTyping = false;
  const el = $('typing-msg');
  if (el) el.remove();
}

// ── Disease Prediction Cards ─────────────────────────────────────────────────
function buildPredictionCards(predictions) {
  if (!predictions || !predictions.length) return '';

  const rank = ['🥇', '🥈', '🥉'];
  let html = `<div class="prediction-cards">`;

  predictions.forEach((p, i) => {
    const color = p.color || 'var(--primary)';
    const sev = p.severity || 5;
    const sevColor = getSeverityColor(sev);
    const sevPct = (sev / 10) * 100;
    const confColor = p.confidence > 70 ? 'var(--danger)' : p.confidence > 40 ? 'var(--warning)' : 'var(--success)';

    html += `
    <div class="pred-card" style="--card-color:${color};" onclick="showDiseaseModal('${p.disease.replace(/'/g,"\\'")}')">
      <div class="pred-card-header">
        <div class="pred-name">
          <span>${rank[i] || '🏥'}</span>
          <span>${p.emoji || '🏥'} ${p.disease}</span>
        </div>
        <span class="confidence-badge" style="color:${confColor};border-color:${confColor}30;background:${confColor}15;">
          ${p.confidence}% match
        </span>
      </div>

      <div class="pred-desc">${p.description || ''}</div>

      <div class="severity-bar" title="Severity: ${sev}/10">
        <div class="severity-fill" style="width:${sevPct}%;background:${sevColor};"></div>
      </div>

      <div class="pred-meta" style="margin-top:8px;">
        <div class="pred-meta-item">⚠️ Severity: <span>${sev}/10</span></div>
        <div class="pred-meta-item">⏱️ Duration: <span>${p.duration || 'Variable'}</span></div>
        <div class="pred-meta-item">👨‍⚕️ <span>${p.specialist || 'General Physician'}</span></div>
        <div class="pred-meta-item">🏥 <span>Consult ASAP ${sev >= 8 ? '🚨' : sev >= 6 ? '⚠️' : '✅'}</span></div>
      </div>

      <div class="cost-highlight">
        💰 Avg Treatment Cost: <strong>${formatCost(p.avg_cost)}</strong>
      </div>

      ${p.precautions && p.precautions.length ? `
      <div class="precautions-list">
        ${p.precautions.slice(0, 3).map(pc => `<div class="precaution-item">${pc}</div>`).join('')}
      </div>` : ''}
    </div>`;
  });

  html += `</div>
  <p style="font-size:0.72rem;color:var(--text-muted);margin-top:8px;">
    💡 Click any card for full details. Consult a doctor for official diagnosis.
  </p>`;
  return html;
}

// ── Bot Response Handler ─────────────────────────────────────────────────────
async function sendMessage() {
  const input = $('chat-input');
  const text = input.value.trim();
  if (!text) { input.focus(); return; }

  // Append user message
  appendMessage('user', md(text));
  input.value = '';
  state.conversationHistory.push({ role: 'user', content: text });
  hideAutocomplete();

  // Typing indicator
  showTyping();
  await new Promise(r => setTimeout(r, 900 + Math.random() * 600));

  // Call API
  const resp = await apiFetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      message: text,
      history: state.conversationHistory.slice(-10),
      collected_symptoms: state.collectedSymptoms
    })
  });

  hideTyping();

  if (resp.error) {
    appendMessage('bot', `❌ ${resp.error}`);
    return;
  }

  // Update collected symptoms
  if (resp.collected_symptoms) {
    state.collectedSymptoms = resp.collected_symptoms;
    updateSymptomTags();
  }

  // Build response content
  let content = md(resp.message || '');

  if (resp.type === 'prediction' && resp.predictions && resp.predictions.length) {
    const urgency = resp.predictions[0].severity >= 8
      ? `⚠️ <strong style="color:var(--danger)">High severity detected!</strong> Please seek medical attention immediately.<br/><br/>`
      : resp.predictions[0].severity >= 6
      ? `⚠️ <strong style="color:var(--warning)">Moderate severity.</strong> Schedule a doctor's appointment soon.<br/><br/>`
      : `✅ <strong style="color:var(--success)">Lower severity detected.</strong> Monitor symptoms and consult a doctor if they persist.<br/><br/>`;

    content += `<br/>${urgency}`;
    content += buildPredictionCards(resp.predictions);

    content += `<div style="margin-top:14px;padding:12px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.82rem;">
      💚 <strong>Take care of yourself!</strong> You matter. Early diagnosis saves lives. Stay strong! 🌟<br/>
      🏥 Book an appointment with a <strong>${resp.predictions[0].specialist || 'General Physician'}</strong> near you.
    </div>`;
  }

  if (resp.type === 'greeting') {
    content += `<div style="margin-top:12px;padding:10px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-muted);">
      💙 Remember: <em>Your health is your greatest asset. We're here to help!</em>
    </div>`;
  }

  appendMessage('bot', content);
  state.conversationHistory.push({ role: 'bot', content: resp.message || '' });

  // Update suggestions
  if (resp.suggestions) renderSuggestions(resp.suggestions);
}

// ── Suggestions ──────────────────────────────────────────────────────────────
function renderSuggestions(suggestions) {
  const wrap = $('suggestions-wrap');
  wrap.innerHTML = suggestions.map(s =>
    `<button class="suggestion-chip" onclick="useSuggestion('${s.replace(/'/g,"\\'")}')" aria-label="Suggestion: ${s}">${s}</button>`
  ).join('');
}

function useSuggestion(text) {
  $('chat-input').value = text;
  sendMessage();
}

// ── Symptom Tags ─────────────────────────────────────────────────────────────
function updateSymptomTags() {
  const wrap = $('symptom-tags');
  if (!state.collectedSymptoms.length) { wrap.innerHTML = ''; return; }

  wrap.innerHTML = state.collectedSymptoms.map(s => {
    const label = s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return `<div class="symptom-tag">
      ${label}
      <button onclick="removeSymptom('${s}')" title="Remove" aria-label="Remove ${label}">×</button>
    </div>`;
  }).join('');
}

function removeSymptom(sym) {
  state.collectedSymptoms = state.collectedSymptoms.filter(s => s !== sym);
  updateSymptomTags();
  if (state.collectedSymptoms.length > 0) {
    showToast('Symptom removed. Type again to re-analyse.', 'warn');
  }
}

// ── Quick Symptoms ────────────────────────────────────────────────────────────
const QUICK_SYMPTOMS = [
  'fever', 'headache', 'cough', 'fatigue', 'nausea', 'vomiting',
  'chest pain', 'back pain', 'dizziness', 'rash', 'itching', 'joint pain',
  'breathlessness', 'sweating', 'diarrhea', 'weight loss'
];

function renderQuickSymptoms() {
  const grid = $('quick-symptoms-grid');
  grid.innerHTML = QUICK_SYMPTOMS.map(s =>
    `<button class="sym-chip" onclick="addQuickSymptom('${s}')" aria-label="Add symptom: ${s}">
      ${s.charAt(0).toUpperCase() + s.slice(1)}
    </button>`
  ).join('');
}

function addQuickSymptom(sym) {
  const input = $('chat-input');
  const current = input.value.trim();
  input.value = current ? `${current}, ${sym}` : sym;
  input.focus();
  showToast(`Added: ${sym}`, 'success');
}

// ── Disease List ─────────────────────────────────────────────────────────────
function renderDiseaseList(diseases) {
  const list = $('disease-list');
  if (!diseases.length) { list.innerHTML = '<p style="font-size:0.8rem;color:var(--text-muted);">Loading...</p>'; return; }

  list.innerHTML = diseases.map(d => {
    const sevColor = getSeverityColor(d.severity || 5);
    const cost = d.avg_cost ? `₹${(d.avg_cost.avg || 0).toLocaleString('en-IN')}` : 'N/A';
    return `
    <div class="disease-item" onclick="showDiseaseModal('${d.name.replace(/'/g,"\\'")}')">
      <div class="severity-dot" style="background:${sevColor};" title="Severity ${d.severity}/10"></div>
      <span class="d-emoji">${d.emoji || '🏥'}</span>
      <span class="d-name">${d.name}</span>
      <span class="d-cost">${cost}</span>
    </div>`;
  }).join('');
}

// ── Disease Modal ─────────────────────────────────────────────────────────────
async function showDiseaseModal(name) {
  const modal = $('disease-modal');
  const content = $('modal-content');

  content.innerHTML = `<div style="text-align:center;padding:2rem;color:var(--text-muted);">⏳ Loading...</div>`;
  modal.classList.add('show');

  const data = await apiFetch(`/api/disease/${encodeURIComponent(name)}`);
  if (data.error) { content.innerHTML = `<p style="color:var(--danger);">❌ ${data.error}</p>`; return; }

  const sev = data.severity || 5;
  const sevColor = getSeverityColor(sev);

  content.innerHTML = `
    <div style="margin-bottom:1.2rem;">
      <h2 id="modal-disease-name" style="font-family:var(--font-display);font-size:1.4rem;font-weight:800;margin-bottom:4px;">
        ${data.emoji || '🏥'} ${data.name}
      </h2>
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:1rem;">
        <span style="font-size:0.8rem;padding:3px 12px;border-radius:999px;background:${sevColor}22;color:${sevColor};border:1px solid ${sevColor}44;font-weight:700;">
          Severity ${sev}/10
        </span>
        <span style="font-size:0.8rem;color:var(--text-muted);">👨‍⚕️ ${data.specialist}</span>
        <span style="font-size:0.8rem;color:var(--text-muted);">⏱️ ${data.duration}</span>
      </div>
      <p style="font-size:0.88rem;color:var(--text-secondary);line-height:1.6;">${data.description}</p>
    </div>

    <div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.2);border-radius:var(--radius-md);padding:14px;margin-bottom:1rem;">
      <div style="font-weight:700;color:var(--warning);font-size:0.9rem;margin-bottom:4px;">💰 Treatment Cost (India)</div>
      <div style="font-size:1.1rem;font-weight:800;color:var(--text-primary);">${formatCost(data.avg_cost_inr)}</div>
      <div style="font-size:0.75rem;color:var(--text-muted);margin-top:4px;">Average hospital + medication costs. May vary by city and hospital tier.</div>
    </div>

    <div style="margin-bottom:1rem;">
      <div style="font-weight:700;font-size:0.9rem;margin-bottom:8px;color:var(--text-primary);">🛡️ Precautions & Care</div>
      ${(data.precautions || []).map(p => `
        <div style="display:flex;gap:8px;align-items:flex-start;padding:6px 0;border-bottom:1px solid var(--border);font-size:0.83rem;color:var(--text-secondary);">
          <span style="color:var(--success);font-weight:700;flex-shrink:0;">✓</span>
          ${p}
        </div>`).join('')}
    </div>

    <div style="background:var(--surface);border-radius:var(--radius-md);padding:14px;font-size:0.82rem;color:var(--text-muted);">
      💙 <strong style="color:var(--text-primary);">Important:</strong> This information is general in nature.
      Please consult a <strong style="color:var(--primary-light);">${data.specialist}</strong> for an accurate diagnosis and treatment plan.
      You are not alone — help is available. 🌟
    </div>

    <button onclick="document.getElementById('disease-modal').classList.remove('show')"
      style="margin-top:1rem;width:100%;padding:12px;background:linear-gradient(135deg,var(--primary),var(--primary-dark));
      border:none;border-radius:var(--radius-full);color:white;font-weight:700;cursor:pointer;font-size:0.9rem;">
      Close
    </button>
  `;
}

function closeModal(e) {
  if (e.target === $('disease-modal')) $('disease-modal').classList.remove('show');
}

// ── Mode Toggle ───────────────────────────────────────────────────────────────
function setMode(mode) {
  state.mode = mode;
  $('patient-mode-btn').classList.toggle('active', mode === 'patient');
  $('doctor-mode-btn').classList.toggle('active', mode === 'doctor');
  document.body.classList.toggle('doctor-mode', mode === 'doctor');

  const guideTitle = $(   'mode-guide-title');
  const guideContent = $('mode-guide-content');

  if (mode === 'doctor') {
    $('bot-name').textContent = 'Dr. MediBot — Clinical Assistant';
    guideTitle.textContent = '👨‍⚕️ Doctor Dashboard';
    guideContent.innerHTML = `
      <div style="display:flex;flex-direction:column;gap:8px;margin-top:8px;">
        <div style="padding:10px 14px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-secondary);">
          🔬 <strong style="color:var(--text-primary)">Differential Diagnosis:</strong> Enter patient symptoms for AI-assisted differential analysis
        </div>
        <div style="padding:10px 14px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-secondary);">
          📊 <strong style="color:var(--text-primary)">Confidence Scores:</strong> View ML confidence levels for each disease
        </div>
        <div style="padding:10px 14px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-secondary);">
          💰 <strong style="color:var(--text-primary)">Cost Planning:</strong> Estimate treatment costs for patient counselling
        </div>
        <div style="padding:10px 14px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-secondary);">
          🏥 <strong style="color:var(--text-primary)">Referral Help:</strong> AI-suggested specialist referrals
        </div>
      </div>`;
    showToast('👨‍⚕️ Doctor Mode activated — Clinical view enabled', 'info');
  } else {
    $('bot-name').textContent = 'Dr. MediBot AI';
    guideTitle.textContent = '🙋 Patient Guide';
    guideContent.innerHTML = `
      <div style="display:flex;flex-direction:column;gap:8px;margin-top:8px;">
        <div style="padding:10px 14px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-secondary);">
          📝 <strong style="color:var(--text-primary)">Step 1:</strong> Type your symptoms naturally
        </div>
        <div style="padding:10px 14px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-secondary);">
          🔍 <strong style="color:var(--text-primary)">Step 2:</strong> Our AI analyses them instantly
        </div>
        <div style="padding:10px 14px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-secondary);">
          💊 <strong style="color:var(--text-primary)">Step 3:</strong> Get top probable diseases + costs
        </div>
        <div style="padding:10px 14px;background:var(--surface);border-radius:var(--radius-sm);font-size:0.8rem;color:var(--text-secondary);">
          👨‍⚕️ <strong style="color:var(--text-primary)">Step 4:</strong> Visit the recommended specialist
        </div>
      </div>`;
    showToast('🙋 Patient Mode activated', 'info');
  }
}

// ── Clear Chat ────────────────────────────────────────────────────────────────
function clearChat() {
  state.collectedSymptoms = [];
  state.conversationHistory = [];
  $('chat-messages').innerHTML = '';
  $('symptom-tags').innerHTML = '';
  $('suggestions-wrap').innerHTML = '';
  updateSymptomTags();
  initGreeting();
  showToast('🔄 New session started — Tell me your symptoms!', 'success');
}

// ── Autocomplete ──────────────────────────────────────────────────────────────
let autocompleteDebounce = null;

function setupAutocomplete() {
  const input = $('chat-input');
  const list  = $('autocomplete-list');

  input.addEventListener('input', () => {
    clearTimeout(autocompleteDebounce);
    autocompleteDebounce = setTimeout(() => {
      const q = input.value.trim().toLowerCase().split(/[,\s]+/).pop();
      if (!q || q.length < 2) { hideAutocomplete(); return; }

      const matches = state.allSymptoms.filter(s =>
        s.label.toLowerCase().includes(q) || s.key.toLowerCase().includes(q)
      ).slice(0, 8);

      if (!matches.length) { hideAutocomplete(); return; }

      list.innerHTML = matches.map(s =>
        `<div class="autocomplete-item" onclick="selectAutocomplete('${s.label}')" role="option">
          🩺 ${s.label}
        </div>`
      ).join('');
      list.classList.add('show');
    }, 200);
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    if (e.key === 'Escape') hideAutocomplete();
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('.autocomplete-wrap')) hideAutocomplete();
  });
}

function selectAutocomplete(label) {
  const input = $('chat-input');
  const parts = input.value.split(/[,]+/);
  parts[parts.length - 1] = ' ' + label;
  input.value = parts.join(',').replace(/^,\s*/, '');
  hideAutocomplete();
  input.focus();
}

function hideAutocomplete() {
  $('autocomplete-list').classList.remove('show');
}

// ── Init Greeting ─────────────────────────────────────────────────────────────
async function initGreeting() {
  showTyping();
  await new Promise(r => setTimeout(r, 1200));
  hideTyping();

  const resp = await apiFetch('/api/greeting');
  const msg = resp.message || 'Welcome to MediSense AI! Describe your symptoms to get started. 🏥';

  appendMessage('bot', md(msg));
  renderSuggestions([
    'I have fever, headache and body ache',
    'Chest pain and breathlessness',
    'Skin rash and itching',
    'Stomach pain and nausea',
    'I feel dizzy and tired'
  ]);
}

// ── Boot ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  // Load data in parallel
  await Promise.all([loadSymptoms(), loadDiseases(), checkStatus()]);

  // Setup UI
  renderQuickSymptoms();
  setupAutocomplete();
  await initGreeting();

  // Copy hero image if served via Flask
  console.log('🏥 MediSense AI Front-end Ready!');
});
