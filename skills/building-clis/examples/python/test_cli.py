"""
CLI Testing Example

Demonstrates: Testing CLI commands with pytest and Typer's CliRunner

Dependencies:
    pip install "typer[all]" pytest

Usage:
    pytest test_cli.py -v
"""

import pytest
from typer.testing import CliRunner
from typer_subcommands import app  # Import from typer_subcommands.py

runner = CliRunner()


def test_deploy_command():
    """Test deploy command with required env flag."""
    result = runner.invoke(app, ["deploy", "--env", "prod"])
    assert result.exit_code == 0
    assert "Deploying" in result.stdout
    assert "prod" in result.stdout


def test_deploy_dry_run():
    """Test deploy command with dry-run flag."""
    result = runner.invoke(app, ["deploy", "--env", "staging", "--dry-run"])
    assert result.exit_code == 0
    assert "[DRY RUN]" in result.stdout
    assert "staging" in result.stdout


def test_logs_command():
    """Test logs command with default parameters."""
    result = runner.invoke(app, ["logs"])
    assert result.exit_code == 0
    assert "Showing last 10 lines" in result.stdout


def test_logs_with_lines_option():
    """Test logs command with custom line count."""
    result = runner.invoke(app, ["logs", "--lines", "5"])
    assert result.exit_code == 0
    assert "Showing last 5 lines" in result.stdout


def test_status_command():
    """Test status command."""
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Application Status" in result.stdout
    assert "Running" in result.stdout


def test_missing_required_flag():
    """Test that missing required flag returns error."""
    result = runner.invoke(app, ["deploy"])
    assert result.exit_code != 0


def test_invalid_environment():
    """Test that invalid environment value is rejected."""
    result = runner.invoke(app, ["deploy", "--env", "invalid"])
    assert result.exit_code != 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
