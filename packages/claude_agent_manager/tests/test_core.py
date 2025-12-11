"""Tests for core modules: events, detector, parser, process."""

import asyncio
import json
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from claude_agent_manager.core.detector import AgentDetector, DetectionResult
from claude_agent_manager.core.events import (
    Event,
    EventEmitter,
    EventType,
    create_file_event,
    create_message_chunk_event,
    create_tool_event,
    create_usage_event,
)
from claude_agent_manager.core.parser import ParsedMessage, StreamJsonParser, UsageStats
from claude_agent_manager.core.process import ProcessConfig, ProcessManager, ProcessResult


class TestEventType:
    """Test EventType enum."""

    def test_all_event_types_exist(self):
        """Test that all expected event types are defined."""
        expected_types = [
            "SESSION_STARTED",
            "SESSION_RESUMED",
            "SESSION_COMPLETE",
            "SESSION_ERROR",
            "MESSAGE_RECEIVED",
            "MESSAGE_CHUNK",
            "TOOL_CALLED",
            "TOOL_RESULT",
            "FILE_CREATED",
            "FILE_MODIFIED",
            "FILE_DELETED",
            "PROGRESS_UPDATE",
            "PROCESS_SPAWNED",
            "PROCESS_EXIT",
            "USAGE_UPDATE",
        ]

        for event_name in expected_types:
            assert hasattr(EventType, event_name), f"EventType.{event_name} not found"


class TestEvent:
    """Test Event data class."""

    def test_event_creation(self):
        """Test creating an event."""
        event = Event(
            type=EventType.MESSAGE_RECEIVED,
            session_id="test_session",
            data={"content": "Hello"},
        )

        assert event.type == EventType.MESSAGE_RECEIVED
        assert event.session_id == "test_session"
        assert event.data == {"content": "Hello"}
        assert isinstance(event.timestamp, datetime)

    def test_event_immutability(self):
        """Test that events are immutable (frozen dataclass)."""
        event = Event(
            type=EventType.SESSION_STARTED,
            session_id="test",
            data={"key": "value"},
        )

        with pytest.raises(Exception):  # FrozenInstanceError
            event.session_id = "modified"

    def test_event_default_data(self):
        """Test event with default empty data."""
        event = Event(type=EventType.SESSION_STARTED, session_id="test")

        assert event.data == {}

    def test_event_str_representation(self):
        """Test event string representation."""
        event = Event(
            type=EventType.TOOL_CALLED, session_id="test", data={"tool": "Read"}
        )

        str_repr = str(event)
        assert "TOOL_CALLED" in str_repr
        assert "test" in str_repr


class TestEventEmitter:
    """Test EventEmitter class."""

    def test_emitter_initialization(self):
        """Test creating an event emitter."""
        emitter = EventEmitter()

        assert emitter._listeners == {}
        assert emitter._global_listeners == []

    @pytest.mark.asyncio
    async def test_on_decorator_async(self):
        """Test @emitter.on decorator with async handler."""
        emitter = EventEmitter()
        received_events = []

        @emitter.on(EventType.MESSAGE_CHUNK)
        async def handler(event: Event):
            received_events.append(event)

        event = Event(
            type=EventType.MESSAGE_CHUNK,
            session_id="test",
            data={"chunk": "Hello"},
        )

        await emitter.emit(event)

        assert len(received_events) == 1
        assert received_events[0].data["chunk"] == "Hello"

    @pytest.mark.asyncio
    async def test_on_decorator_sync(self):
        """Test @emitter.on decorator with sync handler."""
        emitter = EventEmitter()
        received_events = []

        @emitter.on(EventType.MESSAGE_CHUNK)
        def handler(event: Event):
            received_events.append(event)

        event = Event(
            type=EventType.MESSAGE_CHUNK, session_id="test", data={"chunk": "Hello"}
        )

        await emitter.emit(event)

        # Give sync handler time to execute in thread pool
        await asyncio.sleep(0.1)

        assert len(received_events) == 1

    @pytest.mark.asyncio
    async def test_add_remove_listener(self):
        """Test adding and removing listeners."""
        emitter = EventEmitter()
        received_events = []

        async def handler(event: Event):
            received_events.append(event)

        # Add listener
        emitter.add_listener(EventType.SESSION_STARTED, handler)
        assert emitter.get_listener_count(EventType.SESSION_STARTED) == 1

        # Emit event
        await emitter.emit(
            Event(type=EventType.SESSION_STARTED, session_id="test")
        )
        assert len(received_events) == 1

        # Remove listener
        removed = emitter.remove_listener(EventType.SESSION_STARTED, handler)
        assert removed is True
        assert emitter.get_listener_count(EventType.SESSION_STARTED) == 0

        # Emit again - should not receive
        await emitter.emit(
            Event(type=EventType.SESSION_STARTED, session_id="test")
        )
        assert len(received_events) == 1  # Still 1, not incremented

    @pytest.mark.asyncio
    async def test_on_all_handler(self):
        """Test global handler that receives all events."""
        emitter = EventEmitter()
        received_events = []

        @emitter.on_all
        async def global_handler(event: Event):
            received_events.append(event)

        # Emit different event types
        await emitter.emit(Event(type=EventType.SESSION_STARTED, session_id="test"))
        await emitter.emit(Event(type=EventType.MESSAGE_CHUNK, session_id="test"))
        await emitter.emit(Event(type=EventType.TOOL_CALLED, session_id="test"))

        assert len(received_events) == 3

    @pytest.mark.asyncio
    async def test_clear_listeners(self):
        """Test clearing listeners."""
        emitter = EventEmitter()

        @emitter.on(EventType.SESSION_STARTED)
        async def handler1(event: Event):
            pass

        @emitter.on(EventType.MESSAGE_CHUNK)
        async def handler2(event: Event):
            pass

        @emitter.on_all
        async def handler3(event: Event):
            pass

        assert emitter.get_listener_count() == 3

        # Clear specific type
        emitter.clear(EventType.SESSION_STARTED)
        assert emitter.get_listener_count(EventType.SESSION_STARTED) == 0
        assert emitter.get_listener_count() == 2

        # Clear all
        emitter.clear()
        assert emitter.get_listener_count() == 0

    @pytest.mark.asyncio
    async def test_emit_no_handlers(self):
        """Test emitting event with no handlers (should not error)."""
        emitter = EventEmitter()

        # Should not raise
        await emitter.emit(Event(type=EventType.SESSION_STARTED, session_id="test"))


class TestEventHelpers:
    """Test event creation helper functions."""

    def test_create_message_chunk_event(self):
        """Test creating message chunk event."""
        event = create_message_chunk_event("session_123", "Hello", 0)

        assert event.type == EventType.MESSAGE_CHUNK
        assert event.session_id == "session_123"
        assert event.data["chunk"] == "Hello"
        assert event.data["index"] == 0

    def test_create_tool_event_called(self):
        """Test creating tool called event."""
        event = create_tool_event(
            "session_123", "Read", is_result=False, args={"file_path": "/tmp/test.txt"}
        )

        assert event.type == EventType.TOOL_CALLED
        assert event.data["tool"] == "Read"
        assert event.data["args"] == {"file_path": "/tmp/test.txt"}

    def test_create_tool_event_result(self):
        """Test creating tool result event."""
        event = create_tool_event(
            "session_123", "Read", is_result=True, result="file contents", duration_ms=150
        )

        assert event.type == EventType.TOOL_RESULT
        assert event.data["tool"] == "Read"
        assert event.data["result"] == "file contents"
        assert event.data["duration_ms"] == 150

    def test_create_file_event(self):
        """Test creating file events."""
        # Created
        event = create_file_event("session_123", "/tmp/test.txt", "created", size=100)
        assert event.type == EventType.FILE_CREATED
        assert event.data["path"] == "/tmp/test.txt"
        assert event.data["size"] == 100

        # Modified (default)
        event = create_file_event("session_123", "/tmp/test.txt")
        assert event.type == EventType.FILE_MODIFIED

        # Deleted
        event = create_file_event("session_123", "/tmp/test.txt", "deleted")
        assert event.type == EventType.FILE_DELETED

    def test_create_usage_event(self):
        """Test creating usage event."""
        event = create_usage_event(
            "session_123", input_tokens=1500, output_tokens=500, cost_usd=0.025
        )

        assert event.type == EventType.USAGE_UPDATE
        assert event.data["input_tokens"] == 1500
        assert event.data["output_tokens"] == 500
        assert event.data["cost_usd"] == 0.025


class TestAgentDetector:
    """Test AgentDetector class."""

    def test_detector_initialization(self):
        """Test creating detector."""
        detector = AgentDetector()
        assert detector.binary_name == "claude"

        detector = AgentDetector("custom-claude")
        assert detector.binary_name == "custom-claude"

    def test_get_expanded_path(self):
        """Test path expansion."""
        detector = AgentDetector()
        expanded_path = detector.get_expanded_path()

        assert expanded_path is not None
        assert isinstance(expanded_path, str)
        # Should contain current PATH
        assert len(expanded_path) > 0

    def test_get_env_with_expanded_path(self):
        """Test getting environment with expanded PATH."""
        detector = AgentDetector()
        env = detector.get_env_with_expanded_path()

        assert "PATH" in env
        assert isinstance(env, dict)

    @pytest.mark.asyncio
    async def test_detect_cached(self):
        """Test detection caching."""
        detector = AgentDetector()

        # First detection (will actually search)
        result1 = await detector.detect()

        # Second detection should return cached result
        result2 = await detector.detect()

        assert result1 is result2  # Same object (cached)


class TestDetectionResult:
    """Test DetectionResult dataclass."""

    def test_detection_result_available(self):
        """Test successful detection result."""
        result = DetectionResult(
            available=True, path="/usr/local/bin/claude", version="1.0.0"
        )

        assert result.available is True
        assert result.path == "/usr/local/bin/claude"
        assert result.version == "1.0.0"
        assert result.error is None

    def test_detection_result_unavailable(self):
        """Test failed detection result."""
        result = DetectionResult(available=False, error="Binary not found")

        assert result.available is False
        assert result.path is None
        assert result.error == "Binary not found"


class TestUsageStats:
    """Test UsageStats dataclass."""

    def test_usage_stats_defaults(self):
        """Test default values."""
        stats = UsageStats()

        assert stats.input_tokens == 0
        assert stats.output_tokens == 0
        assert stats.cache_read_tokens == 0
        assert stats.cache_creation_tokens == 0
        assert stats.total_cost_usd == 0.0
        assert stats.context_window == 200000

    def test_usage_stats_to_dict(self):
        """Test converting to dictionary."""
        stats = UsageStats(input_tokens=100, output_tokens=50, total_cost_usd=0.01)

        data = stats.to_dict()

        assert data["input_tokens"] == 100
        assert data["output_tokens"] == 50
        assert data["total_cost_usd"] == 0.01


class TestParsedMessage:
    """Test ParsedMessage dataclass."""

    def test_parsed_message_creation(self):
        """Test creating parsed message."""
        msg = ParsedMessage(
            type="assistant",
            subtype="text",
            session_id="abc123",
            result="Hello",
            raw={"key": "value"},
        )

        assert msg.type == "assistant"
        assert msg.subtype == "text"
        assert msg.session_id == "abc123"
        assert msg.result == "Hello"
        assert msg.raw == {"key": "value"}

    def test_parsed_message_defaults(self):
        """Test default values."""
        msg = ParsedMessage(type="system:init")

        assert msg.subtype is None
        assert msg.session_id is None
        assert msg.slash_commands == []
        assert msg.tool_use is None


class TestStreamJsonParser:
    """Test StreamJsonParser class."""

    def test_parser_initialization(self):
        """Test creating parser."""
        parser = StreamJsonParser(session_id="test")

        assert parser._session_id == "test"
        assert parser.claude_session_id is None
        assert parser.usage.input_tokens == 0

    @pytest.mark.asyncio
    async def test_process_line_system_init(self):
        """Test parsing system:init message."""
        emitter = EventEmitter()
        parser = StreamJsonParser(session_id="test", emitter=emitter)

        line = json.dumps(
            {
                "type": "system:init",
                "session_id": "claude_abc123",
                "slash_commands": ["/help", "/clear"],
            }
        )

        parsed = await parser.process_line(line)

        assert parsed is not None
        assert parsed.type == "system:init"
        assert parsed.session_id == "claude_abc123"
        assert parser.claude_session_id == "claude_abc123"
        assert parsed.slash_commands == ["/help", "/clear"]

    @pytest.mark.asyncio
    async def test_process_line_assistant_tool_use(self):
        """Test parsing assistant message with tool use."""
        parser = StreamJsonParser(session_id="test")

        line = json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "tool_123",
                            "name": "Read",
                            "input": {"file_path": "/tmp/test.txt"},
                        }
                    ]
                },
            }
        )

        parsed = await parser.process_line(line)

        assert parsed.type == "assistant"
        assert parsed.tool_use is not None
        assert parsed.tool_use["name"] == "Read"
        assert parsed.tool_use["input"]["file_path"] == "/tmp/test.txt"

    @pytest.mark.asyncio
    async def test_process_line_result(self):
        """Test parsing result message."""
        parser = StreamJsonParser(session_id="test")

        line = json.dumps({"type": "result", "result": "Task completed successfully"})

        parsed = await parser.process_line(line)

        assert parsed.type == "result"
        assert parsed.result == "Task completed successfully"

    @pytest.mark.asyncio
    async def test_process_line_with_usage(self):
        """Test parsing message with usage data."""
        parser = StreamJsonParser(session_id="test")

        line = json.dumps(
            {
                "type": "assistant",
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 50,
                    "cache_read_tokens": 500,
                },
            }
        )

        parsed = await parser.process_line(line)

        assert parser.usage.input_tokens == 100
        assert parser.usage.output_tokens == 50
        assert parser.usage.cache_read_tokens == 500
        assert parsed.usage is not None

    @pytest.mark.asyncio
    async def test_process_chunk_multi_line(self):
        """Test processing multi-line chunk."""
        parser = StreamJsonParser(session_id="test")

        chunk = (
            '{"type": "system:init", "session_id": "abc"}\n'
            '{"type": "assistant", "message": {}}\n'
            '{"type": "result", "result": "Done"}'
        )

        messages = await parser.process_chunk(chunk)

        # Last line is incomplete (no newline), so only 2 complete messages
        assert len(messages) == 2
        assert messages[0].type == "system:init"
        assert messages[1].type == "assistant"

        # Flush to get the last message
        final = await parser.flush()
        assert final.type == "result"

    @pytest.mark.asyncio
    async def test_process_line_invalid_json(self):
        """Test processing invalid JSON (should return None)."""
        parser = StreamJsonParser(session_id="test")

        parsed = await parser.process_line("invalid json {")

        assert parsed is None


class TestProcessConfig:
    """Test ProcessConfig dataclass."""

    def test_process_config_defaults(self):
        """Test default values."""
        config = ProcessConfig(prompt="Test prompt")

        assert config.prompt == "Test prompt"
        assert config.cwd == "."
        assert config.session_id is None
        assert config.skip_permissions is True
        assert config.read_only is False
        assert config.timeout == 120.0

    def test_process_config_with_values(self):
        """Test with custom values."""
        config = ProcessConfig(
            prompt="Test",
            cwd="/tmp",
            model="claude-opus-4-5-20251101",
            max_turns=5,
            skip_permissions=False,
        )

        assert config.cwd == "/tmp"
        assert config.model == "claude-opus-4-5-20251101"
        assert config.max_turns == 5
        assert config.skip_permissions is False


class TestProcessResult:
    """Test ProcessResult dataclass."""

    def test_process_result_creation(self):
        """Test creating process result."""
        usage = UsageStats(input_tokens=100, output_tokens=50)

        result = ProcessResult(
            session_id="test",
            claude_session_id="claude_123",
            text="Hello world",
            exit_code=0,
            usage=usage,
            duration_seconds=1.5,
        )

        assert result.session_id == "test"
        assert result.claude_session_id == "claude_123"
        assert result.text == "Hello world"
        assert result.exit_code == 0
        assert result.usage.input_tokens == 100
        assert result.duration_seconds == 1.5
        assert result.error is None


class TestProcessManager:
    """Test ProcessManager class."""

    def test_manager_initialization(self):
        """Test creating process manager."""
        manager = ProcessManager()

        assert manager.detector is not None
        assert manager.emitter is not None
        assert manager._active_processes == {}

    def test_build_args_basic(self):
        """Test building basic arguments."""
        manager = ProcessManager()
        config = ProcessConfig(prompt="Hello")

        args = manager._build_args(config)

        assert "--print" in args
        assert "--verbose" in args
        assert "--output-format" in args
        assert "stream-json" in args
        assert "--dangerously-skip-permissions" in args
        assert "Hello" in args

    def test_build_args_with_resume(self):
        """Test building args with session resume."""
        manager = ProcessManager()
        config = ProcessConfig(prompt="Hello", resume_session_id="claude_abc123")

        args = manager._build_args(config)

        assert "--resume" in args
        assert "claude_abc123" in args

    def test_build_args_with_model(self):
        """Test building args with model selection."""
        manager = ProcessManager()
        config = ProcessConfig(
            prompt="Hello", model="claude-opus-4-5-20251101"
        )

        args = manager._build_args(config)

        assert "--model" in args
        assert "claude-opus-4-5-20251101" in args

    def test_build_env_removes_api_key(self):
        """Test that environment removes ANTHROPIC_API_KEY."""
        manager = ProcessManager()
        config = ProcessConfig(prompt="Hello")

        # Set API key in environment
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test_key"}):
            env = manager._build_env(config)

            # Should be removed
            assert "ANTHROPIC_API_KEY" not in env

    def test_build_image_message(self):
        """Test building image message."""
        manager = ProcessManager()

        data_url = "data:image/png;base64,iVBORw0KGgoAAAANS"
        message_json = manager._build_image_message("Describe this image", [data_url])

        message = json.loads(message_json)

        assert message["type"] == "user"
        assert message["message"]["role"] == "user"
        assert len(message["message"]["content"]) == 2  # image + text
        assert message["message"]["content"][0]["type"] == "image"
        assert message["message"]["content"][1]["type"] == "text"
