/**
 * Modern JavaScript Application
 * Author: Gabriel Demetrios Lafis; Frontend integration by Comet Assistant
 * ES6+ features and modern web APIs
 */
class ApplicationManager {
  constructor() {
    this.initialized = false;
    this.data = new Map();
    this.apiBase = '';
    this.init();
  }

  async init() {
    this.cacheEls();
    this.bindUI();
    await this.refreshStats();
    await this.refreshListings();
    this.startPerformanceMonitoring();
    this.initialized = true;
    console.log('Application initialized successfully');
  }

  cacheEls() {
    this.$form = document.getElementById('filters');
    this.$listings = document.getElementById('listings');
    this.$stats = document.getElementById('stats');
    this.$clear = document.getElementById('clearFilters');
  }

  bindUI() {
    if (this.$form) {
      this.$form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.refreshListings();
      });
    }
    if (this.$clear) {
      this.$clear.addEventListener('click', async () => {
        setTimeout(() => this.refreshListings(), 0);
      });
    }

    // Enhance cards and features if present
    document.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll('.tech-card').forEach((card, idx) => {
        card.style.animationDelay = `${idx * 0.1}s`;
        card.classList.add('fade-in');
      });
    });

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => entry.isIntersecting && entry.target.classList.add('animate-in'));
      }, { threshold: 0.1 });
      document.querySelectorAll('.feature, .tech-card').forEach((el) => observer.observe(el));
    }
  }

  buildQuery() {
    const params = new URLSearchParams();
    const q = document.getElementById('q')?.value?.trim();
    const min = document.getElementById('min_price')?.value;
    const max = document.getElementById('max_price')?.value;
    const type = document.getElementById('type')?.value;
    const beds = document.getElementById('bedrooms')?.value;

    if (q) params.set('q', q);
    if (min) params.set('min_price', min);
    if (max) params.set('max_price', max);
    if (type) params.set('type', type);
    if (beds) params.set('bedrooms', beds);

    return params.toString();
  }

  async refreshStats() {
    try {
      const res = await fetch(`${this.apiBase}/api/stats`);
      const data = await res.json();
      this.$stats.innerHTML = this.renderStats(data);
    } catch (err) {
      console.error('Failed to load stats', err);
    }
  }

  async refreshListings() {
    try {
      const q = this.buildQuery();
      const url = q ? `${this.apiBase}/api/properties?${q}` : `${this.apiBase}/api/properties`;
      const res = await fetch(url);
      const items = await res.json();
      this.$listings.innerHTML = items.map(this.renderCard).join('') || '<p>No results found.</p>';
    } catch (err) {
      console.error('Failed to load properties', err);
      this.$listings.innerHTML = '<p>Failed to load properties.</p>';
    }
  }

  renderStats(s) {
    return `
      <div class="stat-card">
        <strong>Total:</strong> ${s.total_properties}
      </div>
      <div class="stat-card">
        <strong>Available:</strong> ${s.available_properties}
      </div>
      <div class="stat-card">
        <strong>Avg Price:</strong> $${Math.round(s.average_price).toLocaleString()}
      </div>
    `;
  }

  renderCard(p) {
    const features = (p.features || []).slice(0, 4).join(' • ');
    const img = (p.images && p.images[0]) || 'https://via.placeholder.com/600x300?text=Property';
    return `
      <article class="card">
        <img src="${img}" alt="${p.title}" />
        <div class="card-body">
          <h3>${p.title}</h3>
          <p class="muted">${p.address || ''} ${p.city || ''} ${p.state || ''}</p>
          <p>${(p.description || '').slice(0, 120)}...</p>
          <div class="meta">
            <span>$${p.price.toLocaleString()}</span>
            <span>${p.bedrooms} bd • ${p.bathrooms} ba • ${p.area} sqft</span>
          </div>
          <div class="meta">
            <span class="badge">${p.type}</span>
            <span class="muted">${features}</span>
          </div>
        </div>
      </article>
    `;
  }

  startPerformanceMonitoring() {
    if ('performance' in window) {
      const perfData = {
        loadTime: performance.now(),
        memory: navigator.deviceMemory || 'unknown',
        connection: navigator.connection?.effectiveType || 'unknown',
      };
      console.log('Performance metrics:', perfData);
    }
  }
}

// CSS for stats/listings (light inline for demo)
const style = document.createElement('style');
style.textContent = `
  .filters { display:flex; gap:.5rem; flex-wrap:wrap; align-items:center; }
  .stats { display:grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap:1rem; margin-top:1rem; }
  .stat-card { background:#fff; border:1px solid var(--border); padding:1rem; border-radius:.5rem; box-shadow:0 2px 8px rgba(0,0,0,.05); }
  .listings { display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-top:1rem; }
  .card { background:#fff; border-radius:.5rem; overflow:hidden; border:1px solid var(--border); box-shadow:0 4px 16px rgba(0,0,0,.06); }
  .card img { width:100%; height:180px; object-fit:cover; display:block; }
  .card-body { padding:1rem; }
  .card .meta { display:flex; justify-content:space-between; margin-top:.5rem; font-size:.9rem; }
  .badge { background:var(--primary); color:#fff; padding:.15rem .5rem; border-radius:.25rem; font-size:.8rem; }
  .muted { color:#556; opacity:.8; }
`;
document.head.appendChild(style);

// Initialize application
window.addEventListener('DOMContentLoaded', () => new ApplicationManager());
