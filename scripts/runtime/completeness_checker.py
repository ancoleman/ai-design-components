#!/usr/bin/env python3
"""
Project Completeness Checker for Skillchain-Generated Projects

Validates generated projects against blueprint deliverables requirements.
Supports both blueprint-based validation and basic completeness checks.

Usage:
    python completeness_checker.py --project /path/to/project --blueprint ml-pipeline
    python completeness_checker.py --project /path/to/project --maturity advanced --verbose
    python completeness_checker.py --project /path/to/project  # Basic mode
"""

import argparse
import glob
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import yaml


# Exit codes
EXIT_SUCCESS = 0
EXIT_NEEDS_ATTENTION = 1
EXIT_ERROR = 2

# Thresholds
COMPLETENESS_THRESHOLD = 80


class DeliverableStatus:
    """Status of a deliverable check"""
    FULFILLED = "fulfilled"
    MISSING = "missing"
    INCOMPLETE = "incomplete"
    SKIPPED = "skipped"


class CheckResult:
    """Result of a deliverable check"""
    def __init__(self, name: str, status: str, details: Optional[List[str]] = None):
        self.name = name
        self.status = status
        self.details = details or []


class BlueprintValidator:
    """Validates project against blueprint deliverables"""

    def __init__(self, blueprint_path: Path, project_path: Path, maturity: str, verbose: bool = False):
        self.blueprint_path = blueprint_path
        self.project_path = project_path
        self.maturity = maturity
        self.verbose = verbose
        self.deliverables = None
        self.maturity_profiles = None

    def load_blueprint(self) -> bool:
        """Load and parse blueprint file"""
        try:
            with open(self.blueprint_path, 'r') as f:
                content = f.read()

            # Extract YAML from markdown (between ```yaml and ```)
            yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
            if not yaml_match:
                print(f"ERROR: No YAML block found in blueprint: {self.blueprint_path}")
                return False

            yaml_content = yaml_match.group(1)
            blueprint_data = yaml.safe_load(yaml_content)

            self.deliverables = blueprint_data.get('deliverables', {})
            self.maturity_profiles = blueprint_data.get('maturity_profiles', {})

            if not self.deliverables:
                print(f"ERROR: No deliverables found in blueprint")
                return False

            return True

        except FileNotFoundError:
            print(f"ERROR: Blueprint file not found: {self.blueprint_path}")
            return False
        except yaml.YAMLError as e:
            print(f"ERROR: Failed to parse YAML from blueprint: {e}")
            return False
        except Exception as e:
            print(f"ERROR: Failed to load blueprint: {e}")
            return False

    def apply_maturity_filter(self) -> Dict[str, Any]:
        """Filter deliverables based on maturity level"""
        if not self.maturity_profiles or self.maturity not in self.maturity_profiles:
            # No maturity filtering, return all deliverables
            return self.deliverables

        profile = self.maturity_profiles[self.maturity]
        required_deliverables = profile.get('deliverables', [])

        # If no specific deliverables listed, include all
        if not required_deliverables:
            return self.deliverables

        # Filter to only required deliverables
        filtered = {}
        for key, value in self.deliverables.items():
            if key in required_deliverables:
                filtered[key] = value

        return filtered

    def check_files_exist(self, patterns: List[str]) -> Tuple[bool, List[str]]:
        """
        Check if files matching patterns exist

        Returns:
            (all_found, missing_patterns)
        """
        missing = []

        for pattern in patterns:
            # Convert pattern to absolute path
            full_pattern = os.path.join(self.project_path, pattern)

            # Use glob to find matching files
            matches = glob.glob(full_pattern, recursive=True)

            if not matches:
                missing.append(pattern)

        return (len(missing) == 0, missing)

    def run_content_check(self, pattern: str, file_path: str) -> bool:
        """
        Run regex pattern check against file content

        Returns:
            True if pattern found, False otherwise
        """
        try:
            full_path = os.path.join(self.project_path, file_path)

            if not os.path.exists(full_path):
                return False

            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            return bool(re.search(pattern, content))

        except Exception as e:
            if self.verbose:
                print(f"  Warning: Failed to check content in {file_path}: {e}")
            return False

    def check_deliverable(self, name: str, spec: Dict[str, Any]) -> CheckResult:
        """Check a single deliverable"""
        required_files = spec.get('required_files', [])
        content_checks = spec.get('content_checks', {})

        # Check required files
        if required_files:
            files_found, missing_files = self.check_files_exist(required_files)

            if not files_found:
                details = [f"Missing: {f}" for f in missing_files]
                return CheckResult(name, DeliverableStatus.MISSING, details)

        # Check content requirements
        if content_checks:
            incomplete_checks = []

            for file_path, checks in content_checks.items():
                if isinstance(checks, str):
                    checks = [checks]

                for pattern in checks:
                    if not self.run_content_check(pattern, file_path):
                        incomplete_checks.append(f"Missing pattern in {file_path}: {pattern[:50]}...")

            if incomplete_checks:
                return CheckResult(name, DeliverableStatus.INCOMPLETE, incomplete_checks)

        return CheckResult(name, DeliverableStatus.FULFILLED)

    def validate(self) -> Tuple[List[CheckResult], List[str]]:
        """
        Validate project against blueprint

        Returns:
            (results, skipped_deliverables)
        """
        if not self.load_blueprint():
            return [], []

        filtered_deliverables = self.apply_maturity_filter()

        # Identify skipped deliverables
        all_keys = set(self.deliverables.keys())
        filtered_keys = set(filtered_deliverables.keys())
        skipped = list(all_keys - filtered_keys)

        # Check each deliverable
        results = []
        for name, spec in filtered_deliverables.items():
            result = self.check_deliverable(name, spec)
            results.append(result)

        return results, skipped


class BasicValidator:
    """Basic project validation without blueprint"""

    def __init__(self, project_path: Path, verbose: bool = False):
        self.project_path = project_path
        self.verbose = verbose

    def count_directories_and_files(self) -> Tuple[int, int]:
        """Count total directories and files"""
        dir_count = 0
        file_count = 0

        for root, dirs, files in os.walk(self.project_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            dir_count += len(dirs)
            file_count += len(files)

        return dir_count, file_count

    def find_empty_directories(self) -> List[str]:
        """Find directories with no files (recursively)"""
        empty_dirs = []

        for root, dirs, files in os.walk(self.project_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for d in dirs:
                dir_path = os.path.join(root, d)

                # Check if directory is empty (no files recursively)
                has_files = False
                for _, _, files_in_subdir in os.walk(dir_path):
                    if files_in_subdir:
                        has_files = True
                        break

                if not has_files:
                    # Get relative path
                    rel_path = os.path.relpath(dir_path, self.project_path)
                    empty_dirs.append(rel_path)

        return empty_dirs

    def check_readme(self) -> bool:
        """Check if README.md exists"""
        readme_path = os.path.join(self.project_path, 'README.md')
        return os.path.exists(readme_path)

    def validate(self) -> Dict[str, Any]:
        """Run basic validation"""
        dir_count, file_count = self.count_directories_and_files()
        empty_dirs = self.find_empty_directories()
        has_readme = self.check_readme()

        # Calculate directory completeness (percentage of non-empty dirs)
        if dir_count > 0:
            completeness = ((dir_count - len(empty_dirs)) / dir_count) * 100
        else:
            completeness = 0

        return {
            'total_directories': dir_count,
            'total_files': file_count,
            'empty_directories': empty_dirs,
            'readme_exists': has_readme,
            'directory_completeness': completeness
        }


def print_blueprint_results(
    project_path: Path,
    blueprint_name: str,
    maturity: str,
    results: List[CheckResult],
    skipped: List[str],
    verbose: bool
):
    """Print blueprint validation results"""
    print("PROJECT COMPLETENESS CHECK")
    print("=" * 50)
    print()
    print(f"Project: {project_path}")
    print(f"Blueprint: {blueprint_name}")
    print(f"Maturity: {maturity}")
    print()
    print("DELIVERABLES:")

    # Count statuses
    fulfilled_count = 0
    missing_count = 0
    incomplete_count = 0

    for result in results:
        if result.status == DeliverableStatus.FULFILLED:
            symbol = "✓"
            fulfilled_count += 1
        elif result.status == DeliverableStatus.MISSING:
            symbol = "✗"
            missing_count += 1
        elif result.status == DeliverableStatus.INCOMPLETE:
            symbol = "⚠"
            incomplete_count += 1
        else:
            symbol = "?"

        print(f"{symbol} {result.name}", end="")

        if result.status != DeliverableStatus.FULFILLED:
            print(f" - {result.status.upper()}")
            if verbose and result.details:
                for detail in result.details:
                    print(f"  └─ {detail}")
        else:
            print()

    # Print skipped deliverables
    if skipped:
        print()
        for name in skipped:
            print(f"○ {name} (skipped - not required for {maturity})")

    # Summary
    required_count = len(results)
    total_count = required_count + len(skipped)

    if required_count > 0:
        completeness = (fulfilled_count / required_count) * 100
    else:
        completeness = 0

    print()
    print("SUMMARY:")
    print(f"Required: {required_count}")
    print(f"Fulfilled: {fulfilled_count}")
    print(f"Missing: {missing_count}")
    if incomplete_count > 0:
        print(f"Incomplete: {incomplete_count}")
    print(f"Skipped: {len(skipped)}")
    print()
    print(f"Completeness: {completeness:.0f}%")

    if completeness >= COMPLETENESS_THRESHOLD:
        print(f"Status: PASSED (target: {COMPLETENESS_THRESHOLD}%)")
        return EXIT_SUCCESS
    else:
        print(f"Status: NEEDS ATTENTION (target: {COMPLETENESS_THRESHOLD}%)")
        return EXIT_NEEDS_ATTENTION


def print_basic_results(project_path: Path, results: Dict[str, Any]):
    """Print basic validation results"""
    print("PROJECT COMPLETENESS CHECK")
    print("=" * 50)
    print()
    print(f"Project: {project_path}")
    print("Mode: Basic (no blueprint)")
    print()
    print("METRICS:")
    print(f"Total directories: {results['total_directories']}")
    print(f"Total files: {results['total_files']}")
    print(f"Empty directories: {len(results['empty_directories'])}")
    print(f"README exists: {'Yes' if results['readme_exists'] else 'No'}")

    if results['empty_directories']:
        print()
        print("EMPTY DIRECTORIES:")
        for empty_dir in results['empty_directories']:
            print(f"• {empty_dir}/")

    print()
    print(f"Directory completeness: {results['directory_completeness']:.0f}%")

    if results['directory_completeness'] >= COMPLETENESS_THRESHOLD:
        print("Status: PASSED")
        return EXIT_SUCCESS
    else:
        print("Status: NEEDS ATTENTION")
        return EXIT_NEEDS_ATTENTION


def find_blueprint_path(blueprint_name: str) -> Optional[Path]:
    """Find blueprint file in standard locations"""
    # Standard location
    home = Path.home()
    standard_path = home / ".claude" / "commands" / "skillchain" / "blueprints" / f"{blueprint_name}.md"

    if standard_path.exists():
        return standard_path

    # Try local development location (relative to this script)
    script_dir = Path(__file__).parent
    local_path = script_dir.parent / "commands" / "skillchain" / "blueprints" / f"{blueprint_name}.md"

    if local_path.exists():
        return local_path

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Check completeness of skillchain-generated projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate against blueprint
  %(prog)s --project ./my-ml-pipeline --blueprint ml-pipeline

  # Validate with specific maturity level
  %(prog)s --project ./my-app --blueprint api-first --maturity advanced

  # Basic validation (no blueprint)
  %(prog)s --project ./my-project

  # Verbose output
  %(prog)s --project ./my-app --blueprint ml-pipeline --verbose
        """
    )

    parser.add_argument(
        '--project',
        type=str,
        required=True,
        help='Path to generated project'
    )

    parser.add_argument(
        '--blueprint',
        type=str,
        help='Blueprint name to validate against (e.g., ml-pipeline, api-first)'
    )

    parser.add_argument(
        '--maturity',
        type=str,
        choices=['starter', 'intermediate', 'advanced'],
        default='intermediate',
        help='Maturity level for validation (default: intermediate)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project).resolve()
    if not project_path.exists():
        print(f"ERROR: Project path does not exist: {project_path}")
        return EXIT_ERROR

    if not project_path.is_dir():
        print(f"ERROR: Project path is not a directory: {project_path}")
        return EXIT_ERROR

    # Blueprint mode vs basic mode
    if args.blueprint:
        blueprint_path = find_blueprint_path(args.blueprint)

        if not blueprint_path:
            print(f"ERROR: Blueprint not found: {args.blueprint}")
            print(f"Searched in:")
            print(f"  - ~/.claude/commands/skillchain/blueprints/{args.blueprint}.md")
            print(f"  - ../commands/skillchain/blueprints/{args.blueprint}.md (relative to script)")
            return EXIT_ERROR

        if args.verbose:
            print(f"Using blueprint: {blueprint_path}")
            print()

        validator = BlueprintValidator(
            blueprint_path=blueprint_path,
            project_path=project_path,
            maturity=args.maturity,
            verbose=args.verbose
        )

        results, skipped = validator.validate()

        if not results and not skipped:
            # Error occurred during validation
            return EXIT_ERROR

        return print_blueprint_results(
            project_path=project_path,
            blueprint_name=args.blueprint,
            maturity=args.maturity,
            results=results,
            skipped=skipped,
            verbose=args.verbose
        )
    else:
        # Basic mode
        validator = BasicValidator(
            project_path=project_path,
            verbose=args.verbose
        )

        results = validator.validate()

        return print_basic_results(
            project_path=project_path,
            results=results
        )


if __name__ == '__main__':
    sys.exit(main())
