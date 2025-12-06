"""
Basic Typer CLI Example

Demonstrates: Simple single-command CLI with arguments and options

Dependencies:
    pip install "typer[all]"

Usage:
    python typer_basic.py Alice
    python typer_basic.py Bob --formal
    python typer_basic.py --help
"""

import typer
from typing import Annotated

app = typer.Typer()


@app.command()
def greet(
    name: Annotated[str, typer.Argument(help="Name of the person to greet")],
    formal: Annotated[bool, typer.Option("--formal", help="Use formal greeting")] = False,
    count: Annotated[int, typer.Option("--count", "-c", help="Number of times to greet")] = 1,
):
    """
    Greet someone with a friendly message.

    This example demonstrates basic argument and option handling with Typer.
    """
    greeting = "Good day" if formal else "Hello"

    for _ in range(count):
        typer.echo(f"{greeting}, {name}!")


if __name__ == "__main__":
    app()
