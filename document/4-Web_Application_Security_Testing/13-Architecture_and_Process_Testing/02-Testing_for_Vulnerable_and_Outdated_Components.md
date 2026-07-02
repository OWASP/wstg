# Testing for Vulnerable and Outdated Components

|ID|
|---|
|WSTG-APT-02|

## Summary

Modern applications are built using countless third-party components (libraries, frameworks, OS modules). When these components are outdated or contain known vulnerabilities (CVEs), attackers can exploit them to compromise the application. This can range from simple Cross-Site Scripting (XSS) in a frontend library to Remote Code Execution (RCE) in a backend framework.

## Test Objectives

- Inventory the client-side and server-side components in use.
- Identify the exact versions of these components.
- Check these versions against databases for known vulnerabilities.

## How to Test

### Client-Side Component Analysis

Web applications often load numerous JavaScript libraries (e.g., jQuery, React, Angular) into the browser.

- Analyze the page source code. Look for filenames or version numbers in URL paths (e.g., `jquery-3.2.1.min.js`).
- Use browser extensions or automated scanners to detect outdated client libraries.

### Server-Side Component Analysis

Detecting server-side components is often more difficult unless the application voluntarily discloses them.

- **HTTP Headers:** Analyze headers like `Server`, `X-Powered-By`, or `X-AspNet-Version`. These often provide exact details about the web server or framework.
- **Error Messages:** Provoke server errors. Default error pages (e.g., from Tomcat, Nginx, Django) frequently display the exact version number.
- **Software Bill of Materials (SBOM):** If testing in a white-box scenario, review dependency files (like `package.json`, `pom.xml`, `requirements.txt`).

### Exploit Verification

If an outdated component is found:

1. Search public databases (like NVD or Exploit-DB) for known CVEs affecting the identified version.
2. (Optional, if in scope) Carefully test whether the specific vulnerability is actually exploitable given the target application's configuration.

## Remediation

- Maintain a continuously updated inventory list (SBOM) of all components used.
- Establish a patch management process to apply critical updates promptly.
- Remove unused dependencies, features, files, and documentation from production environments.
- Utilize automated dependency scanning tools in the CI/CD pipeline.

## Tools

- Retire.js / Wappalyzer
- OWASP Dependency-Check
- Snyk / npm audit / Dependabot

## References

- OWASP Top 10:2021 - A06: Vulnerable and Outdated Components
- OWASP Dependency-Check
- -- START OF FILE 03-Testing_for_Software_and_Data_Integrity_Failures.md ---