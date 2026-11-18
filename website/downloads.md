---
layout: downloads
title: Past Releases
---

{% for ver in site.data.versions.list %}{% if ver.kind == "stable" %}
## Version {{ ver.label | remove_first: "v" }} {#current-release}

{{ ver.date | date: "%B %-d, %Y" }} | [View online]({{ site.baseurl }}/{{ ver.path }}/) | [Downloads](https://github.com/OWASP/wstg/releases/tag/{{ ver.path }})
{% endif %}{% endfor %}
## Historical Releases {#historical-releases}

| Version | Date | View Online | Downloads |
|---------|------|-------------|-----------|
{% for ver in site.data.versions.list %}{% if ver.kind == "archived" %}| {{ ver.label | remove_first: "v" }} | {{ ver.date | date: "%B %-d, %Y" }} | [{{ ver.label }}]({{ site.baseurl }}/{{ ver.path }}/) | [Release](https://github.com/OWASP/wstg/releases/tag/{{ ver.path }}) |
{% endif %}{% endfor %}| 4.0 | September 17, 2014 | - | [Release](https://github.com/OWASP/wstg/releases/tag/v4.0) |
| 3.0 | December 16, 2008 | - | [Release](https://github.com/OWASP/wstg/releases/tag/v3.0) |
| 3.0 Pre-release | November 6, 2008 | - | [Release](https://github.com/OWASP/wstg/releases/tag/v3.0-pre) |
| 2.0 | February 10, 2007 | - | [Release](https://github.com/OWASP/wstg/releases/tag/v2.0) |
| 1.1 | August 14, 2004 | - | [Release](https://github.com/OWASP/wstg/releases/tag/v1.1) |
| 1.0 | December 10, 2004 | - | [Release](https://github.com/OWASP/wstg/releases/tag/v1.0) |

For a complete list of releases and formats, see the [GitHub releases page](https://github.com/OWASP/wstg/releases).
