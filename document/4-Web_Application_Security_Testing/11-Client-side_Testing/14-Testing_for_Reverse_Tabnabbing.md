# Testing for Reverse Tabnabbing

|ID          |
|------------|
|WSTG-CLNT-14|

## Summary

[Reverse Tabnabbing](https://owasp.org/www-community/attacks/Reverse_Tabnabbing) is an attack which can be used to redirect users to phishing pages. This usually becomes possible due to the `target` attribute of the `<a>` tag being set to `_blank` which causes the link to be opened in a new tab. When the attribute `rel='noopener noreferrer'` is not used in the same `<a>` tag, the newly opened page can influence the original page and redirect it to a domain controlled by the attacker.

Since the user was on the original domain when the new tab opened, they are less likely to notice that the page has changed, especially if the phishing page is identical to the original domain. Any credentials entered on the attacker-controlled domain will thus end up in the attacker's possession.

Links opened via the `window.open` JavaScript function are also vulnerable to this attack.

_NOTE: This is a legacy issue that does not affect [modern browsers](https://caniuse.com/mdn-html_elements_a_implicit_noopener). Older versions of popular browsers (For example, versions prior to Google Chrome 88) as well as Internet Explorer are vulnerable to this attack._

### Example

Imagine a web application where users are allowed to insert a URL in their profile. If the application is vulnerable to reverse tabnabbing, a malicious user will be able to provide a link to a page that has the following code:

```html
<html>
 <body>
  <script>
    window.opener.location = "https://example.org";
  </script>
<b>Error loading...</b>
 </body>
</html>
```

Clicking on the link will open up a new tab while the original tab will redirect to "example.org". Suppose "example.org" looks similar to the vulnerable web application, the user is less likely to notice the change and is more likely to enter sensitive information on the page.

## How to Test

- Check the HTML source of the application to see if links with `target="_blank"` are using the `noopener` and `noreferrer` keywords in the `rel` attribute. If not, it is likely that the application is vulnerable to reverse tabnabbing. Such a link becomes exploitable if it either points to a third-party site that has been compromised by the attacker, or if it is user-controlled.
- Check for areas where an attacker can insert links, i.e. control the `href` argument of an `<a>` tag. Try to insert a link to a page which has the source code given in the above example, and see if the original domain redirects. This test can be done in IE if other browsers don't work.

## Remediation

It is recommended to make sure that the `rel` HTML attribute is set with the `noreferrer` and `noopener` keywords for all links.

## References

- [Tabnabbing - HTML5 Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html#tabnabbing)
- [The target="_blank" vulnerability by example](https://dev.to/ben/the-targetblank-vulnerability-by-example)
- [About rel=noopener](https://mathiasbynens.github.io/rel-noopener/)
- [Target=”_blank” — the most underestimated vulnerability ever](https://medium.com/@jitbit/target-blank-the-most-underestimated-vulnerability-ever-96e328301f4c)
- [Reverse tabnabbing vulnerability affects IBM Business Automation Workflow and IBM Business Process Manager](https://www.ibm.com/support/pages/security-bulletin-reverse-tabnabbing-vulnerability-affects-ibm-business-automation-workflow-and-ibm-business-process-manager-bpm-cve-2020-4490-0)
