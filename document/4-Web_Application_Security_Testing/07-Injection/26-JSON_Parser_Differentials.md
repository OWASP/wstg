# JSON Parser Differentials

|ID          |
|------------|
|WSTG-INJT-26|

## Summary

A JSON request often passes through more than one parser before it is acted on. An API gateway or web application firewall may inspect it, a service may check it against a schema or verify a signature over it, and a different service, perhaps written in another language, may then process it. If these parsers read the same document differently, a request can pass the check with one value and be processed with another. This is the JSON counterpart of [HTTP Parameter Pollution](04-HTTP_Parameter_Pollution.md). Disagreements about where the HTTP request itself starts and ends, such as conflicting `Content-Length` and `Transfer-Encoding` handling, are covered in [HTTP Request Smuggling](16-HTTP_Request_Smuggling.md). This page assumes both parsers already agree on the request body.

[RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html#section-4) only says that object names should be unique, and that when they are not, the behavior of the software that receives the object is unpredictable. In practice, parsers differ in several ways:

- **Duplicate keys.** Given `{"role": "user", "role": "admin"}`, some parsers keep the first value, many keep the last (Python's `json` module and JavaScript's `JSON.parse` both do), and some reject the document.
- **Key matching.** Some parsers match keys to fields loosely. For example, Go's `encoding/json` maps an object key to a struct field case-insensitively when there is no exact match, so `"Role"` and `"ROLE"` can both set the `Role` field, while a check written in another language only looks for `"role"`.
- **Invalid characters in keys.** Parsers handle invalid escape sequences, such as an unpaired surrogate (`\ud800`), and control characters differently. Some reject them, some replace them with U+FFFD, and some drop them, so `"role\ud800"` can be a separate key in one parser and collide with `"role"` in another.
- **Non-standard syntax.** Lenient parsers accept comments, trailing commas, single quotes or unquoted keys. A strict parser rejects the document, and two lenient parsers may disagree on where a comment ends.
- **Numbers.** Large integers and special values are decoded differently. `9007199254740993` is decoded exactly by Python but becomes `9007199254740992` in JavaScript, which stores all numbers as 64-bit floating point. Some parsers accept `NaN` and `Infinity`, which RFC 8259 does not allow, and others turn out-of-range numbers into the largest representable value or into zero.
- **Trailing data.** Python's `json` module and JavaScript's `JSON.parse` reject `{"role": "user"} {"role": "admin"}` because of the extra data after the first value. A streaming decoder, such as Go's `json.Decoder`, which many gateways and middleware use, reads only the first value and ignores the rest.

Where these differences sit between a security decision and the action it protects, they can be used to bypass authorization checks, input validation, rate limits, price or quantity checks, and signature or schema validation.

## Test Objectives

- Identify places where the same JSON document is parsed by more than one component.
- Determine whether those components disagree on duplicate keys, key matching, invalid characters, non-standard syntax, numbers or trailing data.
- Assess whether a disagreement lets a request pass a check with one value and be processed with another.

## How to Test

### Map the Parsers

Look for evidence that a JSON request crosses more than one component:

- Response headers, error messages and timing that point to an API gateway, a web application firewall or a service mesh in front of the application.
- Different error formats for different kinds of invalid input, which often come from different layers. Compare the response to a syntax error, a schema violation and a business rule violation.
- Architecture documents and API definitions that describe a separate validation, authorization or signing step.
- Requests that are forwarded or queued for another service, such as webhooks, background jobs and batch endpoints.

Fingerprinting the parsers helps choose probes. Send the requests below one at a time and note whether each is accepted, rejected, or changes the result. A parser that accepts comments or trailing commas, or that rejects duplicate keys, is often identifiable from these behaviors alone.

### Probe for Differences

For each field that affects a security decision, such as a role, user or account identifier, price, quantity, amount, or a flag that skips a check, send variations where the checked value and the used value can differ. Use a value the checks should accept and one they should reject, and try both orders:

```json
{"role": "user", "role": "admin"}
{"role": "admin", "role": "user"}
```

Then try the other differences:

```json
{"role": "user", "Role": "admin"}
{"role": "user", "role\ud800": "admin"}
{"role": "user", /* "role": "admin", */ "x": 1}
{"amount": 9007199254740993}
{"amount": 1e400}
{"amount": NaN}
{"role": "user"} {"role": "admin"}
```

A bypass needs the checking parser to accept the document and the acting parser to derive the dangerous value from it. Probes that a strict parser rejects outright, such as `NaN`, `Infinity`, comments, trailing commas and single quotes, only lead somewhere when the checking layer is the lenient one. Against a strict front layer they return an error, so note which layer is strict before ruling a probe out.

Look for a result that matches neither a clean accept nor a clean reject, for example:

- The request is accepted, but the stored or returned object holds the value the check should have rejected.
- A validation error mentions one value while the action uses another.
- The amount charged, the quantity shipped or the identifier acted on differs from the one in the request.
- An error from a deeper layer appears for a request that the front layer let through.

When a response echoes the parsed object, or the result can be read back with another request, compare it with the value that was sent. When nothing is echoed, compare the effect of the request, such as which account's data is returned or what was recorded, between a request with the variation and one without it.

### Signatures, Schemas and Stored Documents

Some designs check a JSON document once and use it later, for example a signed webhook, a JSON Web Token, a document validated against a schema before it is stored, or a message placed on a queue. If the check and the later use are done by different parsers, apply the same probes to the document. A signature only protects the bytes it covers, so a document whose meaning depends on which parser reads it can carry a valid signature and still be interpreted in more than one way.

## Related Test Cases

- [HTTP Parameter Pollution](04-HTTP_Parameter_Pollution.md)
- [Mass Assignment](20-Mass_Assignment.md)
- [HTTP Request Smuggling](16-HTTP_Request_Smuggling.md)
- [API Testing Overview](../12-API_Testing/00-API_Testing_Overview.md)

## Remediation

- Parse each request once, at the edge or in the service that makes the decision, and pass the parsed result on instead of the raw document.
- Configure parsers to reject duplicate keys, invalid escape sequences, non-standard syntax and numbers outside the range the application supports. The [I-JSON profile (RFC 7493)](https://www.rfc-editor.org/rfc/rfc7493.html) describes these restrictions.
- Match object keys to fields exactly, including case.
- Where a document has to be checked by one component and used by another, have both use the same parser and the same settings, or have the checking component pass on a normalized copy.
- Represent large or exact numbers, such as identifiers and amounts, as strings.

## References

- [Bishop Fox: An Exploration of JSON Interoperability Vulnerabilities](https://bishopfox.com/blog/json-interoperability-vulnerabilities)
- [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format, Section 4](https://www.rfc-editor.org/rfc/rfc8259.html#section-4)
- [RFC 7493: The I-JSON Message Format](https://www.rfc-editor.org/rfc/rfc7493.html)
- [Go encoding/json: Unmarshal](https://pkg.go.dev/encoding/json#Unmarshal)
- [MDN: Number.MAX_SAFE_INTEGER](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)
