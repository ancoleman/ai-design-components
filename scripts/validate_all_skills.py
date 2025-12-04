#!/usr/bin/env python3
"""
Batch Skill Validation Script

Validates all skills against best practices defined in validation-rules.yaml.

Usage:
    python validate_all_skills.py                    # Validate all completed
    python validate_all_skills.py --phase 1          # Validate Phase 1 skills
    python validate_all_skills.py --completed        # Only existing skills
    python validate_all_skills.py --pending          # List pending skills
    python validate_all_skills.py --list-phases      # Show phase breakdown
    python validate_all_skills.py --skill NAME       # Single skill
    python validate_all_skills.py --show-community   # Show community suggestions
    python validate_all_skills.py --preset strict    # Use strict community preset
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Import from validate_skill.py
from validate_skill import (
    Colors, ValidationResult, load_rules, validate_skill, get_default_rules
)


def get_phases(rules: dict) -> dict:
    """Extract phase definitions from rules."""
    return rules.get('phases', {})


def get_all_phase_skills(rules: dict) -> set:
    """Get all skills defined in phases."""
    phases = get_phases(rules)
    all_skills = set()
    for phase_data in phases.values():
        all_skills.update(phase_data.get('skills', []))
    return all_skills


def get_phase_skills(rules: dict, phase_num: int) -> list:
    """Get skills for a specific phase."""
    phases = get_phases(rules)
    phase_key = f'phase_{phase_num}'
    return phases.get(phase_key, {}).get('skills', [])


def get_phase_for_skill(rules: dict, skill_name: str) -> Optional[int]:
    """Find which phase a skill belongs to."""
    phases = get_phases(rules)
    for phase_key, phase_data in phases.items():
        if skill_name in phase_data.get('skills', []):
            return int(phase_key.split('_')[1])
    return None


def list_phases(rules: dict):
    """Print phase breakdown."""
    print("=" * 42)
    print("Skill Phases")
    print("=" * 42)
    print()

    phases = get_phases(rules)
    for phase_key in sorted(phases.keys()):
        phase_data = phases[phase_key]
        phase_num = phase_key.split('_')[1]
        name = phase_data.get('name', f'Phase {phase_num}')
        skills = phase_data.get('skills', [])

        print(f"{Colors.CYAN}Phase {phase_num} - {name} ({len(skills)} skills):{Colors.NC}")
        for skill in skills:
            print(f"  - {skill}")
        print()

    total = sum(len(p.get('skills', [])) for p in phases.values())
    print(f"Total new skills: {total}")


def list_pending(skills_dir: Path, rules: dict):
    """List pending skills with their phase assignments."""
    print("=" * 42)
    print("Pending Skills (init.md only, no SKILL.md)")
    print("=" * 42)
    print()

    pending = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir():
            has_init = (skill_dir / 'init.md').exists()
            has_skill = (skill_dir / 'SKILL.md').exists()

            if has_init and not has_skill:
                phase = get_phase_for_skill(rules, skill_dir.name)
                pending.append((skill_dir.name, phase))

    for skill_name, phase in pending:
        phase_label = f" (Phase {phase})" if phase else ""
        print(f"  {Colors.YELLOW}{skill_name}{Colors.NC}{phase_label}")

    print()
    print(f"Total pending: {len(pending)}")


def main():
    parser = argparse.ArgumentParser(
        description='Batch validate Claude Skills',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--phase', '-p', type=int, choices=[1, 2, 3, 4],
                        help='Validate skills in specific phase')
    parser.add_argument('--completed', '-c', action='store_true',
                        help='Only validate existing/completed skills')
    parser.add_argument('--pending', action='store_true',
                        help='List pending skills')
    parser.add_argument('--list-phases', action='store_true',
                        help='Show phase breakdown')
    parser.add_argument('--skill', '-s', type=str,
                        help='Validate single skill by name')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed output')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--rules', '-r', type=Path,
                        help='Path to validation rules YAML')
    parser.add_argument('--no-color', action='store_true',
                        help='Disable colored output')
    parser.add_argument('--show-community', action='store_true',
                        help='Show community practice suggestions')
    parser.add_argument('--no-community', action='store_true',
                        help='Skip community practice checks')
    parser.add_argument('--preset', choices=['minimal', 'standard', 'strict'],
                        help='Override community practices preset')

    args = parser.parse_args()

    if args.no_color or not sys.stdout.isatty():
        Colors.disable()

    # Determine paths
    script_dir = Path(__file__).parent
    rules_path = args.rules or (script_dir / 'validation-rules.yaml')
    skills_dir = script_dir.parent / 'skills'

    # Load rules
    rules = load_rules(rules_path)

    # Override preset if specified
    if args.preset:
        if 'community_presets' not in rules:
            rules['community_presets'] = {}
        rules['community_presets']['active_preset'] = args.preset

    # Disable community checks if requested
    if args.no_community:
        rules['community_practices'] = {}

    phase_skills = get_all_phase_skills(rules)

    # Handle list commands
    if args.list_phases:
        list_phases(rules)
        return 0

    if args.pending:
        list_pending(skills_dir, rules)
        return 0

    # Validation mode
    print("=" * 42)
    print("Batch Skill Validation")
    print("=" * 42)
    print()

    results = []
    pending_count = 0
    existing_count = 0

    # Determine skills to validate
    if args.skill:
        # Single skill
        skill_dir = skills_dir / args.skill
        if not skill_dir.exists():
            print(f"{Colors.RED}Skill not found: {args.skill}{Colors.NC}")
            return 1
        skills_to_check = [skill_dir]
        print(f"{Colors.BLUE}Validating single skill: {args.skill}{Colors.NC}")

    elif args.phase:
        # Phase-specific
        phase_skill_names = get_phase_skills(rules, args.phase)
        skills_to_check = [skills_dir / name for name in phase_skill_names]
        print(f"{Colors.BLUE}Validating Phase {args.phase} skills{Colors.NC}")

    elif args.completed:
        # Completed only - any skill with SKILL.md
        skills_to_check = []
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / 'SKILL.md').exists():
                skills_to_check.append(skill_dir)
        print(f"{Colors.BLUE}Validating completed skills (with SKILL.md){Colors.NC}")

    else:
        # All skills
        skills_to_check = sorted(skills_dir.iterdir())
        print(f"{Colors.BLUE}Validating all skills{Colors.NC}")

    print()

    # Run validation
    for skill_path in skills_to_check:
        if not skill_path.is_dir():
            continue

        skill_name = skill_path.name
        has_skill_md = (skill_path / 'SKILL.md').exists()
        has_init_md = (skill_path / 'init.md').exists()
        is_phase_skill = skill_name in phase_skills

        if has_skill_md:
            # Track existing vs new
            if not is_phase_skill:
                existing_count += 1

            # Validate
            result = validate_skill(skill_path, rules)
            results.append(result)

            # Print inline result
            status = f"{Colors.GREEN}PASS{Colors.NC}" if result.passed else \
                     f"{Colors.RED}FAIL{Colors.NC}"
            error_info = ""
            if not result.passed:
                error_info = f" ({len(result.errors)} errors, {len(result.warnings)} warnings)"
            elif args.show_community and result.community:
                error_info = f" ({len(result.community)} suggestions)"
            print(f"Validating: {Colors.BLUE}{skill_name}{Colors.NC}... {status}{error_info}")

        elif has_init_md and (args.phase or not args.completed):
            # Pending skill
            pending_count += 1
            phase = get_phase_for_skill(rules, skill_name)
            phase_info = f" (Phase {phase})" if phase else ""
            print(f"{Colors.YELLOW}Pending: {skill_name} (init.md only){phase_info}{Colors.NC}")

    # Summary
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    total = len(results) + pending_count
    total_community = sum(len(r.community) for r in results)
    skills_with_suggestions = sum(1 for r in results if r.community)

    print()
    print("=" * 42)
    print("BATCH VALIDATION SUMMARY")
    print("=" * 42)
    print()
    print(f"Total Checked: {total}")
    if existing_count > 0:
        print(f"  Existing:    {existing_count}")
        new_validated = len(results) - existing_count
        if new_validated > 0:
            print(f"  New:         {new_validated}")
    print()
    print(f"{Colors.GREEN}Passed:        {passed}{Colors.NC}")
    print(f"{Colors.RED}Failed:        {failed}{Colors.NC}")
    if pending_count > 0:
        print(f"{Colors.YELLOW}Pending:       {pending_count}{Colors.NC}")
    if args.show_community and total_community > 0:
        print(f"{Colors.CYAN}Community:     {total_community} suggestions across {skills_with_suggestions} skills{Colors.NC}")
    print()

    if len(results) > 0:
        pass_rate = (passed * 100) // len(results)
        print(f"Pass Rate: {pass_rate}%")

    if pending_count > 0:
        impl_rate = (len(results) * 100) // total
        print(f"Implementation Rate: {impl_rate}%")

    # Show failed details
    failed_results = [r for r in results if not r.passed]
    if failed_results:
        print()
        print(f"{Colors.RED}Failed Skills:{Colors.NC}")
        print()

        for result in failed_results:
            print(f"  {Colors.RED}{result.skill_name}{Colors.NC}")
            for error in result.errors[:5]:  # Limit to 5 errors
                print(f"    - {error}")
            print()

        print("Fix with: python scripts/validate_skill.py skills/<name> --verbose")

    # Show community suggestions
    if args.show_community and total_community > 0:
        print()
        print(f"{Colors.CYAN}Community Practice Suggestions:{Colors.NC}")
        print()

        for result in results:
            if result.community:
                print(f"  {Colors.CYAN}{result.skill_name}{Colors.NC}")
                for suggestion in result.community[:3]:  # Limit to 3 per skill
                    print(f"    - {suggestion}")
                if len(result.community) > 3:
                    print(f"    ... and {len(result.community) - 3} more")
                print()

        print(f"View all suggestions: python scripts/validate_skill.py skills/<name> --verbose")

    # JSON output
    if args.json:
        output = {
            'summary': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'pending': pending_count,
                'pass_rate': (passed * 100) // len(results) if results else 0,
                'community_suggestions': total_community,
                'skills_with_suggestions': skills_with_suggestions,
            },
            'results': [r.to_dict() for r in results],
        }
        print()
        print(json.dumps(output, indent=2))

    print()
    if failed == 0:
        if passed > 0:
            print(f"{Colors.GREEN}All validated skills passed!{Colors.NC}")
        else:
            print(f"{Colors.YELLOW}No skills to validate{Colors.NC}")
        return 0
    else:
        print(f"{Colors.RED}{failed} skill(s) failed validation{Colors.NC}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
