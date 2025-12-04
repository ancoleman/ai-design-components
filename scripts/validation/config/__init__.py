"""
Configuration module for skill validation.

This module provides utilities for loading and managing validation rules,
community practices, and project-specific rules.
"""

from pathlib import Path

# Default config file paths (relative to this module)
CONFIG_DIR = Path(__file__).parent
DEFAULT_RULES_PATH = CONFIG_DIR / "rules.yaml"
DEFAULT_COMMUNITY_PATH = CONFIG_DIR / "community.yaml"
DEFAULT_PROJECT_PATH = CONFIG_DIR / "project.yaml"


def get_default_rules_path() -> Path:
    """Get the path to the default rules.yaml file."""
    return DEFAULT_RULES_PATH


def get_default_community_path() -> Path:
    """Get the path to the default community.yaml file."""
    return DEFAULT_COMMUNITY_PATH


def get_default_project_path() -> Path:
    """Get the path to the default project.yaml file."""
    return DEFAULT_PROJECT_PATH
