# 4.6 Authorization Testing

Authorization is the concept of allowing access to resources only to those permitted to use them. Testing for Authorization means understanding how the authorization process works, and using that information to circumvent the authorization mechanism.

Authorization is a process that comes after a successful authentication, so the tester will verify this point after he holds valid credentials, associated with a well-defined set of roles and privileges. During this kind of assessment, it should be verified if it is possible to bypass the authorization schema, find a path traversal vulnerability, or find ways to escalate the privileges assigned to the tester.

[4.6.1 Testing Directory Traversal/File Include](4.6.1_Testing_Directory_Traversal_File_Include.md)

[4.6.2 Testing for bypassing authorization schema](4.6.2_Testing_for_Bypassing_Authorization_Schema.md)

[4.6.3 Testing for Privilege Escalation](4.6.3_Testing_for_Privilege_Escalation.md)

[4.6.4 Testing for Insecure Direct Object References](4.6.4_Testing_for_Insecure_Direct_Object_References.md)
