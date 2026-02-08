#!/usr/bin/env python3
"""
Format markdown linting output for better readability in PR comments.

This script parses the raw markdownlint-cli2 output and formats it as
user-friendly markdown with proper structure and visual hierarchy.
"""

import re
import sys


def main():
    """Parse lint.txt and generate formatted markdown output."""
    try:
        with open('lint.txt', 'r') as f:
            content = f.read()
        
        if not content.strip():
            print("**No linting issues found.**")
            sys.exit(0)
        
        # Parse the linter output - can contain multiple files
        lines = content.strip().split('\n')
        
        # Collect all file blocks
        file_blocks = []
        current_file = None
        current_errors = []
        total_error_count = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip version line
            if line.startswith('markdownlint-cli2'):
                i += 1
                continue
            
            # New file block
            if line.startswith('Finding:'):
                # Save previous file block if exists
                if current_file and current_errors:
                    file_blocks.append({
                        'file': current_file,
                        'errors': current_errors,
                        'count': len(current_errors)
                    })
                
                current_file = line.replace('Finding:', '').strip()
                current_errors = []
                i += 1
                continue
            
            # Skip metadata lines
            if line.startswith('Linting:') or line.startswith('Summary:'):
                # Extract error count from Summary line
                if line.startswith('Summary:'):
                    match = re.search(r'(\d+)\s+error', line)
                    if match:
                        total_error_count += int(match.group(1))
                i += 1
                continue
            
            # Parse error line
            if line.strip():
                match = re.search(r':(\d+)(?::(\d+))?\s+error\s+(MD\d+/[\w\-]+)\s+(.+)$', line)
                if match:
                    current_errors.append({
                        'line': match.group(1),
                        'col': match.group(2),
                        'rule': match.group(3),
                        'message': match.group(4)
                    })
            
            i += 1
        
        # Save last file block
        if current_file and current_errors:
            file_blocks.append({
                'file': current_file,
                'errors': current_errors,
                'count': len(current_errors)
            })
        
        # Generate formatted output
        print("## 📝 Markdown Linting Issues\n")
        
        if total_error_count > 0:
            print(f"**Total Errors:** {total_error_count}\n")
        
        # Display each file block
        for block in file_blocks:
            print(f"### `{block['file']}`\n")
            print(f"**Errors:** {block['count']}\n")
            for error in block['errors']:
                line_info = f"Line {error['line']}"
                if error['col']:
                    line_info += f":{error['col']}"
                print(f"- **{line_info}** - `{error['rule']}`: {error['message']}")
            print()  # Extra newline between files
        
        # Fallback if no errors were parsed but content exists
        if not file_blocks and content.strip():
            print("### Raw Output\n")
            print("```")
            for line in lines:
                if not any(line.startswith(prefix) for prefix in ['markdownlint-cli2', 'Finding:', 'Linting:', 'Summary:']):
                    print(line)
            print("```\n")
        
        print("---")
        print("*Please fix these issues before merging. See [.markdownlint.json](.github/configs/.markdownlint.json) for project style rules.*")
        
    except Exception as e:
        # Fallback to simple output if parsing fails
        print("**The following issues were identified:**\n")
        try:
            with open('lint.txt', 'r') as f:
                print(f.read())
        except Exception:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
