# Testing for Prototype Pollution

|ID          |
|------------|
|WSTG-INPV-22|

## Summary

JavaScript is a prototype-based language. Almost every object inherits from `Object.prototype`, and any property that is not found directly on an object is looked up through the prototype chain. Prototype pollution occurs when an application uses attacker-controlled input to set the *keys* of an object during a recursive merge, clone, or path-based assignment, allowing the attacker to reach `Object.prototype` through a special key such as `__proto__`, `constructor`, or `prototype`. Because that prototype is shared by every object in the runtime, the injected property silently becomes visible to unrelated parts of the application.

> Note: This is not the same as [HTTP Parameter Pollution](04-Testing_for_HTTP_Parameter_Pollution.md); despite the similar name, the two vulnerabilities are unrelated.

Pollution on its own rarely causes harm directly. Its impact depends on a *gadget*: existing code that later reads a property the attacker managed to plant and then uses it in a sensitive way. The same root cause appears in two contexts:

- **Server-side (Node.js)**: depending on the available gadget, impact ranges from denial of service and bypass of security logic to remote code execution. A well-known example is the Kibana RCE, [CVE-2019-7609](https://nvd.nist.gov/vuln/detail/CVE-2019-7609).
- **Client-side (browser)**: combined with a suitable gadget it commonly leads to DOM-based [Cross-Site Scripting](01-Testing_for_Reflected_Cross_Site_Scripting.md) and can be used to bypass client-side defenses.

## Test Objectives

- Identify functions and libraries that recursively merge, clone, or assign user-controlled properties.
- Determine whether user input can reach and modify `Object.prototype`.
- Identify gadgets that turn prototype pollution into a concrete impact.

## How to Test

The following example illustrates the root cause. A naive recursive merge copies every key of an attacker-controlled object into a target:

```javascript
function merge(target, source) {
    for (const key in source) {
        if (typeof source[key] === "object" && typeof target[key] === "object") {
            merge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}
```

If the source is parsed from user input such as `{"__proto__": {"polluted": "yes"}}`, the assignment walks into `__proto__` and writes onto `Object.prototype`. Afterwards every object in the runtime inherits the planted property:

```javascript
merge({}, JSON.parse('{"__proto__": {"polluted": "yes"}}'));
({}).polluted;   // "yes"  -> Object.prototype was polluted
```

### Black-Box Testing

#### Identify the Sources

Prototype pollution is reachable through any input whose keys end up as object property names. Review the application for:

- URL query string and the URL fragment (hash), using bracket or dotted notation, e.g. `?__proto__[key]=value` or `?__proto__.key=value`.
- JSON request bodies that are deserialized and then merged or cloned (configuration, profile, or settings endpoints are common candidates).
- Other structured inputs parsed into nested objects, such as form data or cookies.

#### Testing for Client-Side Prototype Pollution

Submit a probe that attempts to set a uniquely-named property on the prototype through a candidate source. The two encodings below express the same intent:

```text
https://example.com/#__proto__[testpolluted]=reflected
https://example.com/#constructor[prototype][testpolluted]=reflected
```

Then confirm in the browser developer console whether the property leaked onto the global prototype by reading it from a brand-new empty object:

```javascript
({}).testpolluted;
// "reflected" -> Object.prototype is polluted via this source
// undefined   -> not polluted through this source
```

If the value is returned, the source is exploitable and the next step is to find a gadget that turns the polluted property into DOM XSS (for example, a property a library reads when building markup or configuring script behavior). Browser tooling that scans for both sources and gadgets, such as DOM Invader (see Tools), significantly speeds up this phase.

#### Testing for Server-Side Prototype Pollution

The tester cannot read the prototype from a console here, so detection is indirect: pollute a property and observe an externally visible change in behavior. Send a JSON body that nests the special key inside an otherwise normal object, targeting an endpoint that merges or clones request data:

```http
POST /api/update HTTP/1.1
Host: example.com
Content-Type: application/json

{"name":"test","__proto__":{"json spaces":10}}
```

A reliable, non-destructive indicator on Express applications is to pollute the `json spaces` property: if a later JSON response from the application comes back pretty-printed (indented) when it previously was not, the server read the indentation setting from the polluted prototype, confirming the vulnerability. Other behavioral indicators include:

- A property the client never sent appearing in subsequent JSON responses.
- A change in HTTP status, headers, or content negotiation after polluting a property the framework reads internally.
- A distinctive error or parsing change for inputs that were previously accepted.

#### Assess the Impact

Because impact is gadget-dependent, analyze each confirmed pollution for realistic consequences. On the client-side this is most often DOM XSS or a bypass of a security control. On the server-side, gadgets have historically escalated to denial of service, authentication or authorization bypass, and remote code execution. Treat any confirmed prototype pollution as potentially high severity until gadget analysis rules out impact.

### Gray-Box Testing

When source code is available, search for the vulnerable patterns directly instead of probing blindly.

Look for recursive merge, clone, extend, or deep-assignment routines, whether hand-written or provided by a utility library. Functions that walk a nested path of keys and assign into an object are the primary sinks. A typical grep would target merge and assignment helpers, deep-clone utilities, and property access by user-controlled path.

For each candidate sink, confirm whether keys are validated before assignment. Safe code rejects or skips `__proto__`, `constructor`, and `prototype`, or uses objects without a prototype:

```javascript
// Vulnerable: blindly assigns into a nested key path
target[key] = source[key];

// Safer: refuse dangerous keys
if (key === "__proto__" || key === "constructor" || key === "prototype") {
    continue;
}
```

Also confirm the versions of any dependencies with known prototype pollution advisories, since many popular utilities have been patched over time. Where source code is available it is straightforward to trace user input from the request parser to these sinks and establish reachability, and to identify gadgets in the application or its dependencies.

## Remediation

- Sanitize property keys before assignment, explicitly rejecting `__proto__`, `constructor`, and `prototype`.
- Use objects without a prototype for map-like data, for example `Object.create(null)`, or use the `Map` data structure instead of plain objects.
- Freeze the base prototype with `Object.freeze(Object.prototype)` where the application's behavior permits it.
- Validate incoming structured data against a strict schema (for example, JSON Schema) so that unexpected keys are dropped.
- Prefer well-maintained merge and clone utilities, and keep all dependencies updated to versions that mitigate prototype pollution.
- On Node.js, the `--disable-proto=delete` runtime flag removes the `__proto__` accessor as a defense-in-depth measure.

## Tools

- [DOM Invader](https://portswigger.net/burp/documentation/desktop/tools/dom-invader) - automated source and gadget discovery for client-side prototype pollution
- [Burp Suite](https://portswigger.net/burp) - intercepting and crafting JSON payloads for server-side testing
- [ppmap](https://github.com/kleiton0x00/ppmap) - scanner for client-side prototype pollution
- [ppfuzz](https://github.com/dwisiswant0/ppfuzz) - prototype pollution fuzzer

## References

- [PortSwigger: Prototype Pollution](https://portswigger.net/web-security/prototype-pollution)
- [PortSwigger: Widespread Prototype Pollution Gadgets](https://portswigger.net/research/widespread-prototype-pollution-gadgets)
- [Olivier Arteau: Prototype Pollution Attacks in NodeJS Applications (NorthSec 2018)](https://github.com/HoLyVieR/prototype-pollution-nsec18)
- [BlackFan: Client-Side Prototype Pollution](https://github.com/BlackFan/client-side-prototype-pollution)
- [Michał Bentkowski: Prototype Pollution in Kibana (CVE-2019-7609)](https://slides.com/securitymb/prototype-pollution-in-kibana)
- [CWE-1321: Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution')](https://cwe.mitre.org/data/definitions/1321.html)
