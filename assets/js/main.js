/**
 * main.js
 * PUBLIC RECORD — WE WERE THERE
 * Site-wide JS: nav active state, lazy loading, misc.
 */

(function () {
  'use strict';

  // --- Nav: mark active link based on current path ---
  function setActiveNav() {
    var path = window.location.pathname;
    var links = document.querySelectorAll('.pr-nav__links a');
    links.forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href) return;
      // Exact match or starts-with for section pages
      if (href !== '/' && path.startsWith(href.replace(/\/$/, ''))) {
        link.classList.add('active');
      } else if (href === '/' && (path === '/' || path === '/index.html')) {
        link.classList.add('active');
      }
    });
  }

  // --- Lazy load images that aren't placeholders ---
  function setupLazyLoad() {
    if (!('IntersectionObserver' in window)) return;

    var lazyImages = document.querySelectorAll('img[data-src]');
    if (!lazyImages.length) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    }, { rootMargin: '200px 0px' });

    lazyImages.forEach(function (img) {
      observer.observe(img);
    });
  }

  // --- Init ---
  function init() {
    setActiveNav();
    setupLazyLoad();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
