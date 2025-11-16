# Abbreviated OWASP Top 10–Focused Web Security Testing Guide

## Introduction

This abbreviated testing guide is a lightweight resource designed for teams that need a quick, minimal web security review focused on the OWASP Top 10.  
It is **not** a replacement for the full OWASP Web Security Testing Guide (WSTG) or the OWASP Application Security Verification Standard (ASVS).  
Instead, it provides a **bare-minimum testing baseline** for organizations with limited time, budget, or multiple applications requiring rapid review.

Testing only the Top 10 risks **does not provide full security coverage**. Many critical issues fall outside the Top 10 and may be more severe depending on context or new research.  
Where possible, a full WSTG assessment is strongly encouraged.

---

# A01: Broken Access Control

### What It Is
Access control failures allow users to act outside their intended permissions, such as accessing other users’ data or performing unauthorized actions.

### Related WSTG Tests
- WSTG-AUTHZ-01: Testing for Privilege Escalation  
- WSTG-AUTHZ-02: Testing for Bypass Techniques  
- WSTG-AUTHZ-03: Testing for Insecure Direct Object References  

### Quick Checks
- Test horizontal access (`/api/user/2`) as user 1  
- Attempt restricted admin functions  
- Try manipulating cookies, headers, and parameters  

---

# A02: Cryptographic Failures

### What It Is
Failures in cryptographic implementation expose sensitive data in transit or at rest.

### Related WSTG Tests
- WSTG-CRYP-01: Testing for Weak SSL/TLS  
- WSTG-CRYP-02: Testing for Poor Encryption Storage  
- WSTG-CRYP-03: Testing for Insecure Transport  

### Quick Checks
- Ensure HTTPS for all pages  
- Check TLS configuration and certificate validity  
- Verify password hashing algorithms (bcrypt, scrypt, Argon2)  

---

# A03: Injection

### What It Is
Injection occurs when attackers can influence interpreters (SQL, OS, LDAP, ORM) through unsanitized inputs.

### Related WSTG Tests
- WSTG-INPV-01: Input Validation Testing  
- WSTG-INSE-01: SQL Injection Testing  
- WSTG-INSE-02: Command Injection Testing  

### Quick Checks
- Test forms with `' OR 1=1--`  
- Try OS commands in parameters (`; ls`, `&& whoami`)  
- Check for unsafe string concatenation  

---

# A04: Insecure Design

### What It Is
Insecure design includes architectural flaws, missing controls, weak workflows, and insecure logic, regardless of implementation.

### Related WSTG Tests
- WSTG-ARCH-01: Architectural Review  
- WSTG-ATHN-03: Testing Workflow and Business Logic  
- WSTG-BUSL-01: Testing for Business Logic Abuse  

### Quick Checks
- Try bypassing multi-step workflows  
- Look for missing rate limits  
- Attempt unauthorized state transitions  

---

# A05: Security Misconfiguration

### What It Is
Misconfigurations include unsecured headers, default accounts, verbose errors, open admin panels, and outdated components.

### Related WSTG Tests
- WSTG-CONF-01: Testing for Security Headers  
- WSTG-CONF-02: Testing for Error Handling  
- WSTG-CONF-03: Testing for Default Credentials  

### Quick Checks
- Use tools like securityheaders.com  
- Check server error messages  
- Look for open admin interfaces  

---

# A06: Vulnerable and Outdated Components

### What It Is
Applications may rely on outdated libraries, dependencies, or frameworks with known vulnerabilities.

### Related WSTG Tests
- WSTG-INST-01: Reviewing Infrastructure and Dependencies  
- WSTG-CONF-04: Testing Patching Practices  

### Quick Checks
- Run `npm audit`, `pip audit`, `yarn audit`, or dependency scanners  
- Check outdated server modules (Apache, Nginx, PHP, Node, etc.)  

---

# A07: Identification and Authentication Failures

### What It Is
Weak or flawed authentication lets attackers assume other users’ identities.

### Related WSTG Tests
- WSTG-ATHN-01: Testing Authentication Mechanisms  
- WSTG-ATHN-02: Testing Password Management  
- WSTG-ATHN-04: Testing Multi-Factor Authentication  

### Quick Checks
- Test weak password policies  
- Check session timeout and reuse  
- Attempt bypassing MFA  

---

# A08: Software and Data Integrity Failures

### What It Is
Applications that rely on insecure CI/CD pipelines, update mechanisms, or untrusted data sources are exposed to integrity attacks.

### Related WSTG Tests
- WSTG-CODE-01: Testing Code Integrity Controls  
- WSTG-INST-02: Testing for Insecure Deployment 

### Quick Checks
- Check for unsigned updates  
- Verify integrity checks and package-lock files  
- Review CI pipelines for secret leakage  

---

# A09: Security Logging and Monitoring Failures

### What It Is
Insufficient logging allows attackers to go undetected and prevents forensic analysis.

### Related WSTG Tests
- WSTG-LOGG-01: Testing Logging Mechanisms  
- WSTG-LOGG-02: Testing Alerting and Monitoring  

### Quick Checks
- Test failed login attempts and see if they trigger logs  
- Verify audit logs are protected from tampering  

---

# A10: Server-Side Request Forgery (SSRF)

### What It Is
SSRF allows attackers to trick the server into making unauthorized internal requests.

### Related WSTG Tests
- WSTG-INPV-02: Testing for Server-Side Request Forgery  
- WSTG-NETW-01: Testing Network Security Controls  

### Quick Checks
- Try accessing localhost (`http://127.0.0.1:80`) via parameters  
- Attempt hitting cloud instance metadata endpoints  
- Check URL validation logic  

---

# Conclusion

This abbreviated guide provides a simple, Top-10–focused testing baseline for quick assessments.  
It helps highlight the most common risks but **should not** be considered a comprehensive security evaluation.  
Security testers are strongly encouraged to use the full OWASP Web Security Testing Guide (WSTG) for complete coverage.

