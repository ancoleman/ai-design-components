"""
Output formatters for validation results.

This module provides various output formats for validation results:
- JSON: Machine-readable, good for parsing in scripts
- JUnit XML: Supported by most CI systems (GitHub Actions, Jenkins, etc.)
- TAP: Test Anything Protocol, universal test format
- Console: Human-readable with colors (via Rich)
"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from xml.dom import minidom

from .result import ValidationReport, ValidationResult


class Formatter(ABC):
    """Base class for output formatters."""

    @abstractmethod
    def format(self, report: ValidationReport) -> str:
        """Format a validation report as a string."""
        pass

    @property
    @abstractmethod
    def extension(self) -> str:
        """File extension for this format (without dot)."""
        pass


class JSONFormatter(Formatter):
    """Format results as JSON."""

    def __init__(self, pretty: bool = True):
        self.pretty = pretty

    def format(self, report: ValidationReport) -> str:
        data = report.to_dict()
        data["generated_at"] = datetime.utcnow().isoformat() + "Z"

        if self.pretty:
            return json.dumps(data, indent=2)
        return json.dumps(data)

    @property
    def extension(self) -> str:
        return "json"


class JUnitFormatter(Formatter):
    """
    Format results as JUnit XML.

    This format is widely supported by CI systems including:
    - GitHub Actions
    - Jenkins
    - GitLab CI
    - CircleCI
    - Azure DevOps
    """

    def format(self, report: ValidationReport) -> str:
        # Create root element
        testsuites = ET.Element("testsuites")
        testsuites.set("name", "Skill Validation")
        testsuites.set("tests", str(report.total))
        testsuites.set("failures", str(report.failed))
        testsuites.set("errors", "0")
        testsuites.set("time", str(report.duration_ms / 1000))

        # Create testsuite
        testsuite = ET.SubElement(testsuites, "testsuite")
        testsuite.set("name", "skills")
        testsuite.set("tests", str(report.total))
        testsuite.set("failures", str(report.failed))
        testsuite.set("errors", "0")
        testsuite.set("time", str(report.duration_ms / 1000))
        testsuite.set("timestamp", datetime.utcnow().isoformat())

        # Add test cases
        for result in report.results:
            testcase = ET.SubElement(testsuite, "testcase")
            testcase.set("name", result.skill_name)
            testcase.set("classname", "skills")
            testcase.set("time", str(result.duration_ms / 1000))

            if not result.passed:
                failure = ET.SubElement(testcase, "failure")
                failure.set("message", f"{len(result.errors)} validation error(s)")
                failure.set("type", "ValidationError")
                failure.text = "\n".join(result.errors)

            # Add warnings as system-out
            if result.warnings:
                system_out = ET.SubElement(testcase, "system-out")
                system_out.text = "Warnings:\n" + "\n".join(result.warnings)

            # Add suggestions as system-err (informational)
            if result.suggestions:
                system_err = ET.SubElement(testcase, "system-err")
                system_err.text = "Suggestions:\n" + "\n".join(result.suggestions)

        # Pretty print
        xml_str = ET.tostring(testsuites, encoding='unicode')
        return minidom.parseString(xml_str).toprettyxml(indent="  ")

    @property
    def extension(self) -> str:
        return "xml"


class TAPFormatter(Formatter):
    """
    Format results as TAP (Test Anything Protocol).

    TAP is a simple, universal test format supported by many tools.
    """

    def format(self, report: ValidationReport) -> str:
        lines = []
        lines.append(f"TAP version 14")
        lines.append(f"1..{report.total}")

        for i, result in enumerate(report.results, 1):
            if result.passed:
                status = "ok"
                directive = ""
            else:
                status = "not ok"
                directive = ""

            lines.append(f"{status} {i} - {result.skill_name}{directive}")

            # Add YAML diagnostics for failures
            if not result.passed:
                lines.append("  ---")
                lines.append(f"  message: '{len(result.errors)} validation error(s)'")
                lines.append("  severity: fail")
                lines.append("  errors:")
                for error in result.errors:
                    # Escape single quotes in error message
                    safe_error = error.replace("'", "''")
                    lines.append(f"    - '{safe_error}'")
                lines.append("  ...")

            # Add warnings as comments
            for warning in result.warnings:
                lines.append(f"# WARNING: {warning}")

        # Summary comment
        lines.append(f"# {report.summary()}")

        return "\n".join(lines)

    @property
    def extension(self) -> str:
        return "tap"


class ConsoleFormatter(Formatter):
    """
    Format results for console output with colors.

    Uses ANSI escape codes for colors. For richer output,
    use the Rich library directly in CLI.
    """

    # ANSI color codes
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def __init__(self, use_color: bool = True, verbose: bool = False):
        self.use_color = use_color
        self.verbose = verbose

    def _color(self, text: str, color: str) -> str:
        if self.use_color:
            return f"{color}{text}{self.RESET}"
        return text

    def format(self, report: ValidationReport) -> str:
        lines = []

        # Header
        lines.append(self._color("Skill Validation Report", self.BOLD))
        lines.append("=" * 50)
        lines.append("")

        # Results
        for result in report.results:
            if result.passed:
                status = self._color("PASS", self.GREEN)
            else:
                status = self._color("FAIL", self.RED)

            warn_count = len(result.warnings)
            warn_str = ""
            if warn_count > 0:
                warn_str = self._color(f" ({warn_count} warnings)", self.YELLOW)

            lines.append(f"[{status}] {result.skill_name}{warn_str}")

            # Show details if verbose or failed
            if self.verbose or not result.passed:
                for error in result.errors:
                    lines.append(f"  {self._color('ERROR', self.RED)}: {error}")
                if self.verbose:
                    for warning in result.warnings:
                        lines.append(f"  {self._color('WARN', self.YELLOW)}: {warning}")
                    for suggestion in result.suggestions:
                        lines.append(f"  {self._color('INFO', self.BLUE)}: {suggestion}")

        # Summary
        lines.append("")
        lines.append("-" * 50)

        passed_str = self._color(str(report.passed), self.GREEN)
        failed_str = self._color(str(report.failed), self.RED if report.failed else self.GREEN)

        lines.append(f"Total: {report.total} | Passed: {passed_str} | Failed: {failed_str}")
        lines.append(f"Duration: {report.duration_ms:.0f}ms")

        if report.all_passed:
            lines.append(self._color("\nAll validations passed!", self.GREEN + self.BOLD))
        else:
            lines.append(self._color(f"\n{report.failed} skill(s) failed validation", self.RED + self.BOLD))

        return "\n".join(lines)

    @property
    def extension(self) -> str:
        return "txt"


class MarkdownFormatter(Formatter):
    """Format results as Markdown for GitHub comments/PRs."""

    def format(self, report: ValidationReport) -> str:
        lines = []

        # Header with status badge
        if report.all_passed:
            lines.append("## :white_check_mark: Skill Validation Passed")
        else:
            lines.append("## :x: Skill Validation Failed")

        lines.append("")

        # Summary table
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total | {report.total} |")
        lines.append(f"| Passed | {report.passed} |")
        lines.append(f"| Failed | {report.failed} |")
        lines.append(f"| Duration | {report.duration_ms:.0f}ms |")
        lines.append("")

        # Failures section
        if report.failures:
            lines.append("### Failures")
            lines.append("")
            for result in report.failures:
                lines.append(f"<details>")
                lines.append(f"<summary><b>{result.skill_name}</b> - {len(result.errors)} error(s)</summary>")
                lines.append("")
                lines.append("**Errors:**")
                for error in result.errors:
                    lines.append(f"- {error}")
                if result.warnings:
                    lines.append("")
                    lines.append("**Warnings:**")
                    for warning in result.warnings:
                        lines.append(f"- {warning}")
                lines.append("")
                lines.append("</details>")
                lines.append("")

        # Passed skills (collapsed)
        if report.successes:
            lines.append("<details>")
            lines.append(f"<summary>Passed Skills ({report.passed})</summary>")
            lines.append("")
            for result in report.successes:
                warn_note = f" ({len(result.warnings)} warnings)" if result.warnings else ""
                lines.append(f"- :white_check_mark: {result.skill_name}{warn_note}")
            lines.append("")
            lines.append("</details>")

        return "\n".join(lines)

    @property
    def extension(self) -> str:
        return "md"


# Formatter registry
FORMATTERS = {
    "json": JSONFormatter,
    "junit": JUnitFormatter,
    "tap": TAPFormatter,
    "console": ConsoleFormatter,
    "text": ConsoleFormatter,
    "markdown": MarkdownFormatter,
    "md": MarkdownFormatter,
}


def get_formatter(name: str, **kwargs) -> Formatter:
    """
    Get a formatter by name.

    Args:
        name: Formatter name (json, junit, tap, console, markdown).
        **kwargs: Arguments to pass to the formatter constructor.

    Returns:
        Formatter instance.

    Raises:
        ValueError: If the formatter name is unknown.
    """
    name = name.lower()
    if name not in FORMATTERS:
        available = ", ".join(FORMATTERS.keys())
        raise ValueError(f"Unknown formatter: {name}. Available: {available}")

    return FORMATTERS[name](**kwargs)
