"""
Utility functions and helpers for Claude Agent Manager.

Provides logging configuration, file system utilities, and other shared helpers.
"""

from .logging import Colors, log
from .path import (
    encode_project_path,
    get_claude_projects_dir,
    get_project_session_dir,
    get_session_file_path,
    list_session_files,
)

__all__ = [
    # Logging utilities
    "Colors",
    "log",
    # Path utilities
    "get_claude_projects_dir",
    "encode_project_path",
    "get_project_session_dir",
    "list_session_files",
    "get_session_file_path",
]
