# Testing for Insecure Deserialization

|ID          |
|------------|
|WSTG-INPV-22|

## Summary

Data serialization is the process of converting an object into a format that can be stored
(for example, in a file or database) or transmitted (for example, over a network) and
reconstructed later. Deserialization is the reverse process: taking data structured from
some format and rebuilding it into an object.

Insecure Deserialization occurs when an application deserializes untrusted data without
sufficiently verifying that the resulting data will be valid. Attackers can leverage this
to manipulate serialized objects in order to influence application behavior or trigger
unintended actions during the deserialization process.

The most critical impact of insecure deserialization is Remote Code Execution (RCE).
However, it may also result in Denial of Service (DoS), Authentication Bypass, Access
Control issues, or abuse of application logic.

## Test Objectives

- Identify entry points where the application accepts serialized objects from untrusted
  sources (e.g., HTTP headers, parameters, cookies).
- Determine the serialization format used by the application.
- Assess whether serialized input is validated or restricted prior to deserialization.
- Evaluate whether manipulation of serialized data leads to unsafe behavior or security
  impact.

## How to Test

### Black-Box Testing

#### Identification of Serialized Data

The first step is identifying where serialized data is processed. Serialized payloads
often expose recognizable patterns, encodings, or structural characteristics.

##### Java Serialization

Java serialized objects typically begin with the hex bytes `AC ED 00 05`. When Base64
encoded, this frequently appears as `rO0`.

```http
Cookie: JSESSIONID=rO0ABXNyABpY...
```

##### PHP Serialization

PHP serialization is human-readable and uses specific characters to represent data types
(e.g., `O` for Object, `a` for Array, `s` for String).

```http
User-Data: O:4:"User":2:{s:8:"username";s:5:"admin";s:8:"isAdmin";b:1;}
```

##### Python Pickle

Python Pickle uses a binary format that may be harder to recognize visually, but often
contains opcode-like characters or terminates with a period (`.`).

##### Node.js (node-serialize)

In Node.js applications using the `node-serialize` library, serialized data is often represented as a JSON-like string. A key indicator of vulnerability is the presence of an **Immediately Invoked Function Expression (IIFE)** pattern, which may start with `_$$ND_FUNC$$_`.

```javascript
{"rce":"_$$ND_FUNC$$_function (){ ... }()"}
```

##### .NET Serialization

Applications using `BinaryFormatter` or `NetDataContractSerializer` often encode the output in Base64. A common pattern for .NET serialized data is starting with the hex bytes `00 01 00 00 00 FF FF FF FF` or the Base64 string `AAEAAAD/////`.

```http
Cookie: SessionData=AAEAAAD/////AQAAAAAAAAAMAgAAAF...
```

##### JSON-based Deserialization (Modern Frameworks)

Modern applications often use JSON libraries like `Jackson` (Java) or `Fastjson`. If "Default Typing" is enabled, the JSON will contain type information, which is a major red flag.

```json
{"@type":"com.example.Exploit","cmd":"calc"}
```

##### Prototype Pollution via Deserialization

In JavaScript environments (Node.js), insecure deserialization often manifests as **Prototype Pollution**. When an application deserializes a JSON object and merges it into an existing object without validation, an attacker can inject properties like `__proto__` or `constructor.prototype`.

This can lead to:

- Overwriting application logic.
- Remote Code Execution (RCE) if the polluted property is later used in a dangerous sink (like `child_process.spawn`).

#### Manipulation of Serialized Objects

Once an entry point is identified, attempt to modify the serialized data and observe how
the application responds.

Common manipulation techniques include:

- Changing object attributes or flags
- Injecting additional fields
- Modifying data types
- Replaying modified serialized payloads

Example (PHP):

A serialized object representing user state:

```php
O:4:"User":2:{s:8:"username";s:3:"bob";s:8:"isAdmin";b:0;}
```

If the application relies on this object for authorization decisions, modifying `b:0;`
to `b:1;` may result in privilege escalation.

#### Testing for Dangerous Side Effects

Assess whether deserialization triggers unintended behavior, such as:

- Execution of system commands
- Invocation of internal application functionality
- Excessive resource consumption (memory, CPU)
- Application crashes or unexpected state changes

These effects may be identified through:

- Behavioral changes in responses
- Error messages or stack traces
- Timing anomalies or service degradation

#### Gadget Chain Abuse

In most modern environments, deserialization vulnerabilities require a "gadget chain"—a sequence of existing code fragments (gadgets) within the application's classpath that, when executed in order during reconstruction, lead to a malicious outcome.

**Exploitation Strategy:**

1. **Identify Libraries:** Determine which third-party libraries are in use (e.g., Commons-Collections, Spring, Jackson).
2. **Payload Generation:** Use specialized tools to generate payloads for known gadget chains.
3. **Out-of-Band (OOB) Testing:** Since RCE often doesn't return direct output, use payloads that trigger a DNS or HTTP request to a server you control (e.g., `ping`, `curl`) to confirm execution.

### White-Box Testing

#### Code Review and Sink Functions

When performing a white-box review, search for the following "sink functions" that process untrusted input:

- **Java:** `java.io.ObjectInputStream.readObject()`, `readUnshared()`
- **PHP:** `unserialize()`
- **Python:** `pickle.loads()`, `marshal.loads()`, `shelve.open()`
- **Node.js:** `node-serialize.unserialize()`, `serialize-javascript` (if misused)
- **.NET:** `BinaryFormatter.Deserialize()`, `NetDataContractSerializer.Deserialize()`

## Remediation

Applications should avoid deserializing untrusted data whenever possible.

If deserialization is required:

- Restrict accepted serialization formats and object types
- Implement integrity controls to detect tampering
- Apply strict validation before deserialization occurs
- **Use Data-Only Formats:** Prefer simple, language-agnostic formats like JSON or XML. Ensure they are parsed with secure, hardened parsers.
- **Look-ahead Deserialization:** For Java, use `ValidatingObjectInputStream` to implement an allow-list of permitted classes before they are instantiated.

**Implement Digital Signatures**: If serialized objects must be passed to the client, use a cryptographic signature (e.g., HMAC) to ensure the data has not been modified since it was created by the server.

## Tools

The following tools may assist during testing:

- **[ysoserial](https://github.com/frohoff/ysoserial):** The industry-standard tool for generating Java deserialization payloads.
- **[ysoserial.net](https://github.com/pwntester/ysoserial.net):** A version of ysoserial for .NET applications.
- **[PHPGGC](https://github.com/ambionics/phpggc):** A library of PHP gadget chains and a tool to generate them.
- **Burp Suite Extensions:**
    - **Freddy:** Automatically identifies and tests for deserialization in Java and .NET.
    - **Java Deserialization Scanner:** Detailed scanning for vulnerable Java libraries.
- **[GadgetProbe](https://github.com/BishopFox/GadgetProbe):** Helpful for identifying which libraries are available on the remote Java classpath.

## References

- [CWE-502](https://cwe.mitre.org/data/definitions/502.html) - Deserialization of Untrusted Data
- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [OWASP Top 10](https://owasp.org/Top10/2021/A08_2021-Software_and_Data_Integrity_Failures) – A08:2021 Software and Data Integrity Failures
- [hacktricks](https://book.hacktricks.wiki/en/pentesting-web/deserialization/index.html)
