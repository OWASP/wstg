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

In black box testing this issue, the tester should replace all the existing paths with the paths that do not exist, and then examine the behavior and status code of the evaluated program.

For example, there is a path in the application that is a dashboard and shows the amount of the user's account balance (money, game credits, etc).

In black-box testing of this topic, the tester must replace all existing paths with non-existent ones, and then examine the behavior and status code of the evaluated application. Example: There is a path in the application that is a dashboard and shows the amount of the user's balance if the path mentioned in this way is ```https://example.com/user/dashboard```, the tester should test the different modes that the developer may have considered for this path, for Web Cache Deception vulnerability if the tester of this path ```https:// example.com/user/dashboard/non.js``` Dashboard information is visible, and the target uses CDN, the Web Cache Deception attack is applicable.

### White-Box Testing

In the white box testing, examine the application routing file, Most of the time, developers use regular expression in application routing.

In this example, in the urls.py file in the Django framework, I will show you an example of Path Confusion that the developer did not use the correct regular expression and there is an incorrect configuration:

```text
    from django.urls import re_path
    from . import views

    urlpatterns = [

        re_path(r'.*^dashboard', views.path_confusion ,name = 'index'),

    ]
```

If the path `https://example.com/dashboard/none.js` is also opened by the user in the browser, the user dashboard information can be displayed, and if the target uses a CDN or web cache, a Web Cache Deception attack can be implemented.

## References

- [Bypassing Web Cache Poisoning Countermeasures](https://portswigger.net/research/bypassing-web-cache-poisoning-countermeasures)
- [Path confusion: Web cache deception threatens user information online](https://portswigger.net/daily-swig/path-confusion-web-cache-deception-threatens-user-information-online)

## Tools

- [OWASP Zed Attack Proxy](https://www.zaproxy.org)

## Whitepaper

[Web Cache Deception Attack](https://omergil.blogspot.com/2017/02/web-cache-deception-attack.html)
