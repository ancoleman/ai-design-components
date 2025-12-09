"""
Skill Validation Package

A comprehensive validation toolkit for Claude Skills and Skillchain Blueprints,
supporting both CI/CD pipelines and interactive development workflows.

Usage:
    CLI:
        python -m validation ci --format=junit -o results.xml
        python -m validation tui --completed
        python -m validation check building-forms
        python -m validation blueprints          # Validate all blueprints
        python -m validation blueprints api-first.md  # Validate single blueprint

    Programmatic:
        from validation import Validator, BlueprintValidator

        # Skill validation
        validator = Validator()
        report = validator.validate_all("./skills")

        # Blueprint validation
        bp_validator = BlueprintValidator()
        bp_report = bp_validator.validate_all(blueprints_dir)
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

from .blueprints import (
    BlueprintValidator,
    BlueprintResult,
    BlueprintReport,
)

from .rules import (
    ValidationRules,
    CommunityPractices,
    ProjectRules,
    ProjectRule,
    BlueprintRules,
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

    # Core - Skills
    "Validator",
    "ValidationResult",
    "ValidationReport",
    "ValidationIssue",
    "Severity",
    "Timer",

    # Core - Blueprints
    "BlueprintValidator",
    "BlueprintResult",
    "BlueprintReport",

    # Rules
    "ValidationRules",
    "CommunityPractices",
    "ProjectRules",
    "ProjectRule",
    "BlueprintRules",
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
