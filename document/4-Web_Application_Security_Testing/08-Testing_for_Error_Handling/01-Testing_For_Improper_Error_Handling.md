# Testing for Improper Error Handling

|ID          |
|------------|
|WSTG-ERRH-01|

## Summary

All types of applications (web apps, web servers, databases, etc.) will generate errors for various reasons. Developers often ignore handling these errors, or push away the idea that a user will ever try to trigger an error purposefully (*e.g.* sending a string where an integer is expected). When the developer only consider the happy path, they forget all other possible user-input the code can receive but can't handle.

Errors sometimes rise as:

- stack traces,
- network timeouts,
- input mismatch,
- and memory dumps.

Improper error handling can allow attackers to:

- Understand the APIs being used internally.
- Map the various services integrating with each other by gaining insight on internal systems and frameworks used, which opens up doors to attack chaining.
- Gather the versions and types of applications being used.
- DoS the system by forcing the system into a deadlock or an unhandled exception that sends a panic signal to the engine running it.
- Controls bypass where a certain exception is not restricted by the logic set around the happy path.

## Test Objectives

- Identify existing error output.
- Analyze the different output returned.

## How to Test

Errors are usually seen as benign as they provide diagnostics data and messages that could help the user understand the problem at hand, or for the developer to debug that error.

By trying to send unexpected data, or forcing the system into certain edge cases and scenarios, the system or application will most of the times give out a bit on what's happening internally, unless the developers turned off all possible errors and return a certain custom message.

### Web Servers

All web apps run on a web server, whether it was an integrated one or a full fledged one. Web apps must handle and parse HTTP requests, and for that a web server is always part of the stack. Some of the most famous web servers are NGINX, Apache, and IIS.

Web servers have known error messages and formats. If one is not familiar with how they look, searching online for them would provide examples. Another way would be to look into their documentation, or simply setup a server locally and discover the errors by going through the pages that the web server uses.

In order to trigger error messages, a tester must:

- Search for random files and folders that will not be found (404s).
- Try to request folders that exist and see the server behavior (403s, blank page, or directory listing).
- Try sending a request that breaks the [HTTP RFC](https://tools.ietf.org/html/rfc7231). One example would be to send a very large path, break the headers format, or change the HTTP version.
    - Even if errors are handled on the application level, breaking the HTTP RFC may make the integrated web server show itself since it has to handle the request, and developers forget to override these errors.

### Applications

Applications are the most susceptible to let out a wide variety of error messages, which include: stack traces, memory dumps, mishandled exceptions, and generic errors. This happens due to the fact that applications are custom built most of the time and the developers need to observe and handle all possible error cases (or have a global error catching mechanism), and these errors can appear from integrations with other services.

In order to make an application throw these errors, a tester must:

1. Identify possible input points where the application is expecting data.
2. Analyse the expected input type (strings, integers, JSON, XML, etc.).
3. Fuzz every input point based on the previous steps to have a more focused test scenario.
   - Fuzzing every input with all possible injections is not the best solution unless you have unlimited testing time and the application can handle that much input.
   - If fuzzing isn't an option, handpick viable inputs that have the highest chance to break a certain parser (*e.g.* a closing bracket for a JSON body, a large text where only a couple of characters are expected, CLRF injection with parameters that might be parsed by servers and input validation controls, special characters that aren't applicable for file names, etc.).
   - Fuzzing with jargon data should be ran for every type as sometimes the interpreters will break outside of the developer's exception handling.
4. Understand the service responding with the error message and try to make a more refined fuzz list to bring out more information or error details from that service (it could be a database, a standalone service, etc.).

Error messages are sometimes the main weakness in mapping out systems, especially under a microservice architecture. If services are not properly set to handle errors in a generic and uniform manner, error messages would let a tester identify which service handles which requests, and allows for a more focused attack per service.

> The tester needs to keep a vigilant eye for the response type. Sometimes errors are returned as success with an error body, hide the error in a 302, or simply by having a custom way of representing that error.

## Remediation

For remediation, check out the [Proactive Controls C10](https://owasp.org/www-project-proactive-controls/v3/en/c10-errors-exceptions) and the [Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html).

## Playgrounds

- [Juice Shop - Error Handling](https://bkimminich.gitbooks.io/pwning-owasp-juice-shop/content/part2/security-misconfiguration.html#provoke-an-error-that-is-neither-very-gracefully-nor-consistently-handled)

## References

- [WSTG: Appendix C - Fuzz Vectors](../../6-Appendix/C-Fuzz_Vectors.md)
- [Proactive Controls C10: Handle All Errors and Exceptions](https://owasp.org/www-project-proactive-controls/v3/en/c10-errors-exceptions)
- [ASVS v4.1 v7.4: Error handling](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x15-V7-Error-Logging.md#v74-error-handling)
- [CWE 728 - Improper Error Handling](https://cwe.mitre.org/data/definitions/728.html)
- [Cheat Sheet Series: Error Handling](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)
  