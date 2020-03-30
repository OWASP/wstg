# Testing Checklist

The following is the list of controls to test during the assessment:

| Ref. No. | Category     | Test Name                  |
|----------|--------------|----------------------------|
| **4.2**  | **WSTG-INFO** | **Information Gathering**  |
| 4.2.1    | WSTG-INFO-01 | Conduct Search Engine Discovery and Reconnaissance for Information Leakage |
| 4.2.2    | WSTG-INFO-02 | Fingerprint Web Server |
| 4.2.3    | WSTG-INFO-03 | Review Webserver Metafiles for Information Leakage |
| 4.2.4    | WSTG-INFO-04 | Enumerate Applications on Webserver |
| 4.2.5    | WSTG-INFO-05 | Review Webpage Comments and Metadata for Information Leakage |
| 4.2.6    | WSTG-INFO-06 | Identify application entry points |
| 4.2.7    | WSTG-INFO-07 | Map execution paths through application |
| 4.2.8    | WSTG-INFO-08 | Fingerprint Web Application Framework |
| 4.2.9    | WSTG-INFO-09 | Fingerprint Web Application |
| 4.2.10   | WSTG-INFO-10 | Map Application Architecture  |
| **4.3**    | **WSTG-CONFIG** | **Configuration and Deploy Management Testing** |
| 4.3.1    | WSTG-CONF-01 | Test Network/Infrastructure Configuration |
| 4.3.2    | WSTG-CONF-02 | Test Application Platform Configuration |
| 4.3.3    | WSTG-CONF-03 | Test File Extensions Handling for Sensitive Information |
| 4.3.4    | WSTG-CONF-04 | Backup and Unreferenced Files for Sensitive Information |
| 4.3.5    | WSTG-CONF-05 | Enumerate Infrastructure and Application Admin Interfaces  |
| 4.3.6    | WSTG-CONF-06 | Test HTTP Methods |
| 4.3.7    | WSTG-CONF-07 | Test HTTP Strict Transport Security |
| 4.3.8    | WSTG-CONF-08 | Test RIA cross domain policy |
| **4.4**  | **WSTG-IDENT**  | **Identity Management Testing** |
| 4.4.1    | WSTG-IDNT-01  | Test Role Definitions |
| 4.4.2    | WSTG-IDNT-02  | Test User Registration Process |
| 4.4.3    | WSTG-IDNT-03  | Test Account Provisioning Process |
| 4.4.4    | WSTG-IDNT-04  | Testing for Account Enumeration and Guessable User Account |
| 4.4.5    | WSTG-IDNT-05  | Testing for Weak or unenforced username policy |
| 4.4.6    | WSTG-IDNT-06  | Test Permissions of Guest/Training Accounts |
| 4.4.7    | WSTG-IDNT-07  | Test Account Suspension/Resumption Process  |
| **4.5**  | **WSTG-AUTHN**  | **Authentication Testing** |
| 4.5.1    | WSTG-ATHN-01  | Testing for Credentials Transported over an Encrypted Channel |
| 4.5.2    | WSTG-ATHN-02  | Testing for default credentials |
| 4.5.3    | WSTG-ATHN-03  | Testing for Weak lock out mechanism |
| 4.5.4    | WSTG-ATHN-04  | Testing for bypassing authentication schema |
| 4.5.5    | WSTG-ATHN-05  | Test remember password functionality |
| 4.5.6    | WSTG-ATHN-06  | Testing for Browser cache weakness |
| 4.5.7    | WSTG-ATHN-07  | Testing for Weak password policy |
| 4.5.8    | WSTG-ATHN-08  | Testing for Weak security question/answer |
| 4.5.9    | WSTG-ATHN-09  | Testing for weak password change or reset functionalities |
| 4.5.10   | WSTG-ATHN-10  | Testing for Weaker authentication in alternative channel |
| **4.6**  | **WSTG-AUTHZ** | **Authorization Testing** |
| 4.6.1    | WSTG-ATHZ-01 | Testing Directory traversal/file include |
| 4.6.2    | WSTG-ATHZ-02 | Testing for bypassing authorization schema |
| 4.6.3    | WSTG-ATHZ-03 | Testing for Privilege Escalation |
| 4.6.4    | WSTG-ATHZ-04 | Testing for Insecure Direct Object References |
| **4.7**  | **WSTG-SESS**  | **Session Management Testing** |
| 4.7.1    | WSTG-SESS-01  | Testing for Bypassing Session Management Schema |
| 4.7.2    | WSTG-SESS-02  | Testing for Cookies attributes |
| 4.7.3    | WSTG-SESS-03  | Testing for Session Fixation |
| 4.7.4    | WSTG-SESS-04  | Testing for Exposed Session Variables |
| 4.7.5    | WSTG-SESS-05  | Testing for Cross Site Request Forgery |
| 4.7.6    | WSTG-SESS-06  | Testing for logout functionality |
| 4.7.7    | WSTG-SESS-07  | Test Session Timeout |
| 4.7.8    | WSTG-SESS-08  | Testing for Session puzzling |
| **4.8**  | **WSTG-INPVAL** | **Data Validation Testing** |
| 4.8.1    | WSTG-INPV-01 | Testing for Reflected Cross Site Scripting |
| 4.8.2    | WSTG-INPV-02 | Testing for Stored Cross Site Scripting |
| 4.8.3    | WSTG-INPV-03 | Testing for HTTP Verb Tampering |
| 4.8.4    | WSTG-INPV-04 | Testing for HTTP Parameter pollution |
| 4.8.5    | WSTG-INPV-05 | Testing for SQL Injection |
| 4.8.5.1  |                | Oracle Testing |
| 4.8.5.2  |                | MySQL Testing |
| 4.8.5.3  |                | SQL Server Testing |
| 4.8.5.4  |                | Testing PostgreSQL |
| 4.8.5.5  |                | MS Access Testing |
| 4.8.5.6  |                | Testing for NoSQL injection |
| 4.8.6    | WSTG-INPV-06 | Testing for LDAP Injection |
| 4.8.7    | WSTG-INPV-07 | Testing for ORM Injection |
| 4.8.8    | WSTG-INPV-08 | Testing for XML Injection |
| 4.8.9    | WSTG-INPV-09 | Testing for SSI Injection |
| 4.8.10   | WSTG-INPV-10 | Testing for XPath Injection |
| 4.8.11   | WSTG-INPV-11 | IMAP/SMTP Injection |
| 4.8.12   | WSTG-INPV-12 | Testing for Code Injection |
| 4.8.12.1 |                | Testing for Local File Inclusion |
| 4.8.12.2 |                | Testing for Remote File Inclusion |
| 4.8.13   | WSTG-INPV-13 | Testing for Command Injection |
| 4.8.14   | WSTG-INPV-14 | Testing for Buffer overflow |
| 4.8.14.1 |                | Testing for Heap overflow |
| 4.8.14.2 |                | Testing for Stack overflow |
| 4.8.14.3 |                | Testing for Format string |
| 4.8.15   | WSTG-INPV-15 | Testing for incubated vulnerabilities |
| 4.8.16   | WSTG-INPV-16 | Testing for HTTP Splitting/Smuggling |
| **4.9**  | **WSTG-ERR**    | **Error Handling** |
| 4.9.1    | WSTG-ERRH-01    | Analysis of Error Codes |
| 4.9.2    | WSTG-ERRH-02    | Analysis of Stack Traces |
| **4.10** | **WSTG-CRYPST** | **Cryptography** |
| 4.10.1   | WSTG-CRYP-01 | Testing for Weak SSL/TSL Ciphers, Insufficient Transport Layer Protection  |
| 4.10.2   | WSTG-CRYP-02 | Testing for Padding Oracle |
| 4.10.3   | WSTG-CRYP-03 | Testing for Sensitive information sent via unencrypted channels |
| **4.11** | **WSTG-BUSLOGIC** | **Business Logic Testing** |
| 4.11.1   | WSTG-BUSLOGIC-001 | Test Business Logic Data Validation |
| 4.11.2   | WSTG-BUSLOGIC-002 | Test Ability to Forge Requests |
| 4.11.3   | WSTG-BUSLOGIC-003 | Test Integrity Checks |
| 4.11.4   | WSTG-BUSLOGIC-004 | Test for Process Timing |
| 4.11.5   | WSTG-BUSLOGIC-005 | Test Number of Times a Function Can be Used Limits |
| 4.11.6   | WSTG-BUSLOGIC-006 | Testing for the Circumvention of Work Flows |
| 4.11.7   | WSTG-BUSLOGIC-007 | Test Defenses Against Application Misuse |
| 4.11.8   | WSTG-BUSLOGIC-008 | Test Upload of Unexpected File Types |
| 4.11.9   | WSTG-BUSLOGIC-009 | Test Upload of Malicious Files |
| **4.12** | **WSTG-CLIENT** | **Client Side Testing** |
| 4.12.1   | WSTG-CLIENT-001 | Testing for DOM based Cross Site Scripting |
| 4.12.2   | WSTG-CLIENT-002 | Testing for JavaScript Execution |
| 4.12.3   | WSTG-CLIENT-003 | Testing for HTML Injection |
| 4.12.4   | WSTG-CLIENT-004 | Testing for Client Side URL Redirect |
| 4.12.5   | WSTG-CLIENT-005 | Testing for CSS Injection |
| 4.12.6   | WSTG-CLIENT-006 | Testing for Client Side Resource Manipulation |
| 4.12.7   | WSTG-CLIENT-007 | Test Cross Origin Resource Sharing |
| 4.12.8   | WSTG-CLIENT-008 | Testing for Cross Site Flashing |
| 4.12.9   | WSTG-CLIENT-009 | Testing for Clickjacking |
| 4.12.10  | WSTG-CLIENT-010 | Testing WebSockets |
| 4.12.11  | WSTG-CLIENT-011 | Test Web Messaging |
| 4.12.12  | WSTG-CLIENT-012 | Test Local Storage |
