#!/usr/bin/env python3
"""
AI Design Components - Skillchain Evaluation Framework
Validates skill detection, blueprint matching, and workflow quality.

Usage:
    python evaluate.py                    # Run all scenarios
    python evaluate.py --scenario S01     # Run specific scenario
    python evaluate.py --domain frontend  # Run domain scenarios
    python evaluate.py --report           # Generate evaluation report
"""

import yaml
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SCENARIOS_FILE = SCRIPT_DIR / "scenarios.yaml"
# Updated for skillchain v3.0 directory structure
REGISTRIES_DIR = PROJECT_ROOT / ".claude-commands" / "skillchain-data" / "registries"
BLUEPRINTS_DIR = PROJECT_ROOT / ".claude-commands" / "skillchain" / "blueprints"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class EvaluationResult:
    """Result of evaluating a single scenario."""
    scenario_id: str
    scenario_name: str
    domain: str
    passed: bool
    scores: Dict[str, float] = field(default_factory=dict)
    skill_detection: Dict = field(default_factory=dict)
    blueprint_detection: Dict = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class EvaluationReport:
    """Complete evaluation report."""
    timestamp: str
    total_scenarios: int
    passed: int
    failed: int
    results: List[EvaluationResult] = field(default_factory=list)
    overall_score: float = 0.0


# =============================================================================
# Registry Loading
# =============================================================================

def load_registries() -> Dict[str, Dict]:
    """Load all domain registries."""
    registries = {}

    index_file = REGISTRIES_DIR / "_index.yaml"
    if not index_file.exists():
        print(f"ERROR: Registry index not found at {index_file}")
        return registries

    with open(index_file) as f:
        index = yaml.safe_load(f)

    for domain, info in index.get("domains", {}).items():
        registry_file = REGISTRIES_DIR / info.get("file", f"{domain}.yaml")
        if registry_file.exists():
            with open(registry_file) as f:
                registries[domain] = yaml.safe_load(f)

    return registries


def load_blueprints() -> Dict[str, Dict]:
    """Load blueprint metadata from files."""
    blueprints = {}

    for bp_file in BLUEPRINTS_DIR.glob("*.md"):
        blueprint_name = bp_file.stem
        content = bp_file.read_text()

        # Extract trigger keywords
        keywords = {"primary": [], "secondary": []}

        # Find primary keywords section
        primary_match = re.search(
            r'\*\*Primary.*?\*\*[:\s]*(.*?)(?:\*\*Secondary|\n\n)',
            content, re.DOTALL | re.IGNORECASE
        )
        if primary_match:
            keywords["primary"] = [
                kw.strip().lower()
                for kw in re.findall(r'[-•]\s*([^\n]+)', primary_match.group(1))
            ]

        # Find secondary keywords section
        secondary_match = re.search(
            r'\*\*Secondary.*?\*\*[:\s]*(.*?)(?:\n\n|##)',
            content, re.DOTALL | re.IGNORECASE
        )
        if secondary_match:
            keywords["secondary"] = [
                kw.strip().lower()
                for kw in re.findall(r'[-•]\s*([^\n]+)', secondary_match.group(1))
            ]

        blueprints[blueprint_name] = {
            "file": str(bp_file),
            "keywords": keywords,
            "line_count": len(content.splitlines())
        }

    return blueprints


# =============================================================================
# Skill Detection Engine
# =============================================================================

class SkillDetector:
    """Detects skills from user goals using domain registries."""

    def __init__(self, registries: Dict[str, Dict]):
        self.registries = registries
        self._build_keyword_index()

    def _build_keyword_index(self):
        """Build index of keywords to skills."""
        self.keyword_to_skills = {}
        self.skill_to_domain = {}

        for domain, registry in self.registries.items():
            skills = registry.get("skills", {})
            # Handle both dict format (skill_name: config) and list format
            if isinstance(skills, dict):
                for skill_name, skill_config in skills.items():
                    if not isinstance(skill_config, dict):
                        continue
                    self.skill_to_domain[skill_name] = domain

                    keywords = skill_config.get("keywords", {})
                    for kw in keywords.get("primary", []):
                        self.keyword_to_skills.setdefault(kw.lower(), []).append(
                            (skill_name, "primary", 10)
                        )
                    for kw in keywords.get("secondary", []):
                        self.keyword_to_skills.setdefault(kw.lower(), []).append(
                            (skill_name, "secondary", 5)
                        )
            elif isinstance(skills, list):
                for skill in skills:
                    if not isinstance(skill, dict):
                        continue
                    skill_name = skill.get("name", "")
                    self.skill_to_domain[skill_name] = domain

                    keywords = skill.get("keywords", {})
                    for kw in keywords.get("primary", []):
                        self.keyword_to_skills.setdefault(kw.lower(), []).append(
                            (skill_name, "primary", 10)
                        )
                    for kw in keywords.get("secondary", []):
                        self.keyword_to_skills.setdefault(kw.lower(), []).append(
                            (skill_name, "secondary", 5)
                        )

    def detect_skills(self, goal: str) -> Tuple[List[str], Dict]:
        """
        Detect skills from user goal.
        Returns: (list of skill names, detection details)
        """
        goal_lower = goal.lower()
        goal_words = set(re.findall(r'\b\w+\b', goal_lower))

        skill_scores = {}
        matched_keywords = {}

        for keyword, skills in self.keyword_to_skills.items():
            if keyword in goal_lower or keyword in goal_words:
                for skill_name, match_type, score in skills:
                    skill_scores[skill_name] = skill_scores.get(skill_name, 0) + score
                    matched_keywords.setdefault(skill_name, []).append(
                        {"keyword": keyword, "type": match_type, "score": score}
                    )

        # Sort by score
        sorted_skills = sorted(
            skill_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        detected = [skill for skill, score in sorted_skills if score >= 5]

        return detected, {
            "scores": skill_scores,
            "matched_keywords": matched_keywords,
            "goal_words": list(goal_words)
        }

    def detect_domain(self, goal: str) -> Tuple[str, Dict]:
        """Detect primary domain from goal using word-boundary matching."""
        domain_keywords = {
            "frontend": ["ui", "form", "dashboard", "chart", "component", "interface",
                        "page", "design", "table", "menu", "navigation", "layout"],
            "backend": ["api", "database", "server", "auth", "queue", "cache",
                       "sql", "postgres", "mongo", "redis", "endpoint", "rest"],
            "devops": ["ci", "cd", "pipeline", "test", "docker", "gitops",
                      "jenkins", "github actions", "gitlab", "prometheus", "grafana",
                      "observability", "monitoring", "tracing"],
            "infrastructure": ["kubernetes", "k8s", "terraform", "ansible",
                              "linux", "nginx", "network", "load balancer", "aws", "gcp", "azure",
                              "microservices", "autoscaling", "deployment", "cluster"],
            "security": ["security", "tls", "ssl", "firewall", "compliance",
                        "soc2", "vulnerability", "encryption"],
            "ai-ml": ["rag", "vector", "embeddings", "llm", "agent", "model",
                     "ai", "chat", "mlops", "prompt"],
            "data": ["etl", "pipeline", "streaming", "kafka", "sql optimization",
                    "data architecture"],
            "cloud": ["aws", "gcp", "azure", "lambda", "s3", "ec2",
                     "cloud functions"],
            "finops": ["cost", "budget", "tagging", "finops", "optimization"]
        }

        goal_lower = goal.lower()
        # Extract words for word-boundary matching
        goal_words = set(re.findall(r'\b\w+\b', goal_lower))
        domain_scores = {}

        for domain, keywords in domain_keywords.items():
            score = 0
            for kw in keywords:
                # For multi-word keywords, check substring
                if ' ' in kw:
                    if kw in goal_lower:
                        score += 1
                # For single-word keywords, check word boundary
                else:
                    if kw in goal_words:
                        score += 1
            if score > 0:
                domain_scores[domain] = score

        if not domain_scores:
            return "unknown", {"scores": {}}

        primary = max(domain_scores.items(), key=lambda x: x[1])
        return primary[0], {"scores": domain_scores}


# =============================================================================
# Blueprint Detector
# =============================================================================

class BlueprintDetector:
    """Detects matching blueprints from user goals."""

    def __init__(self, blueprints: Dict[str, Dict]):
        self.blueprints = blueprints

    def detect_blueprint(self, goal: str) -> Tuple[Optional[str], float, Dict]:
        """
        Detect if a blueprint matches the goal.
        Returns: (blueprint_name, confidence, details)

        Matching criteria (count-based, not percentage-based):
        - HIGH confidence: 2+ primary matches OR (1 primary + 2+ secondary)
        - MEDIUM confidence: 1 primary match + 1 secondary
        - LOW: 1 primary match only
        """
        goal_lower = goal.lower()
        best_match = None
        best_score = 0
        details = {}

        for bp_name, bp_info in self.blueprints.items():
            keywords = bp_info.get("keywords", {})
            primary = keywords.get("primary", [])
            secondary = keywords.get("secondary", [])

            primary_matches = [kw for kw in primary if kw in goal_lower]
            secondary_matches = [kw for kw in secondary if kw in goal_lower]

            # Score: primary = 10 points each, secondary = 5 points each
            score = len(primary_matches) * 10 + len(secondary_matches) * 5

            # Calculate confidence based on match counts (not percentage)
            # 2+ primary = 90%, 1 primary + 2 secondary = 80%, 1 primary + 1 secondary = 70%
            # 1 primary only = 50%, secondary only = 30%
            p_count = len(primary_matches)
            s_count = len(secondary_matches)

            if p_count >= 2:
                confidence = 90.0
            elif p_count >= 1 and s_count >= 2:
                confidence = 80.0
            elif p_count >= 1 and s_count >= 1:
                confidence = 70.0
            elif p_count >= 1:
                confidence = 50.0
            elif s_count >= 2:
                confidence = 40.0
            elif s_count >= 1:
                confidence = 20.0
            else:
                confidence = 0.0

            details[bp_name] = {
                "primary_matches": primary_matches,
                "secondary_matches": secondary_matches,
                "score": score,
                "confidence": confidence
            }

            if score > best_score:
                best_score = score
                best_match = bp_name

        # Return match if confidence >= 50% (at least 1 primary keyword match)
        if best_match and details[best_match]["confidence"] >= 50:
            return best_match, details[best_match]["confidence"], details

        return None, 0, details


# =============================================================================
# Scenario Evaluator
# =============================================================================

class ScenarioEvaluator:
    """Evaluates scenarios against expected outcomes."""

    def __init__(self):
        self.registries = load_registries()
        self.blueprints = load_blueprints()
        self.skill_detector = SkillDetector(self.registries)
        self.blueprint_detector = BlueprintDetector(self.blueprints)

    def evaluate_scenario(self, scenario: Dict) -> EvaluationResult:
        """Evaluate a single scenario."""
        result = EvaluationResult(
            scenario_id=scenario["id"],
            scenario_name=scenario["name"],
            domain=scenario["domain"],
            passed=True
        )

        goal = scenario["goal"]
        expected_skills = set(scenario.get("expected_skills", []))
        expected_blueprint = scenario.get("blueprint")

        # 1. Evaluate skill detection
        detected_skills, skill_details = self.skill_detector.detect_skills(goal)
        detected_set = set(detected_skills)

        skill_overlap = detected_set & expected_skills
        skill_precision = len(skill_overlap) / len(detected_set) if detected_set else 0
        skill_recall = len(skill_overlap) / len(expected_skills) if expected_skills else 0
        skill_f1 = (2 * skill_precision * skill_recall / (skill_precision + skill_recall)
                   if (skill_precision + skill_recall) > 0 else 0)

        result.skill_detection = {
            "expected": list(expected_skills),
            "detected": detected_skills,
            "precision": skill_precision,
            "recall": skill_recall,
            "f1": skill_f1,
            "details": skill_details
        }
        result.scores["skill_detection"] = skill_f1 * 5  # Scale to 0-5

        if skill_recall < 0.8:
            result.issues.append(
                f"Low skill recall ({skill_recall:.0%}): "
                f"Missing {expected_skills - detected_set}"
            )

        # 2. Evaluate domain detection
        detected_domain, domain_details = self.skill_detector.detect_domain(goal)
        domain_correct = detected_domain == scenario["domain"]
        result.scores["domain_detection"] = 5.0 if domain_correct else 0.0

        if not domain_correct:
            result.issues.append(
                f"Domain mismatch: expected {scenario['domain']}, got {detected_domain}"
            )

        # 3. Evaluate blueprint detection
        detected_bp, bp_confidence, bp_details = self.blueprint_detector.detect_blueprint(goal)

        result.blueprint_detection = {
            "expected": expected_blueprint,
            "detected": detected_bp,
            "confidence": bp_confidence,
            "details": bp_details
        }

        if expected_blueprint:
            if detected_bp == expected_blueprint:
                result.scores["blueprint_match"] = 5.0
            elif detected_bp is None:
                result.scores["blueprint_match"] = 0.0
                result.issues.append(
                    f"Blueprint not detected: expected {expected_blueprint}"
                )
                result.suggestions.append(
                    f"Add keywords from goal to {expected_blueprint}.md"
                )
            else:
                result.scores["blueprint_match"] = 2.0
                result.issues.append(
                    f"Wrong blueprint: expected {expected_blueprint}, got {detected_bp}"
                )
        else:
            result.scores["blueprint_match"] = 5.0  # N/A = pass

        # 4. Calculate question reduction score
        # If no blueprint expected, don't penalize for no question reduction
        expected_q = scenario.get("expected_questions", 0)
        normal_q = scenario.get("normal_questions", 0)
        if expected_blueprint is None:
            # No blueprint = no question reduction expected, give full score
            result.scores["question_reduction"] = 5.0
        elif normal_q > 0:
            reduction = (normal_q - expected_q) / normal_q
            result.scores["question_reduction"] = reduction * 5
        else:
            result.scores["question_reduction"] = 5.0

        # 5. Overall pass/fail
        avg_score = sum(result.scores.values()) / len(result.scores)
        result.passed = avg_score >= 3.5 and len(result.issues) <= 2

        return result


# =============================================================================
# Report Generation
# =============================================================================

def generate_report(results: List[EvaluationResult]) -> EvaluationReport:
    """Generate evaluation report from results."""
    report = EvaluationReport(
        timestamp=datetime.now().isoformat(),
        total_scenarios=len(results),
        passed=sum(1 for r in results if r.passed),
        failed=sum(1 for r in results if not r.passed),
        results=results
    )

    if results:
        total_scores = sum(
            sum(r.scores.values()) / len(r.scores)
            for r in results
        )
        report.overall_score = total_scores / len(results)

    return report


def print_report(report: EvaluationReport):
    """Print evaluation report to console."""
    print("\n" + "=" * 70)
    print("AI DESIGN COMPONENTS - SKILLCHAIN EVALUATION REPORT")
    print("=" * 70)
    print(f"\nTimestamp: {report.timestamp}")
    print(f"Overall Score: {report.overall_score:.2f}/5.00")
    print(f"Pass Rate: {report.passed}/{report.total_scenarios} "
          f"({report.passed/report.total_scenarios*100:.0f}%)")

    print("\n" + "-" * 70)
    print("SCENARIO RESULTS")
    print("-" * 70)

    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        avg_score = sum(result.scores.values()) / len(result.scores)
        print(f"\n[{result.scenario_id}] {result.scenario_name}")
        print(f"  Status: {status} | Domain: {result.domain} | Score: {avg_score:.2f}/5.00")
        print(f"  Skill Detection: {result.scores.get('skill_detection', 0):.2f}/5.00")
        print(f"  Blueprint Match: {result.scores.get('blueprint_match', 0):.2f}/5.00")
        print(f"  Question Reduction: {result.scores.get('question_reduction', 0):.2f}/5.00")

        if result.issues:
            print(f"  Issues:")
            for issue in result.issues:
                print(f"    - {issue}")

        if result.suggestions:
            print(f"  Suggestions:")
            for suggestion in result.suggestions:
                print(f"    - {suggestion}")

    print("\n" + "-" * 70)
    print("SUMMARY BY DOMAIN")
    print("-" * 70)

    domains = {}
    for result in report.results:
        if result.domain not in domains:
            domains[result.domain] = {"passed": 0, "total": 0, "scores": []}
        domains[result.domain]["total"] += 1
        if result.passed:
            domains[result.domain]["passed"] += 1
        avg = sum(result.scores.values()) / len(result.scores)
        domains[result.domain]["scores"].append(avg)

    for domain, stats in sorted(domains.items()):
        avg_score = sum(stats["scores"]) / len(stats["scores"])
        print(f"  {domain:15s}: {stats['passed']}/{stats['total']} passed, "
              f"avg score {avg_score:.2f}/5.00")

    print("\n" + "=" * 70)


def save_report(report: EvaluationReport, output_file: Path):
    """Save report to JSON file."""
    report_dict = {
        "timestamp": report.timestamp,
        "total_scenarios": report.total_scenarios,
        "passed": report.passed,
        "failed": report.failed,
        "overall_score": report.overall_score,
        "results": [
            {
                "scenario_id": r.scenario_id,
                "scenario_name": r.scenario_name,
                "domain": r.domain,
                "passed": r.passed,
                "scores": r.scores,
                "skill_detection": r.skill_detection,
                "blueprint_detection": r.blueprint_detection,
                "issues": r.issues,
                "suggestions": r.suggestions
            }
            for r in report.results
        ]
    }

    with open(output_file, "w") as f:
        json.dump(report_dict, f, indent=2)

    print(f"\nReport saved to: {output_file}")


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate skillchain scenarios"
    )
    parser.add_argument(
        "--scenario", "-s",
        help="Run specific scenario by ID (e.g., S01)"
    )
    parser.add_argument(
        "--domain", "-d",
        help="Run scenarios for specific domain"
    )
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="Generate and save report"
    )
    parser.add_argument(
        "--output", "-o",
        default="evaluation_report.json",
        help="Output file for report (default: evaluation_report.json)"
    )

    args = parser.parse_args()

    # Load scenarios
    with open(SCENARIOS_FILE) as f:
        config = yaml.safe_load(f)

    scenarios = config.get("scenarios", [])

    # Filter scenarios
    if args.scenario:
        scenarios = [s for s in scenarios if s["id"] == args.scenario]
        if not scenarios:
            print(f"ERROR: Scenario {args.scenario} not found")
            sys.exit(1)

    if args.domain:
        scenarios = [s for s in scenarios if s["domain"] == args.domain]
        if not scenarios:
            print(f"ERROR: No scenarios found for domain {args.domain}")
            sys.exit(1)

    print(f"Evaluating {len(scenarios)} scenarios...")

    # Run evaluation
    evaluator = ScenarioEvaluator()
    results = []

    for scenario in scenarios:
        print(f"  Evaluating [{scenario['id']}] {scenario['name']}...")
        result = evaluator.evaluate_scenario(scenario)
        results.append(result)

    # Generate report
    report = generate_report(results)
    print_report(report)

    # Save report if requested
    if args.report:
        output_path = SCRIPT_DIR / args.output
        save_report(report, output_path)

    # Exit with error if any failures
    sys.exit(0 if report.failed == 0 else 1)


if __name__ == "__main__":
    main()
