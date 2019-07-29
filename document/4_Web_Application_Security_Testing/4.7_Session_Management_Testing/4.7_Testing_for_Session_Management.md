# 4.7 Session Management Testing

One of the core components of any web-based application is the mechanism by which it controls and maintains the state for a user interacting with it. This is referred to this as Session Management and is defined as the set of all controls governing state-full interaction between a user and the web-based application. This broadly covers anything from how user authentication is performed, to what happens upon them logging out.

HTTP is a stateless protocol, meaning that web servers respond to client requests without linking them to each other. Even simple application logic requires a user's multiple requests to be associated with each other across a "session”. This necessitates third party solutions – through either Off-The-Shelf (OTS) middleware and web server solutions, or bespoke developer implementations. Most popular web application environments, such as ASP and PHP, provide developers with built-in session handling routines. Some kind of identification token will typically be issued, which will be referred to as a “Session ID” or Cookie.

There are a number of ways in which a web application may interact with a user. Each is dependent upon the nature of the site, the security, and availability requirements of the application. Whilst there are accepted best practices for application development, such as those outlined in the OWASP Guide to Building Secure Web Applications, it is important that application security is considered within the context of the provider’s requirements and expectations.

This chapter covers the following topics:

[4.7.1 Testing for Bypassing Session Management Schema (OTG-SESS-001)](4.7.1_Testing_for_Session_Management_Schema_OTG-SESS-001.md)

[4.7.2 Testing for Cookies Attributes (OTG-SESS-002)](4.7.2_Testing_for_Cookies_Attributes_OTG-SESS-002.md)

[4.7.3 Testing for Session Fixation (OTG-SESS-003)](4.7.3_Testing_for_Session_Fixation_OTG-SESS-003.md)

[4.7.4 Testing for Exposed Session Variables (OTG-SESS-004)](4.7.4_Testing_for_Exposed_Session_Variables_OTG-SESS-004.md)

[4.7.5 Testing for Cross Site Request Forgery (CSRF) (OTG-SESS-005)](4.7.5_Testing_for_CSRF_OTG-SESS-005.md)

[4.7.6 Testing for Logout Functionality (OTG-SESS-006)](4.7.6_Testing_for_Logout_Functionality_OTG-SESS-006.md)

[4.7.7 Test Session Timeout (OTG-SESS-007)](4.7.7_Test_Session_Timeout_OTG-SESS-007.md)

[4.7.8 Testing for Session Puzzling (OTG-SESS-008)](4.7.8_Testing_for_Session_Puzzling_OTG-SESS-008.md)
