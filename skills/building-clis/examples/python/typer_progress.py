"""
Typer Progress Indicators Example

Demonstrates: Progress bars, spinners, and colored output

Dependencies:
    pip install "typer[all]"

Usage:
    python typer_progress.py process --count 50
    python typer_progress.py spinner
"""

import typer
import time
from rich.progress import Progress, track
from rich.console import Console
from typing import Annotated

app = typer.Typer()
console = Console()


@app.command()
def process(
    count: Annotated[int, typer.Option("--count", help="Number of items")] = 100
):
    """Process items with a progress bar."""
    console.print(f"[cyan]Processing {count} items...[/cyan]")

    # Using rich progress bar
    for _ in track(range(count), description="Processing..."):
        time.sleep(0.05)  # Simulate work

    console.print("[green]✓ All items processed![/green]")


@app.command()
def spinner():
    """Long-running task with spinner."""
    with console.status("[bold green]Working...") as status:
        time.sleep(2)
        status.update("[bold yellow]Still working...")
        time.sleep(2)

    console.print("[green]✓ Complete![/green]")


if __name__ == "__main__":
    app()
