"""
Circuit Breaker Pattern Implementation

Provides circuit breaker functionality to prevent cascading failures in agent operations.
Implements the classic three-state circuit breaker pattern: CLOSED, OPEN, HALF_OPEN.

The circuit breaker tracks failures and automatically transitions between states:
- CLOSED: Normal operation, tracking failures
- OPEN: Too many failures detected, rejecting calls to fail fast
- HALF_OPEN: Testing if the service has recovered

Usage:
    >>> breaker = CircuitBreaker(failure_threshold=5, timeout_seconds=60.0)
    >>>
    >>> if breaker.state == CircuitState.OPEN:
    ...     print("Circuit is open, failing fast")
    >>> else:
    ...     try:
    ...         # Perform operation
    ...         result = agent.execute(prompt)
    ...         breaker.record_success()
    ...     except Exception:
    ...         breaker.record_failure()
"""

from datetime import datetime, timedelta
from enum import Enum
from threading import Lock
from typing import Optional


class CircuitState(Enum):
    """
    Circuit breaker states.

    States:
        CLOSED: Normal operation, requests are allowed through.
                Failures are tracked and circuit opens if threshold is reached.

        OPEN: Circuit is open due to too many failures.
              Requests are rejected immediately to fail fast.
              After timeout period, transitions to HALF_OPEN.

        HALF_OPEN: Testing if the service has recovered.
                   Limited requests are allowed through to test recovery.
                   Transitions to CLOSED on success, OPEN on failure.
    """
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures.

    The circuit breaker pattern helps prevent cascading failures by failing fast
    when a downstream service is experiencing issues. It tracks failures and
    automatically opens the circuit when a threshold is reached.

    Thread-safe implementation using threading.Lock.

    Attributes:
        failure_threshold: Number of consecutive failures before opening circuit
        timeout_seconds: Seconds to wait before attempting reset from OPEN to HALF_OPEN
        success_threshold: Number of successes in HALF_OPEN needed to close circuit

    State Transitions:
        CLOSED -> OPEN: When failure_count >= failure_threshold
        OPEN -> HALF_OPEN: After timeout_seconds elapsed
        HALF_OPEN -> CLOSED: When success_count >= success_threshold
        HALF_OPEN -> OPEN: On any failure

    Examples:
        >>> # Create circuit breaker
        >>> breaker = CircuitBreaker(
        ...     failure_threshold=5,
        ...     timeout_seconds=60.0,
        ...     success_threshold=2
        ... )
        >>>
        >>> # Check state before operation
        >>> if breaker.state == CircuitState.OPEN:
        ...     raise Exception("Circuit breaker is open")
        >>>
        >>> # Record operation result
        >>> try:
        ...     result = perform_operation()
        ...     breaker.record_success()
        ... except Exception:
        ...     breaker.record_failure()
        ...     raise
        >>>
        >>> # Check if ready to attempt reset
        >>> if breaker.should_attempt_reset():
        ...     print("Circuit ready to test recovery")
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: float = 60.0,
        success_threshold: int = 2
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of consecutive failures before opening circuit.
                             Default: 5
            timeout_seconds: Seconds to wait in OPEN state before attempting reset.
                           Default: 60.0
            success_threshold: Number of consecutive successes in HALF_OPEN state
                             required to close circuit. Default: 2

        Examples:
            >>> # Default settings
            >>> breaker = CircuitBreaker()
            >>>
            >>> # Custom thresholds
            >>> breaker = CircuitBreaker(
            ...     failure_threshold=3,
            ...     timeout_seconds=30.0,
            ...     success_threshold=1
            ... )
        """
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.success_threshold = success_threshold

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[datetime] = None
        self._lock = Lock()

    @property
    def state(self) -> CircuitState:
        """
        Get current circuit breaker state.

        Automatically transitions from OPEN to HALF_OPEN if timeout has expired.
        Thread-safe property access.

        Returns:
            Current CircuitState

        Examples:
            >>> breaker = CircuitBreaker()
            >>> breaker.state
            <CircuitState.CLOSED: 'closed'>
            >>>
            >>> # After failures
            >>> for _ in range(5):
            ...     breaker.record_failure()
            >>> breaker.state
            <CircuitState.OPEN: 'open'>
        """
        with self._lock:
            # Auto-transition from OPEN to HALF_OPEN if timeout expired
            if self._state == CircuitState.OPEN and self.should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                self._success_count = 0

            return self._state

    def should_attempt_reset(self) -> bool:
        """
        Check if timeout has expired and circuit should attempt reset.

        Returns True if circuit is OPEN and timeout period has elapsed.
        Does not modify state - use the state property for auto-transition.

        Returns:
            True if timeout expired and reset should be attempted, False otherwise

        Examples:
            >>> breaker = CircuitBreaker(timeout_seconds=60.0)
            >>> # After circuit opens
            >>> breaker.should_attempt_reset()
            False
            >>>
            >>> # After 60+ seconds
            >>> breaker.should_attempt_reset()
            True
        """
        if self._last_failure_time is None:
            return False

        elapsed = datetime.utcnow() - self._last_failure_time
        return elapsed > timedelta(seconds=self.timeout_seconds)

    def record_success(self) -> None:
        """
        Record a successful operation.

        Behavior by state:
            - CLOSED: Resets failure count to 0
            - HALF_OPEN: Increments success count, transitions to CLOSED if threshold reached
            - OPEN: No effect (should not be called in OPEN state)

        Thread-safe operation.

        Examples:
            >>> breaker = CircuitBreaker(success_threshold=2)
            >>>
            >>> # In CLOSED state
            >>> breaker.record_success()  # Resets failure count
            >>>
            >>> # In HALF_OPEN state
            >>> breaker.record_success()  # success_count = 1
            >>> breaker.record_success()  # success_count = 2, transitions to CLOSED
        """
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1

                if self._success_count >= self.success_threshold:
                    # Recovered - close the circuit
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    self._success_count = 0
                    self._last_failure_time = None

            elif self._state == CircuitState.CLOSED:
                # Reset failure count on success
                self._failure_count = 0

    def record_failure(self) -> None:
        """
        Record a failed operation.

        Behavior by state:
            - CLOSED: Increments failure count, opens circuit if threshold reached
            - HALF_OPEN: Immediately opens circuit (recovery attempt failed)
            - OPEN: Increments failure count

        Thread-safe operation.

        Examples:
            >>> breaker = CircuitBreaker(failure_threshold=3)
            >>>
            >>> # In CLOSED state
            >>> breaker.record_failure()  # failure_count = 1
            >>> breaker.record_failure()  # failure_count = 2
            >>> breaker.record_failure()  # failure_count = 3, opens circuit
            >>>
            >>> # In HALF_OPEN state
            >>> breaker.record_failure()  # Immediately opens circuit
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = datetime.utcnow()

            if self._state == CircuitState.CLOSED:
                # Check if we've hit the failure threshold
                if self._failure_count >= self.failure_threshold:
                    self._state = CircuitState.OPEN

            elif self._state == CircuitState.HALF_OPEN:
                # Failed during recovery attempt - reopen circuit
                self._state = CircuitState.OPEN
                self._success_count = 0

    def reset(self) -> None:
        """
        Manually reset the circuit breaker to CLOSED state.

        Clears all counters and timestamps. Use with caution - this bypasses
        the normal state transition logic.

        Thread-safe operation.

        Examples:
            >>> breaker = CircuitBreaker()
            >>> # After many failures
            >>> breaker.state
            <CircuitState.OPEN: 'open'>
            >>>
            >>> # Manual reset
            >>> breaker.reset()
            >>> breaker.state
            <CircuitState.CLOSED: 'closed'>
        """
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = None

    def __repr__(self) -> str:
        """String representation of circuit breaker state."""
        return (
            f"CircuitBreaker("
            f"state={self._state.value}, "
            f"failures={self._failure_count}/{self.failure_threshold}, "
            f"successes={self._success_count}/{self.success_threshold})"
        )
