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

  // --- Dropdown nav toggle ---
  function setupDropdowns() {
    var dropdowns = document.querySelectorAll('.pr-nav__dropdown');
    if (!dropdowns.length) return;
    dropdowns.forEach(function(dd) {
      var trigger = dd.querySelector('.pr-nav__dropdown-trigger');
      if (!trigger) return;

      function openDropdown() {
        dropdowns.forEach(function(d) {
          if (d !== dd) {
            d.classList.remove('is-open');
            var otherTrigger = d.querySelector('.pr-nav__dropdown-trigger');
            if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
          }
        });
        dd.classList.add('is-open');
        trigger.setAttribute('aria-expanded', 'true');
      }

      function closeDropdown() {
        dd.classList.remove('is-open');
        trigger.setAttribute('aria-expanded', 'false');
      }

      dd.addEventListener('mouseenter', openDropdown);
      dd.addEventListener('mouseleave', closeDropdown);

      trigger.addEventListener('click', function(e) {
        e.stopPropagation();
        var isOpen = dd.classList.contains('is-open');
        dropdowns.forEach(function(d) {
          d.classList.remove('is-open');
          var t = d.querySelector('.pr-nav__dropdown-trigger');
          if (t) t.setAttribute('aria-expanded', 'false');
        });
        if (!isOpen) {
          openDropdown();
        }
      });
    });
    document.addEventListener('click', function() {
      dropdowns.forEach(function(dd) {
        dd.classList.remove('is-open');
        var t = dd.querySelector('.pr-nav__dropdown-trigger');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // --- Ensure dropdown includes a PUBLIC RECORD landing link sitewide ---
  function ensurePublicRecordLandingLink() {
    var dropdownLists = document.querySelectorAll('.pr-nav__dropdown-items');
    if (!dropdownLists.length) return;

    dropdownLists.forEach(function (list) {
      if (list.querySelector('a[href="/"]')) return;

      var li = document.createElement('li');
      var a = document.createElement('a');
      a.className = 'nav-meta';
      a.href = '/';
      a.textContent = 'Public Record';
      li.appendChild(a);

      list.insertBefore(li, list.firstChild);
    });
  }

  // --- Gallery randomizer (residual context sheet) ---
  function randomizeGallery() {
    var gallery = document.querySelector('.pr-gallery--randomize');
    if (!gallery) return;
    var items = Array.from(gallery.children);
    for (var i = items.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      gallery.appendChild(items[j]);
      var tmp = items[i]; items[i] = items[j]; items[j] = tmp;
    }
  }

  // --- Lightbox ---
  function setupLightbox() {
    var triggers = document.querySelectorAll('main img:not(.pr-lightbox__img)');
    if (!triggers.length) return;

    // Build lightbox DOM once
    var lb = document.createElement('div');
    lb.className = 'pr-lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<div class="pr-lightbox__stage">' +
      '<button class="pr-lightbox__btn pr-lightbox__prev" aria-label="Previous">&#8592;</button>' +
      '<div class="pr-lightbox__viewport">' +
        '<button class="pr-lightbox__close" aria-label="Close">&#10005;</button>' +
        '<div class="pr-lightbox__frame">' +
          '<img class="pr-lightbox__img" src="" alt="">' +
        '</div>' +
        '<div class="pr-lightbox__count"></div>' +
      '</div>' +
      '<button class="pr-lightbox__btn pr-lightbox__next" aria-label="Next">&#8594;</button>' +
    '</div>';
    document.body.appendChild(lb);

    var img = lb.querySelector('.pr-lightbox__img');
    var count = lb.querySelector('.pr-lightbox__count');
    var images = Array.from(triggers);
    var current = 0;

    function open(idx) {
      current = (idx + images.length) % images.length;
      var src = images[current].currentSrc || images[current].dataset.lightbox || images[current].src;
      var alt = images[current].alt || '';
      img.src = src;
      img.alt = alt;
      count.textContent = (current + 1) + ' / ' + images.length;
      lb.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    }

    function close() {
      lb.classList.remove('is-open');
      document.body.style.overflow = '';
      img.removeAttribute('src');
    }

    images.forEach(function(el, i) {
      el.setAttribute('data-lightbox', el.currentSrc || el.getAttribute('src'));
      el.style.cursor = 'zoom-in';
      el.addEventListener('click', function() { open(i); });
    });

    lb.querySelector('.pr-lightbox__prev').addEventListener('click', function(e) {
      e.stopPropagation(); open(current - 1);
    });
    lb.querySelector('.pr-lightbox__next').addEventListener('click', function(e) {
      e.stopPropagation(); open(current + 1);
    });
    lb.querySelector('.pr-lightbox__close').addEventListener('click', function(e) {
      e.stopPropagation(); close();
    });
    lb.addEventListener('click', function(e) {
      if (e.target === lb) close();
    });
    document.addEventListener('keydown', function(e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'ArrowLeft') open(current - 1);
      else if (e.key === 'ArrowRight') open(current + 1);
      else if (e.key === 'Escape') close();
    });
  }

  // --- Head: ensure favicon assets are present sitewide ---
  function ensureFavicons() {
    var head = document.head;
    if (!head) return;
    if (!head.querySelector('link[rel="icon"]')) {
      var icon32 = document.createElement('link');
      icon32.rel = 'icon';
      icon32.type = 'image/png';
      icon32.sizes = '32x32';
      icon32.href = '/assets/images/branding/favicon-32.png';
      head.appendChild(icon32);
    }
    if (!head.querySelector('link[rel="apple-touch-icon"]')) {
      var apple = document.createElement('link');
      apple.rel = 'apple-touch-icon';
      apple.href = '/assets/images/branding/favicon-48.png';
      head.appendChild(apple);
    }
  }

  // --- Lower site section: keep newsletter + footer structure consistent sitewide ---
  function ensureSiteLower() {
    var footer = document.querySelector('.pr-footer');
    if (!footer || footer.closest('.pr-site-lower')) return;

    var wrapper = document.createElement('div');
    wrapper.className = 'pr-site-lower';
    wrapper.innerHTML = '' +
      '<section class="pr-section--sm">' +
        '<div class="pr-container">' +
          '<div class="pr-spread">' +
            '<div>' +
              '<div class="pr-email-heading">Stay in the Record</div>' +
            '</div>' +
            '<div>' +
              '<p class="u-mb-gap">New work, print releases, and what comes next &mdash; from Chicago, when it matters.</p>' +
              '<form action="https://buttondown.com/toritorsion/embed" method="post" target="popupwindow" onsubmit="window.open(\'https://buttondown.com/toritorsion\', \'popupwindow\')" class="pr-email-form" aria-label="Subscribe form">' +
                '<input type="email" name="email" class="pr-email-form__input" placeholder="your@email.com" required>' +
                '<input type="hidden" value="1" name="embed">' +
                '<button class="pr-btn" type="submit">Subscribe</button>' +
              '</form>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</section>';

    footer.parentNode.insertBefore(wrapper, footer);
    wrapper.appendChild(footer);
  }

  // --- Footer: standardize core essentials sitewide ---
  function enhanceFooter() {
    var footer = document.querySelector('.pr-footer');
    if (!footer || footer.classList.contains('pr-footer--enhanced')) return;

    var year = new Date().getFullYear();
    footer.classList.add('pr-footer--enhanced');
    footer.innerHTML = '' +
      '<div class="pr-container">' +
        '<div class="pr-footer__brand-row">' +
          '<a class="pr-footer__brand-logo-link" href="/overview/" aria-label="Overview">' +
            '<img class="pr-footer__brand-logo" src="/assets/images/branding/tori-full-logo-reverse.png" alt="Tori Torsion">' +
          '</a>' +
          '<p class="pr-footer__cta">Let&apos;s capture your story.</p>' +
          '<a href="/about/#contact" class="pr-btn pr-footer__cta-btn">Contact Me</a>' +
        '</div>' +
        '<div class="pr-footer__grid">' +
          '<div class="pr-footer__col">' +
            '<h3 class="pr-footer__heading">Contact</h3>' +
            '<p class="pr-footer__text"><a class="pr-footer__link" href="mailto:hello@toritorsion.com">hello@toritorsion.com</a></p>' +
            '<p class="pr-footer__text"><a class="pr-footer__link" href="/about/#contact">Contact Form</a></p>' +
          '</div>' +
          '<div class="pr-footer__col">' +
            '<h3 class="pr-footer__heading">Sitemap</h3>' +
            '<ul class="pr-footer__list">' +
              '<li><a class="pr-footer__link" href="/overview/">Overview</a></li>' +
              '<li><a class="pr-footer__link" href="/street/">Street</a></li>' +
              '<li><a class="pr-footer__link" href="/culture/">Culture</a></li>' +
              '<li><a class="pr-footer__link" href="/lifestyle/">Lifestyle</a></li>' +
              '<li><a class="pr-footer__link" href="/portraits/">Portraits</a></li>' +
              '<li><a class="pr-footer__link" href="/about/">About</a></li>' +
            '</ul>' +
          '</div>' +
          '<div class="pr-footer__col">' +
            '<h3 class="pr-footer__heading">Public Record</h3>' +
            '<ul class="pr-footer__list">' +
              '<li><a class="pr-footer__link" href="/residual/">Residual</a></li>' +
              '<li><a class="pr-footer__link" href="/first-day/">First Day</a></li>' +
              '<li><a class="pr-footer__link" href="/catalog/">Catalog</a></li>' +
            '</ul>' +
          '</div>' +
          '<div class="pr-footer__col">' +
            '<h3 class="pr-footer__heading">Follow</h3>' +
            '<div class="pr-footer__socials">' +
              '<a class="pr-footer__social" href="https://instagram.com/toritorsion" target="_blank" rel="noopener" aria-label="Instagram">' +
                '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4"></rect><circle cx="12" cy="12" r="4.2"></circle><circle cx="17.5" cy="6.5" r="1"></circle></svg>' +
                '<span>Instagram</span>' +
              '</a>' +
              '<a class="pr-footer__social" href="https://www.linkedin.com/in/toritorsion/" target="_blank" rel="noopener" aria-label="LinkedIn">' +
                '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"></rect><line x1="8" y1="10" x2="8" y2="17"></line><line x1="8" y1="7" x2="8" y2="7"></line><path d="M12 17v-4.1c0-1.4 1-2.5 2.3-2.5 1.3 0 2.2.9 2.2 2.6V17"></path></svg>' +
                '<span>LinkedIn</span>' +
              '</a>' +
            '</div>' +
          '</div>' +
          '<div class="pr-footer__col">' +
            '<h3 class="pr-footer__heading">Legal</h3>' +
            '<ul class="pr-footer__list">' +
              '<li><a class="pr-footer__link" href="/privacy/">Privacy Policy</a></li>' +
              '<li><a class="pr-footer__link" href="/terms/">Terms of Use</a></li>' +
            '</ul>' +
          '</div>' +
        '</div>' +
        '<div class="pr-footer__bottom">' +
          '<p class="pr-footer__bottom-copy">&copy; ' + year + ' Tori &ldquo;Torsion&rdquo; Howard. All rights reserved.</p>' +
        '</div>' +
      '</div>';
  }

  // --- Init ---
  function init() {
    ensureFavicons();
    ensurePublicRecordLandingLink();
    setActiveNav();
    setupLazyLoad();
    setupDropdowns();
    randomizeGallery();
    setupLightbox();
    ensureSiteLower();
    enhanceFooter();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
