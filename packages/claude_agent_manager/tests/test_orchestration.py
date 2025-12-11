"""Tests for orchestration modules: circuit_breaker, queue, coordinator."""

import asyncio
import time
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from claude_agent_manager.orchestration.circuit_breaker import CircuitBreaker, CircuitState
from claude_agent_manager.orchestration.coordinator import (
    AgentConfig,
    AgentCoordinator,
    AgentResult,
    AgentRole,
)
from claude_agent_manager.orchestration.queue import Task, TaskPriority, TaskQueue


class TestCircuitState:
    """Test CircuitState enum."""

    def test_all_states_exist(self):
        """Test that all expected states are defined."""
        assert hasattr(CircuitState, "CLOSED")
        assert hasattr(CircuitState, "OPEN")
        assert hasattr(CircuitState, "HALF_OPEN")

    def test_state_values(self):
        """Test state string values."""
        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"


class TestCircuitBreaker:
    """Test CircuitBreaker class."""

    def test_breaker_initialization(self):
        """Test creating circuit breaker with defaults."""
        breaker = CircuitBreaker()

        assert breaker.failure_threshold == 5
        assert breaker.timeout_seconds == 60.0
        assert breaker.success_threshold == 2
        assert breaker.state == CircuitState.CLOSED

    def test_breaker_custom_thresholds(self):
        """Test creating circuit breaker with custom thresholds."""
        breaker = CircuitBreaker(
            failure_threshold=3, timeout_seconds=30.0, success_threshold=1
        )

        assert breaker.failure_threshold == 3
        assert breaker.timeout_seconds == 30.0
        assert breaker.success_threshold == 1

    def test_state_closed_to_open(self):
        """Test transition from CLOSED to OPEN on failures."""
        breaker = CircuitBreaker(failure_threshold=3)

        assert breaker.state == CircuitState.CLOSED

        # Record failures
        breaker.record_failure()
        assert breaker.state == CircuitState.CLOSED

        breaker.record_failure()
        assert breaker.state == CircuitState.CLOSED

        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN  # Threshold reached

    def test_state_open_to_half_open(self):
        """Test transition from OPEN to HALF_OPEN after timeout."""
        breaker = CircuitBreaker(failure_threshold=1, timeout_seconds=0.1)

        # Open the circuit
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Wait for timeout
        time.sleep(0.2)

        # Accessing state property should auto-transition
        assert breaker.state == CircuitState.HALF_OPEN

    def test_state_half_open_to_closed(self):
        """Test transition from HALF_OPEN to CLOSED on success."""
        breaker = CircuitBreaker(
            failure_threshold=1, timeout_seconds=0.1, success_threshold=2
        )

        # Open the circuit
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Wait and transition to HALF_OPEN
        time.sleep(0.2)
        assert breaker.state == CircuitState.HALF_OPEN

        # Record successes
        breaker.record_success()
        assert breaker.state == CircuitState.HALF_OPEN

        breaker.record_success()
        assert breaker.state == CircuitState.CLOSED  # Recovery complete

    def test_state_half_open_to_open_on_failure(self):
        """Test transition from HALF_OPEN back to OPEN on failure."""
        breaker = CircuitBreaker(failure_threshold=1, timeout_seconds=0.1)

        # Open the circuit
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Wait and transition to HALF_OPEN
        time.sleep(0.2)
        assert breaker.state == CircuitState.HALF_OPEN

        # Record failure during recovery
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

    def test_record_success_resets_failures(self):
        """Test that success in CLOSED state resets failure count."""
        breaker = CircuitBreaker(failure_threshold=3)

        # Record some failures
        breaker.record_failure()
        breaker.record_failure()

        # Record success - should reset count
        breaker.record_success()

        # Now we should need 3 more failures to open
        breaker.record_failure()
        breaker.record_failure()
        assert breaker.state == CircuitState.CLOSED

        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

    def test_should_attempt_reset(self):
        """Test should_attempt_reset logic."""
        breaker = CircuitBreaker(failure_threshold=1, timeout_seconds=0.1)

        # Initially no failures
        assert breaker.should_attempt_reset() is False

        # Open the circuit
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Timeout not elapsed
        assert breaker.should_attempt_reset() is False

        # Wait for timeout
        time.sleep(0.2)
        assert breaker.should_attempt_reset() is True

    def test_manual_reset(self):
        """Test manual circuit breaker reset."""
        breaker = CircuitBreaker(failure_threshold=1)

        # Open the circuit
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Manual reset
        breaker.reset()
        assert breaker.state == CircuitState.CLOSED

    def test_repr(self):
        """Test string representation."""
        breaker = CircuitBreaker()
        repr_str = repr(breaker)

        assert "CircuitBreaker" in repr_str
        assert "closed" in repr_str


class TestTaskPriority:
    """Test TaskPriority enum."""

    def test_priority_ordering(self):
        """Test that priorities are correctly ordered."""
        assert TaskPriority.CRITICAL < TaskPriority.HIGH
        assert TaskPriority.HIGH < TaskPriority.NORMAL
        assert TaskPriority.NORMAL < TaskPriority.LOW
        assert TaskPriority.LOW < TaskPriority.BACKGROUND

    def test_priority_values(self):
        """Test priority numeric values."""
        assert TaskPriority.CRITICAL == 0
        assert TaskPriority.HIGH == 1
        assert TaskPriority.NORMAL == 2
        assert TaskPriority.LOW == 3
        assert TaskPriority.BACKGROUND == 4


class TestTask:
    """Test Task dataclass."""

    def test_task_creation(self):
        """Test creating a task."""
        task = Task(
            priority=TaskPriority.HIGH,
            agent_name="coder",
            prompt="Write hello world",
        )

        assert task.priority == TaskPriority.HIGH
        assert task.agent_name == "coder"
        assert task.prompt == "Write hello world"
        assert isinstance(task.id, str)
        assert isinstance(task.created_at, datetime)

    def test_task_ordering_by_priority(self):
        """Test that tasks are ordered by priority."""
        task1 = Task(
            priority=TaskPriority.NORMAL, agent_name="agent1", prompt="Task 1"
        )
        task2 = Task(
            priority=TaskPriority.HIGH, agent_name="agent2", prompt="Task 2"
        )

        assert task2 < task1  # Higher priority comes first

    def test_task_ordering_by_time(self):
        """Test that tasks with same priority are ordered by creation time."""
        task1 = Task(
            priority=TaskPriority.NORMAL, agent_name="agent1", prompt="Task 1"
        )
        time.sleep(0.01)
        task2 = Task(
            priority=TaskPriority.NORMAL, agent_name="agent2", prompt="Task 2"
        )

        assert task1 < task2  # Earlier created comes first

    def test_task_with_callback(self):
        """Test task with callback function."""
        called = []

        def callback(result):
            called.append(result)

        task = Task(
            priority=TaskPriority.NORMAL,
            agent_name="agent",
            prompt="Test",
            callback=callback,
        )

        assert task.callback is not None
        task.callback("result")
        assert called == ["result"]

    def test_task_with_metadata(self):
        """Test task with metadata."""
        task = Task(
            priority=TaskPriority.NORMAL,
            agent_name="agent",
            prompt="Test",
            metadata={"key": "value", "number": 42},
        )

        assert task.metadata["key"] == "value"
        assert task.metadata["number"] == 42


class TestTaskQueue:
    """Test TaskQueue class."""

    def test_queue_initialization(self):
        """Test creating task queue."""
        queue = TaskQueue()

        assert queue.max_size == 1000
        assert queue.size == 0
        assert queue.is_empty() is True

    def test_queue_custom_size(self):
        """Test queue with custom max size."""
        queue = TaskQueue(max_size=100)

        assert queue.max_size == 100

    @pytest.mark.asyncio
    async def test_enqueue_dequeue(self):
        """Test basic enqueue and dequeue."""
        queue = TaskQueue()

        task = Task(
            priority=TaskPriority.NORMAL, agent_name="agent", prompt="Test"
        )

        await queue.enqueue(task)
        assert queue.size == 1
        assert not queue.is_empty()

        dequeued = await queue.dequeue(timeout=1.0)
        assert dequeued is not None
        assert dequeued.id == task.id
        assert queue.size == 0

    @pytest.mark.asyncio
    async def test_dequeue_empty_timeout(self):
        """Test dequeue on empty queue with timeout."""
        queue = TaskQueue()

        result = await queue.dequeue(timeout=0.1)
        assert result is None

    @pytest.mark.asyncio
    async def test_priority_ordering(self):
        """Test that tasks are dequeued in priority order."""
        queue = TaskQueue()

        # Enqueue tasks in random order
        task_normal = Task(
            priority=TaskPriority.NORMAL, agent_name="agent", prompt="Normal"
        )
        task_critical = Task(
            priority=TaskPriority.CRITICAL, agent_name="agent", prompt="Critical"
        )
        task_low = Task(
            priority=TaskPriority.LOW, agent_name="agent", prompt="Low"
        )

        await queue.enqueue(task_normal)
        await queue.enqueue(task_critical)
        await queue.enqueue(task_low)

        # Dequeue should get highest priority first
        first = await queue.dequeue(timeout=1.0)
        assert first.priority == TaskPriority.CRITICAL

        second = await queue.dequeue(timeout=1.0)
        assert second.priority == TaskPriority.NORMAL

        third = await queue.dequeue(timeout=1.0)
        assert third.priority == TaskPriority.LOW

    @pytest.mark.asyncio
    async def test_len(self):
        """Test __len__ method."""
        queue = TaskQueue()

        assert len(queue) == 0

        await queue.enqueue(
            Task(priority=TaskPriority.NORMAL, agent_name="agent", prompt="Test")
        )

        assert len(queue) == 1


class TestAgentRole:
    """Test AgentRole enum."""

    def test_all_roles_exist(self):
        """Test that all expected roles are defined."""
        expected_roles = ["CODER", "REVIEWER", "TESTER", "PLANNER", "CUSTOM"]

        for role_name in expected_roles:
            assert hasattr(AgentRole, role_name), f"AgentRole.{role_name} not found"


class TestAgentConfig:
    """Test AgentConfig dataclass."""

    def test_config_creation(self):
        """Test creating agent config."""
        config = AgentConfig(role=AgentRole.CODER, name="main-coder", cwd="/tmp")

        assert config.role == AgentRole.CODER
        assert config.name == "main-coder"
        assert config.cwd == "/tmp"
        assert config.system_prompt is None
        assert config.model is None

    def test_config_with_optional_fields(self):
        """Test config with all optional fields."""
        config = AgentConfig(
            role=AgentRole.REVIEWER,
            name="reviewer",
            cwd="/tmp",
            system_prompt="You are a code reviewer",
            model="claude-opus-4-5-20251101",
            max_turns=10,
            metadata={"team": "backend"},
        )

        assert config.system_prompt == "You are a code reviewer"
        assert config.model == "claude-opus-4-5-20251101"
        assert config.max_turns == 10
        assert config.metadata["team"] == "backend"

    def test_config_validation_empty_name(self):
        """Test that empty name raises error."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            AgentConfig(role=AgentRole.CODER, name="", cwd="/tmp")

    def test_config_validation_empty_cwd(self):
        """Test that empty cwd raises error."""
        with pytest.raises(ValueError, match="cwd cannot be empty"):
            AgentConfig(role=AgentRole.CODER, name="coder", cwd="")


class TestAgentResult:
    """Test AgentResult dataclass."""

    def test_result_creation_success(self):
        """Test creating successful result."""
        result = AgentResult(
            agent_name="coder",
            task_id="task_123",
            success=True,
            output="Implementation complete",
            cost_usd=0.05,
            duration_seconds=2.5,
        )

        assert result.agent_name == "coder"
        assert result.success is True
        assert result.output == "Implementation complete"
        assert result.error is None

    def test_result_creation_failure(self):
        """Test creating failed result."""
        result = AgentResult(
            agent_name="coder",
            task_id="task_123",
            success=False,
            output="",
            cost_usd=0.0,
            duration_seconds=0.5,
            error="Execution failed",
        )

        assert result.success is False
        assert result.error == "Execution failed"

    def test_result_str_representation(self):
        """Test string representation."""
        result = AgentResult(
            agent_name="coder",
            task_id="task_123",
            success=True,
            output="Done",
            cost_usd=0.01,
            duration_seconds=1.0,
        )

        str_repr = str(result)
        assert "SUCCESS" in str_repr
        assert "coder" in str_repr


class TestAgentCoordinator:
    """Test AgentCoordinator class."""

    def test_coordinator_initialization(self):
        """Test creating coordinator."""
        coordinator = AgentCoordinator(max_concurrent=5)

        assert coordinator.max_concurrent == 5
        assert coordinator.emitter is not None
        assert coordinator.session_manager is not None
        assert len(coordinator._agents) == 0

    def test_register_agent(self):
        """Test registering an agent."""
        coordinator = AgentCoordinator()

        config = AgentConfig(role=AgentRole.CODER, name="coder", cwd="/tmp")

        coordinator.register_agent(config)

        assert "coder" in coordinator._agents
        assert "coder" in coordinator._agent_sessions
        assert "coder" in coordinator._circuit_breakers

    def test_register_duplicate_agent(self):
        """Test that registering duplicate agent raises error."""
        coordinator = AgentCoordinator()

        config = AgentConfig(role=AgentRole.CODER, name="coder", cwd="/tmp")

        coordinator.register_agent(config)

        with pytest.raises(ValueError, match="already registered"):
            coordinator.register_agent(config)

    def test_unregister_agent(self):
        """Test unregistering an agent."""
        coordinator = AgentCoordinator()

        config = AgentConfig(role=AgentRole.CODER, name="coder", cwd="/tmp")
        coordinator.register_agent(config)

        unregistered = coordinator.unregister_agent("coder")
        assert unregistered is True
        assert "coder" not in coordinator._agents

        # Unregister again
        unregistered = coordinator.unregister_agent("coder")
        assert unregistered is False

    def test_list_agents(self):
        """Test listing registered agents."""
        coordinator = AgentCoordinator()

        coordinator.register_agent(
            AgentConfig(role=AgentRole.CODER, name="coder", cwd="/tmp")
        )
        coordinator.register_agent(
            AgentConfig(role=AgentRole.REVIEWER, name="reviewer", cwd="/tmp")
        )

        agents = coordinator.list_agents()

        assert len(agents) == 2
        assert "coder" in agents
        assert "reviewer" in agents

    def test_get_agent_status(self):
        """Test getting agent status."""
        coordinator = AgentCoordinator()

        config = AgentConfig(role=AgentRole.CODER, name="coder", cwd="/tmp")
        coordinator.register_agent(config)

        status = coordinator.get_agent_status("coder")

        assert status is not None
        assert status["name"] == "coder"
        assert status["role"] == "coder"
        assert status["cwd"] == "/tmp"
        assert status["circuit_state"] == "closed"

    def test_get_status_nonexistent_agent(self):
        """Test getting status for nonexistent agent."""
        coordinator = AgentCoordinator()

        status = coordinator.get_agent_status("nonexistent")
        assert status is None

    @pytest.mark.asyncio
    async def test_execute_unregistered_agent(self):
        """Test executing with unregistered agent raises error."""
        coordinator = AgentCoordinator()

        with pytest.raises(ValueError, match="not registered"):
            await coordinator.execute("nonexistent", "Test prompt")

    @pytest.mark.asyncio
    async def test_queue_task(self):
        """Test queuing a task."""
        coordinator = AgentCoordinator()

        config = AgentConfig(role=AgentRole.CODER, name="coder", cwd="/tmp")
        coordinator.register_agent(config)

        task_id = await coordinator.queue_task(
            agent_name="coder",
            prompt="Test prompt",
            priority=TaskPriority.HIGH,
        )

        assert task_id is not None
        assert coordinator._task_queue.size == 1

    @pytest.mark.asyncio
    async def test_queue_task_with_callback(self):
        """Test queuing task with callback."""
        coordinator = AgentCoordinator()

        config = AgentConfig(role=AgentRole.CODER, name="coder", cwd="/tmp")
        coordinator.register_agent(config)

        called = []

        def callback(result):
            called.append(result)

        task_id = await coordinator.queue_task(
            agent_name="coder", prompt="Test", callback=callback
        )

        assert task_id is not None

    def test_stop_worker(self):
        """Test stopping the worker."""
        coordinator = AgentCoordinator()

        coordinator._worker_running = True
        coordinator.stop_worker()

        assert coordinator._worker_running is False

    def test_repr(self):
        """Test string representation."""
        coordinator = AgentCoordinator(max_concurrent=5)

        coordinator.register_agent(
            AgentConfig(role=AgentRole.CODER, name="coder", cwd="/tmp")
        )

        repr_str = repr(coordinator)

        assert "AgentCoordinator" in repr_str
        assert "agents=1" in repr_str
        assert "max_concurrent=5" in repr_str
