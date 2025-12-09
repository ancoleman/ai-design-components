"""
Blueprint validation for skillchain blueprints.

This module provides the BlueprintValidator class which validates
blueprint deliverables specifications against configured rules.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import yaml

from .rules import BlueprintRules, load_rules


@dataclass
class BlueprintResult:
    """Validation result for a single blueprint."""
    blueprint_name: str
    blueprint_path: str
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    deliverable_count: int = 0
    duration_ms: int = 0

    def add_error(self, message: str) -> None:
        """Add an error and mark as invalid."""
        self.is_valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """Add a warning."""
        self.warnings.append(message)


@dataclass
class BlueprintReport:
    """Validation report for multiple blueprints."""
    results: List[BlueprintResult] = field(default_factory=list)
    duration_ms: int = 0

    def add_result(self, result: BlueprintResult) -> None:
        """Add a result to the report."""
        self.results.append(result)

    @property
    def total(self) -> int:
        """Total number of blueprints validated."""
        return len(self.results)

    @property
    def passed(self) -> int:
        """Number of blueprints that passed."""
        return sum(1 for r in self.results if r.is_valid)

    @property
    def failed(self) -> int:
        """Number of blueprints that failed."""
        return self.total - self.passed

    @property
    def all_passed(self) -> bool:
        """True if all blueprints passed."""
        return all(r.is_valid for r in self.results)


class BlueprintValidator:
    """
    Blueprint validation engine.

    Validates skillchain blueprints against configured rules for
    deliverables specifications and maturity profiles.
    """

    def __init__(self, rules: Optional[BlueprintRules] = None):
        """
        Initialize the blueprint validator.

        Args:
            rules: BlueprintRules to use. If None, loads from default config.
        """
        if rules is None:
            validation_rules = load_rules()
            self.rules = validation_rules.blueprints
        else:
            self.rules = rules

        if self.rules is None:
            raise ValueError("No blueprint rules configured")

    def validate_blueprint(self, blueprint_path: Path) -> BlueprintResult:
        """
        Validate a single blueprint file.

        Args:
            blueprint_path: Path to the blueprint markdown file.

        Returns:
            BlueprintResult with validation details.
        """
        import time
        start = time.perf_counter()

        result = BlueprintResult(
            blueprint_name=blueprint_path.name,
            blueprint_path=str(blueprint_path)
        )

        # Check file exists
        if not blueprint_path.exists():
            result.add_error(f"File not found: {blueprint_path}")
            result.duration_ms = int((time.perf_counter() - start) * 1000)
            return result

        # Read file content
        try:
            content = blueprint_path.read_text(encoding='utf-8')
        except Exception as e:
            result.add_error(f"Failed to read file: {e}")
            result.duration_ms = int((time.perf_counter() - start) * 1000)
            return result

        # Check for required section
        if self.rules.required_section not in content:
            result.add_error(f"Missing '{self.rules.required_section}' section")
            result.duration_ms = int((time.perf_counter() - start) * 1000)
            return result

        # Extract and validate deliverables YAML
        deliverables_data, deliverables_error = self._extract_yaml_from_subsection(
            content, self.rules.required_section, "### Deliverables"
        )

        if deliverables_data is None:
            error_msg = "No valid YAML code block found in deliverables section"
            if deliverables_error:
                error_msg += f" ({deliverables_error})"
            result.add_error(error_msg)
            result.duration_ms = int((time.perf_counter() - start) * 1000)
            return result

        # Validate deliverables structure
        self._validate_deliverables(deliverables_data, result)

        # Extract and validate maturity profiles YAML
        profiles_data, profiles_error = self._extract_yaml_from_subsection(
            content, self.rules.required_section, "### Maturity Profiles"
        )

        if profiles_data is None:
            error_msg = "No valid YAML code block found in maturity profiles section"
            if profiles_error:
                error_msg += f" ({profiles_error})"
            result.add_error(error_msg)
            result.duration_ms = int((time.perf_counter() - start) * 1000)
            return result

        # Validate maturity profiles
        self._validate_maturity_profiles(profiles_data, result)

        result.duration_ms = int((time.perf_counter() - start) * 1000)
        return result

    def validate_all(self, blueprints_dir: Path) -> BlueprintReport:
        """
        Validate all blueprint files in a directory.

        Args:
            blueprints_dir: Path to the blueprints directory.

        Returns:
            BlueprintReport with all results.
        """
        import time
        start = time.perf_counter()

        report = BlueprintReport()

        if not blueprints_dir.exists():
            return report

        blueprint_files = sorted(blueprints_dir.glob("*.md"))

        for blueprint_file in blueprint_files:
            result = self.validate_blueprint(blueprint_file)
            report.add_result(result)

        report.duration_ms = int((time.perf_counter() - start) * 1000)
        return report

    def _extract_yaml_from_subsection(
        self,
        content: str,
        section_header: str,
        subsection_header: str
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Extract and parse YAML from a markdown code block in a subsection.

        Returns:
            Tuple of (parsed_data, error_message). Error is None if successful.
        """
        # Find the main section
        section_pattern = re.escape(section_header) + r'\s*\n(.*?)(?=\n## [^#]|\Z)'
        section_match = re.search(section_pattern, content, re.DOTALL | re.MULTILINE)

        if not section_match:
            return None, "Section not found"

        section_content = section_match.group(1)

        # Find the subsection within the section
        subsection_pattern = re.escape(subsection_header) + r'\s*\n(.*?)(?=\n### |\n## |\Z)'
        subsection_match = re.search(subsection_pattern, section_content, re.DOTALL | re.MULTILINE)

        if not subsection_match:
            return None, "Subsection not found"

        subsection_content = subsection_match.group(1)

        # Find YAML code block
        code_block_pattern = r'```(?:yaml|yml)\s*\n(.*?)```'
        code_block_match = re.search(code_block_pattern, subsection_content, re.DOTALL)

        if not code_block_match:
            return None, "No YAML code block found"

        yaml_content = code_block_match.group(1).strip()

        # Parse YAML
        try:
            data = yaml.safe_load(yaml_content)
            return data, None
        except yaml.YAMLError as e:
            error_msg = str(e).split('\n')[0]
            return None, f"YAML syntax error: {error_msg}"

    def _validate_deliverables(self, yaml_data: Dict, result: BlueprintResult) -> None:
        """Validate the deliverables structure."""
        # Check for 'deliverables' key
        if 'deliverables' not in yaml_data:
            result.add_error("Missing 'deliverables' key in YAML")
            return

        deliverables = yaml_data['deliverables']

        if not isinstance(deliverables, dict):
            result.add_error("'deliverables' must be a dictionary")
            return

        if not deliverables:
            result.add_error("'deliverables' must contain at least one deliverable")
            return

        result.deliverable_count = len(deliverables)

        required_fields = self.rules.get_required_deliverable_fields()
        all_valid_fields = self.rules.get_all_deliverable_fields()

        # Validate each deliverable
        for name, spec in deliverables.items():
            if not isinstance(spec, dict):
                result.add_error(f"Deliverable '{name}' must be a dictionary")
                continue

            # Check required fields
            missing_fields = required_fields - set(spec.keys())
            if missing_fields:
                result.add_error(f"Deliverable '{name}' missing required fields: {missing_fields}")

            # Validate primary_skill
            if 'primary_skill' in spec:
                if not isinstance(spec['primary_skill'], str):
                    result.add_error(f"Deliverable '{name}': 'primary_skill' must be a string")

            # Validate required_files
            if 'required_files' in spec:
                if not isinstance(spec['required_files'], list):
                    result.add_error(f"Deliverable '{name}': 'required_files' must be a list")
                elif not spec['required_files']:
                    result.add_error(f"Deliverable '{name}': 'required_files' cannot be empty")

            # Validate content_checks (optional)
            if 'content_checks' in spec:
                if not isinstance(spec['content_checks'], list):
                    result.add_error(f"Deliverable '{name}': 'content_checks' must be a list")
                else:
                    for i, check in enumerate(spec['content_checks']):
                        if not isinstance(check, dict):
                            result.add_error(f"Deliverable '{name}': content_check[{i}] must be a dict")
                        elif 'pattern' not in check or 'in' not in check:
                            result.add_error(f"Deliverable '{name}': content_check[{i}] missing 'pattern' or 'in'")

            # Validate maturity_required (optional)
            if 'maturity_required' in spec:
                maturity = spec['maturity_required']
                if not isinstance(maturity, list):
                    result.add_error(f"Deliverable '{name}': 'maturity_required' must be a list")
                else:
                    valid_levels = self.rules.get_required_maturity_profiles()
                    for level in maturity:
                        if level not in valid_levels:
                            result.add_error(f"Deliverable '{name}': invalid maturity level '{level}'")

            # Check for unexpected fields
            unexpected_fields = set(spec.keys()) - all_valid_fields
            if unexpected_fields:
                result.add_warning(f"Deliverable '{name}': unexpected fields: {unexpected_fields}")

    def _validate_maturity_profiles(self, yaml_data: Dict, result: BlueprintResult) -> None:
        """Validate the maturity profiles structure."""
        if 'maturity_profiles' not in yaml_data:
            result.add_error("Missing 'maturity_profiles' section")
            return

        profiles = yaml_data['maturity_profiles']

        if not isinstance(profiles, dict):
            result.add_error("'maturity_profiles' must be a dictionary")
            return

        # Check for required profiles
        required_profiles = self.rules.get_required_maturity_profiles()
        missing_profiles = required_profiles - set(profiles.keys())
        if missing_profiles:
            result.add_error(f"Missing required maturity profiles: {missing_profiles}")

        allowed_fields = self.rules.get_allowed_profile_fields()

        # Validate each profile
        for profile_name, profile_spec in profiles.items():
            if not isinstance(profile_spec, dict):
                result.add_error(f"Maturity profile '{profile_name}' must be a dictionary")
                continue

            # Check for unexpected fields
            unexpected_fields = set(profile_spec.keys()) - allowed_fields
            if unexpected_fields:
                result.add_warning(f"Profile '{profile_name}': unexpected fields: {unexpected_fields}")

            # Validate field types
            list_fields = ['require_additionally', 'skip_deliverables', 'empty_dirs_allowed',
                          'generation_adjustments', 'additional_deliverables']
            for field_name in list_fields:
                if field_name in profile_spec:
                    if not isinstance(profile_spec[field_name], list):
                        result.add_error(f"Profile '{profile_name}': '{field_name}' must be a list")

            # Validate description (optional)
            if 'description' in profile_spec:
                if not isinstance(profile_spec['description'], str):
                    result.add_error(f"Profile '{profile_name}': 'description' must be a string")
