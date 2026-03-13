/**
 * inspect.js
 * Reusable image zoom module for PUBLIC RECORD.
 * Applies to any element with [data-inspect] attribute.
 *
 * Desktop: scale(1.06) on hover, 900ms ease transition.
 * Mobile: no scale — falls back to browser's native pinch-zoom.
 */

(function () {
  'use strict';

  function initInspect() {
    const isMobile = window.matchMedia('(max-width: 767px)').matches;
    if (isMobile) return; // Let native pinch handle it

    const targets = document.querySelectorAll('[data-inspect]');

    targets.forEach(function (el) {
      // Wrap in .pr-inspect container if not already
      if (!el.classList.contains('pr-inspect') && !el.closest('.pr-inspect')) {
        el.classList.add('pr-inspect');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initInspect);
  } else {
    initInspect();
  }
})();
