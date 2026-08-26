# Bug Bounty Programs as a Testing Technique

## Overview

A bug bounty or coordinated vulnerability disclosure program is a complementary testing technique. The organization publishes a scope, rules of engagement, and reward structure. External security researchers (known as "bug bounty hunters" or "hackers") probe the target for vulnerabilities. Accepted findings are reported confidentially, remediated, and the researcher is compensated. Unlike a traditional penetration test, a bounty program is continuous (not time-boxed), crowd-sourced (not a single team), and often conducted black-box (researchers have no special access or documentation).

The [2025 HackerOne Hacker-Powered Security Report](https://www.hackerone.com/resources/reports/hacker-powered-security-report-2025) found that HackerOne alone processed over 85,000 valid vulnerability reports in 2025, with payouts reaching USD $81 million. Researcher adoption of AI tooling is high (82% of Bugcrowd's hacker respondents in their 2026 report use AI), and programs explicitly scoped for AI systems and APIs are growing rapidly - reflecting both the value and the operational maturity of bounty programs as a testing channel.

## How This Differs from Traditional Penetration Testing

| Aspect | Penetration Test | Bug Bounty Program |
|--------|------------------|-------------------|
| **Duration** | Time-boxed (e.g., 2 weeks) | Continuous (6 months - indefinite) |
| **Tester** | Single team or consultant | Crowd-sourced, anonymous |
| **Access & Documentation** | Usually white-box or gray-box; source code, architecture, threat models provided | Black-box; only the published scope and rules of engagement |
| **Scope** | Negotiated statement of work (SOW); can expand as needs change | Unilaterally defined by the program owner; researchers must work strictly within published scope |
| **Rules** | Custom per engagement | Standard program terms and disclosure policy |
| **Cost Model** | Fixed fee or hourly rate | Pay-per-finding (bounty tiers by severity) |
| **Reporting** | Formal consultancy report with executive summary, root causes, remediation | Submission per finding (detailed but not an integrated report) |

## Applying WSTG Techniques Within a Bug Bounty Program

The testing techniques described in [Section 4](../4-Web_Application_Security_Testing/README.md) of the WSTG - from information gathering to business logic testing - remain fully applicable within a bug bounty program. What changes is how and when you select them:

- A penetration tester given an SOW and architecture documentation can plan a testing roadmap. A bounty researcher works reactively, discovering the application as they go, within the published scope.
- A consultant may spend hours on deep business logic analysis. A bounty researcher may submit dozens of findings across multiple severity levels and take the highest-impact ones.
- Pentest methodology is structured and sequential. Bounty researchers often run automated tools in parallel and follow promising leads.

## Reporting Under a Bounty Program

See the [Reporting](../5-Reporting/01-Reporting_Structure.md) section of this guide for general reporting guidance. Bug bounty submissions typically differ in format and context:

- **Minimum required**: reproduction steps (how to trigger the vulnerability), impact (what an attacker could do), and remediation guidance (what the developer should fix).
- **Severity assessment**: many programs use CVSS scoring, while others define program-specific severity rubrics (Critical / High / Medium / Low). Clarify the rubric in your program's terms.
- **Scope clarity**: a bounty report is only valuable if it falls clearly within the program's stated scope. A report on an out-of-scope third-party service, a staged/test environment, or a deprecated code branch will be rejected regardless of validity.

The [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) and [Reporting](../5-Reporting/) section provide guidance on writing clear, actionable findings.

## Designing a Program: Scope and Disclosure

A successful bug bounty program starts with a clear, published scope document that answers:

- **In-scope targets**: which domains, applications, APIs, and infrastructure are researchers allowed to test? (e.g., "api.example.com and all subdomains; NOT example-staging.com or third-party integrations").
- **Authorization and legal safe harbor**: researchers acting in good faith within scope are authorized and will not face legal action (explicitly granted in the program terms).
- **Rules of engagement**: what testing techniques are permitted? (most programs allow reconnaissance and vulnerability testing, but prohibit social engineering, DoS attacks, and destruction/data exfiltration beyond proof-of-concept).
- **Disclosure timeline**: how much time does the organization have to remediate before the researcher may disclose publicly? (typical: 30-90 days).
- **Reward tiers**: what is the bounty payout for Critical / High / Medium / Low findings? (amount varies by organization size and risk tolerance; may also vary by finding type, e.g., authentication bypass pays more than XSS).

Publish these details in a public `security.txt` file ([RFC 9116](https://datatracker.ietf.org/doc/html/rfc9116)) or a dedicated security page, and register with platforms like [HackerOne](https://www.hackerone.com/), [Bugcrowd](https://www.bugcrowd.com/), or [Intigriti](https://www.intigriti.com/) if you want a managed program. Self-hosted programs (custom web form or email intake) are also viable for smaller organizations.

For organizations seeking a lower-friction starting point, the [OWASP Bug Logging Tool (BLT)](https://owasp.org/www-project-bug-logging-tool/) provides a framework for internal, ad-hoc bug bounty programs where developers, security teams, or other staff can log and track vulnerabilities found when attacking their own applications on a scheduled or continuous basis. BLT is ideal for maturing a security culture and running internal penetration testing campaigns without the overhead of a formal external bug bounty program.

## Where to Learn More

- [EdOverflow Bug Bounty Cheat Sheet](https://github.com/EdOverflow/bugbounty-cheatsheet): practical tips for researchers submitting to bounty programs.
- [HackerOne Community](https://www.hackerone.com/): reports, research, and community resources.
- [Bugcrowd Resources](https://www.bugcrowd.com/resources/): reports on hacker trends and program best practices.
- [Open Bug Bounty](https://www.openbugbounty.org/): formal coordinated disclosure for critical internet infrastructure and open-source projects.

## References

- [2025 HackerOne Hacker-Powered Security Report](https://www.hackerone.com/resources/reports/hacker-powered-security-report-2025)
- [2026 Bugcrowd Inside the Mind of a Hacker Report](https://www.bugcrowd.com/blog/inside-the-mind-of-a-hacker-2026/)
- [OWASP Vulnerability Disclosure Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html)
