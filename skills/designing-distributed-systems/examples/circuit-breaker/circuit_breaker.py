"""
Circuit Breaker Pattern Implementation

Demonstrates: Circuit breaker with CLOSED, OPEN, HALF-OPEN states

Dependencies:
    - Python 3.7+

Usage:
    python circuit_breaker.py
"""

from enum import Enum
from datetime import datetime, timedelta
import threading
import time
import random

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker to prevent cascading failures"""

    def __init__(self, failure_threshold=5, timeout=60, success_threshold=2):
        """
        Initialize circuit breaker

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds before attempting reset from OPEN to HALF-OPEN
            success_threshold: Number of successes in HALF-OPEN before closing
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = threading.Lock()

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        with self.lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    print(f"  [CB] Transitioning to HALF-OPEN")
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN - failing fast")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self):
        """Check if timeout has expired"""
        return (self.last_failure_time and
                datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout))

    def _on_success(self):
        """Handle successful call"""
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                print(f"  [CB] HALF-OPEN: Success {self.success_count}/{self.success_threshold}")

                if self.success_count >= self.success_threshold:
                    print(f"  [CB] Transitioning to CLOSED (recovered)")
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            else:
                self.failure_count = 0

    def _on_failure(self):
        """Handle failed call"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            print(f"  [CB] Failure {self.failure_count}/{self.failure_threshold} (state: {self.state.value})")

            if self.failure_count >= self.failure_threshold:
                print(f"  [CB] Transitioning to OPEN")
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.HALF_OPEN:
                print(f"  [CB] Transitioning to OPEN (failed in HALF-OPEN)")
                self.state = CircuitState.OPEN
                self.success_count = 0

    def get_state(self):
        """Get current circuit breaker state"""
        return self.state


# Simulated external service
class UnreliableService:
    def __init__(self, failure_rate=0.5):
        self.failure_rate = failure_rate
        self.call_count = 0

    def call(self):
        """Simulate service call with configurable failure rate"""
        self.call_count += 1
        time.sleep(0.1)  # Simulate network latency

        if random.random() < self.failure_rate:
            raise Exception(f"Service failed (call {self.call_count})")

        return f"Success (call {self.call_count})"


if __name__ == "__main__":
    print("Circuit Breaker Pattern Demo\n")

    # Create circuit breaker and unreliable service
    circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=5, success_threshold=2)
    service = UnreliableService(failure_rate=0.8)  # 80% failure rate

    print("Phase 1: Failing service (80% failure rate)")
    print("=" * 60)

    # Make calls until circuit opens
    for i in range(10):
        try:
            result = circuit_breaker.call(service.call)
            print(f"Call {i+1}: {result}")
        except Exception as e:
            print(f"Call {i+1}: Failed - {e}")

        time.sleep(0.5)

    print(f"\nCircuit state: {circuit_breaker.get_state().value}")
    print("Circuit is OPEN - failing fast for next requests\n")

    # Wait for timeout
    print(f"Waiting {circuit_breaker.timeout} seconds for timeout...")
    time.sleep(circuit_breaker.timeout + 1)

    print("\nPhase 2: Service recovered (0% failure rate)")
    print("=" * 60)

    # Service recovers
    service.failure_rate = 0.0

    # Make successful calls to close circuit
    for i in range(5):
        try:
            result = circuit_breaker.call(service.call)
            print(f"Call {i+1}: {result}")
        except Exception as e:
            print(f"Call {i+1}: Failed - {e}")

        time.sleep(0.5)

    print(f"\nFinal circuit state: {circuit_breaker.get_state().value}")
