# Test Scenario Template

This area provides an [example template](999-Foo_Testing/1-Testing_for_a_Cat_in_a_Box.md) and [explanation of that template](999-Foo_Testing/2-Template_Explanation.md) for use in developing guide content. (They are based on fake chapter `999`.)

## Formatting Examples

This folder also shows how to format specific types of content:

- [HTTP Requests and Responses](999-Foo_Testing/3-Format_for_HTTP_Request_Response.md)

## Merged or Removed Tests

Tests that are merged into another test, or removed entirely, are retired by replacing the file content with a short placeholder page. The placeholder keeps the ID and title visible so references to the old test can be traced.

### Merged

Use when the content now lives in another test.

```markdown
# Original Title

|ID          |
|------------|
|WSTG-XXXX-NN|

This content has been merged into: [Destination Title](relative/path/to/Destination.md)

[merged]: # (WSTG-YYYY-MM)
```

- The sentence is `This content has been merged into: [Destination Title](relative/link.md)`.
- The final line is the reference-style metadata marker `[merged]: # (WSTG-YYYY-MM)`, where `WSTG-YYYY-MM` is the destination test ID. It is render-safe and machine-readable.

### Removed

Use when the content is retired with no replacement.

```markdown
# Original Title

|ID          |
|------------|
|WSTG-XXXX-NN|

This content has been removed.
```

- The final non-blank line is exactly `This content has been removed.` (the checklist generator in `.github/json/scripts/generate_checklist_json.py` detects removed pages by this line).
- No `[merged]` marker is used.

### Notes

- Placeholder pages are a stopgap: they should be deleted, and the remaining tests renumbered, at the next renumbering pass (for example, when preparing a new WSTG release).
- Update inbound links to point at the destination test (merged) or drop them (removed).
