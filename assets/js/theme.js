/**
 * Theme toggle: light, dark, or system (prefers-color-scheme).
 * Preference saved in localStorage (functional, no tracking).
 * Head script sets data-theme immediately to avoid flash.
 */
(function () {
  'use strict';
  var KEY = 'wstg-theme';
  var systemQuery = typeof window !== 'undefined' && window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var systemListener = null;

  function getStored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function setStored(value) {
    try { localStorage.setItem(KEY, value); } catch (e) {}
  }

  /** User preference: "light", "dark", or "system" (default when nothing stored) */
  function getPreference() {
    var t = getStored();
    return t === 'light' || t === 'dark' || t === 'system' ? t : 'system';
  }

  /** Effective theme for the page: always "light" or "dark" */
  function getEffectiveTheme() {
    var pref = getPreference();
    if (pref === 'system' && systemQuery) return systemQuery.matches ? 'dark' : 'light';
    return pref;
  }

  function applyEffectiveTheme() {
    document.documentElement.setAttribute('data-theme', getEffectiveTheme());
  }

  function setTheme(preference) {
    setStored(preference);
    if (preference === 'system') {
      applyEffectiveTheme();
      if (systemQuery && !systemListener) {
        systemListener = function () { applyEffectiveTheme(); };
        systemQuery.addEventListener('change', systemListener);
      }
    } else {
      document.documentElement.setAttribute('data-theme', preference);
      if (systemQuery && systemListener) {
        systemQuery.removeEventListener('change', systemListener);
        systemListener = null;
      }
    }
  }

  /** Next preference in cycle: light → dark → system → light */
  function nextPreference() {
    var p = getPreference();
    return p === 'light' ? 'dark' : p === 'dark' ? 'system' : 'light';
  }

  /* 24x24 viewBox - sun, crescent moon, monitor */
  var SUN_PATH = '<path fill="currentColor" d="M12 18a6 6 0 0 1 0-12 6 6 0 0 1 0 12zm0-2a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM11 1h2v3h-2V1zm0 19h2v3h-2v-3zM3.514 4.929l1.414 1.414L4.929 6.343 3.514 4.93zM19.071 17.657l1.414 1.414-1.414 1.414-1.414-1.414 1.414-1.414zM1 12h3v2H1v-2zm19 0h3v2h-3v-2zM4.929 19.071l1.414-1.414 1.414 1.414-1.414 1.414-1.414-1.414zm12.728-12.728l1.414-1.414 1.414 1.414-1.414 1.414-1.414-1.414z"/>';
  var MOON_PATH = '<path fill="currentColor" d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/>';
  var SYSTEM_PATH = '<path fill="currentColor" d="M2 4h20v12H2V4zm2 2v8h16V6H4zm4 10v2h8v-2H8z"/>';

  function updateButton(btn) {
    var pref = getPreference();
    var next = nextPreference();
    var labelText = { light: 'Light', dark: 'Dark', system: 'System' };
    var ariaParts = { light: 'Theme: Light. Click to switch to dark.', dark: 'Theme: Dark. Click to switch to system.', system: 'Theme: System. Click to switch to light.' };
    btn.setAttribute('aria-label', ariaParts[pref]);
    btn.setAttribute('title', 'Theme: ' + labelText[pref] + '. Click to change.');
    var svg = btn.querySelector('svg');
    if (svg) {
      var icons = { light: SUN_PATH, dark: MOON_PATH, system: SYSTEM_PATH };
      svg.innerHTML = icons[pref] || MOON_PATH;
    }
    var labelEl = btn.querySelector('.theme-toggle-label');
    if (labelEl) labelEl.textContent = labelText[pref];
  }

  function announceTheme(effective) {
    var live = document.getElementById('theme-announcer');
    if (live) {
      live.textContent = 'Theme set to ' + effective;
    }
  }

  function init() {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    var live = document.getElementById('theme-announcer');
    if (!live) {
      live = document.createElement('div');
      live.id = 'theme-announcer';
      live.setAttribute('aria-live', 'polite');
      live.setAttribute('aria-atomic', 'true');
      live.className = 'sr-only';
      document.body.appendChild(live);
    }
    if (getPreference() === 'system' && systemQuery && !systemListener) {
      systemListener = function () { applyEffectiveTheme(); };
      systemQuery.addEventListener('change', systemListener);
    }
    btn.addEventListener('click', function () {
      setTheme(nextPreference());
      updateButton(btn);
      announceTheme(getEffectiveTheme());
    });
    updateButton(btn);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* Back to top: show floating button after scroll, scroll to top on click */
  function initBackToTop() {
    var btn = document.getElementById('back-to-top');
    if (!btn) return;
    var scrollThreshold = 150;
    var reduceMotion = typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function updateVisible() {
      if (window.scrollY > scrollThreshold) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }

    window.addEventListener('scroll', function () { updateVisible(); }, { passive: true });
    updateVisible();

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, left: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBackToTop);
  } else {
    initBackToTop();
  }
})();
