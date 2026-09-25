const AGE_KEY = 'cloudnine-age-verified';

const products = [
  { name: 'Vaporesso XROS 4', category: 'device', blurb: 'Compact pod system with adjustable airflow.', price: 34.99 },
  { name: 'Uwell Caliburn G3', category: 'device', blurb: 'Long battery life and a rich, smooth draw.', price: 29.99 },
  { name: 'Aspire Flexus Q', category: 'device', blurb: 'Simple, draw-activated starter kit.', price: 24.99 },
  { name: 'XROS Replacement Pods (4-pack)', category: 'pod', blurb: '0.8Ω mesh pods, refillable.', price: 12.99 },
  { name: 'Caliburn G3 Pods (4-pack)', category: 'pod', blurb: '0.6Ω and 0.9Ω options available.', price: 13.99 },
  { name: 'Classic Tobacco 10ml', category: 'liquid', blurb: 'Nic salt, 10mg or 20mg.', price: 5.99 },
  { name: 'Fresh Mint 10ml', category: 'liquid', blurb: 'Nic salt, 10mg or 20mg.', price: 5.99 },
  { name: 'Nicotine-free Berry 50ml', category: 'liquid', blurb: 'Shortfill, 0mg.', price: 11.99 },
];

const categoryLabels = { device: 'Device', pod: 'Pods', liquid: 'E-liquid' };

function renderProducts(filter) {
  const grid = document.getElementById('product-grid');
  grid.innerHTML = '';
  products
    .filter((p) => filter === 'all' || p.category === filter)
    .forEach((p) => {
      const li = document.createElement('li');
      li.className = 'product';
      li.innerHTML = `
        <span class="product__tag">${categoryLabels[p.category]}</span>
        <h3></h3>
        <p></p>
        <span class="product__price">$${p.price.toFixed(2)}</span>`;
      li.querySelector('h3').textContent = p.name;
      li.querySelector('p').textContent = p.blurb;
      grid.appendChild(li);
    });
}

function setupFilters() {
  const buttons = document.querySelectorAll('.filter');
  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      buttons.forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      renderProducts(btn.dataset.filter);
    });
  });
}

function readVerified() {
  try {
    return localStorage.getItem(AGE_KEY) === 'yes';
  } catch {
    return false;
  }
}

function setupAgeGate() {
  if (readVerified()) return;

  const gate = document.getElementById('age-gate');
  gate.hidden = false;
  document.body.classList.add('is-gated');

  document.getElementById('age-yes').addEventListener('click', () => {
    try {
      localStorage.setItem(AGE_KEY, 'yes');
    } catch {
      // Storage unavailable; the gate will show again next visit.
    }
    gate.hidden = true;
    document.body.classList.remove('is-gated');
  });

  document.getElementById('age-no').addEventListener('click', () => {
    document.getElementById('age-denied').hidden = false;
    document.querySelector('.age-gate__actions').hidden = true;
  });
}

document.getElementById('year').textContent = new Date().getFullYear();
setupAgeGate();
renderProducts('all');
setupFilters();
