/* Konektivitas.com - Frontend JavaScript */

// API base URL
const API_BASE = '/api/v1';

// ============ MOBILE NAV ============
function toggleMobileNav() {
    const nav = document.getElementById('mainNav');
    const toggle = document.getElementById('menuToggle');
    nav.classList.toggle('active');
    toggle.textContent = nav.classList.contains('active') ? '✕' : '☰';
}

// Close mobile nav when clicking a link
document.addEventListener('DOMContentLoaded', function () {
    const nav = document.getElementById('mainNav');
    if (nav) {
        nav.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                if (window.innerWidth <= 768) {
                    nav.classList.remove('active');
                    var toggle = document.getElementById('menuToggle');
                    if (toggle) toggle.textContent = '☰';
                }
            });
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.nav-dropdown')) {
            document.querySelectorAll('.nav-dropdown-menu').forEach(function (menu) {
                menu.classList.remove('active');
            });
        }
    });
});

// ============ NAV DROPDOWN ============
function toggleDropdown(btn) {
    // Close other dropdowns
    document.querySelectorAll('.nav-dropdown-menu').forEach(function (menu) {
        if (menu !== btn.nextElementSibling) {
            menu.classList.remove('active');
        }
    });
    btn.nextElementSibling.classList.toggle('active');
}

// ============ SEARCH / FILTER ============
function filterTools(query) {
    query = query.toLowerCase().trim();
    var sections = document.querySelectorAll('.section[data-category]');
    var cards = document.querySelectorAll('.tool-card[data-name]');
    var noResults = document.getElementById('noResults');
    var searchQuery = document.getElementById('searchQuery');
    var visibleCount = 0;

    cards.forEach(function (card) {
        var name = card.getAttribute('data-name') || '';
        var text = card.textContent.toLowerCase();
        var match = !query || name.includes(query) || text.includes(query);
        card.style.display = match ? '' : 'none';
        if (match) visibleCount++;
    });

    // Show/hide sections based on visible cards
    sections.forEach(function (section) {
        var hasVisible = false;
        section.querySelectorAll('.tool-card').forEach(function (c) {
            if (c.style.display !== 'none') hasVisible = true;
        });
        section.style.display = hasVisible ? '' : 'none';
    });

    // No results message
    if (noResults) {
        if (visibleCount === 0 && query) {
            noResults.style.display = 'block';
            if (searchQuery) searchQuery.textContent = query;
        } else {
            noResults.style.display = 'none';
        }
    }
}

// ============ BACK TO TOP ============
window.addEventListener('scroll', function () {
    var btn = document.getElementById('backToTop');
    if (btn) {
        if (window.scrollY > 300) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    }
});

// ============ URL QUERY STATE ============
function updateURLState(params) {
    var url = new URL(window.location);
    for (var key in params) {
        if (params.hasOwnProperty(key) && params[key]) {
            url.searchParams.set(key, params[key]);
        } else {
            url.searchParams.delete(key);
        }
    }
    window.history.replaceState({}, '', url);
}

function loadURLState(formId) {
    var url = new URL(window.location);
    var form = document.getElementById(formId);
    if (!form) return false;

    var hasParams = false;
    for (var pair of url.searchParams) {
        var key = pair[0];
        var value = pair[1];
        var input = form.querySelector('[name="' + key + '"]') || document.getElementById(key);
        if (input) {
            input.value = value;
            hasParams = true;
        }
    }

    // Auto-submit if there are parameters
    if (hasParams && url.searchParams.toString()) {
        setTimeout(function () {
            form.dispatchEvent(new Event('submit'));
        }, 100);
    }
    return hasParams;
}

// ============ KEYBOARD SHORTCUTS ============
document.addEventListener('keydown', function (e) {
    // Don't trigger shortcuts when typing in input/textarea/select
    var tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') {
        // Allow Escape even in inputs
        if (e.key !== 'Escape') return;
    }

    // Ctrl+K or Cmd+K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        var searchInput = document.querySelector('.search-box input, input[type="search"]');
        if (searchInput) {
            searchInput.focus();
            showToast('🔍 Search focused');
        }
        return;
    }

    // Ctrl+D or Cmd+D: Toggle dark mode
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        if (typeof toggleTheme === 'function') toggleTheme();
        return;
    }

    // Escape: Close dropdowns/menus/modal
    if (e.key === 'Escape') {
        // Close shortcuts modal first
        var overlay = document.getElementById('shortcutsOverlay');
        if (overlay && overlay.classList.contains('active')) {
            closeShortcutsModal();
            return;
        }
        // Close all dropdowns
        document.querySelectorAll('.nav-dropdown-menu.active').forEach(function (d) {
            d.classList.remove('active');
        });
        // Close mobile nav
        var nav = document.querySelector('.nav.active');
        if (nav) {
            nav.classList.remove('active');
            var toggle = document.getElementById('menuToggle');
            if (toggle) toggle.textContent = '☰';
        }
        return;
    }

    // ?: Show keyboard shortcuts modal (only when not in input)
    if (e.key === '?' || (e.shiftKey && e.key === '/')) {
        e.preventDefault();
        openShortcutsModal();
        return;
    }

    // Home: Scroll to top
    if (e.key === 'Home' && !e.ctrlKey) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

// ============ SHORTCUTS MODAL ============
function openShortcutsModal() {
    var overlay = document.getElementById('shortcutsOverlay');
    if (overlay) {
        overlay.classList.add('active');
        overlay.setAttribute('aria-hidden', 'false');
    }
}

function closeShortcutsModal() {
    var overlay = document.getElementById('shortcutsOverlay');
    if (overlay) {
        overlay.classList.remove('active');
        overlay.setAttribute('aria-hidden', 'true');
    }
}

// ============ TOOL HISTORY ============
function saveToHistory(toolName, query) {
    if (!toolName || !query) return;
    const key = 'konek_history_' + toolName;
    let history = [];
    try {
        history = JSON.parse(localStorage.getItem(key) || '[]');
    } catch (e) {
        history = [];
    }
    // Remove duplicate
    history = history.filter(function (h) { return h !== query; });
    // Add to front
    history.unshift(query);
    // Keep only 10
    history = history.slice(0, 10);
    try {
        localStorage.setItem(key, JSON.stringify(history));
    } catch (e) { /* ignore */ }
}

function getHistory(toolName) {
    const key = 'konek_history_' + toolName;
    try {
        return JSON.parse(localStorage.getItem(key) || '[]');
    } catch (e) {
        return [];
    }
}

function displayHistory(toolName, containerId) {
    const history = getHistory(toolName);
    if (history.length === 0) return;
    const container = document.getElementById(containerId);
    if (!container) return;
    let html = '<div class="history-section"><div class="history-header"><h4>📋 Riwayat Pencarian</h4>';
    html += '<button class="btn-clear-history" data-history-tool="' + escapeHtml(toolName) + '" data-history-container="' + escapeHtml(containerId) + '" title="Hapus semua riwayat">🗑️ Hapus</button>';
    html += '</div><div class="history-list">';
    history.forEach(function (item, idx) {
        html += '<button class="history-item" data-history-query="' + escapeHtml(item) + '" data-history-idx="' + idx + '">' +
            escapeHtml(item) + '</button>';
    });
    html += '</div></div>';
    container.innerHTML = html;

    // Event delegation for history items (safe from XSS)
    container.querySelectorAll('.history-item').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var query = this.getAttribute('data-history-query');
            useHistoryItem(toolName, query);
        });
    });
    // Event delegation for clear button
    container.querySelectorAll('.btn-clear-history').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var tn = this.getAttribute('data-history-tool');
            var cid = this.getAttribute('data-history-container');
            clearHistory(tn, cid);
        });
    });
}

function clearHistory(toolName, containerId) {
    if (!confirm('Hapus semua riwayat pencarian?')) return;
    const key = 'konek_history_' + toolName;
    try { localStorage.removeItem(key); } catch (e) { /* ignore */ }
    const container = document.getElementById(containerId);
    if (container) container.innerHTML = '';
    showToast('🗑️ Riwayat berhasil dihapus');
}

function useHistoryItem(toolName, query) {
    var form = document.querySelector('.tool-form form');
    if (form) {
        var input = form.querySelector('input[type="text"], input:not([type="hidden"])');
        if (input) {
            input.value = query;
            form.dispatchEvent(new Event('submit'));
        }
    }
}

function extractToolName(endpoint) {
    // Extract tool name from API endpoint and map to page-based tool name
    // Used by saveToHistory() — must match keys used in displayHistory() calls
    // /dns/google.com → dns-lookup
    // /ssl/example.com → ssl-checker
    // /whois/example.com → whois-lookup
    // /ip/8.8.8.8 → ip-lookup
    var TOOL_NAME_MAP = {
        'dns': 'dns-lookup',
        'whois': 'whois-lookup',
        'ssl': 'ssl-checker',
        'ping': 'ping-checker',
        'ip': 'ip-lookup',
        'http': 'http-status',
        'redirect': 'redirect-checker',
        'headers': 'header-checker',
        'ua': 'ua-checker',
        'email': 'email-validator',
        'port': 'port-scanner',
        'cdn': 'cdn-detect',
        'asn': 'asn-lookup',
        'blacklist': 'blacklist-checker',
        'batch': 'batch-lookup',
        'compare': 'compare'
    };
    // Handle nested endpoints like /dns/google.com/reverse → reverse-dns
    var parts = endpoint.split('?')[0].split('/').filter(function (p) { return p && p !== 'api' && p !== 'v1'; });
    var rawName = parts[0] || 'unknown';
    var subPath = parts[1] || '';
    // Check for sub-path mappings first
    var SUB_PATH_MAP = {
        'reverse': 'reverse-dns',
        'mx': 'mx-lookup',
        'txt': 'txt-lookup',
        'cname': 'cname-lookup',
        'spf': 'spf-checker',
        'dmarc': 'dmarc-checker',
        'propagation': 'dns-propagation',
        'expiry': rawName === 'ssl' ? 'ssl-expiry' : 'domain-expiry',
        'asn': 'asn-lookup',
        'blacklist': 'blacklist-checker',
        'me': 'my-ip',
        'validate': 'email-validator'
    };
    if (subPath && SUB_PATH_MAP[subPath]) {
        return SUB_PATH_MAP[subPath];
    }
    return TOOL_NAME_MAP[rawName] || rawName;
}

// ============ TOOL FORM HANDLER ============
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

        if (!response.ok) {
            const errorMsg = data.detail || data.error || `HTTP ${response.status}`;
            throw new Error(errorMsg);
        }

        displayResults(results, data, endpoint, elapsed);

        // Update URL state for shareability
        var urlParams = {};
        form.querySelectorAll('input, select').forEach(function (el) {
            if (el.name && el.value) {
                urlParams[el.name] = el.value;
            }
        });
        if (Object.keys(urlParams).length > 0) {
            updateURLState(urlParams);
        }

        // Save to history after successful query
        var toolName = extractToolName(endpoint);
        saveToHistory(toolName, input);
    } catch (error) {
        results.innerHTML = `
            <div class="result-header">
                <h3>Error</h3>
                <span class="result-status status-error">Gagal</span>
            </div>
            <div class="result-error">
                <p>⚠️ Gagal mengambil data: ${escapeHtml(error.message)}</p>
                <p class="result-error-hint">Pastikan koneksi internet aktif dan input sudah benar.</p>
            </div>`;
    } finally {
        loading.classList.remove('active');
        btn.disabled = false;
        btn.innerHTML = 'Cek Sekarang';
    }
}

// Map to store JSON data for copy (avoids XSS via HTML attributes)
const jsonDataMap = new Map();
let copyCounter = 0;

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

    // Build table from data with per-field copy buttons
    html += '<table class="result-table">';
    let rowIndex = 0;
    for (const [key, value] of Object.entries(data)) {
        if (key === 'error') continue;
        const displayKey = formatKey(key);
        const displayValue = formatValue(value);
        if (displayValue !== '' && displayValue !== 'null' && displayValue !== '[]') {
            const fieldId = `field-${copyCounter}-${rowIndex}`;
            const rawValue = typeof value === 'object' ? JSON.stringify(value) : String(value);
            jsonDataMap.set(fieldId, rawValue);
            html += `<tr><th>${displayKey}</th><td data-label="${escapeHtml(displayKey)}">${displayValue}<button class="btn-copy-field" onclick="copyField('${fieldId}')" title="Salin nilai">📋</button></td></tr>`;
            rowIndex++;
        }
    }
    html += '</table>';

    // Timestamp "Terakhir diperiksa"
    const now = new Date();
    const timeStr = now.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' }) + ' ' + now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
    html += `<div class="result-timestamp">🕐 Diperiksa: ${timeStr}</div>`;

    // Action buttons: Copy JSON + Copy All + Export + Share
    const id = `copy-${copyCounter++}`;
    jsonDataMap.set(id, data);
    const jsonStr = JSON.stringify(data, null, 2);
    html += `<div class="result-actions">
        <button class="btn-copy" onclick="copyJSON('${id}')">📋 Salin JSON</button>
        <button class="btn-copy" onclick="copyAllResults()">📑 Salin Semua</button>
        <button class="btn-copy" onclick="exportResultsAsCSV()">📊 Export CSV</button>
        <button class="btn-copy" onclick="exportResultsAsText()">📄 Export TXT</button>
        <button class="btn-share" onclick="shareTool('${escapeHtml(document.querySelector("h1") ? document.querySelector("h1").textContent.trim() : "Konektivitas.com")}')">🔗 Share</button>
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

// Copy single field value to clipboard
function copyField(fieldId) {
    const text = jsonDataMap.get(fieldId);
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
        showToast('📋 Nilai berhasil disalin!');
    }).catch(() => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('📋 Nilai berhasil disalin!');
    });
}

// Copy JSON to clipboard
function copyJSON(id) {
    const data = jsonDataMap.get(id);
    if (!data) return;
    const json = JSON.stringify(data, null, 2);
    const btn = document.querySelector(`[onclick="copyJSON('${id}')"]`);
    navigator.clipboard.writeText(json).then(() => {
        if (btn) {
            const original = btn.innerHTML;
            btn.innerHTML = '✅ Tersalin!';
            btn.classList.add('copied');
            setTimeout(() => {
                btn.innerHTML = original;
                btn.classList.remove('copied');
            }, 2000);
        }
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = json;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        if (btn) {
            btn.innerHTML = '✅ Tersalin!';
            setTimeout(() => btn.innerHTML = '📋 Salin JSON', 2000);
        }
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

// ============ WEB SHARE API ============
function shareTool(toolName) {
    var url = window.location.href;
    var title = toolName + ' - Konektivitas.com';
    if (navigator.share) {
        navigator.share({ title: title, url: url }).catch(function () { });
    } else {
        copyToClipboard(url);
    }
}

// ============ COPY ALL RESULTS ============
function copyAllResults() {
    var container = document.querySelector('.results');
    if (!container) return;
    var rows = container.querySelectorAll('tr');
    if (rows.length === 0) {
        var pre = container.querySelector('pre');
        if (pre) {
            copyToClipboard(pre.textContent);
            return;
        }
        showToast('Tidak ada hasil untuk disalin');
        return;
    }
    var lines = [];
    rows.forEach(function (row) {
        var th = row.querySelector('th');
        var td = row.querySelector('td');
        if (th && td) {
            lines.push(th.textContent.trim() + ': ' + td.textContent.trim());
        }
    });
    if (lines.length > 0) {
        copyToClipboard(lines.join('\n'));
    }
}

// ============ EXPORT AS TEXT ============
function exportResultsAsText() {
    var container = document.querySelector('.results');
    if (!container) return;
    var title = document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : 'Konektivitas.com';
    var lines = [title, '='.repeat(title.length), ''];
    var rows = container.querySelectorAll('tr');
    if (rows.length > 0) {
        rows.forEach(function (row) {
            var th = row.querySelector('th');
            var td = row.querySelector('td');
            if (th && td) {
                lines.push(th.textContent.trim() + ': ' + td.textContent.trim());
            }
        });
    } else {
        var pre = container.querySelector('pre');
        if (pre) {
            lines.push(pre.textContent);
        } else {
            lines.push(container.textContent.trim());
        }
    }
    lines.push('');
    lines.push('---');
    lines.push('Generated by Konektivitas.com — Memahami. Mengelola. Mengembangkan Internet.');
    lines.push(new Date().toISOString());
    var text = lines.join('\n');
    var blob = new Blob([text], { type: 'text/plain' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = title.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50) + '.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('📄 File berhasil didownload!');
}

// ============ EXPORT AS CSV ============
function exportResultsAsCSV() {
    var container = document.querySelector('.results');
    if (!container) return;
    var title = document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : 'Konektivitas.com';
    var rows = container.querySelectorAll('tr');
    var csvLines = [];
    // BOM for proper UTF-8 encoding in Excel
    csvLines.push('\uFEFF"Field","Value"');
    if (rows.length > 0) {
        rows.forEach(function (row) {
            var th = row.querySelector('th');
            var td = row.querySelector('td');
            if (th && td) {
                var field = th.textContent.trim().replace(/"/g, '""');
                // Get only text content, strip copy button emoji
                var value = td.textContent.trim().replace(/📋/g, '').replace(/"/g, '""').trim();
                csvLines.push('"' + field + '","' + value + '"');
            }
        });
    }
    if (csvLines.length <= 1) {
        showToast('⚠️ Tidak ada data tabel untuk di-export');
        return;
    }
    var csv = csvLines.join('\n');
    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = title.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50) + '.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('📊 CSV berhasil didownload!');
}
