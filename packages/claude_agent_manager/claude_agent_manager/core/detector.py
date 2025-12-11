"""Binary detection module for Claude Code CLI.

This module provides functionality to detect and locate the Claude Code CLI binary,
handling various installation methods and paths.
"""

import asyncio
import os
import shutil
from dataclasses import dataclass
from typing import Optional


@dataclass
class DetectionResult:
    """Result of binary detection.

    Attributes:
        available: Whether the binary was found
        path: Full path to the binary if found
        version: Version string if available
        error: Error message if detection failed
    """
    available: bool
    path: Optional[str] = None
    version: Optional[str] = None
    error: Optional[str] = None


class AgentDetector:
    """Detector for Claude Code CLI binary.

    Searches common installation locations and PATH to find the Claude Code CLI.
    Caches detection results to avoid repeated searches.
    """

    # Common binary installation locations
    ADDITIONAL_PATHS = [
        '/opt/homebrew/bin',           # Homebrew Apple Silicon
        '/opt/homebrew/sbin',
        '/usr/local/bin',              # Homebrew Intel / common
        '/usr/local/sbin',
        '{home}/.local/bin',           # pip, poetry, etc.
        '{home}/.npm-global/bin',      # npm global
        '{home}/bin',                  # User bin
        '{home}/.claude/local',        # Claude local install
        '/usr/bin',
        '/bin',
        '/usr/sbin',
        '/sbin'
    ]

    def __init__(self, binary_name: str = 'claude'):
        """Initialize the detector.

        Args:
            binary_name: Name of the binary to detect (default: 'claude')
        """
        self.binary_name = binary_name
        self._cached_result: Optional[DetectionResult] = None

    def get_expanded_path(self) -> str:
        """Build an expanded PATH that includes common Claude Code installation locations.

        Packaged apps and certain environments may not inherit the full shell PATH,
        so we explicitly add common binary locations.

        Returns:
            Expanded PATH string with additional binary directories
        """
        home = os.path.expanduser("~")

        # Expand {home} placeholders in paths
        additional_paths = [
            p.format(home=home) for p in self.ADDITIONAL_PATHS
        ]

        current_path = os.environ.get('PATH', '')
        existing = set(current_path.split(':'))

        # Prepend additional paths that aren't already present and exist
        new_paths = [
            p for p in additional_paths
            if p not in existing and os.path.isdir(p)
        ]

        return ':'.join(new_paths + list(existing))

    def get_env_with_expanded_path(self) -> dict:
        """Get environment dictionary with expanded PATH.

        Returns:
            Environment dict with PATH expanded to include common locations
        """
        env = os.environ.copy()
        env['PATH'] = self.get_expanded_path()
        return env

    async def _get_version(self, path: str) -> Optional[str]:
        """Get version string from binary.

        Args:
            path: Full path to the binary

        Returns:
            Version string if available, None otherwise
        """
        try:
            process = await asyncio.create_subprocess_exec(
                path,
                '--version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=5.0
            )

            if process.returncode == 0 and stdout:
                # Get first line of version output
                version = stdout.decode('utf-8').strip().split('\n')[0]
                return version

        except asyncio.TimeoutError:
            pass
        except Exception:
            pass

        return None

    async def detect(self, force_refresh: bool = False) -> DetectionResult:
        """Detect Claude Code CLI binary.

        Tries multiple detection methods:
        1. shutil.which with current PATH
        2. which command with expanded PATH
        3. Direct check of common installation locations

        Args:
            force_refresh: If True, ignore cached result and re-detect

        Returns:
            DetectionResult with binary information
        """
        # Return cached result if available and not forcing refresh
        if not force_refresh and self._cached_result is not None:
            return self._cached_result

        # Try shutil.which with current PATH
        claude_path = shutil.which(self.binary_name)

        if claude_path:
            version = await self._get_version(claude_path)
            result = DetectionResult(
                available=True,
                path=claude_path,
                version=version
            )
            self._cached_result = result
            return result

        # Try with expanded PATH via subprocess
        try:
            process = await asyncio.create_subprocess_exec(
                'which',
                self.binary_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=self.get_env_with_expanded_path()
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=5.0
            )

            if process.returncode == 0 and stdout:
                path = stdout.decode('utf-8').strip().split('\n')[0]
                if path:
                    version = await self._get_version(path)
                    result = DetectionResult(
                        available=True,
                        path=path,
                        version=version
                    )
                    self._cached_result = result
                    return result

        except asyncio.TimeoutError:
            pass
        except Exception:
            pass

        # Check common locations directly
        home = os.path.expanduser("~")
        common_locations = [
            f'/opt/homebrew/bin/{self.binary_name}',
            f'/usr/local/bin/{self.binary_name}',
            f'{home}/.local/bin/{self.binary_name}',
            f'{home}/.npm-global/bin/{self.binary_name}',
            f'{home}/.claude/local/{self.binary_name}',
        ]

        for location in common_locations:
            if os.path.isfile(location) and os.access(location, os.X_OK):
                version = await self._get_version(location)
                result = DetectionResult(
                    available=True,
                    path=location,
                    version=version
                )
                self._cached_result = result
                return result

        # Binary not found
        error_message = (
            f"{self.binary_name} CLI not found. Please install it:\n"
            "  npm install -g @anthropic-ai/claude-code\n"
            "  # or\n"
            "  brew install claude-code\n"
            "\n"
            "Then authenticate:\n"
            f"  {self.binary_name} login"
        )

        result = DetectionResult(
            available=False,
            error=error_message
        )
        self._cached_result = result
        return result
