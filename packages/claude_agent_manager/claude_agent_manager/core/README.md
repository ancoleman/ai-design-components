# Core Module

The core module provides fundamental building blocks for managing Claude Code CLI processes.

## Components

### Process Management (`process.py`)

Orchestrates Claude Code CLI execution with async support, streaming output, and event emission.

**Key Classes:**
- `ProcessManager` - Main process orchestration
- `ProcessConfig` - Configuration for process execution
- `ProcessResult` - Execution results with usage stats

**Features:**
- Async process execution
- Streaming output support
- Session continuity with `--resume`
- Image input support
- Process interruption
- Event emission for lifecycle tracking
- Automatic usage tracking

**Example:**
```python
from claude_agent_manager.core import ProcessManager, ProcessConfig

manager = ProcessManager()
config = ProcessConfig(
    prompt="Explain this code",
    cwd="/path/to/project",
    session_id="session-1"
)

result = await manager.execute(config)
print(result.text)
```

### Stream Parser (`parser.py`)

Parses stream-json output from Claude Code CLI, extracting session IDs, response text, and usage statistics.

**Key Classes:**
- `StreamJsonParser` - Main parser
- `ParsedMessage` - Parsed message container
- `UsageStats` - Token usage and cost tracking

**Features:**
- JSONL parsing with buffering
- Session ID extraction
- Tool usage tracking
- Cumulative usage statistics
- Event emission for parsed messages

**Example:**
```python
from claude_agent_manager.core import StreamJsonParser

parser = StreamJsonParser(session_id="test", emitter=emitter)

async for line in process.stdout:
    messages = await parser.process_chunk(line)
    for msg in messages:
        if msg.result:
            print(msg.result)
```

### Event System (`events.py`)

Async event emitter for tracking agent lifecycle, tool usage, and file operations.

**Key Classes:**
- `EventEmitter` - Async event dispatcher
- `Event` - Immutable event object
- `EventType` - Enum of event types

**Features:**
- Async/sync handler support
- Type-safe event registration
- Concurrent handler execution
- Global and type-specific listeners

**Example:**
```python
from claude_agent_manager.core import EventEmitter, EventType, Event

emitter = EventEmitter()

@emitter.on(EventType.SESSION_COMPLETE)
async def on_complete(event):
    print(f"Session {event.session_id} complete")

await emitter.emit(Event(
    type=EventType.SESSION_COMPLETE,
    session_id="session-1",
    data={"duration": 5.2}
))
```

### Binary Detection (`detector.py`)

Locates Claude Code CLI binary across various installation methods and paths.

**Key Classes:**
- `AgentDetector` - Binary location detector
- `DetectionResult` - Detection outcome

**Features:**
- Expanded PATH search
- Common location checking
- Version detection
- Result caching
- Homebrew/npm/manual install support

**Example:**
```python
from claude_agent_manager.core import AgentDetector

detector = AgentDetector()
result = await detector.detect()

if result.available:
    print(f"Found at: {result.path}")
    print(f"Version: {result.version}")
else:
    print(f"Not found: {result.error}")
```

## Event Types

The core module emits the following events:

| Event Type | Trigger | Data Fields |
|------------|---------|-------------|
| `SESSION_STARTED` | Session initialized | `claude_session_id` |
| `SESSION_RESUMED` | Session resumed | `claude_session_id` |
| `SESSION_COMPLETE` | Session finished | `usage`, `duration_seconds` |
| `SESSION_ERROR` | Error occurred | `error`, `exit_code` |
| `MESSAGE_RECEIVED` | Complete message | `content` |
| `MESSAGE_CHUNK` | Streaming chunk | `chunk` |
| `TOOL_CALLED` | Tool invoked | `tool`, `args` |
| `TOOL_RESULT` | Tool completed | `tool`, `result` |
| `PROCESS_SPAWNED` | Process started | `pid`, `args` |
| `PROCESS_EXIT` | Process terminated | `exit_code`, `duration_seconds` |
| `USAGE_UPDATE` | Usage data | `input_tokens`, `output_tokens`, `cost` |

## Architecture

```
Core Module Architecture
========================

┌─────────────────────────────────────────────────────────────┐
│                        Application                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      ProcessManager                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Detector   │  │    Parser    │  │   Emitter    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Claude Code CLI Process                    │
│                    (subprocess.Process)                      │
└─────────────────────────────────────────────────────────────┘
```

## Usage Patterns

### Basic Execution

```python
manager = ProcessManager()
config = ProcessConfig(prompt="Hello")
result = await manager.execute(config)
```

### Session Continuity

```python
result1 = await manager.execute(config1)
config2.resume_session_id = result1.claude_session_id
result2 = await manager.execute(config2)
```

### Streaming

```python
async for chunk in manager.execute_streaming(config):
    print(chunk, end="")
```

### Event Monitoring

```python
emitter = EventEmitter()

@emitter.on(EventType.USAGE_UPDATE)
async def track_usage(event):
    print(f"Cost: ${event.data['total_cost_usd']}")

manager = ProcessManager(emitter=emitter)
```

## Dependencies

- Python 3.11+
- asyncio (stdlib)
- dataclasses (stdlib)
- json (stdlib)

## See Also

- [Process Documentation](../../docs/core/process.md)
- [Examples](../../examples/)
- [Integration Patterns](../../../../source_data/ideas/cc-integration/patterns.md)
