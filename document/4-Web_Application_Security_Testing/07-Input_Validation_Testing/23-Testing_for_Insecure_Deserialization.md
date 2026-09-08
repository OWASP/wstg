# Testing for Insecure Deserialization

|ID          |
|------------|
|WSTG-INPV-23|

## Summary

Data serialization is the process of converting an object into a format that can be stored
(for example, in a file or database) or transmitted (for example, over a network) and
reconstructed later. Deserialization is the reverse process: taking data structured from
some format and rebuilding it into an object.

Insecure deserialization occurs when an application deserializes untrusted data without
sufficiently verifying that the resulting data will be valid. Attackers can leverage this
to manipulate serialized objects in order to influence application behavior or trigger
unintended actions during the deserialization process.

The most critical impact of insecure deserialization is remote code execution (RCE).
However, it may also result in denial of service (DoS), authentication bypass, access
control issues, or abuse of application logic.

JSON that is merged into objects in JavaScript runtimes can also enable
[prototype pollution](22-Testing_for_Prototype_Pollution.md). Treat that as a related
test case rather than a separate deserialization format.

## Test Objectives

- Identify entry points where the application accepts serialized objects from untrusted
  sources (for example, HTTP headers, parameters, or cookies).
- Determine the serialization format used by the application.
- Assess whether serialized input is validated or restricted prior to deserialization.
- Evaluate whether manipulation of serialized data leads to unsafe behavior or security
  impact.

## How to Test

### Black-Box Testing

#### Identification of Serialized Data

Identify where the application processes serialized data. Inspect cookies, hidden fields,
API bodies, headers, and file uploads for recognizable patterns, encodings, or structural
characteristics.

##### Java Serialization

Java serialized objects typically begin with the hex bytes `AC ED 00 05`. When base64
encoded, this frequently appears as `rO0`.

```http
Cookie: rememberMe=rO0ABXNyABpY...
```

##### PHP Serialization

PHP serialization is human-readable and uses specific characters to represent data types
(for example, `O` for object, `a` for array, `s` for string).

```http
Cookie: user_data=O:4:"User":2:{s:8:"username";s:5:"admin";s:8:"isAdmin";b:1;}
```

##### Python Pickle

Python pickle is a binary format that may be harder to recognize visually. Protocol 0
payloads are more readable and often end with a period (`.`). Higher protocols look like
opaque binary or base64 blobs in cookies, tokens, or job/queue parameters.

After fingerprinting a candidate, send a controlled out-of-band (OOB) or benign crash
probe generated for pickle (for example a payload that performs a DNS or HTTP callback to
a server you control). Confirm whether the application deserializes the value by watching
for the callback, a distinctive error, or a process crash. Never start with a destructive
RCE payload.

##### Node.js (node-serialize)

In Node.js applications using the `node-serialize` library, serialized data is often
represented as a JSON-like string. A key indicator of risk is an immediately invoked
function expression (IIFE) marker that starts with `_$$ND_FUNC$$_`.

```javascript
{"rce":"_$$ND_FUNC$$_function (){require('child_process').exec('id')}()"}
```

If you observe this marker in application traffic, replace the function body with a
harmless OOB callback and resubmit to confirm execution.

##### .NET Serialization

Legacy applications that still use `BinaryFormatter` or `NetDataContractSerializer` often
encode the output in base64. A common pattern for .NET serialized data starts with the hex
bytes `00 01 00 00 00 FF FF FF FF` or the base64 string `AAEAAAD/////`. Prefer treating
`BinaryFormatter` as legacy-only; it is obsolete and removed from modern .NET.

```http
Cookie: SessionData=AAEAAAD/////AQAAAAAAAAAMAgAAAF...
```

##### JSON-Based Deserialization with Type Metadata

Some JSON libraries support polymorphic typing. If attacker-controlled type metadata is
accepted, deserialization can instantiate unexpected classes.

Jackson with default typing often includes a type ID such as `@class`:

```json
{"@class":"com.example.Exploit","cmd":"id"}
```

Fastjson commonly uses `@type`:

```json
{"@type":"com.example.Exploit","cmd":"id"}
```

Treat attacker-controlled `@class`, `@type`, or similar type specifiers as a high-priority
finding, then confirm with a safe OOB gadget for that library.

#### Manipulation of Serialized Objects

Once an entry point is identified, modify the serialized data and observe how the
application responds.

Common manipulation techniques include:

- Changing object attributes or flags.
- Injecting additional fields.
- Modifying data types.
- Replaying modified serialized payloads.

Example (PHP):

A serialized object representing user state:

```php
O:4:"User":2:{s:8:"username";s:3:"bob";s:8:"isAdmin";b:0;}
```

If the application relies on this object for authorization decisions, change `b:0;` to
`b:1;` and resubmit. Privilege escalation confirms insecure trust in the deserialized
object. When editing string or array lengths, keep the PHP serialization length prefixes
consistent or the parser will reject the payload.

#### Testing for Dangerous Side Effects

Check whether deserialization triggers unintended behavior, such as:

- Execution of system commands.
- Invocation of internal application functionality.
- Excessive resource consumption (memory, CPU).
- Application crashes or unexpected state changes.

Look for evidence through:

- Behavioral changes in responses.
- Error messages or stack traces.
- Timing anomalies or service degradation.
- OOB DNS or HTTP callbacks from safe probe payloads.

#### Gadget Chain Abuse

In many environments, deserialization vulnerabilities require a gadget chain: a sequence
of existing code fragments (gadgets) within the application or its dependencies that,
during reconstruction, produce a malicious outcome.

Test with this sequence:

1. Identify third-party libraries in use (for example Commons Collections, Spring, or
   Jackson) from headers, errors, dependency files, or fingerprinting tools.
2. Generate a non-destructive confirmation payload with a specialized tool.
3. Submit the payload to the serialized-data sink and watch for an OOB callback. RCE often
   produces no direct response body, so DNS or HTTP callbacks are the reliable signal.

Example (Java, using ysoserial's `URLDNS` gadget for confirmation only):

```bash
java -jar ysoserial.jar URLDNS http://<collaborator-host>/
```

Base64-encode the raw output if the application expects base64, place it in the candidate
parameter or cookie, and resubmit. A DNS lookup for `<collaborator-host>` confirms that
the application deserialized the object. Use RCE gadgets only after confirmation and only
in authorized test environments.

For PHP, use PHPGGC to generate an equivalent OOB or file-write proof payload for a known
gadget chain present in the application.

### White-Box Testing

#### Code Review and Sink Functions

When source code is available, do not stop at finding sinks. Trace untrusted input to each
sink and verify which controls exist.

Common sinks include:

- Java: `java.io.ObjectInputStream.readObject()`, `readUnshared()`
- PHP: `unserialize()`
- Python: `pickle.loads()`, `marshal.loads()`, `shelve.open()`
- Node.js: `node-serialize.unserialize()`
- .NET: `BinaryFormatter.Deserialize()`, `NetDataContractSerializer.Deserialize()`

For each sink:

1. Confirm whether request parameters, cookies, headers, files, or queue messages reach it.
2. Check for allow-lists of permitted classes, integrity checks (for example HMAC), or
   platform filters such as Java's `ObjectInputFilter`.
3. Note missing controls, overly broad allow-lists, or signing that the client can bypass.

Apache Commons IO's `ValidatingObjectInputStream` is one allow-list approach for Java; prefer
documenting whatever filter the codebase actually uses, including JDK
`ObjectInputFilter` configuration.

## Remediation

Avoid deserializing untrusted data whenever possible.

If deserialization is required:

- Restrict accepted serialization formats and object types with a strict allow-list.
- Implement integrity controls to detect tampering.
- Apply validation before deserialization occurs.
- Prefer data-only formats such as JSON or XML parsed without attacker-controlled type
  metadata or polymorphic typing.
- For Java, apply an `ObjectInputFilter` or an allow-list mechanism such as Commons IO
  `ValidatingObjectInputStream` before classes are instantiated.
- If serialized objects must be passed to the client, sign them (for example with HMAC) so
  the server can reject modified payloads.
- Do not use legacy .NET `BinaryFormatter` for untrusted data.

See the [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
for deeper remediation guidance.

## Tools

- [ysoserial](https://github.com/frohoff/ysoserial) - generate Java deserialization payloads
- [ysoserial.net](https://github.com/pwntester/ysoserial.net) - generate .NET deserialization payloads
- [PHPGGC](https://github.com/ambionics/phpggc) - PHP gadget chains and payload generator
- [Freddy, Deserialization Bug Finder](https://portswigger.net/bappstore/ae1cce0c6d6c47528b4af35faebc3ab3) - Burp extension for Java and .NET deserialization detection
- [Java Deserialization Scanner](https://portswigger.net/bappstore/228336544ebe4e68824b5146dbbd93ae) - Burp extension for Java deserialization scanning and exploitation
- [GadgetProbe](https://github.com/BishopFox/GadgetProbe) - identify libraries available on a remote Java classpath

## References

- [CWE-502: Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html)
- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [OWASP Top 10 2021 A08: Software and Data Integrity Failures](https://owasp.org/Top10/2021/A08_2021-Software_and_Data_Integrity_Failures)
- [HackTricks: Deserialization](https://book.hacktricks.wiki/en/pentesting-web/deserialization/index.html)
