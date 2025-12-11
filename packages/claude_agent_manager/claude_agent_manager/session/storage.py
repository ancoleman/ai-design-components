"""
Session storage for Claude Agent Manager.

Provides persistent storage for session data using JSON files in the filesystem.
"""

import json
from pathlib import Path
from typing import List, Optional

from claude_agent_manager.session.types.session import Session


class SessionStorage:
    """
    Storage backend for session persistence.

    Stores sessions as JSON files in a designated directory, typically
    ~/.claude_agent_manager/sessions/. Each session is stored in a separate
    file named {session_id}.json.

    Attributes:
        storage_dir: Path to the directory where session files are stored

    Examples:
        >>> storage = SessionStorage()
        >>>
        >>> # Save a session
        >>> session = Session(id='session_123', cwd='/tmp/project')
        >>> path = storage.save(session)
        >>> print(path)
        /Users/username/.claude_agent_manager/sessions/session_123.json
        >>>
        >>> # Load a session
        >>> loaded = storage.load('session_123')
        >>> print(loaded.id)
        session_123
        >>>
        >>> # List all sessions
        >>> session_ids = storage.list()
        >>> print(session_ids)
        ['session_123', 'session_456']
        >>>
        >>> # Delete a session
        >>> storage.delete('session_123')
        True
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize the session storage.

        Args:
            storage_dir: Directory to store session files. If None, defaults to
                        ~/.claude_agent_manager/sessions/

        Examples:
            >>> # Use default directory
            >>> storage = SessionStorage()
            >>>
            >>> # Use custom directory
            >>> storage = SessionStorage(Path('/tmp/sessions'))
        """
        if storage_dir is None:
            storage_dir = Path.home() / ".claude_agent_manager" / "sessions"

        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save(self, session: Session) -> Path:
        """
        Save a session to disk.

        Serializes the session to JSON and writes it to a file named
        {session_id}.json in the storage directory.

        Args:
            session: The session to save

        Returns:
            Path to the saved session file

        Examples:
            >>> storage = SessionStorage()
            >>> session = Session(id='session_123', cwd='/tmp')
            >>> path = storage.save(session)
            >>> print(path.exists())
            True
        """
        session_file = self.storage_dir / f"{session.id}.json"

        # Serialize session to JSON
        data = session.to_dict()

        # Write to file with pretty formatting
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return session_file

    def load(self, session_id: str) -> Optional[Session]:
        """
        Load a session from disk.

        Args:
            session_id: The session ID to load

        Returns:
            Session object if found, None if the session file doesn't exist

        Examples:
            >>> storage = SessionStorage()
            >>> session = storage.load('session_123')
            >>> if session:
            ...     print(session.id)
            ... else:
            ...     print("Session not found")
        """
        session_file = self.storage_dir / f"{session_id}.json"

        if not session_file.exists():
            return None

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return Session.from_dict(data)

        except (json.JSONDecodeError, KeyError, ValueError):
            # Invalid session file
            return None

    def list(self) -> List[str]:
        """
        List all stored session IDs.

        Returns:
            List of session IDs (filenames without .json extension)

        Examples:
            >>> storage = SessionStorage()
            >>> session_ids = storage.list()
            >>> print(session_ids)
            ['session_123', 'session_456', 'session_789']
        """
        if not self.storage_dir.exists():
            return []

        session_files = self.storage_dir.glob("*.json")
        return [f.stem for f in session_files]

    def delete(self, session_id: str) -> bool:
        """
        Delete a session from disk.

        Args:
            session_id: The session ID to delete

        Returns:
            True if the session was deleted, False if it didn't exist

        Examples:
            >>> storage = SessionStorage()
            >>> storage.delete('session_123')
            True
            >>> storage.delete('nonexistent')
            False
        """
        session_file = self.storage_dir / f"{session_id}.json"

        if not session_file.exists():
            return False

        try:
            session_file.unlink()
            return True
        except OSError:
            return False

    def exists(self, session_id: str) -> bool:
        """
        Check if a session exists in storage.

        Args:
            session_id: The session ID to check

        Returns:
            True if the session file exists, False otherwise

        Examples:
            >>> storage = SessionStorage()
            >>> if storage.exists('session_123'):
            ...     print("Session exists")
            ... else:
            ...     print("Session not found")
        """
        session_file = self.storage_dir / f"{session_id}.json"
        return session_file.exists()
