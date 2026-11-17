/* Header search: Fuse.js loaded lazily on first interaction.
   Panel = quick results; Enter goes to /<channel>/search/?search=term (results page).
   Does not touch the nav filter (?filter=, "/" key). */
(function () {
  "use strict";
  var openBtn = document.getElementById("wstg-search-open");
  var root = document.getElementById("wstg-search");
  if (!openBtn || !root) return;

  var input = document.getElementById("wstg-search-input");
  var list = document.getElementById("wstg-search-results");
  var status = document.getElementById("wstg-search-status");
  var PARAM = "search";
  var DEBOUNCE_MS = 120;
  var fuse = null;
  var loading = null;
  var loadFailed = false;
  var prefetchAbort = null;
  var timer = null;
  var active = -1;
  var lastFocus = null;
  var baseurl = (openBtn.getAttribute("data-index") || "").replace(/\/assets\/search\/.*$/, "");
  var ID_RE = /^(?:wstg-)?([a-z]{3,5})-?(\d{1,2})$/i;

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      if (window.Fuse) return resolve();
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  // Load Fuse + index once; instance cached for the session.
  function load(signal) {
    if (fuse) return Promise.resolve(fuse);
    if (loading) return loading;
    loadFailed = false;
    loading = Promise.all([
      loadScript(openBtn.getAttribute("data-fuse")),
      fetch(openBtn.getAttribute("data-index"), signal ? { signal: signal, priority: "low" } : undefined)
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    ]).then(function (res) {
      var records = res[1].records;
      fuse = new window.Fuse(records, {
        keys: [
          { name: "t", weight: 0.4 },
          { name: "i", weight: 0.25 },
          { name: "h", weight: 0.15 },
          { name: "e", weight: 0.12 },
          { name: "o", weight: 0.08 }
        ],
        threshold: 0.3,
        ignoreLocation: true,
        minMatchCharLength: 2,
        includeScore: true
      });
      fuse._records = records;
      fuse._channel = res[1].channel;
      return fuse;
    }).catch(function (err) {
      loading = null;
      loadFailed = true;
      throw err;
    });
    return loading;
  }

  function goodConnection() {
    var c = navigator.connection;
    if (!c) return false; // unknown (Safari/Firefox): load on demand only
    return !c.saveData && !/^(slow-2g|2g)$/.test(c.effectiveType || "");
  }

  function idlePrefetch() {
    if (!goodConnection()) return;
    var idle = window.requestIdleCallback || function (f) { return setTimeout(f, 2000); };
    idle(function () {
      if (fuse || loading) return;
      prefetchAbort = new AbortController();
      load(prefetchAbort.signal).catch(function () {});
    });
  }
  window.addEventListener("pagehide", function () { if (prefetchAbort && !fuse) prefetchAbort.abort(); });

  function normalizeId(q) {
    var m = q.trim().match(ID_RE);
    return m ? "WSTG-" + m[1].toUpperCase() + "-" + ("0" + m[2]).slice(-2) : null;
  }

  function search(q, max) {
    q = q.trim();
    if (q.length < 2) return [];
    var out = [];
    var seen = {};
    var id = normalizeId(q);
    var lower = q.toLowerCase();
    // Exact WSTG-ID, then exact alias token (e.g. "sqli"), pinned first.
    fuse._records.forEach(function (r) {
      var hit = (id && r.i && r.i.indexOf(id) !== -1) ||
        (r.h && (" " + r.h + " ").indexOf(" " + lower + " ") !== -1);
      if (hit && !seen[r.u]) { seen[r.u] = 1; out.push(r); }
    });
    if (id && out.length) return out.slice(0, max);
    // Short queries fuzz too easily: stricter score cutoff.
    var cutoff = q.length <= 4 ? 0.2 : 0.3;
    fuse.search(q.replace(/^wstg-/i, ""), { limit: max * 2 }).forEach(function (x) {
      if (x.score > cutoff) return;
      if (!seen[x.item.u]) { seen[x.item.u] = 1; out.push(x.item); }
    });
    // Multi-word typos: Fuse matches the whole string, so retry per word (AND).
    if (!out.length && /\s/.test(q.trim())) {
      var keys = ["t", "i", "h", "e", "o"];
      var expr = { $and: q.trim().split(/\s+/).filter(function (w) { return w.length > 1; }).map(function (w) {
        return { $or: keys.map(function (k) { var o = {}; o[k] = w; return o; }) };
      }) };
      fuse.search(expr, { limit: max }).forEach(function (x) { if (x.score <= 0.3) out.push(x.item); });
    }
    return out.slice(0, max);
  }

  function resultHref(r) {
    return baseurl + "/" + fuse._channel + "/" + r.u.replace(/^(\.?\/)+/, "");
  }

  function resultsUrl(q) {
    return openBtn.getAttribute("data-results") + "?" + PARAM + "=" + encodeURIComponent(q.trim());
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function render(q) {
    list.textContent = "";
    active = -1;
    input.setAttribute("aria-expanded", "false");
    input.removeAttribute("aria-activedescendant");
    if (q.trim().length < 2) { status.textContent = ""; return; }
    if (loadFailed) { status.textContent = "Search is unavailable. Use the Contents filter instead."; return; }
    if (!fuse) { status.textContent = "Loading search…"; return; }
    var results = search(q, window.matchMedia("(max-width: 900px)").matches ? 12 : 8);
    if (!results.length) { status.textContent = "No results for “" + q.trim() + "”."; return; }
    status.textContent = results.length + (results.length === 1 ? " result" : " results");
    results.forEach(function (r, i) {
      var li = el("li", "wstg-search-result");
      li.id = "wstg-search-r" + i;
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", "false");
      var a = el("a");
      a.href = resultHref(r);
      a.tabIndex = -1; // options are driven by arrow keys, not Tab
      a.appendChild(el("span", "wstg-search-result-title", r.t));
      var meta = el("span", "wstg-search-result-meta");
      if (r.i) meta.appendChild(el("span", "wstg-search-id", r.i.split(" ")[0]));
      if (r.c) meta.appendChild(el("span", "", r.c));
      a.appendChild(meta);
      li.appendChild(a);
      list.appendChild(li);
    });
    input.setAttribute("aria-expanded", "true");
  }

  function select(i) {
    var items = list.children;
    if (!items.length) return;
    if (active >= 0 && items[active]) items[active].setAttribute("aria-selected", "false");
    active = (i + items.length) % items.length;
    items[active].setAttribute("aria-selected", "true");
    input.setAttribute("aria-activedescendant", items[active].id);
    items[active].scrollIntoView({ block: "nearest" });
  }

  function run() {
    render(input.value);
  }

  var inerted = [];
  function setBackgroundInert(on) {
    if (on) {
      Array.prototype.forEach.call(document.body.children, function (n) {
        if (n !== root && n.tagName !== "SCRIPT" && !n.inert) { n.inert = true; inerted.push(n); }
      });
    } else {
      inerted.forEach(function (n) { n.inert = false; });
      inerted = [];
    }
  }

  function openSearch(initial) {
    if (root.hidden) {
      lastFocus = document.activeElement;
      root.hidden = false;
      setBackgroundInert(true);
      document.body.classList.add("wstg-search-open");
    }
    if (typeof initial === "string") input.value = initial;
    input.focus();
    input.select();
    if (!fuse) {
      status.textContent = input.value.trim().length >= 2 ? "Loading search…" : "";
      load().then(run, function () { render(input.value); });
    }
    render(input.value);
  }

  function closeSearch() {
    root.hidden = true;
    setBackgroundInert(false);
    document.body.classList.remove("wstg-search-open");
    input.value = "";
    list.textContent = "";
    status.textContent = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus(); else openBtn.focus();
  }

  openBtn.addEventListener("click", function () { openSearch(); });
  // Intent signals: start loading before the click lands.
  ["pointerenter", "focus"].forEach(function (ev) {
    openBtn.addEventListener(ev, function () { load().catch(function () {}); }, { once: true });
  });
  input.addEventListener("focus", function () { load().catch(function () {}); }, { once: true });
  root.addEventListener("click", function (e) {
    if (e.target.closest("[data-search-close]")) closeSearch();
  });

  input.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { timer = null; run(); }, DEBOUNCE_MS);
  });

  input.addEventListener("keydown", function (e) {
    // Render any pending debounced query first so arrows/Enter act on current results.
    if (timer && (e.key === "ArrowDown" || e.key === "ArrowUp" || e.key === "Enter")) {
      clearTimeout(timer);
      timer = null;
      run();
    }
    if (e.key === "ArrowDown") { e.preventDefault(); select(active + 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); select(active < 0 ? -1 : active - 1); }
    else if (e.key === "Enter") {
      e.preventDefault();
      // Arrowed-to result opens directly; plain Enter goes to the results page.
      var a = active >= 0 && list.children[active] && list.children[active].querySelector("a");
      if (a) window.location.href = a.href;
      else if (input.value.trim()) window.location.href = resultsUrl(input.value);
    } else if (e.key === "Escape") {
      e.preventDefault();
      if (input.value) { input.value = ""; run(); } else { closeSearch(); }
    }
  });

  // Keep Tab inside the dialog (input <-> close button).
  root.addEventListener("keydown", function (e) {
    if (e.key !== "Tab") return;
    var closeBtn = root.querySelector(".wstg-search-close");
    if (e.shiftKey && document.activeElement === input) { e.preventDefault(); closeBtn.focus(); }
    else if (!e.shiftKey && document.activeElement === closeBtn) { e.preventDefault(); input.focus(); }
  });

  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey && e.key.toLowerCase() === "k") {
      e.preventDefault();
      openSearch();
    } else if (e.key === "Escape" && !root.hidden && e.target !== input) {
      closeSearch();
    }
  });

  var urlQuery = new URLSearchParams(window.location.search).get(PARAM);
  var page = document.getElementById("wstg-search-page");

  function renderPage(q) {
    var heading = document.getElementById("wstg-search-page-heading");
    var pstatus = document.getElementById("wstg-search-page-status");
    var plist = document.getElementById("wstg-search-page-results");
    plist.textContent = "";
    if (q.trim().length < 2) { heading.textContent = "Search"; pstatus.textContent = "Enter at least 2 characters."; return; }
    heading.textContent = "Results for \u201C" + q.trim() + "\u201D";
    if (loadFailed) { pstatus.textContent = "Search is unavailable. Use the Contents filter instead."; return; }
    if (!fuse) { pstatus.textContent = "Loading search…"; return; }
    var results = search(q, 50);
    pstatus.textContent = results.length ? results.length + (results.length === 1 ? " result" : " results") : "No results.";
    results.forEach(function (r) {
      var li = el("li");
      var a = el("a", "", r.t);
      a.href = resultHref(r);
      li.appendChild(a);
      var meta = el("div", "wstg-search-result-meta");
      if (r.i) meta.appendChild(el("span", "wstg-search-id", r.i.split(" ")[0]));
      if (r.c) meta.appendChild(el("span", "", r.c));
      li.appendChild(meta);
      if (r.e) li.appendChild(el("p", "", r.e));
      plist.appendChild(li);
    });
  }

  if (page) {
    var pinput = document.getElementById("wstg-search-page-input");
    pinput.value = urlQuery || "";
    renderPage(pinput.value);
    load().then(function () { renderPage(pinput.value); }, function () { renderPage(pinput.value); });
    if (!urlQuery) pinput.focus();
    // Carry the query across the version switcher (links to the other channels' search pages).
    if (window.location.search) {
      Array.prototype.forEach.call(document.querySelectorAll(".version-switcher-list a[href]"), function (a) {
        if (/\/search\/?$/.test(a.getAttribute("href"))) a.href = a.getAttribute("href") + window.location.search;
      });
    }
  } else if (urlQuery) {
    // Old/shared ?search= links on normal pages land on the results page.
    window.location.replace(resultsUrl(urlQuery));
  } else {
    idlePrefetch();
  }
})();
