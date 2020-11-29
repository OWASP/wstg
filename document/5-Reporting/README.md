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
- The status of the application.

**Note:** The summary should be constructive and meaningful, not full of jargon and destructive takeaways. In case graphs are used, make sure they help deliver a message in a clearer way than text would.

## 2. Detailed Findings

This section is aimed at the technical team. It should include all the necessary information to understand the vulnerability, replicate it, and resolve it.

Each finding should be detailed with the following information:

- Reference ID, which can be used for communication between parties and for other references across the report.
- The vulnerability identified in a clear form, such as "Privilege Escalation from Client to Admin".
- Exploitability, or likelihood. This states the persona that is capable of exploiting said vulnerability based on how easy it is to achieve it, the level of access, and the impact achieved, which is related to the motivation behind an attack.
  - Possible values are "User", "Technical", "Hacker".
- Risk of the vulnerability on the application.
  - Possible values are: "Informational", "Low", "Medium", "High", "Critical".
  - On certain engagements it is required to have a [CVSS](https://www.first.org/cvss/) score. If not required, sometimes it is good to have, and other times it just adds complexity to the report.
- A detailed description of what the vulnerability is, how to exploit it, and the damage that may result from its abuse.
- A detailed remediation on how to resolve the vulnerability, possible improvements that could help strengthen the posture, and missing security practices.
- Provide any additional resources that could help the reader to understand the vulnerability, such as an image, a video, a CVE, an external guide, etc.

Findings can be delivered in normal format, like the above, it could be delivered in a table format that can formatted in various ways, or any other format that the testers see as fitting to deliver the message in a more comprehensible format.

## 3. Conclusion

State the organization's next steps, specifying the positive and negative findings of the report, and improvements on a big picture, such as "implement unit tests across the organization to set a security baseline".

This should be concise, providing the organization with high level points to go after, risks to consider before going live, etc.

## Appendices

Multiple appendices can be added, such as:

- Test methodology used.
- Severity and risk rating explanations.
- Tools used, scripts, and the relevant generated output.
  - Make sure to clean the output and not just dump it.
- A checklist of all the tests conducted, such as the [WSTG checklist](https://github.com/OWASP/wstg/tree/master/checklist). These can be provided as attachments to the report.

## References

_This is not part of the report. More guidance to writing your reports._

- [SANS: Tips for Creating a Strong Cybersecurity Assessment Report](https://www.sans.org/blog/tips-for-creating-a-strong-cybersecurity-assessment-report/)
- [SANS: Writing a Penetration Testing Report](https://www.sans.org/reading-room/whitepapers/bestprac/paper/33343)
- [Infosec Institute: The Art of Writing Penetration Test Reports](https://resources.infosecinstitute.com/topic/writing-penetration-testing-reports/)
- [Dummies: How to Structure a Pen Test Report](https://www.dummies.com/computers/macs/security/how-to-structure-a-pen-test-report/)
- [Rhino Security Labs: Four Things Every Penetration Test Report Should Have](https://rhinosecuritylabs.com/penetration-testing/four-things-every-penetration-test-report/)
