#!/usr/bin/env python3
"""
Format markdown linting output for better readability in PR comments.

This script parses the raw markdownlint-cli2 output and formats it as
user-friendly markdown with proper structure and visual hierarchy.
"""

import re
import sys
from typing import List, Dict, Optional, Tuple


def read_lint_file(filepath: str = 'lint.txt') -> str:
    """
    Read the lint output file.
    
    Args:
        filepath: Path to the lint output file
        
    Returns:
        Content of the lint file
    """
    with open(filepath, 'r') as f:
        return f.read()


def parse_error_line(line: str) -> Optional[Dict[str, str]]:
    """
    Parse a single error line from markdownlint output.
    
    Args:
        line: A line from the linter output
        
    Returns:
        Dictionary with error details or None if not an error line
    """
    match = re.search(r':(\d+)(?::(\d+))?\s+error\s+(MD\d+/[\w\-]+)\s+(.+)$', line)
    if match:
        return {
            'line': match.group(1),
            'col': match.group(2),
            'rule': match.group(3),
            'message': match.group(4)
        }
    return None


def extract_error_count(line: str) -> int:
    """
    Extract error count from a Summary line.
    
    Args:
        line: A Summary line from linter output
        
    Returns:
        Number of errors found, or 0 if not found
    """
    match = re.search(r'(\d+)\s+error', line)
    return int(match.group(1)) if match else 0


def parse_lint_output(content: str) -> Tuple[List[Dict], int]:
    """
    Parse the linter output and extract file blocks and error counts.
    
    Args:
        content: Raw linter output content
        
    Returns:
        Tuple of (file_blocks, total_error_count)
    """
    lines = content.strip().split('\n')
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
            if line.startswith('Summary:'):
                total_error_count += extract_error_count(line)
            i += 1
            continue
        
        # Parse error line
        if line.strip():
            error = parse_error_line(line)
            if error:
                current_errors.append(error)
        
        i += 1
    
    # Save last file block
    if current_file and current_errors:
        file_blocks.append({
            'file': current_file,
            'errors': current_errors,
            'count': len(current_errors)
        })
    
    return file_blocks, total_error_count


def format_error_line(error: Dict[str, str]) -> str:
    """
    Format a single error as a markdown list item.
    
    Args:
        error: Dictionary containing error details
        
    Returns:
        Formatted error line
    """
    line_info = f"Line {error['line']}"
    if error['col']:
        line_info += f":{error['col']}"
    return f"- **{line_info}** - `{error['rule']}`: {error['message']}"


def format_file_block(block: Dict) -> str:
    """
    Format a file block with its errors.
    
    Args:
        block: Dictionary containing file path and errors
        
    Returns:
        Formatted file block as markdown
    """
    output = []
    output.append(f"### `{block['file']}`\n")
    output.append(f"**Errors:** {block['count']}\n")
    
    for error in block['errors']:
        output.append(format_error_line(error))
    
    output.append("")  # Extra newline between files
    return '\n'.join(output)


def generate_formatted_output(file_blocks: List[Dict], total_error_count: int) -> str:
    """
    Generate the complete formatted markdown output.
    
    Args:
        file_blocks: List of file blocks with errors
        total_error_count: Total number of errors across all files (from Summary lines)
        
    Returns:
        Formatted markdown output
    """
    output = []
    output.append("## 📝 Markdown Linting Issues\n")
    
    # Compute actual total from file_blocks as fallback if Summary parsing failed
    actual_total = sum(block['count'] for block in file_blocks)
    display_total = actual_total if actual_total > 0 else total_error_count
    
    if display_total > 0:
        output.append(f"**Total Errors:** {display_total}\n")
    
    for block in file_blocks:
        output.append(format_file_block(block))
    
    output.append("---")
    output.append("*Please fix these issues before merging. See [.markdownlint.json](.github/configs/.markdownlint.json) for project style rules.*")
    
    return '\n'.join(output)


def generate_fallback_output(lines: List[str]) -> str:
    """
    Generate fallback output when parsing fails.
    
    Args:
        lines: Raw output lines
        
    Returns:
        Fallback formatted output
    """
    output = []
    output.append("### Raw Output\n")
    output.append("```")
    
    for line in lines:
        if not any(line.startswith(prefix) for prefix in ['markdownlint-cli2', 'Finding:', 'Linting:', 'Summary:']):
            output.append(line)
    
    output.append("```\n")
    return '\n'.join(output)


def main():
    """Parse lint.txt and generate formatted markdown output."""
    try:
        content = read_lint_file()
        
        if not content.strip():
            print("**No linting issues found.**")
            sys.exit(0)
        
        file_blocks, total_error_count = parse_lint_output(content)
        
        if file_blocks:
            output = generate_formatted_output(file_blocks, total_error_count)
            print(output)
        elif content.strip():
            # Fallback if no errors were parsed but content exists
            lines = content.strip().split('\n')
            print(generate_fallback_output(lines))
        
    except Exception as e:
        # Fallback to simple output if parsing fails
        print("**The following issues were identified:**\n")
        try:
            content = read_lint_file()
            print(content)
        except Exception:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
