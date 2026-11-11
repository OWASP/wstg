# DNS Rebinding

|ID          |
|------------|
|WSTG-CLNT-21|

## Summary

DNS rebinding lets a web page on an attacker's domain send requests to services that the attacker cannot reach directly, such as services on the victim's local network or on `localhost`, and read the responses. The same-origin policy compares the scheme, host name and port of a URL, not the IP address the host name resolves to. If the attacker's domain first resolves to the attacker's server and later resolves to an internal address, the browser still treats both as the same origin.

A typical attack works like this:

1. The victim visits `http://rebind.attacker.example:8080/`, and the attacker's DNS server answers with the attacker's public IP address and a very short TTL.
2. The page loads JavaScript from the attacker's server and waits until the browser's DNS cache entry expires.
3. When the script sends another request to `http://rebind.attacker.example:8080/`, the DNS server now answers with an internal address, such as `127.0.0.1` or `192.168.1.1`.
4. The request goes to the internal service on port 8080, and since the origin has not changed, the script can read the response and send it back to the attacker.

The request still carries `Host: rebind.attacker.example:8080`, and it does not include the internal service's cookies, because the browser stores cookies by host name. The attack therefore works against services that accept any `Host` header and do not require authentication, or rely only on the network for protection. Common targets include:

- Administration consoles and APIs that listen on `localhost` or an internal network and have no authentication.
- Development servers, debuggers and build tools.
- Desktop applications and browser helpers that expose a local HTTP or WebSocket API.
- Routers, printers, cameras and other devices on the local network.
- Cloud instance metadata services, when the browser runs on a cloud instance.

DNS rebinding is also used against servers. When an application protects against [Server-Side Request Forgery](../07-Injection/19-Server-Side_Request_Forgery.md) by resolving a host name, checking that the IP address is public, and then letting its HTTP client resolve the name again, a DNS server that changes its answer between the two lookups can make the second request go to an internal address.

## Test Objectives

- Identify services in scope that are reachable only from the local machine or an internal network and are used from a browser.
- Determine whether those services accept requests with an unexpected `Host` header and without authentication.
- Determine whether server-side URL fetching can be redirected to internal addresses by changing DNS answers between validation and use.

## How to Test

DNS rebinding tests need a DNS server that the tester controls, or a public rebinding service. Agree the scope with the owner first, and only point rebinding domains at addresses that are in scope.

### Identify Exposed Local Services

List the services that the application installs or depends on and that are reachable from a browser without going through the internet:

- Local HTTP or WebSocket listeners of desktop applications and agents. On the test machine, `netstat -an`, `ss -ltnp` or `lsof -i -P` shows listening ports.
- Web interfaces of devices and internal tools on the same network.
- Services documented as "only listens on localhost" or "only reachable from the internal network".

For each service, note whether it requires authentication and whether its interface can change data or settings.

### Check Host Header Validation

The most important defense is that the service rejects requests whose `Host` header does not match a name it expects. This can be tested without a rebinding domain, by sending a request to the service with a different `Host` header:

```bash
curl -i -H 'Host: rebind.attacker.example:8080' http://127.0.0.1:8080/api/status
```

If the response is the same as with `Host: localhost:8080`, the service does not check the `Host` header and is likely exploitable through DNS rebinding. A service that responds with an error, a redirect to its expected name, or a different virtual host is protected against this part of the attack.

Also check whether the service requires authentication for every request, including requests from `localhost`, and whether it accepts cross-origin requests without a preflight, such as simple `POST` requests with a `text/plain` body.

### Demonstrate the Attack

To confirm the impact, use a rebinding service:

- [Singularity of Origin](https://github.com/nccgroup/singularity) runs the DNS server and a web interface that rebinds a domain to a chosen target and port, with payloads for common services and techniques to speed up the rebinding.
- [rbndr](https://github.com/taviso/rbndr) answers with one of two IPv4 addresses encoded in the host name, chosen at random for each query. For example, `7f000001.c0a80001.rbndr.us` resolves to either `127.0.0.1` or `192.168.0.1`.

Open the attack page in a browser on the machine or network where the target service runs, and check whether the page can read a response from the service or perform an action on it. Browsers cache DNS answers for some time and may try several addresses, so a single attempt can take a minute or more.

Recent versions of Chrome ask the user for permission before a public site can connect to local network or loopback addresses, as part of [Local Network Access](https://developer.chrome.com/blog/local-network-access). Test in the browsers the users of the service are expected to use. A service that is only protected by a browser prompt is still at risk from users who accept it and from browsers that do not show it.

### Server-Side Rebinding

If the application fetches URLs supplied by users and blocks internal addresses, submit a URL whose host name alternates between a public address and an internal one, for example with rbndr or Singularity. Submit it several times, because each attempt only succeeds when the validation sees the public address and the fetch sees the internal one. Watch for responses, errors or timing that show the request reached an internal service. Also check whether the application follows redirects to internal addresses after validating the first URL.

## Related Test Cases

- [Server-Side Request Forgery](../07-Injection/19-Server-Side_Request_Forgery.md)
- [Host Header Injection](../07-Injection/17-Host_Header_Injection.md)
- [Cross Origin Resource Sharing](07-Cross_Origin_Resource_Sharing.md)
- [WebSockets](10-WebSockets.md)
- [Enumerate Infrastructure and Application Admin Interfaces](../02-Configuration_and_Deployment_Management/05-Enumerate_Infrastructure_and_Application_Admin_Interfaces.md)

## Remediation

- Validate the `Host` header on every local and internal service, and reject requests for names the service does not serve.
- Require authentication on local and internal services, including for requests from `localhost`. Use a secret that a web page cannot obtain, such as a random token written to a file that only the local user can read.
- Use TLS for internal services where possible. A rebound request goes to the attacker's host name, which does not match the service's certificate, so the browser refuses the connection.
- Check the `Origin` header on state-changing requests and WebSocket handshakes, and reject origins that are not expected.
- For server-side URL fetching, resolve the host name once, check the resulting IP address, and connect to that address. Repeat the check for every redirect. The [Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) has more guidance.
- On networks the organization controls, configure DNS resolvers to drop answers with private addresses for public names, for example with the `--stop-dns-rebind` option of dnsmasq or the `private-address` option of Unbound.

## Tools

- [Singularity of Origin](https://github.com/nccgroup/singularity), a DNS rebinding attack framework
- [rbndr](https://github.com/taviso/rbndr), a simple DNS rebinding service

## References

- [NCC Group: Singularity of Origin documentation](https://github.com/nccgroup/singularity/wiki)
- [Chrome for Developers: New permission prompt for Local Network Access](https://developer.chrome.com/blog/local-network-access)
- [WICG: Local Network Access](https://wicg.github.io/local-network-access/)
- [OWASP Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [dnsmasq manual page](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)
