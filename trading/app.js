const STORAGE_KEY = 'paper-trader-v1';
const STARTING_CASH = 10000;
const TICK_MS = 1000;
const HISTORY_POINTS = 120;

// Fictional symbols so nobody mistakes simulated prices for real quotes.
const SYMBOLS = [
  { symbol: 'NOVA', start: 142.5, vol: 0.004 },
  { symbol: 'QBIT', start: 58.2, vol: 0.007 },
  { symbol: 'HELX', start: 23.9, vol: 0.01 },
  { symbol: 'ORBT', start: 310.0, vol: 0.003 },
  { symbol: 'FERN', start: 8.75, vol: 0.012 },
];

const market = {};
let selected = SYMBOLS[0].symbol;
let account = loadAccount();

function freshAccount() {
  return { cash: STARTING_CASH, positions: {}, trades: [] };
}

function loadAccount() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (saved && typeof saved.cash === 'number') return saved;
  } catch {
    // Missing or unreadable storage; start fresh.
  }
  return freshAccount();
}

function saveAccount() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(account));
  } catch {
    // Storage unavailable; the account lasts for this page view only.
  }
}

// Random walk with slight mean reversion toward the starting price.
function nextPrice(prev, cfg) {
  const shock = (Math.random() - 0.5) * 2 * cfg.vol;
  const pull = ((cfg.start - prev) / cfg.start) * 0.002;
  return Math.max(0.01, prev * (1 + shock + pull));
}

function initMarket() {
  SYMBOLS.forEach((cfg) => {
    const history = [cfg.start];
    for (let i = 1; i < HISTORY_POINTS; i++) history.push(nextPrice(history[i - 1], cfg));
    market[cfg.symbol] = { cfg, history, open: history[0] };
  });
}

function tick() {
  Object.values(market).forEach((m) => {
    m.history.push(nextPrice(m.history[m.history.length - 1], m.cfg));
    if (m.history.length > HISTORY_POINTS) m.history.shift();
  });
  render();
}

const price = (symbol) => {
  const h = market[symbol].history;
  return h[h.length - 1];
};

const money = (n) => n.toLocaleString(undefined, { style: 'currency', currency: 'USD' });
const signed = (n) => (n >= 0 ? '+' : '') + money(n);
const pct = (n) => (n >= 0 ? '+' : '') + (n * 100).toFixed(2) + '%';
const tone = (n) => (n > 0 ? 'up' : n < 0 ? 'down' : '');

function positionsValue() {
  return Object.entries(account.positions).reduce((sum, [s, p]) => sum + p.qty * price(s), 0);
}

function placeOrder(side, symbol, qty) {
  const px = price(symbol);
  const pos = account.positions[symbol];

  if (side === 'buy') {
    const cost = px * qty;
    if (cost > account.cash) return `Not enough cash: need ${money(cost)}, have ${money(account.cash)}.`;
    account.cash -= cost;
    const prevQty = pos ? pos.qty : 0;
    const prevCost = pos ? pos.avg * pos.qty : 0;
    account.positions[symbol] = { qty: prevQty + qty, avg: (prevCost + cost) / (prevQty + qty) };
  } else {
    if (!pos || pos.qty < qty) return `You only hold ${pos ? pos.qty : 0} ${symbol}. Short selling isn't supported.`;
    account.cash += px * qty;
    pos.qty -= qty;
    if (pos.qty === 0) delete account.positions[symbol];
  }

  account.trades.unshift({ time: Date.now(), side, symbol, qty, price: px });
  saveAccount();
  return null;
}

function renderStats() {
  const pv = positionsValue();
  const equity = account.cash + pv;
  const pnl = equity - STARTING_CASH;
  document.getElementById('cash').textContent = money(account.cash);
  document.getElementById('positions-value').textContent = money(pv);
  document.getElementById('equity').textContent = money(equity);
  const pnlEl = document.getElementById('pnl');
  pnlEl.textContent = signed(pnl);
  pnlEl.className = 'value ' + tone(pnl);
}

function renderWatchlist() {
  const body = document.getElementById('watchlist');
  body.innerHTML = '';
  SYMBOLS.forEach(({ symbol }) => {
    const m = market[symbol];
    const change = price(symbol) / m.open - 1;
    const tr = document.createElement('tr');
    tr.className = symbol === selected ? 'is-selected' : '';
    tr.tabIndex = 0;
    tr.innerHTML = `<td>${symbol}</td><td class="num">${money(price(symbol))}</td><td class="num ${tone(change)}">${pct(change)}</td>`;
    const pick = () => { selected = symbol; render(); };
    tr.addEventListener('click', pick);
    tr.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
    body.appendChild(tr);
  });
}

function renderChart() {
  const canvas = document.getElementById('chart');
  const dpr = window.devicePixelRatio || 1;
  const width = canvas.clientWidth;
  const height = 220;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);

  const data = market[selected].history;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const pad = (max - min) * 0.1 || 1;
  const lo = min - pad;
  const hi = max + pad;
  const x = (i) => (i / (data.length - 1)) * width;
  const y = (v) => height - ((v - lo) / (hi - lo)) * height;

  const styles = getComputedStyle(document.documentElement);
  const up = data[data.length - 1] >= data[0];
  const color = styles.getPropertyValue(up ? '--up' : '--down').trim();

  ctx.clearRect(0, 0, width, height);

  ctx.strokeStyle = styles.getPropertyValue('--border').trim();
  ctx.lineWidth = 1;
  for (let i = 1; i < 4; i++) {
    const gy = Math.round((height / 4) * i) + 0.5;
    ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(width, gy); ctx.stroke();
  }

  ctx.beginPath();
  data.forEach((v, i) => (i ? ctx.lineTo(x(i), y(v)) : ctx.moveTo(x(i), y(v))));
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.stroke();

  ctx.lineTo(width, height);
  ctx.lineTo(0, height);
  ctx.closePath();
  ctx.globalAlpha = 0.12;
  ctx.fillStyle = color;
  ctx.fill();
  ctx.globalAlpha = 1;

  document.getElementById('chart-title').textContent = selected;
  document.getElementById('chart-price').textContent = money(price(selected));
}

function renderOrderForm() {
  const side = document.querySelector('input[name=side]:checked').value;
  const qty = parseInt(document.getElementById('qty').value, 10) || 0;
  document.getElementById('estimate').textContent = money(qty * price(selected));
  const submit = document.getElementById('submit');
  submit.textContent = `${side === 'buy' ? 'Buy' : 'Sell'} ${selected}`;
  submit.classList.toggle('btn--sell', side === 'sell');
}

function renderPositions() {
  const body = document.getElementById('positions');
  body.innerHTML = '';
  const entries = Object.entries(account.positions);
  document.getElementById('no-positions').hidden = entries.length > 0;
  entries.forEach(([symbol, p]) => {
    const value = p.qty * price(symbol);
    const unreal = value - p.avg * p.qty;
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${symbol}</td><td class="num">${p.qty}</td><td class="num">${money(p.avg)}</td><td class="num">${money(value)}</td><td class="num ${tone(unreal)}">${signed(unreal)}</td>`;
    body.appendChild(tr);
  });
}

function renderHistory() {
  const body = document.getElementById('history');
  body.innerHTML = '';
  document.getElementById('no-history').hidden = account.trades.length > 0;
  account.trades.slice(0, 50).forEach((t) => {
    const tr = document.createElement('tr');
    const time = new Date(t.time).toLocaleTimeString();
    tr.innerHTML = `<td>${time}</td><td class="${t.side === 'buy' ? 'up' : 'down'}">${t.side.toUpperCase()}</td><td>${t.symbol}</td><td class="num">${t.qty}</td><td class="num">${money(t.price)}</td>`;
    body.appendChild(tr);
  });
}

function render() {
  renderStats();
  renderWatchlist();
  renderChart();
  renderOrderForm();
  renderPositions();
  renderHistory();
}

function setupForm() {
  const form = document.getElementById('order-form');
  const msg = document.getElementById('order-msg');
  form.addEventListener('input', renderOrderForm);
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const side = form.side.value;
    const qty = parseInt(document.getElementById('qty').value, 10);
    if (!Number.isInteger(qty) || qty < 1) {
      msg.textContent = 'Enter a whole number of shares.';
      msg.className = 'order-msg down';
      return;
    }
    const fillPrice = price(selected);
    const error = placeOrder(side, selected, qty);
    msg.textContent = error || `Filled: ${side} ${qty} ${selected} @ ${money(fillPrice)}`;
    msg.className = 'order-msg ' + (error ? 'down' : 'up');
    render();
  });

  document.getElementById('reset').addEventListener('click', () => {
    if (!confirm('Reset to $10,000 cash and clear all positions and trades?')) return;
    account = freshAccount();
    saveAccount();
    msg.textContent = '';
    render();
  });
}

initMarket();
setupForm();
render();
setInterval(tick, TICK_MS);
window.addEventListener('resize', renderChart);
