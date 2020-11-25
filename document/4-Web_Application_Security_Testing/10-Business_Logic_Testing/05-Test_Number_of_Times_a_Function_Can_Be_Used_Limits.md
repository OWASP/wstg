# Test Number of Times a Function Can Be Used Limits

|ID          |
|------------|
|WSTG-BUSL-05|

## Summary

Many of the problems that applications are solving require limits to the number of times a function can be used or action can be executed. Applications must be "smart enough" to not allow the user to exceed their limit on the use of these functions since in many cases each time the function is used the user may gain some type of benefit that must be accounted for to properly compensate the owner. For example: an eCommerce site may only allow a users apply a discount once per transaction, or some applications may be on a subscription plan and only allow users to download three complete documents monthly.

Vulnerabilities related to testing for the function limits are application specific and misuse cases must be created that strive to exercise parts of the application/functions/ or actions more than the allowable number of times.

Attackers may be able to circumvent the business logic and execute a function more times than "allowable" exploiting the application for personal gain.

### Example

Suppose an eCommerce site allows users to take advantage of any one of many discounts on their total purchase and then proceed to checkout and tendering. What happens of the attacker navigates back to the discounts page after taking and applying the one "allowable" discount? Can they take advantage of another discount? Can they take advantage of the same discount multiple times?

## Test Objectives

- Identify functions that must set limits to the times they can be called.
- Assess if there is a logical limit set on the functions and if it is properly validated.

## How to Test

- Review the project documentation and use exploratory testing looking for functions or features in the application or system that should not be executed more that a single time or specified number of times during the business logic workflow.
- For each of the functions and features found that should only be executed a single time or specified number of times during the business logic workflow, develop abuse/misuse cases that may allow a user to execute more than the allowable number of times. For example, can a user navigate back and forth through the pages multiple times executing a function that should only execute once? or can a user load and unload shopping carts allowing for additional discounts.

## Related Test Cases

- [Testing for Account Enumeration and Guessable User Account](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md)
- [Testing for Weak lock out mechanism](../04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism.md)

## Remediation

The application should set hard controls to prevent limit abuse. This can be achieved by setting a coupon to be no longer valid on the database level, to set a counter limit per user on the back end or database level, as all users should be identified through a session, whichever is better to the business requirement.

## References

- [InfoPath Forms Services business logic exceeded the maximum limit of operations Rule](http://mpwiki.viacode.com/default.aspx?g=posts&t=115678)
- [Gold Trading Was Temporarily Halted On The CME This Morning](https://www.businessinsider.com/gold-halted-on-cme-for-stop-logic-event-2013-10)
