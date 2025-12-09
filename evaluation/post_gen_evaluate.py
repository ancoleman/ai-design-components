#!/usr/bin/env python3
"""
Post-Generation Evaluation Script

Evaluates generated projects against blueprint promises and quality thresholds.

Usage:
    python post_gen_evaluate.py --project ~/Documents/repos/ml-pipeline-project --scenario S11
    python post_gen_evaluate.py --project ~/Documents/repos/ml-pipeline-project --blueprint ml-pipeline
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class CheckResult:
    """Result of a single check."""
    name: str
    passed: bool
    details: str = ""
    score: float = 0.0


@dataclass
class PostGenResult:
    """Full post-generation evaluation result."""
    project_path: str
    scenario_id: Optional[str] = None
    blueprint: Optional[str] = None

    # Scores (0-1)
    directory_completeness: float = 0.0
    runnability: float = 0.0
    blueprint_fulfillment: float = 0.0
    sample_data_availability: float = 0.0
    documentation_coverage: float = 0.0

    # Detailed results
    checks: List[CheckResult] = field(default_factory=list)
    empty_directories: List[str] = field(default_factory=list)
    empty_modules: List[str] = field(default_factory=list)
    missing_promises: List[str] = field(default_factory=list)

    # Overall
    overall_score: float = 0.0
    passed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_path": self.project_path,
            "scenario_id": self.scenario_id,
            "blueprint": self.blueprint,
            "scores": {
                "directory_completeness": round(self.directory_completeness, 2),
                "runnability": round(self.runnability, 2),
                "blueprint_fulfillment": round(self.blueprint_fulfillment, 2),
                "sample_data_availability": round(self.sample_data_availability, 2),
                "documentation_coverage": round(self.documentation_coverage, 2),
            },
            "overall_score": round(self.overall_score, 2),
            "passed": self.passed,
            "details": {
                "empty_directories": self.empty_directories,
                "empty_modules": self.empty_modules,
                "missing_promises": self.missing_promises,
                "checks": [
                    {"name": c.name, "passed": c.passed, "details": c.details}
                    for c in self.checks
                ],
            },
        }


class PostGenEvaluator:
    """Evaluates generated projects for quality and completeness."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.result = PostGenResult(project_path=str(project_path))

    def evaluate(
        self,
        scenario: Optional[Dict] = None,
        blueprint_promises: Optional[List[str]] = None,
    ) -> PostGenResult:
        """Run full post-generation evaluation."""

        print(f"\n{'='*60}")
        print(f"POST-GENERATION EVALUATION: {self.project_path.name}")
        print(f"{'='*60}\n")

        # 1. Directory completeness
        self.result.directory_completeness = self._check_directory_completeness()
        print(f"[1/5] Directory Completeness: {self.result.directory_completeness:.0%}")

        # 2. Runnability
        self.result.runnability = self._check_runnability()
        print(f"[2/5] Runnability: {self.result.runnability:.0%}")

        # 3. Blueprint fulfillment
        if scenario and "post_generation" in scenario:
            promises = scenario["post_generation"].get("blueprint_promises", [])
            self.result.blueprint_fulfillment = self._check_blueprint_fulfillment(promises)
        elif blueprint_promises:
            self.result.blueprint_fulfillment = self._check_blueprint_fulfillment_simple(
                blueprint_promises
            )
        else:
            self.result.blueprint_fulfillment = 1.0  # No promises = 100%
        print(f"[3/5] Blueprint Fulfillment: {self.result.blueprint_fulfillment:.0%}")

        # 4. Sample data availability
        self.result.sample_data_availability = self._check_sample_data()
        print(f"[4/5] Sample Data: {self.result.sample_data_availability:.0%}")

        # 5. Documentation coverage
        self.result.documentation_coverage = self._check_documentation()
        print(f"[5/5] Documentation: {self.result.documentation_coverage:.0%}")

        # Calculate overall score (weighted)
        weights = {
            "directory_completeness": 0.20,
            "runnability": 0.25,
            "blueprint_fulfillment": 0.25,
            "sample_data_availability": 0.15,
            "documentation_coverage": 0.15,
        }

        self.result.overall_score = sum(
            getattr(self.result, k) * v for k, v in weights.items()
        )

        # Pass if all thresholds met
        thresholds = {
            "directory_completeness": 0.70,
            "runnability": 0.80,  # Allow some test failures
            "blueprint_fulfillment": 0.80,
            "sample_data_availability": 0.50,  # At least something
            "documentation_coverage": 0.60,
        }

        self.result.passed = all(
            getattr(self.result, k) >= v for k, v in thresholds.items()
        )

        print(f"\n{'='*60}")
        print(f"OVERALL SCORE: {self.result.overall_score:.0%}")
        print(f"PASSED: {'YES' if self.result.passed else 'NO'}")
        print(f"{'='*60}\n")

        return self.result

    def _check_directory_completeness(self) -> float:
        """Check what % of directories have actual content."""
        dirs_with_content = 0
        total_dirs = 0

        for dir_path in self.project_path.rglob("*"):
            if not dir_path.is_dir():
                continue
            if ".git" in str(dir_path):
                continue
            if "__pycache__" in str(dir_path):
                continue

            total_dirs += 1
            files = [
                f for f in dir_path.iterdir()
                if f.is_file() and f.name != ".gitkeep"
            ]

            if files:
                dirs_with_content += 1
            else:
                rel_path = str(dir_path.relative_to(self.project_path))
                self.result.empty_directories.append(rel_path)

        if total_dirs == 0:
            return 0.0

        return dirs_with_content / total_dirs

    def _check_runnability(self) -> float:
        """Check if project can install and run tests."""
        checks_passed = 0
        total_checks = 3

        # Check 1: Dependencies can be resolved
        if (self.project_path / "pyproject.toml").exists():
            try:
                result = subprocess.run(
                    ["poetry", "check"],
                    cwd=self.project_path,
                    capture_output=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    checks_passed += 1
                    self.result.checks.append(
                        CheckResult("poetry_check", True, "pyproject.toml is valid")
                    )
                else:
                    self.result.checks.append(
                        CheckResult("poetry_check", False, result.stderr.decode()[:200])
                    )
            except Exception as e:
                self.result.checks.append(
                    CheckResult("poetry_check", False, str(e))
                )
        elif (self.project_path / "package.json").exists():
            checks_passed += 1  # Assume npm projects are valid
            self.result.checks.append(
                CheckResult("npm_check", True, "package.json exists")
            )
        else:
            total_checks -= 1  # No package manager

        # Check 2: Tests exist and can be collected
        if (self.project_path / "tests").exists():
            try:
                result = subprocess.run(
                    ["poetry", "run", "pytest", "--collect-only", "-q"],
                    cwd=self.project_path,
                    capture_output=True,
                    timeout=60,
                )
                if result.returncode == 0:
                    checks_passed += 1
                    output = result.stdout.decode()
                    test_count = len([l for l in output.split("\n") if "test_" in l])
                    self.result.checks.append(
                        CheckResult("tests_collect", True, f"{test_count} tests found")
                    )
                else:
                    self.result.checks.append(
                        CheckResult("tests_collect", False, "Tests failed to collect")
                    )
            except Exception as e:
                self.result.checks.append(
                    CheckResult("tests_collect", False, str(e))
                )
        else:
            total_checks -= 1

        # Check 3: Main module can be imported
        src_init = self.project_path / "src" / "__init__.py"
        if src_init.exists() or (self.project_path / "src").exists():
            try:
                result = subprocess.run(
                    ["poetry", "run", "python", "-c", "import src"],
                    cwd=self.project_path,
                    capture_output=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    checks_passed += 1
                    self.result.checks.append(
                        CheckResult("import_src", True, "src module imports")
                    )
                else:
                    self.result.checks.append(
                        CheckResult("import_src", False, result.stderr.decode()[:200])
                    )
            except Exception as e:
                self.result.checks.append(
                    CheckResult("import_src", False, str(e))
                )

        if total_checks == 0:
            return 0.0

        return checks_passed / total_checks

    def _check_blueprint_fulfillment(self, promises: List[Dict]) -> float:
        """Check blueprint promises with shell commands."""
        if not promises:
            return 1.0

        fulfilled = 0

        for promise in promises:
            name = promise.get("name", "unknown")
            check_cmd = promise.get("check", "")

            try:
                result = subprocess.run(
                    check_cmd,
                    shell=True,
                    cwd=self.project_path,
                    capture_output=True,
                    timeout=10,
                )
                passed = result.returncode == 0 and result.stdout.decode().strip()

                if passed:
                    fulfilled += 1
                    self.result.checks.append(
                        CheckResult(f"promise_{name}", True, "Delivered")
                    )
                else:
                    self.result.missing_promises.append(name)
                    self.result.checks.append(
                        CheckResult(f"promise_{name}", False, "Not found")
                    )
            except Exception as e:
                self.result.missing_promises.append(name)
                self.result.checks.append(
                    CheckResult(f"promise_{name}", False, str(e))
                )

        return fulfilled / len(promises)

    def _check_blueprint_fulfillment_simple(self, promises: List[str]) -> float:
        """Simple keyword-based blueprint fulfillment check."""
        if not promises:
            return 1.0

        fulfilled = 0
        checks = {
            "mlflow": lambda: self._grep_exists("mlflow", "src/"),
            "feature store": lambda: self._has_content("src/features/"),
            "feast": lambda: self._grep_exists("feast", "src/"),
            "kubernetes": lambda: self._has_content("infrastructure/kubernetes/"),
            "grafana": lambda: self._has_content("monitoring/grafana/dashboards/"),
            "sample data": lambda: (
                self._has_content("data/raw/") or
                (self.project_path / "scripts" / "generate_sample_data.py").exists()
            ),
            "notebooks": lambda: self._has_content("notebooks/"),
            "docker": lambda: list(self.project_path.glob("**/Dockerfile*")),
            "prometheus": lambda: self._grep_exists("prometheus", "."),
        }

        for promise in promises:
            promise_lower = promise.lower()
            for keyword, check_fn in checks.items():
                if keyword in promise_lower:
                    try:
                        if check_fn():
                            fulfilled += 1
                            break
                    except:
                        pass
            else:
                self.result.missing_promises.append(promise)

        return fulfilled / len(promises) if promises else 1.0

    def _check_sample_data(self) -> float:
        """Check if sample data or generation script exists."""
        checks = [
            # Sample data files
            list((self.project_path / "data" / "raw").glob("*.csv")),
            list((self.project_path / "data" / "raw").glob("*.json")),
            list((self.project_path / "data" / "raw").glob("*.parquet")),
            # Generation scripts
            (self.project_path / "scripts" / "generate_sample_data.py").exists(),
            (self.project_path / "scripts" / "generate_data.py").exists(),
            (self.project_path / "scripts" / "seed_data.py").exists(),
        ]

        # Check README for data generation snippet
        readme = self.project_path / "README.md"
        if readme.exists():
            content = readme.read_text()
            if "sample data" in content.lower() or "generate" in content.lower():
                # Has instructions at least
                checks.append(True)

        if any(checks):
            self.result.checks.append(
                CheckResult("sample_data", True, "Sample data or script found")
            )
            return 1.0
        else:
            self.result.checks.append(
                CheckResult("sample_data", False, "No sample data found")
            )
            return 0.0

    def _check_documentation(self) -> float:
        """Check documentation coverage."""
        score = 0.0
        total = 5

        readme = self.project_path / "README.md"
        if not readme.exists():
            return 0.0

        content = readme.read_text().lower()

        # Check for key sections
        sections = [
            ("quick start", ["quick start", "getting started", "installation"]),
            ("project structure", ["project structure", "directory", "├──"]),
            ("configuration", ["config", "configuration", "yaml", "settings"]),
            ("usage", ["usage", "how to", "example"]),
            ("testing", ["test", "pytest", "make test"]),
        ]

        for section_name, keywords in sections:
            if any(kw in content for kw in keywords):
                score += 1
                self.result.checks.append(
                    CheckResult(f"doc_{section_name}", True, "Present")
                )
            else:
                self.result.checks.append(
                    CheckResult(f"doc_{section_name}", False, "Missing")
                )

        return score / total

    def _grep_exists(self, pattern: str, path: str) -> bool:
        """Check if pattern exists in path."""
        try:
            result = subprocess.run(
                f"grep -r '{pattern}' {path}",
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                timeout=10,
            )
            return result.returncode == 0
        except:
            return False

    def _has_content(self, path: str) -> bool:
        """Check if directory has content beyond .gitkeep."""
        full_path = self.project_path / path
        if not full_path.exists():
            return False

        files = [
            f for f in full_path.iterdir()
            if f.is_file() and f.name != ".gitkeep"
        ]
        return len(files) > 0


def find_empty_modules(project_path: Path) -> List[str]:
    """Find Python modules with only docstrings/imports."""
    empty = []

    for py_file in project_path.rglob("*.py"):
        if ".git" in str(py_file) or "__pycache__" in str(py_file):
            continue

        try:
            content = py_file.read_text()
        except:
            continue

        # Remove docstrings
        cleaned = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)
        cleaned = re.sub(r"'''.*?'''", '', cleaned, flags=re.DOTALL)
        # Remove comments
        cleaned = re.sub(r'#.*$', '', cleaned, flags=re.MULTILINE)
        # Remove imports
        cleaned = re.sub(r'^from\s+.*$', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'^import\s+.*$', '', cleaned, flags=re.MULTILINE)
        # Remove __all__
        cleaned = re.sub(r'^__all__\s*=.*$', '', cleaned, flags=re.MULTILINE)
        # Remove empty lines
        cleaned = cleaned.strip()

        if not cleaned:
            rel_path = str(py_file.relative_to(project_path))
            empty.append(rel_path)

    return empty


def load_scenario(scenario_id: str) -> Optional[Dict]:
    """Load scenario from scenarios.yaml."""
    scenarios_file = Path(__file__).parent / "scenarios.yaml"
    if not scenarios_file.exists():
        return None

    with open(scenarios_file) as f:
        data = yaml.safe_load(f)

    for scenario in data.get("scenarios", []):
        if scenario.get("id") == scenario_id:
            return scenario

    return None


def main():
    parser = argparse.ArgumentParser(description="Post-generation project evaluation")
    parser.add_argument("--project", "-p", required=True, help="Path to generated project")
    parser.add_argument("--scenario", "-s", help="Scenario ID (e.g., S11)")
    parser.add_argument("--blueprint", "-b", help="Blueprint name (e.g., ml-pipeline)")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    project_path = Path(args.project).expanduser().resolve()
    if not project_path.exists():
        print(f"ERROR: Project path does not exist: {project_path}")
        sys.exit(1)

    evaluator = PostGenEvaluator(project_path)

    # Load scenario if specified
    scenario = None
    if args.scenario:
        scenario = load_scenario(args.scenario)
        if not scenario:
            print(f"WARNING: Scenario {args.scenario} not found")

    # Run evaluation
    result = evaluator.evaluate(scenario=scenario)

    # Find empty modules
    result.empty_modules = find_empty_modules(project_path)
    if result.empty_modules:
        print(f"\nEmpty modules found ({len(result.empty_modules)}):")
        for m in result.empty_modules[:10]:
            print(f"  - {m}")
        if len(result.empty_modules) > 10:
            print(f"  ... and {len(result.empty_modules) - 10} more")

    # Print summary
    if result.empty_directories:
        print(f"\nEmpty directories ({len(result.empty_directories)}):")
        for d in result.empty_directories[:10]:
            print(f"  - {d}")

    if result.missing_promises:
        print(f"\nMissing blueprint promises:")
        for p in result.missing_promises:
            print(f"  - {p}")

    # Save output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\nResults saved to: {output_path}")

    # Exit code based on pass/fail
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
