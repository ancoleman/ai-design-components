#!/usr/bin/env python3
"""
Rename skills to use gerund naming convention.
Updates directories, frontmatter, and all references.
"""

import os
import re
import json
from pathlib import Path

# Mapping of old names to new gerund names
RENAMES = {
    # API & Design
    "designing-apis": "designing-apis",
    "implementing-api-patterns": "implementing-api-patterns",
    "designing-sdks": "designing-sdks",

    # Security
    "securing-authentication": "securing-authentication",
    "architecting-security": "architecting-security",
    "managing-vulnerabilities": "managing-vulnerabilities",
    "implementing-compliance": "implementing-compliance",

    # Cloud Providers
    "deploying-on-aws": "deploying-on-aws",
    "deploying-on-azure": "deploying-on-azure",
    "deploying-on-gcp": "deploying-on-gcp",

    # Infrastructure & Operations
    "managing-configuration": "managing-configuration",
    "writing-infrastructure-code": "writing-infrastructure-code",
    "operating-kubernetes": "operating-kubernetes",
    "administering-linux": "administering-linux",
    "planning-disaster-recovery": "planning-disaster-recovery",
    "managing-incidents": "managing-incidents",
    "implementing-service-mesh": "implementing-service-mesh",
    "architecting-networks": "architecting-networks",

    # Data
    "architecting-data": "architecting-data",
    "transforming-data": "transforming-data",
    "using-document-databases": "using-document-databases",
    "using-graph-databases": "using-graph-databases",
    "using-relational-databases": "using-relational-databases",
    "using-timeseries-databases": "using-timeseries-databases",
    "using-vector-databases": "using-vector-databases",
    "optimizing-sql": "optimizing-sql",

    # DevOps & Workflows
    "managing-git-workflows": "managing-git-workflows",
    "implementing-gitops": "implementing-gitops",
    "managing-dns": "managing-dns",
    "optimizing-costs": "optimizing-costs",

    # ML/AI
    "evaluating-llms": "evaluating-llms",
    "implementing-mlops": "implementing-mlops",

    # Misc
    "generating-documentation": "generating-documentation",
    "using-message-queues": "using-message-queues",
    "implementing-observability": "implementing-observability",
    "implementing-realtime-sync": "implementing-realtime-sync",
}


def update_file_content(file_path: Path, renames: dict) -> int:
    """Update all references in a file. Returns count of changes."""
    try:
        content = file_path.read_text()
    except Exception:
        return 0

    original = content
    changes = 0

    for old_name, new_name in renames.items():
        # Match the old name as a whole word/path component
        # Handles: skills/old-name, "old-name", 'old-name', /old-name/, old-name/
        patterns = [
            (f'skills/{old_name}', f'skills/{new_name}'),
            (f'"{old_name}"', f'"{new_name}"'),
            (f"'{old_name}'", f"'{new_name}'"),
            (f'/{old_name}/', f'/{new_name}/'),
            (f'{old_name}/', f'{new_name}/'),
            (f'name: {old_name}', f'name: {new_name}'),
        ]

        for old_pattern, new_pattern in patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes += 1

    if content != original:
        file_path.write_text(content)

    return changes


def update_frontmatter_name(skill_path: Path, new_name: str) -> bool:
    """Update the name field in SKILL.md frontmatter."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False

    content = skill_md.read_text()

    # Update name in frontmatter
    new_content = re.sub(
        r'^(name:\s*)[\w-]+',
        f'\\1{new_name}',
        content,
        count=1,
        flags=re.MULTILINE
    )

    if new_content != content:
        skill_md.write_text(new_content)
        return True
    return False


def main():
    import sys

    dry_run = '--dry-run' in sys.argv
    skills_dir = Path('skills')

    if not skills_dir.exists():
        print("Error: skills/ directory not found")
        sys.exit(1)

    print(f"{'DRY RUN - ' if dry_run else ''}Renaming {len(RENAMES)} skills to gerund form\n")

    # Step 1: Rename directories
    print("Step 1: Renaming directories...")
    renamed = []
    for old_name, new_name in RENAMES.items():
        old_path = skills_dir / old_name
        new_path = skills_dir / new_name

        if old_path.exists():
            if dry_run:
                print(f"  Would rename: {old_name} → {new_name}")
            else:
                old_path.rename(new_path)
                print(f"  Renamed: {old_name} → {new_name}")
            renamed.append((old_name, new_name))
        elif new_path.exists():
            print(f"  Already renamed: {new_name}")
        else:
            print(f"  Not found: {old_name}")

    print(f"\n  Renamed {len(renamed)} directories")

    # Step 2: Update frontmatter in renamed skills
    print("\nStep 2: Updating SKILL.md frontmatter...")
    for old_name, new_name in renamed:
        new_path = skills_dir / new_name
        if not dry_run and new_path.exists():
            if update_frontmatter_name(new_path, new_name):
                print(f"  Updated frontmatter: {new_name}")

    # Step 3: Update all references in the codebase
    print("\nStep 3: Updating references in codebase...")

    # Files to update
    files_to_update = []

    # All markdown files
    files_to_update.extend(Path('.').glob('**/*.md'))

    # JSON files
    files_to_update.extend(Path('.').glob('**/*.json'))

    # YAML files
    files_to_update.extend(Path('.').glob('**/*.yaml'))
    files_to_update.extend(Path('.').glob('**/*.yml'))

    # Python files
    files_to_update.extend(Path('.').glob('**/*.py'))

    # TypeScript/JavaScript
    files_to_update.extend(Path('.').glob('**/*.ts'))
    files_to_update.extend(Path('.').glob('**/*.tsx'))
    files_to_update.extend(Path('.').glob('**/*.js'))

    total_changes = 0
    files_changed = 0

    for file_path in files_to_update:
        # Skip node_modules, .git, etc
        if any(part.startswith('.') or part == 'node_modules' for part in file_path.parts):
            continue

        if dry_run:
            continue

        changes = update_file_content(file_path, RENAMES)
        if changes > 0:
            total_changes += changes
            files_changed += 1
            print(f"  Updated: {file_path} ({changes} changes)")

    print(f"\n  Updated {files_changed} files with {total_changes} changes")

    # Summary
    print(f"\n{'Would rename' if dry_run else 'Renamed'} {len(renamed)} skills")
    if not dry_run:
        print("\nNext steps:")
        print("  1. Run validation: python -m scripts.validation ci")
        print("  2. Review changes: git diff")
        print("  3. Test documentation site")


if __name__ == '__main__':
    main()
