"""
Session manager for Claude Agent Manager.

Manages the lifecycle of Claude agent sessions, including creation, message handling,
state management, and integration with the process manager for executing prompts.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional

from claude_agent_manager.core.events import Event, EventEmitter, EventType
from claude_agent_manager.core.process import ProcessConfig, ProcessManager, ProcessResult
from claude_agent_manager.session.storage import SessionStorage
from claude_agent_manager.session.types.session import Message, Session, SessionState


class SessionManager:
    """
    Manager for Claude agent sessions.

    Handles session lifecycle, message tracking, state management, and integration
    with the ProcessManager for executing prompts. Automatically tracks usage
    statistics and message history.

    Features:
        - Session creation with custom metadata
        - Auto-resume using Claude session IDs
        - State management (IDLE/BUSY/ERROR/CLOSED)
        - Message history tracking
        - Usage aggregation (tokens and cost)
        - Event-driven architecture
        - Persistent storage integration

    Attributes:
        process_manager: ProcessManager for executing prompts
        emitter: EventEmitter for lifecycle events
        storage: SessionStorage for persistence

    Examples:
        >>> # Create manager
        >>> manager = SessionManager()
        >>>
        >>> # Create a new session
        >>> session = manager.create_session(
        ...     cwd='/tmp/project',
        ...     metadata={'purpose': 'code review'}
        ... )
        >>>
        >>> # Send a message
        >>> result = await manager.send_message(
        ...     session.id,
        ...     'Explain this code',
        ...     model='claude-opus-4-5-20251101'
        ... )
        >>>
        >>> # Get session
        >>> session = manager.get_session(session.id)
        >>> print(f"Cost: ${session.total_cost_usd:.4f}")
        >>> print(f"Messages: {len(session.messages)}")
        >>>
        >>> # Close session
        >>> manager.close_session(session.id)
    """

    def __init__(
        self,
        process_manager: Optional[ProcessManager] = None,
        emitter: Optional[EventEmitter] = None,
        storage: Optional[SessionStorage] = None
    ):
        """
        Initialize the session manager.

        Args:
            process_manager: ProcessManager for executing prompts (creates new if None)
            emitter: EventEmitter for lifecycle events (creates new if None)
            storage: SessionStorage for persistence (creates new if None)

        Examples:
            >>> # Use defaults
            >>> manager = SessionManager()
            >>>
            >>> # With custom components
            >>> emitter = EventEmitter()
            >>> process_manager = ProcessManager(emitter=emitter)
            >>> manager = SessionManager(
            ...     process_manager=process_manager,
            ...     emitter=emitter
            ... )
        """
        self.emitter = emitter or EventEmitter()
        self.process_manager = process_manager or ProcessManager(emitter=self.emitter)
        self.storage = storage or SessionStorage()
        self._sessions: Dict[str, Session] = {}

        # Set up event handlers
        self._setup_event_handlers()

    def _setup_event_handlers(self) -> None:
        """
        Register event handlers for session lifecycle events.

        Handles:
            - SESSION_STARTED: Update session with Claude session ID
            - MESSAGE_RECEIVED: Add assistant message to history
            - USAGE_UPDATE: Aggregate token usage and cost
            - SESSION_COMPLETE: Update state to IDLE
            - SESSION_ERROR: Update state to ERROR
        """
        @self.emitter.on(EventType.SESSION_STARTED)
        async def on_session_started(event: Event):
            """Update session with Claude session ID."""
            session = self._sessions.get(event.session_id)
            if session:
                session.claude_session_id = event.data.get('claude_session_id')
                session.updated_at = datetime.utcnow()

        @self.emitter.on(EventType.MESSAGE_RECEIVED)
        async def on_message_received(event: Event):
            """Add assistant message to history."""
            session = self._sessions.get(event.session_id)
            if session:
                message = Message(
                    role='assistant',
                    content=event.data.get('content', '')
                )
                session.messages.append(message)
                session.updated_at = datetime.utcnow()

        @self.emitter.on(EventType.USAGE_UPDATE)
        async def on_usage_update(event: Event):
            """Update session usage statistics."""
            session = self._sessions.get(event.session_id)
            if session:
                usage_data = event.data
                session.total_input_tokens += usage_data.get('input_tokens', 0)
                session.total_output_tokens += usage_data.get('output_tokens', 0)
                session.total_cost_usd = usage_data.get('total_cost_usd', session.total_cost_usd)
                session.updated_at = datetime.utcnow()

        @self.emitter.on(EventType.SESSION_COMPLETE)
        async def on_session_complete(event: Event):
            """Mark session as idle after completion."""
            session = self._sessions.get(event.session_id)
            if session:
                session.state = SessionState.IDLE
                session.updated_at = datetime.utcnow()

        @self.emitter.on(EventType.SESSION_ERROR)
        async def on_session_error(event: Event):
            """Mark session as error state."""
            session = self._sessions.get(event.session_id)
            if session:
                session.state = SessionState.ERROR
                session.updated_at = datetime.utcnow()

    def create_session(
        self,
        cwd: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Session:
        """
        Create a new session.

        Args:
            cwd: Working directory for the session
            session_id: Optional custom session ID (generates UUID if None)
            metadata: Optional custom metadata dictionary

        Returns:
            Created Session object

        Examples:
            >>> manager = SessionManager()
            >>>
            >>> # Basic session
            >>> session = manager.create_session('/tmp/project')
            >>>
            >>> # With custom ID and metadata
            >>> session = manager.create_session(
            ...     cwd='/tmp/project',
            ...     session_id='my_session',
            ...     metadata={'purpose': 'code review', 'reviewer': 'alice'}
            ... )
        """
        if session_id is None:
            session_id = f"session_{uuid.uuid4().hex[:8]}"

        session = Session(
            id=session_id,
            cwd=cwd,
            state=SessionState.IDLE,
            metadata=metadata or {}
        )

        self._sessions[session_id] = session

        # Persist to storage
        self.storage.save(session)

        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get a session by ID.

        First checks in-memory cache, then attempts to load from storage.

        Args:
            session_id: The session ID to retrieve

        Returns:
            Session object if found, None otherwise

        Examples:
            >>> manager = SessionManager()
            >>> session = manager.get_session('session_123')
            >>> if session:
            ...     print(f"Session in {session.cwd}")
            ... else:
            ...     print("Session not found")
        """
        # Check in-memory cache
        if session_id in self._sessions:
            return self._sessions[session_id]

        # Try to load from storage
        session = self.storage.load(session_id)
        if session:
            self._sessions[session_id] = session

        return session

    def list_sessions(self, state: Optional[SessionState] = None) -> List[Session]:
        """
        List all sessions, optionally filtered by state.

        Args:
            state: Optional state filter (returns all sessions if None)

        Returns:
            List of Session objects

        Examples:
            >>> manager = SessionManager()
            >>>
            >>> # Get all sessions
            >>> all_sessions = manager.list_sessions()
            >>>
            >>> # Get only idle sessions
            >>> idle_sessions = manager.list_sessions(state=SessionState.IDLE)
            >>>
            >>> # Get only busy sessions
            >>> busy_sessions = manager.list_sessions(state=SessionState.BUSY)
        """
        # Load all sessions from storage
        session_ids = self.storage.list()
        for sid in session_ids:
            if sid not in self._sessions:
                session = self.storage.load(sid)
                if session:
                    self._sessions[sid] = session

        # Filter by state if specified
        sessions = list(self._sessions.values())
        if state is not None:
            sessions = [s for s in sessions if s.state == state]

        return sessions

    async def send_message(
        self,
        session_id: str,
        prompt: str,
        **kwargs
    ) -> ProcessResult:
        """
        Send a message to a session and execute it.

        Automatically resumes the session using the Claude session ID if available.
        Updates session state to BUSY during execution, then back to IDLE on completion.

        Args:
            session_id: The session ID to send the message to
            prompt: The user prompt to send
            **kwargs: Additional ProcessConfig parameters (model, max_turns, etc.)

        Returns:
            ProcessResult with execution outcome

        Raises:
            ValueError: If session not found or in invalid state

        Examples:
            >>> manager = SessionManager()
            >>> session = manager.create_session('/tmp/project')
            >>>
            >>> # Send a message
            >>> result = await manager.send_message(
            ...     session.id,
            ...     'Explain this code',
            ...     model='claude-opus-4-5-20251101'
            ... )
            >>>
            >>> print(result.text)
            >>> print(f"Cost: ${result.usage.total_cost_usd:.4f}")
        """
        # Get session
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")

        if session.state == SessionState.CLOSED:
            raise ValueError(f"Session is closed: {session_id}")

        # Add user message to history
        user_message = Message(role='user', content=prompt)
        session.messages.append(user_message)

        # Update state to BUSY
        session.state = SessionState.BUSY
        session.updated_at = datetime.utcnow()

        # Build process config
        config = ProcessConfig(
            prompt=prompt,
            cwd=session.cwd,
            session_id=session_id,
            resume_session_id=session.claude_session_id,
            **kwargs
        )

        # Execute
        result = await self.process_manager.execute(config)

        # Update session with Claude session ID if not set
        if result.claude_session_id and not session.claude_session_id:
            session.claude_session_id = result.claude_session_id

        # Update usage statistics
        session.total_input_tokens += result.usage.input_tokens
        session.total_output_tokens += result.usage.output_tokens
        session.total_cost_usd += result.usage.total_cost_usd

        # Add assistant message to history
        assistant_message = Message(role='assistant', content=result.text)
        session.messages.append(assistant_message)

        # Update state based on result
        if result.error:
            session.state = SessionState.ERROR
        else:
            session.state = SessionState.IDLE

        session.updated_at = datetime.utcnow()

        # Persist updated session
        self.storage.save(session)

        return result

    def close_session(self, session_id: str) -> bool:
        """
        Close a session.

        Marks the session as CLOSED and persists the final state.

        Args:
            session_id: The session ID to close

        Returns:
            True if session was closed, False if not found

        Examples:
            >>> manager = SessionManager()
            >>> manager.close_session('session_123')
            True
        """
        session = self.get_session(session_id)
        if not session:
            return False

        session.state = SessionState.CLOSED
        session.updated_at = datetime.utcnow()

        # Persist final state
        self.storage.save(session)

        return True

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session completely.

        Removes the session from both memory and storage.

        Args:
            session_id: The session ID to delete

        Returns:
            True if session was deleted, False if not found

        Examples:
            >>> manager = SessionManager()
            >>> manager.delete_session('session_123')
            True
        """
        # Remove from memory
        self._sessions.pop(session_id, None)

        # Remove from storage
        return self.storage.delete(session_id)
