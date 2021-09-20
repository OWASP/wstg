# Testing for Host Header Injection

|ID          |
|------------|
|WSTG-INPV-17|

## Summary

A web server commonly hosts several web applications on the same IP address, referring to each application via the virtual host. In an incoming HTTP request, web servers often dispatch the request to the target virtual host based on the value supplied in the Host header. Without proper validation of the header value, the attacker can supply invalid input to cause the web server to:

- Dispatch requests to the first virtual host on the list.
- Perform a redirect to an attacker-controlled domain.
- Perform web cache poisoning.
- Manipulate password reset functionality.
- Allow access to virtual hosts that were not intended to be externally accessible.

## Test Objectives

- Assess if the Host header is being parsed dynamically in the application.
- Bypass security controls that rely on the header.

## How to Test

Initial testing is as simple as supplying another domain (i.e. `attacker.com`) into the Host header field. It is how the web server processes the header value that dictates the impact. The attack is valid when the web server processes the input to send the request to an attacker-controlled host that resides at the supplied domain, and not to an internal virtual host that resides on the web server.

```http
GET / HTTP/1.1
Host: www.attacker.com
[...]
```

In the simplest case, this may cause a 302 redirect to the supplied domain.

```http
HTTP/1.1 302 Found
[...]
Location: http://www.attacker.com/login.php

```

Alternatively, the web server may send the request to the first virtual host on the list.

### X-Forwarded Host Header Bypass

In the event that Host header injection is mitigated by checking for invalid input injected via the Host header, you can supply the value to the `X-Forwarded-Host` header.

```http
GET / HTTP/1.1
Host: www.example.com
X-Forwarded-Host: www.attacker.com
[...]
```

Potentially producing client-side output such as:

```html
[...]
<link src="http://www.attacker.com/link" />
[...]
```

Once again, this depends on how the web server processes the header value.

### Web Cache Poisoning

Using this technique, an attacker can manipulate a web-cache to serve poisoned content to anyone who requests it. This relies on the ability to poison the caching proxy run by the application itself, CDNs, or other downstream providers. As a result, the victim will have no control over receiving the malicious content when requesting the vulnerable application.

```http
GET / HTTP/1.1
Host: www.attacker.com
[...]
```

The following will be served from the web cache, when a victim visits the vulnerable application.

```html
[...]
<link src="http://www.attacker.com/link" />
[...]
```

### Password Reset Poisoning

It is common for password reset functionality to include the Host header value when creating password reset links that use a generated secret token. If the application processes an attacker-controlled domain to create a password reset link, the victim may click on the link in the email and allow the attacker to obtain the reset token, thus resetting the victim's password.

The example below shows a password reset link that is generated in PHP using the value of `$_SERVER['HTTP_HOST']`, which is set based on the contents of the HTTP Host header:

```php
$reset_url = "https://" . $_SERVER['HTTP_HOST'] . "/reset.php?token=" .$token;
send_reset_email($email,$rset_url);
```

By making a HTTP request to the password reset page with a tampered Host header, we can modify where the URL points:

```http
POST /request_password_reset.php HTTP/1.1
Host: www.attacker.com
[...]

email=user@example.org
```

The specified domain (`www.attacker.com`) will then be used in the reset link, which is emailed to the user. When the user clicks this link, the attacker can steal the token and compromise their account.

```text
... Email snippet ...

Click on the following link to reset your password:

https://www.attacker.com/reset.php?token=12345

... Email snippet ...
```

### Accessing Private Virtual Hosts

In some cases a server may have virtual hosts that are not intended to be externally accessible. This is most common with a [split-horizon](https://en.wikipedia.org/wiki/Split-horizon_DNS) DNS setup (where internal and external DNS servers return different records for the same domain).

For example, an organisation may have a single webserver on their internal network, which hosts both their public website (on `www.example.org`) and their internal Intranet (on `intranet.example.org`, but that record only exists on the internal DNS server). Although it would not be possible to browse directly to `intranet.example.org` from outside the network (as the domain would not resolve), it may be possible to access to Intranet by making a request from outside with the following `Host` header:

```http
Host: intranet.example.org
```

This could also be achieved by adding an entry for `intranet.example.org` to your hosts file with the public IP address of `www.example.org`, or by overriding DNS resolution in your testing tool.

## References

- [What is a Host Header Attack?](https://www.acunetix.com/blog/articles/automated-detection-of-host-header-attacks/)
- [Host Header Attack](https://www.briskinfosec.com/blogs/blogsdetail/Host-Header-Attack)
- [HTTP Host header attacks](https://portswigger.net/web-security/host-header)
