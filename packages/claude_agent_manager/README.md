# Claude Agent Manager

A Python library for managing Claude AI subagents with session control, event streaming, and process orchestration.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Process Management**: Spawn and control Claude Code CLI processes with full lifecycle management
- **Event System**: Real-time event streaming for messages, tool calls, file operations, and usage tracking
- **Session Management**: Persistent sessions with resume capability and message history
- **Multi-Agent Orchestration**: Coordinate multiple agents with priority queues and circuit breakers
- **Binary Detection**: Automatic Claude Code CLI detection across multiple installation methods
- **Stream Parsing**: Parse and process Claude's stream-json output format with usage tracking
- **Zero Dependencies**: Built entirely on Python standard library (optional deps for extras)

## Installation

```bash
# Basic installation
pip install -e .

# With development tools
pip install -e ".[dev]"

# With session file watching
pip install -e ".[watch]"

# With rich terminal UI
pip install -e ".[ui]"

# Install everything
pip install -e ".[all]"
```

## Quick Start

### Basic Single-Agent Usage

```python
import asyncio
from claude_agent_manager import ProcessManager, ProcessConfig, EventType

async def main():
    # Create process manager
    manager = ProcessManager()

    # Register event handlers
    @manager.emitter.on(EventType.MESSAGE_CHUNK)
    async def on_chunk(event):
        # Print streaming response in real-time
        print(event.data['chunk'], end='', flush=True)

    @manager.emitter.on(EventType.TOOL_CALLED)
    async def on_tool(event):
        print(f"\n[Tool: {event.data['tool']}]")

    # Execute a prompt
    result = await manager.execute(ProcessConfig(
        prompt="Write a hello world function in Python",
        cwd="/path/to/project",
        model="claude-opus-4-5-20251101"
    ))

    # Check results
    print(f"\n\nCost: ${result.usage.total_cost_usd:.4f}")
    print(f"Tokens: {result.usage.input_tokens + result.usage.output_tokens}")
    print(f"Duration: {result.duration_seconds:.2f}s")

asyncio.run(main())
```

### Session Management with Resume

```python
from claude_agent_manager import SessionManager

async def main():
    manager = SessionManager()

    # Create a session
    session = manager.create_session(
        cwd="/path/to/project",
        metadata={"purpose": "code review"}
    )

    # Send first message
    result1 = await manager.send_message(
        session.id,
        "Analyze the security of this authentication code"
    )

    # Session automatically resumes with context
    result2 = await manager.send_message(
        session.id,
        "What specific vulnerabilities did you find?"
    )

    # View session history
    session = manager.get_session(session.id)
    print(f"Total messages: {len(session.messages)}")
    print(f"Total cost: ${session.total_cost_usd:.4f}")

    # Close when done
    manager.close_session(session.id)

asyncio.run(main())
```

### Multi-Agent Pipeline

```python
from claude_agent_manager import AgentCoordinator, AgentConfig, AgentRole

async def main():
    # Create coordinator
    coordinator = AgentCoordinator(max_concurrent=3)

    # Register specialized agents
    coordinator.register_agent(AgentConfig(
        role=AgentRole.PLANNER,
        name="planner",
        cwd="/project",
        system_prompt="You create implementation plans."
    ))

    coordinator.register_agent(AgentConfig(
        role=AgentRole.CODER,
        name="coder",
        cwd="/project",
        system_prompt="You implement code based on plans."
    ))

    coordinator.register_agent(AgentConfig(
        role=AgentRole.TESTER,
        name="tester",
        cwd="/project",
        system_prompt="You write and run tests."
    ))

    # Execute pipeline with context passing
    stages = [
        ("planner", "Create a plan for a user authentication system"),
        ("coder", "Implement this plan: {prev_result}"),
        ("tester", "Write tests for this implementation: {prev_result}")
    ]

    results = await coordinator.execute_pipeline(stages)

    # Check results
    for i, result in enumerate(results, 1):
        print(f"\nStage {i} ({result.agent_name}): {result.success}")
        print(f"  Cost: ${result.cost_usd:.4f}")
        print(f"  Duration: {result.duration_seconds:.2f}s")

asyncio.run(main())
```

### Session File Watching

```python
from claude_agent_manager import SessionWatcher, EventType

async def main():
    watcher = SessionWatcher(
        cwd="/path/to/project",
        poll_interval=1.0
    )

    # Register event handlers
    @watcher.emitter.on(EventType.FILE_CREATED)
    async def on_session_created(event):
        print(f"New session: {event.data['session_id']}")
        print(f"  First message: {event.data['first_message']}")

    @watcher.emitter.on(EventType.FILE_MODIFIED)
    async def on_session_updated(event):
        print(f"Session updated: {event.data['session_id']}")
        print(f"  Messages: {event.data['message_count']}")

    # Start watching
    await watcher.start()

    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await watcher.stop()

asyncio.run(main())
```

### Parallel Task Execution

```python
from claude_agent_manager import AgentCoordinator, AgentConfig, AgentRole

async def main():
    coordinator = AgentCoordinator(max_concurrent=3)

    # Register agents
    coordinator.register_agent(AgentConfig(
        role=AgentRole.CODER,
        name="coder",
        cwd="/project"
    ))

    # Execute multiple tasks in parallel
    tasks = [
        ("coder", "Implement user registration endpoint"),
        ("coder", "Implement login endpoint"),
        ("coder", "Implement password reset endpoint")
    ]

    results = await coordinator.execute_parallel(tasks)

    # All tasks run concurrently (up to max_concurrent limit)
    total_cost = sum(r.cost_usd for r in results)
    print(f"Total cost: ${total_cost:.4f}")

asyncio.run(main())
```

## CLI Usage

The package includes a CLI for managing agents:

```bash
# Execute a single prompt
claude-agent execute "Write hello world" --cwd /project

# Execute with session resume
claude-agent execute "Continue the previous task" \
    --resume session_abc123 \
    --cwd /project

# List active sessions
claude-agent sessions list

# View session details
claude-agent sessions show session_abc123

# Watch for session changes
claude-agent watch /project

# Multi-agent pipeline
claude-agent pipeline \
    --stage "planner:Create implementation plan" \
    --stage "coder:Implement: {prev_result}" \
    --stage "tester:Test: {prev_result}" \
    --cwd /project
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Agent Manager                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │    Core      │  │   Session    │  │ Orchestration   │  │
│  ├──────────────┤  ├──────────────┤  ├─────────────────┤  │
│  │              │  │              │  │                 │  │
│  │ • Events     │  │ • Manager    │  │ • Coordinator   │  │
│  │ • Detector   │  │ • Storage    │  │ • Queue         │  │
│  │ • Parser     │  │ • Types      │  │ • Circuit       │  │
│  │ • Process    │  │ • Watcher    │  │   Breaker       │  │
│  │              │  │              │  │                 │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│         │                 │                    │            │
│         └─────────────────┴────────────────────┘            │
│                           │                                 │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Claude Code │
                    │     CLI      │
                    └──────────────┘
```

### Core Components

- **EventEmitter**: Async event system with concurrent handler execution
- **AgentDetector**: Automatic binary detection with PATH expansion
- **StreamJsonParser**: Parse stream-json output with usage tracking
- **ProcessManager**: Spawn and control CLI processes

### Session Components

- **Session**: Immutable session state with message history
- **SessionStorage**: File-based persistence with JSON serialization
- **SessionManager**: High-level session lifecycle management
- **SessionWatcher**: Real-time session file monitoring

### Orchestration Components

- **TaskQueue**: Priority-based async task queue
- **CircuitBreaker**: Fault tolerance with CLOSED/OPEN/HALF_OPEN states
- **AgentCoordinator**: Multi-agent orchestration with pipelines

## API Reference

### Core: ProcessManager

```python
from claude_agent_manager import ProcessManager, ProcessConfig

manager = ProcessManager()

# Execute and wait for completion
result = await manager.execute(ProcessConfig(
    prompt="Your prompt",
    cwd="/path/to/project",
    model="claude-opus-4-5-20251101",      # Optional
    max_turns=10,                           # Optional
    skip_permissions=True,                  # Default: True
    read_only=False,                        # Default: False
    timeout=120.0,                          # Default: 120s
    images=["data:image/png;base64,..."],  # Optional
))

# Stream responses in real-time
async for chunk in manager.execute_streaming(config):
    print(chunk, end='', flush=True)

# Interrupt running process
await manager.interrupt(session_id="session_123")
```

### Session: SessionManager

```python
from claude_agent_manager import SessionManager

manager = SessionManager()

# Create session
session = manager.create_session(
    cwd="/project",
    session_id="custom_id",    # Optional
    metadata={"key": "value"}  # Optional
)

# Send message (auto-resumes if Claude session ID exists)
result = await manager.send_message(
    session_id=session.id,
    prompt="Your prompt",
    model="claude-opus-4-5-20251101",  # Optional
    max_turns=5                         # Optional
)

# Get session
session = manager.get_session(session.id)

# List sessions
all_sessions = manager.list_sessions()
idle_sessions = manager.list_sessions(state=SessionState.IDLE)

# Close/delete session
manager.close_session(session.id)
manager.delete_session(session.id)
```

### Orchestration: AgentCoordinator

```python
from claude_agent_manager import (
    AgentCoordinator,
    AgentConfig,
    AgentRole,
    TaskPriority
)

coordinator = AgentCoordinator(max_concurrent=3)

# Register agent
coordinator.register_agent(AgentConfig(
    role=AgentRole.CODER,
    name="main-coder",
    cwd="/project",
    system_prompt="Custom prompt",    # Optional
    model="claude-opus-4-5-20251101", # Optional
    max_turns=10,                     # Optional
    metadata={"key": "value"}         # Optional
))

# Execute single task
result = await coordinator.execute(
    agent_name="main-coder",
    prompt="Implement feature X",
    priority=TaskPriority.HIGH
)

# Execute parallel tasks
results = await coordinator.execute_parallel([
    ("agent1", "Task 1"),
    ("agent2", "Task 2"),
])

# Execute pipeline with context passing
results = await coordinator.execute_pipeline(
    stages=[
        ("planner", "Create plan"),
        ("coder", "Implement: {prev_result}"),
        ("tester", "Test: {prev_result}")
    ],
    context={"feature": "auth"}  # Optional
)

# Queue task for background processing
task_id = await coordinator.queue_task(
    agent_name="coder",
    prompt="Background task",
    priority=TaskPriority.BACKGROUND,
    callback=lambda result: print(result)
)

# Start/stop background worker
await coordinator.start_worker()
coordinator.stop_worker()
```

### Events: EventEmitter

```python
from claude_agent_manager import EventEmitter, EventType, Event

emitter = EventEmitter()

# Register async handler with decorator
@emitter.on(EventType.MESSAGE_CHUNK)
async def handle_chunk(event: Event):
    print(event.data['chunk'], end='', flush=True)

# Register sync handler
def sync_handler(event: Event):
    print(f"Tool: {event.data['tool']}")

emitter.add_listener(EventType.TOOL_CALLED, sync_handler)

# Register global handler (receives all events)
@emitter.on_all
async def log_all(event: Event):
    print(f"[{event.type.name}] {event.session_id}")

# Emit event
await emitter.emit(Event(
    type=EventType.MESSAGE_RECEIVED,
    session_id="session_123",
    data={"content": "Hello"}
))

# Remove listener
emitter.remove_listener(EventType.TOOL_CALLED, sync_handler)

# Clear listeners
emitter.clear(EventType.MESSAGE_CHUNK)  # Clear specific type
emitter.clear()                          # Clear all
```

### Event Types

All available event types:

```python
from claude_agent_manager import EventType

# Session events
EventType.SESSION_STARTED    # New session initiated
EventType.SESSION_RESUMED    # Existing session resumed
EventType.SESSION_COMPLETE   # Session completed
EventType.SESSION_ERROR      # Session error

# Message events
EventType.MESSAGE_RECEIVED   # Complete message received
EventType.MESSAGE_CHUNK      # Streaming chunk received

# Tool events
EventType.TOOL_CALLED        # Tool invocation started
EventType.TOOL_RESULT        # Tool execution completed

# File events
EventType.FILE_CREATED       # File created
EventType.FILE_MODIFIED      # File modified
EventType.FILE_DELETED       # File deleted

# Progress events
EventType.PROGRESS_UPDATE    # Progress update

# Process events
EventType.PROCESS_SPAWNED    # Process started
EventType.PROCESS_EXIT       # Process completed

# Usage events
EventType.USAGE_UPDATE       # Token usage/cost update
```

## Advanced Usage

### Custom Event Handlers

```python
from claude_agent_manager import EventEmitter, EventType

emitter = EventEmitter()

# Track token usage across session
total_tokens = 0

@emitter.on(EventType.USAGE_UPDATE)
async def track_usage(event):
    global total_tokens
    total_tokens += event.data['input_tokens']
    total_tokens += event.data['output_tokens']
    print(f"Total tokens used: {total_tokens}")

# Monitor tool usage
@emitter.on(EventType.TOOL_CALLED)
async def log_tools(event):
    print(f"Tool called: {event.data['tool']}")
    print(f"  Args: {event.data['args']}")
```

### Circuit Breaker Usage

```python
from claude_agent_manager.orchestration import CircuitBreaker, CircuitState

breaker = CircuitBreaker(
    failure_threshold=5,      # Open after 5 failures
    timeout_seconds=60.0,     # Wait 60s before retry
    success_threshold=2       # Close after 2 successes
)

# Check before operation
if breaker.state == CircuitState.OPEN:
    print("Service unavailable, failing fast")
    return

try:
    result = await perform_operation()
    breaker.record_success()
except Exception as e:
    breaker.record_failure()
    raise

# Manual reset if needed
breaker.reset()
```

### Priority Queue Usage

```python
from claude_agent_manager.orchestration import TaskQueue, Task, TaskPriority

queue = TaskQueue(max_size=1000)

# Enqueue tasks with different priorities
await queue.enqueue(Task(
    priority=TaskPriority.CRITICAL,
    agent_name="security-agent",
    prompt="Fix critical security vulnerability"
))

await queue.enqueue(Task(
    priority=TaskPriority.BACKGROUND,
    agent_name="docs-agent",
    prompt="Update documentation"
))

# Dequeue (highest priority first)
task = await queue.dequeue(timeout=30.0)
if task:
    print(f"Processing: {task.prompt}")
```

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=claude_agent_manager --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::TestEventEmitter::test_on_decorator_async
```

## Development

```bash
# Clone repository
git clone https://github.com/ancoleman/ai-design-components.git
cd ai-design-components/packages/claude_agent_manager

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black claude_agent_manager tests

# Lint
ruff claude_agent_manager tests

# Type check
mypy claude_agent_manager
```

## Requirements

- **Python**: 3.10 or higher
- **Claude Code CLI**: Must be installed and authenticated
  ```bash
  npm install -g @anthropic-ai/claude-code
  # or
  brew install claude-code

  # Authenticate
  claude login
  ```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Built for the [Claude Code](https://www.anthropic.com/code) CLI
- Part of the [AI Design Components](https://github.com/ancoleman/ai-design-components) project
- Inspired by modern async Python patterns and agent orchestration needs

## Support

- **Documentation**: [https://ancoleman.github.io/ai-design-components/](https://ancoleman.github.io/ai-design-components/)
- **Issues**: [GitHub Issues](https://github.com/ancoleman/ai-design-components/issues)
- **Repository**: [GitHub](https://github.com/ancoleman/ai-design-components)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.
