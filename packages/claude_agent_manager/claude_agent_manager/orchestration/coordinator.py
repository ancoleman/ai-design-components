"""
Agent Coordinator for Multi-Agent Orchestration

Provides high-level coordination of multiple Claude agents with support for:
- Agent registration and lifecycle management
- Concurrent execution with semaphore-based rate limiting
- Priority-based task queuing
- Pipeline execution with context passing
- Circuit breaker integration for fault tolerance
- Progress tracking and event emission

Usage:
    >>> coordinator = AgentCoordinator(max_concurrent=3)
    >>>
    >>> # Register agents
    >>> coordinator.register_agent(AgentConfig(
    ...     role=AgentRole.CODER,
    ...     name="main-coder",
    ...     cwd="/tmp/project"
    ... ))
    >>>
    >>> # Execute task
    >>> result = await coordinator.execute(
    ...     agent_name="main-coder",
    ...     prompt="Implement feature X"
    ... )
    >>>
    >>> # Pipeline execution
    >>> stages = [
    ...     ("planner", "Create implementation plan"),
    ...     ("coder", "Implement: {prev_result}"),
    ...     ("tester", "Test implementation: {prev_result}")
    ... ]
    >>> results = await coordinator.execute_pipeline(stages)
"""

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from claude_agent_manager.core.events import Event, EventEmitter, EventType
from claude_agent_manager.orchestration.circuit_breaker import CircuitBreaker, CircuitState
from claude_agent_manager.orchestration.queue import Task, TaskPriority, TaskQueue
from claude_agent_manager.session.manager import SessionManager


class AgentRole(Enum):
    """
    Predefined agent role types.

    Roles provide semantic meaning to agents and can be used for routing,
    capabilities filtering, or organizational purposes.

    Roles:
        CODER: Implements code, writes features
        REVIEWER: Reviews code, provides feedback
        TESTER: Writes and executes tests
        PLANNER: Creates plans, architectures, designs
        CUSTOM: User-defined role
    """
    CODER = "coder"
    REVIEWER = "reviewer"
    TESTER = "tester"
    PLANNER = "planner"
    CUSTOM = "custom"


@dataclass
class AgentConfig:
    """
    Configuration for registering an agent.

    Defines the identity, role, working directory, and behavioral parameters
    for an agent managed by the coordinator.

    Attributes:
        role: The agent's role (CODER, REVIEWER, TESTER, etc.)
        name: Unique identifier for the agent
        cwd: Working directory for the agent's file operations
        system_prompt: Optional custom system prompt to override defaults
        model: Optional model to use (e.g., 'claude-opus-4-5-20251101')
        max_turns: Optional maximum conversation turns per execution
        metadata: Additional agent-specific configuration

    Examples:
        >>> # Basic coder agent
        >>> config = AgentConfig(
        ...     role=AgentRole.CODER,
        ...     name="backend-coder",
        ...     cwd="/tmp/backend"
        ... )
        >>>
        >>> # Custom agent with system prompt
        >>> config = AgentConfig(
        ...     role=AgentRole.CUSTOM,
        ...     name="docs-writer",
        ...     cwd="/tmp/docs",
        ...     system_prompt="You are a technical documentation expert.",
        ...     model="claude-opus-4-5-20251101",
        ...     metadata={"style": "markdown"}
        ... )
    """
    role: AgentRole
    name: str
    cwd: str
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    max_turns: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.name:
            raise ValueError("Agent name cannot be empty")
        if not self.cwd:
            raise ValueError("Agent cwd cannot be empty")


@dataclass
class AgentResult:
    """
    Result from an agent execution.

    Contains the output, metrics, and status information from executing
    a prompt with an agent.

    Attributes:
        agent_name: Name of the agent that executed the task
        task_id: Unique identifier for the task
        success: Whether the execution completed successfully
        output: The agent's response text
        cost_usd: Total cost in USD for the execution
        duration_seconds: How long the execution took
        error: Error message if execution failed (None if successful)

    Examples:
        >>> result = await coordinator.execute("coder", "Write hello world")
        >>> if result.success:
        ...     print(f"Output: {result.output}")
        ...     print(f"Cost: ${result.cost_usd:.4f}")
        ...     print(f"Duration: {result.duration_seconds:.2f}s")
        ... else:
        ...     print(f"Error: {result.error}")
    """
    agent_name: str
    task_id: str
    success: bool
    output: str
    cost_usd: float
    duration_seconds: float
    error: Optional[str] = None

    def __str__(self) -> str:
        """Human-readable result representation."""
        status = "SUCCESS" if self.success else "FAILED"
        return (
            f"AgentResult({status}, agent={self.agent_name}, "
            f"task={self.task_id[:8]}, duration={self.duration_seconds:.2f}s, "
            f"cost=${self.cost_usd:.4f})"
        )


class AgentCoordinator:
    """
    Orchestrates multiple Claude agents with advanced coordination features.

    The coordinator manages agent lifecycles, executes tasks with priority-based
    queuing, supports pipeline workflows with context passing, and provides
    fault tolerance through circuit breakers.

    Features:
        - Agent registration with dedicated sessions
        - Concurrent execution with semaphore-based rate limiting
        - Priority-based task queue
        - Circuit breaker integration per agent
        - Pipeline execution with {prev_result} context substitution
        - Parallel task execution
        - Progress tracking via events
        - Background task worker

    Attributes:
        session_manager: SessionManager for creating agent sessions
        emitter: EventEmitter for progress and lifecycle events
        max_concurrent: Maximum number of concurrent agent executions

    Examples:
        >>> # Create coordinator
        >>> coordinator = AgentCoordinator(max_concurrent=3)
        >>>
        >>> # Register agents
        >>> coordinator.register_agent(AgentConfig(
        ...     role=AgentRole.CODER,
        ...     name="coder",
        ...     cwd="/tmp/project"
        ... ))
        >>>
        >>> # Execute single task
        >>> result = await coordinator.execute(
        ...     agent_name="coder",
        ...     prompt="Implement feature X",
        ...     priority=TaskPriority.HIGH
        ... )
        >>>
        >>> # Execute pipeline
        >>> stages = [
        ...     ("planner", "Plan implementation"),
        ...     ("coder", "Implement: {prev_result}"),
        ...     ("tester", "Test: {prev_result}")
        ... ]
        >>> results = await coordinator.execute_pipeline(stages)
        >>>
        >>> # Execute in parallel
        >>> tasks = [
        ...     ("coder", "Fix bug A"),
        ...     ("reviewer", "Review PR B")
        ... ]
        >>> results = await coordinator.execute_parallel(tasks)
    """

    def __init__(
        self,
        session_manager: Optional[SessionManager] = None,
        emitter: Optional[EventEmitter] = None,
        max_concurrent: int = 3
    ):
        """
        Initialize the agent coordinator.

        Args:
            session_manager: SessionManager for agent sessions (creates new if None)
            emitter: EventEmitter for events (creates new if None)
            max_concurrent: Maximum concurrent agent executions (default: 3)

        Examples:
            >>> # Use defaults
            >>> coordinator = AgentCoordinator()
            >>>
            >>> # Custom configuration
            >>> emitter = EventEmitter()
            >>> manager = SessionManager(emitter=emitter)
            >>> coordinator = AgentCoordinator(
            ...     session_manager=manager,
            ...     emitter=emitter,
            ...     max_concurrent=5
            ... )
        """
        self.emitter = emitter or EventEmitter()
        self.session_manager = session_manager or SessionManager(emitter=self.emitter)
        self.max_concurrent = max_concurrent

        # Agent registry
        self._agents: Dict[str, AgentConfig] = {}
        self._agent_sessions: Dict[str, str] = {}  # agent_name -> session_id
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}

        # Task queue and worker
        self._task_queue = TaskQueue(max_size=1000)
        self._worker_running = False
        self._worker_task: Optional[asyncio.Task] = None

        # Concurrency control
        self._semaphore = asyncio.Semaphore(max_concurrent)

    def register_agent(self, config: AgentConfig) -> None:
        """
        Register an agent with the coordinator.

        Creates a dedicated session and circuit breaker for the agent.
        Agent names must be unique.

        Args:
            config: Agent configuration

        Raises:
            ValueError: If agent with same name already registered

        Examples:
            >>> coordinator = AgentCoordinator()
            >>>
            >>> # Register coder agent
            >>> coordinator.register_agent(AgentConfig(
            ...     role=AgentRole.CODER,
            ...     name="backend-coder",
            ...     cwd="/tmp/backend",
            ...     system_prompt="You are a backend developer.",
            ...     model="claude-opus-4-5-20251101"
            ... ))
            >>>
            >>> # Register reviewer agent
            >>> coordinator.register_agent(AgentConfig(
            ...     role=AgentRole.REVIEWER,
            ...     name="code-reviewer",
            ...     cwd="/tmp/backend"
            ... ))
        """
        if config.name in self._agents:
            raise ValueError(f"Agent '{config.name}' is already registered")

        # Store config
        self._agents[config.name] = config

        # Create session for agent
        session = self.session_manager.create_session(
            cwd=config.cwd,
            metadata={
                "agent_name": config.name,
                "agent_role": config.role.value,
                **config.metadata
            }
        )
        self._agent_sessions[config.name] = session.id

        # Create circuit breaker
        self._circuit_breakers[config.name] = CircuitBreaker(
            failure_threshold=5,
            timeout_seconds=60.0,
            success_threshold=2
        )

    def unregister_agent(self, name: str) -> bool:
        """
        Unregister an agent and close its session.

        Args:
            name: Name of the agent to unregister

        Returns:
            True if agent was found and unregistered, False otherwise

        Examples:
            >>> coordinator.unregister_agent("backend-coder")
            True
            >>> coordinator.unregister_agent("nonexistent")
            False
        """
        if name not in self._agents:
            return False

        # Close session
        session_id = self._agent_sessions.get(name)
        if session_id:
            self.session_manager.close_session(session_id)
            del self._agent_sessions[name]

        # Remove from registries
        del self._agents[name]
        del self._circuit_breakers[name]

        return True

    async def execute(
        self,
        agent_name: str,
        prompt: str,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> AgentResult:
        """
        Execute a prompt with a registered agent.

        Uses circuit breaker pattern for fault tolerance and semaphore
        for concurrency control.

        Args:
            agent_name: Name of the registered agent
            prompt: Prompt to send to the agent
            priority: Task priority (default: NORMAL)

        Returns:
            AgentResult with execution outcome and metrics

        Raises:
            ValueError: If agent not registered
            RuntimeError: If circuit breaker is open

        Examples:
            >>> # Execute with default priority
            >>> result = await coordinator.execute(
            ...     agent_name="coder",
            ...     prompt="Write a hello world function"
            ... )
            >>>
            >>> # High priority execution
            >>> result = await coordinator.execute(
            ...     agent_name="reviewer",
            ...     prompt="Review this critical security fix",
            ...     priority=TaskPriority.HIGH
            ... )
        """
        if agent_name not in self._agents:
            raise ValueError(f"Agent '{agent_name}' is not registered")

        # Check circuit breaker
        breaker = self._circuit_breakers[agent_name]
        if breaker.state == CircuitState.OPEN:
            raise RuntimeError(
                f"Circuit breaker is OPEN for agent '{agent_name}'. "
                "Service may be experiencing issues."
            )

        task_id = str(uuid.uuid4())
        start_time = time.time()

        # Acquire semaphore for concurrency control
        async with self._semaphore:
            try:
                # Get agent config and session
                config = self._agents[agent_name]
                session_id = self._agent_sessions[agent_name]

                # Execute prompt
                result = await self.session_manager.send_message(
                    session_id=session_id,
                    prompt=prompt,
                    model=config.model,
                    max_turns=config.max_turns
                )

                # Calculate metrics
                duration = time.time() - start_time
                session = self.session_manager.get_session(session_id)
                cost = session.total_cost_usd if session else 0.0

                # Record success in circuit breaker
                breaker.record_success()

                return AgentResult(
                    agent_name=agent_name,
                    task_id=task_id,
                    success=True,
                    output=result.output,
                    cost_usd=cost,
                    duration_seconds=duration,
                    error=None
                )

            except Exception as e:
                # Record failure in circuit breaker
                breaker.record_failure()

                duration = time.time() - start_time
                return AgentResult(
                    agent_name=agent_name,
                    task_id=task_id,
                    success=False,
                    output="",
                    cost_usd=0.0,
                    duration_seconds=duration,
                    error=str(e)
                )

    async def execute_parallel(
        self,
        tasks: List[Tuple[str, str]],
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> List[AgentResult]:
        """
        Execute multiple agent tasks in parallel.

        Tasks are executed concurrently up to max_concurrent limit.
        Returns results in the same order as input tasks.

        Args:
            tasks: List of (agent_name, prompt) tuples
            priority: Priority for all tasks (default: NORMAL)

        Returns:
            List of AgentResult objects in same order as input

        Examples:
            >>> # Execute multiple tasks in parallel
            >>> tasks = [
            ...     ("coder", "Implement feature A"),
            ...     ("coder", "Implement feature B"),
            ...     ("reviewer", "Review PR #123")
            ... ]
            >>> results = await coordinator.execute_parallel(tasks)
            >>>
            >>> for result in results:
            ...     print(f"{result.agent_name}: {result.success}")
        """
        # Create execution coroutines
        coros = [
            self.execute(agent_name, prompt, priority)
            for agent_name, prompt in tasks
        ]

        # Execute all in parallel
        results = await asyncio.gather(*coros, return_exceptions=True)

        # Convert exceptions to failed results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                agent_name, prompt = tasks[i]
                final_results.append(AgentResult(
                    agent_name=agent_name,
                    task_id=str(uuid.uuid4()),
                    success=False,
                    output="",
                    cost_usd=0.0,
                    duration_seconds=0.0,
                    error=str(result)
                ))
            else:
                final_results.append(result)

        return final_results

    async def execute_pipeline(
        self,
        stages: List[Tuple[str, str]],
        context: Optional[Dict[str, Any]] = None
    ) -> List[AgentResult]:
        """
        Execute a multi-stage pipeline with context passing.

        Stages are executed sequentially. Each stage can reference the previous
        stage's output using {prev_result} in the prompt. Additional context
        variables can be provided.

        Emits PROGRESS_UPDATE events for each stage.

        Args:
            stages: List of (agent_name, prompt) tuples. Prompts can contain
                   {prev_result} to reference previous stage output.
            context: Optional context dict for template substitution

        Returns:
            List of AgentResult objects, one per stage

        Raises:
            ValueError: If any agent is not registered

        Examples:
            >>> # Simple pipeline
            >>> stages = [
            ...     ("planner", "Create a plan for feature X"),
            ...     ("coder", "Implement this plan: {prev_result}"),
            ...     ("tester", "Test this implementation: {prev_result}")
            ... ]
            >>> results = await coordinator.execute_pipeline(stages)
            >>>
            >>> # Pipeline with context
            >>> stages = [
            ...     ("coder", "Implement {feature_name}"),
            ...     ("tester", "Test {feature_name}: {prev_result}")
            ... ]
            >>> results = await coordinator.execute_pipeline(
            ...     stages,
            ...     context={"feature_name": "user authentication"}
            ... )
        """
        results = []
        ctx = context or {}
        prev_result = ""

        for stage_num, (agent_name, prompt_template) in enumerate(stages, 1):
            # Emit progress event
            await self.emitter.emit(Event(
                type=EventType.PROGRESS_UPDATE,
                session_id="coordinator",
                data={
                    "stage": stage_num,
                    "total_stages": len(stages),
                    "agent": agent_name,
                    "description": f"Stage {stage_num}/{len(stages)}: {agent_name}"
                }
            ))

            # Substitute context variables
            ctx["prev_result"] = prev_result
            prompt = prompt_template.format(**ctx)

            # Execute stage
            result = await self.execute(
                agent_name=agent_name,
                prompt=prompt,
                priority=TaskPriority.NORMAL
            )
            results.append(result)

            # Update context with result
            if result.success:
                prev_result = result.output
            else:
                # Stop pipeline on failure
                break

        return results

    async def queue_task(
        self,
        agent_name: str,
        prompt: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        callback: Optional[Callable[[AgentResult], None]] = None
    ) -> str:
        """
        Add a task to the priority queue for background processing.

        Tasks are processed by the worker task (started via start_worker).
        Returns a task ID that can be used for tracking.

        Args:
            agent_name: Name of the registered agent
            prompt: Prompt to send to the agent
            priority: Task priority (default: NORMAL)
            callback: Optional callback to call when task completes

        Returns:
            Task ID (UUID string)

        Raises:
            ValueError: If agent not registered

        Examples:
            >>> # Queue a background task
            >>> task_id = await coordinator.queue_task(
            ...     agent_name="coder",
            ...     prompt="Generate documentation",
            ...     priority=TaskPriority.BACKGROUND
            ... )
            >>>
            >>> # Queue with callback
            >>> def on_complete(result: AgentResult):
            ...     print(f"Task completed: {result.success}")
            >>>
            >>> task_id = await coordinator.queue_task(
            ...     agent_name="reviewer",
            ...     prompt="Review PR #456",
            ...     callback=on_complete
            ... )
        """
        if agent_name not in self._agents:
            raise ValueError(f"Agent '{agent_name}' is not registered")

        # Create task
        task = Task(
            priority=priority,
            agent_name=agent_name,
            prompt=prompt,
            callback=callback,
            metadata={"queued_at": time.time()}
        )

        # Add to queue
        await self._task_queue.enqueue(task)

        return task.id

    async def start_worker(self) -> None:
        """
        Start background worker to process queued tasks.

        The worker runs continuously, dequeuing and executing tasks.
        Should be called after registering agents.

        Examples:
            >>> coordinator = AgentCoordinator()
            >>> coordinator.register_agent(config)
            >>>
            >>> # Start worker in background
            >>> asyncio.create_task(coordinator.start_worker())
            >>>
            >>> # Queue tasks
            >>> await coordinator.queue_task("coder", "Task 1")
            >>> await coordinator.queue_task("coder", "Task 2")
        """
        if self._worker_running:
            return

        self._worker_running = True

        while self._worker_running:
            try:
                # Dequeue task (wait up to 5 seconds)
                task = await self._task_queue.dequeue(timeout=5.0)

                if task is None:
                    continue

                # Execute task
                result = await self.execute(
                    agent_name=task.agent_name,
                    prompt=task.prompt,
                    priority=task.priority
                )

                # Call callback if provided
                if task.callback:
                    try:
                        task.callback(result)
                    except Exception as e:
                        # Log callback error but don't stop worker
                        print(f"Error in task callback: {e}")

            except Exception as e:
                # Log error but keep worker running
                print(f"Error in worker: {e}")

    def stop_worker(self) -> None:
        """
        Stop the background worker.

        Gracefully stops the worker after the current task completes.

        Examples:
            >>> coordinator.stop_worker()
        """
        self._worker_running = False

    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """
        Get status information for a registered agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Dict with agent status, or None if not registered

        Examples:
            >>> status = coordinator.get_agent_status("coder")
            >>> print(f"Circuit: {status['circuit_state']}")
            >>> print(f"Session: {status['session_id']}")
        """
        if agent_name not in self._agents:
            return None

        config = self._agents[agent_name]
        breaker = self._circuit_breakers[agent_name]
        session_id = self._agent_sessions.get(agent_name)

        return {
            "name": agent_name,
            "role": config.role.value,
            "cwd": config.cwd,
            "session_id": session_id,
            "circuit_state": breaker.state.value,
            "circuit_breaker": repr(breaker)
        }

    def list_agents(self) -> List[str]:
        """
        Get list of all registered agent names.

        Returns:
            List of agent names

        Examples:
            >>> coordinator.list_agents()
            ['coder', 'reviewer', 'tester']
        """
        return list(self._agents.keys())

    def __repr__(self) -> str:
        """String representation of coordinator state."""
        return (
            f"AgentCoordinator("
            f"agents={len(self._agents)}, "
            f"max_concurrent={self.max_concurrent}, "
            f"queue_size={self._task_queue.size})"
        )
