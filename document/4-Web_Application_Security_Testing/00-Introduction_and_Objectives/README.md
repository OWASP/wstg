# 4.0 Introduction and Objectives

This section describes the OWASP web application security testing methodology and explains how to test for evidence of vulnerabilities within the application due to deficiencies with identified security controls.

## What is Web Application Security Testing?

A security test is a method of evaluating the security of a computer system or network by methodically validating and verifying the effectiveness of application security controls. A web application security test focuses only on evaluating the security of a web application. The process involves an active analysis of the application for any weaknesses, technical flaws, or vulnerabilities. Any security issues that are found will be presented to the system owner, together with an assessment of the impact, a proposal for mitigation or a technical solution.

## What is a Vulnerability?

A vulnerability is a flaw or weakness in a system's design, implementation, operation or management that could be exploited to compromise the system's security objectives.

## What is a Threat?

A threat is anything (a malicious external attacker, an internal user, a system instability, etc) that may harm the assets owned by an application (resources of value, such as the data in a database or in the file system) by exploiting a vulnerability.

## What is a Test?

A test is an action to demonstrate that an application meets the security requirements of its stakeholders.

## The Approach in Writing this Guide

The OWASP approach is open and collaborative:

- Open: every security expert can participate with their experience in the project. Everything is free.
- Collaborative: brainstorming is performed before the articles are written so the team can share ideas and develop a collective vision of the project. That means rough consensus, a wider audience and increased participation.

This approach tends to result in a defined Testing Methodology that will be:

- Consistent
- Reproducible
- Rigorous
- Under quality control

The problems to be addressed are fully documented and tested. It is important to use various methods to test all the known vulnerabilities and document all the security test activities.

## What Is the OWASP Testing Methodology?

Security testing will never be an exact science where a complete list of all possible issues that should be tested can be defined. In fact, security testing is only one of the several suitable techniques for testing the security of web applications under certain circumstances. The goal of this project is to collect all the possible testing techniques, explain these techniques, and keep the guide updated. The OWASP Web Application Security Testing methodology is based on the black box approach. The tester has little to no information about the application to be tested.

The testing model consists of:

- Tester: Who performs the testing activities
- Tools and methodology: The core of this Testing Guide project
- Application: The black box to test

Testing can be categorized as passive or active:

### Passive Testing

During passive testing, a tester tries to understand the application's logic and explores the application as an end user. Tools can be used for information gathering. For example, an HTTP(S) proxy can be used to observe all the HTTP(S) requests and responses. At the end of this phase, the tester should generally understand all the access points and functionality of the system (e.g., HTTP headers, parameters, cookies, APIs, technology usage/patterns, etc). The [Information Gathering](../01-Information_Gathering/README.md) section explains how to perform passive testing.

For example, a tester may find a page at the following URL: `https://www.example.com/login/auth_form`

This may indicate an authentication form where the application requests a username and password.

The following parameters represent two access points to the application: `https://www.example.com/appx?a=1&b=1`

In this case, the application has two access points (parameters `a` and `b`). All the input points found in this phase represent targets for testing. Keeping track of the directory or call tree of the application and all the access points can be useful during active testing.

### Active Testing

During active testing, a tester uses the methodologies described in the following sections.

The set of active tests have been split into 12 categories:

- Information Gathering
- Configuration and Deployment Management Testing
- Identity Management Testing
- Authentication Testing
- Authorization Testing
- Session Management Testing
- Input Validation Testing
- Testing for Error Handling
- Testing for Weak Cryptography
- Business Logic Testing
- Client-side Testing
- API Testing
