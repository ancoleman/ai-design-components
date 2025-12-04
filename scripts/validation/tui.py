"""
Interactive TUI (Terminal User Interface) for skill validation.

This module provides a rich, interactive terminal interface for
exploring and validating skills using the Textual framework.
"""

from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, field

from textual.app import App, ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.widgets import Header, Footer, Static, DataTable, Label, Button
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import work
from textual.worker import Worker, get_current_worker

from rich.text import Text

from .validator import Validator
from .rules import load_rules, load_community_practices, load_project_rules
from .result import ValidationResult


@dataclass
class SkillData:
    """Data for displaying a skill in the TUI."""
    name: str
    path: str
    status: str  # 'pass', 'fail', 'pending'
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    result: Optional[ValidationResult] = None


class DetailPanel(Static):
    """Panel showing details for the selected skill."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skill: Optional[SkillData] = None

    def update_skill(self, skill: SkillData) -> None:
        """Update the panel with skill details."""
        self.skill = skill

        lines = []
        lines.append(f"[bold]{skill.name}[/bold]")
        lines.append(f"Status: {self._format_status(skill.status)}")
        lines.append("")

        # Separate warnings by source (core rules vs project rules)
        core_warnings = []
        project_warnings = []

        if skill.result and skill.result.issues:
            from .result import Severity
            for issue in skill.result.issues:
                if issue.severity == Severity.WARNING:
                    if issue.rule_id and issue.rule_id.startswith("project."):
                        project_warnings.append(issue.message)
                    else:
                        core_warnings.append(issue.message)
        else:
            # Fallback if no detailed issues available
            core_warnings = skill.warnings

        if skill.errors:
            lines.append(f"[bold red]Errors ({len(skill.errors)}):[/bold red]")
            for err in skill.errors[:10]:  # Limit display
                lines.append(f"  [red]• {err}[/red]")
            if len(skill.errors) > 10:
                lines.append(f"  [dim]... and {len(skill.errors) - 10} more[/dim]")
            lines.append("")

        if core_warnings:
            lines.append(f"[bold yellow]Warnings ({len(core_warnings)}):[/bold yellow]")
            for warn in core_warnings[:10]:
                lines.append(f"  [yellow]• {warn}[/yellow]")
            if len(core_warnings) > 10:
                lines.append(f"  [dim]... and {len(core_warnings) - 10} more[/dim]")
            lines.append("")

        if project_warnings:
            lines.append(f"[bold magenta]Project Rules ({len(project_warnings)}):[/bold magenta]")
            for warn in project_warnings[:10]:
                lines.append(f"  [magenta]• {warn}[/magenta]")
            if len(project_warnings) > 10:
                lines.append(f"  [dim]... and {len(project_warnings) - 10} more[/dim]")
            lines.append("")

        if skill.suggestions:
            lines.append(f"[bold blue]Suggestions ({len(skill.suggestions)}):[/bold blue]")
            for sug in skill.suggestions[:5]:
                lines.append(f"  [blue]• {sug}[/blue]")
            if len(skill.suggestions) > 5:
                lines.append(f"  [dim]... and {len(skill.suggestions) - 5} more[/dim]")

        self.update("\n".join(lines))

    def _format_status(self, status: str) -> str:
        if status == 'pass':
            return "[green]PASS[/green]"
        elif status == 'fail':
            return "[bold red]FAIL[/bold red]"
        else:
            return "[yellow]PENDING[/yellow]"


class SummaryBar(Static):
    """Summary statistics bar."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.passed = 0
        self.failed = 0
        self.pending = 0

    def update_stats(self, passed: int, failed: int, pending: int) -> None:
        """Update summary statistics."""
        self.passed = passed
        self.failed = failed
        self.pending = pending

        total = passed + failed + pending
        self.update(
            f"[bold]Skills:[/bold] {total} total | "
            f"[green]{passed} passed[/green] | "
            f"[red]{failed} failed[/red] | "
            f"[yellow]{pending} pending[/yellow]"
        )


class FilterModal(ModalScreen):
    """Modal for filtering skills."""

    BINDINGS = [
        Binding("escape", "dismiss", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Filter Skills", id="filter-title"),
            Button("All Skills", id="filter-all", variant="primary"),
            Button("Passed Only", id="filter-pass", variant="success"),
            Button("Failed Only", id="filter-fail", variant="error"),
            Button("With Warnings", id="filter-warn", variant="warning"),
            Button("Cancel", id="filter-cancel"),
            id="filter-dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        filter_map = {
            "filter-all": "all",
            "filter-pass": "pass",
            "filter-fail": "fail",
            "filter-warn": "warn",
            "filter-cancel": None,
        }
        result = filter_map.get(event.button.id)
        self.dismiss(result)


class SkillValidationApp(App):
    """Interactive Skill Validation Dashboard."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 2fr 1fr;
        grid-rows: auto 1fr auto;
    }

    #summary-bar {
        column-span: 2;
        height: 3;
        background: $surface;
        border: solid $primary;
        padding: 0 1;
    }

    #main-table {
        height: 100%;
        border: solid $primary;
    }

    #detail-panel {
        height: 100%;
        border: solid $secondary;
        padding: 1;
        overflow-y: auto;
    }

    #status-bar {
        column-span: 2;
        height: 1;
        background: $surface;
        padding: 0 1;
    }

    #filter-dialog {
        width: 40;
        height: auto;
        padding: 1 2;
        background: $surface;
        border: thick $primary;
    }

    #filter-dialog Label {
        text-align: center;
        width: 100%;
        margin-bottom: 1;
    }

    #filter-dialog Button {
        width: 100%;
        margin: 1 0;
    }

    DataTable {
        height: 100%;
    }

    DataTable > .datatable--cursor {
        background: $secondary;
    }

    .hidden {
        display: none;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("f", "filter", "Filter"),
        Binding("r", "refresh", "Refresh"),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
    ]

    def __init__(
        self,
        skills_dir: Path,
        completed_only: bool = False,
        phase: Optional[int] = None,
        rules_only: bool = False,
        skip_project_rules: bool = False,
    ):
        super().__init__()
        self.skills_dir = skills_dir
        self.completed_only = completed_only
        self.phase = phase
        self.rules_only = rules_only
        self.skip_project_rules = skip_project_rules

        # State
        self.skills_data: List[SkillData] = []
        self.filtered_data: List[SkillData] = []
        self.current_filter = "all"
        self.selected_skill: Optional[SkillData] = None

        # Validator (created on mount)
        self.validator: Optional[Validator] = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield SummaryBar(id="summary-bar")
        yield DataTable(id="main-table")
        yield ScrollableContainer(
            DetailPanel(id="detail-panel"),
            id="detail-container"
        )
        yield Static("Loading...", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app."""
        self.title = "Skill Validation Dashboard"

        mode_str = "completed" if self.completed_only else "all"
        if self.phase:
            mode_str = f"phase {self.phase}"
        self.sub_title = f"Mode: {mode_str}"

        # Setup table
        table = self.query_one("#main-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("#", "Skill Name", "Status", "Err", "Warn", "Proj", "Sug")

        # Initialize validator
        try:
            rules = load_rules()
            community = None if self.rules_only else load_community_practices()
            project = None if self.skip_project_rules else load_project_rules()
            self.validator = Validator(
                rules=rules,
                community=community,
                project=project,
                include_community=not self.rules_only,
                include_project=not self.skip_project_rules
            )
        except Exception as e:
            self.update_status(f"Error loading config: {e}")
            return

        # Start validation
        self.run_validation()

    @work(exclusive=True, thread=True)
    def run_validation(self) -> None:
        """Run validation in background thread."""
        worker = get_current_worker()

        if not self.validator:
            return

        # Collect skills to validate
        skills_to_check = []

        if self.phase is not None:
            phase_skills = self.validator.rules.get_phase_skills(self.phase)
            for name in phase_skills:
                skill_path = self.skills_dir / name
                if skill_path.exists():
                    if not self.completed_only or (skill_path / "SKILL.md").exists():
                        skills_to_check.append(skill_path)
        else:
            for skill_dir in sorted(self.skills_dir.iterdir()):
                if skill_dir.is_dir():
                    has_skill_md = (skill_dir / 'SKILL.md').exists()
                    has_init_md = (skill_dir / 'init.md').exists()

                    if self.completed_only:
                        if has_skill_md:
                            skills_to_check.append(skill_dir)
                    elif has_skill_md or has_init_md:
                        skills_to_check.append(skill_dir)

        # Validate each skill
        results = []
        total = len(skills_to_check)

        for i, skill_path in enumerate(skills_to_check):
            if worker.is_cancelled:
                return

            skill_name = skill_path.name

            # Update status
            self.call_from_thread(
                self.update_status,
                f"Validating {skill_name}... ({i+1}/{total})"
            )

            has_skill_md = (skill_path / 'SKILL.md').exists()

            if has_skill_md:
                result = self.validator.validate_skill(skill_path)
                skill_data = SkillData(
                    name=skill_name,
                    path=str(skill_path),
                    status='pass' if result.passed else 'fail',
                    errors=result.errors,
                    warnings=result.warnings,
                    suggestions=result.suggestions,
                    result=result
                )
            else:
                skill_data = SkillData(
                    name=skill_name,
                    path=str(skill_path),
                    status='pending',
                    errors=[],
                    warnings=[],
                    suggestions=[]
                )

            results.append(skill_data)

        # Update UI with results
        self.call_from_thread(self.populate_results, results)

    def update_status(self, message: str) -> None:
        """Update status bar."""
        status = self.query_one("#status-bar", Static)
        status.update(message)

    def populate_results(self, results: List[SkillData]) -> None:
        """Populate table with validation results."""
        self.skills_data = results
        self.apply_filter()
        self.update_status(f"Validated {len(results)} skills")

    def apply_filter(self) -> None:
        """Apply current filter to data."""
        filtered = self.skills_data

        if self.current_filter == "pass":
            filtered = [s for s in filtered if s.status == 'pass']
        elif self.current_filter == "fail":
            filtered = [s for s in filtered if s.status == 'fail']
        elif self.current_filter == "warn":
            filtered = [s for s in filtered if s.warnings]

        self.filtered_data = filtered
        self.refresh_table()
        self.update_summary()

    def refresh_table(self) -> None:
        """Refresh the data table."""
        from .result import Severity

        table = self.query_one("#main-table", DataTable)
        table.clear()

        for i, skill in enumerate(self.filtered_data, 1):
            if skill.status == 'pass':
                status = Text("PASS", style="green")
            elif skill.status == 'fail':
                status = Text("FAIL", style="bold red")
            else:
                status = Text("PEND", style="yellow")

            # Calculate separate counts for warnings vs project rules
            core_warn_count = 0
            proj_warn_count = 0

            if skill.result and skill.result.issues:
                for issue in skill.result.issues:
                    if issue.severity == Severity.WARNING:
                        if issue.rule_id and issue.rule_id.startswith("project."):
                            proj_warn_count += 1
                        else:
                            core_warn_count += 1
            else:
                # Fallback if no detailed issues
                core_warn_count = len(skill.warnings)

            sug_count = len(skill.suggestions)

            errors = Text(str(len(skill.errors)), style="red" if skill.errors else "dim")
            warnings = Text(str(core_warn_count), style="yellow" if core_warn_count else "dim")
            proj = Text(str(proj_warn_count), style="magenta" if proj_warn_count else "dim")
            sug = Text(str(sug_count), style="blue" if sug_count else "dim")

            table.add_row(str(i), skill.name, status, errors, warnings, proj, sug, key=skill.name)

    def update_summary(self) -> None:
        """Update summary statistics."""
        passed = sum(1 for s in self.skills_data if s.status == 'pass')
        failed = sum(1 for s in self.skills_data if s.status == 'fail')
        pending = sum(1 for s in self.skills_data if s.status == 'pending')

        summary = self.query_one("#summary-bar", SummaryBar)
        summary.update_stats(passed, failed, pending)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection."""
        if event.row_key:
            skill_name = str(event.row_key.value)
            skill = next((s for s in self.filtered_data if s.name == skill_name), None)
            if skill:
                self.selected_skill = skill
                detail = self.query_one("#detail-panel", DetailPanel)
                detail.update_skill(skill)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle row highlight (cursor movement)."""
        if event.row_key:
            skill_name = str(event.row_key.value)
            skill = next((s for s in self.filtered_data if s.name == skill_name), None)
            if skill:
                self.selected_skill = skill
                detail = self.query_one("#detail-panel", DetailPanel)
                detail.update_skill(skill)

    def action_filter(self) -> None:
        """Show filter modal."""
        def handle_filter(filter_type: Optional[str]) -> None:
            if filter_type:
                self.current_filter = filter_type
                self.apply_filter()

        self.push_screen(FilterModal(), handle_filter)

    def action_refresh(self) -> None:
        """Re-run validation."""
        self.skills_data = []
        self.filtered_data = []
        table = self.query_one("#main-table", DataTable)
        table.clear()
        self.update_status("Re-validating...")
        self.run_validation()

    def action_cursor_down(self) -> None:
        """Move cursor down (vim binding)."""
        table = self.query_one("#main-table", DataTable)
        table.action_cursor_down()

    def action_cursor_up(self) -> None:
        """Move cursor up (vim binding)."""
        table = self.query_one("#main-table", DataTable)
        table.action_cursor_up()


def run_tui(
    skills_dir: Path,
    completed_only: bool = False,
    phase: Optional[int] = None,
    rules_only: bool = False,
    skip_project_rules: bool = False,
) -> None:
    """
    Launch the interactive TUI.

    Args:
        skills_dir: Directory containing skills.
        completed_only: Only show skills with SKILL.md.
        phase: Only show skills in this phase.
        rules_only: Skip community practice checks.
        skip_project_rules: Skip project-specific rule checks.
    """
    app = SkillValidationApp(
        skills_dir=skills_dir,
        completed_only=completed_only,
        phase=phase,
        rules_only=rules_only,
        skip_project_rules=skip_project_rules,
    )
    app.run()
