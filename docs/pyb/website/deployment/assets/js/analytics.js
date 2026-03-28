/**
 * PicYourBooth — GA4 Custom Event Tracking
 * Loaded on all pages. Reads DOM structure to wire events automatically.
 *
 * Events:
 *   cta_click          — click on any link to offerte.html
 *   upgrade_toggle     — toggle upgrade on/off (product pages)
 *   faq_open           — open a FAQ item (product pages)
 *   dj_hours_select    — change hour selector (DJs page)
 *   offerte_start      — first interaction with offerte form
 *   offerte_field_fill — individual field completed on offerte form
 *   (offerte_submit is fired inline in offerte.html after HubSpot 200)
 */
(function () {
  'use strict';

  if (typeof gtag !== 'function') return;

  var page = location.pathname.split('/').pop().replace('.html', '') || 'index';

  /* ── Helpers ───────────────────────────────────────── */

  function parseParams(href) {
    try {
      var url = new URL(href, location.origin);
      return {
        service: url.searchParams.get('service') || '',
        upgrades: url.searchParams.get('upgrades') || ''
      };
    } catch (e) {
      return { service: '', upgrades: '' };
    }
  }

  function ctaLocation(link) {
    if (link.classList.contains('nav-cta')) return 'nav';
    if (link.classList.contains('sticky-price-bar__cta')) return 'sticky_bar';
    if (link.closest('.sticky-cta')) return 'sticky_bar';
    if (link.classList.contains('cta-btn') || link.classList.contains('booking-cta')) return 'builder';
    if (link.classList.contains('btn-violet')) return 'spotify';
    return 'other';
  }

  function builderToService(val) {
    if (val === 'mirror') return 'magic-mirror';
    if (val === 'party') return 'party-booth';
    return val;
  }

  /* ── 1. cta_click ─────────────────────────────────── */

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href*="offerte.html"]');
    if (!link) return;

    var p = parseParams(link.href);
    gtag('event', 'cta_click', {
      service: p.service,
      source_page: page,
      cta_location: ctaLocation(link),
      upgrades: p.upgrades
    });
  });

  /* ── 2. upgrade_toggle ────────────────────────────── */
  /* Use click on the row + setTimeout so we read checkbox state
     AFTER the existing toggleUpgrade() handler has flipped it. */

  document.querySelectorAll('.upgrade-row[data-upgrade]').forEach(function (row) {
    var cb = row.querySelector('input[type="checkbox"]');
    if (!cb) return;
    row.addEventListener('click', function (e) {
      if (e.target.closest('.info-btn') || e.target.closest('.modal')) return;
      setTimeout(function () {
        gtag('event', 'upgrade_toggle', {
          upgrade_name: row.dataset.upgrade,
          action: cb.checked ? 'on' : 'off',
          service: builderToService(row.dataset.builder)
        });
      }, 0);
    });
  });

  /* ── 3. faq_open ──────────────────────────────────── */

  document.querySelectorAll('details.faq-item').forEach(function (details) {
    details.addEventListener('toggle', function () {
      if (!details.open) return;
      var summary = details.querySelector('summary');
      gtag('event', 'faq_open', {
        question: summary ? summary.textContent.trim() : '',
        source_page: page
      });
    });
  });

  /* ── 4. dj_hours_select ───────────────────────────── */

  var hourSelector = document.getElementById('hourSelector');
  if (hourSelector) {
    hourSelector.addEventListener('click', function (e) {
      var option = e.target.closest('.hour-option');
      if (!option) return;
      gtag('event', 'dj_hours_select', {
        hours: option.dataset.hours,
        price: option.dataset.price
      });
    });
  }

  /* ── 5. offerte_start (first interaction) ──────────── */

  var form = document.querySelector('form');
  if (form && page === 'offerte') {
    var started = false;

    function fireStart() {
      if (started) return;
      started = true;
      var serviceEl = document.getElementById('service');
      var params = new URLSearchParams(location.search);
      gtag('event', 'offerte_start', {
        service: (serviceEl && serviceEl.value) || params.get('service') || ''
      });
    }

    form.addEventListener('input', fireStart, { once: true });
    form.addEventListener('change', fireStart, { once: true });

    /* ── 6. offerte_field_fill ─────────────────────── */

    var filled = {};
    var fields = form.querySelectorAll('input:not([type="hidden"]):not([type="submit"]), select, textarea');

    fields.forEach(function (field) {
      var eventType = (field.tagName === 'SELECT') ? 'change' : 'blur';
      field.addEventListener(eventType, function () {
        var name = field.name || field.id || 'unknown';
        if (!field.value || filled[name]) return;
        filled[name] = true;
        gtag('event', 'offerte_field_fill', {
          field_name: name
        });
      });
    });
  }

})();
