---
layout: home
title: OWASP Web Security Testing Guide
project_title: OWASP Web Security Testing Guide
project_subtitle: An OWASP Flagship Project
project_tagline: The premier cybersecurity testing resource for web application developers and security professionals.
---

<section class="section section-home">
  <div class="container container-wide">
    <div class="home-cta-row">
      <a class="btn btn-secondary" href="{{ site.baseurl }}/latest/">Latest (Dev)</a>
      <a class="btn btn-primary" href="{{ site.baseurl }}/stable/">Read the Stable Guide</a>
      <a class="btn btn-secondary" href="https://github.com/OWASP/wstg">Contribute on GitHub</a>
    </div>
    <div class="doc-nav-bar">
      <button type="button" id="doc-nav-toggle" class="doc-nav-toggle" aria-controls="doc-sidebar" aria-expanded="false">
        <span class="doc-nav-toggle-icon" aria-hidden="true"></span>
        Versions
      </button>
    </div>
    <div class="doc-layout">
      <div id="doc-nav-backdrop" class="doc-nav-backdrop" hidden></div>
      <aside id="doc-sidebar" class="doc-sidebar" aria-label="Versions on This Site">
        <button type="button" id="doc-nav-close" class="doc-nav-close" aria-label="Close versions">
          <span aria-hidden="true">&times;</span>
        </button>
        {% include home-versions-nav.html %}
      </aside>
      <article class="doc-content">
        <h2>About the WSTG</h2>
        <p>
          The Web Security Testing Guide (WSTG) is a comprehensive guide to testing the security of
          web applications and web services. Created by the collaborative efforts of cybersecurity
          professionals and dedicated volunteers, the WSTG provides a framework of best practices
          used by penetration testers and organizations all over the world.
        </p>
        <p>
          Contributions to the guide should be made via the
          <a href="https://github.com/OWASP/wstg">OWASP/wstg</a> repository.
        </p>
        <h2>Citing Scenarios</h2>
        <p>
          Prefer versioned links when citing scenarios. Identifiers use the form
          <code>WSTG-&lt;category&gt;-&lt;number&gt;</code> (for example <code>WSTG-INFO-02</code>).
          For version-specific citations use
          <code>WSTG-&lt;version&gt;-&lt;category&gt;-&lt;number&gt;</code>
          (for example <code>WSTG-v42-INFO-02</code>).
        </p>
      </article>
    </div>
  </div>
</section>
<script src="{{ site.baseurl }}/assets/js/doc-nav.js" defer></script>
