#!/usr/bin/env python3
"""
Update GitHub Pages documentation with gerund skill names.
Handles sidebars.ts, markdown files, and cross-references.
"""

import os
import re
from pathlib import Path

# Complete mapping of old names to new gerund names
RENAMES = {
    # Infrastructure
    "kubernetes-operations": "operating-kubernetes",
    "infrastructure-as-code": "writing-infrastructure-code",
    "linux-administration": "administering-linux",
    "network-architecture": "architecting-networks",
    "disaster-recovery": "planning-disaster-recovery",
    "service-mesh": "implementing-service-mesh",
    "configuration-management": "managing-configuration",
    "dns-management": "managing-dns",

    # Security
    "security-architecture": "architecting-security",
    "compliance-frameworks": "implementing-compliance",
    "vulnerability-management": "managing-vulnerabilities",

    # DevOps
    "gitops-workflows": "implementing-gitops",
    "incident-management": "managing-incidents",

    # Developer Productivity
    "api-design-principles": "designing-apis",
    "sdk-design": "designing-sdks",
    "documentation-generation": "generating-documentation",
    "git-workflows": "managing-git-workflows",

    # Data
    "data-architecture": "architecting-data",
    "data-transformation": "transforming-data",
    "sql-optimization": "optimizing-sql",

    # AI/ML
    "mlops-patterns": "implementing-mlops",
    "llm-evaluation": "evaluating-llms",

    # Cloud
    "aws-patterns": "deploying-on-aws",
    "gcp-patterns": "deploying-on-gcp",
    "azure-patterns": "deploying-on-azure",

    # FinOps
    "cost-optimization": "optimizing-costs",

    # Backend skills (sidebar paths)
    "api-patterns": "implementing-api-patterns",
    "databases-relational": "using-relational-databases",
    "databases-vector": "using-vector-databases",
    "databases-timeseries": "using-timeseries-databases",
    "databases-document": "using-document-databases",
    "databases-graph": "using-graph-databases",
    "message-queues": "using-message-queues",
    "realtime-sync": "implementing-realtime-sync",
    "observability": "implementing-observability",
    "auth-security": "securing-authentication",
}

# Also fix duplicate prefixes from previous rename bugs
DUPLICATE_FIXES = {
    "planning-planning-disaster-recovery": "planning-disaster-recovery",
    "implementing-implementing-service-mesh": "implementing-service-mesh",
    "implementing-implementing-api-patterns": "implementing-api-patterns",
    "implementing-implementing-realtime-sync": "implementing-realtime-sync",
    "implementing-implementing-observability": "implementing-observability",
    "implementing-implementing-gitops": "implementing-gitops",
    "implementing-implementing-mlops": "implementing-mlops",
    "implementing-implementing-compliance": "implementing-compliance",
    "implementing-implementing-tls": "implementing-tls",
    "using-using-relational-databases": "using-relational-databases",
    "using-using-vector-databases": "using-vector-databases",
    "using-using-timeseries-databases": "using-timeseries-databases",
    "using-using-document-databases": "using-document-databases",
    "using-using-graph-databases": "using-graph-databases",
    "using-using-message-queues": "using-message-queues",
    "managing-managing-vulnerabilities": "managing-vulnerabilities",
    "managing-managing-incidents": "managing-incidents",
    "managing-managing-configuration": "managing-configuration",
    "managing-managing-dns": "managing-dns",
    "managing-managing-git-workflows": "managing-git-workflows",
    "architecting-architecting-security": "architecting-security",
    "architecting-architecting-networks": "architecting-networks",
    "architecting-architecting-data": "architecting-data",
    "designing-designing-apis": "designing-apis",
    "designing-designing-sdks": "designing-sdks",
    "generating-generating-documentation": "generating-documentation",
    "operating-operating-kubernetes": "operating-kubernetes",
    "writing-writing-infrastructure-code": "writing-infrastructure-code",
    "administering-administering-linux": "administering-linux",
    "transforming-transforming-data": "transforming-data",
    "optimizing-optimizing-sql": "optimizing-sql",
    "optimizing-optimizing-costs": "optimizing-costs",
    "evaluating-evaluating-llms": "evaluating-llms",
    "deploying-deploying-on-aws": "deploying-on-aws",
    "deploying-deploying-on-gcp": "deploying-on-gcp",
    "deploying-deploying-on-azure": "deploying-on-azure",
    "securing-securing-authentication": "securing-authentication",
}


def update_file(file_path: Path, dry_run: bool = False) -> tuple[int, list[str]]:
    """Update a file with new skill names. Returns (change_count, changes_list)."""
    try:
        content = file_path.read_text()
    except Exception as e:
        return 0, [f"Error reading: {e}"]

    original = content
    changes = []

    # First fix any duplicate prefixes
    for old, new in DUPLICATE_FIXES.items():
        if old in content:
            content = content.replace(old, new)
            changes.append(f"Fixed duplicate: {old} -> {new}")

    # Then apply renames
    for old_name, new_name in RENAMES.items():
        # Different patterns to match
        patterns = [
            # Sidebar paths: 'master-plans/xxx/old-name' or 'skills/backend/old-name'
            (f"'{old_name}'", f"'{new_name}'"),
            (f'"{old_name}"', f'"{new_name}"'),

            # Markdown links: ./old-name or (./old-name)
            (f"./{old_name})", f"./{new_name})"),
            (f"./{old_name}]", f"./{new_name}]"),

            # Backtick references: `old-name`
            (f"`{old_name}`", f"`{new_name}`"),

            # Path segments in URLs
            (f"/{old_name}/", f"/{new_name}/"),
            (f"/{old_name})", f"/{new_name})"),

            # Sidebar path segments
            (f"/{old_name}',", f"/{new_name}',"),
            (f"/{old_name}\"", f"/{new_name}\""),

            # Plain text references (more careful - only at word boundaries)
        ]

        for old_pattern, new_pattern in patterns:
            if old_pattern in content:
                count = content.count(old_pattern)
                content = content.replace(old_pattern, new_pattern)
                changes.append(f"{old_pattern} -> {new_pattern} ({count}x)")

    if content != original and not dry_run:
        file_path.write_text(content)

    return len(changes), changes


def main():
    import sys

    dry_run = '--dry-run' in sys.argv
    pages_dir = Path('pages')

    if not pages_dir.exists():
        print("Error: pages/ directory not found")
        sys.exit(1)

    print(f"{'DRY RUN - ' if dry_run else ''}Updating GitHub Pages documentation\n")

    # Files to update
    files_to_update = []

    # TypeScript files (sidebars)
    files_to_update.extend(pages_dir.glob('*.ts'))
    files_to_update.extend(pages_dir.glob('*.tsx'))

    # All markdown files
    files_to_update.extend(pages_dir.glob('**/*.md'))
    files_to_update.extend(pages_dir.glob('**/*.mdx'))

    # JSON files
    files_to_update.extend(pages_dir.glob('**/*.json'))

    total_changes = 0
    files_changed = 0

    for file_path in sorted(files_to_update):
        # Skip node_modules
        if 'node_modules' in str(file_path):
            continue

        change_count, changes = update_file(file_path, dry_run=dry_run)
        if change_count > 0:
            files_changed += 1
            total_changes += change_count
            print(f"\n{file_path.relative_to(pages_dir)}:")
            for change in changes[:10]:  # Limit output
                print(f"  {change}")
            if len(changes) > 10:
                print(f"  ... and {len(changes) - 10} more changes")

    print(f"\n{'Would update' if dry_run else 'Updated'} {files_changed} files with {total_changes} changes")

    if not dry_run:
        print("\nNext steps:")
        print("  1. Review changes: git diff pages/")
        print("  2. Test build: cd pages && npm run build")
        print("  3. Run validation: python -m scripts.validation ci")


if __name__ == '__main__':
    main()
