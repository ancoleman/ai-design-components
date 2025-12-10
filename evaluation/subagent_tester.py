#!/usr/bin/env python3
"""
Subagent Test Framework

Tests skill-executor and other subagents by spawning Claude Code CLI sessions
and validating outputs against expected results.

Usage:
    python evaluation/subagent_tester.py [test_file.yaml]
    python evaluation/subagent_tester.py --all
    python evaluation/subagent_tester.py --subagent skill-executor
"""

import argparse
import json
import subprocess
import yaml
from pathlib import Path
from datetime import datetime
import tempfile
import os
import sys
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class TestResult:
    """Result of a single test case execution"""
    name: str
    subagent: str
    passed: bool
    duration_seconds: float
    activation: bool
    protocol_adherence: Dict[str, Any] = field(default_factory=dict)
    output_quality: Dict[str, Any] = field(default_factory=dict)
    tool_compliance: Dict[str, Any] = field(default_factory=dict)
    cost_usd: float = 0.0
    tokens: Dict[str, int] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


@dataclass
class AggregateReport:
    """Aggregate results across multiple tests"""
    subagent: str
    total_tests: int
    passed: int
    failed: int
    activation_rate: float
    protocol_adherence_avg: float
    output_quality_avg: float
    tool_compliance_rate: float
    total_cost_usd: float
    avg_duration_seconds: float
    failed_tests: List[str]


class SubagentTester:
    """Test subagents using Claude Code CLI"""

    def __init__(self, project_path: str, verbose: bool = False):
        """
        Initialize the subagent tester.

        Args:
            project_path: Root path of the project
            verbose: Enable verbose output
        """
        self.project_path = Path(project_path).resolve()
        self.verbose = verbose
        self.results: List[TestResult] = []

    def log(self, message: str, level: str = "INFO") -> None:
        """Log a message with optional color coding"""
        if level == "ERROR":
            print(f"{Colors.RED}{message}{Colors.RESET}", file=sys.stderr)
        elif level == "SUCCESS":
            print(f"{Colors.GREEN}{message}{Colors.RESET}")
        elif level == "WARNING":
            print(f"{Colors.YELLOW}{message}{Colors.RESET}")
        elif level == "DEBUG" and self.verbose:
            print(f"{Colors.CYAN}[DEBUG] {message}{Colors.RESET}")
        else:
            print(message)

    def load_test_cases(self, test_file: Path) -> Dict[str, Any]:
        """
        Load test cases from YAML file.

        Args:
            test_file: Path to YAML test file

        Returns:
            Dictionary containing test suite configuration
        """
        try:
            with open(test_file, 'r') as f:
                data = yaml.safe_load(f)

            if not data:
                raise ValueError(f"Empty test file: {test_file}")

            if 'test_cases' not in data:
                raise ValueError(f"No 'test_cases' key in {test_file}")

            self.log(f"Loaded {len(data['test_cases'])} test(s) from {test_file.name}", "DEBUG")
            return data

        except yaml.YAMLError as e:
            self.log(f"Failed to parse YAML file {test_file}: {e}", "ERROR")
            raise
        except FileNotFoundError:
            self.log(f"Test file not found: {test_file}", "ERROR")
            raise

    def run_test(self, test_case: Dict[str, Any], subagent: str) -> TestResult:
        """
        Run a single test case via Claude Code CLI.

        Args:
            test_case: Test case configuration
            subagent: Subagent name to test

        Returns:
            TestResult object with validation results
        """
        test_name = test_case.get('name', 'unnamed-test')
        prompt = test_case.get('prompt', '')
        timeout = test_case.get('timeout', 120)
        cwd = test_case.get('cwd', None)

        self.log(f"\n{Colors.BOLD}Running test: {test_name}{Colors.RESET}")
        self.log(f"Subagent: {subagent}", "DEBUG")

        # Run setup commands if specified
        setup_commands = test_case.get('setup', [])
        if setup_commands:
            self.log("Running setup commands...", "DEBUG")
            for cmd in setup_commands:
                try:
                    subprocess.run(cmd, shell=True, check=True, capture_output=True)
                except subprocess.CalledProcessError as e:
                    self.log(f"Setup command failed: {cmd}", "WARNING")

        # Build Claude Code CLI command
        cmd = [
            'claude',
            '--print',
            '--verbose',
            '--output-format', 'stream-json',
            '--dangerously-skip-permissions',
            '--agent', subagent,
            '--', prompt
        ]

        work_dir = cwd if cwd else str(self.project_path)

        self.log(f"Spawning Claude Code CLI (timeout: {timeout}s)...", "DEBUG")
        start_time = datetime.now()

        try:
            # Execute Claude Code CLI
            result = subprocess.run(
                cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            duration = (datetime.now() - start_time).total_seconds()

            # Parse JSONL output
            parsed_output = self._parse_output(result.stdout)

            # Check if subagent activated (received output)
            activation = bool(parsed_output.get('text', '').strip())

            # Validate expectations
            validation = self._validate_output(
                parsed_output,
                test_case.get('expected', {}),
                work_dir
            )

            # Build test result
            test_result = TestResult(
                name=test_name,
                subagent=subagent,
                passed=validation['passed'],
                duration_seconds=duration,
                activation=activation,
                protocol_adherence=validation.get('protocol_adherence', {}),
                output_quality=validation.get('output_quality', {}),
                tool_compliance=validation.get('tool_compliance', {}),
                cost_usd=parsed_output.get('cost', 0.0),
                tokens=parsed_output.get('tokens', {}),
                errors=validation.get('errors', [])
            )

            # Run teardown commands
            teardown_commands = test_case.get('teardown', [])
            if teardown_commands:
                self.log("Running teardown commands...", "DEBUG")
                for cmd in teardown_commands:
                    try:
                        subprocess.run(cmd, shell=True, check=True, capture_output=True)
                    except subprocess.CalledProcessError:
                        self.log(f"Teardown command failed: {cmd}", "WARNING")

            if test_result.passed:
                self.log(f"✓ {test_name} PASSED ({duration:.1f}s, ${test_result.cost_usd:.4f})", "SUCCESS")
            else:
                self.log(f"✗ {test_name} FAILED ({duration:.1f}s)", "ERROR")
                for error in test_result.errors:
                    self.log(f"  - {error}", "ERROR")

            return test_result

        except subprocess.TimeoutExpired:
            duration = (datetime.now() - start_time).total_seconds()
            self.log(f"✗ {test_name} TIMEOUT after {timeout}s", "ERROR")

            return TestResult(
                name=test_name,
                subagent=subagent,
                passed=False,
                duration_seconds=duration,
                activation=False,
                errors=[f"Test timed out after {timeout} seconds"]
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log(f"✗ {test_name} ERROR: {e}", "ERROR")

            return TestResult(
                name=test_name,
                subagent=subagent,
                passed=False,
                duration_seconds=duration,
                activation=False,
                errors=[str(e)]
            )

    def _parse_output(self, stdout: str) -> Dict[str, Any]:
        """
        Parse JSONL output from Claude Code CLI.

        Args:
            stdout: Raw stdout from Claude CLI

        Returns:
            Parsed output dictionary
        """
        result = {
            'session_id': None,
            'text': '',
            'cost': 0.0,
            'tokens': {}
        }

        for line in stdout.strip().split('\n'):
            if not line.strip():
                continue

            try:
                msg = json.loads(line)

                # Extract session ID
                if msg.get('session_id') and not result['session_id']:
                    result['session_id'] = msg['session_id']
                    self.log(f"Session ID: {result['session_id']}", "DEBUG")

                # Extract result text (prefer 'result' over streaming 'assistant')
                if msg.get('type') == 'result' and msg.get('result'):
                    result['text'] = msg['result']
                    self.log(f"Got result text ({len(result['text'])} chars)", "DEBUG")

                # Extract cost and usage
                if msg.get('total_cost_usd') is not None:
                    result['cost'] = msg['total_cost_usd']
                    self.log(f"Cost: ${result['cost']:.4f}", "DEBUG")

                if msg.get('modelUsage'):
                    input_tokens = 0
                    output_tokens = 0
                    cache_read = 0
                    cache_creation = 0

                    for stats in msg['modelUsage'].values():
                        input_tokens += stats.get('inputTokens', 0)
                        output_tokens += stats.get('outputTokens', 0)
                        cache_read += stats.get('cacheReadInputTokens', 0)
                        cache_creation += stats.get('cacheCreationInputTokens', 0)

                    result['tokens'] = {
                        'input': input_tokens,
                        'output': output_tokens,
                        'cache_read': cache_read,
                        'cache_creation': cache_creation
                    }
                    self.log(f"Tokens: {input_tokens} in, {output_tokens} out", "DEBUG")

            except json.JSONDecodeError:
                # Non-JSON line, could be raw output
                self.log(f"Non-JSON line: {line[:100]}", "DEBUG")
                pass

        return result

    def _validate_output(
        self,
        output: Dict[str, Any],
        expected: Dict[str, Any],
        work_dir: str
    ) -> Dict[str, Any]:
        """
        Validate Claude's output against expected results.

        Args:
            output: Parsed output from Claude
            expected: Expected results from test case
            work_dir: Working directory for file checks

        Returns:
            Validation results dictionary
        """
        errors = []
        text = output.get('text', '')

        # Protocol adherence checks
        protocol_checks = []

        # Check skill invocation (for skill executors)
        if 'skill_invoked' in expected:
            skill_invoked = expected['skill_invoked']
            found = skill_invoked in text
            protocol_checks.append({
                'check': f'skill_invoked:{skill_invoked}',
                'passed': found
            })
            if not found:
                errors.append(f"Expected skill '{skill_invoked}' not found in output")

        # Check report contains required strings
        if 'report_contains' in expected:
            for marker in expected['report_contains']:
                found = marker in text
                protocol_checks.append({
                    'check': f'contains:{marker}',
                    'passed': found
                })
                if not found:
                    errors.append(f"Expected text '{marker}' not found in output")

        # Check report excludes forbidden strings
        if 'report_excludes' in expected:
            for marker in expected['report_excludes']:
                found = marker in text
                protocol_checks.append({
                    'check': f'excludes:{marker}',
                    'passed': not found
                })
                if found:
                    errors.append(f"Forbidden text '{marker}' found in output")

        # Check report matches regex patterns
        if 'report_matches' in expected:
            for pattern_spec in expected['report_matches']:
                pattern = pattern_spec.get('pattern', '')
                description = pattern_spec.get('description', pattern)
                try:
                    matched = bool(re.search(pattern, text))
                    protocol_checks.append({
                        'check': f'matches:{description}',
                        'passed': matched
                    })
                    if not matched:
                        errors.append(f"Pattern not matched: {description}")
                except re.error as e:
                    errors.append(f"Invalid regex pattern: {pattern} ({e})")
                    protocol_checks.append({
                        'check': f'matches:{description}',
                        'passed': False
                    })

        # Calculate protocol adherence score
        protocol_passed = sum(1 for c in protocol_checks if c['passed'])
        protocol_total = len(protocol_checks)
        protocol_score = protocol_passed / protocol_total if protocol_total > 0 else 1.0

        # Output quality checks (file creation)
        quality_checks = []

        if 'files_created' in expected:
            for file_spec in expected['files_created']:
                pattern = file_spec.get('pattern', '')
                min_count = file_spec.get('min_count', 1)

                try:
                    # Use glob to find matching files
                    work_path = Path(work_dir)
                    matches = list(work_path.glob(pattern))
                    found_count = len(matches)
                    passed = found_count >= min_count

                    quality_checks.append({
                        'check': f'files:{pattern}',
                        'expected': min_count,
                        'found': found_count,
                        'passed': passed
                    })

                    if not passed:
                        errors.append(
                            f"File pattern '{pattern}': expected >={min_count}, found {found_count}"
                        )
                    else:
                        self.log(
                            f"File pattern '{pattern}': found {found_count} file(s)",
                            "DEBUG"
                        )

                except Exception as e:
                    errors.append(f"Error checking file pattern '{pattern}': {e}")
                    quality_checks.append({
                        'check': f'files:{pattern}',
                        'expected': min_count,
                        'found': 0,
                        'passed': False
                    })

        # Calculate output quality score
        quality_passed = sum(1 for c in quality_checks if c['passed'])
        quality_total = len(quality_checks)
        quality_score = quality_passed / quality_total if quality_total > 0 else 1.0

        # Tool compliance (placeholder - would require parsing session JSONL)
        tool_score = 1.0  # Assume compliant unless we implement tool tracking

        # Overall pass/fail
        all_passed = len(errors) == 0

        return {
            'passed': all_passed,
            'errors': errors,
            'protocol_adherence': {
                'score': protocol_score,
                'checks': protocol_checks,
                'passed': protocol_passed,
                'total': protocol_total
            },
            'output_quality': {
                'score': quality_score,
                'checks': quality_checks,
                'passed': quality_passed,
                'total': quality_total
            },
            'tool_compliance': {
                'score': tool_score,
                'unauthorized_tools': []
            }
        }

    def run_test_suite(self, test_file: Path) -> List[TestResult]:
        """
        Run all tests in a test file.

        Args:
            test_file: Path to YAML test file

        Returns:
            List of test results
        """
        suite = self.load_test_cases(test_file)
        subagent = suite.get('subagent', 'unknown')

        self.log(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
        self.log(f"{Colors.BOLD}Test Suite: {suite.get('name', 'unnamed')}{Colors.RESET}")
        self.log(f"Subagent: {subagent}")
        self.log(f"Tests: {len(suite['test_cases'])}")
        self.log(f"{Colors.BOLD}{'='*70}{Colors.RESET}")

        results = []
        for test_case in suite['test_cases']:
            result = self.run_test(test_case, subagent)
            results.append(result)
            self.results.append(result)

        return results

    def generate_report(self, results: Optional[List[TestResult]] = None) -> str:
        """
        Generate test report with pass/fail summary.

        Args:
            results: List of test results (uses all results if None)

        Returns:
            Formatted report string
        """
        if results is None:
            results = self.results

        if not results:
            return "No test results to report."

        # Group results by subagent
        by_subagent = {}
        for result in results:
            if result.subagent not in by_subagent:
                by_subagent[result.subagent] = []
            by_subagent[result.subagent].append(result)

        # Generate report for each subagent
        reports = []
        for subagent, subagent_results in by_subagent.items():
            total = len(subagent_results)
            passed = sum(1 for r in subagent_results if r.passed)
            failed = total - passed

            activation_rate = sum(1 for r in subagent_results if r.activation) / total

            protocol_scores = [
                r.protocol_adherence.get('score', 0)
                for r in subagent_results
                if r.protocol_adherence
            ]
            protocol_avg = sum(protocol_scores) / len(protocol_scores) if protocol_scores else 0

            quality_scores = [
                r.output_quality.get('score', 0)
                for r in subagent_results
                if r.output_quality
            ]
            quality_avg = sum(quality_scores) / len(quality_scores) if quality_scores else 0

            tool_scores = [
                r.tool_compliance.get('score', 0)
                for r in subagent_results
                if r.tool_compliance
            ]
            tool_rate = sum(tool_scores) / len(tool_scores) if tool_scores else 0

            total_cost = sum(r.cost_usd for r in subagent_results)
            avg_duration = sum(r.duration_seconds for r in subagent_results) / total

            failed_tests = [r.name for r in subagent_results if not r.passed]

            # Format report
            report = f"""
{Colors.BOLD}SUBAGENT TEST RESULTS: {subagent}{Colors.RESET}
{'='*70}

Tests run: {total}
Passed: {Colors.GREEN}{passed}{Colors.RESET}
Failed: {Colors.RED if failed > 0 else Colors.GREEN}{failed}{Colors.RESET}

ACTIVATION RATE: {activation_rate*100:.1f}%
PROTOCOL ADHERENCE: {protocol_avg*100:.1f}%
OUTPUT QUALITY: {quality_avg*100:.1f}%
TOOL COMPLIANCE: {tool_rate*100:.1f}%

Total Cost: ${total_cost:.4f}
Avg Duration: {avg_duration:.1f}s
"""

            if failed_tests:
                report += f"\n{Colors.RED}FAILED TESTS:{Colors.RESET}\n"
                for test_name in failed_tests:
                    result = next(r for r in subagent_results if r.name == test_name)
                    report += f"  - {test_name}\n"
                    for error in result.errors:
                        report += f"    {error}\n"

            reports.append(report)

        return "\n".join(reports)

    def export_json(self, output_file: Path) -> None:
        """
        Export test results to JSON file.

        Args:
            output_file: Path to output JSON file
        """
        # Group by subagent
        by_subagent = {}
        for result in self.results:
            if result.subagent not in by_subagent:
                by_subagent[result.subagent] = []
            by_subagent[result.subagent].append(result)

        # Build aggregate reports
        aggregates = []
        for subagent, results in by_subagent.items():
            total = len(results)
            passed = sum(1 for r in results if r.passed)

            aggregate = AggregateReport(
                subagent=subagent,
                total_tests=total,
                passed=passed,
                failed=total - passed,
                activation_rate=sum(1 for r in results if r.activation) / total,
                protocol_adherence_avg=sum(
                    r.protocol_adherence.get('score', 0) for r in results
                ) / total,
                output_quality_avg=sum(
                    r.output_quality.get('score', 0) for r in results
                ) / total,
                tool_compliance_rate=sum(
                    r.tool_compliance.get('score', 0) for r in results
                ) / total,
                total_cost_usd=sum(r.cost_usd for r in results),
                avg_duration_seconds=sum(r.duration_seconds for r in results) / total,
                failed_tests=[r.name for r in results if not r.passed]
            )
            aggregates.append(aggregate)

        # Convert to JSON-serializable format
        output = {
            'timestamp': datetime.now().isoformat(),
            'aggregates': [
                {
                    'subagent': a.subagent,
                    'total_tests': a.total_tests,
                    'passed': a.passed,
                    'failed': a.failed,
                    'activation_rate': a.activation_rate,
                    'protocol_adherence_avg': a.protocol_adherence_avg,
                    'output_quality_avg': a.output_quality_avg,
                    'tool_compliance_rate': a.tool_compliance_rate,
                    'total_cost_usd': a.total_cost_usd,
                    'avg_duration_seconds': a.avg_duration_seconds,
                    'failed_tests': a.failed_tests
                }
                for a in aggregates
            ],
            'individual_results': [
                {
                    'name': r.name,
                    'subagent': r.subagent,
                    'passed': r.passed,
                    'duration_seconds': r.duration_seconds,
                    'activation': r.activation,
                    'protocol_adherence': r.protocol_adherence,
                    'output_quality': r.output_quality,
                    'tool_compliance': r.tool_compliance,
                    'cost_usd': r.cost_usd,
                    'tokens': r.tokens,
                    'errors': r.errors
                }
                for r in self.results
            ]
        }

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        self.log(f"\nResults exported to: {output_file}", "SUCCESS")


def find_test_files(
    tests_dir: Path,
    subagent: Optional[str] = None
) -> List[Path]:
    """
    Find test files in the evaluation/subagent-tests directory.

    Args:
        tests_dir: Path to evaluation/subagent-tests directory
        subagent: Filter by subagent name (optional)

    Returns:
        List of test file paths
    """
    test_files = []

    if subagent:
        # Look in subagent-specific directory
        subagent_dir = tests_dir / subagent
        if subagent_dir.exists() and subagent_dir.is_dir():
            test_files.extend(subagent_dir.glob("*.yaml"))
            test_files.extend(subagent_dir.glob("*.yml"))
    else:
        # Find all YAML files in all subdirectories
        test_files.extend(tests_dir.glob("**/*.yaml"))
        test_files.extend(tests_dir.glob("**/*.yml"))

    return sorted(test_files)


def main():
    """Main entry point for the subagent tester"""
    parser = argparse.ArgumentParser(
        description='Test subagents using Claude Code CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run a specific test file
  python evaluation/subagent_tester.py evaluation/subagent-tests/skill-executor/basic.yaml

  # Run all tests for a specific subagent
  python evaluation/subagent_tester.py --subagent skill-executor

  # Run all tests
  python evaluation/subagent_tester.py --all

  # Export results to JSON
  python evaluation/subagent_tester.py --all --report test-results.json
        """
    )

    parser.add_argument(
        'test_file',
        nargs='?',
        type=Path,
        help='Test file to run (YAML)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all tests in evaluation/subagent-tests/'
    )
    parser.add_argument(
        '--subagent',
        help='Test specific subagent (e.g., skill-executor)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--report',
        type=Path,
        help='Export results to JSON file'
    )

    args = parser.parse_args()

    # Determine project path (parent of evaluation/)
    script_dir = Path(__file__).parent
    project_path = script_dir.parent
    tests_dir = script_dir / 'subagent-tests'

    # Create tester instance
    tester = SubagentTester(str(project_path), verbose=args.verbose)

    # Determine which tests to run
    test_files = []

    if args.test_file:
        # Run specific test file
        if not args.test_file.exists():
            tester.log(f"Test file not found: {args.test_file}", "ERROR")
            sys.exit(1)
        test_files = [args.test_file]

    elif args.all:
        # Run all tests
        test_files = find_test_files(tests_dir)
        if not test_files:
            tester.log(f"No test files found in {tests_dir}", "ERROR")
            sys.exit(1)
        tester.log(f"Found {len(test_files)} test file(s)")

    elif args.subagent:
        # Run tests for specific subagent
        test_files = find_test_files(tests_dir, args.subagent)
        if not test_files:
            tester.log(f"No test files found for subagent '{args.subagent}'", "ERROR")
            sys.exit(1)
        tester.log(f"Found {len(test_files)} test file(s) for subagent '{args.subagent}'")

    else:
        parser.print_help()
        sys.exit(1)

    # Run tests
    try:
        for test_file in test_files:
            tester.run_test_suite(test_file)

        # Generate and print report
        report = tester.generate_report()
        print("\n" + report)

        # Export to JSON if requested
        if args.report:
            tester.export_json(args.report)

        # Exit with non-zero code if any tests failed
        failed_count = sum(1 for r in tester.results if not r.passed)
        if failed_count > 0:
            sys.exit(1)

    except KeyboardInterrupt:
        tester.log("\n\nInterrupted by user", "WARNING")
        sys.exit(130)
    except Exception as e:
        tester.log(f"\nFatal error: {e}", "ERROR")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
