# Test Ability to Forge Requests

|ID          |
|------------|
|WSTG-BUSL-02|

## Summary

Forging requests is a method that attackers use to circumvent the front end GUI application to directly submit information for back end processing. The goal of the attacker is to send HTTP POST/GET requests through an intercepting proxy with data values that is not supported, guarded against or expected by the applications business logic. Some examples of forged requests include exploiting guessable or predictable parameters or expose "hidden" features and functionality such as enabling debugging or presenting special screens or windows that are very useful during development but may leak information or bypass the business logic.

Vulnerabilities related to the ability to forge requests is unique to each application and different from business logic data validation in that it s focus is on breaking the business logic workflow.

Applications should have logic checks in place to prevent the system from accepting forged requests that may allow attackers the opportunity to exploit the business logic, process, or flow of the application. Request forgery is nothing new; the attacker uses an intercepting proxy to send HTTP POST/GET requests to the application. Through request forgeries attackers may be able to circumvent the business logic or process by finding, predicting and manipulating parameters to make the application think a process or task has or has not taken place.

Also, forged requests may allow subvention of programmatic or business logic flow by invoking "hidden" features or functionality such as debugging initially used by developers and testers sometimes referred to as an ["Easter egg"](http://en.wikipedia.org/wiki/Easter_egg_(media)). "An Easter egg is an intentional inside joke, hidden message, or feature in a work such as a computer program, movie, book, or crossword. According to game designer Warren Robinett, the term was coined at Atari by personnel who were alerted to the presence of a secret message which had been hidden by Robinett in his already widely distributed game, Adventure. The name has been said to evoke the idea of a traditional Easter egg hunt."

### Example 1

Suppose an e-commerce theater site allows users to select their ticket, apply a onetime 10% Senior discount on the entire sale, view the subtotal and tender the sale. If an attacker is able to see through a proxy that the application has a hidden field (of 1 or 0) used by the business logic to determine if a discount has been taken or not. The attacker is then able to submit the 1 or "no discount has been taken" value multiple times to take advantage of the same discount multiple times.

### Example 2

Suppose an online video game pays out tokens for points scored for finding pirates treasure and pirates and for each level completed. These tokens can later be that can later be exchanged for prizes. Additionally each level's points have a multiplier value equal to the level. If an attacker was able to see through a proxy that the application has a hidden field used during development and testing to quickly get to the highest levels of the game they could quickly get to the highest levels and accumulate unearned points quickly.

Also, if an attacker was able to see through a proxy that the application has a hidden field used during development and testing to enabled a log that indicated where other online players, or hidden treasure were in relation to the attacker, they would then be able to quickly go to these locations and score points.

## Test Objectives

- Review the project documentation looking for guessable, predictable, or hidden functionality of fields.
- Insert logically valid data in order to bypass normal business logic workflow.

## How to Test

### Through Identifying Guessable Values

- Using an intercepting proxy observe the HTTP POST/GET looking for some indication that values are incrementing at a regular interval or are easily guessable.
- If it is found that some value is guessable this value may be changed and one may gain unexpected visibility.

### Through Identifying Hidden Options

- Using an intercepting proxy observe the HTTP POST/GET looking for some indication of hidden features such as debug that can be switched on or activated.
- If any are found try to guess and change these values to get a different application response or behavior.

## Related Test Cases

- [Testing for Exposed Session Variables](../06-Session_Management_Testing/04-Testing_for_Exposed_Session_Variables.md)
- [Testing for Cross Site Request Forgery (CSRF)](../06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery.md)
- [Testing for Account Enumeration and Guessable User Account](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md)

## Remediation

The application must be smart enough and designed with business logic that will prevent attackers from predicting and manipulating parameters to subvert programmatic or business logic flow, or exploiting hidden/undocumented functionality such as debugging.

## Tools

- [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org)
- [Burp Suite](https://portswigger.net/burp)

## References

- [Cross Site Request Forgery - Legitimizing Forged Requests](http://www.stan.gr/2012/11/cross-site-request-forgery-legitimazing.html)
- [Easter egg](https://en.wikipedia.org/wiki/Easter_egg_(media))
- [Top 10 Software Easter Eggs](https://lifehacker.com/371083/top-10-software-easter-eggs)
