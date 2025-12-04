#!/usr/bin/env python3
"""
Batch Skill Validation Script (Rich Output)

Validates all skills against best practices with beautiful terminal output.

Usage:
    python validate_all_skills_rich.py                    # Validate all completed
    python validate_all_skills_rich.py --phase 1          # Validate Phase 1 skills
    python validate_all_skills_rich.py --completed        # Only existing skills
    python validate_all_skills_rich.py --pending          # List pending skills
    python validate_all_skills_rich.py --list-phases      # Show phase breakdown
    python validate_all_skills_rich.py --skill NAME       # Single skill
    python validate_all_skills_rich.py --show-community   # Show community suggestions
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, List, Tuple

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.tree import Tree
    from rich.text import Text
    from rich.columns import Columns
    from rich.rule import Rule
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("Rich library not installed. Install with: pip install rich")
    sys.exit(1)

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Import from validate_skill.py
from validate_skill import (
    Colors, ValidationResult, load_rules, validate_skill, get_default_rules
)

console = Console()


def get_phases(rules: dict) -> dict:
    """Extract phase definitions from rules."""
    return rules.get('phases', {})


def get_all_phase_skills(rules: dict) -> set:
    """Get all skills defined in phases."""
    phases = get_phases(rules)
    all_skills = set()
    for phase_data in phases.values():
        all_skills.update(phase_data.get('skills', []))
    return all_skills


def get_phase_skills(rules: dict, phase_num: int) -> list:
    """Get skills for a specific phase."""
    phases = get_phases(rules)
    phase_key = f'phase_{phase_num}'
    return phases.get(phase_key, {}).get('skills', [])


def get_phase_for_skill(rules: dict, skill_name: str) -> Optional[int]:
    """Find which phase a skill belongs to."""
    phases = get_phases(rules)
    for phase_key, phase_data in phases.items():
        if skill_name in phase_data.get('skills', []):
            return int(phase_key.split('_')[1])
    return None


def create_summary_panel(passed: int, failed: int, pending: int, total: int) -> Panel:
    """Create a summary panel with key metrics."""
    pass_rate = (passed * 100) // (passed + failed) if (passed + failed) > 0 else 0

    # Create colored stats
    stats = []
    stats.append(f"[green bold]{passed}[/green bold] passed")
    stats.append(f"[red bold]{failed}[/red bold] failed")
    if pending > 0:
        stats.append(f"[yellow bold]{pending}[/yellow bold] pending")

    # Pass rate color
    if pass_rate == 100:
        rate_color = "green"
    elif pass_rate >= 80:
        rate_color = "yellow"
    else:
        rate_color = "red"

    content = "  ".join(stats) + f"\n\n[{rate_color} bold]{pass_rate}%[/{rate_color} bold] pass rate"

    return Panel(
        content,
        title=f"[bold cyan]Validation Summary[/bold cyan] • {total} skills",
        border_style="cyan",
        padding=(1, 2),
        expand=False
    )


def create_results_table(results: List[ValidationResult], show_community: bool = False) -> Table:
    """Create a rich table of validation results."""
    table = Table(
        title="Validation Results",
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=False,
        padding=(0, 1)
    )

    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Skill Name", style="bold", min_width=25)
    table.add_column("Status", justify="center", width=8)
    table.add_column("Errors", justify="center", width=8)
    table.add_column("Warnings", justify="center", width=10)
    if show_community:
        table.add_column("Suggestions", justify="center", width=12)

    for i, result in enumerate(results, 1):
        if result.passed:
            status = "[green]PASS[/]"
            row_style = ""
        else:
            status = "[red]FAIL[/]"
            row_style = "dim red"

        errors = str(len(result.errors))
        warnings = str(len(result.warnings))

        if len(result.errors) > 0:
            errors = f"[red]{errors}[/]"
        if len(result.warnings) > 0:
            warnings = f"[yellow]{warnings}[/]"

        row = [str(i), result.skill_name, status, errors, warnings]
        if show_community:
            suggestions = str(len(result.community))
            if len(result.community) > 0:
                suggestions = f"[cyan]{suggestions}[/]"
            row.append(suggestions)

        table.add_row(*row, style=row_style if not result.passed else None)

    return table


def create_pending_table(pending_list: List[Tuple[str, Optional[int]]]) -> Table:
    """Create a table of pending skills."""
    table = Table(
        title="[yellow]Pending Skills[/] (init.md only)",
        box=box.ROUNDED,
        header_style="bold yellow",
        show_lines=False
    )

    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Skill Name", style="yellow")
    table.add_column("Phase", justify="center")

    for i, (name, phase) in enumerate(pending_list, 1):
        phase_str = f"Phase {phase}" if phase else "-"
        table.add_row(str(i), name, phase_str)

    return table


def create_error_tree(failed_results: List[ValidationResult]) -> Tree:
    """Create a tree view of errors for failed skills."""
    tree = Tree("[red bold]Failed Skills[/]", guide_style="red dim")

    for result in failed_results:
        skill_branch = tree.add(f"[red bold]{result.skill_name}[/]")

        if result.errors:
            errors_branch = skill_branch.add("[red]Errors[/]")
            for error in result.errors[:5]:
                errors_branch.add(f"[dim]{error}[/]")
            if len(result.errors) > 5:
                errors_branch.add(f"[dim italic]... and {len(result.errors) - 5} more[/]")

        if result.warnings:
            warnings_branch = skill_branch.add("[yellow]Warnings[/]")
            for warning in result.warnings[:3]:
                warnings_branch.add(f"[dim]{warning}[/]")
            if len(result.warnings) > 3:
                warnings_branch.add(f"[dim italic]... and {len(result.warnings) - 3} more[/]")

    return tree


def create_phases_table(rules: dict) -> Table:
    """Create a table showing phase breakdown."""
    phases = get_phases(rules)

    table = Table(
        title="Skill Development Phases",
        box=box.ROUNDED,
        header_style="bold cyan"
    )

    table.add_column("Phase", style="cyan bold", justify="center")
    table.add_column("Name", style="bold")
    table.add_column("Skills", justify="center")
    table.add_column("Status", justify="center")

    for phase_key in sorted(phases.keys()):
        phase_data = phases[phase_key]
        phase_num = phase_key.split('_')[1]
        name = phase_data.get('name', f'Phase {phase_num}')
        skills = phase_data.get('skills', [])

        table.add_row(
            f"Phase {phase_num}",
            name,
            str(len(skills)),
            "[yellow]Planned[/]"
        )

    return table


def list_phases(rules: dict, skills_dir: Path):
    """Display phases with details."""
    phases = get_phases(rules)

    console.print()
    console.print(Panel("[bold cyan]SKILL DEVELOPMENT PHASES[/]", expand=False))
    console.print()

    console.print(create_phases_table(rules))

    console.print()
    console.print(Rule("Skills per Phase", style="cyan"))

    for phase_key in sorted(phases.keys()):
        phase_data = phases[phase_key]
        phase_num = phase_key.split('_')[1]
        name = phase_data.get('name', f'Phase {phase_num}')
        skills = phase_data.get('skills', [])

        tree = Tree(f"[cyan bold]Phase {phase_num}[/] - {name}")
        for skill in skills:
            skill_path = skills_dir / skill
            if (skill_path / 'SKILL.md').exists():
                tree.add(f"[green]{skill}[/] [dim](completed)[/]")
            elif (skill_path / 'init.md').exists():
                tree.add(f"[yellow]{skill}[/] [dim](planned)[/]")
            else:
                tree.add(f"[red]{skill}[/] [dim](not started)[/]")

        console.print(tree)
        console.print()

    total = sum(len(p.get('skills', [])) for p in phases.values())
    console.print(f"[bold]Total planned skills:[/] {total}")


def list_pending(skills_dir: Path, rules: dict):
    """List pending skills."""
    pending = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir():
            has_init = (skill_dir / 'init.md').exists()
            has_skill = (skill_dir / 'SKILL.md').exists()

            if has_init and not has_skill:
                phase = get_phase_for_skill(rules, skill_dir.name)
                pending.append((skill_dir.name, phase))

    console.print()
    console.print(Panel(f"[bold yellow]PENDING SKILLS[/] • {len(pending)} skills", expand=False))
    console.print()

    if pending:
        console.print(create_pending_table(pending))
    else:
        console.print("[green]No pending skills - all planned skills are complete![/]")


def main():
    parser = argparse.ArgumentParser(
        description='Batch validate Claude Skills (Rich Output)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--phase', '-p', type=int, choices=[1, 2, 3, 4],
                        help='Validate skills in specific phase')
    parser.add_argument('--completed', '-c', action='store_true',
                        help='Only validate existing/completed skills')
    parser.add_argument('--pending', action='store_true',
                        help='List pending skills')
    parser.add_argument('--list-phases', action='store_true',
                        help='Show phase breakdown')
    parser.add_argument('--skill', '-s', type=str,
                        help='Validate single skill by name')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed output')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--rules', '-r', type=Path,
                        help='Path to validation rules YAML')
    parser.add_argument('--show-community', action='store_true',
                        help='Show community practice suggestions')
    parser.add_argument('--no-community', action='store_true',
                        help='Skip community practice checks')
    parser.add_argument('--preset', choices=['minimal', 'standard', 'strict'],
                        help='Override community practices preset')

    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).parent
    rules_path = args.rules or (script_dir / 'validation-rules.yaml')
    skills_dir = script_dir.parent / 'skills'

    # Load rules
    rules = load_rules(rules_path)

    # Override preset if specified
    if args.preset:
        if 'community_presets' not in rules:
            rules['community_presets'] = {}
        rules['community_presets']['active_preset'] = args.preset

    # Disable community checks if requested
    if args.no_community:
        rules['community_practices'] = {}

    phase_skills = get_all_phase_skills(rules)

    # Handle list commands
    if args.list_phases:
        list_phases(rules, skills_dir)
        return 0

    if args.pending:
        list_pending(skills_dir, rules)
        return 0

    # Determine skills to validate
    mode_desc = ""
    if args.skill:
        skill_dir = skills_dir / args.skill
        if not skill_dir.exists():
            console.print(f"[red]Skill not found: {args.skill}[/]")
            return 1
        skills_to_check = [skill_dir]
        mode_desc = f"Single skill: {args.skill}"

    elif args.phase:
        phase_skill_names = get_phase_skills(rules, args.phase)
        skills_to_check = [skills_dir / name for name in phase_skill_names]
        mode_desc = f"Phase {args.phase} skills"

    elif args.completed:
        skills_to_check = []
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / 'SKILL.md').exists():
                skills_to_check.append(skill_dir)
        mode_desc = "Completed skills"

    else:
        skills_to_check = sorted(skills_dir.iterdir())
        mode_desc = "All skills"

    # Header
    console.print()
    console.print(Panel(
        f"[bold cyan]SKILL VALIDATION REPORT[/]\n[dim]{mode_desc}[/]",
        expand=False,
        border_style="cyan"
    ))
    console.print()

    results = []
    pending_list = []
    existing_count = 0

    # Run validation with progress bar
    validatable_skills = [
        p for p in skills_to_check
        if p.is_dir() and (p / 'SKILL.md').exists()
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Validating skills...", total=len(validatable_skills))

        for skill_path in skills_to_check:
            if not skill_path.is_dir():
                continue

            skill_name = skill_path.name
            has_skill_md = (skill_path / 'SKILL.md').exists()
            has_init_md = (skill_path / 'init.md').exists()
            is_phase_skill = skill_name in phase_skills

            if has_skill_md:
                if not is_phase_skill:
                    existing_count += 1

                progress.update(task, description=f"[cyan]Validating {skill_name}...")
                result = validate_skill(skill_path, rules)
                results.append(result)
                progress.advance(task)

            elif has_init_md and (args.phase or not args.completed):
                phase = get_phase_for_skill(rules, skill_name)
                pending_list.append((skill_name, phase))

    # Display results table
    if results:
        console.print(create_results_table(results, args.show_community))

    # Display pending skills
    if pending_list:
        console.print()
        console.print(create_pending_table(pending_list))

    # Calculate summary stats
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    pending_count = len(pending_list)
    total = len(results) + pending_count

    # Display summary panel
    console.print()
    console.print(create_summary_panel(passed, failed, pending_count, total))

    # Show failed details
    failed_results = [r for r in results if not r.passed]
    if failed_results:
        console.print()
        console.print(create_error_tree(failed_results))
        console.print()
        console.print("[dim]Fix with:[/] python scripts/validate_skill.py skills/<name> --verbose")

    # Show community suggestions
    if args.show_community:
        community_results = [r for r in results if r.community]
        if community_results:
            console.print()
            tree = Tree("[cyan bold]Community Suggestions[/]", guide_style="cyan dim")
            for result in community_results:
                skill_branch = tree.add(f"[cyan]{result.skill_name}[/]")
                for suggestion in result.community[:3]:
                    skill_branch.add(f"[dim]{suggestion}[/]")
                if len(result.community) > 3:
                    skill_branch.add(f"[dim italic]... and {len(result.community) - 3} more[/]")
            console.print(tree)

    # JSON output
    if args.json:
        total_community = sum(len(r.community) for r in results)
        skills_with_suggestions = sum(1 for r in results if r.community)
        output = {
            'summary': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'pending': pending_count,
                'pass_rate': (passed * 100) // len(results) if results else 0,
                'community_suggestions': total_community,
                'skills_with_suggestions': skills_with_suggestions,
            },
            'results': [r.to_dict() for r in results],
        }
        console.print()
        console.print_json(json.dumps(output))

    # Final status
    console.print()
    if failed == 0:
        if passed > 0:
            console.print("[green bold]✓ All validated skills passed![/]")
        else:
            console.print("[yellow]No skills to validate[/]")
        return 0
    else:
        console.print(f"[red bold]✗ {failed} skill(s) failed validation[/]")
        return 1


if __name__ == '__main__':
    sys.exit(main())
