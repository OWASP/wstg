/**
 * Mobile guide contents drawer. Desktop layout is CSS-only; this script is a
 * small open/close controller (no framework).
 */
(function () {
  var toggle = document.getElementById("doc-nav-toggle");
  var closeBtn = document.getElementById("doc-nav-close");
  var sidebar = document.getElementById("doc-sidebar");
  var backdrop = document.getElementById("doc-nav-backdrop");
  if (!toggle || !sidebar) {
    return;
  }

  var mq = window.matchMedia("(max-width: 900px)");

  function isOpen() {
    return document.body.classList.contains("doc-nav-open");
  }

  function setOpen(open) {
    document.body.classList.toggle("doc-nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) {
      backdrop.hidden = !open;
    }
    if (open) {
      sidebar.scrollTop = 0;
      sidebar.scrollLeft = 0;
      var filter = sidebar.querySelector(".wstg-nav-filter");
      if (filter && mq.matches) {
        filter.focus({ preventScroll: true });
        sidebar.scrollLeft = 0;
      }
    } else if (mq.matches) {
      toggle.focus();
    }
  }

  function close() {
    if (isOpen()) {
      setOpen(false);
    }
  }

  toggle.addEventListener("click", function () {
    setOpen(!isOpen());
  });
  if (closeBtn) {
    closeBtn.addEventListener("click", close);
  }
  if (backdrop) {
    backdrop.addEventListener("click", close);
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      close();
    }
  });
  sidebar.addEventListener("click", function (e) {
    var link = e.target.closest("a[href]");
    if (link && mq.matches) {
      close();
    }
  });
  if (typeof mq.addEventListener === "function") {
    mq.addEventListener("change", function () {
      if (!mq.matches) {
        close();
      }
    });
  }
})();
