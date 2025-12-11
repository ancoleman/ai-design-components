"""
Session type definitions for Claude Agent Manager.

This module defines the core data structures for managing Claude agent sessions,
including session state tracking, message history, and usage statistics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class SessionState(Enum):
    """
    State of a Claude agent session.

    States:
        IDLE: Session is created but not currently processing
        BUSY: Session is actively processing a request
        ERROR: Session encountered an error
        CLOSED: Session has been closed and cannot be resumed
    """
    IDLE = auto()
    BUSY = auto()
    ERROR = auto()
    CLOSED = auto()


@dataclass
class Message:
    """
    A single message in the conversation history.

    Attributes:
        role: Message role ('user' or 'assistant')
        content: Message text content
        timestamp: When the message was created
        tool_calls: List of tool calls made in this message (for assistant messages)

    Examples:
        >>> # User message
        >>> Message(role='user', content='Explain this code')
        >>>
        >>> # Assistant message with tool call
        >>> Message(
        ...     role='assistant',
        ...     content='Let me read that file...',
        ...     tool_calls=[{'name': 'Read', 'args': {'file_path': '/tmp/test.txt'}}]
        ... )
    """
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format for serialization."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "tool_calls": self.tool_calls,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create Message from dictionary."""
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            tool_calls=data.get("tool_calls", []),
        )


@dataclass
class Session:
    """
    A Claude agent session with state, history, and usage tracking.

    Sessions track the complete lifecycle of a conversation with Claude, including
    message history, token usage, cost, and the ability to resume conversations
    using Claude's session ID.

    Attributes:
        id: Our internal session identifier
        claude_session_id: Claude's session ID for resumption (from --resume)
        cwd: Working directory for the session
        state: Current session state
        messages: Conversation history
        created_at: When the session was created
        updated_at: When the session was last modified
        total_cost_usd: Cumulative cost in USD
        total_input_tokens: Cumulative input tokens
        total_output_tokens: Cumulative output tokens
        metadata: Additional custom metadata

    Examples:
        >>> # Create new session
        >>> session = Session(
        ...     id='session_abc123',
        ...     cwd='/Users/user/project'
        ... )
        >>>
        >>> # Add a message
        >>> session.messages.append(Message(
        ...     role='user',
        ...     content='Explain this code'
        ... ))
        >>>
        >>> # Update state
        >>> session.state = SessionState.BUSY
        >>>
        >>> # Track usage
        >>> session.total_input_tokens += 1500
        >>> session.total_output_tokens += 500
        >>> session.total_cost_usd += 0.025
    """
    id: str
    claude_session_id: Optional[str] = None
    cwd: str = '.'
    state: SessionState = SessionState.IDLE
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    total_cost_usd: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary format for serialization."""
        return {
            "id": self.id,
            "claude_session_id": self.claude_session_id,
            "cwd": self.cwd,
            "state": self.state.name,
            "messages": [msg.to_dict() for msg in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "total_cost_usd": self.total_cost_usd,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        """Create Session from dictionary."""
        return cls(
            id=data["id"],
            claude_session_id=data.get("claude_session_id"),
            cwd=data.get("cwd", "."),
            state=SessionState[data.get("state", "IDLE")],
            messages=[Message.from_dict(m) for m in data.get("messages", [])],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            total_cost_usd=data.get("total_cost_usd", 0.0),
            total_input_tokens=data.get("total_input_tokens", 0),
            total_output_tokens=data.get("total_output_tokens", 0),
            metadata=data.get("metadata", {}),
        )
