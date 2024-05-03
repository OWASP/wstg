# Testing for Clickjacking

|ID          |
|------------|
|WSTG-CLNT-09|

## Summary

Clickjacking, a subset of UI redressing, is a malicious technique whereby a web user is deceived into interacting (in most cases by clicking) with something other than what the user believes they are interacting with. This type of attack, either alone or in conjunction with other attacks, could potentially send unauthorized commands or reveal confidential information while the victim is interacting with seemingly-harmless web pages. The term clickjacking was coined by Jeremiah Grossman and Robert Hansen in 2008.

A clickjacking attack uses seemingly-harmless features of HTML and JavaScript to force the victim to perform undesired actions, such as clicking an invisible button that performs an unintended operation. This is a client-side security issue that affects a variety of browsers and platforms.

To carry out this attack, an attacker creates a seemingly-harmless web page that loads the target application through the use of an inline frame (concealed with CSS code). Once this is done, an attacker may induce the victim to interact with the web page by other means (through, for example, social engineering). Like other attacks, a common prerequisite is that the victim is authenticated against the attacker’s target application.

![Clickjacking illustration](images/Clickjacking_description.png)\
*Figure 4.11.9-1: Clickjacking inline frame illustration*

The victim surfs the attacker's web page with the intention of interacting with the visible user interface, but is inadvertently performing actions on the hidden web page. Using the hidden page, an attacker can deceive users into performing actions they never intended to perform through the positioning of the hidden elements in the web page.

![Masked inline frame illustration](images/Masked_iframe.png)\
*Figure 4.11.9-2: Masked inline frame illustration*

The power of this method is that the actions performed by the victim are originated from the hidden but authentic target web page. Consequently, some of the anti-CSRF protections deployed by the developers to protect the web page from CSRF attacks could be bypassed.

## Test Objectives

- Assess application vulnerability to clickjacking attacks.

## How to Test

As mentioned above, this type of attack is often designed to allow an attacker to induce users’ actions on the target site, even if anti-CSRF tokens are being used.

### Load target web page on a HTML interpreter usign HTML iframe tag

Sites that do not protected against frame busting are vulnerable to clickjacking attack. If the `http://www.target.site` web page is successfully loaded into a frame, then the site is vulnerable to Clickjacking. An example of HTML code to create this testing web page is displayed in the following snippet:

    ```html
    <html>
        <head>
            <title>Clickjack test web page</title>
        </head>
        <body>
            <iframe src="http://www.target.site" width="400" height="400"></iframe>
        </body>
    </html>
    ```

### Test application against disabled JavaScript

Since these types of client-side protections relies on JavaScript frame busting code, if the victim has JavaScript disabled or it is possible for an attacker to disable JavaScript code, the web page will not have any protection mechanism against clickjacking.

There are few deactivation techniques that can be used with frames. More in depth techniques can be found on the [Clickjacking Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html).

### Sandbox attribute

With HTML5 a new attribute called "sandbox" is availanle. It enables a set of restrictions on content loaded into the iframe. At this moment this attribute is only compatible with Chrome and Safari.

Example:

```html
<iframe src="http://example.org" sandbox></iframe>
```

### Test application on compatibility and acessibility mode

Mobile versions of the web page are usually smaller and faster than the desktop ones, and they have to be less complex than the main application. Mobile variants have often less protection. However, an attacker can fake the real origin given by a web browser, and a non-mobile victim may be able to visit an application made for mobile users. This scenario could allow the attacker to exploit a mobile version of the web page.
Site running on acessibility mode should also be tested against clickjacking, because site framming could be affected.

#### Redefining Location

For several browsers the `document.location` variable is an immutable attribute. However, for some version of Internet Explorer and Safari, it is possible to redefine this attribute. This fact can be exploited to evade frame busting code.

- **Redefining location in IE7 and IE8**: it is possible to redefine `location` as it is illustrated in the following example. By defining `location` as a variable, any code that tries to read or to navigate by assigning `top.location` will fail due to a security violation and so the frame busting code is suspended.

Example:

```html
<script>
    var location = "xyz";
</script>
<iframe src="http://example.org"></iframe>
```

- **Redefining location in Safari 4.0.4**: To bust frame busting code with `top.location` it is possible to bind `location` to a function via `defineSetter` (through window), so that an attempt to read or navigate to the `top.location` will fail.

Example:

```html
<script>
    window.defineSetter("location" , function(){});
</script>
<iframe src="http://example.org"></iframe>
```

Some frame busting action try to break frame by assigning a value to the `parent.location` attribute in the "counter-action" statement.
Such actions are, for example:

- `self.parent.location` = `document.location`
- `parent.location.href` = `self.location`
- `parent.location` = `self.location`

This method works well until the target web page is framed by a single page. However, if the attacker encloses the target web page in one frame which is nested in another one (a double frame), then trying to access to `parent.location` becomes a security violation in all popular browsers, due to the descendant frame navigation policy. This security violation disables the counter-action navigation.

### Server-side Protection: Using frame-ancestors directive of Content Security Policy (CSP)

The HTTP Content-Security-Policy (CSP) response header allows web page administrators to control resources the user agent is allowed to load for a given web page. The `frame-ancestors` directive in the HTTP CSP specifies the acceptable parents that may embed a web page using the `<frame>`, `<iframe>`, `<object>`, `<embed>`, or `<applet>` tags.

#### Testing Content Security Policy Response Header

- Using a browser, open developer tools and access the target web page. Navigate to the Network tab.
- Look for the request that loads the web page. It should have the same domain as the web page - usually be the first item on the Network tab.
- Once you click on the file, more information will come up. Look for a 200 OK response code.
- Scroll down to the Response Header Section. Content-Security-Policy section indicates level of protecting adopted.

Alternatively view the web page source to find Content-Security-Policy in a meta tag.

WSTG has a detailed information on [Test for Content Security Policy](../02-Configuration_and_Deployment_Management_Testing/12-Test_for_Content_Security_Policy.md)

##### Proxies

Web proxies are known for adding and stripping headers. In the case in which a web proxy strips the `X-FRAME-OPTIONS` header then the site loses its framing protection.

##### Mobile web page Version

Also in this case, since the `X-FRAME-OPTIONS` has to be implemented in every web page of the web page, the developers may have not protected the mobile version of the web page.

### Remediation

- For measures to prevent Clickjacking, see the [Clickjacking Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html).
- For interactive labs on Clickjacking visit [Port Swigger Web Page](https://portswigger.net/web-security/clickjacking)
- For additional resources on ClickJacking visit the [Owasp community](https://owasp.org/www-community/attacks/Clickjacking)

## References

- [OWASP Clickjacking](https://owasp.org/www-community/attacks/Clickjacking)
- [Wikipedia Clickjacking](https://en.wikipedia.org/wiki/Clickjacking)
- [Gustav Rydstedt, Elie Bursztein, Dan Boneh, and Collin Jackson: "Busting Frame Busting: a Study of Clickjacking Vulnerabilities on Popular Sites"](https://seclab.stanford.edu/websec/framebusting/framebust.pdf)
