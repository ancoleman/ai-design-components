#!/usr/bin/env python3
"""
Subagent Test Framework

Tests skills and subagent behaviors by spawning Claude Code CLI sessions
and validating outputs against expected results.

Claude Code CLI Integration:
    - Uses headless mode with --print flag for non-interactive execution
    - Parses stream-json output for structured response handling
    - Skills are triggered via prompts that activate SKILL.md files in context

Usage:
    python evaluation/subagent_tester.py [test_file.yaml]
    python evaluation/subagent_tester.py --all
    python evaluation/subagent_tester.py --subagent skill-executor

Requirements:
    - Claude Code CLI installed and accessible in PATH
    - ANTHROPIC_API_KEY environment variable set (or authenticated via 'claude login')
    - PyYAML: pip install pyyaml

Reference:
    - CLI Reference: https://code.claude.com/docs/en/cli-reference
    - SDK Overview: https://platform.claude.com/docs/en/agent-sdk/overview
"""

import argparse
import json
import subprocess
import yaml
import shutil
from pathlib import Path
from datetime import datetime
import tempfile
import os
import sys
import re
from typing import Dict, List, Any, Optional, Tuple
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


def get_expanded_path() -> str:
    """
    Build an expanded PATH that includes common Claude Code installation locations.

    Packaged apps and certain environments may not inherit the full shell PATH,
    so we explicitly add common binary locations.

    Returns:
        Expanded PATH string with additional binary directories
    """
    home = os.path.expanduser("~")
    additional_paths = [
        '/opt/homebrew/bin',           # Homebrew Apple Silicon
        '/opt/homebrew/sbin',
        '/usr/local/bin',              # Homebrew Intel / common
        '/usr/local/sbin',
        f'{home}/.local/bin',          # pip, poetry, etc.
        f'{home}/.npm-global/bin',     # npm global
        f'{home}/bin',                 # User bin
        f'{home}/.claude/local',       # Claude local install
        '/usr/bin', '/bin', '/usr/sbin', '/sbin'
    ]

    current_path = os.environ.get('PATH', '')
    existing = set(current_path.split(':'))

    # Prepend additional paths that aren't already present
    new_paths = [p for p in additional_paths if p not in existing and os.path.isdir(p)]

    return ':'.join(new_paths + list(existing))


def detect_claude_binary() -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Detect if Claude Code CLI is available and get its path.

    Returns:
        Tuple of (available: bool, path: Optional[str], error: Optional[str])
    """
    # First try shutil.which with current PATH
    claude_path = shutil.which('claude')

    if claude_path:
        return True, claude_path, None

    # Try with expanded PATH
    expanded_env = os.environ.copy()
    expanded_env['PATH'] = get_expanded_path()

    try:
        result = subprocess.run(
            ['which', 'claude'],
            capture_output=True,
            text=True,
            env=expanded_env,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return True, result.stdout.strip().split('\n')[0], None
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        pass

    # Check common locations directly
    home = os.path.expanduser("~")
    common_locations = [
        '/opt/homebrew/bin/claude',
        '/usr/local/bin/claude',
        f'{home}/.local/bin/claude',
        f'{home}/.npm-global/bin/claude',
        f'{home}/.claude/local/claude',
    ]

    for location in common_locations:
        if os.path.isfile(location) and os.access(location, os.X_OK):
            return True, location, None

    return False, None, (
        "Claude Code CLI not found. Please install it:\n"
        "  npm install -g @anthropic-ai/claude-code\n"
        "  # or\n"
        "  brew install claude-code\n"
        "\n"
        "Then authenticate:\n"
        "  claude login"
    )


def check_authentication() -> Tuple[bool, Optional[str]]:
    """
    Check if Claude Code is authenticated.

    Returns:
        Tuple of (authenticated: bool, error: Optional[str])
    """
    # Check for API key in environment
    if os.environ.get('ANTHROPIC_API_KEY'):
        return True, None

    # Check for Bedrock auth
    if os.environ.get('CLAUDE_CODE_USE_BEDROCK') == '1':
        if os.environ.get('AWS_ACCESS_KEY_ID') or os.environ.get('AWS_PROFILE'):
            return True, None

    # Check for Vertex AI auth
    if os.environ.get('CLAUDE_CODE_USE_VERTEX') == '1':
        return True, None

    # Check for Claude login session (presence of config files)
    claude_config = Path.home() / '.claude'
    if claude_config.exists():
        # Claude Code stores auth in ~/.claude
        return True, None

    return False, (
        "Claude Code authentication not detected.\n"
        "Options:\n"
        "  1. Set ANTHROPIC_API_KEY environment variable\n"
        "  2. Run 'claude login' to authenticate interactively\n"
        "  3. For AWS Bedrock: set CLAUDE_CODE_USE_BEDROCK=1 and AWS credentials\n"
        "  4. For Vertex AI: set CLAUDE_CODE_USE_VERTEX=1"
    )


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
    """
    Test skills and subagent behaviors using Claude Code CLI.

    This tester spawns Claude Code in headless mode (--print) with stream-json
    output format for structured response parsing.

    Claude Code CLI Reference:
        --print / -p       : Execute query and exit (headless mode)
        --output-format    : text | json | stream-json
        --verbose          : Enable detailed output
        --dangerously-skip-permissions : Skip permission prompts (automation)
        --max-turns        : Limit agentic turns
        --model            : Specify model version
    """

    def __init__(
        self,
        project_path: str,
        verbose: bool = False,
        model: Optional[str] = None,
        max_turns: Optional[int] = None,
        skip_permissions: bool = True
    ):
        """
        Initialize the subagent tester.

        Args:
            project_path: Root path of the project (used as cwd for Claude)
            verbose: Enable verbose output for debugging
            model: Override default model (e.g., 'claude-sonnet-4-20250514')
            max_turns: Limit number of agentic turns
            skip_permissions: Skip permission prompts (default True for automation)
        """
        self.project_path = Path(project_path).resolve()
        self.verbose = verbose
        self.model = model
        self.max_turns = max_turns
        self.skip_permissions = skip_permissions
        self.results: List[TestResult] = []

        # Detect Claude binary
        self.claude_available, self.claude_path, self.claude_error = detect_claude_binary()

        # Build environment with expanded PATH
        self.env = os.environ.copy()
        self.env['PATH'] = get_expanded_path()

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

    def _build_cli_args(
        self,
        prompt: str,
        test_case: Dict[str, Any]
    ) -> List[str]:
        """
        Build Claude Code CLI arguments.

        Args:
            prompt: The user prompt to send
            test_case: Test case configuration for additional options

        Returns:
            List of CLI arguments
        """
        args = [
            '--print', prompt,           # Headless mode with prompt
            '--output-format', 'stream-json',  # Structured output for parsing
        ]

        # Add verbose flag if enabled
        if self.verbose:
            args.append('--verbose')

        # Skip permission prompts for automation
        if self.skip_permissions:
            args.append('--dangerously-skip-permissions')

        # Override model if specified
        model = test_case.get('model') or self.model
        if model:
            args.extend(['--model', model])

        # Limit agentic turns if specified
        max_turns = test_case.get('max_turns') or self.max_turns
        if max_turns:
            args.extend(['--max-turns', str(max_turns)])

        # Add system prompt if specified in test case
        system_prompt = test_case.get('system_prompt')
        if system_prompt:
            args.extend(['--system-prompt', system_prompt])

        # Add allowed/disallowed tools if specified
        allowed_tools = test_case.get('allowed_tools')
        if allowed_tools:
            args.extend(['--allowedTools', ','.join(allowed_tools)])

        disallowed_tools = test_case.get('disallowed_tools')
        if disallowed_tools:
            args.extend(['--disallowedTools', ','.join(disallowed_tools)])

        # Resume session if specified
        session_id = test_case.get('resume_session')
        if session_id:
            args.extend(['--resume', session_id])

        return args

    def run_test(self, test_case: Dict[str, Any], subagent: str) -> TestResult:
        """
        Run a single test case via Claude Code CLI.

        The 'subagent' parameter is used for categorization and reporting.
        Skills are triggered via the prompt content and SKILL.md files
        present in the working directory context.

        Args:
            test_case: Test case configuration with keys:
                - name: Test name
                - prompt: User prompt to send
                - timeout: Timeout in seconds (default 120)
                - cwd: Working directory (default: project_path)
                - setup: List of setup shell commands
                - teardown: List of teardown shell commands
                - expected: Validation expectations
                - model: Override model
                - max_turns: Limit agentic turns
                - system_prompt: Custom system prompt
                - allowed_tools: List of allowed tools
                - disallowed_tools: List of disallowed tools
                - resume_session: Session ID to resume
            subagent: Subagent/skill category for reporting

        Returns:
            TestResult object with validation results
        """
        test_name = test_case.get('name', 'unnamed-test')
        prompt = test_case.get('prompt', '')
        timeout = test_case.get('timeout', 120)
        cwd = test_case.get('cwd', None)

        self.log(f"\n{Colors.BOLD}Running test: {test_name}{Colors.RESET}")
        self.log(f"Skill/Subagent Category: {subagent}", "DEBUG")

        # Check if Claude CLI is available
        if not self.claude_available:
            self.log(f"Claude CLI not available: {self.claude_error}", "ERROR")
            return TestResult(
                name=test_name,
                subagent=subagent,
                passed=False,
                duration_seconds=0.0,
                activation=False,
                errors=[f"Claude CLI not available: {self.claude_error}"]
            )

        # Run setup commands if specified
        setup_commands = test_case.get('setup', [])
        if setup_commands:
            self.log("Running setup commands...", "DEBUG")
            for cmd in setup_commands:
                try:
                    subprocess.run(
                        cmd,
                        shell=True,
                        check=True,
                        capture_output=True,
                        env=self.env
                    )
                except subprocess.CalledProcessError as e:
                    self.log(f"Setup command failed: {cmd}", "WARNING")

        # Build Claude Code CLI command
        cli_args = self._build_cli_args(prompt, test_case)
        cmd = [self.claude_path] + cli_args

        work_dir = cwd if cwd else str(self.project_path)

        self.log(f"Spawning Claude Code CLI (timeout: {timeout}s)...", "DEBUG")
        self.log(f"Command: {' '.join(cmd[:5])}...", "DEBUG")  # Log partial command
        start_time = datetime.now()

        try:
            # Execute Claude Code CLI
            # Note: Using stdin=subprocess.DEVNULL to prevent stdin issues
            # that can cause hangs (similar to Node.js spawn issue)
            result = subprocess.run(
                cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=self.env,
                stdin=subprocess.DEVNULL  # Prevent stdin blocking
            )

            duration = (datetime.now() - start_time).total_seconds()

            # Log exit code for debugging
            if result.returncode != 0:
                self.log(f"CLI exited with code {result.returncode}", "DEBUG")

            # Parse JSONL output (pass stderr for error logging)
            parsed_output = self._parse_output(result.stdout, result.stderr)

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
                        subprocess.run(
                            cmd,
                            shell=True,
                            check=True,
                            capture_output=True,
                            env=self.env
                        )
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

    def _parse_output(self, stdout: str, stderr: str = '') -> Dict[str, Any]:
        """
        Parse JSONL output from Claude Code CLI.

        Stream-JSON output format includes several message types:
        - system:init - Contains session_id and slash_commands
        - assistant - Streaming partial responses (skip these)
        - result - Final complete response with session_id, result text, usage

        Args:
            stdout: Raw stdout from Claude CLI
            stderr: Raw stderr from Claude CLI (for error logging)

        Returns:
            Parsed output dictionary with keys:
            - session_id: Session identifier
            - text: Final response text
            - cost: Total cost in USD
            - tokens: Token usage breakdown
            - slash_commands: Available slash commands (if present)
            - errors: Any error messages from stderr
        """
        result = {
            'session_id': None,
            'text': '',
            'cost': 0.0,
            'tokens': {},
            'slash_commands': [],
            'errors': []
        }

        # Log stderr if present
        if stderr and stderr.strip():
            self.log(f"CLI stderr: {stderr[:200]}", "DEBUG")
            result['errors'].append(stderr.strip())

        if not stdout or not stdout.strip():
            self.log("No stdout received from Claude CLI", "DEBUG")
            return result

        for line in stdout.strip().split('\n'):
            if not line.strip():
                continue

            try:
                msg = json.loads(line)
                msg_type = msg.get('type', '')

                # Handle system:init message (first message)
                if msg_type == 'system' and msg.get('subtype') == 'init':
                    if msg.get('session_id') and not result['session_id']:
                        result['session_id'] = msg['session_id']
                        self.log(f"Session ID (init): {result['session_id']}", "DEBUG")
                    if msg.get('slash_commands'):
                        result['slash_commands'] = msg['slash_commands']
                    continue

                # Extract session ID from any message that has it
                if msg.get('session_id') and not result['session_id']:
                    result['session_id'] = msg['session_id']
                    self.log(f"Session ID: {result['session_id']}", "DEBUG")

                # Extract result text (prefer 'result' over streaming 'assistant')
                # The 'result' message is the final complete response
                if msg_type == 'result' and msg.get('result'):
                    result['text'] = msg['result']
                    self.log(f"Got result text ({len(result['text'])} chars)", "DEBUG")

                # Skip streaming assistant messages - they are partial responses
                if msg_type == 'assistant':
                    continue

                # Extract cost and usage (usually in the result message)
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
                # Non-JSON line, could be raw output or error
                self.log(f"Non-JSON line: {line[:100]}", "DEBUG")
                # If we haven't gotten structured output, accumulate raw text
                if not result['text']:
                    result['text'] += line + '\n'

        # Trim accumulated raw text
        if result['text']:
            result['text'] = result['text'].strip()

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
        description='Test skills and subagent behaviors using Claude Code CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check Claude Code CLI setup
  python evaluation/subagent_tester.py --check

  # Run a specific test file
  python evaluation/subagent_tester.py evaluation/subagent-tests/skill-executor/basic.yaml

  # Run all tests for a specific subagent/skill category
  python evaluation/subagent_tester.py --subagent skill-executor

  # Run all tests with a specific model
  python evaluation/subagent_tester.py --all --model claude-sonnet-4-20250514

  # Run all tests with verbose output and export to JSON
  python evaluation/subagent_tester.py --all -v --report test-results.json

  # Run with limited turns to control cost
  python evaluation/subagent_tester.py --all --max-turns 3

Requirements:
  - Claude Code CLI installed: npm install -g @anthropic-ai/claude-code
  - Authenticated: claude login OR set ANTHROPIC_API_KEY
  - PyYAML: pip install pyyaml

Documentation:
  - CLI Reference: https://code.claude.com/docs/en/cli-reference
  - SDK Overview: https://platform.claude.com/docs/en/agent-sdk/overview
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
        help='Test specific subagent/skill category (e.g., skill-executor)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    parser.add_argument(
        '--report',
        type=Path,
        help='Export results to JSON file'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check Claude Code CLI setup and exit (no tests run)'
    )
    parser.add_argument(
        '--model',
        help='Override model (e.g., claude-sonnet-4-20250514, claude-opus-4-20250514)'
    )
    parser.add_argument(
        '--max-turns',
        type=int,
        help='Limit number of agentic turns (helps control costs)'
    )
    parser.add_argument(
        '--allow-permissions',
        action='store_true',
        help='Allow permission prompts (default: skip for automation)'
    )

    args = parser.parse_args()

    # Determine project path (parent of evaluation/)
    script_dir = Path(__file__).parent
    project_path = script_dir.parent
    tests_dir = script_dir / 'subagent-tests'

    # Check mode: verify Claude Code CLI setup
    if args.check:
        print(f"{Colors.BOLD}Claude Code CLI Setup Check{Colors.RESET}")
        print("=" * 50)

        # Check binary
        available, path, error = detect_claude_binary()
        if available:
            print(f"{Colors.GREEN}[PASS]{Colors.RESET} Claude CLI found: {path}")
        else:
            print(f"{Colors.RED}[FAIL]{Colors.RESET} Claude CLI not found")
            print(f"       {error}")
            sys.exit(1)

        # Check authentication
        authed, auth_error = check_authentication()
        if authed:
            print(f"{Colors.GREEN}[PASS]{Colors.RESET} Authentication detected")
        else:
            print(f"{Colors.YELLOW}[WARN]{Colors.RESET} Authentication may be required")
            print(f"       {auth_error}")

        # Check test files directory
        if tests_dir.exists():
            test_count = len(list(tests_dir.glob("**/*.yaml"))) + len(list(tests_dir.glob("**/*.yml")))
            print(f"{Colors.GREEN}[PASS]{Colors.RESET} Tests directory found: {tests_dir}")
            print(f"       Found {test_count} test file(s)")
        else:
            print(f"{Colors.YELLOW}[WARN]{Colors.RESET} Tests directory not found: {tests_dir}")

        # Try a simple CLI invocation
        print(f"\n{Colors.BOLD}Quick CLI Test{Colors.RESET}")
        print("-" * 50)
        try:
            result = subprocess.run(
                [path, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()
                print(f"{Colors.GREEN}[PASS]{Colors.RESET} CLI responds: {version[:60]}")
            else:
                print(f"{Colors.YELLOW}[WARN]{Colors.RESET} CLI returned exit code {result.returncode}")
        except Exception as e:
            print(f"{Colors.RED}[FAIL]{Colors.RESET} CLI test failed: {e}")

        print("\n" + "=" * 50)
        print(f"{Colors.GREEN}Setup check complete. Ready to run tests.{Colors.RESET}")
        sys.exit(0)

    # Create tester instance
    tester = SubagentTester(
        str(project_path),
        verbose=args.verbose,
        model=args.model,
        max_turns=args.max_turns,
        skip_permissions=not args.allow_permissions
    )

    # Verify Claude CLI is available before proceeding
    if not tester.claude_available:
        tester.log(f"{Colors.RED}Claude Code CLI not available.{Colors.RESET}", "ERROR")
        tester.log(tester.claude_error, "ERROR")
        tester.log("\nRun with --check to diagnose setup issues.", "INFO")
        sys.exit(1)

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
