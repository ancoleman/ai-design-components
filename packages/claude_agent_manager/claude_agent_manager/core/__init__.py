"""
Core components for Claude Agent Manager.

Provides fundamental building blocks for process management, event handling,
JSON stream parsing, and agent detection.
"""

from claude_agent_manager.core.detector import AgentDetector, DetectionResult
from claude_agent_manager.core.events import Event, EventEmitter, EventType
from claude_agent_manager.core.parser import ParsedMessage, StreamJsonParser, UsageStats
from claude_agent_manager.core.process import ProcessConfig, ProcessManager, ProcessResult

__all__ = [
    # Detection
    "AgentDetector",
    "DetectionResult",
    # Events
    "Event",
    "EventEmitter",
    "EventType",
    # Parser
    "ParsedMessage",
    "StreamJsonParser",
    "UsageStats",
    # Process
    "ProcessConfig",
    "ProcessManager",
    "ProcessResult",
]
