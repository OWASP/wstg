# Security Policy

## Supported Versions

This repository contains documentation and educational content.
There are no executable components or deployed services associated with this project.

The `master` branch reflects the latest maintained version of the documentation.

| Version | Supported |
|--------|-----------|
| master | ✅ |
| Others | ❌ |

---

## Reporting a Vulnerability

This repository does **not** directly process user data, authentication, or runtime execution.
However, if you believe you have identified:

- A security issue affecting linked tooling or referenced examples
- A misconfiguration that could lead to unsafe usage patterns
- A vulnerability related to CI/CD workflows or repository automation

Please follow **responsible disclosure** practices.

### How to Report
- Open a **private GitHub Security Advisory** for this repository, **or**
- Contact the OWASP project maintainers through official OWASP communication channels

Please include:
- A clear description of the issue
- Steps to reproduce (if applicable)
- Potential impact
- Suggested remediation (if available)

---

## Disclosure Process

- Reports will be reviewed by project maintainers
- If applicable, fixes will be discussed and implemented
- Public disclosure may occur after remediation, with reporter credit if desired

---

## Security Best Practices for Contributors

- Do not include secrets, tokens, or credentials in documentation or workflows
- Avoid using user-controlled input in CI/CD pipelines without validation
- Follow the OWASP Cheat Sheet Series for secure development and governance practices

---

## Recognition

Security researchers and contributors who responsibly disclose issues may be acknowledged
in release notes or project documentation, unless anonymity is requested.
