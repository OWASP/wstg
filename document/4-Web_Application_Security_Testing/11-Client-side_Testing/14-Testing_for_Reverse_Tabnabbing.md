# Testing for Reverse Tabnabbing

|ID          |
|------------|
|WSTG-CLNT-14|

## Summary

Reverse Tabnabbing is an attack which can be used to redirect users to phishing pages. This usually becomes possible due to the `target` attribute in links being set to `_blank` which causes the links to be opened in a new tab. When such a link does not use the attribute `rel='noopener noreferrer'`, clicking it opens a new tab and causes the original page to be redirected to a domain controlled by the attacker.

Since the user was on the original domain when the new tap opened, it is less likely for them to notice that the page has changed, especially if the phishing page is identical to the original domain. Any credentials entered on the attacker controlled domain will thus end up in the attacker's possession.

Links opened via the window.open javascript function is also vulnerable to this attack.

### Example

Imagine a web application where users are allowed to insert a URL in their profile. If the application is vulnerable to reverse tabnabbing, a malicious user will be able to provide a link to a page that has the following code:

```
<html>
 <body>
  <script>
    window.opener.location = "https://evil.com";
  </script>
<b>Error loading...</b>
 </body>
</html>
```

Clicking on the link will open up a new tab while the original tab will redirect to evil.com. Suppose evil.com looks similar to the vulnerable web application, the user is less likely to notice the change and is more likely to trustingly share sensitive information as and when required on the page.

## How to Test

+ Check the source code of the application homepage/dashboard to see if links with `target="_blank"` is using the `noopener` and `noreferrer` keywords in the `rel` attribute. If not, it is likely that the application is vulnerable to reverse tabnabbing.
+ Check for areas where an attacker can insert links, i.e. control the `href` argument of an `<a` tag. Try to insert a link to a page which has the source code given in the above example, and see if the original domain redirects. This test can be done in IE if other browsers don't work.

## Remediation

It would be recommended to avoid using the `target` attribute. If it cannot be avoided, make sure to add the attribute `rel='noopener noreferrer'` to it.

## References

+ [Reverse Tabnabbing - OWASP](https://owasp.org/www-community/attacks/Reverse_Tabnabbing)
+ [The target="_blank" vulnerability by example](https://dev.to/ben/the-targetblank-vulnerability-by-example)
+ [About rel=noopener](https://mathiasbynens.github.io/rel-noopener/)
+ [Target=”_blank” — the most underestimated vulnerability ever](https://medium.com/@jitbit/target-blank-the-most-underestimated-vulnerability-ever-96e328301f4c)
