// ==========================================
// TEXNORINOK — MAIN JS
// ==========================================

document.addEventListener('DOMContentLoaded', () => {

  // --- REVEAL ON SCROLL ANIMATION ---
  const revealElements = document.querySelectorAll('[data-reveal]');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        // If it's a grid, reveal children with delay
        const children = entry.target.querySelectorAll('.reveal-item');
        children.forEach((child, i) => {
          setTimeout(() => child.classList.add('revealed'), i * 100);
        });
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  revealElements.forEach(el => revealObserver.observe(el));

  // Auto-apply reveal to common elements
  document.querySelectorAll('.product-card, .cat-card, .feature-item, .section-header, .hero-content > *').forEach((el, i) => {
    el.setAttribute('data-reveal', '');
    if (i < 8) el.classList.add('reveal-delay-' + (i % 3 + 1));
  });

  // --- MOBILE MENU ---
  const hamburger = document.getElementById('hamburger');
  const body = document.body;
  
  if (hamburger) {
    // Create mobile menu dynamically if it doesn't exist
    let mobileNav = document.querySelector('.mobile-nav');
    if (!mobileNav) {
      mobileNav = document.createElement('div');
      mobileNav.className = 'mobile-nav';
      const navLinks = document.querySelector('.nav-links')?.innerHTML || '';
      mobileNav.innerHTML = `
        <div class="mobile-nav-close">×</div>
        <div style="display:flex; flex-direction:column; gap:20px; margin-top:20px;">
          ${navLinks}
        </div>
      `;
      body.appendChild(mobileNav);
      
      const overlay = document.createElement('div');
      overlay.className = 'mobile-nav-overlay';
      body.appendChild(overlay);
      
      const closeBtn = mobileNav.querySelector('.mobile-nav-close');
      const toggleMenu = (show) => {
        mobileNav.classList.toggle('active', show);
        overlay.classList.toggle('active', show);
        body.style.overflow = show ? 'hidden' : '';
      };
      
      hamburger.addEventListener('click', () => toggleMenu(true));
      closeBtn.addEventListener('click', () => toggleMenu(false));
      overlay.addEventListener('click', () => toggleMenu(false));
    }
  }

  // --- AJAX ADD TO CART ---
  document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('.btn-add-cart');
      const original = btn.innerHTML;
      btn.innerHTML = '✓';
      btn.style.width = btn.offsetWidth + 'px'; // Keep width
      
      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();
        if (data.success) {
          updateCartBadge(data.count);
          showToast(data.message || "Savatga qo'shildi!", 'success');
        }
      } catch (err) {
        showToast('Xatolik yuz berdi', 'error');
      }
      setTimeout(() => { btn.innerHTML = original; btn.style.width = ''; }, 2000);
    });
  });

  function updateCartBadge(count) {
    const badge = document.querySelector('.cart-btn .badge');
    if (badge) {
      badge.textContent = count;
      badge.style.transform = 'scale(1.2)';
      setTimeout(() => badge.style.transform = 'scale(1)', 200);
    } else if (count > 0) {
      const cartBtn = document.querySelector('.cart-btn');
      if (cartBtn) {
        const b = document.createElement('span');
        b.className = 'badge';
        b.textContent = count;
        cartBtn.appendChild(b);
      }
    }
  }

  function showToast(message, type = 'success') {
    const container = document.querySelector('.messages-container') || (() => {
      const c = document.createElement('div');
      c.className = 'messages-container';
      document.body.appendChild(c);
      return c;
    })();

    const toast = document.createElement('div');
    toast.className = `message message--${type}`;
    toast.innerHTML = `<span>${message}</span><button class="msg-close">×</button>`;
    toast.querySelector('.msg-close').addEventListener('click', () => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(20px)';
      setTimeout(() => toast.remove(), 300);
    });
    container.appendChild(toast);
    setTimeout(() => {
      if (toast.parentElement) {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 300);
      }
    }, 4000);
  }

  // --- UTILS ---
  document.querySelectorAll('img').forEach(img => {
    if (!img.getAttribute('loading')) img.setAttribute('loading', 'lazy');
  });

  // Sticky Header
  const header = document.getElementById('header');
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    if (currentScroll > 50) {
      header.style.background = 'rgba(13, 13, 15, 0.95)';
      header.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
    } else {
      header.style.background = 'rgba(13, 13, 15, 0.85)';
      header.style.boxShadow = 'none';
    }
    lastScroll = currentScroll;
  });
});
