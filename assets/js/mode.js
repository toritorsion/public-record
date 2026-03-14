/**
 * mode.js — Dark / Light mode toggle for PUBLIC RECORD
 * Persists to localStorage. Applies .dark-mode class to <body>.
 */
(function () {
  'use strict';

  var DARK = 'dark-mode';
  var KEY  = 'pr-mode';

  // Apply saved preference before paint to avoid flash
  if (localStorage.getItem(KEY) === 'dark') {
    document.documentElement.classList.add(DARK);
    document.body && document.body.classList.add(DARK);
  }

  function init() {
    // Re-apply in case body wasn't ready above
    if (localStorage.getItem(KEY) === 'dark') {
      document.body.classList.add(DARK);
    }

    var btn = document.getElementById('mode-toggle');
    if (!btn) return;

    btn.addEventListener('click', function () {
      document.body.classList.toggle(DARK);
      document.documentElement.classList.toggle(DARK);
      var isDark = document.body.classList.contains(DARK);
      localStorage.setItem(KEY, isDark ? 'dark' : 'light');
      btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
