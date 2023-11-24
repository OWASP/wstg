# Test Path Confusion

|ID          |
|------------|
|WSTG-CONF-13|

## Summary

Proper configuration of application paths is important because, if paths are not configured correctly, they allow an attacker to exploit other vulnerabilities at a later stage using this misconfiguration.

For example, if the routes are not configured correctly and the target also uses a CDN, the attacker can use this misconfiguration to execute web cache deception attacks.

As a result, to prevent other attacks, this configuration should be evaluated by the tester.

## Test Objectives

- Make sure application paths are configured correctly.

## How To Test

### Black-Box Testing

In a black-box testing scenario, the tester should replace all the existing paths with paths that do not exist, and then examine the behavior and status code of the target.

For example, there is a path in the application that is a dashboard and shows the amount of the user's account balance (money, game credits, etc).

Assume the path is `https://example.com/user/dashboard`, the tester should test the different modes that the developer may have considered for this path. For Web Cache Deception vulnerabilities the analyst should consider a path such as `https:// example.com/user/dashboard/non.js` if dashboard information is visible, and the target uses a CDN (or other web cache), then Web Cache Deception attacks are likely applicable.

### White-Box Testing

Examine the application routing configuration, Most of the time, developers use regular expressions in application routing.

In this example, in the `urls.py` file of a Django framework application, we see an example of Path Confusion. The developer did not use the correct regular expression resulting in a vulnerability:

```python
    from django.urls import re_path
    from . import views

    urlpatterns = [

        re_path(r'.*^dashboard', views.path_confusion ,name = 'index'),

    ]
```

If the path `https://example.com/dashboard/none.js` is also opened by the user in the browser, the user dashboard information can be displayed, and if the target uses a CDN or web cache, a Web Cache Deception attack can be implemented.

## Tools

- [Zed Attack Proxy](https://www.zaproxy.org)
- [Burp Suite](https://portswigger.net/burp)

## Remediation

- Refrain from classify/handling cached based on file extension or path (leverage content-type).
- Ensure the caching mechanism(s) adhere to cache-control headers specified by your application.
- Implement RFC compliant File Not Found handling and redirects.

## References

- [Bypassing Web Cache Poisoning Countermeasures](https://portswigger.net/research/bypassing-web-cache-poisoning-countermeasures)
- [Path confusion: Web cache deception threatens user information online](https://portswigger.net/daily-swig/path-confusion-web-cache-deception-threatens-user-information-online)
- [Web Cache Deception Attack](https://omergil.blogspot.com/2017/02/web-cache-deception-attack.html)
