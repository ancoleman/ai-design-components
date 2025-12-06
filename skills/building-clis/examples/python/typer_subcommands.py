"""
Typer Subcommands Example

Demonstrates: Multi-command CLI with subcommands

Dependencies:
    pip install "typer[all]"

Usage:
    python typer_subcommands.py deploy --env prod
    python typer_subcommands.py logs --follow
    python typer_subcommands.py status
"""

import typer
from typing import Annotated
from enum import Enum

app = typer.Typer(help="Application management CLI")


class Environment(str, Enum):
    """Valid deployment environments."""
    dev = "dev"
    staging = "staging"
    prod = "prod"


@app.command()
def deploy(
    env: Annotated[Environment, typer.Option("--env", help="Target environment")],
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Simulate deployment")] = False,
    version: Annotated[str, typer.Option("--version", help="Version to deploy")] = "latest",
):
    """
    Deploy the application to the specified environment.
    """
    if dry_run:
        typer.echo(f"[DRY RUN] Would deploy version {version} to {env.value}")
    else:
        typer.secho(f"Deploying version {version} to {env.value}...", fg=typer.colors.GREEN)
        # Deployment logic here
        typer.secho("✓ Deployment successful!", fg=typer.colors.GREEN, bold=True)


@app.command()
def logs(
    follow: Annotated[bool, typer.Option("--follow", "-f", help="Follow log output")] = False,
    lines: Annotated[int, typer.Option("--lines", "-n", help="Number of lines to show")] = 10,
):
    """
    View application logs.
    """
    typer.echo(f"Showing last {lines} lines...")

    # Simulated log output
    for i in range(1, lines + 1):
        typer.echo(f"[{i:03d}] Log line {i}")

    if follow:
        typer.secho("\nFollowing logs... (Press Ctrl+C to stop)", fg=typer.colors.YELLOW)


@app.command()
def status():
    """
    Show application status.
    """
    status_info = {
        "Application": "myapp",
        "Status": "Running",
        "Uptime": "2 days",
        "Version": "v1.2.3",
    }

    typer.secho("Application Status:", bold=True)
    for key, value in status_info.items():
        typer.echo(f"  {key}: {value}")


@app.command()
def rollback(
    version: Annotated[str, typer.Argument(help="Version to rollback to")],
    force: Annotated[bool, typer.Option("--force", help="Skip confirmation")] = False,
):
    """
    Rollback to a previous version.
    """
    if not force:
        confirm = typer.confirm(f"Are you sure you want to rollback to version {version}?")
        if not confirm:
            typer.echo("Rollback cancelled.")
            raise typer.Abort()

    typer.secho(f"Rolling back to version {version}...", fg=typer.colors.YELLOW)
    typer.secho("✓ Rollback complete!", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
