/**
 * Document page tools: breadcrumb, WSTG ID copy button, permalink, prev/next nav
 */
(function () {
  'use strict';

  /**
   * Extract WSTG ID from the ID table in doc-content
   * Looks for: <table> <thead> <th>ID</th> </thead> <tbody> <td>WSTG-...</td>
   * Returns the base ID (e.g., "WSTG-INFO-01")
   */
  function extractBaseWstgId() {
    var docContent = document.querySelector('.doc-content');
    if (!docContent) return null;

    var tables = docContent.querySelectorAll('table');
    for (var t = 0; t < tables.length; t++) {
      var table = tables[t];
      var th = table.querySelector('thead th');
      if (th && th.textContent.trim() === 'ID') {
        var td = table.querySelector('tbody td');
        if (td) {
          var id = td.textContent.trim();
          // If versioned (e.g., "WSTG-v42-INFO-01"), extract base (e.g., "WSTG-INFO-01")
          return id.replace(/^(WSTG)-v\d+-/, '$1-');
        }
      }
    }
    return null;
  }

  /**
   * Get page collection (latest, v42, v41) from URL
   */
  function getPageCollection() {
    var path = window.location.pathname;
    if (path.includes('/latest/')) return 'latest';
    if (path.includes('/v4.2/') || path.includes('/v42/')) return 'v42';
    if (path.includes('/v4.1/') || path.includes('/v41/')) return 'v41';
    if (path.includes('/stable/')) return 'stable';
    return null;
  }

  /**
   * Format WSTG ID for copying based on current page collection
   * Latest (no version): WSTG-INFO-01
   * v4.2 (versioned): WSTG-v42-INFO-01
   * v4.1 (versioned): WSTG-v41-INFO-01
   * Follows "How To Reference WSTG Scenarios" format
   */
  function getFormattedWstgId() {
    var baseId = extractBaseWstgId();
    if (!baseId) return null;

    var collection = getPageCollection();
    if (!collection || collection === 'latest' || collection === 'stable') {
      return baseId;  // e.g., "WSTG-INFO-01"
    }

    // Add version prefix for v4.2 and v4.1
    if (collection === 'v42') {
      return baseId.replace(/^WSTG-/, 'WSTG-v42-');  // e.g., "WSTG-v42-INFO-01"
    } else if (collection === 'v41') {
      return baseId.replace(/^WSTG-/, 'WSTG-v41-');  // e.g., "WSTG-v41-INFO-01"
    }

    return baseId;
  }

  /**
   * Copy text to clipboard
   */
  function copyToClipboard(text) {
    if (!navigator.clipboard) {
      var textarea = document.createElement('textarea');
      textarea.textContent = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        return true;
      } catch (e) {
        return false;
      } finally {
        document.body.removeChild(textarea);
      }
    } else {
      navigator.clipboard.writeText(text).catch(function () {});
      return true;
    }
  }

  /**
   * Create copy ID button next to h1
   */
  function addCopyIdButton() {
    var id = getFormattedWstgId();
    if (!id) return;

    var h1 = document.querySelector('.doc-content h1');
    if (!h1) return;

    var btnCopy = document.createElement('button');
    btnCopy.type = 'button';
    btnCopy.className = 'doc-tools-btn doc-tools-copy-id';
    btnCopy.setAttribute('title', 'Copy WSTG ID to clipboard');
    btnCopy.setAttribute('aria-label', 'Copy WSTG ID: ' + id);
    btnCopy.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="1em" height="1em" aria-hidden="true"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M15 2H9a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"/></svg> <span class="doc-tools-btn-text">Copy ID</span>';

    btnCopy.addEventListener('click', function (e) {
      e.preventDefault();
      var copied = copyToClipboard(id);
      if (copied) {
        var origText = btnCopy.querySelector('.doc-tools-btn-text').textContent;
        btnCopy.querySelector('.doc-tools-btn-text').textContent = 'Copied!';
        setTimeout(function () {
          btnCopy.querySelector('.doc-tools-btn-text').textContent = origText;
        }, 2000);
      }
    });

    h1.appendChild(btnCopy);
  }

  /**
   * Create permalink button (only on versioned pages like /v4.2/ or /v4.1/)
   */
  function addPermalinkButton() {
    var collection = getPageCollection();
    // Only show on v42, v41 (not latest, not stable)
    if (!collection || collection === 'latest' || collection === 'stable') return;

    var id = getFormattedWstgId();
    if (!id) return;

    var h1 = document.querySelector('.doc-content h1');
    if (!h1) return;

    var url = window.location.href;
    var btnPermalink = document.createElement('button');
    btnPermalink.type = 'button';
    btnPermalink.className = 'doc-tools-btn doc-tools-permalink';
    btnPermalink.setAttribute('title', 'Copy permanent link to this page');
    btnPermalink.setAttribute('aria-label', 'Copy permanent link');
    btnPermalink.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="1em" height="1em" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg> <span class="doc-tools-btn-text">Copy Link</span>';

    btnPermalink.addEventListener('click', function (e) {
      e.preventDefault();
      var copied = copyToClipboard(url);
      if (copied) {
        var origText = btnPermalink.querySelector('.doc-tools-btn-text').textContent;
        btnPermalink.querySelector('.doc-tools-btn-text').textContent = 'Copied!';
        setTimeout(function () {
          btnPermalink.querySelector('.doc-tools-btn-text').textContent = origText;
        }, 2000);
      }
    });

    h1.appendChild(btnPermalink);
  }

  /**
   * Extract human-readable label from path segment
   * "4-Web_Application_Security_Testing" → "Web Application Security Testing"
   * "07-Input_Validation_Testing" → "Input Validation Testing"
   */
  function extractLabelFromSegment(segment) {
    // Remove leading number and dash
    var label = segment.replace(/^\d+-/, '');
    // Replace underscores with spaces
    label = label.replace(/_/g, ' ');
    return label;
  }

  /**
   * Build breadcrumb from URL path
   * E.g. /latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/1-Testing_for_XSS/
   * → Web Application Security Testing → Input Validation Testing → Testing for XSS
   */
  function buildBreadcrumb() {
    var path = window.location.pathname;
    var parts = path.split('/').filter(function (p) { return p && p !== 'index.html'; });

    if (parts.length < 2) return null;

    // Remove 'latest', 'v4.2', etc from the path
    var collection = parts[0];
    if (!['latest', 'v42', 'v41', 'stable'].includes(collection)) return null;

    // Get the remaining parts (chapter/section/test)
    var pathParts = parts.slice(1);
    if (pathParts.length === 0) return null;

    var breadcrumbItems = [];
    for (var i = 0; i < pathParts.length; i++) {
      var segment = pathParts[i];
      // Extract label from segment
      // E.g. "4-Web_Application_Security_Testing" → "Web Application Security Testing"
      var label = extractLabelFromSegment(segment);

      // Build URL to this level
      var url = '/' + collection + '/' + pathParts.slice(0, i + 1).join('/') + '/';

      breadcrumbItems.push({
        label: label,
        url: url,
        fullSegment: segment
      });
    }

    return breadcrumbItems;
  }

  /**
   * Insert breadcrumb before doc-content
   */
  function addBreadcrumb() {
    var items = buildBreadcrumb();
    if (!items || items.length === 0) return;

    var docContent = document.querySelector('.doc-content');
    if (!docContent) return;

    var breadcrumb = document.createElement('nav');
    breadcrumb.className = 'doc-breadcrumb';
    breadcrumb.setAttribute('aria-label', 'Breadcrumb');

    var list = document.createElement('ol');
    list.className = 'doc-breadcrumb-list';

    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      var li = document.createElement('li');

      if (i === items.length - 1) {
        // Last item: current page (no link)
        li.className = 'doc-breadcrumb-item doc-breadcrumb-current';
        li.textContent = item.label;
        li.setAttribute('aria-current', 'page');
      } else {
        // Intermediate items: links
        li.className = 'doc-breadcrumb-item';
        var link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.label;
        link.title = item.title;
        li.appendChild(link);
      }

      list.appendChild(li);
    }

    breadcrumb.appendChild(list);
    docContent.insertBefore(breadcrumb, docContent.firstChild);
  }

  /**
   * Extract nav items from the wstg-nav tree and find prev/next for current page
   */
  function extractNavItems() {
    var nav = document.querySelector('.wstg-nav');
    if (!nav) return [];

    var items = [];
    var links = nav.querySelectorAll('a[data-nav-url]');

    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var url = link.getAttribute('data-nav-url');
      if (!url) continue;

      // Normalize URL: remove fragment, trailing slashes, .html, /index
      var normalized = normalizeUrl(url);

      items.push({
        url: url,
        normalizedUrl: normalized,
        title: link.textContent.trim()
      });
    }

    return items;
  }

  /**
   * Normalize URL for comparison
   */
  function normalizeUrl(url) {
    if (!url) return '';
    return (url || '')
      .split('#')[0]  // Remove fragment
      .replace(/\/+$/, '')  // Remove trailing slashes
      .replace(/\/index(?:\.html)?$/i, '')  // Remove /index or /index.html
      .replace(/\.html?$/i, '');  // Remove .html or .htm
  }

  /**
   * Find prev/next nav items based on current page
   */
  function findPrevNext() {
    var items = extractNavItems();
    if (items.length < 2) return null;

    var currentPath = window.location.pathname;
    // Remove collection prefix (latest, v4.2, v42, v4.1, v41, stable) and normalize
    currentPath = currentPath.replace(/^\/(latest|v4\.2|v42|v4\.1|v41|stable)\//, '');
    currentPath = normalizeUrl(currentPath);

    var currentIndex = -1;

    // Find current page in nav items (exact match)
    for (var i = 0; i < items.length; i++) {
      if (items[i].normalizedUrl === currentPath) {
        currentIndex = i;
        break;
      }
    }

    // Strategy 2: Match by segment comparison if exact match fails
    if (currentIndex === -1) {
      var currentSegments = currentPath.split('/').filter(function(s) { return s; });

      for (var i = 0; i < items.length; i++) {
        var itemSegments = items[i].normalizedUrl.split('/').filter(function(s) { return s; });

        // If same number of segments and all match, it's a hit
        if (currentSegments.length === itemSegments.length) {
          var allMatch = true;
          for (var j = 0; j < currentSegments.length; j++) {
            if (currentSegments[j] !== itemSegments[j]) {
              allMatch = false;
              break;
            }
          }
          if (allMatch) {
            currentIndex = i;
            break;
          }
        }
      }
    }

    // Strategy 3: Partial match as last resort
    if (currentIndex === -1) {
      for (var i = 0; i < items.length; i++) {
        if (currentPath.endsWith('/' + items[i].normalizedUrl) ||
            items[i].normalizedUrl.endsWith(currentPath)) {
          currentIndex = i;
          break;
        }
      }
    }

    if (currentIndex === -1) return null;

    return {
      prev: currentIndex > 0 ? items[currentIndex - 1] : null,
      next: currentIndex < items.length - 1 ? items[currentIndex + 1] : null
    };
  }

  /**
   * Add floating prev/next navigation buttons (left/right arrows)
   */
  function addPrevNext() {
    var nav = findPrevNext();
    if (!nav || (!nav.prev && !nav.next)) return;

    var collection = getPageCollection();
    if (!collection) return;

    var navContainer = document.createElement('nav');
    navContainer.className = 'doc-prev-next-floating';
    navContainer.setAttribute('aria-label', 'Page navigation');

    // Previous button
    if (nav.prev) {
      var prevBtn = document.createElement('a');
      prevBtn.href = '/' + collection + '/' + nav.prev.url;
      prevBtn.className = 'doc-prev-next-btn doc-prev-next-prev';
      prevBtn.setAttribute('title', 'Previous: ' + (nav.prev.title || 'Previous'));
      prevBtn.setAttribute('aria-label', 'Previous: ' + (nav.prev.title || 'Previous'));
      prevBtn.innerHTML = '<span class="doc-prev-next-arrow">←</span><span class="doc-prev-next-tooltip">' + (nav.prev.title || 'Previous') + '</span>';
      navContainer.appendChild(prevBtn);
    }

    // Next button
    if (nav.next) {
      var nextBtn = document.createElement('a');
      nextBtn.href = '/' + collection + '/' + nav.next.url;
      nextBtn.className = 'doc-prev-next-btn doc-prev-next-next';
      nextBtn.setAttribute('title', 'Next: ' + (nav.next.title || 'Next'));
      nextBtn.setAttribute('aria-label', 'Next: ' + (nav.next.title || 'Next'));
      nextBtn.innerHTML = '<span class="doc-prev-next-arrow">→</span><span class="doc-prev-next-tooltip">' + (nav.next.title || 'Next') + '</span>';
      navContainer.appendChild(nextBtn);
    }

    document.body.appendChild(navContainer);
  }

  /**
   * Keyboard shortcuts: ? for help, / for filter focus
   */
  function setupKeyboardShortcuts() {
    var helpMessage = 'Keyboard shortcuts:\n? - Show this help\n/ - Focus contents filter';

    document.addEventListener('keydown', function(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      if (e.key === '?') {
        e.preventDefault();
        alert(helpMessage);
      } else if (e.key === '/') {
        e.preventDefault();
        var filter = document.querySelector('.wstg-nav-filter');
        if (filter) {
          filter.focus();
        }
      }
    });
  }

  /**
   * Focus mode: hide sidebar, wider content, toggle with localStorage
   */
  function setupFocusMode() {
    var focusModeClass = 'focus-mode';
    var storageKey = 'wstg-focus-mode';

    // Check if focus mode was enabled before
    var isFocusMode = localStorage.getItem(storageKey) === 'true';
    if (isFocusMode) {
      document.documentElement.classList.add(focusModeClass);
    }

    // Add toggle button to doc-nav-bar
    var navBar = document.querySelector('.doc-nav-bar');
    if (navBar) {
      var focusBtn = document.createElement('button');
      focusBtn.type = 'button';
      focusBtn.className = 'doc-focus-toggle';
      focusBtn.setAttribute('title', 'Toggle focus mode');
      focusBtn.setAttribute('aria-label', 'Toggle focus mode');
      focusBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="1.25em" height="1.25em" aria-hidden="true"><circle cx="12" cy="12" r="1"/><path d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg>';

      focusBtn.addEventListener('click', function() {
        document.documentElement.classList.toggle(focusModeClass);
        var isNowFocusMode = document.documentElement.classList.contains(focusModeClass);
        localStorage.setItem(storageKey, isNowFocusMode);
      });

      navBar.appendChild(focusBtn);
    }
  }

  /**
   * Mark external links with icon and attributes
   */
  function markExternalLinks() {
    var docContent = document.querySelector('.doc-content');
    if (!docContent) return;

    var links = docContent.querySelectorAll('a[href]');
    links.forEach(function(link) {
      var href = link.getAttribute('href');
      if (!href) return;

      // Check if external (not same domain, not fragment, not relative)
      var isExternal = false;
      if (href.startsWith('http://') || href.startsWith('https://')) {
        try {
          var linkUrl = new URL(href);
          var currentUrl = new URL(window.location.href);
          isExternal = linkUrl.hostname !== currentUrl.hostname;
        } catch (e) {
          // Invalid URL, treat as internal
        }
      }

      if (isExternal) {
        link.classList.add('ext-link');
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
      }
    });
  }

  /**
   * Initialize all doc tools when DOM is ready
   */
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }

    // Only run on document pages
    if (!document.querySelector('.doc-content')) return;

    addBreadcrumb();
    addCopyIdButton();
    addPermalinkButton();
    addPrevNext();
    setupKeyboardShortcuts();
    setupFocusMode();
    markExternalLinks();
  }

  init();
})();
