# Foreword by Eoin Keary

The problem of insecure software is perhaps the most important technical challenge of our time. The dramatic rise of web applications enabling business, social networking etc has only compounded the requirements to establish a robust approach to writing and securing our Internet, Web Applications and Data.

At the Open Web Application Security Project® (OWASP®), we're trying to make the world a place where insecure software is the anomaly, not the norm. The OWASP Testing Guide has an important role to play in solving this serious issue. It is vitally important that our approach to testing software for security issues is based on the principles of engineering and science. We need a consistent, repeatable and defined approach to testing web applications. A world without some minimal standards in terms of engineering and technology is a world in chaos.

It goes without saying that you can't build a secure application without performing security testing on it. Testing is part of a wider approach to build a secure system. Many software development organizations do not include security testing as part of their standard software development process. What is even worse is that many security vendors deliver testing with varying degrees of quality and rigor.

Security testing, by itself, isn't a particularly good stand alone measure of how secure an application is, because there are an infinite number of ways that an attacker might be able to make an application break, and it simply isn't possible to test them all. We can't hack ourselves secure as we only have a limited time to test and defend where an attacker does not have such constraints.

In conjunction with other OWASP projects such as the Code Review Guide, the Development Guide and tools such as [ZAP](https://www.zaproxy.org/), this is a great start towards building and maintaining secure applications. This Testing Guide will show you how to verify the security of your running application. I highly recommend using these guides as part of your application security initiatives.

## Why OWASP?

Creating a guide like this is a huge undertaking, requiring the expertise of hundreds of people around the world. There are many different ways to test for security flaws and this guide captures the consensus of the leading experts on how to perform this testing quickly, accurately, and efficiently. OWASP gives like minded security folks the ability to work together and form a leading practice approach to a security problem.

The importance of having this guide available in a completely free and open way is important for the foundation's mission. It gives anyone the ability to understand the techniques used to test for common security issues. Security should not be a black art or closed secret that only a few can practice. It should be open to all and not exclusive to security practitioners but also QA, Developers and Technical Managers. The project to build this guide keeps this expertise in the hands of the people who need it - you, me and anyone that is involved in building software.

This guide must make its way into the hands of developers and software testers. There are not nearly enough application security experts in the world to make any significant dent in the overall problem. The initial responsibility for application security must fall on the shoulders of the developers because they write the code. It shouldn't be a surprise that developers aren't producing secure code if they're not testing for it or consider the types of bugs which introduce vulnerability.

Keeping this information up to date is a critical aspect of this guide project. By adopting the wiki approach, the OWASP community can evolve and expand the information in this guide to keep pace with the fast moving application security threat landscape.

This Guide is a great testament to the passion and energy our members and project volunteers have for this subject. It shall certainly help to change the world a line of code at a time.

## Tailoring and Prioritizing

You should adopt this guide in your organization. You may need to tailor the information to match your organization's technologies, processes, and organizational structure.

In general there are several different roles within organizations that may use this guide:

- Developers should use this guide to ensure that they are producing secure code. These tests should be a part of normal code and unit testing procedures.
- Software testers and QA should use this guide to expand the set of test cases they apply to applications. Catching these vulnerabilities early saves considerable time and effort later.
- Security specialists should use this guide in combination with other techniques as one way to verify that no security holes have been missed in an application.
- Project Managers should consider the reason this guide exists and that security issues are manifested via bugs in code and design.

The most important thing to remember when performing security testing is to continuously re-prioritize. There are infinite ways that an application could fail, and organizations always have limited testing time and resources. Be sure time and resources are spent wisely. Try to focus on the security holes that are a real risk to your business. Try to contextualize risk in terms of the application and its use cases.

This guide is best viewed as a set of techniques that you can use to find different types of security holes. But not all the techniques are equally important. Try to avoid using the guide as a checklist, new vulnerabilities are always manifesting and no guide can be an exhaustive list of "things to test for", but rather a great place to start.

## The Role of Automated Tools

There are a number of companies selling automated security analysis and testing tools. Remember the limitations of these tools so that you can use them for what they're good at. As Michael Howard put it at the 2006 OWASP AppSec Conference in Seattle, "Tools do not make software secure! They help scale the process and help enforce policy."

Most importantly, these tools are generic - meaning that they are not designed for your custom code, but for applications in general. That means that while they can find some generic problems, they do not have enough knowledge of your application to allow them to detect most flaws. In my experience, the most serious security issues are the ones that are not generic, but deeply intertwined in your business logic and custom application design.

These tools can also be very useful, since they do find lots of potential issues. While running the tools doesn't take much time, each one of the potential problems takes time to investigate and verify. If the goal is to find and eliminate the most serious flaws as quickly as possible, consider whether your time is best spent with automated tools or with the techniques described in this guide. Still, these tools are certainly part of a well-balanced application security program. Used wisely, they can support your overall processes to produce more secure code.

## Call to Action

If you're building, designing or testing software, I strongly encourage you to get familiar with the security testing guidance in this document. It is a great road map for testing the most common issues that applications are facing today, but it is not exhaustive. If you find errors, please add a note to the discussion page or make the change yourself. You'll be helping thousands of others who use this guide.

Please consider [joining us](https://owasp.org/membership/) as an individual or corporate member so that we can continue to produce materials like this testing guide and all the other great projects at OWASP.

Thank you to all the past and future contributors to this guide, your work will help to make applications worldwide more secure.

--Eoin Keary, OWASP Board Member, April 19, 2013

Open Web Application Security Project and OWASP are registered trademarks of the OWASP Foundation, Inc.
