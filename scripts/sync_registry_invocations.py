#!/usr/bin/env python3
"""
Sync registry YAML invocation fields with marketplace.json plugin names.

This script reads marketplace.json (source of truth) and updates all registry
YAML files so their `invocation` fields match the actual plugin:skill format.

Usage:
    python scripts/sync_registry_invocations.py
    python scripts/sync_registry_invocations.py --dry-run
"""

import json
import re
import sys
from pathlib import Path

def load_marketplace_mappings(marketplace_path: Path) -> dict[str, str]:
    """Load skill -> plugin:skill mappings from marketplace.json."""
    with open(marketplace_path) as f:
        data = json.load(f)

    mappings = {}
    for plugin in data.get('plugins', []):
        plugin_name = plugin['name']
        for skill_path in plugin.get('skills', []):
            # Extract skill name from path like "./skills/theming-components"
            skill_name = skill_path.replace('./skills/', '')
            invocation = f"{plugin_name}:{skill_name}"
            mappings[skill_name] = invocation

    return mappings

def update_registry_file(registry_path: Path, mappings: dict[str, str], dry_run: bool = False) -> list[tuple[str, str, str]]:
    """Update invocation fields in a registry YAML file."""
    changes = []

    with open(registry_path, 'r') as f:
        content = f.read()

    original_content = content

    # Pattern to match skill blocks with invocation field
    # We need to find the skill name and its invocation field
    skill_pattern = re.compile(r'^  (\S+):\s*\n((?:    .*\n)*)', re.MULTILINE)
    invocation_pattern = re.compile(r'(    invocation: ["\'])([^"\']+)(["\'])')

    def replace_invocation(match):
        prefix = match.group(1)
        old_invocation = match.group(2)
        suffix = match.group(3)

        # Extract skill name from old invocation
        if ':' in old_invocation:
            skill_name = old_invocation.split(':')[1]
        else:
            skill_name = old_invocation

        # Look up correct invocation
        if skill_name in mappings:
            new_invocation = mappings[skill_name]
            if old_invocation != new_invocation:
                changes.append((registry_path.name, old_invocation, new_invocation))
            return f'{prefix}{new_invocation}{suffix}'

        return match.group(0)

    content = invocation_pattern.sub(replace_invocation, content)

    if content != original_content and not dry_run:
        with open(registry_path, 'w') as f:
            f.write(content)

    return changes

def main():
    dry_run = '--dry-run' in sys.argv

    # Find paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Try multiple locations for marketplace.json
    marketplace_paths = [
        repo_root / '.claude-plugin' / 'marketplace.json',
        Path.home() / '.claude' / 'plugins' / 'marketplaces' / 'ai-design-components' / '.claude-plugin' / 'marketplace.json',
    ]

    marketplace_path = None
    for p in marketplace_paths:
        if p.exists():
            marketplace_path = p
            break

    if not marketplace_path:
        print("ERROR: Could not find marketplace.json")
        sys.exit(1)

    print(f"Using marketplace.json from: {marketplace_path}")

    # Load mappings
    mappings = load_marketplace_mappings(marketplace_path)
    print(f"Loaded {len(mappings)} skill mappings")

    # Find registry files
    registry_dirs = [
        repo_root / '.claude-commands' / 'skillchain-data' / 'registries',
        Path.home() / '.claude' / 'skillchain-data' / 'registries',
    ]

    all_changes = []

    for registry_dir in registry_dirs:
        if not registry_dir.exists():
            continue

        print(f"\nProcessing registries in: {registry_dir}")

        for registry_file in registry_dir.glob('*.yaml'):
            if registry_file.name == '_index.yaml':
                continue

            changes = update_registry_file(registry_file, mappings, dry_run)
            all_changes.extend(changes)

    # Report changes
    if all_changes:
        print(f"\n{'Would update' if dry_run else 'Updated'} {len(all_changes)} invocations:")
        for file, old, new in all_changes:
            print(f"  {file}: {old} → {new}")
    else:
        print("\nNo changes needed - all invocations match marketplace.json")

    if dry_run and all_changes:
        print("\nRun without --dry-run to apply changes")

if __name__ == '__main__':
    main()
