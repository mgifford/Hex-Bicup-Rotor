/* ═══════════════════════════════════════════════════════
   VINDSNURR site-wide JavaScript
   Shared by all pages in docs/
   ═══════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Theme toggle ──────────────────────────────────── */
  const toggle      = document.getElementById('theme-toggle');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
  const saved       = localStorage.getItem('vindsnurr-theme');
  let   current     = saved || (prefersDark.matches ? 'dark' : 'light');
  let   userSet     = !!saved;

  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    if (toggle) {
      toggle.setAttribute('aria-label',
        t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    }
  }

  if (toggle) {
    toggle.addEventListener('click', function () {
      current = current === 'light' ? 'dark' : 'light';
      userSet = true;
      localStorage.setItem('vindsnurr-theme', current);
      applyTheme(current);
    });
  }

  prefersDark.addEventListener('change', function (e) {
    if (!userSet) {
      current = e.matches ? 'dark' : 'light';
      applyTheme(current);
    }
  });

  applyTheme(current);

  /* ── Mark current nav link ─────────────────────────── */
  const path  = window.location.pathname;
  const links = document.querySelectorAll('.site-nav a');
  links.forEach(function (a) {
    const href = a.getAttribute('href');
    if (!href) return;
    // Exact match, or index.html for root path
    const isHome = (href === 'index.html' || href === './') &&
                   (path.endsWith('/') || path.endsWith('/index.html'));
    const isPage = !isHome && path.endsWith(href.replace('./', ''));
    if (isHome || isPage) {
      a.setAttribute('aria-current', 'page');
    }
  });
})();
