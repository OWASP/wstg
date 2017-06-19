Testing for Vertical Bypassing Authorization Schema (OTG-AUTHZ-00X)

Summary
---------
It is common in modern enterprises to define system roles to manage users and authorization to system resources. The purpose of the system role is to distinguish among user levels and binding the wanted privileges to each role.
This kind of test focuses on verifying how the Vertical authorization schema has been implemented for each role to get access rights to data and resources of other users with different role or privilege.
Vertical authorization bypass may occur when an attacker gets access to more resources or data than they are normally allowed. Such elevation or changes should be prevented by the application. 
For every function, page, specific role and request that the application executes during the post-authentication phase, it is necessary to verify:
•	Is it possible to access resources that should be accessible only to higher role user?
•	Is it possible to operate functions on resources that should be operative only by a user that holds a higher or specific role identity?

How to test
--------------
For each role:
1.	For each role, register/generate a user.
2.	Generate and keep the session tokens by authenticating the application (one session token for each user).
3.	For every request, change the session token from the original token to another role session token and diagnose the responses for each token.
4.	An application will be considered vulnerable if the responses are the same, contain same private data or indicate successful operation on other users resource or data.

Example 1:
-----------
The following table illustrates the system role on banking site. Each role bind with specific permissions for the event menu functionality:
ROLE	Administrator	Manager	Staff	Customer
PERMISSION	Full Control	Modify, Add, Read	Read, Modify	Read Only
ADDITIONAL PERMISSION	Delete	Add	Modify	-
The application will be considered vulnerable if:
1.	Customer could operate administrator, manager or staff functions; 
2.	Staff user could operate manager or administrator functions; 
3.	Manager could operate administrator functions.
Suppose that the 'deleteEvent.jsp' function is part of the administrator account menu of the application, and it is possible to access it by requesting the following URL:
 https://www.example.com/account/deleteEvent.jsp 

Then, the following HTTP request is generated when calling the deleteEvent function:
POST /account/deleteEvent.jsp HTTP/1.1
Host: www.example.com
[other HTTP headers]
Cookie: SessionID=xh6Tm2DfgRp01AZ03

EventID=1000001

Valid and legitimate response:
HTTP1.1 200 OK
[other HTTP headers]

{“message”:”Event was deleted”}
The attacker may try and execute the same request:
POST /account/deleteEvent.jsp HTTP/1.1
Host: www.example.com
[other HTTP headers]
Cookie: SessionID=GbcvA1_CUSTOMER_ATTACKER_SESSION_6fhTscd

EventID=1000002
If the response of the attacker’s request contains the same data (“message”:”Event was deleted”) the application is vulnerable.

Example 2:
-----------
Suppose that the administrator menu is part of the administrator account. The application will be considered vulnerable if any other role rather than administrator could access the administrator menu.
Sometimes, developer perform authorization validation at the GUI level only, and leave the functions without authorization validation.

Tools
--------
Burp extension: Authorize.

References
------------
OWASP Application Security Verification Standard 3.0.1, V4.1, 4.4, 4.9, 4.16.
