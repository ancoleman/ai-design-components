#!/usr/bin/env python3
"""
Interactive Skill Validation Dashboard (Textual TUI)

A full interactive terminal UI for validating Claude Skills.

Usage:
    python validate_skills_tui.py                    # Launch dashboard
    python validate_skills_tui.py --completed        # Only completed skills
    python validate_skills_tui.py --phase 1          # Phase 1 skills only

Controls:
    ↑/↓ or j/k    Navigate skills
    Enter/Space   Expand/collapse details
    f             Filter by status
    /             Search skills
    r             Re-run validation
    q             Quit
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Static, DataTable, Label,
    Input, Button, Rule, LoadingIndicator
)
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import work
from textual.worker import Worker, get_current_worker

from rich.text import Text
from rich.panel import Panel
from rich.table import Table

# Import validation logic
from validate_skill import (
    ValidationResult, load_rules, validate_skill
)


@dataclass
class SkillData:
    """Container for skill validation data."""
    name: str
    status: str  # 'pass', 'fail', 'pending'
    errors: List[str]
    warnings: List[str]
    community: List[str]
    result: Optional[ValidationResult] = None


class DetailPanel(Static):
    """Panel showing detailed errors/warnings for selected skill."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill_data: Optional[SkillData] = None

    def update_skill(self, skill: Optional[SkillData]):
        """Update the panel with skill details."""
        self.skill_data = skill
        if skill is None:
            self.update("[dim]Select a skill to view details[/dim]")
            return

        content = []

        # Header
        if skill.status == 'pass':
            status_icon = "[green]✓[/green]"
            status_text = "[green]PASSED[/green]"
        elif skill.status == 'fail':
            status_icon = "[red]✗[/red]"
            status_text = "[red]FAILED[/red]"
        else:
            status_icon = "[yellow]○[/yellow]"
            status_text = "[yellow]PENDING[/yellow]"

        content.append(f"{status_icon} [bold]{skill.name}[/bold] - {status_text}")
        content.append("")

        # Errors
        if skill.errors:
            content.append("[red bold]Errors:[/red bold]")
            for error in skill.errors:
                content.append(f"  [red]•[/red] {error}")
            content.append("")

        # Warnings
        if skill.warnings:
            content.append("[yellow bold]Warnings:[/yellow bold]")
            for warning in skill.warnings[:10]:  # Limit display
                content.append(f"  [yellow]•[/yellow] {warning}")
            if len(skill.warnings) > 10:
                content.append(f"  [dim]... and {len(skill.warnings) - 10} more[/dim]")
            content.append("")

        # Community suggestions
        if skill.community:
            content.append("[cyan bold]Community Suggestions:[/cyan bold]")
            for suggestion in skill.community[:5]:
                content.append(f"  [cyan]•[/cyan] {suggestion}")
            if len(skill.community) > 5:
                content.append(f"  [dim]... and {len(skill.community) - 5} more[/dim]")

        if not skill.errors and not skill.warnings and not skill.community:
            content.append("[green]No issues found![/green]")

        self.update("\n".join(content))


class SummaryBar(Static):
    """Summary statistics bar."""

    def update_stats(self, passed: int, failed: int, pending: int):
        total = passed + failed + pending
        validated = passed + failed
        pass_rate = (passed * 100 // validated) if validated > 0 else 0

        if pass_rate == 100:
            rate_style = "green bold"
        elif pass_rate >= 80:
            rate_style = "yellow bold"
        else:
            rate_style = "red bold"

        text = Text()
        text.append(f"  Total: {total}  │  ", style="dim")
        text.append(f"✓ {passed}", style="green bold")
        text.append("  │  ", style="dim")
        text.append(f"✗ {failed}", style="red bold")
        if pending > 0:
            text.append("  │  ", style="dim")
            text.append(f"○ {pending}", style="yellow bold")
        text.append("  │  ", style="dim")
        text.append(f"{pass_rate}%", style=rate_style)
        text.append(" pass rate", style="dim")

        self.update(text)


class FilterModal(ModalScreen):
    """Modal for filtering skills."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
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

    #loading-container {
        width: 100%;
        height: 100%;
        align: center middle;
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
        Binding("slash", "search", "Search"),
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "toggle_details", "Details", show=False),
        Binding("space", "toggle_details", "Details", show=False),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
    ]

    def __init__(self, skills_dir: Path, rules: dict, mode: str = "all", phase: int = None):
        super().__init__()
        self.skills_dir = skills_dir
        self.rules = rules
        self.mode = mode
        self.phase = phase
        self.skills_data: List[SkillData] = []
        self.filtered_data: List[SkillData] = []
        self.current_filter = "all"
        self.search_query = ""
        self.selected_skill: Optional[SkillData] = None

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
        self.sub_title = f"Mode: {self.mode}"

        # Setup table
        table = self.query_one("#main-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("#", "Skill Name", "Status", "Err", "Warn")

        # Start validation
        self.run_validation()

    @work(exclusive=True, thread=True)
    def run_validation(self) -> None:
        """Run validation in background thread."""
        worker = get_current_worker()

        # Collect skills to validate
        skills_to_check = []

        if self.mode == "completed":
            for skill_dir in sorted(self.skills_dir.iterdir()):
                if skill_dir.is_dir() and (skill_dir / 'SKILL.md').exists():
                    skills_to_check.append(skill_dir)
        elif self.mode == "phase" and self.phase:
            phases = self.rules.get('phases', {})
            phase_key = f'phase_{self.phase}'
            phase_skills = phases.get(phase_key, {}).get('skills', [])
            for name in phase_skills:
                skill_path = self.skills_dir / name
                if skill_path.exists():
                    skills_to_check.append(skill_path)
        else:
            for skill_dir in sorted(self.skills_dir.iterdir()):
                if skill_dir.is_dir():
                    skills_to_check.append(skill_dir)

        # Validate each skill
        results = []
        total = len(skills_to_check)

        for i, skill_path in enumerate(skills_to_check):
            if worker.is_cancelled:
                return

            skill_name = skill_path.name
            has_skill_md = (skill_path / 'SKILL.md').exists()
            has_init_md = (skill_path / 'init.md').exists()

            # Update status
            self.call_from_thread(
                self.update_status,
                f"Validating {skill_name}... ({i+1}/{total})"
            )

            if has_skill_md:
                result = validate_skill(skill_path, self.rules)
                skill_data = SkillData(
                    name=skill_name,
                    status='pass' if result.passed else 'fail',
                    errors=result.errors,
                    warnings=result.warnings,
                    community=result.community,
                    result=result
                )
            elif has_init_md:
                skill_data = SkillData(
                    name=skill_name,
                    status='pending',
                    errors=[],
                    warnings=[],
                    community=[]
                )
            else:
                continue

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
        """Apply current filter and search to data."""
        filtered = self.skills_data

        # Apply status filter
        if self.current_filter == "pass":
            filtered = [s for s in filtered if s.status == 'pass']
        elif self.current_filter == "fail":
            filtered = [s for s in filtered if s.status == 'fail']
        elif self.current_filter == "warn":
            filtered = [s for s in filtered if s.warnings]

        # Apply search
        if self.search_query:
            query = self.search_query.lower()
            filtered = [s for s in filtered if query in s.name.lower()]

        self.filtered_data = filtered
        self.refresh_table()
        self.update_summary()

    def refresh_table(self) -> None:
        """Refresh the data table."""
        table = self.query_one("#main-table", DataTable)
        table.clear()

        for i, skill in enumerate(self.filtered_data, 1):
            if skill.status == 'pass':
                status = Text("✓ PASS", style="green")
            elif skill.status == 'fail':
                status = Text("✗ FAIL", style="bold red")
            else:
                status = Text("○ PEND", style="yellow")

            errors = Text(str(len(skill.errors)), style="red" if skill.errors else "dim")
            warnings = Text(str(len(skill.warnings)), style="yellow" if skill.warnings else "dim")

            table.add_row(str(i), skill.name, status, errors, warnings, key=skill.name)

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

    def action_search(self) -> None:
        """Focus search (simplified - just toggle)."""
        # For now, cycle through simple filters
        filters = ["all", "pass", "fail"]
        current_idx = filters.index(self.current_filter) if self.current_filter in filters else 0
        self.current_filter = filters[(current_idx + 1) % len(filters)]
        self.apply_filter()
        self.update_status(f"Filter: {self.current_filter}")

    def action_refresh(self) -> None:
        """Re-run validation."""
        self.skills_data = []
        self.filtered_data = []
        table = self.query_one("#main-table", DataTable)
        table.clear()
        self.update_status("Re-validating...")
        self.run_validation()

    def action_toggle_details(self) -> None:
        """Toggle details panel visibility or expand details."""
        # Currently just ensures detail panel is updated
        if self.selected_skill:
            detail = self.query_one("#detail-panel", DetailPanel)
            detail.update_skill(self.selected_skill)

    def action_cursor_down(self) -> None:
        """Move cursor down (vim binding)."""
        table = self.query_one("#main-table", DataTable)
        table.action_cursor_down()

    def action_cursor_up(self) -> None:
        """Move cursor up (vim binding)."""
        table = self.query_one("#main-table", DataTable)
        table.action_cursor_up()


def main():
    parser = argparse.ArgumentParser(
        description='Interactive Skill Validation Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--completed', '-c', action='store_true',
                        help='Only validate completed skills')
    parser.add_argument('--phase', '-p', type=int, choices=[1, 2, 3, 4],
                        help='Validate skills in specific phase')
    parser.add_argument('--rules', '-r', type=Path,
                        help='Path to validation rules YAML')

    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).parent
    rules_path = args.rules or (script_dir / 'validation-rules.yaml')
    skills_dir = script_dir.parent / 'skills'

    # Load rules
    rules = load_rules(rules_path)

    # Determine mode
    if args.completed:
        mode = "completed"
    elif args.phase:
        mode = "phase"
    else:
        mode = "all"

    # Run app
    app = SkillValidationApp(
        skills_dir=skills_dir,
        rules=rules,
        mode=mode,
        phase=args.phase
    )
    app.run()


if __name__ == '__main__':
    main()
