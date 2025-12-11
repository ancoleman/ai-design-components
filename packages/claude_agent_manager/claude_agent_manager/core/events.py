"""
Event System for Claude Agent Manager

This module provides a comprehensive event system for tracking and responding to
agent lifecycle events, tool usage, file operations, and message streaming.

The event system supports:
- Async/await patterns for non-blocking event handling
- Both synchronous and asynchronous event handlers
- Type-safe event types with enum
- Immutable event objects
- Concurrent event handler execution
- Flexible listener registration and removal

Usage:
    >>> emitter = EventEmitter()
    >>>
    >>> @emitter.on(EventType.MESSAGE_RECEIVED)
    >>> async def log_message(event: Event):
    >>>     print(f"Message: {event.data['content']}")
    >>>
    >>> event = Event(
    >>>     type=EventType.MESSAGE_RECEIVED,
    >>>     session_id="session_123",
    >>>     data={"content": "Hello, world!"}
    >>> )
    >>> await emitter.emit(event)
"""

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps


class EventType(Enum):
    """
    Event types for agent lifecycle and operations.

    Session Events:
        SESSION_STARTED: New agent session initiated
        SESSION_RESUMED: Existing session resumed
        SESSION_COMPLETE: Session completed successfully
        SESSION_ERROR: Session encountered an error

    Message Events:
        MESSAGE_RECEIVED: Complete message received
        MESSAGE_CHUNK: Streaming token/chunk received (for real-time updates)

    Tool Events:
        TOOL_CALLED: Tool invocation started
        TOOL_RESULT: Tool execution completed

    File Events:
        FILE_CREATED: New file created by agent
        FILE_MODIFIED: Existing file modified by agent
        FILE_DELETED: File deleted by agent

    Progress Events:
        PROGRESS_UPDATE: Generic progress update (e.g., "50% complete")

    Process Events:
        PROCESS_SPAWNED: Background process started
        PROCESS_EXIT: Process completed or terminated

    Usage Events:
        USAGE_UPDATE: Token usage, API costs, or resource consumption
    """

    # Session events
    SESSION_STARTED = auto()
    SESSION_RESUMED = auto()
    SESSION_COMPLETE = auto()
    SESSION_ERROR = auto()

    # Message events
    MESSAGE_RECEIVED = auto()
    MESSAGE_CHUNK = auto()

    # Tool events
    TOOL_CALLED = auto()
    TOOL_RESULT = auto()

    # File events
    FILE_CREATED = auto()
    FILE_MODIFIED = auto()
    FILE_DELETED = auto()

    # Progress events
    PROGRESS_UPDATE = auto()

    # Process events
    PROCESS_SPAWNED = auto()
    PROCESS_EXIT = auto()

    # Usage events
    USAGE_UPDATE = auto()


@dataclass(frozen=True)
class Event:
    """
    Immutable event object representing a single agent event.

    Attributes:
        type: The type of event (from EventType enum)
        session_id: Unique identifier for the agent session
        timestamp: When the event occurred (auto-generated if not provided)
        data: Additional event-specific data as key-value pairs

    Examples:
        >>> # Message chunk event (streaming)
        >>> Event(
        ...     type=EventType.MESSAGE_CHUNK,
        ...     session_id="session_123",
        ...     data={"chunk": "Hello", "index": 0}
        ... )

        >>> # Tool call event
        >>> Event(
        ...     type=EventType.TOOL_CALLED,
        ...     session_id="session_123",
        ...     data={"tool": "read_file", "args": {"path": "/tmp/file.txt"}}
        ... )

        >>> # File modification event
        >>> Event(
        ...     type=EventType.FILE_MODIFIED,
        ...     session_id="session_123",
        ...     data={"path": "/tmp/file.txt", "size": 1024}
        ... )
    """

    type: EventType
    session_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Human-readable event representation."""
        return (
            f"Event({self.type.name}, "
            f"session={self.session_id}, "
            f"time={self.timestamp.isoformat()}, "
            f"data={self.data})"
        )


# Type aliases for handler functions
AsyncHandler = Callable[[Event], Any]
SyncHandler = Callable[[Event], Any]
Handler = Union[AsyncHandler, SyncHandler]


class EventEmitter:
    """
    Async event emitter for managing and dispatching events.

    The emitter supports both synchronous and asynchronous event handlers,
    automatically wrapping sync handlers to run in a thread pool to avoid
    blocking the event loop.

    Features:
        - Type-safe event registration with decorators
        - Concurrent handler execution via asyncio.gather
        - Automatic sync/async handler detection
        - Per-event-type listeners
        - Global listeners (on_all)
        - Thread-safe handler management

    Examples:
        >>> emitter = EventEmitter()
        >>>
        >>> # Register with decorator
        >>> @emitter.on(EventType.MESSAGE_CHUNK)
        >>> async def handle_chunk(event: Event):
        ...     print(event.data["chunk"], end="", flush=True)
        >>>
        >>> # Register manually
        >>> def sync_handler(event: Event):
        ...     print(f"Sync: {event.type.name}")
        >>>
        >>> emitter.add_listener(EventType.SESSION_STARTED, sync_handler)
        >>>
        >>> # Emit event
        >>> await emitter.emit(Event(
        ...     type=EventType.MESSAGE_CHUNK,
        ...     session_id="session_123",
        ...     data={"chunk": "Hello"}
        ... ))
    """

    def __init__(self):
        """Initialize the event emitter with empty listener maps."""
        self._listeners: Dict[EventType, List[Handler]] = defaultdict(list)
        self._global_listeners: List[Handler] = []
        self._lock = asyncio.Lock()

    def on(self, event_type: EventType) -> Callable[[Handler], Handler]:
        """
        Decorator to register an event handler for a specific event type.

        Args:
            event_type: The type of event to listen for

        Returns:
            Decorator function that registers the handler

        Examples:
            >>> emitter = EventEmitter()
            >>>
            >>> @emitter.on(EventType.TOOL_CALLED)
            >>> async def log_tool_call(event: Event):
            ...     print(f"Tool: {event.data['tool']}")
            >>>
            >>> @emitter.on(EventType.FILE_CREATED)
            >>> def sync_handler(event: Event):
            ...     print(f"File created: {event.data['path']}")
        """
        def decorator(handler: Handler) -> Handler:
            self.add_listener(event_type, handler)
            return handler
        return decorator

    def on_all(self, handler: Handler) -> Handler:
        """
        Register a global handler that receives all events.

        Global handlers are called for every event, regardless of type.
        Useful for logging, monitoring, or debugging.

        Args:
            handler: Function to call for all events

        Returns:
            The handler (for decorator pattern)

        Examples:
            >>> emitter = EventEmitter()
            >>>
            >>> @emitter.on_all
            >>> async def log_all(event: Event):
            ...     print(f"[{event.type.name}] {event.data}")
        """
        self._global_listeners.append(handler)
        return handler

    def add_listener(self, event_type: EventType, handler: Handler) -> None:
        """
        Add an event listener for a specific event type.

        Args:
            event_type: The type of event to listen for
            handler: Function to call when event is emitted (sync or async)

        Examples:
            >>> emitter = EventEmitter()
            >>>
            >>> async def my_handler(event: Event):
            ...     print(event.data)
            >>>
            >>> emitter.add_listener(EventType.MESSAGE_RECEIVED, my_handler)
        """
        self._listeners[event_type].append(handler)

    def remove_listener(self, event_type: EventType, handler: Handler) -> bool:
        """
        Remove a specific event listener.

        Args:
            event_type: The event type to remove the handler from
            handler: The handler function to remove

        Returns:
            True if the handler was found and removed, False otherwise

        Examples:
            >>> emitter = EventEmitter()
            >>> handler = lambda e: print(e)
            >>> emitter.add_listener(EventType.SESSION_STARTED, handler)
            >>> emitter.remove_listener(EventType.SESSION_STARTED, handler)
            True
        """
        if handler in self._listeners[event_type]:
            self._listeners[event_type].remove(handler)
            return True
        return False

    def clear(self, event_type: Optional[EventType] = None) -> None:
        """
        Clear event listeners.

        Args:
            event_type: If provided, clear only listeners for this event type.
                       If None, clear all listeners (including global).

        Examples:
            >>> emitter = EventEmitter()
            >>> # Clear specific event type
            >>> emitter.clear(EventType.MESSAGE_CHUNK)
            >>>
            >>> # Clear everything
            >>> emitter.clear()
        """
        if event_type is not None:
            self._listeners[event_type].clear()
        else:
            self._listeners.clear()
            self._global_listeners.clear()

    async def emit(self, event: Event) -> None:
        """
        Emit an event to all registered handlers.

        Handlers are executed concurrently using asyncio.gather. Synchronous
        handlers are automatically wrapped to run in a thread pool to avoid
        blocking the event loop.

        If any handler raises an exception, it is logged but does not prevent
        other handlers from executing.

        Args:
            event: The event to emit

        Examples:
            >>> emitter = EventEmitter()
            >>>
            >>> await emitter.emit(Event(
            ...     type=EventType.TOOL_CALLED,
            ...     session_id="session_123",
            ...     data={"tool": "read_file", "args": {"path": "/tmp/test.txt"}}
            ... ))
        """
        # Collect all relevant handlers
        handlers: List[Handler] = []

        # Add type-specific handlers
        handlers.extend(self._listeners[event.type])

        # Add global handlers
        handlers.extend(self._global_listeners)

        # No handlers to call
        if not handlers:
            return

        # Create tasks for all handlers
        tasks = []
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                # Async handler - call directly
                tasks.append(self._safe_call_async(handler, event))
            else:
                # Sync handler - run in thread pool
                tasks.append(self._safe_call_sync(handler, event))

        # Execute all handlers concurrently
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_call_async(self, handler: AsyncHandler, event: Event) -> None:
        """
        Safely call an async handler, catching and logging exceptions.

        Args:
            handler: The async handler to call
            event: The event to pass to the handler
        """
        try:
            await handler(event)
        except Exception as e:
            # In production, you might want to use proper logging
            print(f"Error in async handler {handler.__name__}: {e}")

    async def _safe_call_sync(self, handler: SyncHandler, event: Event) -> None:
        """
        Safely call a sync handler in a thread pool, catching exceptions.

        Args:
            handler: The sync handler to call
            event: The event to pass to the handler
        """
        try:
            # Run sync handler in thread pool to avoid blocking
            await asyncio.to_thread(handler, event)
        except Exception as e:
            print(f"Error in sync handler {handler.__name__}: {e}")

    def get_listener_count(self, event_type: Optional[EventType] = None) -> int:
        """
        Get the number of registered listeners.

        Args:
            event_type: If provided, count only listeners for this event type.
                       If None, count all listeners (including global).

        Returns:
            Number of registered listeners

        Examples:
            >>> emitter = EventEmitter()
            >>> emitter.add_listener(EventType.MESSAGE_CHUNK, lambda e: None)
            >>> emitter.get_listener_count(EventType.MESSAGE_CHUNK)
            1
            >>> emitter.get_listener_count()  # All listeners
            1
        """
        if event_type is not None:
            return len(self._listeners[event_type])
        else:
            # Count all type-specific + global listeners
            total = sum(len(handlers) for handlers in self._listeners.values())
            total += len(self._global_listeners)
            return total


# Convenience function for creating common events
def create_message_chunk_event(
    session_id: str,
    chunk: str,
    index: int = 0
) -> Event:
    """
    Create a MESSAGE_CHUNK event for streaming tokens.

    Args:
        session_id: The session identifier
        chunk: The text chunk/token
        index: The chunk index in the stream (default: 0)

    Returns:
        Event object ready to emit

    Examples:
        >>> event = create_message_chunk_event("session_123", "Hello", 0)
        >>> await emitter.emit(event)
    """
    return Event(
        type=EventType.MESSAGE_CHUNK,
        session_id=session_id,
        data={"chunk": chunk, "index": index}
    )


def create_tool_event(
    session_id: str,
    tool_name: str,
    is_result: bool = False,
    **kwargs
) -> Event:
    """
    Create a TOOL_CALLED or TOOL_RESULT event.

    Args:
        session_id: The session identifier
        tool_name: Name of the tool
        is_result: True for TOOL_RESULT, False for TOOL_CALLED
        **kwargs: Additional tool-specific data (args, result, error, etc.)

    Returns:
        Event object ready to emit

    Examples:
        >>> # Tool call
        >>> event = create_tool_event(
        ...     "session_123",
        ...     "read_file",
        ...     args={"path": "/tmp/test.txt"}
        ... )
        >>>
        >>> # Tool result
        >>> event = create_tool_event(
        ...     "session_123",
        ...     "read_file",
        ...     is_result=True,
        ...     result="file contents",
        ...     duration_ms=150
        ... )
    """
    event_type = EventType.TOOL_RESULT if is_result else EventType.TOOL_CALLED
    return Event(
        type=event_type,
        session_id=session_id,
        data={"tool": tool_name, **kwargs}
    )


def create_file_event(
    session_id: str,
    path: str,
    operation: str = "modified",
    **kwargs
) -> Event:
    """
    Create a file operation event (FILE_CREATED, FILE_MODIFIED, FILE_DELETED).

    Args:
        session_id: The session identifier
        path: File path
        operation: "created", "modified", or "deleted" (default: "modified")
        **kwargs: Additional file-specific data (size, content_type, etc.)

    Returns:
        Event object ready to emit

    Examples:
        >>> event = create_file_event(
        ...     "session_123",
        ...     "/tmp/output.txt",
        ...     operation="created",
        ...     size=1024
        ... )
    """
    operation_map = {
        "created": EventType.FILE_CREATED,
        "modified": EventType.FILE_MODIFIED,
        "deleted": EventType.FILE_DELETED,
    }

    event_type = operation_map.get(
        operation.lower(),
        EventType.FILE_MODIFIED
    )

    return Event(
        type=event_type,
        session_id=session_id,
        data={"path": path, **kwargs}
    )


def create_usage_event(
    session_id: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    **kwargs
) -> Event:
    """
    Create a USAGE_UPDATE event for tracking token consumption.

    Args:
        session_id: The session identifier
        input_tokens: Number of input tokens used
        output_tokens: Number of output tokens generated
        **kwargs: Additional usage data (cost, cache_hits, etc.)

    Returns:
        Event object ready to emit

    Examples:
        >>> event = create_usage_event(
        ...     "session_123",
        ...     input_tokens=1500,
        ...     output_tokens=500,
        ...     cost_usd=0.025
        ... )
    """
    return Event(
        type=EventType.USAGE_UPDATE,
        session_id=session_id,
        data={
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            **kwargs
        }
    )
