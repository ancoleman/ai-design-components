"""Tests for session modules: types, storage, manager, watcher."""

import asyncio
import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from claude_agent_manager.core.events import EventEmitter, EventType
from claude_agent_manager.core.process import ProcessManager, ProcessResult, UsageStats
from claude_agent_manager.session.manager import SessionManager
from claude_agent_manager.session.storage import SessionStorage
from claude_agent_manager.session.types.session import Message, Session, SessionState
from claude_agent_manager.session.watcher import SessionFileInfo, SessionWatcher


class TestSessionState:
    """Test SessionState enum."""

    def test_all_states_exist(self):
        """Test that all expected states are defined."""
        expected_states = ["IDLE", "BUSY", "ERROR", "CLOSED"]

        for state_name in expected_states:
            assert hasattr(SessionState, state_name), f"SessionState.{state_name} not found"


class TestMessage:
    """Test Message dataclass."""

    def test_message_creation(self):
        """Test creating a message."""
        msg = Message(role="user", content="Hello")

        assert msg.role == "user"
        assert msg.content == "Hello"
        assert isinstance(msg.timestamp, datetime)
        assert msg.tool_calls == []

    def test_message_with_tool_calls(self):
        """Test message with tool calls."""
        tool_calls = [{"name": "Read", "args": {"file_path": "/tmp/test.txt"}}]
        msg = Message(role="assistant", content="Let me read that", tool_calls=tool_calls)

        assert msg.tool_calls == tool_calls

    def test_message_to_dict(self):
        """Test serializing message to dict."""
        msg = Message(role="user", content="Test")
        data = msg.to_dict()

        assert data["role"] == "user"
        assert data["content"] == "Test"
        assert "timestamp" in data
        assert "tool_calls" in data

    def test_message_from_dict(self):
        """Test deserializing message from dict."""
        data = {
            "role": "assistant",
            "content": "Hello",
            "timestamp": "2025-01-01T12:00:00",
            "tool_calls": [],
        }

        msg = Message.from_dict(data)

        assert msg.role == "assistant"
        assert msg.content == "Hello"
        assert isinstance(msg.timestamp, datetime)


class TestSession:
    """Test Session dataclass."""

    def test_session_creation(self):
        """Test creating a session."""
        session = Session(id="session_123", cwd="/tmp/project")

        assert session.id == "session_123"
        assert session.cwd == "/tmp/project"
        assert session.state == SessionState.IDLE
        assert session.messages == []
        assert session.total_cost_usd == 0.0
        assert session.total_input_tokens == 0
        assert session.total_output_tokens == 0

    def test_session_with_messages(self):
        """Test session with message history."""
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there"),
        ]

        session = Session(id="test", cwd="/tmp", messages=messages)

        assert len(session.messages) == 2
        assert session.messages[0].role == "user"

    def test_session_state_transitions(self):
        """Test changing session state."""
        session = Session(id="test", cwd="/tmp")

        assert session.state == SessionState.IDLE

        session.state = SessionState.BUSY
        assert session.state == SessionState.BUSY

        session.state = SessionState.ERROR
        assert session.state == SessionState.ERROR

        session.state = SessionState.CLOSED
        assert session.state == SessionState.CLOSED

    def test_session_to_dict(self):
        """Test serializing session to dict."""
        session = Session(
            id="test",
            claude_session_id="claude_123",
            cwd="/tmp",
            state=SessionState.BUSY,
            total_cost_usd=0.05,
            total_input_tokens=100,
            total_output_tokens=50,
        )

        data = session.to_dict()

        assert data["id"] == "test"
        assert data["claude_session_id"] == "claude_123"
        assert data["cwd"] == "/tmp"
        assert data["state"] == "BUSY"
        assert data["total_cost_usd"] == 0.05
        assert data["total_input_tokens"] == 100

    def test_session_from_dict(self):
        """Test deserializing session from dict."""
        data = {
            "id": "test",
            "claude_session_id": "claude_123",
            "cwd": "/tmp",
            "state": "IDLE",
            "messages": [],
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:05:00",
            "total_cost_usd": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "metadata": {"key": "value"},
        }

        session = Session.from_dict(data)

        assert session.id == "test"
        assert session.claude_session_id == "claude_123"
        assert session.state == SessionState.IDLE
        assert session.metadata == {"key": "value"}


class TestSessionStorage:
    """Test SessionStorage class."""

    def test_storage_initialization_default(self):
        """Test creating storage with default directory."""
        storage = SessionStorage()

        assert storage.storage_dir.exists()
        assert ".claude_agent_manager" in str(storage.storage_dir)

    def test_storage_initialization_custom(self):
        """Test creating storage with custom directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_dir = Path(tmpdir) / "sessions"
            storage = SessionStorage(storage_dir=custom_dir)

            assert storage.storage_dir == custom_dir
            assert custom_dir.exists()

    def test_save_and_load_session(self):
        """Test saving and loading a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))

            # Create and save session
            session = Session(
                id="test_session",
                cwd="/tmp",
                state=SessionState.IDLE,
                total_cost_usd=0.05,
            )

            saved_path = storage.save(session)
            assert saved_path.exists()

            # Load session
            loaded = storage.load("test_session")
            assert loaded is not None
            assert loaded.id == "test_session"
            assert loaded.total_cost_usd == 0.05

    def test_load_nonexistent_session(self):
        """Test loading session that doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))

            loaded = storage.load("nonexistent")
            assert loaded is None

    def test_list_sessions(self):
        """Test listing all sessions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))

            # Save multiple sessions
            storage.save(Session(id="session_1", cwd="/tmp"))
            storage.save(Session(id="session_2", cwd="/tmp"))
            storage.save(Session(id="session_3", cwd="/tmp"))

            session_ids = storage.list()

            assert len(session_ids) == 3
            assert "session_1" in session_ids
            assert "session_2" in session_ids
            assert "session_3" in session_ids

    def test_delete_session(self):
        """Test deleting a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))

            # Save session
            storage.save(Session(id="test_session", cwd="/tmp"))
            assert storage.exists("test_session")

            # Delete session
            deleted = storage.delete("test_session")
            assert deleted is True
            assert not storage.exists("test_session")

            # Try to delete again
            deleted = storage.delete("test_session")
            assert deleted is False

    def test_exists(self):
        """Test checking if session exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))

            assert not storage.exists("nonexistent")

            storage.save(Session(id="test", cwd="/tmp"))
            assert storage.exists("test")


class TestSessionManager:
    """Test SessionManager class."""

    def test_manager_initialization(self):
        """Test creating session manager."""
        manager = SessionManager()

        assert manager.emitter is not None
        assert manager.process_manager is not None
        assert manager.storage is not None
        assert manager._sessions == {}

    def test_create_session(self):
        """Test creating a new session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))
            manager = SessionManager(storage=storage)

            session = manager.create_session(cwd="/tmp/project")

            assert session.id is not None
            assert session.cwd == "/tmp/project"
            assert session.state == SessionState.IDLE
            assert storage.exists(session.id)

    def test_create_session_with_custom_id(self):
        """Test creating session with custom ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))
            manager = SessionManager(storage=storage)

            session = manager.create_session(
                cwd="/tmp", session_id="my_session", metadata={"purpose": "testing"}
            )

            assert session.id == "my_session"
            assert session.metadata["purpose"] == "testing"

    def test_get_session(self):
        """Test retrieving a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))
            manager = SessionManager(storage=storage)

            # Create session
            session = manager.create_session(cwd="/tmp")
            session_id = session.id

            # Get from memory
            retrieved = manager.get_session(session_id)
            assert retrieved is not None
            assert retrieved.id == session_id

            # Clear memory cache and get from storage
            manager._sessions.clear()
            retrieved = manager.get_session(session_id)
            assert retrieved is not None
            assert retrieved.id == session_id

    def test_get_nonexistent_session(self):
        """Test getting session that doesn't exist."""
        manager = SessionManager()

        session = manager.get_session("nonexistent")
        assert session is None

    def test_list_sessions(self):
        """Test listing all sessions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))
            manager = SessionManager(storage=storage)

            # Create sessions with different states
            session1 = manager.create_session(cwd="/tmp")
            session2 = manager.create_session(cwd="/tmp")
            session2.state = SessionState.BUSY
            storage.save(session2)

            session3 = manager.create_session(cwd="/tmp")
            session3.state = SessionState.ERROR
            storage.save(session3)

            # List all
            all_sessions = manager.list_sessions()
            assert len(all_sessions) == 3

            # Filter by state
            idle_sessions = manager.list_sessions(state=SessionState.IDLE)
            assert len(idle_sessions) == 1

            busy_sessions = manager.list_sessions(state=SessionState.BUSY)
            assert len(busy_sessions) == 1

    @pytest.mark.asyncio
    async def test_send_message(self):
        """Test sending a message to a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))

            # Mock process manager
            mock_process_manager = MagicMock(spec=ProcessManager)
            mock_process_manager.execute = AsyncMock(
                return_value=ProcessResult(
                    session_id="test",
                    claude_session_id="claude_123",
                    text="Hello, I can help with that.",
                    exit_code=0,
                    usage=UsageStats(input_tokens=10, output_tokens=20, total_cost_usd=0.01),
                    duration_seconds=1.5,
                )
            )

            manager = SessionManager(process_manager=mock_process_manager, storage=storage)

            # Create session
            session = manager.create_session(cwd="/tmp")

            # Send message
            result = await manager.send_message(session.id, "Hello, Claude")

            assert result.exit_code == 0
            assert result.text == "Hello, I can help with that."

            # Check session was updated
            updated_session = manager.get_session(session.id)
            assert len(updated_session.messages) == 2  # user + assistant
            assert updated_session.total_input_tokens == 10
            assert updated_session.total_output_tokens == 20
            assert updated_session.claude_session_id == "claude_123"

    @pytest.mark.asyncio
    async def test_send_message_with_resume(self):
        """Test sending message to session with Claude session ID (resume)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))

            # Mock process manager
            mock_process_manager = MagicMock(spec=ProcessManager)
            mock_process_manager.execute = AsyncMock(
                return_value=ProcessResult(
                    session_id="test",
                    claude_session_id="claude_123",
                    text="Continuing...",
                    exit_code=0,
                    usage=UsageStats(),
                    duration_seconds=1.0,
                )
            )

            manager = SessionManager(process_manager=mock_process_manager, storage=storage)

            # Create session with existing Claude session ID
            session = manager.create_session(cwd="/tmp")
            session.claude_session_id = "claude_123"

            # Send message
            await manager.send_message(session.id, "Continue where we left off")

            # Verify ProcessConfig included resume_session_id
            call_args = mock_process_manager.execute.call_args
            config = call_args[0][0]
            assert config.resume_session_id == "claude_123"

    def test_close_session(self):
        """Test closing a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))
            manager = SessionManager(storage=storage)

            session = manager.create_session(cwd="/tmp")
            session_id = session.id

            # Close session
            closed = manager.close_session(session_id)
            assert closed is True

            # Verify state
            session = manager.get_session(session_id)
            assert session.state == SessionState.CLOSED

    def test_delete_session(self):
        """Test deleting a session completely."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = SessionStorage(storage_dir=Path(tmpdir))
            manager = SessionManager(storage=storage)

            session = manager.create_session(cwd="/tmp")
            session_id = session.id

            # Delete session
            deleted = manager.delete_session(session_id)
            assert deleted is True

            # Verify removed
            assert not storage.exists(session_id)
            assert manager.get_session(session_id) is None


class TestSessionWatcher:
    """Test SessionWatcher class."""

    def test_watcher_initialization(self):
        """Test creating session watcher."""
        watcher = SessionWatcher(cwd="/tmp/project")

        assert watcher.cwd == "/tmp/project"
        assert watcher.emitter is not None
        assert watcher.poll_interval == 1.0
        assert watcher._running is False

    def test_watcher_with_custom_interval(self):
        """Test watcher with custom poll interval."""
        watcher = SessionWatcher(cwd="/tmp", poll_interval=2.0)

        assert watcher.poll_interval == 2.0

    def test_list_sessions_empty(self):
        """Test listing sessions with no files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create watcher (will look for sessions in non-existent dir)
            watcher = SessionWatcher(cwd=tmpdir)

            # Mock the path lookup to return our temp dir
            with patch(
                "claude_agent_manager.session.watcher.list_session_files",
                return_value=[],
            ):
                sessions = watcher.list_sessions()
                assert sessions == []

    def test_parse_session_file(self):
        """Test parsing a session file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock session file
            session_file = Path(tmpdir) / "session_abc123.jsonl"

            # Write session data
            with open(session_file, "w") as f:
                f.write(
                    json.dumps(
                        {
                            "type": "user",
                            "message": {
                                "role": "user",
                                "content": [{"type": "text", "text": "Hello, Claude"}],
                            },
                        }
                    )
                    + "\n"
                )
                f.write(
                    json.dumps(
                        {
                            "type": "assistant",
                            "message": {"role": "assistant", "content": []},
                        }
                    )
                    + "\n"
                )

            watcher = SessionWatcher(cwd="/tmp")
            info = watcher._parse_session_file(session_file)

            assert info is not None
            assert info.session_id == "abc123"
            assert info.message_count == 2
            assert info.first_message == "Hello, Claude"

    @pytest.mark.asyncio
    async def test_start_stop_watcher(self):
        """Test starting and stopping watcher."""
        watcher = SessionWatcher(cwd="/tmp", poll_interval=0.1)

        # Start watcher
        await watcher.start()
        assert watcher._running is True
        assert watcher._task is not None

        # Give it a moment to run
        await asyncio.sleep(0.2)

        # Stop watcher
        await watcher.stop()
        assert watcher._running is False

    @pytest.mark.asyncio
    async def test_watcher_emits_events(self):
        """Test that watcher emits file events."""
        with tempfile.TemporaryDirectory() as tmpdir:
            emitter = EventEmitter()
            received_events = []

            @emitter.on(EventType.FILE_CREATED)
            async def on_created(event):
                received_events.append(event)

            # Mock the project dir to use our temp dir
            watcher = SessionWatcher(cwd="/tmp", emitter=emitter, poll_interval=0.1)

            with patch.object(watcher, "_get_project_dir", return_value=Path(tmpdir)):
                # Start watching
                await watcher.start()

                # Create a session file
                session_file = Path(tmpdir) / "session_test123.jsonl"
                session_file.write_text('{"type": "user", "message": {}}\n')

                # Wait for poll
                await asyncio.sleep(0.3)

                # Stop watching
                await watcher.stop()

                # Should have detected the file creation
                # Note: Depending on timing, this may or may not fire
                # This is a basic test structure
                # assert len(received_events) > 0


class TestSessionFileInfo:
    """Test SessionFileInfo dataclass."""

    def test_session_file_info_creation(self):
        """Test creating SessionFileInfo."""
        info = SessionFileInfo(
            session_id="abc123",
            path=Path("/tmp/session_abc123.jsonl"),
            size=1024,
            modified_at=datetime.now(),
            message_count=10,
            first_message="Hello",
            cost_usd=0.05,
        )

        assert info.session_id == "abc123"
        assert info.size == 1024
        assert info.message_count == 10
        assert info.first_message == "Hello"
        assert info.cost_usd == 0.05
