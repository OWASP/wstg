# Reporting

Performing the technical side of the assessment is only half of the overall assessment process. The final product is the production of a well written and informative report. A report should be easy to understand and should highlight all the risks found during the assessment phase. The report should appeal to both executive management and technical staff.

## About This Section

This guide provides only suggestions about one possible approach to reporting, and should not be treated as as strict rules that must be followed. When considering any of the recommendations below, always ask yourself whether the recommendation would improve your report.

This guide to reporting is a best fit for consultancy-based reports. It may be overkill for internal or bug bounty reports.

Regardless of the audience, it's advisable to secure the report and encrypt it to ensure that only the receiving party is able to use it.

A good report helps your client understand your findings and highlights the quality of your technical testing. The quality of the technical testing is completely irrelevant if the client can't understand your findings.

## 1. Introduction

### 1.1 Version Control

Sets report changes, mostly presented in a table format such as the below.

| Version | Description | Date | Author |
|:-------:|-------------|------|--------|
| 1.0 | Initial report | DD/MM/YYYY | J. Doe |

### 1.2 Table of Contents

A table of contents page for the document.

### 1.3 The Team

A list of the team members detailing their expertise and qualifications.

### 1.4 Scope

The boundaries and the needs of the engagement agreed upon with the organization.

### 1.5 Limitations

Limitations can be:

- Out-of-bounds areas in relation to testing.
- Broken functionality.
- Lack of cooperation.
- Lack of time.
- Lack of access or credentials.

### 1.6 Timeline

The duration of the engagement.

### 1.7 Disclaimer

You may wish to provide a disclaimer for your service. Always consult a legal professional in order to create a legally-binding document.

The following example is for illustrative purposes only. It should not be used as-is and does not constitute legal advice.

*This test is a "point in time" assessment and as such the environment could have changed since the test was run. There is no guarantee that all possible security issues have been identified, and that new vulnerabilities may have been discovered since the tests were run. As such, this report serves as a guiding document and not a warranty that the report provides a full representation of the risks threatening the systems at hand.*

## 2. Executive Summary

This is like the elevator pitch of the report, it aims at providing executives with:

- The objective of the test.
    - Describe the business need behind the security test.
    - Describe how the tests helped the organization understand their systems.
- Key findings in a business context, such as possible compliance issues, reputation damage, etc. Focus on the business impact and leave out technical details for now.
- The strategic recommendations on how the business can stop the issues from happening again. Describe these in a non-technical context and leave specific technical recommendations out for now.

The summary should be constructive and meaningful. Avoid jargon and negative speculation. If figures, graphs, or illustrations are used, ensure they help deliver a message in a clearer way than text would.

## 3. Findings

This section is aimed at the technical team. It should include all the necessary information to understand the vulnerability, replicate it, and resolve it. Logical separation can help improve the readability of the report. For example, you might have separate sections titled "External Access" and "Internal Access".

If this is a re-test, you might create a subsection that summarizes findings of the previous test, the updated status of previously identified vulnerabilities, and any cross-references with the current test.

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
    - How easy it is to exploit.
    - Whether there is working exploit code for it.
    - The level of access required.
    - Attacker motivation to exploit it.
- The impact of the vulnerability on the system.
- Risk of the vulnerability on the application.
    - Some suggested values are: Informational, Low, Medium, High, and Critical. Ensure that you detail the values you decide to use in an appendix. This allows the reader to understand how each score is determined.
    - On certain engagements it is required to have a [CVSS](https://www.first.org/cvss/) score. If not required, sometimes it is good to have, and other times it just adds complexity to the report.
- Detailed description of what the vulnerability is, how to exploit it, and the damage that may result from its exploitation. Any possibly-sensitive data should be masked, for example, passwords, personal information, or credit card details.
- Detailed steps on how to remediate the vulnerability, possible improvements that could help strengthen the security posture, and missing security practices.
- Additional resources that could help the reader to understand the vulnerability, such as an image, a video, a CVE, an external guide, etc.

Format this section in a way that best delivers your message.

Always ensure that your descriptions provide enough information for the engineer reading this report to take action based on it. Explain the finding thoroughly and provide as much technical detail as might be necessary to remedy it.

## Appendices

Multiple appendices can be added, such as:

- Test methodology used.
- Severity and risk rating explanations.
- Relevant output from tools used.
    - Make sure to clean the output and not just dump it.
- A checklist of all the tests conducted, such as the [WSTG checklists](https://github.com/OWASP/wstg/tree/master/checklists). These can be provided as attachments to the report.

## References

This section is not part of the suggested report format. The below links provide more guidance to writing your reports.

- [SANS: Tips for Creating a Strong Cybersecurity Assessment Report](https://www.sans.org/blog/tips-for-creating-a-strong-cybersecurity-assessment-report/)
- [SANS: Writing a Penetration Testing Report](https://www.sans.org/reading-room/whitepapers/bestprac/paper/33343)
- [Infosec Institute: The Art of Writing Penetration Test Reports](https://resources.infosecinstitute.com/topic/writing-penetration-testing-reports/)
- [Dummies: How to Structure a Pen Test Report](https://www.dummies.com/computers/macs/security/how-to-structure-a-pen-test-report/)
- [Rhino Security Labs: Four Things Every Penetration Test Report Should Have](https://rhinosecuritylabs.com/penetration-testing/four-things-every-penetration-test-report/)
