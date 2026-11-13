# Regular Expression Denial of Service

|ID          |
|------------|
|WSTG-INJT-28|

## Summary

Regular expression denial of service (ReDoS) happens when an application matches user input against a regular expression that takes a very long time on some inputs. Most regular expression engines in common use, including the ones in JavaScript, Java, Python, PHP (PCRE), Ruby and .NET by default, are backtracking engines. When a pattern can match the same part of the input in many different ways, a backtracking engine may try every one of them before it gives up, and the number of attempts can grow exponentially with the length of the input.

A classic example is the pattern `^(a+)+$`. Matching it against `aaaaaaaaaaaaaaaaaaaaaaaaaaaaa!` fails, but only after the engine has tried every way of splitting the `a` characters between the inner and outer group. Each extra `a` roughly doubles the time, so an input of a few dozen characters can keep a CPU busy for seconds or minutes. Real patterns rarely look this obvious. The same problem shows up in validation patterns for email addresses, URLs, usernames and filenames, many of which have been copied between projects for years.

Not every slow pattern is exponential. Patterns such as `\s+$` or `^\s+|\s+$` take time that grows with the square of the input length when the input is a long run of whitespace followed by another character. That is usually harmless for short fields, but it is enough to cause an outage when the input is a whole request body or a long text field.

The impact depends on where the pattern runs:

- On a server with a single event loop, such as Node.js, one slow match blocks every other request handled by that process.
- On thread-based servers, each slow request ties up a worker thread, and a handful of concurrent requests can exhaust the pool.
- In the browser, a slow match freezes the tab of the user who triggered it. This matters when the attacker controls content that is matched in other users' browsers, such as a message or a profile field.

Applications that let users supply their own regular expression, for example in a search filter, a routing rule or a log query, are exposed to the same problem even when the application's own patterns are safe.

## Test Objectives

- Identify inputs that are validated or processed with regular expressions.
- Determine whether any of those regular expressions take super-linear time on crafted input.
- Determine whether users can supply their own regular expressions and whether those are run with any limits.

## How to Test

ReDoS testing can make a shared environment unresponsive. Agree the scope with the application owner first, prefer a non-production environment, send one request at a time, and stop increasing the input size as soon as response times start to grow.

### Find Regular Expressions

Look for places where input is checked against a format or transformed with a pattern:

- Fields with format rules, such as email, phone number, URL, username, password complexity, postal code and date fields. Error messages like "invalid email format" suggest that a pattern is applied.
- Client-side JavaScript. Validation patterns are often duplicated in the browser, so search the scripts for regular expression literals (`/.../`), `new RegExp(`, `pattern` attributes on `input` elements and calls such as `.match(`, `.test(` and `.replace(`.
- Search, filter and query features. Check whether characters such as `.*`, `(`, `[` or `\` change the results, which suggests that the input itself is used as a pattern.
- Parsers for structured headers and values, such as `User-Agent`, `Accept-Language`, cookies and Markdown or template content.
- Third-party libraries. Identify libraries and their versions from client-side bundles or response headers, and check them against public advisories, as many published advisories for JavaScript packages are ReDoS issues.

When the source code is available, review patterns for these warning signs:

- Nested quantifiers, such as `(a+)+`, `(a*)*` or `(\w+\s?)+`.
- Alternation where the branches can match the same text, such as `(a|a)*`, `(a|ab)*` or `(\w|\d)+`.
- Several quantified parts next to each other that can match the same characters, such as `\s*\s*$` or `.*.*=.*`.

### Measure Response Times

For each candidate input, send the same request with inputs of increasing length and compare the response times. The input should be long runs of characters that the pattern accepts, followed by one character that makes the match fail, because the engine only explores every alternative when it cannot find a match.

For a field validated with a pattern like `^([a-zA-Z0-9]+\.?)+@example\.com$`, an input such as `aaaaaaaaaaaaaaaaaaaaaaaa!` works. A simple loop with `curl` shows how the time grows:

```bash
for n in 10 14 18 20 22 24 26; do
  payload=$(printf 'a%.0s' $(seq 1 $n))'!'
  printf '%s: ' "$n"
  curl -s -o /dev/null -w '%{time_total}\n' \
    --data-urlencode "email=$payload" https://example.com/register
done
```

Response times that stay roughly flat suggest the pattern is safe for that input. Times that double with every one or two extra characters indicate exponential backtracking. Times that grow steadily but much faster than the input length indicate polynomial backtracking, which is worth confirming with longer inputs if the field accepts them.

Network jitter can hide small differences, so repeat each measurement a few times, and compare against a request with a valid input of the same length. If the application enforces a short length limit before applying the pattern, note the limit, as it may make the issue impractical to exploit.

For client-side patterns, the same inputs can be tested in the browser developer tools console by timing the match directly, for example with `console.time()` and `console.timeEnd()` around `pattern.test(input)`.

### User-Supplied Patterns

If the application accepts a regular expression from the user, submit a pattern known to backtrack badly together with a matching input, for example the pattern `^(a+)+$` against content that contains a long run of `a` characters followed by another character. Check whether the application:

- Rejects or limits the pattern.
- Applies a timeout and returns an error.
- Uses an engine that is not affected, in which case the response time stays low.

### Validation Bypass on Backtracking Limits

Some engines stop after a fixed amount of backtracking instead of running forever. For example, PHP's PCRE functions return `false` or `null` when `pcre.backtrack_limit` is reached. If the application only checks whether a match was found, an input that hits the limit may be treated differently from both a match and a non-match. Where a validation pattern backtracks heavily, check whether an input that hits the limit is accepted when it should be rejected.

## Related Test Cases

- [Business Logic Data Validation](../10-Business_Logic/01-Business_Logic_Data_Validation.md)
- [Defenses Against Application Misuse](../10-Business_Logic/07-Defenses_Against_Application_Misuse.md)
- [Circumvention of Work Flows](../10-Business_Logic/06-Circumvention_of_Work_Flows.md)

## Remediation

- Use a regular expression engine that guarantees linear-time matching for untrusted input, such as [RE2](https://github.com/google/re2), Go's `regexp` package, Rust's `regex` crate, or `RegexOptions.NonBacktracking` in .NET 7 and later.
- Where a backtracking engine has to be used, set a match timeout. .NET accepts a timeout when a `Regex` is created, Ruby 3.2 and later has `Regexp.timeout`, and the third-party `regex` module for Python accepts a `timeout` argument.
- Rewrite patterns so that each part of the input can only be matched one way, for example by removing nested quantifiers and overlapping alternatives. Check patterns with a ReDoS analysis tool in code review or CI.
- Limit the length of input before applying a pattern.
- Treat an engine error, such as a timeout or a backtracking limit, as a failed validation.
- Avoid running user-supplied patterns. If the feature is required, run them with a linear-time engine, or with a strict timeout and length limits.

## Tools

- [recheck](https://makenowjust-labs.github.io/recheck/), a ReDoS checker for JavaScript and other regular expression syntaxes
- [regexploit](https://github.com/doyensec/regexploit), which finds regular expressions vulnerable to ReDoS and suggests an attack string
- CodeQL queries for [exponential](https://codeql.github.com/codeql-query-help/javascript/js-redos/) and [polynomial](https://codeql.github.com/codeql-query-help/javascript/js-polynomial-redos/) ReDoS in JavaScript

## References

- [OWASP: Regular expression Denial of Service - ReDoS](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)
- [CWE-1333: Inefficient Regular Expression Complexity](https://cwe.mitre.org/data/definitions/1333.html)
- [Cloudflare: Details of the Cloudflare outage on July 2, 2019](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)
- [Russ Cox: Regular Expression Matching Can Be Simple And Fast](https://swtch.com/~rsc/regexp/regexp1.html)
- [Ruby 3.2.0: Regexp improvements against ReDoS](https://www.ruby-lang.org/en/news/2022/12/25/ruby-3-2-0-released/)
- [Microsoft: Best practices for regular expressions in .NET](https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex)
