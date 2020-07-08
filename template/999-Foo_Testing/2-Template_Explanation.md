# Article Template Explanation

|ID          |
|------------|
|WSTG-FOO-002|

## How to Name Your File

The filename format is:

`<number>-Article_Name.md`

To name your file:

- Replace `<number>` with the appropriate integer. If you are unsure which section your article belongs in, post a comment in your [new content issue](https://github.com/OWASP/wstg/issues?q=is%3Aopen+is%3Aissue+label%3ANew) asking for input.
- Write the article name in title case spaced with underscores for better URL encoding. If the article is titled, "Testing Foo Bypass in Bars" the filename component is: `Testing_Foo_Bypass_in_Bars` (with a hyphen separating the `<number>` from the title).

## Article Sections

The remainder of this document explains each section in the [article example](1-Testing_for_a_Cat_in_a_Box.md).

## Title

The first line of the document is a title at level H1. Followed by a Markdown table that includes the ID of the testing scenario. For example:

```md
|ID          |
|------------|
|WSTG-FOO-002|
```

## Summary

Fully describe the reason for the test. Name specific vulnerabilities. Give the background information necessary for a reader with basic technical expertise. Explain terminology and abbreviations. See the [style guide](../../style_guide.md) for more.

## Test Objectives

Use an [active voice](../../style_guide.md#active-voice) to describe the goal of the test.

## How to Test

Provide specific instructions for performing one or more tests that satisfy the stated objective above. Use individual headings for different tests or methods. Be concise and complete. Use code snippets or images where necessary.

## Remediation

Give a short overview of preventative measures. You may use bullet points. Provide leads to solutions that the reader can follow, but do not try to describe the entire solution itself. Remediation is outside the scope of the testing guide project.

Avoid duplicating content from other OWASP projects. Provide inline links to outside content as needed. Consider the following OWASP resources: [Application Security Verification Standard (ASVS)](https://github.com/OWASP/ASVS), [Top 10](https://github.com/OWASP/Top10), [Proactive Controls](https://owasp.org/www-project-proactive-controls/), or the [Cheat Sheet Series](https://cheatsheetseries.owasp.org).

## References

If the article contains information sourced from other documents that you could not gracefully link inline, include them here in a bulleted list of links.
