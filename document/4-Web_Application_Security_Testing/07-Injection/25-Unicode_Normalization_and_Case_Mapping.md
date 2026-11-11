# Testing Unicode Normalization and Case Mapping

|ID          |
|------------|
|WSTG-INJT-25|

## Summary

Unicode normalization and case mapping can change a string after an application accepts it. For example, [Unicode compatibility normalization](https://www.unicode.org/reports/tr15/) (NFKC) changes fullwidth angle brackets into ASCII angle brackets. [Full case mappings](https://www.unicode.org/faq/casemap_charprop.html#case-mapping) can also change the number of characters in a string. If a security check examines one form while a later component uses another, the check may miss a value it was meant to reject.

A changed string alone is not a vulnerability. Confirm that the application accepts the input, transforms it, and then uses the result in a way that bypasses a security control. The impact depends on the field and its destination. For example, a transformed value could become a path separator, an HTML delimiter, or an identifier that an earlier check treated differently.

## Test Objectives

- Identify fields that undergo Unicode normalization or case mapping after validation.
- Determine whether the value used by a security control differs from the value used later by the application.
- Confirm a security impact rather than reporting a transformation alone.

## How to Test

### Identify Transformations

Find inputs whose meaning depends on string comparison or special characters, such as file paths, user identifiers, allowlists, and text displayed in HTML. Review the application's validation, storage, and use of each value when source code is available. Check transformations in application code, frameworks, databases, and downstream services.

For a black-box test, submit a distinctive value and inspect the response, stored value, or later lookup. Compare the submitted value with the form used at the point where the application makes a security decision. Use a controlled test account or environment for state-changing requests.

### Compare Equivalent Inputs

Submit an ordinary value, a value that the application rejects, and a Unicode variant that becomes the rejected value under the application's transformation. Keep the request and account state the same between comparisons. These examples show possible transformations, not universal application behavior:

| Submitted value | Transformation | Result |
| --- | --- | --- |
| `＜tag＞` | NFKC | `<tag>` |
| `．．／` | NFKC | `../` |
| `ı` (dotless i) | Default uppercase mapping | `I` |
| `ß` (sharp s) | Full uppercase mapping | `SS` |

NFC and NFD preserve distinctions that NFKC or NFKD may remove. Case mappings may also depend on the implementation and locale. Verify the actual transformation used by the target rather than assuming that every Unicode variant maps to the same result.

If an ASCII path sequence is rejected but its fullwidth form is accepted, check whether a later file or URL operation uses the transformed `../` sequence. If angle brackets are filtered before NFKC, check whether the transformed value reaches an HTML context without suitable output encoding. Do not infer path traversal or cross-site scripting from acceptance alone; verify the resulting access or rendering with a harmless marker.

For fields with length limits or case-insensitive comparisons, compare the value and length before and after the application's case mapping. Check whether validation, storage, and lookup use the same representation. Test a collision only with accounts or records you control.

### Confirm the Boundary

Record the form of the value at each relevant step: request decoding, normalization or case mapping, validation, storage, and final use. A finding requires evidence that an earlier check allowed a value that the later component treated as forbidden or privileged. If the application rejects the transformed value or safely encodes it at the destination, the Unicode transformation does not establish a bypass.

## Related Test Cases

- [Business Logic Data Validation](../10-Business_Logic/01-Business_Logic_Data_Validation.md)
- [Reflected Cross Site Scripting](01-Reflected_Cross_Site_Scripting.md)
- [File Inclusion](11.1-File_Inclusion.md)

## Remediation

Define a normalization and case-comparison policy for each field, then apply it consistently before validation, storage, and comparison. Validate the representation the application will actually use. Do not apply compatibility normalization to every field without checking whether it erases meaningful distinctions. Continue to use context-appropriate output encoding and safe path handling; normalization does not replace those controls. See the [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html#validating-free-form-unicode-text).
