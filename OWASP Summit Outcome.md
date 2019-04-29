OWASP Testing Guide v5 Track at the OWASP SUMMIT 2017
-----------------------------------------------------

14-15th June, 2017

TASKS DONE:
---------------------
- Brainstorming regarding the new activities to perform to improve the guide
- Alignment with OWASP guides: Development Guide, Code Review Guide, ASVS, Top10, Testing Checklist, ZAP, Vulnerability list
- Discussion on tools
- Add the list of new tests to the v5

OUTCOME
-----------------
NEW TESTS TO WRITE:
- Server-Side Request Forgery (SSRF)
- Server-side Remote Code Execution (RCE)
- XML External Entity Attacks (XXE)
- Self Based DOM XSS
- Authorization bypass horizontal 
- Authorization bypass vertical
- Server-Side Template Injection (SSTI) 
- Host Header Attack
- SPARQL Injection
- Testing for Deserialization of untrusted data
- API Abuse
- Testing Content Security Policy V2 (CSP)?
- Testing for SSO?

REVIEW:
- Client Side Testing
- ORM Injection 
- Authorization Testing
- Information and Config management testing
- Authentication Testing: add oauth testing
- Reporting: adding how to create security testing case for devs
- https://www.owasp.org/index.php/Test_Local_Storage_(OTG-CLIENT-012) add Client Side SQLi

Two questions for OWASP:
------------------------------------
- TOOLS discussion: in the old version of Testing Guide we cited open source and commercial ones for each type of test to perform that could help during the analysis. Would you like to cite both?

- CWE: many companies are using this standard, but at the moment not all the Testing Guide tests are mapped to a specified CWE. Is it possible to set up a working team with CWE in order to update it with all the tests we describe in the Testing Guide?

# Project Summit 2017 Update

THIS IS THE OWASP TESTING GUIDE PROJECT ROADMAP FOR V5.

## WHAT
The OWASP Testing Guide v4 includes a “best practice” penetration testing framework which users can implement in their own organisations. The Testing Guide v4 also includes a “low level” penetration testing guide that describes techniques for testing the most common web application and web service security issues. Today the Testing Guide is the standard to perform Web Application Penetration Testing, and many companies around the world have adopted it. It is vital to maintain an updated project that represents the state of the art for WebAppSec.

The aim of the Working Session is to discuss and define the scope and content of OWASP Testing Guide v5.

## OUTCOMES
* All sections in v4 reviewed
* Project aligned with the ASVS and OWASP Top 10 vulnerabilities
* A more readable guide created that eliminates sections that are not useful
* New testing techniques inserted
* Some sections rationalised as Session Management Testing
* New section created: Client side security and Firefox extensions testing
* Project v5 Deadlines:
* 1: Setup the team of authors
* 2: Start a brainstorming for the new index starting from “Release Description”
* 3: Create the new index and confirm new team
* 4: Start writing articles first phase
* 5: OWASP Summit TGv5 review and brainstorming
* 6: Start writing articles II phase
* 7: Start the second review phase
* 8: Create the RC1
* 9: Release version 5

## Test Changes
This outline will include proposed test changes that need to be incorporated into OTG v5. These should be proposed significant changes that are associated with an explicit test.

### New Tests
* Server-Side Template Injection

### Test Changes
* Testing for Horizontal Bypassing Authorization Schema
* Testing for CSRF

### Deprecated Tests
* *(Include brief explanation of reasoning)*

## Methodology Changes
* *(Include brief explanation of reasoning)*