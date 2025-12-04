"""
Result types for skill validation.

This module defines the data structures used to represent validation results,
distinguishing between:
- Errors: Core rule violations that cause failure
- Warnings: Core rule violations that don't fail but should be addressed
- Suggestions: Community practice recommendations (informational only)
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import time


class Severity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"        # Fails validation
    WARNING = "warning"    # Doesn't fail, but important
    SUGGESTION = "suggestion"  # Community practice, informational


@dataclass
class ValidationIssue:
    """A single validation issue."""
    message: str
    severity: Severity
    rule_id: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None

    def __str__(self) -> str:
        prefix = {
            Severity.ERROR: "ERROR",
            Severity.WARNING: "WARN",
            Severity.SUGGESTION: "INFO"
        }[self.severity]

        location = ""
        if self.file_path:
            location = f" [{self.file_path}"
            if self.line_number:
                location += f":{self.line_number}"
            location += "]"

        return f"{prefix}{location}: {self.message}"


@dataclass
class ValidationResult:
    """Result of validating a single skill."""
    skill_name: str
    skill_path: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    duration_ms: float = 0.0

    # Detailed issues (optional, for richer output)
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Validation passes if there are no errors."""
        return len(self.errors) == 0

    @property
    def status(self) -> str:
        """Human-readable status."""
        if self.errors:
            return "FAIL"
        elif self.warnings:
            return "WARN"
        else:
            return "PASS"

    @property
    def total_issues(self) -> int:
        """Total count of all issues."""
        return len(self.errors) + len(self.warnings) + len(self.suggestions)

    def add_error(self, message: str, rule_id: Optional[str] = None) -> None:
        """Add an error (causes failure)."""
        self.errors.append(message)
        self.issues.append(ValidationIssue(
            message=message,
            severity=Severity.ERROR,
            rule_id=rule_id
        ))

    def add_warning(self, message: str, rule_id: Optional[str] = None) -> None:
        """Add a warning (doesn't cause failure)."""
        self.warnings.append(message)
        self.issues.append(ValidationIssue(
            message=message,
            severity=Severity.WARNING,
            rule_id=rule_id
        ))

    def add_suggestion(self, message: str, rule_id: Optional[str] = None) -> None:
        """Add a community suggestion (informational)."""
        self.suggestions.append(message)
        self.issues.append(ValidationIssue(
            message=message,
            severity=Severity.SUGGESTION,
            rule_id=rule_id
        ))

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "skill_name": self.skill_name,
            "skill_path": self.skill_path,
            "passed": self.passed,
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "duration_ms": round(self.duration_ms, 2),
            "counts": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "suggestions": len(self.suggestions)
            }
        }


@dataclass
class ValidationReport:
    """Aggregated results from validating multiple skills."""
    results: List[ValidationResult] = field(default_factory=list)
    duration_ms: float = 0.0
    config_path: Optional[str] = None

    @property
    def total(self) -> int:
        """Total number of skills validated."""
        return len(self.results)

    @property
    def passed(self) -> int:
        """Number of skills that passed."""
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        """Number of skills that failed."""
        return sum(1 for r in self.results if not r.passed)

    @property
    def with_warnings(self) -> int:
        """Number of skills with warnings (but may have passed)."""
        return sum(1 for r in self.results if r.warnings)

    @property
    def all_passed(self) -> bool:
        """True if all skills passed validation."""
        return self.failed == 0

    @property
    def exit_code(self) -> int:
        """
        Exit code for CLI usage.
        0 = all passed
        1 = one or more failures
        """
        return 0 if self.all_passed else 1

    @property
    def failures(self) -> List[ValidationResult]:
        """List of failed validation results."""
        return [r for r in self.results if not r.passed]

    @property
    def successes(self) -> List[ValidationResult]:
        """List of successful validation results."""
        return [r for r in self.results if r.passed]

    def add_result(self, result: ValidationResult) -> None:
        """Add a validation result to the report."""
        self.results.append(result)

    def summary(self) -> str:
        """Human-readable summary."""
        return (
            f"Validated {self.total} skills: "
            f"{self.passed} passed, {self.failed} failed, "
            f"{self.with_warnings} with warnings "
            f"({self.duration_ms:.0f}ms)"
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "summary": {
                "total": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "with_warnings": self.with_warnings,
                "duration_ms": round(self.duration_ms, 2),
                "all_passed": self.all_passed,
                "exit_code": self.exit_code
            },
            "results": [r.to_dict() for r in self.results],
            "config_path": self.config_path
        }


class Timer:
    """Context manager for timing operations."""

    def __init__(self):
        self.start_time: float = 0
        self.end_time: float = 0

    def __enter__(self) -> 'Timer':
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args) -> None:
        self.end_time = time.perf_counter()

    @property
    def elapsed_ms(self) -> float:
        """Elapsed time in milliseconds."""
        return (self.end_time - self.start_time) * 1000
