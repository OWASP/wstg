# Reporting

Performing the technical side of the assessment is only half of the overall assessment process. The final product is the production of a well written and informative report. A report should be easy to understand and should highlight all the risks found during the assessment phase. The report should appeal to both executive management and technical staff.

Note: It is advised to secure the report by using a password or any similar technology as pentest reports are marked as sensitive information.

## 1. Executive Summary

This is like the elevator pitch of the report, it aims at providing executives with:

- the run down of the report in a page or two.
- quick actions and their criticality.
- the status of their application.

### 1.1 Objective

The purpose of this engagement and the need for it.

### 1.2 Scope

What this test will cover precisely. This is crucial in order to set the boundaries of the engagement.

### 1.3 Timeline

The duration of the engagement.

### 1.4 Summary

The summary should contain, in the best possible form to deliver the message (*e.g.* graphs, tables, lists, etc.):

- Key risks identified by the test.
- Key recommendations for the organization.
- State of the application. A concise and direct conclusion that states whether the application is secure or not.

**Note:** The summary should be constructive and meaningful, not full of jargon and destructive takeaways.

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
