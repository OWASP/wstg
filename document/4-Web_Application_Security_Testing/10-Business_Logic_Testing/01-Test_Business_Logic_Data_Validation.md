# Test Business Logic Data Validation

|ID          |
|------------|
|WSTG-BUSL-01|

## Summary

The application must ensure that only logically valid data can be entered at the front end as well as directly to the server-side of an application of system. Only verifying data locally may leave applications vulnerable to server injections through proxies or at handoffs with other systems. This is different from simply performing Boundary Value Analysis (BVA) in that it is more difficult and in most cases cannot be simply verified at the entry point, but usually requires checking some other system.

For example: An application may ask for your Social Security Number. In BVA the application should check formats and semantics (is the value 9 digits long, not negative and not all 0's) for the data entered, but there are logic considerations also. SSNs are grouped and categorized. Is this person on a death file? Are they from a certain part of the country?

Vulnerabilities related to business data validation is unique in that they are application specific and different from the vulnerabilities related to forging requests in that they are more concerned about logical data as opposed to simply breaking the business logic workflow.

The front end and the back end of the application should be verifying and validating that the data it has, is using and is passing along is logically valid. Even if the user provides valid data to an application the business logic may make the application behave differently depending on data or circumstances.

### Example 1

Suppose you manage a multi-tiered e-commerce site that allows users to order carpet. The user selects their carpet, enters the size, makes the payment, and the front end application has verified that all entered information is correct and valid for contact information, size, make and color of the carpet. But, the business logic in the background has two paths, if the carpet is in stock it is directly shipped from your warehouse, but if it is out of stock in your warehouse a call is made to a partner’s system and if they have it in-stock they will ship the order from their warehouse and reimbursed by them. What happens if an attacker is able to continue a valid in-stock transaction and send it as out-of-stock to your partner? What happens if an attacker is able to get in the middle and send messages to the partner warehouse ordering carpet without payment?

### Example 2

Many credit card systems are now downloading account balances nightly so the customers can check out more quickly for amounts under a certain value. The inverse is also true. If I pay my credit card off in the morning I may not be able to use the available credit in the evening. Another example may be if I use my credit card at multiple locations very quickly it may be possible to exceed my limit if the systems are basing decisions on last night’s data.

### Example 3

**[Distributed Denial of Dollar (DDo$)](https://news.hitb.org/content/pirate-bay-proposes-distributed-denial-dollars-attack-ddo):**
This was a campaign that was proposed by the founder of the website "The Pirate Bay" against the law firm who brought prosecutions against "The Pirate Bay". The goal was to take advantage of errors in the design of business features and in the process of credit transfer validation.

This attack was performed by sending very small amounts of money of 1 SEK ($0.13 USD) to the law firm.
The bank account to which the payments were directed had only 1000 free transfers, after which any transfers have a surcharge for the account holder (2 SEK). After the first thousand Internet transactions every 1 SEK donation to the law firm will actually end up costing it 1 SEK instead.

## Test Objectives

- Identify data injection points.
- Validate that all checks are occurring on the back end and can't be bypassed.
- Attempt to break the format of the expected data and analyze how the application is handling it.

## How to Test

### Generic Test Method

- Review the project documentation and use exploratory testing looking for data entry points or hand off points between systems or software.
- Once found try to insert logically invalid data into the application/system.
Specific Testing Method:
- Perform front-end GUI Functional Valid testing on the application to ensure that the only "valid" values are accepted.
- Using an intercepting proxy observe the HTTP POST/GET looking for places that variables such as cost and quality are passed. Specifically, look for "hand-offs" between application/systems that may be possible injection or tamper points.
- Once variables are found start interrogating the field with logically "invalid" data, such as social security numbers or unique identifiers that do not exist or that do not fit the business logic. This testing verifies that the server functions properly and does not accept logically invalid data.

## Related Test Cases

- All [Input Validation](../07-Input_Validation_Testing/README.md) test cases.
- [Testing for Account Enumeration and Guessable User Account](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md).
- [Testing for Bypassing Session Management Schema](../06-Session_Management_Testing/01-Testing_for_Session_Management_Schema.md).
- [Testing for Exposed Session Variables](../06-Session_Management_Testing/04-Testing_for_Exposed_Session_Variables.md).

## Remediation

The application/system must ensure that only "logically valid" data is accepted at all input and hand off points of the application or system and data is not simply trusted once it has entered the system.

## Tools

- [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org)
- [Burp Suite](https://portswigger.net/burp)

## References

- [OWASP Proactive Controls (C5) - Validate All Inputs](https://owasp.org/www-project-proactive-controls/v3/en/c5-validate-inputs)
- [OWASP Cheatsheet Series - Input_Validation_Cheat_Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
