# Information Gathering Overview

You can only test what you can find. Before a tester can assess authentication, authorization, business logic, or any other area of an application, they must first identify what is actually in scope: the applications, hosts, endpoints, and technologies that make up the attack surface. Assets that are never discovered are never tested, regardless of how thorough the rest of the assessment is.

Information gathering and discovery is therefore the foundation of any web application security assessment. It combines passive reconnaissance (which does not directly interact with the target) with active enumeration (which does) to build as complete a picture as possible of what is exposed, how it is exposed, and what technologies are involved.

Contemporary assessments commonly combine passive subdomain enumeration (`subfinder`, Amass passive), live-host probing (`httpx`), Certificate Transparency, archive URL collection (`gau`, `waybackurls`, `waymore`), JavaScript analysis (`jsluice`, LinkFinder), and targeted content discovery (`ffuf`, `feroxbuster`, Kiterunner). See the individual INFO scenarios and the [API Reconnaissance](../12-API_Testing/01-API_Reconnaissance.md) chapter for concrete examples.

Always stay within the defined scope of the engagement.
