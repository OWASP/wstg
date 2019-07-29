Testing for Horizontal Bypassing Authorization Schema (OTG-AUTHZ-002)

Summary
--------
This kind of test focuses on verifying how the Horizontal authorization schema has been implemented for each role or privilege to get access rights to data and resources of other users with the same role or privilege.
Horizontal authorization bypass may occur when an attacker gets access to more resources or data than they are normally allowed. Such elevation or changes should be prevented by the application. 
For every function, specific role and request that the application executes during the post-authentication phase, it is necessary to verify:
-	Is it possible to access resources that should be accessible to a user that holds a different identity with the same role or privilege?
-	Is it possible to operate functions on resources that should be accessible to a user that holds a different identity?

How to test
------------
For each role:
1.	Register/generate two users with the same role.
2.	Generate and keep two different session tokens by authenticating the application (one session token for each user).
3.	For every request, change the relevant parameters and the session token from token one to token two and diagnose the responses for each token.
4.	An application will be considered vulnerable if the responses are the same, contain same private data or indicate successful operation on other users resource or data.

For example, suppose that the 'viewCCpincode.jsp' function is part of every account menu of the application with the same role, and it is possible to access it by requesting the following URL:
https://www.example.com/account/viewCCpincode.jsp 

Then, the following HTTP request is generated when calling the viewCCpincode function:
POST /account/viewCCpincode.jsp HTTP/1.1
Host: www.example.com
[other HTTP headers]
Cookie: SessionID=xh6Tm2DfgRp01AZ03

Idpincode=user1

Valid and legitimate response:
HTTP1.1 200 OK
[other HTTP headers]

{“pincode”:8432}
The attacker may try and execute that request with the same Idpincode parameter:
POST /account/viewCCpincode.jsp HTTP/1.1
Host: www.example.com
[other HTTP headers]
Cookie: SessionID=GbcvA1_ATTACKER_SESSION_6fhTscd

Idpincode=user1
If the response of the attacker’s request contains the same data (“pincode”:8432) the application is vulnerable.

Tools
-------
Burp extension: Authorize.
References
OWASP Application Security Verification Standard 3.0.1, V4.1, 4.4, 4.9, 4.16.
