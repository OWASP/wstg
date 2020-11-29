# Reporting

Performing the technical side of the assessment is only half of the overall assessment process. The final product is the production of a well written and informative report. A report should be easy to understand and should highlight all the risks found during the assessment phase. The report should appeal to both executive management and technical staff.

Note: It is advised to secure the report and encrypt it to ensure that only the receiving party is able to use it.

## 1. Introduction

### 1.1 Version Control

Sets report changes, mostly presented in a table format such as the below.

| Version | Description | Date | Author |
|:-------:|-------------|------|--------|
| 1.0 | Initial report | DD/MM/YYYY | Foo Bar |

### 1.2 Table of Contents

A table of contents page for the document.

### 1.3 The Team

A list of the team members detailing their expertise and qualifications.

### 1.4 Scope

The boundaries and the needs of the engagement agreed upon with the organization.

### 1.5 Limitations

Limitations can be:

- Areas that were off boundaries that related to the test.
- Broken functionality.
- Lack of cooperation.
- Lack of time.
- Lack of accesses.

### 1.6 Timeline

The duration of the engagement.

### 1.7 Disclaimer

A disclaimer providing legal protection. The below example should be modified to your use case and shouldn't be used as is.

*This test is a "point in time" assessment and as such the environment could have changed since the test was run. There is no guarantee that all possible security issues have been identified, and that new vulnerabilities may have been discovered since the tests were run. Thus, this report serves as a guiding document and not a warranty that the report provides a full representation of the risks threatening the systems at hand.*

## 2. Executive Summary

This is like the elevator pitch of the report, it aims at providing executives with:

- The objective of the test, which contains the need for it and the answers that the organization need to better understand their systems.
- The key findings in a business context, such as compliance issues, reputational damage, etc.
  - It shouldn't state the technical findings and the technical impact. Only discuss the business impact.
- The strategic recommendations on how the business can stop the issues from happening again.
  - It shouldn't state technical and specific recommendations, as this concerns the technical team.

**Note:** The summary should be constructive and meaningful, not full of jargon and destructive takeaways. In case graphs are used, make sure they help deliver a message in a clearer way than text would.

## 3. Findings

This section is aimed at the technical team. It should include all the necessary information to understand the vulnerability, replicate it, and resolve it. Logical separation can help improve the readability of the report (*e.g* external access, internal access, etc.)

*If this is a re-test, a subsection could be set with the findings summary of the previous test, the status of the identified vulnerabilities, and any cross-references with the current test.*

### 3.1 Findings Summary

A list of the findings with their risk level. A table can be used for ease of use by both teams.

| Ref. ID |  Title | Risk Level |
|:------------:|--------|------------|
| 1 | User Authentication Bypass | High |

### 3.2 Findings Details

Each finding should be detailed with the following information:

- Reference ID, which can be used for communication between parties and for cross-references across the report.
- The vulnerability title, such as "User Authentication Bypass".
- The likelihood or exploitability of the issue, based on various factors such as:
  - How easy it is to exploit it.
  - Whether there is a working exploit code for it.
  - The level of access required.
  - Attacker motivation to exploit it.
- The impact of the vulnerability on the system.
- Risk of the vulnerability on the application.
  - Possible values are: "Informational", "Low", "Medium", "High", "Critical".
    - The values set in here should be detailed in an appendix to allow the reader to understand how each score was set.
  - On certain engagements it is required to have a [CVSS](https://www.first.org/cvss/) score. If not required, sometimes it is good to have, and other times it just adds complexity to the report.
- Detailed description of what the vulnerability is, how to exploit it, and the damage that may result from its abuse. Any sensitive data should be masked (*e.g.* passwords, personal information, credit card details, etc.)
- Detailed steps on how to remediate the vulnerability, possible improvements that could help strengthen the security posture, and missing security practices.
- Additional resources that could help the reader to understand the vulnerability, such as an image, a video, a CVE, an external guide, etc.

The above can be formatted in the way the tester deems as fitting to deliver their message in the best possible way.

**Note:** Always check if the issue provides enough information for the engineer reading this report and if they can take action based on it. If not, the issue should be better explained.

## Appendices

Multiple appendices can be added, such as:

- Test methodology used.
- Severity and risk rating explanations.
- Relevant output from tools used.
  - Make sure to clean the output and not just dump it.
- A checklist of all the tests conducted, such as the [WSTG checklist](https://github.com/OWASP/wstg/tree/master/checklist). These can be provided as attachments to the report.

## References

_This is not part of the report. More guidance to writing your reports._

- [SANS: Tips for Creating a Strong Cybersecurity Assessment Report](https://www.sans.org/blog/tips-for-creating-a-strong-cybersecurity-assessment-report/)
- [SANS: Writing a Penetration Testing Report](https://www.sans.org/reading-room/whitepapers/bestprac/paper/33343)
- [Infosec Institute: The Art of Writing Penetration Test Reports](https://resources.infosecinstitute.com/topic/writing-penetration-testing-reports/)
- [Dummies: How to Structure a Pen Test Report](https://www.dummies.com/computers/macs/security/how-to-structure-a-pen-test-report/)
- [Rhino Security Labs: Four Things Every Penetration Test Report Should Have](https://rhinosecuritylabs.com/penetration-testing/four-things-every-penetration-test-report/)
