"""Registry management for skillchain skills.

Loads and queries skill registries from .claude-commands/skillchain-data/registries/.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml


@dataclass
class SkillInfo:
    """Information about a skill from the registry."""
    name: str
    domain: str
    invocation: str  # e.g., "ui-foundation-skills:theming-components"
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    priority: int = 5
    required: bool = False
    defaults: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RouteResult:
    """Result of routing a goal to skills."""
    goal: str
    domains: List[str]
    primary_domain: str
    matched_skills: List[SkillInfo]
    blueprint: Optional[str] = None
    confidence: float = 0.0


class RegistryManager:
    """Manages skill registries and routing.

    Loads registry YAML files and provides skill lookup and routing.

    Example:
        >>> registry = RegistryManager("/path/to/ai-design-components")
        >>> route = registry.route_goal("dashboard with charts")
        >>> print(route.matched_skills)
    """

    # Blueprint keywords for detection
    BLUEPRINT_KEYWORDS = {
        "dashboard": ["dashboard", "analytics", "metrics", "kpi"],
        "crud-api": ["crud", "rest api", "api endpoint", "backend"],
        "rag-pipeline": ["rag", "retrieval", "embeddings", "vector"],
        "ci-cd": ["ci/cd", "pipeline", "github actions", "deployment"],
        "k8s": ["kubernetes", "k8s", "container", "helm"],
        "security": ["security", "authentication", "authorization"],
        "observability": ["monitoring", "logging", "tracing", "observability"],
        "data-pipeline": ["etl", "data pipeline", "ingestion"],
        "ml-pipeline": ["mlops", "model training", "ml pipeline"],
        "cloud": ["aws", "gcp", "azure", "cloud"],
        "cost": ["cost optimization", "finops", "billing"],
        "api-first": ["api design", "openapi", "swagger"],
    }

    # Domain keywords for detection
    DOMAIN_KEYWORDS = {
        "frontend": ["ui", "component", "react", "vue", "chart", "form", "dashboard", "layout"],
        "backend": ["api", "database", "rest", "graphql", "auth", "server"],
        "devops": ["ci/cd", "pipeline", "docker", "testing", "deployment"],
        "infrastructure": ["kubernetes", "terraform", "nginx", "networking"],
        "security": ["security", "compliance", "encryption", "firewall"],
        "data": ["etl", "data pipeline", "warehouse", "streaming"],
        "ai-ml": ["ml", "ai", "model", "embeddings", "rag", "llm"],
        "cloud": ["aws", "gcp", "azure"],
        "finops": ["cost", "billing", "optimization"],
    }

    def __init__(self, repo_root: str):
        """Initialize registry manager.

        Args:
            repo_root: Path to ai-design-components repository root
        """
        self.repo_root = Path(repo_root)
        self.registries_dir = self.repo_root / ".claude-commands" / "skillchain-data" / "registries"
        self._registries: Dict[str, Dict] = {}
        self._skills: Dict[str, SkillInfo] = {}
        self._loaded = False

    def load_registries(self) -> None:
        """Load all registry YAML files."""
        if self._loaded:
            return

        if not self.registries_dir.exists():
            raise FileNotFoundError(f"Registries directory not found: {self.registries_dir}")

        # Load each domain registry
        for yaml_file in self.registries_dir.glob("*.yaml"):
            if yaml_file.name.startswith("_"):
                continue  # Skip index files

            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)

                domain = data.get("domain", yaml_file.stem)
                self._registries[domain] = data

                # Index skills
                for skill_name, skill_data in data.get("skills", {}).items():
                    self._skills[skill_name] = SkillInfo(
                        name=skill_name,
                        domain=domain,
                        invocation=skill_data.get("invocation", f"{domain}:{skill_name}"),
                        description=skill_data.get("description", ""),
                        keywords=skill_data.get("keywords", {}).get("primary", []),
                        dependencies=skill_data.get("dependencies", []),
                        priority=skill_data.get("priority", 5),
                        required=skill_data.get("required", False),
                        defaults=skill_data.get("questions", {}).get("defaults", {}),
                    )
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")

        self._loaded = True

    def get_skill(self, name: str) -> Optional[SkillInfo]:
        """Get a skill by name."""
        self.load_registries()
        return self._skills.get(name)

    def get_skills_by_domain(self, domain: str) -> List[SkillInfo]:
        """Get all skills in a domain."""
        self.load_registries()
        return [s for s in self._skills.values() if s.domain == domain]

    def list_all_skills(self) -> List[SkillInfo]:
        """List all registered skills."""
        self.load_registries()
        return list(self._skills.values())

    def route_goal(self, goal: str, blueprint_hint: Optional[str] = None) -> RouteResult:
        """Route a goal to matched skills.

        Args:
            goal: User's goal description
            blueprint_hint: Optional blueprint name to use

        Returns:
            RouteResult with matched domains and skills
        """
        self.load_registries()

        goal_lower = goal.lower()

        # Detect blueprint
        detected_blueprint = blueprint_hint
        blueprint_confidence = 0.0

        if not detected_blueprint:
            for bp_name, keywords in self.BLUEPRINT_KEYWORDS.items():
                matches = sum(1 for kw in keywords if kw in goal_lower)
                if matches > 0:
                    confidence = matches / len(keywords)
                    if confidence > blueprint_confidence:
                        detected_blueprint = bp_name
                        blueprint_confidence = confidence

        # Detect domains
        domain_scores: Dict[str, float] = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in goal_lower)
            if matches > 0:
                domain_scores[domain] = matches / len(keywords)

        # Sort domains by score
        sorted_domains = sorted(
            domain_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        detected_domains = [d[0] for d in sorted_domains[:3]]  # Top 3 domains
        primary_domain = detected_domains[0] if detected_domains else "frontend"

        # Match skills based on goal keywords
        matched_skills: List[SkillInfo] = []

        for skill in self._skills.values():
            # Check if skill domain is relevant
            if skill.domain not in detected_domains:
                continue

            # Check keyword matches
            keyword_matches = sum(
                1 for kw in skill.keywords
                if kw.lower() in goal_lower
            )

            # Include required skills for detected domains
            if skill.required and skill.domain in detected_domains:
                matched_skills.append(skill)
            elif keyword_matches > 0:
                matched_skills.append(skill)

        # Sort by priority and dependencies
        matched_skills = self._sort_by_dependencies(matched_skills)

        return RouteResult(
            goal=goal,
            domains=detected_domains,
            primary_domain=primary_domain,
            matched_skills=matched_skills,
            blueprint=detected_blueprint if blueprint_confidence > 0.3 else None,
            confidence=blueprint_confidence,
        )

    def _sort_by_dependencies(self, skills: List[SkillInfo]) -> List[SkillInfo]:
        """Sort skills by dependencies (topological sort)."""
        # Build dependency graph
        skill_map = {s.name: s for s in skills}
        in_degree = {s.name: 0 for s in skills}

        for skill in skills:
            for dep in skill.dependencies:
                if dep in skill_map:
                    in_degree[skill.name] += 1

        # Kahn's algorithm
        sorted_skills = []
        queue = [s for s in skills if in_degree[s.name] == 0]
        queue.sort(key=lambda s: s.priority)  # Sort by priority within same level

        while queue:
            skill = queue.pop(0)
            sorted_skills.append(skill)

            # Reduce in-degree for dependents
            for other in skills:
                if skill.name in other.dependencies:
                    in_degree[other.name] -= 1
                    if in_degree[other.name] == 0:
                        queue.append(other)
                        queue.sort(key=lambda s: s.priority)

        # Add any remaining (cycles or missing deps)
        remaining = [s for s in skills if s not in sorted_skills]
        remaining.sort(key=lambda s: s.priority)
        sorted_skills.extend(remaining)

        return sorted_skills

    def get_blueprint_skills(self, blueprint: str) -> List[SkillInfo]:
        """Get skills for a specific blueprint.

        This would ideally load from blueprint YAML files,
        but for now returns common skill sets.
        """
        self.load_registries()

        # Common blueprint skill mappings
        blueprint_skills = {
            "dashboard": [
                "theming-components", "designing-layouts", "creating-dashboards",
                "visualizing-data", "building-tables", "providing-feedback",
                "assembling-components"
            ],
            "crud-api": [
                "implementing-api-patterns", "using-relational-databases",
                "securing-authentication", "observability", "deploying-applications"
            ],
            "rag-pipeline": [
                "using-vector-databases", "ai-data-engineering", "model-serving",
                "implementing-api-patterns", "observability"
            ],
        }

        skill_names = blueprint_skills.get(blueprint, [])
        return [self._skills[name] for name in skill_names if name in self._skills]
