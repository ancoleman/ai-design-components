#!/usr/bin/env python3
"""
Fix incorrect skill invocations across blueprints and orchestrators.

Maps incorrect/outdated skill names to their correct marketplace.json equivalents.
"""

import os
import re
import sys
from pathlib import Path

# Mapping of incorrect invocations to correct ones
# Format: "wrong" -> "correct"
CORRECTIONS = {
    # Backend API skills
    "backend-api-skills:api-patterns": "backend-api-skills:implementing-api-patterns",
    "api-patterns": "implementing-api-patterns",

    # Backend data skills
    "backend-data-skills:databases-relational": "backend-data-skills:using-relational-databases",
    "databases-relational": "using-relational-databases",

    # Backend platform skills
    "backend-platform-skills:auth-security": "backend-platform-skills:securing-authentication",
    "backend-platform-skills:observability": "backend-platform-skills:implementing-observability",
    "backend-platform-skills:implementing-auth": "backend-platform-skills:securing-authentication",
    "auth-security": "securing-authentication",
    "implementing-auth": "securing-authentication",

    # DevOps skills - remove non-existent ones
    "devops-skills:deploying-containers": "devops-skills:writing-dockerfiles",
    "devops-skills:managing-infrastructure": "infrastructure-skills:writing-infrastructure-code",
    "deploying-containers": "writing-dockerfiles",
    "managing-infrastructure": "writing-infrastructure-code",

    # Security skills
    "security-skills:managing-secrets": "data-engineering-skills:secret-management",
    "security-skills:securing-apis": "security-skills:architecting-security",
    "managing-secrets": "secret-management",
    "securing-apis": "architecting-security",

    # Cloud provider skills
    "cloud-provider-skills:managing-cloud-resources": "cloud-provider-skills:deploying-on-aws",
    "managing-cloud-resources": "deploying-on-aws",

    # Data engineering skills
    "data-engineering-skills:orchestrating-workflows": "data-engineering-skills:transforming-data",
    "data-engineering-skills:managing-databases": "backend-data-skills:using-relational-databases",
    "orchestrating-workflows": "transforming-data",
    "managing-databases": "using-relational-databases",

    # AI/ML skills
    "ai-ml-skills:building-rag-systems": "backend-ai-skills:ai-data-engineering",
    "ai-ml-skills:deploying-models": "backend-ai-skills:model-serving",
    "ai-ml-skills:monitoring-ml": "ai-ml-skills:implementing-mlops",
    "building-rag-systems": "ai-data-engineering",
    "deploying-models": "model-serving",
    "monitoring-ml": "implementing-mlops",

    # Developer productivity
    "developer-productivity-skills:configuring-development": "developer-productivity-skills:debugging-techniques",
    "developer-productivity-skills:testing-strategies": "devops-skills:testing-strategies",
    "developer-productivity-skills:debugging-applications": "developer-productivity-skills:debugging-techniques",
    "configuring-development": "debugging-techniques",
    "debugging-applications": "debugging-techniques",

    # FinOps skills
    "finops-skills:tracking-budgets": "finops-skills:optimizing-costs",
    "finops-skills:implementing-tagging": "finops-skills:resource-tagging",
    "tracking-budgets": "optimizing-costs",
    "implementing-tagging": "resource-tagging",
}

def fix_file(filepath: Path, dry_run: bool = False) -> list:
    """Fix skill invocations in a file."""
    changes = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return changes

    original = content

    # Apply corrections
    for wrong, correct in CORRECTIONS.items():
        if wrong in content:
            # Count occurrences
            count = content.count(wrong)
            if count > 0:
                content = content.replace(wrong, correct)
                changes.append((wrong, correct, count))

    # Write if changed
    if content != original and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

def main():
    dry_run = '--dry-run' in sys.argv

    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Directories to fix
    dirs_to_check = [
        repo_root / '.claude-commands' / 'skillchain' / 'blueprints',
        repo_root / '.claude-commands' / 'skillchain' / 'categories',
        repo_root / '.claude-commands' / 'skillchain-data' / 'registries',
        repo_root / '.claude-commands' / 'skillchain-data' / 'shared',
    ]

    all_changes = []
    files_changed = 0

    for dir_path in dirs_to_check:
        if not dir_path.exists():
            continue

        print(f"\nChecking: {dir_path}")

        for filepath in dir_path.glob('*.md'):
            changes = fix_file(filepath, dry_run)
            if changes:
                files_changed += 1
                print(f"  {filepath.name}:")
                for wrong, correct, count in changes:
                    print(f"    {wrong} -> {correct} ({count}x)")
                    all_changes.append((filepath.name, wrong, correct, count))

        for filepath in dir_path.glob('*.yaml'):
            changes = fix_file(filepath, dry_run)
            if changes:
                files_changed += 1
                print(f"  {filepath.name}:")
                for wrong, correct, count in changes:
                    print(f"    {wrong} -> {correct} ({count}x)")
                    all_changes.append((filepath.name, wrong, correct, count))

    # Summary
    print(f"\n{'Would fix' if dry_run else 'Fixed'} {len(all_changes)} issues in {files_changed} files")

    if dry_run and all_changes:
        print("\nRun without --dry-run to apply changes")

if __name__ == '__main__':
    main()
