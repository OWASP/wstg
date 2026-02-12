# Workflow Scripts

This directory contains helper scripts used by GitHub Actions workflows.

## Scripts

### format_lint_output.py

Formats markdown linting output for better readability in PR comments.

**Input:** Reads from `lint.txt` (raw markdownlint-cli2 output) in the current working directory  
**Output:** Writes formatted markdown to stdout

**Features:**
- Removes redundant metadata (version info, "Finding:", "Linting:", "Summary:")
- Groups errors by file with proper markdown formatting
- Shows file paths as section headers instead of repeating for each error
- Uses bullet points with line numbers, rule codes, and descriptions
- Includes total error count and helpful footer with link to config
- Graceful fallback to raw output if parsing fails

**Usage:**

From the repository root (where `lint.txt` is generated):
```bash
python3 .github/workflows/scripts/format_lint_output.py > artifact.txt
```

Or from within the workflow (with base checkout):
```bash
python3 base/.github/workflows/scripts/format_lint_output.py > artifact.txt
```
