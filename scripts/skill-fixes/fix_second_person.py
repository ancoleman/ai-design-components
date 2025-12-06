#!/usr/bin/env python3
"""
Fix second person (you/your) usage in SKILL.md files.
Only fixes instructional text, not code examples.
"""

import re
from pathlib import Path

# Replacements for common "your" patterns in instructional text
REPLACEMENTS = [
    # Common patterns - order matters (more specific first)
    (r'\bfor your use case\b', 'for the use case'),
    (r'\bmatching your needs\b', 'matching the requirements'),
    (r'\bmatching your use case\b', 'matching the use case'),
    (r'\byour specific needs\b', 'specific requirements'),
    (r'\byour data volume\b', 'the data volume'),
    (r'\byour data source\b', 'the data source'),
    (r'\byour project requirements\b', 'project requirements'),
    (r'\byour project\b', 'the project'),
    (r'\byour use case\b', 'the use case'),
    (r'\byour content type\b', 'the content type'),
    (r'\byour information architecture\b', 'the information architecture'),
    (r'\byour user journey\b', 'the user journey'),
    (r'\byour media type\b', 'the media type'),
    (r'\byour deployment\b', 'the deployment'),
    (r'\byour dashboard\b', 'dashboard'),
    (r'\byour systems\b', 'systems'),
    (r'\byour server\b', 'the server'),
    (r'\byour app\b', 'the app'),
    (r'\bbased on your\b', 'based on'),
    (r'\bbenefits your\b', 'benefits the'),
    (r'\banalyze your\b', 'analyze'),
    (r'\boptimize your\b', 'optimize'),
    (r'\bmeasure your\b', 'measure'),
    (r'\bIdentify your\b', 'Identify the'),
    (r'\bDetermine your\b', 'Determine'),
    (r'\bAnalyze your\b', 'Analyze'),
    (r'\bMap your\b', 'Map the'),
]


def is_in_code_block(content: str, pos: int) -> bool:
    """Check if position is inside a code block."""
    # Count ``` before this position
    before = content[:pos]
    code_block_count = before.count('```')
    return code_block_count % 2 == 1


def is_in_inline_code(line: str, match_start: int) -> bool:
    """Check if match is inside inline code `...`."""
    # Count backticks before match position in the line
    before = line[:match_start]
    backtick_count = before.count('`')
    return backtick_count % 2 == 1


def fix_file(file_path: Path, dry_run: bool = False) -> list[str]:
    """Fix second person usage in a file. Returns list of changes made."""
    content = file_path.read_text()
    changes = []

    for pattern, replacement in REPLACEMENTS:
        # Find all matches
        for match in re.finditer(pattern, content, re.IGNORECASE):
            pos = match.start()

            # Skip if in code block
            if is_in_code_block(content, pos):
                continue

            # Get the line for inline code check
            line_start = content.rfind('\n', 0, pos) + 1
            line_end = content.find('\n', pos)
            if line_end == -1:
                line_end = len(content)
            line = content[line_start:line_end]
            match_in_line = pos - line_start

            # Skip if in inline code
            if is_in_inline_code(line, match_in_line):
                continue

            # Skip if line starts with common code indicators
            line_stripped = line.strip()
            if any(line_stripped.startswith(x) for x in ['#', '//', '/*', '*', '-', '|', '>']):
                # But allow markdown headers
                if not line_stripped.startswith('## ') and not line_stripped.startswith('### '):
                    continue

            # Record the change
            original = match.group(0)
            # Preserve case of first letter
            if original[0].isupper():
                new_text = replacement[0].upper() + replacement[1:]
            else:
                new_text = replacement

            changes.append(f"  Line ~{content[:pos].count(chr(10))+1}: '{original}' → '{new_text}'")

    if changes and not dry_run:
        # Apply replacements
        new_content = content
        for pattern, replacement in REPLACEMENTS:
            def replace_if_not_code(m):
                pos = m.start()
                if is_in_code_block(content, pos):
                    return m.group(0)

                line_start = content.rfind('\n', 0, pos) + 1
                line = content[line_start:content.find('\n', pos)]
                if is_in_inline_code(line, pos - line_start):
                    return m.group(0)

                line_stripped = line.strip()
                if any(line_stripped.startswith(x) for x in ['#', '//', '/*', '*', '-', '|', '>']):
                    if not line_stripped.startswith('## ') and not line_stripped.startswith('### '):
                        return m.group(0)

                original = m.group(0)
                if original[0].isupper():
                    return replacement[0].upper() + replacement[1:]
                return replacement

            new_content = re.sub(pattern, replace_if_not_code, new_content, flags=re.IGNORECASE)

        file_path.write_text(new_content)

    return changes


def main():
    import sys

    dry_run = '--dry-run' in sys.argv

    skills_dir = Path('skills')
    total_changes = 0

    for skill_md in sorted(skills_dir.glob('*/SKILL.md')):
        changes = fix_file(skill_md, dry_run=dry_run)
        if changes:
            print(f"\n{skill_md.parent.name}:")
            for change in changes:
                print(change)
            total_changes += len(changes)

    print(f"\n{'Would make' if dry_run else 'Made'} {total_changes} changes")


if __name__ == '__main__':
    main()
