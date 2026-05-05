// ==========================================
// TEXNORINOK — MAIN JS
// ==========================================

document.addEventListener('DOMContentLoaded', () => {

  // Auto-close messages
  document.querySelectorAll('.message').forEach(msg => {
    setTimeout(() => msg.remove(), 5000);
    msg.querySelector('.msg-close')?.addEventListener('click', () => msg.remove());
  });

  // Sticky header shadow
  const header = document.getElementById('header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.style.boxShadow = window.scrollY > 10 ? '0 2px 20px rgba(0,0,0,0.4)' : 'none';
    });
  }

  // Add to cart AJAX
  document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('.btn-add-cart');
      const original = btn.innerHTML;
      btn.innerHTML = '✓ Qo\'shildi!';
      btn.style.background = '#22c55e';

      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();
        if (data.success) {
          // Update cart badge
          const badge = document.querySelector('.cart-btn .badge');
          if (badge) {
            badge.textContent = data.count;
          } else if (data.count > 0) {
            const cartBtn = document.querySelector('.cart-btn');
            if (cartBtn) {
              const b = document.createElement('span');
              b.className = 'badge';
              b.textContent = data.count;
              cartBtn.appendChild(b);
            }
          }
          showToast(data.message || "Savatga qo'shildi!", 'success');
        }
      } catch (err) {
        showToast('Xatolik yuz berdi', 'error');
      }

      setTimeout(() => {
        btn.innerHTML = original;
        btn.style.background = '';
      }, 2000);
    });
  });

  // Toast notification
  function showToast(message, type = 'success') {
    const container = document.querySelector('.messages-container') || (() => {
      const c = document.createElement('div');
      c.className = 'messages-container';
      document.body.appendChild(c);
      return c;
    })();

    const toast = document.createElement('div');
    toast.className = `message message--${type}`;
    toast.innerHTML = `${message}<button class="msg-close">×</button>`;
    toast.querySelector('.msg-close').addEventListener('click', () => toast.remove());
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  }

  // Hamburger menu
  const hamburger = document.getElementById('hamburger');
  if (hamburger) {
    hamburger.addEventListener('click', () => {
      // Simple mobile nav toggle
      const nav = document.querySelector('.nav-links');
      if (nav) {
        nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        nav.style.flexDirection = 'column';
        nav.style.position = 'absolute';
        nav.style.top = '100%';
        nav.style.left = '0';
        nav.style.right = '0';
        nav.style.background = 'var(--bg)';
        nav.style.padding = '16px 24px';
        nav.style.borderBottom = '1px solid var(--border)';
        nav.style.zIndex = '99';
      }
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href && href !== '#' && href.startsWith('#')) {
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });

  // Intersection Observer for fade-in animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.product-card, .cat-card, .feature-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });

  // Custom visible class
  document.head.insertAdjacentHTML('beforeend', `
    <style>.visible { opacity: 1 !important; transform: translateY(0) !important; }</style>
  `);
});
