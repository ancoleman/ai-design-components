"""
CI-friendly command-line interface for skill validation.

This module provides a non-interactive CLI suitable for CI/CD pipelines,
with proper exit codes and machine-readable output formats.
"""

import sys
from pathlib import Path
from typing import Optional

from .validator import Validator
from .rules import load_rules, load_community_practices, load_project_rules
from .formatters import get_formatter, ConsoleFormatter
from .result import ValidationReport


def run_ci(
    skills_dir: Path,
    output_format: str = "console",
    output_file: Optional[Path] = None,
    completed_only: bool = False,
    phase: Optional[int] = None,
    rules_only: bool = False,
    skip_project_rules: bool = False,
    fail_fast: bool = False,
    quiet: bool = False,
    verbose: bool = False,
    rules_path: Optional[Path] = None,
    community_path: Optional[Path] = None,
    project_path: Optional[Path] = None,
) -> int:
    """
    Run validation in CI mode.

    Args:
        skills_dir: Directory containing skills to validate.
        output_format: Output format (json, junit, tap, console, markdown).
        output_file: Write output to this file instead of stdout.
        completed_only: Only validate skills with SKILL.md.
        phase: Only validate skills in this phase (1-4).
        rules_only: Skip community practice checks.
        skip_project_rules: Skip project-specific rule checks.
        fail_fast: Stop on first failure.
        quiet: Suppress progress output.
        verbose: Show detailed output including suggestions.
        rules_path: Custom rules file path.
        community_path: Custom community practices file path.
        project_path: Custom project rules file path.

    Returns:
        Exit code (0 = success, 1 = failures, 2 = error).
    """
    try:
        # Load configuration
        rules = load_rules(rules_path)
        community = None if rules_only else load_community_practices(community_path)
        project = None if skip_project_rules else load_project_rules(project_path)

        # Create validator
        validator = Validator(
            rules=rules,
            community=community,
            project=project,
            include_community=not rules_only,
            include_project=not skip_project_rules
        )

        # Progress callback for non-quiet mode
        def progress_callback(skill_name: str, current: int, total: int) -> None:
            if not quiet and output_format == "console":
                # Use carriage return for same-line updates
                sys.stderr.write(f"\rValidating: {skill_name} ({current}/{total})...")
                sys.stderr.flush()

        # Run validation
        report = validator.validate_all(
            skills_dir=skills_dir,
            completed_only=completed_only,
            phase=phase,
            progress_callback=None if quiet else progress_callback
        )

        # Clear progress line
        if not quiet and output_format == "console":
            sys.stderr.write("\r" + " " * 60 + "\r")
            sys.stderr.flush()

        # Format output
        if output_format == "console":
            formatter = ConsoleFormatter(use_color=True, verbose=verbose)
        else:
            formatter = get_formatter(output_format)

        output = formatter.format(report)

        # Write output
        if output_file:
            output_file.write_text(output)
            if not quiet:
                print(f"Results written to: {output_file}", file=sys.stderr)
                # Also print summary to console
                print(report.summary())
        else:
            print(output)

        return report.exit_code

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


def run_check(
    skill_path: Path,
    rules_only: bool = False,
    skip_project_rules: bool = False,
    verbose: bool = False,
    rules_path: Optional[Path] = None,
    project_path: Optional[Path] = None,
) -> int:
    """
    Validate a single skill.

    Args:
        skill_path: Path to the skill directory.
        rules_only: Skip community practice checks.
        skip_project_rules: Skip project-specific rule checks.
        verbose: Show detailed output including suggestions.
        rules_path: Custom rules file path.
        project_path: Custom project rules file path.

    Returns:
        Exit code (0 = pass, 1 = fail, 2 = error).
    """
    try:
        # Load configuration
        rules = load_rules(rules_path)
        community = None if rules_only else load_community_practices()
        project = None if skip_project_rules else load_project_rules(project_path)

        # Create validator
        validator = Validator(
            rules=rules,
            community=community,
            project=project,
            include_community=not rules_only,
            include_project=not skip_project_rules
        )

        # Run validation
        result = validator.validate_skill(skill_path)

        # Format output
        formatter = ConsoleFormatter(use_color=True, verbose=verbose)

        # Create a mini report for formatting
        report = ValidationReport()
        report.add_result(result)
        report.duration_ms = result.duration_ms

        print(formatter.format(report))

        return 0 if result.passed else 1

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


def print_summary(report: ValidationReport) -> None:
    """Print a brief summary of validation results."""
    if report.all_passed:
        print(f"✓ All {report.total} skills passed validation")
    else:
        print(f"✗ {report.failed}/{report.total} skills failed validation")
        for result in report.failures:
            print(f"  - {result.skill_name}: {len(result.errors)} error(s)")
