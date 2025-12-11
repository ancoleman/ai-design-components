"""
Session file watcher for Claude Agent Manager.

Monitors Claude's project session directory for changes to session files,
emitting events when sessions are created, modified, or deleted.
"""

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from claude_agent_manager.core.events import Event, EventEmitter, EventType
from claude_agent_manager.utils.path import get_project_session_dir, list_session_files


@dataclass
class SessionFileInfo:
    """
    Information about a Claude session file.

    Attributes:
        session_id: The Claude session ID (extracted from filename)
        path: Full path to the session file
        size: File size in bytes
        modified_at: Last modification timestamp
        message_count: Number of messages in the session
        first_message: First user message content (for display)
        cost_usd: Approximate cost in USD (if available)

    Examples:
        >>> info = SessionFileInfo(
        ...     session_id='abc123',
        ...     path=Path('/Users/user/.claude/projects/-tmp-project/session_abc123.jsonl'),
        ...     size=12345,
        ...     modified_at=datetime.now(),
        ...     message_count=10,
        ...     first_message='Explain this code'
        ... )
    """
    session_id: str
    path: Path
    size: int
    modified_at: datetime
    message_count: int = 0
    first_message: Optional[str] = None
    cost_usd: float = 0.0


class SessionWatcher:
    """
    Watches Claude's session directory for file changes.

    Polls the session directory at regular intervals and emits events when
    session files are created, modified, or deleted. Parses session files
    to extract metadata like message count and first message.

    Features:
        - Automatic project directory detection
        - File change detection (create/modify/delete)
        - Session file parsing for metadata
        - Configurable poll interval
        - Async event emission

    Events Emitted:
        - FILE_CREATED: New session file detected
        - FILE_MODIFIED: Existing session file changed
        - FILE_DELETED: Session file removed

    Examples:
        >>> # Create watcher
        >>> emitter = EventEmitter()
        >>> watcher = SessionWatcher('/tmp/project', emitter=emitter)
        >>>
        >>> # Register event handlers
        >>> @emitter.on(EventType.FILE_CREATED)
        >>> async def on_new_session(event: Event):
        ...     print(f"New session: {event.data['session_id']}")
        >>>
        >>> # Start watching
        >>> await watcher.start()
        >>>
        >>> # Stop watching
        >>> await watcher.stop()
    """

    def __init__(
        self,
        cwd: str,
        emitter: Optional[EventEmitter] = None,
        poll_interval: float = 1.0
    ):
        """
        Initialize the session watcher.

        Args:
            cwd: Working directory to watch (project root)
            emitter: EventEmitter for file change events (creates new if None)
            poll_interval: Seconds between poll checks (default: 1.0)

        Examples:
            >>> # Basic watcher
            >>> watcher = SessionWatcher('/tmp/project')
            >>>
            >>> # With custom poll interval
            >>> watcher = SessionWatcher('/tmp/project', poll_interval=2.0)
            >>>
            >>> # With shared emitter
            >>> emitter = EventEmitter()
            >>> watcher = SessionWatcher('/tmp/project', emitter=emitter)
        """
        self.cwd = cwd
        self.emitter = emitter or EventEmitter()
        self.poll_interval = poll_interval
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._file_states: Dict[str, int] = {}  # session_id -> file_size

    def _get_project_dir(self) -> Path:
        """
        Get the Claude project directory for the current working directory.

        Returns:
            Path to the project session directory

        Examples:
            >>> watcher = SessionWatcher('/tmp/project')
            >>> project_dir = watcher._get_project_dir()
            >>> print(project_dir)
            /Users/username/.claude/projects/-tmp-project
        """
        return get_project_session_dir(self.cwd)

    def list_sessions(self) -> List[SessionFileInfo]:
        """
        List all session files in the project directory.

        Parses each session file to extract metadata.

        Returns:
            List of SessionFileInfo objects, sorted by modification time (newest first)

        Examples:
            >>> watcher = SessionWatcher('/tmp/project')
            >>> sessions = watcher.list_sessions()
            >>> for session in sessions:
            ...     print(f"{session.session_id}: {session.message_count} messages")
        """
        session_files = list_session_files(self.cwd)
        sessions = []

        for file_path in session_files:
            info = self._parse_session_file(file_path)
            if info:
                sessions.append(info)

        return sessions

    def _parse_session_file(self, path: Path) -> Optional[SessionFileInfo]:
        """
        Parse a session file and extract metadata.

        Args:
            path: Path to the session file

        Returns:
            SessionFileInfo if file is valid, None otherwise

        Examples:
            >>> watcher = SessionWatcher('/tmp/project')
            >>> path = Path('/Users/user/.claude/projects/-tmp-project/session_abc123.jsonl')
            >>> info = watcher._parse_session_file(path)
            >>> if info:
            ...     print(f"Messages: {info.message_count}")
        """
        try:
            # Extract session ID from filename
            # Format: session_{session_id}.jsonl
            filename = path.stem  # Remove .jsonl extension
            if not filename.startswith('session_'):
                return None

            session_id = filename.replace('session_', '', 1)

            # Get file stats
            stat = path.stat()
            size = stat.st_size
            modified_at = datetime.fromtimestamp(stat.st_mtime)

            # Parse file to count messages and extract first user message
            message_count = 0
            first_message = None
            cost_usd = 0.0

            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        data = json.loads(line)
                        msg_type = data.get('type', '')

                        # Count messages
                        if msg_type in ('user', 'assistant'):
                            message_count += 1

                            # Extract first user message
                            if msg_type == 'user' and first_message is None:
                                message_data = data.get('message', {})
                                content = message_data.get('content', [])

                                # Extract text from content array
                                for item in content:
                                    if isinstance(item, dict) and item.get('type') == 'text':
                                        text = item.get('text', '').strip()
                                        if text:
                                            first_message = text
                                            break

                        # Try to extract cost information
                        if 'total_cost_usd' in data:
                            cost_usd = data['total_cost_usd']

                    except json.JSONDecodeError:
                        # Skip invalid JSON lines
                        continue

            return SessionFileInfo(
                session_id=session_id,
                path=path,
                size=size,
                modified_at=modified_at,
                message_count=message_count,
                first_message=first_message,
                cost_usd=cost_usd
            )

        except (OSError, ValueError):
            return None

    async def start(self) -> None:
        """
        Start watching the session directory for changes.

        Begins the polling loop in a background task.

        Examples:
            >>> watcher = SessionWatcher('/tmp/project')
            >>> await watcher.start()
            >>> # Watcher is now running in background
        """
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._poll_loop())

    async def stop(self) -> None:
        """
        Stop watching the session directory.

        Cancels the polling loop and waits for cleanup.

        Examples:
            >>> watcher = SessionWatcher('/tmp/project')
            >>> await watcher.start()
            >>> # ... later ...
            >>> await watcher.stop()
        """
        if not self._running:
            return

        self._running = False

        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _poll_loop(self) -> None:
        """
        Main polling loop.

        Checks for file changes at regular intervals and emits events.
        """
        project_dir = self._get_project_dir()

        while self._running:
            try:
                await self._check_changes(project_dir)
                await asyncio.sleep(self.poll_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Log error but continue polling
                print(f"Error in poll loop: {e}")
                await asyncio.sleep(self.poll_interval)

    async def _check_changes(self, project_dir: Path) -> None:
        """
        Check for file changes and emit events.

        Compares current file states with previous states to detect
        creates, modifies, and deletes.

        Args:
            project_dir: Path to the project session directory
        """
        if not project_dir.exists():
            return

        # Get current state
        current_files = {}
        for file_path in project_dir.glob("*.jsonl"):
            if file_path.stem.startswith('session_'):
                session_id = file_path.stem.replace('session_', '', 1)
                try:
                    size = file_path.stat().st_size
                    current_files[session_id] = size
                except OSError:
                    continue

        # Detect changes
        previous_ids = set(self._file_states.keys())
        current_ids = set(current_files.keys())

        # New files (created)
        created = current_ids - previous_ids
        for session_id in created:
            file_path = project_dir / f"session_{session_id}.jsonl"
            info = self._parse_session_file(file_path)

            await self.emitter.emit(Event(
                type=EventType.FILE_CREATED,
                session_id=session_id,
                data={
                    'session_id': session_id,
                    'path': str(file_path),
                    'size': current_files[session_id],
                    'message_count': info.message_count if info else 0,
                    'first_message': info.first_message if info else None
                }
            ))

        # Modified files (size changed)
        existing = previous_ids & current_ids
        for session_id in existing:
            old_size = self._file_states[session_id]
            new_size = current_files[session_id]

            if old_size != new_size:
                file_path = project_dir / f"session_{session_id}.jsonl"
                info = self._parse_session_file(file_path)

                await self.emitter.emit(Event(
                    type=EventType.FILE_MODIFIED,
                    session_id=session_id,
                    data={
                        'session_id': session_id,
                        'path': str(file_path),
                        'size': new_size,
                        'old_size': old_size,
                        'message_count': info.message_count if info else 0,
                        'first_message': info.first_message if info else None
                    }
                ))

        # Deleted files
        deleted = previous_ids - current_ids
        for session_id in deleted:
            await self.emitter.emit(Event(
                type=EventType.FILE_DELETED,
                session_id=session_id,
                data={
                    'session_id': session_id,
                }
            ))

        # Update state
        self._file_states = current_files
