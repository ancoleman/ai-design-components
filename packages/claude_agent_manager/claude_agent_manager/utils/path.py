"""
Path utilities for Claude Agent Manager.

Provides functions for working with Claude's project directory structure,
session files, and path encoding.
"""

from pathlib import Path
from typing import List


def get_claude_projects_dir() -> Path:
    """
    Return the Claude projects directory path.

    Returns:
        Path: The ~/.claude/projects/ directory path

    Example:
        >>> projects_dir = get_claude_projects_dir()
        >>> print(projects_dir)
        /Users/username/.claude/projects
    """
    return Path.home() / ".claude" / "projects"


def encode_project_path(path: str) -> str:
    """
    Encode a file path for use as a directory name.

    Replaces forward slashes with hyphens to match Claude's encoding scheme.

    Args:
        path: The file path to encode

    Returns:
        str: The encoded path safe for use as a directory name

    Example:
        >>> encode_project_path("/Users/user/project")
        '-Users-user-project'
        >>> encode_project_path("/home/user/my-app")
        '-home-user-my-app'
    """
    return path.replace("/", "-")


def get_project_session_dir(cwd: str) -> Path:
    """
    Return the session directory for a given working directory.

    Args:
        cwd: The current working directory path

    Returns:
        Path: The session directory path for the project

    Example:
        >>> session_dir = get_project_session_dir("/Users/user/project")
        >>> print(session_dir)
        /Users/username/.claude/projects/-Users-user-project
    """
    projects_dir = get_claude_projects_dir()
    encoded_path = encode_project_path(cwd)
    return projects_dir / encoded_path


def list_session_files(cwd: str) -> List[Path]:
    """
    List all .jsonl session files in a project directory.

    Sorts files by modification time with newest first.

    Args:
        cwd: The current working directory path

    Returns:
        List[Path]: List of session file paths, sorted by modification time (newest first)

    Example:
        >>> files = list_session_files("/Users/user/project")
        >>> for f in files:
        ...     print(f.name)
        session_abc123.jsonl
        session_def456.jsonl
    """
    session_dir = get_project_session_dir(cwd)

    # Return empty list if directory doesn't exist
    if not session_dir.exists():
        return []

    # Get all .jsonl files
    session_files = list(session_dir.glob("*.jsonl"))

    # Sort by modification time, newest first
    session_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    return session_files


def get_session_file_path(cwd: str, session_id: str) -> Path:
    """
    Get path to a specific session file.

    Args:
        cwd: The current working directory path
        session_id: The session identifier

    Returns:
        Path: The path to the session file

    Example:
        >>> path = get_session_file_path("/Users/user/project", "abc123")
        >>> print(path)
        /Users/username/.claude/projects/-Users-user-project/session_abc123.jsonl
    """
    session_dir = get_project_session_dir(cwd)
    return session_dir / f"session_{session_id}.jsonl"
