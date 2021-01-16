# Self DOM-Based Cross-Site Scripting Testing

|ID          |
|------------|
|WSTG-INPV-20|

## Summary

A Self DOM-Based Cross-Site Scripting is a specific attack and needs prior knowledge of DOM-Based cross site scripting and successful social engineering. The term 'self' is a reference here to the fact, that the user needs to put the payload himself into the input field, and thus execute the vulnerability himself. The vulnerability is further specific, as the website's Content Security Policy (CSP) can block the execution of scripts.

We will use the term sink in the following. In computing, a sink, event sink or data sink is a class or function designed to receive incoming events from another object or function. Thus in order to find possible vulnerabilities we first need to identify the sinks of the application we want to test.

## How to Test

The process of testing for Self DOM-Based cross site scripting follows:

1. Look for vulnerable sinks, which allow user input.
2. Once a possible sink is identified, a payload can be inserted.
3. Check the error log in the browser's developer tools to see the outcome, and draw your conclusions.
4. Check if an attacker could convince a user to insert the payload with no extensive technical knowledge required.

### Example

This specific example is from this [hackerone ticket](https://hackerone.com/reports/406587).

In the example the following JavaScript function is executed on the website `https://example.com`.

```js
//Marketo Form Code
function strip(html) {
    var tmp = document.createElement("DIV");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
}

$('form').submit(function() {
    $('textarea').val(function() {
        return strip($(this).val());
    });
});
```

In the following the execution of the code will be explained and the implications for the security of the code are shown.

1. The `submit` event handler passes the current value of any `textarea` elements to the `strip` function.
2. This function creates a new `div` element and sets the `innerHTML` property to the provided value.
3. In the last step it then returns the `textContent` property of the resulting `div`.

 This type of code is typically used to remove HTML tags from a string, as the `textContent` property contains the String which was rendered by the browser when the HTML was parsed. This particular method is inherently insecure because it uses `innerHTML`. When user input is provided to the `innerHTML` property, it is parsed by the web browser and can therefore lead to the execution of malicious JavaScript.

The following payload can be used to test the vulnerability.`<img src=x onerror=alert(1) />`

The developer console would display two errors: One which indicates that `https://www.example.com/x` was requested and returned a 404 (due to the src attribute of the img tag). Another which reported a violation of the website's CSP.

This second error occurred because the browser attempts to execute the JavaScript code in the `onerror` attribute, but the website's CSP prevented the execution. Performing the same actions in a browser with CSP disabled allowed the JavaScript in the `onerror` attribute to execute.

An attacker could exploit this vulnerability by convincing a user to paste a malicious payload into the 'message' field of the contact form and then click the 'send message' button. This attack could be enhanced by convincing the user to use a browser version which does not support CSP.

## Remediation

In order to properly protect services from DOM based XSS, refer to the [DOM based XSS prevention cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html).

### References

- [OWASP - DOM-Based Cross Site Scripting](https://owasp.org/www-community/attacks/DOM_Based_XSS)
- [CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
