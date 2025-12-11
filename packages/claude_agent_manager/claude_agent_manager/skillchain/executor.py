"""Skillchain executor for delegated multi-agent execution.

Provides high-level orchestration of skillchain workflows using
claude_agent_manager for agent spawning and coordination.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ..core.events import Event, EventEmitter, EventType
from ..core.process import ProcessConfig, ProcessManager, ProcessResult
from ..orchestration.coordinator import AgentConfig, AgentCoordinator, AgentResult, AgentRole
from .progress import ProgressFile, ProgressManager, SkillProgress
from .registry import RegistryManager, RouteResult, SkillInfo


@dataclass
class SkillExecutionResult:
    """Result of executing a single skill."""
    skill_name: str
    invocation: str
    success: bool
    files_created: List[str] = field(default_factory=list)
    decisions: Dict[str, Any] = field(default_factory=dict)
    output_text: str = ""
    cost_usd: float = 0.0
    duration_seconds: float = 0.0
    error: Optional[str] = None


@dataclass
class SkillchainResult:
    """Result of executing a complete skillchain."""
    goal: str
    blueprint: Optional[str]
    maturity: str
    skills_planned: int
    skills_completed: int
    skills_failed: int
    skills_skipped: int
    activation_rate: float
    total_files_created: List[str] = field(default_factory=list)
    total_cost_usd: float = 0.0
    total_duration_seconds: float = 0.0
    skill_results: List[SkillExecutionResult] = field(default_factory=list)
    error: Optional[str] = None


class SkillchainExecutor:
    """Execute skillchains using delegated multi-agent orchestration.

    Coordinates multiple Claude agents to execute skills in sequence,
    with progress tracking and context passing between skills.

    Example:
        >>> executor = SkillchainExecutor("/path/to/ai-design-components")
        >>>
        >>> # Execute a skillchain
        >>> result = await executor.execute(
        ...     goal="Build a dashboard with charts",
        ...     project_path="/path/to/project",
        ...     maturity="intermediate"
        ... )
        >>>
        >>> print(f"Completed {result.skills_completed}/{result.skills_planned} skills")
        >>> print(f"Files created: {result.total_files_created}")
    """

    def __init__(
        self,
        repo_root: str,
        process_manager: Optional[ProcessManager] = None,
        emitter: Optional[EventEmitter] = None,
        max_concurrent: int = 1,  # Sequential by default for skills
    ):
        """Initialize the skillchain executor.

        Args:
            repo_root: Path to ai-design-components repository
            process_manager: Optional ProcessManager instance
            emitter: Optional EventEmitter for events
            max_concurrent: Max concurrent skill executions (default: 1)
        """
        self.repo_root = Path(repo_root)
        self.emitter = emitter or EventEmitter()
        self.process_manager = process_manager or ProcessManager(emitter=self.emitter)
        self.registry = RegistryManager(str(repo_root))
        self.progress_mgr = ProgressManager()
        self.max_concurrent = max_concurrent

        # Coordinator for delegated execution
        self.coordinator = AgentCoordinator(
            emitter=self.emitter,
            max_concurrent=max_concurrent
        )

    async def execute(
        self,
        goal: str,
        project_path: str,
        blueprint: Optional[str] = None,
        maturity: str = "intermediate",
        skills: Optional[List[str]] = None,
        on_skill_start: Optional[Callable[[SkillInfo, int, int], None]] = None,
        on_skill_complete: Optional[Callable[[SkillExecutionResult, int, int], None]] = None,
    ) -> SkillchainResult:
        """Execute a skillchain.

        Args:
            goal: User's goal description
            project_path: Path to project directory
            blueprint: Optional blueprint name to use
            maturity: Detail level (starter, intermediate, advanced)
            skills: Optional explicit list of skill names to execute
            on_skill_start: Callback when skill starts (skill, index, total)
            on_skill_complete: Callback when skill completes (result, index, total)

        Returns:
            SkillchainResult with execution summary
        """
        start_time = datetime.now()

        # Route goal to skills
        if skills:
            # Use explicit skill list
            matched_skills = [
                self.registry.get_skill(name) for name in skills
                if self.registry.get_skill(name)
            ]
            route = RouteResult(
                goal=goal,
                domains=[],
                primary_domain="custom",
                matched_skills=matched_skills,
                blueprint=blueprint,
            )
        else:
            # Auto-detect skills from goal
            route = self.registry.route_goal(goal, blueprint)

        if not route.matched_skills:
            return SkillchainResult(
                goal=goal,
                blueprint=route.blueprint,
                maturity=maturity,
                skills_planned=0,
                skills_completed=0,
                skills_failed=0,
                skills_skipped=0,
                activation_rate=0.0,
                error="No skills matched the goal",
            )

        # Create progress file
        progress = self.progress_mgr.create(
            project_path=project_path,
            goal=goal,
            skills=route.matched_skills,
            blueprint=route.blueprint,
            maturity=maturity,
        )
        self.progress_mgr.save(progress)

        # Emit skillchain started event
        await self.emitter.emit(Event(
            type=EventType.SESSION_STARTED,
            session_id=progress.session_id,
            data={
                "goal": goal,
                "blueprint": route.blueprint,
                "skills": [s.name for s in route.matched_skills],
                "mode": progress.execution.mode,
            }
        ))

        # Execute skills
        skill_results: List[SkillExecutionResult] = []
        total_skills = len(route.matched_skills)

        for i, skill in enumerate(route.matched_skills):
            # Callback
            if on_skill_start:
                on_skill_start(skill, i, total_skills)

            # Mark as running
            self.progress_mgr.mark_skill_running(
                progress, i, agent_id=f"executor-{i}"
            )
            self.progress_mgr.save(progress)

            # Execute skill
            try:
                result = await self._execute_skill(
                    skill=skill,
                    progress=progress,
                    project_path=project_path,
                    maturity=maturity,
                )

                skill_results.append(result)

                # Update progress
                if result.success:
                    self.progress_mgr.mark_skill_complete(
                        progress, i,
                        files=result.files_created,
                        decisions=result.decisions,
                    )
                else:
                    self.progress_mgr.mark_skill_failed(
                        progress, i,
                        error=result.error or "Unknown error",
                    )

                self.progress_mgr.save(progress)

                # Callback
                if on_skill_complete:
                    on_skill_complete(result, i, total_skills)

            except Exception as e:
                error_result = SkillExecutionResult(
                    skill_name=skill.name,
                    invocation=skill.invocation,
                    success=False,
                    error=str(e),
                )
                skill_results.append(error_result)

                self.progress_mgr.mark_skill_failed(progress, i, error=str(e))
                self.progress_mgr.save(progress)

                if on_skill_complete:
                    on_skill_complete(error_result, i, total_skills)

        # Calculate totals
        duration = (datetime.now() - start_time).total_seconds()

        completed = sum(1 for r in skill_results if r.success)
        failed = sum(1 for r in skill_results if not r.success)

        all_files = []
        total_cost = 0.0
        for r in skill_results:
            all_files.extend(r.files_created)
            total_cost += r.cost_usd

        activation_rate = completed / total_skills if total_skills > 0 else 0.0

        # Emit completion
        await self.emitter.emit(Event(
            type=EventType.SESSION_COMPLETE,
            session_id=progress.session_id,
            data={
                "skills_completed": completed,
                "skills_failed": failed,
                "activation_rate": activation_rate,
                "total_cost_usd": total_cost,
            }
        ))

        return SkillchainResult(
            goal=goal,
            blueprint=route.blueprint,
            maturity=maturity,
            skills_planned=total_skills,
            skills_completed=completed,
            skills_failed=failed,
            skills_skipped=0,
            activation_rate=activation_rate,
            total_files_created=all_files,
            total_cost_usd=total_cost,
            total_duration_seconds=duration,
            skill_results=skill_results,
        )

    async def _execute_skill(
        self,
        skill: SkillInfo,
        progress: ProgressFile,
        project_path: str,
        maturity: str,
    ) -> SkillExecutionResult:
        """Execute a single skill using Claude.

        Args:
            skill: Skill to execute
            progress: Current progress state
            project_path: Path to project
            maturity: Detail level

        Returns:
            SkillExecutionResult
        """
        start_time = datetime.now()

        # Build execution prompt
        prompt = self._build_skill_prompt(skill, progress, maturity)

        # Emit progress
        await self.emitter.emit(Event(
            type=EventType.PROGRESS_UPDATE,
            session_id=progress.session_id,
            data={
                "skill": skill.name,
                "invocation": skill.invocation,
                "status": "executing",
            }
        ))

        # Execute via ProcessManager
        config = ProcessConfig(
            prompt=prompt,
            cwd=project_path,
            session_id=f"{progress.session_id}-{skill.name}",
            skip_permissions=True,
            timeout=300.0,  # 5 min per skill
        )

        result = await self.process_manager.execute(config)

        duration = (datetime.now() - start_time).total_seconds()

        # Parse result for files and decisions
        files_created = self._extract_files_from_response(result.text)
        decisions = self._extract_decisions_from_response(result.text)

        return SkillExecutionResult(
            skill_name=skill.name,
            invocation=skill.invocation,
            success=result.exit_code == 0,
            files_created=files_created,
            decisions=decisions,
            output_text=result.text,
            cost_usd=result.usage.total_cost_usd,
            duration_seconds=duration,
            error=result.error,
        )

    def _build_skill_prompt(
        self,
        skill: SkillInfo,
        progress: ProgressFile,
        maturity: str,
    ) -> str:
        """Build prompt for skill execution."""

        previous_outputs = progress.get_previous_outputs()

        prompt = f"""Execute this skill completely following the execution protocol.

## SKILL TO EXECUTE
Name: {skill.name}
Invocation: Skill: {skill.invocation}

## CONTEXT
Goal: {progress.goal}
Blueprint: {progress.blueprint or "None"}
Maturity: {maturity}
Project: {progress.project_path}

## PREVIOUS SKILL OUTPUTS
{self._format_previous_outputs(previous_outputs)}

## EXECUTION PROTOCOL

### Step 1: Announce
Say: "Now invoking skill: {skill.name}"
Purpose: {skill.description or "Execute skill requirements"}

### Step 2: Invoke
Use the Skill tool with: {skill.invocation}

### Step 3: Complete
Follow ALL instructions from the skill's SKILL.md file.
Generate all required code and configurations.

### Step 4: Report
When complete, report:
- FILES_CREATED: [list each file path]
- KEY_DECISIONS: [list key configuration choices]
- STATUS: complete

Now execute the skill."""

        return prompt

    def _format_previous_outputs(self, outputs: Dict[str, Any]) -> str:
        """Format previous skill outputs for context."""
        if not outputs:
            return "None (this is the first skill)"

        lines = []
        for skill_name, data in outputs.items():
            lines.append(f"### {skill_name}")
            if data.get("files"):
                lines.append(f"Files: {', '.join(data['files'])}")
            if data.get("decisions"):
                for key, value in data["decisions"].items():
                    lines.append(f"- {key}: {value}")

        return "\n".join(lines)

    def _extract_files_from_response(self, response: str) -> List[str]:
        """Extract created file paths from response."""
        files = []

        # Look for FILES_CREATED section
        if "FILES_CREATED:" in response:
            section = response.split("FILES_CREATED:")[1]
            # Take until next section or end
            if "KEY_DECISIONS:" in section:
                section = section.split("KEY_DECISIONS:")[0]

            # Parse file paths (one per line, may have - prefix)
            for line in section.strip().split("\n"):
                line = line.strip().lstrip("-").strip()
                if line and ("/" in line or "." in line):
                    files.append(line)

        # Also look for common patterns
        import re
        file_patterns = [
            r"Created:?\s+[`'\"]?([a-zA-Z0-9_/.-]+\.[a-z]+)[`'\"]?",
            r"Writing:?\s+[`'\"]?([a-zA-Z0-9_/.-]+\.[a-z]+)[`'\"]?",
            r"File:?\s+[`'\"]?([a-zA-Z0-9_/.-]+\.[a-z]+)[`'\"]?",
        ]

        for pattern in file_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            files.extend(matches)

        return list(set(files))  # Deduplicate

    def _extract_decisions_from_response(self, response: str) -> Dict[str, Any]:
        """Extract key decisions from response."""
        decisions = {}

        # Look for KEY_DECISIONS section
        if "KEY_DECISIONS:" in response:
            section = response.split("KEY_DECISIONS:")[1]
            # Take until STATUS or end
            if "STATUS:" in section:
                section = section.split("STATUS:")[0]

            # Parse decisions (key: value format)
            for line in section.strip().split("\n"):
                line = line.strip().lstrip("-").strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    decisions[key.strip()] = value.strip()

        return decisions

    async def resume(
        self,
        project_path: str,
        on_skill_start: Optional[Callable] = None,
        on_skill_complete: Optional[Callable] = None,
    ) -> SkillchainResult:
        """Resume an interrupted skillchain.

        Args:
            project_path: Path to project with .skillchain-progress.json
            on_skill_start: Callback when skill starts
            on_skill_complete: Callback when skill completes

        Returns:
            SkillchainResult with execution summary
        """
        progress = self.progress_mgr.load(project_path)

        if not progress:
            raise FileNotFoundError(
                f"No progress file found at {project_path}"
            )

        # Get remaining skills
        remaining = self.progress_mgr.get_resumable_skills(progress)

        if not remaining:
            return SkillchainResult(
                goal=progress.goal,
                blueprint=progress.blueprint,
                maturity=progress.maturity,
                skills_planned=progress.execution.total_skills,
                skills_completed=progress.execution.completed_count,
                skills_failed=progress.execution.failed_count,
                skills_skipped=progress.execution.skipped_count,
                activation_rate=progress.execution.activation_rate,
                error="No skills remaining to execute",
            )

        # Get skill infos
        skill_names = [s.name for s in remaining]

        # Continue execution
        return await self.execute(
            goal=progress.goal,
            project_path=project_path,
            blueprint=progress.blueprint,
            maturity=progress.maturity,
            skills=skill_names,
            on_skill_start=on_skill_start,
            on_skill_complete=on_skill_complete,
        )

    def list_blueprints(self) -> List[str]:
        """List available blueprints."""
        return list(self.registry.BLUEPRINT_KEYWORDS.keys())

    def list_domains(self) -> List[str]:
        """List available domains."""
        return list(self.registry.DOMAIN_KEYWORDS.keys())

    def route(self, goal: str) -> RouteResult:
        """Route a goal to skills without executing.

        Useful for previewing what skills would be matched.
        """
        return self.registry.route_goal(goal)
