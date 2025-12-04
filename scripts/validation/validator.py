"""
Core validation engine for skill validation.

This module provides the Validator class which performs validation
of individual skills and batches of skills against configured rules
and community practices.
"""

import re
from pathlib import Path
from typing import List, Optional, Iterator, Callable

import yaml

from .result import ValidationResult, ValidationReport, Timer
from .rules import (
    ValidationRules, CommunityPractices, ProjectRules,
    load_rules, load_community_practices, load_project_rules
)


class Validator:
    """
    Skill validation engine.

    Validates skills against configured rules and optionally checks
    community practices for suggestions.
    """

    def __init__(
        self,
        rules: Optional[ValidationRules] = None,
        community: Optional[CommunityPractices] = None,
        project: Optional[ProjectRules] = None,
        include_community: bool = True,
        include_project: bool = True
    ):
        """
        Initialize the validator.

        Args:
            rules: ValidationRules to use. If None, loads default.
            community: CommunityPractices to use. If None, loads default.
            project: ProjectRules to use. If None, loads default.
            include_community: Whether to include community practice checks.
            include_project: Whether to include project-specific rule checks.
        """
        self.rules = rules or load_rules()

        # Load community practices
        self.community = community if include_community else None
        if include_community and community is None:
            try:
                self.community = load_community_practices()
            except FileNotFoundError:
                self.community = None

        # Load project rules
        self.project = project if include_project else None
        if include_project and project is None:
            try:
                self.project = load_project_rules()
            except FileNotFoundError:
                self.project = None

    def validate_skill(self, skill_path: Path) -> ValidationResult:
        """
        Validate a single skill.

        Args:
            skill_path: Path to the skill directory.

        Returns:
            ValidationResult with errors, warnings, and suggestions.
        """
        skill_path = Path(skill_path)
        result = ValidationResult(
            skill_name=skill_path.name,
            skill_path=str(skill_path)
        )

        with Timer() as timer:
            # Check SKILL.md exists
            skill_md_path = skill_path / "SKILL.md"
            if not skill_md_path.exists():
                result.add_error("SKILL.md not found", "skill_md.required")
                result.duration_ms = timer.elapsed_ms
                return result

            # Read content
            try:
                content = skill_md_path.read_text(encoding='utf-8', errors='replace')
            except Exception as e:
                result.add_error(f"Failed to read SKILL.md: {e}", "skill_md.read")
                result.duration_ms = timer.elapsed_ms
                return result

            lines = content.split('\n')

            # Validate frontmatter
            self._validate_frontmatter(content, lines, result)

            # Validate body length
            self._validate_body_length(lines, result)

            # Check anti-patterns
            self._check_anti_patterns(content, result)

            # Validate references
            self._validate_references(skill_path, content, result)

            # Validate examples
            self._validate_examples(skill_path, content, result)

            # Check community practices (suggestions only)
            if self.community:
                self._check_community_practices(content, result)

            # Check project-specific rules
            if self.project:
                self._check_project_rules(content, result)

        result.duration_ms = timer.elapsed_ms
        return result

    def validate_all(
        self,
        skills_dir: Path,
        completed_only: bool = False,
        phase: Optional[int] = None,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> ValidationReport:
        """
        Validate all skills in a directory.

        Args:
            skills_dir: Path to the skills directory.
            completed_only: Only validate skills with SKILL.md.
            phase: Only validate skills in this phase.
            progress_callback: Called with (skill_name, current, total) for progress.

        Returns:
            ValidationReport with all results.
        """
        skills_dir = Path(skills_dir)
        report = ValidationReport()

        # Collect skills to validate
        skills_to_check = list(self._collect_skills(
            skills_dir, completed_only, phase
        ))
        total = len(skills_to_check)

        with Timer() as timer:
            for i, skill_path in enumerate(skills_to_check):
                if progress_callback:
                    progress_callback(skill_path.name, i + 1, total)

                result = self.validate_skill(skill_path)
                report.add_result(result)

        report.duration_ms = timer.elapsed_ms
        return report

    def _collect_skills(
        self,
        skills_dir: Path,
        completed_only: bool,
        phase: Optional[int]
    ) -> Iterator[Path]:
        """Collect skill directories to validate."""
        if phase is not None:
            # Only skills in the specified phase
            phase_skills = self.rules.get_phase_skills(phase)
            for name in phase_skills:
                skill_path = skills_dir / name
                if skill_path.exists() and skill_path.is_dir():
                    if not completed_only or (skill_path / "SKILL.md").exists():
                        yield skill_path
        else:
            # All skills
            for skill_path in sorted(skills_dir.iterdir()):
                if skill_path.is_dir():
                    if completed_only:
                        if (skill_path / "SKILL.md").exists():
                            yield skill_path
                    else:
                        # Include if has SKILL.md or init.md
                        if (skill_path / "SKILL.md").exists() or \
                           (skill_path / "init.md").exists():
                            yield skill_path

    def _validate_frontmatter(
        self,
        content: str,
        lines: List[str],
        result: ValidationResult
    ) -> None:
        """Validate YAML frontmatter."""
        fm_rules = self.rules.frontmatter

        # Check frontmatter exists
        if not content.startswith('---'):
            result.add_error("Missing frontmatter (must start with ---)", "frontmatter.missing")
            return

        # Find frontmatter end
        try:
            end_idx = lines[1:].index('---') + 1
        except ValueError:
            result.add_error("Frontmatter not closed (missing ---)", "frontmatter.unclosed")
            return

        # Parse frontmatter
        fm_content = '\n'.join(lines[1:end_idx])
        try:
            frontmatter = yaml.safe_load(fm_content)
        except yaml.YAMLError as e:
            result.add_error(f"Invalid frontmatter YAML: {e}", "frontmatter.invalid")
            return

        if not isinstance(frontmatter, dict):
            result.add_error("Frontmatter must be a YAML mapping", "frontmatter.type")
            return

        # Check required fields
        for field in fm_rules.get("required_fields", []):
            if field not in frontmatter:
                result.add_error(f"Missing required field: {field}", f"frontmatter.{field}.missing")

        # Validate name field
        if "name" in frontmatter:
            self._validate_name(frontmatter["name"], result)

        # Validate description field
        if "description" in frontmatter:
            self._validate_description(frontmatter["description"], result)

    def _validate_name(self, name: str, result: ValidationResult) -> None:
        """Validate the name field."""
        name_rules = self.rules.frontmatter.get("name", {})

        # Check max length
        max_len = name_rules.get("max_length", 64)
        if len(name) > max_len:
            result.add_error(
                f"Name too long: {len(name)} chars (max {max_len})",
                "frontmatter.name.length"
            )

        # Check pattern
        pattern = name_rules.get("pattern", r"^[a-z0-9-]+$")
        if not re.match(pattern, name):
            desc = name_rules.get("pattern_description", "invalid format")
            result.add_error(f"Name '{name}' invalid: {desc}", "frontmatter.name.pattern")

        # Check leading/trailing hyphens
        if name_rules.get("no_leading_hyphen") and name.startswith('-'):
            result.add_error("Name cannot start with hyphen", "frontmatter.name.leading_hyphen")
        if name_rules.get("no_trailing_hyphen") and name.endswith('-'):
            result.add_error("Name cannot end with hyphen", "frontmatter.name.trailing_hyphen")

        # Check consecutive hyphens
        if name_rules.get("no_consecutive_hyphens") and '--' in name:
            result.add_error("Name cannot have consecutive hyphens", "frontmatter.name.consecutive_hyphens")

        # Check reserved words
        for word in name_rules.get("reserved_words", []):
            if word.lower() in name.lower():
                result.add_error(f"Name contains reserved word: {word}", "frontmatter.name.reserved")

        # Check preferred format (warning)
        pref = name_rules.get("preferred_format", {})
        if pref and pref.get("pattern"):
            if not re.search(pref["pattern"], name):
                desc = pref.get("description", "preferred format")
                result.add_warning(f"Name '{name}' doesn't use {desc}", "frontmatter.name.preferred")

    def _validate_description(self, desc: str, result: ValidationResult) -> None:
        """Validate the description field."""
        desc_rules = self.rules.frontmatter.get("description", {})

        # Check length
        max_len = desc_rules.get("max_length", 1024)
        if len(desc) > max_len:
            result.add_error(
                f"Description too long: {len(desc)} chars (max {max_len})",
                "frontmatter.description.length"
            )

        min_len = desc_rules.get("min_length", 1)
        if len(desc) < min_len:
            result.add_error("Description too short", "frontmatter.description.empty")

        # Check for XML tags
        if desc_rules.get("no_xml_tags") and re.search(r'<[^>]+>', desc):
            result.add_error("Description contains XML-like tags", "frontmatter.description.xml_tags")

        # Check for "when" keywords (warning)
        when_check = desc_rules.get("should_include_when", {})
        if when_check:
            keywords = when_check.get("keywords", [])
            has_when = any(kw in desc for kw in keywords)
            if not has_when:
                result.add_warning(
                    "Description should indicate when to use this skill",
                    "frontmatter.description.when"
                )

    def _validate_body_length(self, lines: List[str], result: ValidationResult) -> None:
        """Validate SKILL.md body length."""
        max_lines = self.rules.skill_md.get("max_lines", 500)

        # Find where body starts (after frontmatter)
        try:
            end_idx = lines[1:].index('---') + 2
            body_lines = len(lines) - end_idx
            if body_lines > max_lines:
                result.add_warning(
                    f"SKILL.md body too long: {body_lines} lines (recommended max {max_lines})",
                    "skill_md.length"
                )
        except ValueError:
            pass  # Frontmatter issue already reported

    def _check_anti_patterns(self, content: str, result: ValidationResult) -> None:
        """Check for anti-patterns in content."""
        for anti_pattern in self.rules.anti_patterns:
            if not anti_pattern.enabled:
                continue

            matches = anti_pattern.find_matches(content)
            if matches:
                count = len(matches)
                msg = f"{anti_pattern.message} ({count} instance{'s' if count > 1 else ''})"

                if anti_pattern.severity == "error":
                    result.add_error(msg, f"anti_pattern.{anti_pattern.name}")
                else:
                    result.add_warning(msg, f"anti_pattern.{anti_pattern.name}")

    def _validate_references(
        self,
        skill_path: Path,
        content: str,
        result: ValidationResult
    ) -> None:
        """Validate referenced files exist and check structure."""
        ref_rules = self.rules.references
        ref_pattern = r'references/[a-z0-9_-]+\.md'

        referenced_files = set(re.findall(ref_pattern, content))

        for ref in referenced_files:
            ref_path = skill_path / ref

            if not ref_path.exists():
                result.add_error(f"Missing reference file: {ref}", "references.missing")
                continue

            # Check for nested references
            try:
                ref_content = ref_path.read_text(encoding='utf-8', errors='replace')
                if re.search(ref_pattern, ref_content):
                    max_depth = ref_rules.get("max_depth", 1)
                    result.add_error(
                        f"Nested reference in {ref} (max depth is {max_depth})",
                        "references.nested"
                    )

                # Check for ToC in long files
                ref_lines = len(ref_content.split('\n'))
                toc_threshold = ref_rules.get("toc_threshold", 100)
                if ref_lines > toc_threshold:
                    toc_patterns = ref_rules.get("toc_patterns", [
                        r'^## Table of Contents',
                        r'^## Contents'
                    ])
                    has_toc = any(
                        re.search(p, ref_content, re.MULTILINE)
                        for p in toc_patterns
                    )
                    if not has_toc and not ref_rules.get("toc_required", False):
                        result.add_warning(
                            f"Reference {ref} ({ref_lines} lines) should have Table of Contents",
                            "references.toc"
                        )
            except Exception:
                pass  # Ignore read errors for reference files

    def _validate_examples(
        self,
        skill_path: Path,
        content: str,
        result: ValidationResult
    ) -> None:
        """Validate referenced example files exist."""
        example_pattern = r'examples/[a-zA-Z0-9_/-]+\.[a-z]+'
        referenced_examples = set(re.findall(example_pattern, content))

        for example in referenced_examples:
            example_path = skill_path / example
            if not example_path.exists():
                result.add_error(f"Missing example file: {example}", "examples.missing")

    def _check_community_practices(
        self,
        content: str,
        result: ValidationResult
    ) -> None:
        """Check community practices and add suggestions."""
        if not self.community:
            return

        for practice in self.community.get_auto_checkable_practices():
            # Check by keywords
            if practice.keywords:
                found = any(
                    re.search(kw, content, re.IGNORECASE)
                    for kw in practice.keywords
                )
                if not found:
                    msg = practice.message or practice.description
                    result.add_suggestion(msg, f"community.{practice.name}")

            # Check by pattern
            elif practice.pattern:
                if not re.search(practice.pattern, content):
                    msg = practice.message or practice.description
                    result.add_suggestion(msg, f"community.{practice.name}")

    def _check_project_rules(
        self,
        content: str,
        result: ValidationResult
    ) -> None:
        """Check project-specific rules."""
        if not self.project:
            return

        for rule in self.project.get_enabled_rules():
            # Check if rule applies to this content
            if not rule.applies_to_content(content):
                continue

            # Keyword-based checks
            if rule.check_type == "keyword":
                if not rule.check_keywords(content):
                    if rule.severity == "error":
                        result.add_error(rule.message, f"project.{rule.name}")
                    else:
                        result.add_warning(rule.message, f"project.{rule.name}")
