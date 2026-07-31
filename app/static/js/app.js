/* Konektivitas.com - Frontend JavaScript */

// API base URL
const API_BASE = '/api/v1';

// Tool form handler
async function handleToolForm(event, endpoint, transformInput) {
    event.preventDefault();
    
    const form = event.target;
    const container = form.closest('.tool-form') || form.parentElement;
    const loading = container.querySelector('.loading');
    const results = container.querySelector('.results');
    const btn = form.querySelector('.btn-primary');
    
    // Get input value
    let input = form.querySelector('input, select').value.trim();
    if (transformInput) input = transformInput(input);
    
    if (!input) {
        form.querySelector('input, select').focus();
        return;
    }
    
    // Show loading
    loading.classList.add('active');
    results.innerHTML = '';
    btn.disabled = true;
    btn.innerHTML = '<span class="btn-spinner"></span> Memproses...';
    
    const startTime = performance.now();
    
    try {
        const url = `${API_BASE}${endpoint.replace('{input}', encodeURIComponent(input))}`;
        const response = await fetch(url);
        const data = await response.json();
        const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);
        
        displayResults(results, data, endpoint, elapsed);
    } catch (error) {
        results.innerHTML = `
            <div class="result-header">
                <h3>Error</h3>
                <span class="result-status status-error">Gagal</span>
            </div>
            <div class="result-error">
                <p>⚠️ Gagal mengambil data: ${error.message}</p>
                <p class="result-error-hint">Pastikan koneksi internet aktif dan input sudah benar.</p>
            </div>`;
    } finally {
        loading.classList.remove('active');
        btn.disabled = false;
        btn.innerHTML = 'Cek Sekarang';
    }
}

// Display results in table format
function displayResults(container, data, endpoint, elapsed) {
    if (data.error) {
        container.innerHTML = `
            <div class="result-header">
                <h3>Hasil</h3>
                <span class="result-status status-error">Error</span>
            </div>
            <div class="result-error">
                <p>⚠️ ${data.error}</p>
            </div>`;
        return;
    }
    
    let html = '<div class="result-header"><h3>Hasil</h3>';
    html += '<div class="result-meta">';
    html += '<span class="result-status status-success">Berhasil</span>';
    if (elapsed) html += `<span class="result-time">⚡ ${elapsed}s</span>`;
    html += '</div></div>';
    
    // Build table from data
    html += '<table class="result-table">';
    for (const [key, value] of Object.entries(data)) {
        if (key === 'error') continue;
        const displayKey = formatKey(key);
        const displayValue = formatValue(value);
        if (displayValue !== '' && displayValue !== 'null' && displayValue !== '[]') {
            html += `<tr><th>${displayKey}</th><td>${displayValue}</td></tr>`;
        }
    }
    html += '</table>';
    
    // Copy JSON button + Raw JSON
    const jsonStr = JSON.stringify(data, null, 2);
    html += `<div class="result-actions">
        <button class="btn-copy" onclick="copyJSON(this)" data-json='${jsonStr.replace(/'/g, "'")}'>📋 Salin JSON</button>
    </div>`;
    html += `<details class="result-details"><summary>Lihat Raw JSON</summary><div class="result-json"><pre>${escapeHtml(jsonStr)}</pre></div></details>`;
    
    container.innerHTML = html;
}

// Format key names
function formatKey(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Format values
function formatValue(value) {
    if (Array.isArray(value)) {
        if (value.length === 0) return '<span class="text-muted">Kosong</span>';
        return value.map(v => `<code>${escapeHtml(String(v))}</code>`).join('<br>');
    }
    if (typeof value === 'object' && value !== null) {
        return Object.entries(value).map(([k, v]) => `<strong>${escapeHtml(k)}:</strong> ${escapeHtml(String(v))}`).join('<br>');
    }
    if (typeof value === 'boolean') {
        return value ? '✅ Ya' : '❌ Tidak';
    }
    const str = String(value);
    if (str.startsWith('http')) {
        return `<a href="${escapeHtml(str)}" target="_blank" rel="noopener">${escapeHtml(str)}</a>`;
    }
    return escapeHtml(str);
}

// Extract domain from URL or input
function extractDomain(input) {
    input = input.replace(/^https?:\/\//, '').replace(/\/.*$/, '');
    return input;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Copy JSON to clipboard
function copyJSON(btn) {
    const json = btn.getAttribute('data-json').replace(/'/g, "'");
    navigator.clipboard.writeText(json).then(() => {
        const original = btn.innerHTML;
        btn.innerHTML = '✅ Tersalin!';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.innerHTML = original;
            btn.classList.remove('copied');
        }, 2000);
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = json;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        btn.innerHTML = '✅ Tersalin!';
        setTimeout(() => btn.innerHTML = '📋 Salin JSON', 2000);
    });
}

// Copy text to clipboard (generic)
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Berhasil disalin!');
    }).catch(() => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Berhasil disalin!');
    });
}

// Toast notification
function showToast(message) {
    let toast = document.querySelector('.toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
}