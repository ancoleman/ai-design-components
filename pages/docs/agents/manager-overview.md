---
sidebar_position: 2
title: Agent Manager
description: Claude Agent Manager - Python library for programmatic agent orchestration
---

# Claude Agent Manager

The Claude Agent Manager (`claude_agent_manager`) is a production-ready Python library for spawning, managing, and orchestrating Claude Code CLI agents with real-time streaming, event-driven architecture, session management, and multi-agent coordination.

## Package Overview

```
claude_agent_manager/
├── core/                  # Core functionality
│   ├── detector.py       # CLI binary detection
│   ├── events.py         # Event system (16 event types)
│   ├── parser.py         # Stream-JSON parser
│   └── process.py        # Process management
│
├── session/              # Session management
│   ├── manager.py        # Session lifecycle
│   ├── watcher.py        # File monitoring
│   ├── storage.py        # JSON persistence
│   └── types/            # Session types
│
├── orchestration/        # Multi-agent coordination
│   ├── coordinator.py    # Agent coordination
│   ├── queue.py          # Priority task queue
│   └── circuit_breaker.py # Fault tolerance
│
├── skillchain/           # Skillchain integration
│   ├── executor.py       # Skill execution
│   ├── progress.py       # Progress tracking
│   └── registry.py       # Skill routing
│
└── cli/                  # Command-line interface
    └── main.py           # claude-agent command
```

## Installation

```bash
# Basic installation (stdlib only)
pip install claude-agent-manager

# With skillchain support
pip install claude-agent-manager[skillchain]

# From source
cd ai-design-components/packages/claude_agent_manager
pip install -e ".[dev,skillchain]"
```

## Core Modules

### ProcessManager

The central component for spawning and managing Claude processes:

```python
from claude_agent_manager import ProcessManager, ProcessConfig

manager = ProcessManager()

result = await manager.execute(ProcessConfig(
    prompt="Write a function that calculates factorial",
    cwd="/my/project",
    timeout=120.0,
    skip_permissions=True,
))

print(result.text)               # Response text
print(result.claude_session_id)  # For --resume later
print(result.usage.total_cost_usd)
```

### EventEmitter

Subscribe to agent lifecycle events:

```python
from claude_agent_manager import EventEmitter, EventType

emitter = EventEmitter()

@emitter.on(EventType.MESSAGE_CHUNK)
async def on_chunk(event):
    print(event.data['chunk'], end='', flush=True)

@emitter.on(EventType.TOOL_CALLED)
async def on_tool(event):
    print(f"Tool: {event.data['tool']}")

@emitter.on(EventType.USAGE_UPDATE)
async def on_usage(event):
    print(f"Cost: ${event.data['total_cost_usd']:.4f}")
```

### AgentDetector

Locate the Claude Code CLI binary:

```python
from claude_agent_manager import AgentDetector

detector = AgentDetector()
detection = await detector.detect()

if detection.available:
    print(f"Found: {detection.path}")
    print(f"Version: {detection.version}")
else:
    print(f"Not found: {detection.error}")
```

### StreamJsonParser

Parse Claude's stream-json output format:

```python
from claude_agent_manager import StreamJsonParser

parser = StreamJsonParser(session_id="my-session", emitter=emitter)

# Process streaming output
messages = await parser.process_chunk(chunk)

# Access parsed state
print(parser.claude_session_id)  # Session ID from system init
print(parser.usage.total_cost_usd)  # Accumulated cost
```

## Session Management

### SessionManager

Track conversations across sessions:

```python
from claude_agent_manager import SessionManager

manager = SessionManager()

# Create session
session = await manager.create_session(
    cwd="/my/project",
    metadata={"task": "feature-implementation"}
)

# Execute with tracking
result = await manager.execute(session.id, "Write the login component")

# Resume later
result = await manager.execute(
    session.id,
    "Add form validation",
    resume=True  # Uses --resume flag
)

# List sessions
sessions = manager.list_sessions()
for s in sessions:
    print(f"{s.id}: {s.state.name} - {len(s.messages)} messages")
```

### SessionWatcher

Monitor session files for real-time updates:

```python
from claude_agent_manager import SessionWatcher, EventEmitter, EventType

emitter = EventEmitter()

@emitter.on(EventType.FILE_CREATED)
async def on_new_session(event):
    print(f"New session: {event.data['session_id']}")

@emitter.on(EventType.FILE_MODIFIED)
async def on_update(event):
    print(f"Updated: {event.data['session_id']}")

watcher = SessionWatcher(cwd="/my/project", emitter=emitter)
await watcher.start()
```

## Orchestration

### AgentCoordinator

Coordinate multiple agents:

```python
from claude_agent_manager import AgentCoordinator, AgentConfig, AgentRole

coordinator = AgentCoordinator(max_concurrent=3)

# Register agents
coordinator.register_agent(AgentConfig(
    name="coder",
    role=AgentRole.CODER,
    cwd="/project"
))

coordinator.register_agent(AgentConfig(
    name="tester",
    role=AgentRole.TESTER,
    cwd="/project"
))

coordinator.register_agent(AgentConfig(
    name="reviewer",
    role=AgentRole.REVIEWER,
    cwd="/project"
))

# Execute tasks
result = await coordinator.execute_task("coder", "Implement user auth")

# Execute pipeline with context passing
results = await coordinator.execute_pipeline([
    {"agent": "coder", "task": "Write the feature"},
    {"agent": "tester", "task": "Write tests for: {prev_result}"},
    {"agent": "reviewer", "task": "Review: {prev_result}"}
])
```

### TaskQueue

Priority-based task scheduling:

```python
from claude_agent_manager import TaskQueue, Task, TaskPriority

queue = TaskQueue()

# Add tasks with priorities
await queue.put(Task(
    id="urgent-fix",
    priority=TaskPriority.CRITICAL,
    payload={"prompt": "Fix production bug"}
))

await queue.put(Task(
    id="feature",
    priority=TaskPriority.NORMAL,
    payload={"prompt": "Add new feature"}
))

# Process in priority order
task = await queue.get()  # Returns urgent-fix first
```

### CircuitBreaker

Fault tolerance for agent operations:

```python
from claude_agent_manager import CircuitBreaker, CircuitState

breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=30.0,
    half_open_max_calls=2
)

async def execute_with_protection():
    if breaker.state == CircuitState.OPEN:
        raise Exception("Circuit is open, agent unavailable")

    try:
        result = await manager.execute(config)
        breaker.record_success()
        return result
    except Exception as e:
        breaker.record_failure()
        raise
```

## Skillchain Integration

### SkillchainExecutor

Execute skillchains programmatically:

```python
from claude_agent_manager import SkillchainExecutor

executor = SkillchainExecutor("/path/to/ai-design-components")

# Route a goal to skills
route = executor.route("dashboard with charts and postgres")
print(f"Blueprint: {route.blueprint}")
print(f"Domains: {route.domains}")
print(f"Skills: {[s.name for s in route.matched_skills]}")

# Execute
result = await executor.execute(
    goal="Build a sales dashboard",
    project_path="/my/project",
    blueprint="dashboard",
    maturity="intermediate",
    on_skill_start=lambda s, i, t: print(f"Starting {s.name}"),
    on_skill_complete=lambda r, i, t: print(f"Done: {r.skill_name}")
)
```

### ProgressManager

Track skillchain progress:

```python
from claude_agent_manager import ProgressManager

pm = ProgressManager()

# Load existing progress
progress = pm.load("/my/project")

if progress:
    print(f"Goal: {progress.goal}")
    print(f"Completed: {progress.execution.completed_count}")
    print(f"Remaining: {len(pm.get_resumable_skills(progress))}")
```

## CLI Commands

```bash
# Check Claude CLI status
claude-agent check

# Run single prompt
claude-agent run "Explain recursion" --cwd /project

# Run with streaming
claude-agent run "Write a function" --stream

# Resume session
claude-agent run "Add tests" --resume abc123

# Session management
claude-agent sessions list --cwd /project
claude-agent sessions show abc123

# Watch for changes
claude-agent watch --cwd /project

# Skillchain commands
claude-agent skillchain blueprints
claude-agent skillchain route "dashboard with charts"
claude-agent skillchain run "Build API" --blueprint crud-api
claude-agent skillchain status --project /my/project
claude-agent skillchain resume --project /my/project
```

## Event Types

| Event | Data | Description |
|-------|------|-------------|
| `SESSION_STARTED` | `claude_session_id`, `slash_commands` | Agent initialized |
| `SESSION_RESUMED` | `claude_session_id` | Resumed existing session |
| `SESSION_COMPLETE` | `exit_code`, `duration` | Agent finished |
| `SESSION_ERROR` | `error`, `code` | Agent error |
| `MESSAGE_RECEIVED` | `content` | Complete message |
| `MESSAGE_CHUNK` | `chunk` | Streaming text |
| `TOOL_CALLED` | `tool`, `tool_id`, `input` | Tool invocation |
| `TOOL_RESULT` | `tool_id`, `result` | Tool completion |
| `FILE_CREATED` | `path` | File created |
| `FILE_MODIFIED` | `path` | File modified |
| `FILE_DELETED` | `path` | File deleted |
| `USAGE_UPDATE` | `input_tokens`, `output_tokens`, `cost` | Token usage |
| `PROGRESS_UPDATE` | `percent`, `message` | Task progress |
| `PROCESS_SPAWNED` | `pid` | CLI process started |
| `PROCESS_EXIT` | `exit_code` | CLI process ended |

## Configuration

### ProcessConfig Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `prompt` | str | required | The prompt to send |
| `cwd` | str | required | Working directory |
| `session_id` | str | auto | Internal tracking ID |
| `resume_session_id` | str | None | Claude session to resume |
| `model` | str | None | Model override |
| `max_turns` | int | None | Max conversation turns |
| `read_only` | bool | False | Read-only mode |
| `timeout` | float | 120.0 | Execution timeout |
| `skip_permissions` | bool | True | Skip permission prompts |

## Next Steps

- [Architecture](./architecture) - System design and data flow diagrams
- [Skillchain Integration](./skillchain-integration) - Deep dive into skill execution
- [Real-World Usage](./real-world-usage) - Practical examples and patterns
