#!/usr/bin/env python3
"""
Automatically add Table of Contents to markdown files.

Usage:
    python scripts/add_toc.py skills/configuring-firewalls/references/ufw-patterns.md
    python scripts/add_toc.py --all  # Process all files missing TOCs
"""

import re
import sys
from pathlib import Path


def slugify(text: str) -> str:
    """Convert heading text to anchor slug."""
    # Remove special characters, lowercase, replace spaces with hyphens
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def extract_headings(content: str) -> list[tuple[int, str]]:
    """Extract headings (## and ###) from markdown content."""
    headings = []
    lines = content.split('\n')
    in_code_block = False

    for line in lines:
        # Track code blocks to skip headings inside them
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Match ## and ### headings (skip # which is title)
        match = re.match(r'^(#{2,3})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            # Skip the "Table of Contents" heading itself
            if text.lower() != 'table of contents':
                headings.append((level, text))

    return headings


def generate_toc(headings: list[tuple[int, str]]) -> str:
    """Generate markdown TOC from headings."""
    if not headings:
        return ""

    toc_lines = ["## Table of Contents", ""]

    for level, text in headings:
        indent = "  " * (level - 2)  # ## = no indent, ### = 2 spaces
        slug = slugify(text)
        toc_lines.append(f"{indent}- [{text}](#{slug})")

    toc_lines.append("")  # Trailing newline
    return '\n'.join(toc_lines)


def has_toc(content: str) -> bool:
    """Check if content already has a Table of Contents."""
    return bool(re.search(r'^## Table of Contents', content, re.MULTILINE))


def find_insertion_point(content: str) -> int:
    """Find where to insert the TOC (after title + intro paragraph)."""
    lines = content.split('\n')

    # Find the first H1 or first content
    h1_index = -1
    for i, line in enumerate(lines):
        if line.startswith('# ') and not line.startswith('##'):
            h1_index = i
            break

    if h1_index == -1:
        # No H1 found, insert at beginning
        return 0

    # Find end of intro paragraph (first blank line after H1)
    # or first ## heading, whichever comes first
    for i in range(h1_index + 1, len(lines)):
        line = lines[i].strip()

        # Skip immediately following blank lines
        if i == h1_index + 1 and not line:
            continue

        # Found start of intro paragraph, now find its end
        if line:
            # Look for end of paragraph (blank line) or next heading
            for j in range(i, len(lines)):
                next_line = lines[j].strip()
                if not next_line:
                    # Found blank line after intro
                    return sum(len(l) + 1 for l in lines[:j+1])
                if next_line.startswith('## '):
                    # Found next heading
                    return sum(len(l) + 1 for l in lines[:j])

    # Fallback: insert after H1
    return sum(len(l) + 1 for l in lines[:h1_index + 2])


def add_toc(file_path: Path) -> bool:
    """Add TOC to a markdown file. Returns True if modified."""
    content = file_path.read_text()

    # Skip if already has TOC
    if has_toc(content):
        print(f"  Skipped (already has TOC): {file_path.name}")
        return False

    # Extract headings
    headings = extract_headings(content)

    if not headings:
        print(f"  Skipped (no headings): {file_path.name}")
        return False

    # Generate TOC
    toc = generate_toc(headings)

    # Find insertion point
    insert_pos = find_insertion_point(content)

    # Insert TOC
    new_content = content[:insert_pos] + '\n' + toc + '\n' + content[insert_pos:]

    # Clean up excessive blank lines
    new_content = re.sub(r'\n{4,}', '\n\n\n', new_content)

    # Write back
    file_path.write_text(new_content)
    print(f"  Added TOC: {file_path.name}")
    return True


def get_files_needing_toc(skills_dir: Path) -> list[Path]:
    """Get all reference files that need TOCs (>100 lines, no TOC)."""
    files = []

    for ref_dir in skills_dir.glob('*/references'):
        for md_file in ref_dir.glob('*.md'):
            content = md_file.read_text()
            lines = len(content.split('\n'))

            if lines > 100 and not has_toc(content):
                files.append(md_file)

    return sorted(files)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/add_toc.py <file.md>")
        print("  python scripts/add_toc.py --all")
        print("  python scripts/add_toc.py --list")
        sys.exit(1)

    if sys.argv[1] == '--list':
        skills_dir = Path('skills')
        files = get_files_needing_toc(skills_dir)
        print(f"Found {len(files)} files needing TOCs:")
        for f in files:
            lines = len(f.read_text().split('\n'))
            print(f"  {f.relative_to(skills_dir)} ({lines} lines)")
        sys.exit(0)

    if sys.argv[1] == '--all':
        skills_dir = Path('skills')
        files = get_files_needing_toc(skills_dir)
        print(f"Processing {len(files)} files...")

        modified = 0
        for f in files:
            if add_toc(f):
                modified += 1

        print(f"\nModified {modified} files")
        sys.exit(0)

    # Single file mode
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    add_toc(file_path)


if __name__ == '__main__':
    main()
