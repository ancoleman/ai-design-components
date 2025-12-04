"""
Rules and community practices loading for skill validation.

This module handles loading, parsing, and accessing validation rules
and community practices from YAML configuration files.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

from .config import DEFAULT_RULES_PATH, DEFAULT_COMMUNITY_PATH, DEFAULT_PROJECT_PATH


@dataclass
class AntiPattern:
    """Configuration for an anti-pattern check."""
    name: str
    enabled: bool
    severity: str
    patterns: List[str]
    message: str
    compiled_patterns: List[re.Pattern] = field(default_factory=list)

    def __post_init__(self):
        """Compile regex patterns."""
        self.compiled_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.patterns
        ]

    def find_matches(self, content: str) -> List[str]:
        """Find all matches of this anti-pattern in content."""
        matches = []
        for pattern in self.compiled_patterns:
            found = pattern.findall(content)
            matches.extend(found)
        return matches


@dataclass
class CommunityPractice:
    """Configuration for a community practice check."""
    name: str
    category: str
    enabled: bool
    description: str
    message: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    pattern: Optional[str] = None
    check_type: str = "auto"  # "auto" or "manual"

    def is_auto_checkable(self) -> bool:
        """Return True if this practice can be automatically checked."""
        return self.check_type == "auto" and (self.keywords or self.pattern)


@dataclass
class ValidationRules:
    """Container for all validation rules."""
    version: str
    skill_md: Dict[str, Any]
    frontmatter: Dict[str, Any]
    references: Dict[str, Any]
    anti_patterns: List[AntiPattern]
    structure: Dict[str, Any]
    phases: Dict[str, Any]
    severity: Dict[str, List[str]]

    # Raw config for advanced access
    _raw: Dict[str, Any] = field(default_factory=dict)

    def get_phase_skills(self, phase: int) -> List[str]:
        """Get list of skills for a specific phase."""
        phase_key = f"phase_{phase}"
        return self.phases.get(phase_key, {}).get("skills", [])

    def get_all_phase_skills(self) -> Set[str]:
        """Get all skills across all phases."""
        all_skills = set()
        for phase_data in self.phases.values():
            if isinstance(phase_data, dict):
                all_skills.update(phase_data.get("skills", []))
        return all_skills


@dataclass
class CommunityPractices:
    """Container for community practices."""
    version: str
    sources: List[str]
    practices: List[CommunityPractice]
    active_preset: str
    presets: Dict[str, Any]

    # Raw config for advanced access
    _raw: Dict[str, Any] = field(default_factory=dict)

    def get_enabled_practices(self) -> List[CommunityPractice]:
        """Get list of enabled practices based on active preset."""
        if self.active_preset == "strict":
            return [p for p in self.practices if p.enabled]

        preset = self.presets.get(self.active_preset, {})
        enabled_names = preset.get("enabled_practices", [])

        if enabled_names == "all":
            return [p for p in self.practices if p.enabled]

        return [
            p for p in self.practices
            if p.enabled and p.name in enabled_names
        ]

    def get_auto_checkable_practices(self) -> List[CommunityPractice]:
        """Get practices that can be automatically checked."""
        return [
            p for p in self.get_enabled_practices()
            if p.is_auto_checkable()
        ]


@dataclass
class ProjectRule:
    """Configuration for a project-specific rule."""
    name: str
    enabled: bool
    severity: str
    description: str
    check_type: str  # "keyword", "file_exists", "frontmatter_field"
    message: str
    keywords: List[str] = field(default_factory=list)
    alternative_keywords: List[str] = field(default_factory=list)
    conditional: Optional[Dict[str, Any]] = None

    def get_all_keywords(self) -> List[str]:
        """Get all keywords including alternatives."""
        return self.keywords + self.alternative_keywords

    def applies_to_content(self, content: str) -> bool:
        """Check if this rule applies based on conditional settings."""
        if not self.conditional:
            return True

        applies_when = self.conditional.get("applies_when_contains", [])
        if applies_when:
            content_lower = content.lower()
            return any(kw.lower() in content_lower for kw in applies_when)

        return True

    def check_keywords(self, content: str) -> bool:
        """Check if any of the keywords are present in content."""
        all_keywords = self.get_all_keywords()
        return any(kw in content for kw in all_keywords)


@dataclass
class ProjectRules:
    """Container for project-specific rules."""
    version: str
    project: str
    rules: List[ProjectRule]
    active_preset: str
    presets: Dict[str, Any]

    # Raw config for advanced access
    _raw: Dict[str, Any] = field(default_factory=dict)

    def get_enabled_rules(self) -> List[ProjectRule]:
        """Get list of enabled rules based on active preset."""
        preset = self.presets.get(self.active_preset, {})
        enabled_names = preset.get("enabled_rules", [])
        enable_disabled = preset.get("enable_disabled", False)

        if enabled_names == "all":
            if enable_disabled:
                return self.rules
            return [r for r in self.rules if r.enabled]

        return [
            r for r in self.rules
            if r.enabled and r.name in enabled_names
        ]

    def get_keyword_rules(self) -> List[ProjectRule]:
        """Get rules that use keyword checking."""
        return [
            r for r in self.get_enabled_rules()
            if r.check_type == "keyword"
        ]


def load_rules(path: Optional[Path] = None) -> ValidationRules:
    """
    Load validation rules from a YAML file.

    Args:
        path: Path to rules YAML file. If None, uses default.

    Returns:
        ValidationRules object.

    Raises:
        FileNotFoundError: If the rules file doesn't exist.
        yaml.YAMLError: If the YAML is invalid.
    """
    if path is None:
        path = DEFAULT_RULES_PATH

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Rules file not found: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    # Parse anti-patterns
    anti_patterns = []
    for name, config in raw.get("anti_patterns", {}).items():
        if isinstance(config, dict) and config.get("enabled", True):
            anti_patterns.append(AntiPattern(
                name=name,
                enabled=config.get("enabled", True),
                severity=config.get("severity", "warning"),
                patterns=config.get("patterns", []),
                message=config.get("message", f"Anti-pattern detected: {name}")
            ))

    return ValidationRules(
        version=raw.get("version", "1.0.0"),
        skill_md=raw.get("skill_md", {}),
        frontmatter=raw.get("frontmatter", {}),
        references=raw.get("references", {}),
        anti_patterns=anti_patterns,
        structure=raw.get("structure", {}),
        phases=raw.get("phases", {}),
        severity=raw.get("severity", {"fail_on": ["error"], "warn_on": ["warning"]}),
        _raw=raw
    )


def load_community_practices(path: Optional[Path] = None) -> CommunityPractices:
    """
    Load community practices from a YAML file.

    Args:
        path: Path to community YAML file. If None, uses default.

    Returns:
        CommunityPractices object.

    Raises:
        FileNotFoundError: If the community file doesn't exist.
        yaml.YAMLError: If the YAML is invalid.
    """
    if path is None:
        path = DEFAULT_COMMUNITY_PATH

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Community practices file not found: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    # Parse practices from all categories
    practices = []
    practice_categories = [
        "skill_design", "token_optimization", "portability",
        "documentation", "workflow", "structure_patterns",
        "composition", "quality_indicators"
    ]

    for category in practice_categories:
        category_config = raw.get(category, {})
        for name, config in category_config.items():
            if isinstance(config, dict):
                practices.append(CommunityPractice(
                    name=name,
                    category=category,
                    enabled=config.get("enabled", True),
                    description=config.get("description", ""),
                    message=config.get("message"),
                    keywords=config.get("keywords", []),
                    pattern=config.get("pattern"),
                    check_type=config.get("check_type", "auto")
                ))

    return CommunityPractices(
        version=raw.get("version", "1.0.0"),
        sources=raw.get("sources", []),
        practices=practices,
        active_preset=raw.get("active_preset", "standard"),
        presets=raw.get("presets", {}),
        _raw=raw
    )


def load_project_rules(path: Optional[Path] = None) -> ProjectRules:
    """
    Load project-specific rules from a YAML file.

    Args:
        path: Path to project YAML file. If None, uses default.

    Returns:
        ProjectRules object.

    Raises:
        FileNotFoundError: If the project file doesn't exist.
        yaml.YAMLError: If the YAML is invalid.
    """
    if path is None:
        path = DEFAULT_PROJECT_PATH

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Project rules file not found: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    # Parse rules
    rules = []
    rules_config = raw.get("rules", {})
    for name, config in rules_config.items():
        if isinstance(config, dict):
            rules.append(ProjectRule(
                name=name,
                enabled=config.get("enabled", True),
                severity=config.get("severity", "warning"),
                description=config.get("description", ""),
                check_type=config.get("check_type", "keyword"),
                message=config.get("message", ""),
                keywords=config.get("keywords", []),
                alternative_keywords=config.get("alternative_keywords", []),
                conditional=config.get("conditional"),
            ))

    return ProjectRules(
        version=raw.get("version", "1.0.0"),
        project=raw.get("project", "unknown"),
        rules=rules,
        active_preset=raw.get("active_preset", "standard"),
        presets=raw.get("presets", {}),
        _raw=raw
    )


def load_config(
    rules_path: Optional[Path] = None,
    community_path: Optional[Path] = None,
    project_path: Optional[Path] = None
) -> tuple[ValidationRules, CommunityPractices, ProjectRules]:
    """
    Load all configuration: rules, community practices, and project rules.

    Args:
        rules_path: Path to rules YAML. If None, uses default.
        community_path: Path to community YAML. If None, uses default.
        project_path: Path to project YAML. If None, uses default.

    Returns:
        Tuple of (ValidationRules, CommunityPractices, ProjectRules).
    """
    rules = load_rules(rules_path)
    community = load_community_practices(community_path)
    project = load_project_rules(project_path)
    return rules, community, project


# Convenience function to load legacy combined config
def load_legacy_rules(path: Path) -> Dict[str, Any]:
    """
    Load a legacy combined rules file (validation-rules.yaml format).

    This is for backwards compatibility with the old validate_skill.py.

    Args:
        path: Path to the legacy rules file.

    Returns:
        Raw dictionary from the YAML file.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
