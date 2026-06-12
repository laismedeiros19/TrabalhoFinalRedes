/**
 * NetWatch — dashboard.js
 * VERSÃO FINAL — 100% CORRIGIDA (Métricas, Gráficos e Segurança via API)
 * IDP · Redes de Computadores · Prof.ª Lorena Borges · 2026
 */

'use strict';

// Detecção inteligente da URL Base do Codespaces para ambas as rotas da API
const getBaseBackendUrl = () => {
    const hostname = window.location.hostname;
    if (hostname.includes('github.dev') || hostname.includes('app.github.dev')) {
        return `https://${hostname.replace('-3000', '-8000')}`;
    }
    return 'http://localhost:8000';
};

const BASE_URL = getBaseBackendUrl();

const CONFIG = {
  apiUrl:         `${BASE_URL}/api/metrics/latest`,
  securityUrl:    `${BASE_URL}/api/security`,
  pollInterval:   5000,      
  historyLength:  20,        
  thresholds: {
    latencyWarn:   200,       
    errorRateWarn: 2,         
  },
};

/* ══════════════════════════════════════════════
   ESTADO HISTÓRICO DOS GRÁFICOS
══════════════════════════════════════════════ */
const history = {
  web:  { labels: [], latency: [], rps: [] },
  db:   { labels: [], cpu: [],     qps: [] },
  dns:  { labels: [], resp: [],    fails: [] },
  smtp: { labels: [], delivery: [], queue: [] },
};

/* ══════════════════════════════════════════════
   INICIALIZAÇÃO DOS GRÁFICOS (CHART.JS)
══════════════════════════════════════════════ */
Chart.defaults.color       = '#6b7280';
Chart.defaults.borderColor     = '#374151';
Chart.defaults.font.family     = 'ui-monospace, monospace';
Chart.defaults.font.size       = 11;

function makeChart(canvasId, ds1, ds2) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label:           ds1.label,
          data:            [],
          borderColor:     ds1.color,
          backgroundColor: ds1.color + '18',
          borderWidth:     1.8,
          pointRadius:     0,
          tension:         0.4,
          fill:            true,
          yAxisID:         'y',
        },
        {
          label:           ds2.label,
          data:            [],
          borderColor:     ds2.color,
          backgroundColor: ds2.color + '18',
          borderWidth:     1.8,
          pointRadius:     0,
          tension:         0.4,
          fill:            true,
          yAxisID:         'y1',
        },
      ],
    },
    options: {
      responsive:          true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { maxTicksLimit: 6 }, grid: { color: '#1f2937' } },
        y: { position: 'left', grid: { color: '#1f293780' } },
        y1: { position: 'right', grid: { drawOnChartArea: false } },
      },
    },
  });
}

const charts = {
  web:  makeChart('chart-web',  { label: 'Latência (ms)', color: '#60a5fa' }, { label: 'RPS',        color: '#34d399' }),
  db:   makeChart('chart-db',   { label: 'CPU (%)',       color: '#a78bfa' }, { label: 'QPS',        color: '#f472b6' }),
  dns:  makeChart('chart-dns',  { label: 'Resp (ms)',     color: '#2dd4bf' }, { label: 'Falhas/s',   color: '#facc15' }),
  smtp: makeChart('chart-smtp', { label: 'Entrega (%)',   color: '#fb923c' }, { label: 'Fila',       color: '#f87171' }),
};

/* ══════════════════════════════════════════════
   HELPERS DE FORMATAÇÃO E UI
══════════════════════════════════════════════ */
function nowTime() { return new Date().toLocaleTimeString('pt-BR', { hour12: false }); }
function setText(id, value) { const el = document.getElementById(id); if (el) el.textContent = value; }
function pushHistory(arr, value) { arr.push(value); if (arr.length > CONFIG.historyLength) arr.shift(); }
function syncChart(chart, labels, d1, d2) {
  chart.data.labels = [...labels]; chart.data.datasets[0].data = [...d1]; chart.data.datasets[1].data = [...d2]; chart.update('active');
}

function calcLevel(availability, latencyMs = 0, errorRatePct = 0) {
  if (availability === 0) return 'crit';
  if (latencyMs > CONFIG.thresholds.latencyWarn || errorRatePct > CONFIG.thresholds.errorRateWarn) return 'warn';
  return 'ok';
}

const BADGE_LABELS = { ok: 'OK', warn: 'Atenção (E-mail)', crit: 'Crítico (E-mail)' };
const BADGE_CLASSES = { ok: ['badge-ok','status-ok'], warn: ['badge-warn','status-warn'], crit: ['badge-crit','status-crit'] };

function applyStatus(service, level) {
  const badge = document.getElementById(`badge-${service}`);
  const card  = document.getElementById(`card-${service}`);
  if (badge && card) {
    badge.className = `status-badge ${BADGE_CLASSES[level][0]}`; badge.textContent = BADGE_LABELS[level];
    card.classList.remove('status-ok', 'status-warn', 'status-crit'); card.classList.add(BADGE_CLASSES[level][1]);
  }
}

/* ══════════════════════════════════════════════
   ATUALIZAÇÃO ATIVA DOS CARDS E GRIDS INFERIORES
══════════════════════════════════════════════ */
function updateWeb(m) {
  const level = calcLevel(m.availability, m.latency_ms, m.error_rate_pct); applyStatus('web', level);
  
  setText('web-latency', `${m.latency_ms.toFixed(1)} ms`); setText('web-rps', Math.round(m.rps));
  setText('web-error', `${m.error_rate_pct.toFixed(1)} %`); setText('web-conn', Math.round(m.active_connections));
  
  setText('cs-web-lat', `${m.latency_ms.toFixed(1)} ms`); setText('cs-web-rps', Math.round(m.rps));
  setText('cs-web-conn', Math.round(m.active_connections)); setText('cs-web-err', `${m.error_rate_pct.toFixed(1)} %`);

  pushHistory(history.web.labels, nowTime()); pushHistory(history.web.latency, m.latency_ms); pushHistory(history.web.rps, m.rps);
  syncChart(charts.web, history.web.labels, history.web.latency, history.web.rps);
}

function updateDb(m) {
  const level = calcLevel(m.availability, 0, m.error_rate_pct); applyStatus('db', level);
  
  setText('db-cpu', `${m.cpu_pct.toFixed(1)} %`); setText('db-qps', Math.round(m.qps));
  setText('db-slow', m.slow_queries); setText('db-size', `${m.size_gb.toFixed(3)} GB`);
  
  setText('cs-db-cpu', `${m.cpu_pct.toFixed(1)} %`);
  setText('cs-db-mem', `${(m.memory_usage || 55.0).toFixed(1)} %`);
  setText('cs-db-qps', Math.round(m.qps));
  setText('cs-db-conn', Math.round(m.active_connections || 15));
  setText('cs-db-slow', m.slow_queries);
  setText('cs-db-err', `${m.error_rate_pct.toFixed(1)} %`);
  setText('cs-db-size', `${m.size_gb.toFixed(3)} GB`);

  pushHistory(history.db.labels, nowTime()); pushHistory(history.db.cpu, m.cpu_pct); pushHistory(history.db.qps, m.qps);
  syncChart(charts.db, history.db.labels, history.db.cpu, history.db.qps);
}

function updateDns(m) {
  const level = calcLevel(m.availability, m.response_ms); applyStatus('dns', level);
  
  setText('dns-resp', `${m.response_ms.toFixed(1)} ms`); setText('dns-qps', Math.round(m.qps));
  setText('dns-fail', m.failed_resolutions); setText('dns-up', `${m.availability} %`);
  
  setText('cs-dns-resp', `${m.response_ms.toFixed(1)} ms`); setText('cs-dns-qps', Math.round(m.qps));
  setText('cs-dns-fail', m.failed_resolutions); setText('cs-dns-up', `${m.availability} %`);

  pushHistory(history.dns.labels, nowTime()); pushHistory(history.dns.resp, m.response_ms); pushHistory(history.dns.fails, m.failed_resolutions);
  syncChart(charts.dns, history.dns.labels, history.dns.resp, history.dns.fails);
}

function updateSmtp(m) {
  const level = calcLevel(m.availability, m.latency_ms, m.error_rate_pct); applyStatus('smtp', level);
  
  setText('smtp-delivery', `${m.delivery_rate_pct.toFixed(1)} %`); setText('smtp-queue', m.queue_length);
  setText('smtp-lat', `${m.latency_ms.toFixed(1)} ms`); setText('smtp-err', `${m.error_rate_pct.toFixed(1)} %`);
  
  setText('cs-smtp-del', `${m.delivery_rate_pct.toFixed(1)} %`); setText('cs-smtp-q', m.queue_length);
  setText('cs-smtp-lat', `${m.latency_ms.toFixed(1)} ms`); setText('cs-smtp-err', `${m.error_rate_pct.toFixed(1)} %`);
  setText('cs-smtp-vol', `${Math.round(m.volume_per_minute || 45)}/m`);

  pushHistory(history.smtp.labels, nowTime()); pushHistory(history.smtp.delivery, m.delivery_rate_pct); pushHistory(history.smtp.queue, m.queue_length);
  syncChart(charts.smtp, history.smtp.labels, history.smtp.delivery, history.smtp.queue);
}

/* ══════════════════════════════════════════════
   INTEGRAÇÃO REAL DO PAINEL DE SEGURANÇA (API)
══════════════════════════════════════════════ */
const CAT_META = {
  ddos:   { label: 'DDoS / Anomalia',   cls: 'cat-ddos'  },
  brute:  { label: 'Brute-force',       cls: 'cat-brute' },
  config: { label: 'Config. Alterada',  cls: 'cat-config' },
  vuln:   { label: 'Vulnerabilidade',   cls: 'cat-vuln'   },
};

const LEVEL_META = {
  crit: { label: 'Crítico', cls: 'sec-badge-crit' },
  warn: { label: 'Atenção', cls: 'sec-badge-warn' },
  info: { label: 'Info',    cls: 'sec-badge-info' },
};

let _secFeed = [];

async function fetchSecurityEvents() {
    try {
        const res = await fetch(CONFIG.securityUrl);
        if (!res.ok) throw new Error();
        const data = await res.json();
        
        _secFeed = data.map(item => {
            const alertTime = item.timestamp ? item.timestamp.split("T")[1].substring(0, 8) : nowTime();
            return {
                cat: item.event_type,
                level: item.severity.toLowerCase(),
                service: item.service,
                desc: item.description,
                ip: item.source_ip,
                time: alertTime
            };
        });
        renderFeed();
    } catch (e) {
        console.log("Erro ao carregar feed de segurança da API.");
    }
}

function renderSecRow(alert) {
  const cat = CAT_META[alert.cat] || { label: alert.cat, cls: 'cat-ddos' };
  const lvl = LEVEL_META[alert.level] || { label: alert.level, cls: 'sec-badge-info' };

  return `<tr class="sec-row">
    <td class="sec-td"><span class="sec-badge ${lvl.cls}">${lvl.label}</span></td>
    <td class="sec-td"><span class="cat-chip ${cat.cls}">${cat.label}</span></td>
    <td class="sec-td text-gray-300">${alert.service}</td>
    <td class="sec-td-desc">${alert.desc}</td>
    <td class="sec-td"><span class="ip-mono">${alert.ip}</span></td>
    <td class="sec-td"><span class="time-mono">${alert.time}</span></td>
  </tr>`;
}

function updateSecCounts() {
  const counts = { ddos: 0, brute: 0, config: 0, vuln: 0 };
  _secFeed.forEach(a => { if (counts[a.cat] !== undefined) counts[a.cat]++; });
  setText('sec-cnt-ddos',  counts.ddos); setText('sec-cnt-brute', counts.brute);
  setText('sec-cnt-cfg',   counts.config); setText('sec-cnt-vuln',  counts.vuln);
  setText('sec-count',     _secFeed.length);
}

function renderFeed() {
  const tbody = document.getElementById('sec-feed');
  if (!tbody) return;
  if (_secFeed.length === 0) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="6">Nenhum alerta registrado no banco SQLite.</td></tr>'; return;
  }
  tbody.innerHTML = _secFeed.map(renderSecRow).join('');
  updateSecCounts();
}

function refreshSecurityFeed() { fetchSecurityEvents(); }

/* ══════════════════════════════════════════════
   POLLING CENTRALIZADO E SEGURO
══════════════════════════════════════════════ */
let _consecutiveErrors = 0;

async function fetchAndUpdate() {
  let data = null;
  try {
    const res = await fetch(CONFIG.apiUrl, { signal: AbortSignal.timeout(4000) });
    if (!res.ok) throw new Error();
    const rawLogs = await res.json();
    _consecutiveErrors = 0; setConnectionStatus(true);

    data = {
      web: { availability: 100, latency_ms: 0, rps: 0, error_rate_pct: 0, active_connections: 0 },
      db: { availability: 100, cpu_pct: 0, qps: 0, slow_queries: 0, size_gb: 12.4, error_rate_pct: 0 },
      dns: { availability: 100, response_ms: 0, qps: 0, failed_resolutions: 0 },
      smtp: { availability: 100, delivery_rate_pct: 100, queue_length: 0, latency_ms: 0, error_rate_pct: 0 }
    };

    rawLogs.slice().reverse().forEach(log => {
        let srv = log.service === 'database' ? 'db' : log.service;
        if (!data[srv]) return;
        
        if (log.metric_name === 'latency') {
            data[srv].latency_ms = log.value; data[srv].response_ms = log.value;
        } else if (log.metric_name === 'error_rate') {
            data[srv].error_rate_pct = log.value;
        } else if (log.metric_name === 'cpu_usage') {
            data[srv].cpu_pct = log.value;
        } else if (log.metric_name === 'open_connections') {
            data[srv].active_connections = log.value;
        } else if (log.metric_name === 'db_size') {
            data[srv].size_gb = log.value;
        } else if (log.metric_name === 'delivery_rate') {
            data[srv].delivery_rate_pct = log.value;
        } else if (log.metric_name === 'availability') {
            data[srv].availability = log.value === 1.0 ? 100 : 0;
        } else {
            data[srv][log.metric_name] = log.value;
        }
    });

  } catch (error) {
    _consecutiveErrors++; if (_consecutiveErrors >= 2) setConnectionStatus(false);
  }

  if (data) {
    updateWeb(data.web); updateDb(data.db); updateDns(data.dns); updateSmtp(data.smtp);
  }
  setText('last-update', `Atualizado: ${nowTime()}`);
}

function setConnectionStatus(online) {
  const badge = document.getElementById('conn-badge');
  if (badge) {
    badge.className = online ? 'status-badge badge-ok' : 'status-badge badge-crit';
    badge.textContent = online ? 'Conectado' : 'Offline';
  }
}

// Inicialização das rotas síncronas
function init() { 
    fetchAndUpdate(); fetchSecurityEvents();
    setInterval(fetchAndUpdate, CONFIG.pollInterval); 
    setInterval(fetchSecurityEvents, CONFIG.pollInterval);
}
if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }