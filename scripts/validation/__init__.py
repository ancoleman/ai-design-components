"""
Skill Validation Package

A comprehensive validation toolkit for Claude Skills, supporting both
CI/CD pipelines and interactive development workflows.

Usage:
    CLI:
        python -m validation ci --format=junit -o results.xml
        python -m validation tui --completed
        python -m validation check building-forms

    Programmatic:
        from validation import Validator

        validator = Validator()
        report = validator.validate_all("./skills")

        if not report.all_passed:
            for result in report.failures:
                print(f"{result.skill_name}: {result.errors}")
"""

__version__ = "1.0.0"

# Core classes
from .result import (
    ValidationResult,
    ValidationReport,
    ValidationIssue,
    Severity,
    Timer,
)

from .validator import Validator

from .rules import (
    ValidationRules,
    CommunityPractices,
    ProjectRules,
    ProjectRule,
    load_rules,
    load_community_practices,
    load_project_rules,
    load_config,
)

from .formatters import (
    Formatter,
    JSONFormatter,
    JUnitFormatter,
    TAPFormatter,
    ConsoleFormatter,
    MarkdownFormatter,
    get_formatter,
)

# Public API
__all__ = [
    # Version
    "__version__",

    # Core
    "Validator",
    "ValidationResult",
    "ValidationReport",
    "ValidationIssue",
    "Severity",
    "Timer",

    # Rules
    "ValidationRules",
    "CommunityPractices",
    "ProjectRules",
    "ProjectRule",
    "load_rules",
    "load_community_practices",
    "load_project_rules",
    "load_config",

    # Formatters
    "Formatter",
    "JSONFormatter",
    "JUnitFormatter",
    "TAPFormatter",
    "ConsoleFormatter",
    "MarkdownFormatter",
    "get_formatter",
]
