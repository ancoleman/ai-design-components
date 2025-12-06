#!/usr/bin/env python3
"""
GitHub Actions Workflow Validator

Validates GitHub Actions workflow YAML files for syntax errors,
common mistakes, and best practices.

Usage:
    python validate_workflow.py <workflow-file>
    python validate_workflow.py .github/workflows/ci.yml
"""

import sys
import yaml
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple


class WorkflowValidator:
    def __init__(self, workflow_path: str):
        self.workflow_path = Path(workflow_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.workflow: Dict[str, Any] = {}

    def validate(self) -> bool:
        """Run all validations. Returns True if valid."""
        if not self.workflow_path.exists():
            self.errors.append(f"File not found: {self.workflow_path}")
            return False

        if not self._load_yaml():
            return False

        self._validate_structure()
        self._validate_triggers()
        self._validate_permissions()
        self._validate_jobs()
        self._validate_actions()
        self._validate_secrets()

        return len(self.errors) == 0

    def _load_yaml(self) -> bool:
        """Load and parse YAML file."""
        try:
            with open(self.workflow_path, 'r') as f:
                self.workflow = yaml.safe_load(f)
            return True
        except yaml.YAMLError as e:
            self.errors.append(f"YAML syntax error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return False

    def _validate_structure(self):
        """Validate basic workflow structure."""
        required_keys = ['name', 'on', 'jobs']
        for key in required_keys:
            if key not in self.workflow:
                self.errors.append(f"Missing required key: '{key}'")

        if 'name' in self.workflow and not self.workflow['name']:
            self.errors.append("Workflow name cannot be empty")

    def _validate_triggers(self):
        """Validate trigger events."""
        if 'on' not in self.workflow:
            return

        triggers = self.workflow['on']

        # Check for common trigger mistakes
        if isinstance(triggers, dict):
            if 'pull_request_target' in triggers:
                self.warnings.append(
                    "Using 'pull_request_target' can be dangerous - "
                    "ensure proper validation of untrusted code"
                )

            if 'push' in triggers and isinstance(triggers['push'], dict):
                if 'branches' in triggers['push']:
                    branches = triggers['push']['branches']
                    if '*' in branches:
                        self.warnings.append(
                            "Using wildcard '*' in push branches - "
                            "consider being more specific"
                        )

    def _validate_permissions(self):
        """Validate permissions configuration."""
        if 'permissions' not in self.workflow:
            self.warnings.append(
                "No permissions specified - consider using least privilege"
            )
            return

        permissions = self.workflow['permissions']

        # Check for overly broad permissions
        if permissions == 'write-all':
            self.warnings.append(
                "Using 'write-all' permissions - consider specifying minimal permissions"
            )

        if isinstance(permissions, dict):
            if permissions.get('contents') == 'write':
                self.warnings.append(
                    "Using 'contents: write' - ensure this is necessary"
                )

    def _validate_jobs(self):
        """Validate job definitions."""
        if 'jobs' not in self.workflow:
            return

        jobs = self.workflow['jobs']

        if not jobs:
            self.errors.append("No jobs defined in workflow")
            return

        for job_name, job_config in jobs.items():
            self._validate_job(job_name, job_config)

    def _validate_job(self, job_name: str, job_config: Dict[str, Any]):
        """Validate individual job configuration."""
        # Check for uses (reusable workflow) vs steps
        if 'uses' in job_config:
            # Reusable workflow
            if 'steps' in job_config:
                self.errors.append(
                    f"Job '{job_name}' cannot have both 'uses' and 'steps'"
                )
            return

        # Regular job
        if 'runs-on' not in job_config:
            self.errors.append(f"Job '{job_name}' missing 'runs-on'")

        if 'steps' not in job_config:
            self.errors.append(f"Job '{job_name}' missing 'steps'")
            return

        steps = job_config['steps']
        if not steps:
            self.errors.append(f"Job '{job_name}' has no steps")

        for i, step in enumerate(steps):
            self._validate_step(job_name, i, step)

    def _validate_step(self, job_name: str, step_index: int, step: Dict[str, Any]):
        """Validate individual step configuration."""
        step_id = f"{job_name}[{step_index}]"

        # Step must have either 'run' or 'uses'
        if 'run' not in step and 'uses' not in step:
            self.errors.append(
                f"Step {step_id} must have either 'run' or 'uses'"
            )

        # Step cannot have both 'run' and 'uses'
        if 'run' in step and 'uses' in step:
            self.errors.append(
                f"Step {step_id} cannot have both 'run' and 'uses'"
            )

        # Check for name (recommended)
        if 'name' not in step:
            self.warnings.append(
                f"Step {step_id} missing 'name' (recommended for clarity)"
            )

    def _validate_actions(self):
        """Validate action usage."""
        if 'jobs' not in self.workflow:
            return

        for job_name, job_config in self.workflow['jobs'].items():
            if 'steps' not in job_config:
                continue

            for step in job_config['steps']:
                if 'uses' not in step:
                    continue

                action = step['uses']
                self._validate_action_version(job_name, action)

    def _validate_action_version(self, job_name: str, action: str):
        """Validate action version pinning."""
        # Check for unpinned versions
        if '@' not in action:
            self.errors.append(
                f"Action '{action}' in job '{job_name}' not pinned to version"
            )
            return

        # Check for mutable references
        parts = action.split('@')
        if len(parts) != 2:
            return

        version = parts[1]

        # Major version only (e.g., v4)
        if re.match(r'^v\d+$', version):
            self.warnings.append(
                f"Action '{action}' uses mutable major version - "
                f"consider pinning to commit SHA or full version"
            )

        # Branch name
        if version in ['main', 'master', 'develop']:
            self.warnings.append(
                f"Action '{action}' pinned to branch '{version}' - "
                f"this is mutable and less secure"
            )

    def _validate_secrets(self):
        """Validate secret usage."""
        workflow_str = str(self.workflow)

        # Check for hardcoded secrets (common patterns)
        secret_patterns = [
            r'password["\s]*:["\s]*[^$]',
            r'api[_-]?key["\s]*:["\s]*[^$]',
            r'token["\s]*:["\s]*[^$]',
        ]

        for pattern in secret_patterns:
            if re.search(pattern, workflow_str, re.IGNORECASE):
                self.warnings.append(
                    f"Possible hardcoded secret detected (pattern: {pattern}) - "
                    f"use ${{{{ secrets.SECRET_NAME }}}}"
                )

    def print_results(self):
        """Print validation results."""
        print(f"\nValidating: {self.workflow_path}")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ Workflow is valid!")

        print("\n" + "=" * 60)

        if self.errors:
            print("❌ VALIDATION FAILED")
            return False
        else:
            print("✅ VALIDATION PASSED")
            return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_workflow.py <workflow-file>")
        print("Example: python validate_workflow.py .github/workflows/ci.yml")
        sys.exit(1)

    workflow_path = sys.argv[1]
    validator = WorkflowValidator(workflow_path)

    is_valid = validator.validate()
    validator.print_results()

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
