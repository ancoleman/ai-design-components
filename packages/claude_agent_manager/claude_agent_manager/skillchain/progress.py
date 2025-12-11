"""Progress tracking for skillchain execution.

Manages .skillchain-progress.json for resumable sessions.
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .registry import SkillInfo


@dataclass
class SkillProgress:
    """Progress tracking for a single skill."""
    name: str
    invocation: str
    status: str = "pending"  # pending, running, complete, failed, skipped
    executor: Optional[str] = None
    agent_id: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    files_created: List[str] = field(default_factory=list)
    decisions: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class ExecutionState:
    """Execution state tracking."""
    mode: str = "standard"  # standard, delegated
    total_skills: int = 0
    completed_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    current_index: int = 0
    activation_rate: float = 0.0


@dataclass
class ProgressFile:
    """Complete progress file structure.

    Stored as .skillchain-progress.json in project root.
    """
    version: str = "1.0"
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    goal: str = ""
    blueprint: Optional[str] = None
    maturity: str = "intermediate"
    project_path: str = ""
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    skills: List[SkillProgress] = field(default_factory=list)
    execution: ExecutionState = field(default_factory=ExecutionState)
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "session_id": self.session_id,
            "goal": self.goal,
            "blueprint": self.blueprint,
            "maturity": self.maturity,
            "project_path": self.project_path,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "skills": [asdict(s) for s in self.skills],
            "execution": asdict(self.execution),
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgressFile":
        """Create from dictionary."""
        skills = [
            SkillProgress(**s) for s in data.get("skills", [])
        ]
        execution = ExecutionState(**data.get("execution", {}))

        return cls(
            version=data.get("version", "1.0"),
            session_id=data.get("session_id", str(uuid.uuid4())),
            goal=data.get("goal", ""),
            blueprint=data.get("blueprint"),
            maturity=data.get("maturity", "intermediate"),
            project_path=data.get("project_path", ""),
            started_at=data.get("started_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
            skills=skills,
            execution=execution,
            context=data.get("context", {}),
        )

    def get_current_skill(self) -> Optional[SkillProgress]:
        """Get the current skill being executed."""
        if self.execution.current_index < len(self.skills):
            return self.skills[self.execution.current_index]
        return None

    def get_pending_skills(self) -> List[SkillProgress]:
        """Get all pending skills."""
        return [s for s in self.skills if s.status == "pending"]

    def get_completed_skills(self) -> List[SkillProgress]:
        """Get all completed skills."""
        return [s for s in self.skills if s.status == "complete"]

    def get_previous_outputs(self) -> Dict[str, Any]:
        """Get outputs from all completed skills for context passing."""
        outputs = {}
        for skill in self.get_completed_skills():
            outputs[skill.name] = {
                "files": skill.files_created,
                "decisions": skill.decisions,
            }
        return outputs


class ProgressManager:
    """Manages skillchain progress files.

    Provides CRUD operations for .skillchain-progress.json files.

    Example:
        >>> pm = ProgressManager()
        >>> progress = pm.create("/path/to/project", "Build dashboard", ["skill1", "skill2"])
        >>> pm.update_skill(progress, 0, status="complete", files=["file.tsx"])
        >>> pm.save(progress)
    """

    PROGRESS_FILENAME = ".skillchain-progress.json"

    def create(
        self,
        project_path: str,
        goal: str,
        skills: List[SkillInfo],
        blueprint: Optional[str] = None,
        maturity: str = "intermediate",
    ) -> ProgressFile:
        """Create a new progress file.

        Args:
            project_path: Path to project directory
            goal: User's goal description
            skills: List of skills to execute
            blueprint: Optional blueprint name
            maturity: Skill detail level

        Returns:
            New ProgressFile instance
        """
        skill_progress = [
            SkillProgress(
                name=skill.name,
                invocation=skill.invocation,
                executor=self._select_executor(skill),
            )
            for skill in skills
        ]

        execution_mode = "delegated" if len(skills) >= 4 else "standard"

        progress = ProgressFile(
            goal=goal,
            blueprint=blueprint,
            maturity=maturity,
            project_path=project_path,
            skills=skill_progress,
            execution=ExecutionState(
                mode=execution_mode,
                total_skills=len(skills),
            ),
        )

        return progress

    def _select_executor(self, skill: SkillInfo) -> str:
        """Select executor type based on skill domain."""
        domain_executors = {
            "frontend": "frontend-skill-executor",
            "backend": "backend-skill-executor",
            "devops": "devops-skill-executor",
            "infrastructure": "infra-skill-executor",
            "security": "security-skill-executor",
            "data": "data-skill-executor",
            "ai-ml": "ai-ml-skill-executor",
            "cloud": "cloud-skill-executor",
            "finops": "finops-skill-executor",
        }
        return domain_executors.get(skill.domain, "general-skill-executor")

    def save(self, progress: ProgressFile) -> Path:
        """Save progress file to disk.

        Args:
            progress: ProgressFile to save

        Returns:
            Path to saved file
        """
        progress.updated_at = datetime.now().isoformat()

        file_path = Path(progress.project_path) / self.PROGRESS_FILENAME

        with open(file_path, "w") as f:
            json.dump(progress.to_dict(), f, indent=2)

        return file_path

    def load(self, project_path: str) -> Optional[ProgressFile]:
        """Load progress file from disk.

        Args:
            project_path: Path to project directory

        Returns:
            ProgressFile if exists, None otherwise
        """
        file_path = Path(project_path) / self.PROGRESS_FILENAME

        if not file_path.exists():
            return None

        with open(file_path) as f:
            data = json.load(f)

        return ProgressFile.from_dict(data)

    def exists(self, project_path: str) -> bool:
        """Check if progress file exists."""
        file_path = Path(project_path) / self.PROGRESS_FILENAME
        return file_path.exists()

    def delete(self, project_path: str) -> bool:
        """Delete progress file.

        Args:
            project_path: Path to project directory

        Returns:
            True if deleted, False if not found
        """
        file_path = Path(project_path) / self.PROGRESS_FILENAME

        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def update_skill(
        self,
        progress: ProgressFile,
        skill_index: int,
        status: Optional[str] = None,
        files: Optional[List[str]] = None,
        decisions: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> None:
        """Update a skill's progress.

        Args:
            progress: ProgressFile to update
            skill_index: Index of skill to update
            status: New status (pending, running, complete, failed, skipped)
            files: Files created by skill
            decisions: Decisions made during skill execution
            error: Error message if failed
            agent_id: ID of agent executing skill
        """
        if skill_index >= len(progress.skills):
            raise IndexError(f"Skill index {skill_index} out of range")

        skill = progress.skills[skill_index]

        if status:
            old_status = skill.status
            skill.status = status

            # Update execution counts
            if status == "running" and old_status == "pending":
                skill.started_at = datetime.now().isoformat()
            elif status == "complete":
                skill.completed_at = datetime.now().isoformat()
                progress.execution.completed_count += 1
            elif status == "failed":
                skill.completed_at = datetime.now().isoformat()
                progress.execution.failed_count += 1
            elif status == "skipped":
                progress.execution.skipped_count += 1

            # Update current index
            if status in ("complete", "failed", "skipped"):
                progress.execution.current_index = skill_index + 1

            # Update activation rate
            total_processed = (
                progress.execution.completed_count +
                progress.execution.failed_count +
                progress.execution.skipped_count
            )
            if total_processed > 0:
                progress.execution.activation_rate = (
                    progress.execution.completed_count / total_processed
                )

        if files:
            skill.files_created.extend(files)

        if decisions:
            skill.decisions.update(decisions)

        if error:
            skill.error = error

        if agent_id:
            skill.agent_id = agent_id

        progress.updated_at = datetime.now().isoformat()

    def mark_skill_running(
        self,
        progress: ProgressFile,
        skill_index: int,
        agent_id: str
    ) -> None:
        """Mark a skill as running."""
        self.update_skill(progress, skill_index, status="running", agent_id=agent_id)

    def mark_skill_complete(
        self,
        progress: ProgressFile,
        skill_index: int,
        files: List[str],
        decisions: Dict[str, Any],
    ) -> None:
        """Mark a skill as complete."""
        self.update_skill(
            progress, skill_index,
            status="complete",
            files=files,
            decisions=decisions,
        )

    def mark_skill_failed(
        self,
        progress: ProgressFile,
        skill_index: int,
        error: str,
    ) -> None:
        """Mark a skill as failed."""
        self.update_skill(progress, skill_index, status="failed", error=error)

    def get_resumable_skills(self, progress: ProgressFile) -> List[SkillProgress]:
        """Get skills that can be resumed (pending or failed)."""
        return [
            s for s in progress.skills
            if s.status in ("pending", "failed")
        ]
