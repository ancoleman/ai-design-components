"""
Logging utilities for Claude Agent Manager.

Provides colored console logging with ANSI color codes and level-based formatting.
"""

import sys
from typing import Literal


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


LogLevel = Literal["INFO", "DEBUG", "SUCCESS", "WARNING", "ERROR"]


def log(message: str, level: LogLevel = "INFO") -> None:
    """
    Print a colored log message based on the level.

    Args:
        message: The message to log
        level: The log level (INFO, DEBUG, SUCCESS, WARNING, ERROR)

    Example:
        >>> log("Starting process", "INFO")
        [INFO] Starting process
        >>> log("Operation completed", "SUCCESS")
        [SUCCESS] Operation completed
        >>> log("File not found", "ERROR")
        [ERROR] File not found
    """
    # Map log levels to colors
    level_colors = {
        "INFO": Colors.BLUE,
        "DEBUG": Colors.CYAN,
        "SUCCESS": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
    }

    # Get color for level (default to no color if level not recognized)
    color = level_colors.get(level, "")

    # Format and print message
    formatted_message = f"{color}{Colors.BOLD}[{level}]{Colors.RESET} {message}"

    # Print to stderr for ERROR and WARNING, stdout for others
    output = sys.stderr if level in ("ERROR", "WARNING") else sys.stdout
    print(formatted_message, file=output)
