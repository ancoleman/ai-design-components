"""
Session management for Claude agents.

Provides session lifecycle management, state tracking, and file system watching
for detecting session changes.
"""

from claude_agent_manager.session.manager import SessionManager
from claude_agent_manager.session.storage import SessionStorage
from claude_agent_manager.session.types.session import Message, Session, SessionState
from claude_agent_manager.session.watcher import SessionFileInfo, SessionWatcher

__all__ = [
    "Message",
    "Session",
    "SessionState",
    "SessionManager",
    "SessionStorage",
    "SessionWatcher",
    "SessionFileInfo",
]
