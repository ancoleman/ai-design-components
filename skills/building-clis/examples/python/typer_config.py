"""
Typer Configuration Management Example

Demonstrates: Loading config from files, env vars, and CLI args with precedence

Dependencies:
    pip install "typer[all]" pyyaml

Usage:
    python typer_config.py --host localhost --port 8080
    MYAPP_PORT=9000 python typer_config.py
"""

import os
import yaml
import typer
from pathlib import Path
from typing import Annotated, Optional

app = typer.Typer()


def load_config() -> dict:
    """Load configuration from multiple sources with precedence."""
    config = {}

    # 1. System config
    system_config = Path("/etc/myapp/config.yaml")
    if system_config.exists():
        config.update(yaml.safe_load(system_config.read_text()))

    # 2. User config
    user_config = Path.home() / ".config" / "myapp" / "config.yaml"
    if user_config.exists():
        config.update(yaml.safe_load(user_config.read_text()))

    # 3. Local config
    local_config = Path("./myapp.yaml")
    if local_config.exists():
        config.update(yaml.safe_load(local_config.read_text()))

    return config


@app.command()
def serve(
    host: Annotated[Optional[str], typer.Option("--host", help="Server host")] = None,
    port: Annotated[Optional[int], typer.Option("--port", help="Server port")] = None,
):
    """
    Start server with configuration from multiple sources.

    Precedence (highest to lowest):
      1. CLI arguments (--host, --port)
      2. Environment variables (MYAPP_HOST, MYAPP_PORT)
      3. Config files (./myapp.yaml, ~/.config/myapp/config.yaml)
      4. Built-in defaults
    """
    config = load_config()

    # Apply precedence: CLI > Env > Config > Default
    final_host = host or os.getenv("MYAPP_HOST") or config.get("host") or "localhost"
    final_port = port or int(os.getenv("MYAPP_PORT", 0)) or config.get("port") or 8080

    typer.secho(f"Starting server at {final_host}:{final_port}", fg=typer.colors.GREEN)
    typer.echo("\nEffective configuration:")
    typer.echo(f"  Host: {final_host}")
    typer.echo(f"  Port: {final_port}")


@app.command("config-show")
def config_show():
    """Show effective configuration (after merging all sources)."""
    config = load_config()
    typer.echo(yaml.dump(config, default_flow_style=False))


if __name__ == "__main__":
    app()
