# Unicode Normalization and Case Mapping

|ID          |
|------------|
|WSTG-INJT-25|

## Summary

Many Unicode characters have an equivalent that is written differently. Applications often turn input into one standard representation before they use it, either through Unicode normalization or through case mapping:

- [Unicode normalization](https://www.unicode.org/reports/tr15/) has four forms. NFC and NFD only change characters that are canonically equivalent, mostly combining accents and a few signs such as the Kelvin sign `K` (U+212A), which becomes `K`. The compatibility forms NFKC and NFKD also replace characters with their plain equivalents. For example, they turn the fullwidth `＜` (U+FF1C) into `<`, `＇` (U+FF07) into `'`, `．．／` into `../`, and the ligature `ﬁ` (U+FB01) into `fi`.
- Case mapping is not a one-to-one mapping of letters. Uppercasing turns `ß` into `SS`, `ﬁ` into `FI`, the dotless `ı` (U+0131) into `I` and the long `ſ` (U+017F) into `S`. Lowercasing turns the Kelvin sign `K` (U+212A) into `k`, and `İ` (U+0130) into `i` followed by a combining dot, which is two code points. Some functions also depend on the server's locale: in Java, `"FILE".toLowerCase()` returns `fıle` when the default locale is Turkish.

These transformations are a problem when they run after a security check. A filter that blocks `<`, `'` or `../` sees only the harmless-looking equivalents and lets them through, and the code that runs later receives the characters the filter was meant to block. This is known as validating before canonicalizing ([CWE-180](https://cwe.mitre.org/data/definitions/180.html)), and it can turn a filter bypass into Cross Site Scripting, SQL injection, path traversal or another injection. Normalization and case mapping can also make a value longer after its length was checked: NFKC turns the single character `ﷺ` (U+FDFA) into 18 characters.

The same problem appears when two components transform input differently, for example a web application firewall that does not normalize in front of an application that does, or a front end and a back end that use different normalization forms.

When different identifiers, such as usernames or email addresses, become the same value after normalization or case mapping, the risk is account collision and takeover. That is a separate issue and is not covered here.

## Test Objectives

- Identify where the application normalizes or changes the case of input.
- Determine whether validation, filtering or length checks run before that transformation.
- Assess whether the transformation can be used to bypass filters for injection, path traversal or length limits.

## How to Test

Send non-ASCII characters as UTF-8 and percent-encode them in URLs and form bodies. For example, `＜` is sent as `%EF%BC%9C`. Browsers and intercepting proxies do this automatically when the character is typed or pasted.

### Detect Normalization and Case Mapping

Submit harmless probe characters wherever input is reflected, stored and displayed again, or used to look up data, and compare what comes back with what was sent:

| Probe | Code point | Encoded | Comes back as | Indicates |
|-------|------------|---------|---------------|-----------|
| `ﬁ` | U+FB01 | `%EF%AC%81` | `fi` | NFKC or NFKD |
| `Ａ` | U+FF21 | `%EF%BC%A1` | `A` | NFKC or NFKD |
| `²` | U+00B2 | `%C2%B2` | `2` | NFKC or NFKD |
| `ß` | U+00DF | `%C3%9F` | `SS` or `ss` | Uppercasing or case folding |
| `ı` | U+0131 | `%C4%B1` | `I` | Uppercasing |
| `K` | U+212A | `%E2%84%AA` | `k`, or `K` | Lowercasing, or any normalization form |

If the probe is not reflected, look for its effect instead. For example, check whether a search for `ﬁle` returns the same results as a search for `file`, or whether a file uploaded as `ﬁle.txt` is listed as `file.txt`.

When the source code is available, search for normalization and case conversion functions, such as `unicodedata.normalize` and `str.casefold` in Python, `String.prototype.normalize` in JavaScript, `java.text.Normalizer` and `String.toLowerCase()` without a `Locale` argument in Java, and `String.Normalize` in .NET. Note where they are called relative to validation, sanitization and encoding.

### Determine the Order of Validation and Transformation

Find an input where a character is blocked, and confirm that sending the character itself is rejected. Then send a compatibility equivalent of the same character. If the request is accepted and the plain character reaches the output or the sink, the application validates before it normalizes.

The following equivalents become the plain characters under NFKC and NFKD:

| Blocked | Equivalent | Code points |
|---------|------------|-------------|
| `<` `>` | `＜` `＞` | U+FF1C, U+FF1E |
| `'` | `＇` | U+FF07 |
| `"` | `＂` | U+FF02 |
| `/` `\` | `／` `＼` | U+FF0F, U+FF3C |
| `..` | `．．` or `‥` | U+FF0E, or U+2025 (two dot leader) |
| `;` | `；` | U+FF1B |

For example, an application that rejects `<` and `>` in a name, and normalizes the name before including it in a page, accepts this request:

```http
GET /greet?name=%EF%BC%9Cimg%20src%3Dx%20onerror%3Dalert(document.domain)%EF%BC%9E HTTP/1.1
Host: www.example.com
```

The response then contains the markup the filter was meant to block:

```html
<p>Hello <img src=x onerror=alert(document.domain)></p>
```

In the same way, an application that rejects `..`, `/` and `\` in a filename, and normalizes the name before opening the file, opens `../secret.txt` when it receives `‥／secret.txt` (`%E2%80%A5%EF%BC%8Fsecret.txt`).

A single character can also combine both kinds of transformation. The long `ſ` is not changed by lowercasing, so a filter that lowercases the input and looks for `script` does not match `<ſcript>`, but NFKC turns the long `ſ` into `s` and the value into `<script>`.

[REcollapse](https://github.com/0xacb/recollapse) generates variants of a payload with normalization and case mapping equivalents at chosen positions, which helps when the blocked characters are not known.

### Test Case Mapping

Check the inputs that are compared with keywords or allow lists without regard to case:

- Send keywords that contain characters that change into ASCII letters when the case changes, such as `ſ`, `ı`, `K` and the ligatures `ﬁ` and `ﬂ`, and check whether they are treated as the ASCII keyword.
- Send keywords that contain `I` and `i`. On a server whose locale is Turkish or Azerbaijani, locale-dependent functions turn `I` into `ı` when lowercasing and `i` into `İ` when uppercasing, so a check such as `value.toLowerCase().equals("file")` in Java no longer matches `FILE`.

### Test Length Checks

Find inputs with a maximum length, and submit values within the limit that become longer after normalization or case mapping, such as `ﷺ` (18 characters after NFKC), `ﬃ` (3 characters) or `ß` (2 characters when uppercased). For example, if `ﷺﷺ` is accepted where the limit is five characters, and it is later stored or processed as 36 characters, the length check runs too early. Look for truncated values that cut an escape sequence or a closing quote in half, for database errors, and for limits on payload size that no longer apply.

## Related Test Cases

- [Reflected Cross Site Scripting](01-Reflected_Cross_Site_Scripting.md)
- [Stored Cross Site Scripting](02-Stored_Cross_Site_Scripting.md)
- [SQL Injection](05-SQL_Injection.md)
- [Directory Traversal and File Include](../05-Authorization/01-Directory_Traversal_File_Include.md)

## Remediation

- Normalize and change case first, then validate. Validate the exact value that the rest of the application uses, and do not transform it again after validation.
- Use one normalization form and one case policy in every component that handles the value, including web application firewalls, front ends, back ends and databases.
- Use locale-independent case conversion, such as `toLowerCase(Locale.ROOT)` in Java or `ToUpperInvariant()` in .NET, and use case folding (for example `str.casefold()` in Python) for case-insensitive comparisons.
- Check length after normalization and case mapping, and limit the size of input in bytes as well as in characters.
- Rely on context-aware output encoding and parameterized queries rather than on blocking characters. A filter can be bypassed with an equivalent character, while encoding at the point of use is not affected by how the value was written.

## Tools

- [REcollapse](https://github.com/0xacb/recollapse)

## References

- [Unicode Standard Annex #15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/)
- [Unicode Technical Report #36: Unicode Security Considerations](https://www.unicode.org/reports/tr36/)
- [CWE-180: Incorrect Behavior Order: Validate Before Canonicalize](https://cwe.mitre.org/data/definitions/180.html)
- [CWE-176: Improper Handling of Unicode Encoding](https://cwe.mitre.org/data/definitions/176.html)
