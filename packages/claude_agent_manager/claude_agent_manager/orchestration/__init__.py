"""
Orchestration components for managing multiple Claude agents.

Provides high-level coordination, task queuing, circuit breaker patterns,
and multi-agent workflow management.
"""

from claude_agent_manager.orchestration.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
)
from claude_agent_manager.orchestration.coordinator import (
    AgentConfig,
    AgentCoordinator,
    AgentResult,
    AgentRole,
)
from claude_agent_manager.orchestration.queue import (
    Task,
    TaskPriority,
    TaskQueue,
)

__all__ = [
    # Circuit breaker
    "CircuitBreaker",
    "CircuitState",
    # Coordinator
    "AgentConfig",
    "AgentCoordinator",
    "AgentResult",
    "AgentRole",
    # Queue
    "Task",
    "TaskPriority",
    "TaskQueue",
]
