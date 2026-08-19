(function () {
  if (window.__wstgNavInit) {
    return;
  }
  window.__wstgNavInit = true;

  function normalizePath(path) {
    return (path || "")
      .replace(/\/+$/, "")
      .replace(/\/index(?:\.html)?$/i, "")
      .replace(/\/README(?:\.html)?$/i, "")
      .replace(/\.html?$/i, "")
      .replace(/\/+$/, "");
  }

  function itemPathFromNavUrl(navUrl) {
    return normalizePath((navUrl || "").split("#")[0]);
  }

  /** Scroll overflow ancestors so el is centered; do not move the window. */
  function scrollNavLinkIntoView(el) {
    var node = el.parentElement;
    while (node && node !== document.body) {
      var style = window.getComputedStyle(node);
      var oy = style.overflowY;
      var ox = style.overflowX;
      var canY =
        (oy === "auto" || oy === "scroll" || oy === "overlay") &&
        node.scrollHeight > node.clientHeight + 1;
      var canX =
        (ox === "auto" || ox === "scroll" || ox === "overlay") &&
        node.scrollWidth > node.clientWidth + 1;
      if (canY || canX) {
        var pRect = node.getBoundingClientRect();
        var cRect = el.getBoundingClientRect();
        if (canY) {
          node.scrollTop +=
            cRect.top + cRect.height / 2 - (pRect.top + pRect.height / 2);
        }
        if (canX) {
          node.scrollLeft +=
            cRect.left + cRect.width / 2 - (pRect.left + pRect.width / 2);
        }
      }
      node = node.parentElement;
    }
  }

  function pageMatchesItem(pagePath, itemPath) {
    if (!itemPath) {
      return false;
    }
    if (pagePath === itemPath) {
      return true;
    }
    return pagePath.endsWith("/" + itemPath);
  }

  function directChildItems(item) {
    var details = null;
    for (var i = 0; i < item.children.length; i++) {
      if (item.children[i].tagName === "DETAILS") {
        details = item.children[i];
        break;
      }
    }
    var ul = null;
    if (details) {
      for (var j = 0; j < details.children.length; j++) {
        if (details.children[j].tagName === "UL") {
          ul = details.children[j];
          break;
        }
      }
    } else {
      for (var k = 0; k < item.children.length; k++) {
        if (item.children[k].tagName === "UL") {
          ul = item.children[k];
          break;
        }
      }
    }
    if (!ul) {
      return [];
    }
    var out = [];
    for (var n = 0; n < ul.children.length; n++) {
      if (ul.children[n].classList.contains("wstg-nav-item")) {
        out.push(ul.children[n]);
      }
    }
    return out;
  }

  function encodeFilterParams(filterValue) {
    var params = new URLSearchParams();
    if (filterValue && filterValue.trim()) {
      params.set('filter', filterValue);
    }
    return params.toString();
  }

  function decodeFilterParams() {
    var params = new URLSearchParams(window.location.search);
    return params.get('filter') || '';
  }

  function updateFilterUrl(filterValue) {
    var params = encodeFilterParams(filterValue);
    var newUrl = params ? '?' + params : '?';
    window.history.replaceState(null, '', newUrl);
  }

  function initNav(nav) {
    var pagePath = normalizePath(window.location.pathname);
    var pageHash = (window.location.hash || "").replace(/^#/, "").toLowerCase();
    var activeLink = null;
    var bestScore = -1;

    var links = nav.querySelectorAll("a[data-nav-url]");
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var navUrl = link.getAttribute("data-nav-url") || "";
      var itemPath = itemPathFromNavUrl(navUrl);
      if (!pageMatchesItem(pagePath, itemPath)) {
        continue;
      }
      var frag = navUrl.indexOf("#") >= 0 ? navUrl.split("#")[1].toLowerCase() : "";
      var score = itemPath.length;
      if (frag) {
        if (frag !== pageHash) {
          continue;
        }
        score += 10000;
      } else if (pageHash) {
        // Prefer fragment-specific entries when the URL has a hash.
        score -= 1;
      }
      if (score > bestScore) {
        bestScore = score;
        activeLink = link;
      }
    }

    if (activeLink) {
      activeLink.setAttribute("aria-current", "page");
      var item = activeLink.closest(".wstg-nav-item");
      if (item) {
        item.classList.add("is-active");
      }
      var parent = activeLink.parentElement;
      while (parent && parent !== nav) {
        if (parent.tagName === "DETAILS") {
          parent.open = true;
        }
        parent = parent.parentElement;
      }
      // Open ancestors, then scroll after layout (details expand is async).
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          scrollNavLinkIntoView(activeLink);
          if (!pageHash) {
            window.scrollTo(0, 0);
          }
          // Second pass after nested details finish expanding.
          setTimeout(function () {
            scrollNavLinkIntoView(activeLink);
            if (!pageHash) {
              window.scrollTo(0, 0);
            }
          }, 50);
        });
      });
    } else if (!pageHash) {
      window.scrollTo(0, 0);
    }

    var filter = nav.querySelector(".wstg-nav-filter");
    if (filter) {
      var savedFilterValue = decodeFilterParams();
      if (savedFilterValue) {
        filter.value = savedFilterValue;
        applyFilter(nav, savedFilterValue);
      }
      filter.addEventListener("input", function () {
        applyFilter(nav, filter.value);
        updateFilterUrl(filter.value);
      });
    }

    var expandBtn = nav.querySelector("[data-wstg-expand]");
    var collapseBtn = nav.querySelector("[data-wstg-collapse]");
    if (expandBtn) {
      expandBtn.addEventListener("click", function () {
        var details = nav.querySelectorAll("details");
        for (var d = 0; d < details.length; d++) {
          details[d].open = true;
        }
      });
    }
    if (collapseBtn) {
      collapseBtn.addEventListener("click", function () {
        var details = nav.querySelectorAll("details");
        for (var d = 0; d < details.length; d++) {
          details[d].open = false;
        }
      });
    }

    var summaryLinks = nav.querySelectorAll("summary a");
    for (var s = 0; s < summaryLinks.length; s++) {
      summaryLinks[s].addEventListener("click", function (event) {
        event.stopPropagation();
      });
    }
  }

  function applyFilter(nav, rawQuery) {
    var query = (rawQuery || "").trim().toLowerCase();
    var items = nav.querySelectorAll(".wstg-nav-item");
    var i;

    if (!query) {
      for (i = 0; i < items.length; i++) {
        items[i].classList.remove("is-filtered-out");
      }
      return;
    }

    // Mark self-matches, then walk bottom-up so parents of matches stay visible.
    var ordered = [];
    for (i = 0; i < items.length; i++) {
      var title = (items[i].getAttribute("data-title") || "").toLowerCase();
      var hints = (items[i].getAttribute("data-hints") || "").toLowerCase();
      items[i]._wstgSelfMatch = (title + " " + hints).indexOf(query) !== -1;
      ordered.push(items[i]);
    }

    ordered.sort(function (a, b) {
      return depth(b) - depth(a);
    });

    for (i = 0; i < ordered.length; i++) {
      var node = ordered[i];
      var visible = !!node._wstgSelfMatch;
      var children = directChildItems(node);
      for (var c = 0; c < children.length; c++) {
        if (!children[c].classList.contains("is-filtered-out")) {
          visible = true;
          break;
        }
      }
      node.classList.toggle("is-filtered-out", !visible);
      if (visible) {
        var details = null;
        for (var t = 0; t < node.children.length; t++) {
          if (node.children[t].tagName === "DETAILS") {
            details = node.children[t];
            break;
          }
        }
        if (details) {
          details.open = true;
        }
      }
    }
  }

  function depth(el) {
    var d = 0;
    var p = el.parentElement;
    while (p) {
      if (p.classList && p.classList.contains("wstg-nav-item")) {
        d += 1;
      }
      p = p.parentElement;
    }
    return d;
  }

  function boot() {
    var navs = document.querySelectorAll(".wstg-nav");
    for (var i = 0; i < navs.length; i++) {
      initNav(navs[i]);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
