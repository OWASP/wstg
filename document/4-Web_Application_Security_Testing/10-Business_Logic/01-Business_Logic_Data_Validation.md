# Business Logic Data Validation

|ID          |
|------------|
|WSTG-BUSL-01|

## Summary

The application must ensure that only logically valid data can be entered at the frontend as well as directly to the server-side of an application or system. Only verifying data on the client/frontend may leave applications vulnerable to server injections through proxies or at handoffs with other systems. This is different from simply performing Boundary Value Analysis (BVA) in that it is more difficult and in most cases cannot be simply verified at the entry point, but usually requires checking some other system.

For example: An application may ask for your Social Security Number. In BVA, the application should check formats and semantics (is the value 9 digits long, not negative, and not all 0's) for the data entered, but there are logic considerations also. SSNs are grouped and categorized. Is this person on a death file? Are they from a certain part of the country?

Vulnerabilities related to business data validation is unique in that they are application specific and different from the vulnerabilities related to forging requests in that they are more concerned about logical data as opposed to simply breaking the business logic workflow.

The frontend and the backend of the application should be verifying and validating that the data it has, is using, and is passing along is logically valid. Even if the user provides valid data to an application the business logic may make the application behave differently depending on data or circumstances.

### Example 1

Suppose you manage a multi-tiered e-commerce site that allows users to order carpet. The user selects their carpet, enters the size, makes the payment, and the frontend application has verified that all entered information is correct and valid for contact information, size, make and color of the carpet. But, the business logic in the background has two paths, if the carpet is in stock it is directly shipped from your warehouse, but if it is out of stock in your warehouse a call is made to a partner’s system and if they have it in-stock they will ship the order from their warehouse and reimbursed by them.

What happens if an attacker is able to continue a valid in-stock transaction and send it as out-of-stock to your partner? What happens if an attacker is able to get in the middle and send messages to the partner warehouse ordering carpet without payment?

### Example 2

Many credit card systems are now downloading account balances nightly so the customers can check out more quickly for amounts under a certain value. The inverse is also true. If I pay my credit card off in the morning I may not be able to use the available credit in the evening. Another example may be if I use my credit card at multiple locations very quickly it may be possible to exceed my limit if the systems are basing decisions on last night’s data.

### Example 3

**[Distributed Denial of Dollar (DDo$)](https://www.zdnet.com/article/pirate-bay-defendant-urges-ddo-attack-on-lawyer/):**
This was a campaign that was proposed by the founder of the site "The Pirate Bay" against the law firm who brought prosecutions against "The Pirate Bay". The goal was to take advantage of errors in the design of business features and in the process of credit transfer validation.

This attack was performed by sending very small amounts of money of 1 SEK ($0.13 USD) to the law firm.
The bank account to which the payments were directed had only 1000 free transfers, after which any transfers have a surcharge for the account holder (2 SEK). After the first thousand internet transactions every 1 SEK donation to the law firm will actually end up costing it 1 SEK instead.

### Example 4

A profile page lets users pick an avatar. The frontend always sends the image as a base64 `data:` URI, so the developers never validate what the `avatar` parameter contains. An attacker intercepts the request and replaces the value with `http://attacker.example/pixel.png`. The application accepts it and, later, a server-side job or an administrator's browser fetches that URL. The request reaches the attacker, who learns that the input was never validated and may use it to reach internal hosts or to track other users.

### Example 5

A product review form offers a rating from 1 to 5 stars through a set of radio buttons. If the backend only checks that the value is a number, `rating=-100` or `rating=99999` is stored and skews the average score, and a value such as `rating=NaN` may break the pages that display it.

## Test Objectives

- Identify data injection points.
- Validate that all checks are occurring on the backend and can't be bypassed.
- Attempt to break the format of the expected data and analyze how the application is handling it.
- Determine whether parameters that the frontend restricts (type, range, set of allowed values, or relationship to other fields) are restricted again on the server.

## How to Test

### Generic Test Method

- Review the project documentation and use exploratory testing looking for data entry points or hand off points between systems or software.
- Once found try to insert logically invalid data into the application/system.

Specific Testing Method:

- Perform frontend GUI Functional Valid testing on the application to ensure that the only "valid" values are accepted.
- Using an intercepting proxy observe the HTTP POST/GET looking for places that variables such as cost and quantity are passed. Specifically, look for "hand-offs" between application/systems that may be possible injection or tamper points.
- Once variables are found start interrogating the field with logically "invalid" data, such as social security numbers or unique identifiers that do not exist or that do not fit the business logic. This testing verifies that the server functions properly and does not accept logically invalid data.

### Parameter-Based Test Cases

For every parameter observed in the previous steps, replay the request with a modified value and compare the response, the stored data, and any later behavior (emails, background jobs, other users' views) with those of the valid request. The aim is to find values that the frontend would never send but that the server accepts. Useful variations are:

- **Range and sign:** values below the minimum or above the maximum offered by the interface, zero, negative numbers, and very large numbers (for example a rating of `-1` or `1000`, a quantity of `0`, or a transfer of `-50`).
- **Allowed set:** values that are not in the list the interface offers, such as a role, country, plan, status, or currency that is not in the drop-down, or a different valid value that belongs to another user or tenant.
- **Type and format:** a different data type than expected (string instead of number, array or object instead of string, `null`, an empty value, `true` instead of `1`), or the same field with a different format (a URL where the application expects a `data:` URI or a filename, a date in another format, or Unicode digits).
- **Length and encoding:** empty values, values longer than the length enforced by the frontend, and values containing characters that the interface filters out.
- **Relationships between fields:** values that are individually valid but inconsistent together, for example an end date before a start date, a discount that is larger than the price, or a shipping country that does not match the payment country.
- **Missing and additional parameters:** remove parameters that look mandatory and add parameters the interface never sends (see [Mass Assignment](../07-Injection/20-Mass_Assignment.md)), and repeat a parameter with different values (see [HTTP Parameter Pollution](../07-Injection/04-HTTP_Parameter_Pollution.md)).
- **Hand-off values:** values that are later passed to another system, such as an email address, a URL, or a file path (see [Server-Side Request Forgery](../07-Injection/19-Server-Side_Request_Forgery.md)). Use a unique value that you control, so that you can detect when and where it is used, including by a delayed or out-of-band request.

Record which of the variations were accepted, because the impact depends on how the application uses the value afterwards and not only on whether it was rejected.

## Related Test Cases

- All [Injection Testing](../07-Injection/README.md) test cases.
- [HTTP Parameter Pollution](../07-Injection/04-HTTP_Parameter_Pollution.md).
- [Mass Assignment](../07-Injection/20-Mass_Assignment.md).
- [Server-Side Request Forgery](../07-Injection/19-Server-Side_Request_Forgery.md).
- [Payment Functionality](10-Payment_Functionality.md).
- [Account Enumeration and Guessable User Account](../03-Identity_Management/04-Account_Enumeration_and_Guessable_User_Account.md).
- [Bypassing Session Management Schema](../06-Session_Management/01-Session_Management_Schema.md).
- [Exposed Session Variables](../06-Session_Management/04-Exposed_Session_Variables.md).

## Remediation

The application/system must ensure that only "logically valid" data is accepted at all input and hand off points of the application or system and data is not simply trusted once it has entered the system.

- Validate every parameter on the server, even when the frontend restricts it. Check the type, the range, the length, the format, and membership in the set of allowed values (preferably with an allowlist).
- Validate relationships between fields and between the value and the state of the user, the account, or the order, and not only each value alone.
- Reject unexpected or unknown parameters instead of silently using or ignoring them.
- Treat data received from other systems with the same suspicion as data received from users.

## Tools

- [Zed Attack Proxy (ZAP)](https://www.zaproxy.org)
- [Burp Suite](https://portswigger.net/burp)

## References

- [OWASP Proactive Controls (C5) - Validate All Inputs](https://owasp.org/www-project-proactive-controls/v3/en/c5-validate-inputs)
- [OWASP Cheat Sheet Series - Input_Validation_Cheat_Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
