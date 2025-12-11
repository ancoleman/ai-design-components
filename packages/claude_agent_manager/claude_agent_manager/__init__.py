"""
Claude Agent Manager

A Python library for managing Claude AI subagents with session control,
event streaming, and process orchestration.
"""

__version__ = "0.1.0"

# Core components
from claude_agent_manager.core.detector import AgentDetector, DetectionResult
from claude_agent_manager.core.events import Event, EventEmitter, EventType
from claude_agent_manager.core.parser import ParsedMessage, StreamJsonParser, UsageStats
from claude_agent_manager.core.process import ProcessConfig, ProcessManager, ProcessResult

# Session management
from claude_agent_manager.session.manager import SessionManager
from claude_agent_manager.session.watcher import SessionWatcher
from claude_agent_manager.session.storage import SessionStorage
from claude_agent_manager.session.types import Session, SessionState, Message

# Orchestration
from claude_agent_manager.orchestration.coordinator import (
    AgentConfig,
    AgentCoordinator,
    AgentResult,
    AgentRole,
)
from claude_agent_manager.orchestration.queue import TaskQueue, Task, TaskPriority
from claude_agent_manager.orchestration.circuit_breaker import CircuitBreaker, CircuitState

# Skillchain integration (optional - requires PyYAML)
try:
    from claude_agent_manager.skillchain import (
        SkillchainExecutor,
        SkillExecutionResult,
        ProgressManager,
        ProgressFile,
        RegistryManager,
        SkillInfo,
    )
    SKILLCHAIN_AVAILABLE = True
except ImportError:
    SKILLCHAIN_AVAILABLE = False

__all__ = [
    # Version
    "__version__",
    # Core
    "AgentDetector",
    "DetectionResult",
    "Event",
    "EventEmitter",
    "EventType",
    "ParsedMessage",
    "StreamJsonParser",
    "UsageStats",
    "ProcessConfig",
    "ProcessManager",
    "ProcessResult",
    # Session
    "Session",
    "SessionManager",
    "SessionState",
    "SessionWatcher",
    "SessionStorage",
    "Message",
    # Orchestration
    "AgentConfig",
    "AgentCoordinator",
    "AgentResult",
    "AgentRole",
    "TaskQueue",
    "Task",
    "TaskPriority",
    "CircuitBreaker",
    "CircuitState",
    # Skillchain (when available)
    "SKILLCHAIN_AVAILABLE",
]

# Add skillchain exports if available
if SKILLCHAIN_AVAILABLE:
    __all__.extend([
        "SkillchainExecutor",
        "SkillExecutionResult",
        "ProgressManager",
        "ProgressFile",
        "RegistryManager",
        "SkillInfo",
    ])
