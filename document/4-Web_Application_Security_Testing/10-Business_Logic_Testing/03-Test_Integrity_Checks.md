# Test Integrity Checks

|ID          |
|------------|
|WSTG-BUSL-03|

## Summary

Many applications are designed to display different fields depending on the user of situation by leaving some inputs hidden. However, in many cases it is possible to submit values hidden field values to the server using a proxy. In these cases the server-side controls must be smart enough to perform relational or server-side edits to ensure that the proper data is allowed to the server based on user and application specific business logic.

Additionally, the application must not depend on non-editable controls, drop-down menus or hidden fields for business logic processing because these fields remain non-editable only in the context of the browsers. Users may be able to edit their values using proxy editor tools and try to manipulate business logic. If the application exposes values related to business rules like quantity, etc. as non-editable fields it must maintain a copy on the server-side and use the same for business logic processing. Finally, aside application/system data, log systems must be secured to prevent read, writing and updating.

Business logic integrity check vulnerabilities is unique in that these misuse cases are application specific and if users are able to make changes one should only be able to write or update/edit specific artifacts at specific times per the business process logic.

The application must be smart enough to check for relational edits and not allow users to submit information directly to the server that is not valid, trusted because it came from a non-editable controls or the user is not authorized to submit through the front end. Additionally, system artifacts such as logs must be "protected" from unauthorized read, writing and removal.

### Example 1

Imagine an ASP.NET application GUI application that only allows the admin user to change the password for other users in the system. The admin user will see the username and password fields to enter a username and password while other users will not see either field. However, if a non admin user submits information in the username and password field through a proxy they may be able to "trick" the server into believing that the request has come from an admin user and change password of other users.

### Example 2

Most web applications have dropdown lists making it easy for the user to quickly select their state, month of birth, etc. Suppose a Project Management application allowed users to login and depending on their privileges presented them with a drop down list of projects they have access to. What happens if an attacker finds the name of another project that they should not have access to and submits the information via a proxy. Will the application give access to the project? They should not have access even though they skipped an authorization business logic check.

### Example 3

Suppose the motor vehicle administration system required an employee initially verify each citizens documentation and information when they issue an identification or driver's license. At this point the business process has created data with a high level of integrity as the integrity of submitted data is checked by the application. Now suppose the application is moved to the Internet so employees can log on for full service or citizens can log on for a reduced self-service application to update certain information. At this point an attacker may be able to use an intercepting proxy to add or update data that they should not have access to and they could destroy the integrity of the data by stating that the citizen was not married but supplying data for a spouse’s name. This type of inserting or updating of unverified data destroys the data integrity and might have been prevented if the business process logic was followed.

### Example 4

Many systems include logging for auditing and troubleshooting purposes. But, how good/valid is the information in these logs? Can they be manipulated by attackers either intentionally or accidentally having their integrity destroyed?

## Test Objectives

- Review the project documentation for components of the system that move, store, or handle data.
- Determine what type of data is logically acceptable by the component and what types the system should guard against.
- Determine who should be allowed to modify or read that data in each component.
- Attempt to insert, update, or delete data values used by each component that should not be allowed per the business logic workflow.

## How to Test

### Specific Testing Method 1

- Using a proxy capture HTTP traffic looking for hidden fields.
- If a hidden field is found see how these fields compare with the GUI application and start interrogating this value through the proxy by submitting different data values trying to circumvent the business process and manipulate values you were not intended to have access to.

### Specific Testing Method 2

- Using a proxy capture HTTP traffic looking for a place to insert information into areas of the application that are non-editable.
- If it is found see how these fields compare with the GUI application and start interrogating this value through the proxy by submitting different data values trying to circumvent the business process and manipulate values you were not intended to have access to.

### Specific Testing Method 3

- List components of the application or system that could be impacted, for example logs or databases.
- For each component identified, try to read, edit or remove its information. For example log files should be identified and Testers should try to manipulate the data/information being collected.

## Related Test Cases

All [Input Validation](../07-Input_Validation_Testing/README.md) test cases.

## Remediation

The application should follow strict access controls on how data and artifacts can be modified and read, and through trusted channels that ensure the integrity of the data. Proper logging should be set in place to review and ensure that no unauthorized access or modification is happening.

## Tools

- Various system/application tools such as editors and file manipulation tools.
- [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org)
- [Burp Suite](https://portswigger.net/burp)

## References

- [Implementing Referential Integrity and Shared Business Logic in a RDB](http://www.agiledata.org/essays/referentialIntegrity.html)
- [On Rules and Integrity Constraints in Database Systems](https://www.comp.nus.edu.sg/~lingtw/papers/IST92.teopk.pdf)
- [Use referential integrity to enforce basic business rules in Oracle](https://www.techrepublic.com/article/use-referential-integrity-to-enforce-basic-business-rules-in-oracle/)
- [Maximizing Business Logic Reuse with Reactive Logic](https://dzone.com/articles/maximizing-business-logic)
