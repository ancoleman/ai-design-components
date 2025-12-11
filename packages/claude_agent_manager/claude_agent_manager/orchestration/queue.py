"""
Priority Task Queue Implementation

Provides an async priority queue for managing agent tasks with different priority levels.
Tasks are processed in priority order (CRITICAL first, BACKGROUND last), with FIFO ordering
within the same priority level.

Usage:
    >>> queue = TaskQueue(max_size=1000)
    >>>
    >>> # Create and enqueue a task
    >>> task = Task(
    ...     priority=TaskPriority.HIGH,
    ...     agent_name="coder",
    ...     prompt="Implement feature X",
    ...     callback=lambda result: print(f"Done: {result}")
    ... )
    >>> await queue.enqueue(task)
    >>>
    >>> # Dequeue and process
    >>> task = await queue.dequeue(timeout=30.0)
    >>> if task:
    ...     print(f"Processing: {task.prompt}")
"""

import asyncio
import heapq
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Any, Callable, Dict, Optional


class TaskPriority(IntEnum):
    """
    Task priority levels for queue ordering.

    Lower numeric values = higher priority (processed first).
    Tasks with the same priority are processed in FIFO order.

    Priority Levels:
        CRITICAL (0): Urgent tasks requiring immediate attention (e.g., error recovery)
        HIGH (1): Important tasks that should be processed soon (e.g., user requests)
        NORMAL (2): Standard priority for most tasks (default)
        LOW (3): Non-urgent tasks that can wait
        BACKGROUND (4): Lowest priority for background processing
    """
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


@dataclass(order=True)
class Task:
    """
    Represents a task to be executed by an agent.

    Tasks are ordered by priority (lower = higher priority), then by creation time (FIFO).
    The dataclass ordering is configured to only compare priority and created_at fields.

    Attributes:
        priority: Task priority level (used for heap ordering)
        created_at: When the task was created (used for FIFO within priority)
        id: Unique task identifier (auto-generated if not provided)
        agent_name: Name of the agent that should execute this task
        prompt: The prompt/instruction for the agent
        callback: Optional callback function to call when task completes
        metadata: Additional task-specific metadata

    Examples:
        >>> # High priority task
        >>> task = Task(
        ...     priority=TaskPriority.HIGH,
        ...     agent_name="reviewer",
        ...     prompt="Review PR #123"
        ... )
        >>>
        >>> # Task with callback
        >>> task = Task(
        ...     priority=TaskPriority.NORMAL,
        ...     agent_name="coder",
        ...     prompt="Write unit tests",
        ...     callback=lambda result: print(f"Tests: {result}"),
        ...     metadata={"pr_number": 123}
        ... )
    """
    # Fields used for ordering (compare=True) - must have defaults or come first
    priority: TaskPriority = field(compare=True)

    # Required fields not used for ordering (compare=False)
    agent_name: str = field(compare=False)
    prompt: str = field(compare=False)

    # Optional fields with defaults
    created_at: datetime = field(default_factory=datetime.utcnow, compare=True)
    id: str = field(default_factory=lambda: str(uuid.uuid4()), compare=False)
    callback: Optional[Callable[[Any], None]] = field(default=None, compare=False)
    metadata: Dict[str, Any] = field(default_factory=dict, compare=False)

    def __str__(self) -> str:
        """Human-readable task representation."""
        return (
            f"Task(id={self.id[:8]}, priority={self.priority.name}, "
            f"agent={self.agent_name}, prompt={self.prompt[:50]}...)"
        )


class TaskQueue:
    """
    Async priority queue for managing agent tasks.

    Uses heapq for efficient priority-based ordering. Tasks are processed in order of:
    1. Priority (CRITICAL first, BACKGROUND last)
    2. Creation time (FIFO within same priority)

    Thread-safe using asyncio.Condition for coordination between producers and consumers.

    Attributes:
        max_size: Maximum number of tasks the queue can hold (default: 1000)

    Examples:
        >>> # Create queue
        >>> queue = TaskQueue(max_size=100)
        >>>
        >>> # Producer: Add tasks
        >>> task = Task(
        ...     priority=TaskPriority.HIGH,
        ...     agent_name="coder",
        ...     prompt="Fix bug in module X"
        ... )
        >>> await queue.enqueue(task)
        >>>
        >>> # Consumer: Process tasks
        >>> while True:
        ...     task = await queue.dequeue(timeout=60.0)
        ...     if task:
        ...         result = await execute_task(task)
        ...         if task.callback:
        ...             task.callback(result)
        >>>
        >>> # Check queue status
        >>> print(f"Queue size: {queue.size}")
        >>> print(f"Is empty: {queue.is_empty()}")
    """

    def __init__(self, max_size: int = 1000):
        """
        Initialize task queue.

        Args:
            max_size: Maximum number of tasks the queue can hold.
                     Enqueue will block when queue is full. Default: 1000

        Examples:
            >>> # Default size
            >>> queue = TaskQueue()
            >>>
            >>> # Custom size
            >>> queue = TaskQueue(max_size=500)
        """
        self.max_size = max_size
        self._heap: list[Task] = []
        self._condition = asyncio.Condition()

    async def enqueue(self, task: Task) -> None:
        """
        Add a task to the queue.

        Blocks if queue is full until space becomes available.
        Tasks are ordered by priority and creation time.

        Args:
            task: Task to add to the queue

        Raises:
            RuntimeError: If called outside an asyncio event loop

        Examples:
            >>> queue = TaskQueue()
            >>>
            >>> # Add high priority task
            >>> task = Task(
            ...     priority=TaskPriority.HIGH,
            ...     agent_name="coder",
            ...     prompt="Implement feature"
            ... )
            >>> await queue.enqueue(task)
            >>>
            >>> # Add critical task (will be processed first)
            >>> critical_task = Task(
            ...     priority=TaskPriority.CRITICAL,
            ...     agent_name="reviewer",
            ...     prompt="Review security issue"
            ... )
            >>> await queue.enqueue(critical_task)
        """
        async with self._condition:
            # Wait if queue is full
            while len(self._heap) >= self.max_size:
                await self._condition.wait()

            # Add to heap (priority queue)
            heapq.heappush(self._heap, task)

            # Notify waiting consumers
            self._condition.notify()

    async def dequeue(self, timeout: Optional[float] = None) -> Optional[Task]:
        """
        Remove and return the highest priority task from the queue.

        Blocks if queue is empty until a task becomes available or timeout expires.
        Returns None if timeout is reached.

        Args:
            timeout: Maximum seconds to wait for a task. None = wait forever.
                    Default: None

        Returns:
            The highest priority task, or None if timeout reached

        Raises:
            RuntimeError: If called outside an asyncio event loop

        Examples:
            >>> queue = TaskQueue()
            >>>
            >>> # Wait forever for a task
            >>> task = await queue.dequeue()
            >>> print(f"Got task: {task.prompt}")
            >>>
            >>> # Wait with timeout
            >>> task = await queue.dequeue(timeout=30.0)
            >>> if task is None:
            ...     print("No tasks available")
            >>> else:
            ...     print(f"Processing: {task.prompt}")
        """
        async with self._condition:
            # Wait for task or timeout
            if timeout is not None:
                try:
                    await asyncio.wait_for(
                        self._wait_for_task(),
                        timeout=timeout
                    )
                except asyncio.TimeoutError:
                    return None
            else:
                await self._wait_for_task()

            # Get highest priority task
            task = heapq.heappop(self._heap)

            # Notify waiting producers (in case queue was full)
            self._condition.notify()

            return task

    async def _wait_for_task(self) -> None:
        """
        Wait until a task is available in the queue.

        Internal helper method used by dequeue.
        """
        while len(self._heap) == 0:
            await self._condition.wait()

    @property
    def size(self) -> int:
        """
        Get the current number of tasks in the queue.

        Returns:
            Number of tasks currently in the queue

        Examples:
            >>> queue = TaskQueue()
            >>> queue.size
            0
            >>>
            >>> await queue.enqueue(task1)
            >>> await queue.enqueue(task2)
            >>> queue.size
            2
        """
        return len(self._heap)

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        Returns:
            True if queue has no tasks, False otherwise

        Examples:
            >>> queue = TaskQueue()
            >>> queue.is_empty()
            True
            >>>
            >>> await queue.enqueue(task)
            >>> queue.is_empty()
            False
        """
        return len(self._heap) == 0

    def __len__(self) -> int:
        """Support len() built-in."""
        return len(self._heap)

    def __repr__(self) -> str:
        """String representation of queue state."""
        return (
            f"TaskQueue(size={len(self._heap)}, "
            f"max_size={self.max_size})"
        )
