#!/usr/bin/env python3
"""
Skill Validation CLI

Usage:
    python -m validation ci [options]       # CI mode with machine-readable output
    python -m validation tui [options]      # Interactive TUI
    python -m validation check <skill>      # Validate single skill

Examples:
    python -m validation ci --format=junit -o results.xml
    python -m validation ci --completed --format=json
    python -m validation tui --completed
    python -m validation check building-forms
"""

import argparse
import sys
from pathlib import Path


def find_skills_dir() -> Path:
    """Find the skills directory relative to script location."""
    # Try common locations
    candidates = [
        Path.cwd() / "skills",
        Path(__file__).parent.parent.parent / "skills",
        Path.cwd(),
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate

    return Path.cwd() / "skills"


def cmd_ci(args: argparse.Namespace) -> int:
    """Run CI validation."""
    from .cli import run_ci

    skills_dir = Path(args.skills_dir) if args.skills_dir else find_skills_dir()
    output_file = Path(args.output) if args.output else None
    rules_path = Path(args.rules) if args.rules else None
    community_path = Path(args.community) if args.community else None
    project_path = Path(args.project) if args.project else None

    return run_ci(
        skills_dir=skills_dir,
        output_format=args.format,
        output_file=output_file,
        completed_only=args.completed,
        phase=args.phase,
        rules_only=args.rules_only,
        skip_project_rules=args.skip_project_rules,
        fail_fast=args.fail_fast,
        quiet=args.quiet,
        verbose=args.verbose,
        rules_path=rules_path,
        community_path=community_path,
        project_path=project_path,
    )


def cmd_tui(args: argparse.Namespace) -> int:
    """Run interactive TUI."""
    try:
        from .tui import run_tui
    except ImportError:
        print("Error: TUI requires 'textual' package. Install with: pip install textual", file=sys.stderr)
        return 2

    skills_dir = Path(args.skills_dir) if args.skills_dir else find_skills_dir()

    run_tui(
        skills_dir=skills_dir,
        completed_only=args.completed,
        phase=args.phase,
        rules_only=args.rules_only,
        skip_project_rules=args.skip_project_rules,
    )
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """Validate a single skill."""
    from .cli import run_check

    # Handle skill as name or path
    skill_input = args.skill
    if Path(skill_input).exists():
        skill_path = Path(skill_input)
    else:
        # Assume it's a skill name, find it
        skills_dir = Path(args.skills_dir) if args.skills_dir else find_skills_dir()
        skill_path = skills_dir / skill_input
        if not skill_path.exists():
            print(f"Error: Skill not found: {skill_input}", file=sys.stderr)
            print(f"Looked in: {skill_path}", file=sys.stderr)
            return 2

    rules_path = Path(args.rules) if args.rules else None
    project_path = Path(args.project) if args.project else None

    return run_check(
        skill_path=skill_path,
        rules_only=args.rules_only,
        skip_project_rules=args.skip_project_rules,
        verbose=args.verbose,
        rules_path=rules_path,
        project_path=project_path,
    )


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="validation",
        description="Skill Validation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ci                          Validate all skills, console output
  %(prog)s ci --format=junit -o r.xml  Output JUnit XML for CI
  %(prog)s ci --completed              Only validate completed skills
  %(prog)s ci --phase=1                Only validate phase 1 skills
  %(prog)s ci --rules-only             Skip community suggestions
  %(prog)s tui                         Launch interactive TUI
  %(prog)s tui --completed             TUI with completed skills only
  %(prog)s check building-forms        Validate single skill
        """
    )

    # Global options
    parser.add_argument(
        "--skills-dir", "-d",
        help="Path to skills directory (default: auto-detect)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # CI command
    ci_parser = subparsers.add_parser(
        "ci",
        help="CI-friendly validation with machine-readable output"
    )
    ci_parser.add_argument(
        "--format", "-f",
        choices=["console", "json", "junit", "tap", "markdown"],
        default="console",
        help="Output format (default: console)"
    )
    ci_parser.add_argument(
        "--output", "-o",
        help="Write output to file instead of stdout"
    )
    ci_parser.add_argument(
        "--completed", "-c",
        action="store_true",
        help="Only validate skills with SKILL.md"
    )
    ci_parser.add_argument(
        "--phase", "-p",
        type=int,
        choices=[1, 2, 3, 4],
        help="Only validate skills in specific phase"
    )
    ci_parser.add_argument(
        "--rules-only",
        action="store_true",
        help="Skip community practice checks (faster)"
    )
    ci_parser.add_argument(
        "--skip-project-rules",
        action="store_true",
        help="Skip project-specific rule checks"
    )
    ci_parser.add_argument(
        "--rules",
        help="Custom rules YAML file"
    )
    ci_parser.add_argument(
        "--community",
        help="Custom community practices YAML file"
    )
    ci_parser.add_argument(
        "--project",
        help="Custom project rules YAML file"
    )
    ci_parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first failure"
    )
    ci_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    ci_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output including suggestions"
    )
    ci_parser.set_defaults(func=cmd_ci)

    # TUI command
    tui_parser = subparsers.add_parser(
        "tui",
        help="Interactive terminal UI"
    )
    tui_parser.add_argument(
        "--completed", "-c",
        action="store_true",
        help="Only show skills with SKILL.md"
    )
    tui_parser.add_argument(
        "--phase", "-p",
        type=int,
        choices=[1, 2, 3, 4],
        help="Only show skills in specific phase"
    )
    tui_parser.add_argument(
        "--rules-only",
        action="store_true",
        help="Skip community practice checks"
    )
    tui_parser.add_argument(
        "--skip-project-rules",
        action="store_true",
        help="Skip project-specific rule checks"
    )
    tui_parser.set_defaults(func=cmd_tui)

    # Check command
    check_parser = subparsers.add_parser(
        "check",
        help="Validate a single skill"
    )
    check_parser.add_argument(
        "skill",
        help="Skill name or path"
    )
    check_parser.add_argument(
        "--rules-only",
        action="store_true",
        help="Skip community practice checks"
    )
    check_parser.add_argument(
        "--skip-project-rules",
        action="store_true",
        help="Skip project-specific rule checks"
    )
    check_parser.add_argument(
        "--rules",
        help="Custom rules YAML file"
    )
    check_parser.add_argument(
        "--project",
        help="Custom project rules YAML file"
    )
    check_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    check_parser.set_defaults(func=cmd_check)

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command
    if not args.command:
        parser.print_help()
        return 0

    # Run command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
