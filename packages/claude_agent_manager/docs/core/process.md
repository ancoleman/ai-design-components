# Process Management Module

The `process.py` module provides comprehensive process management for Claude Code CLI execution, handling spawning, streaming output, event emission, and lifecycle management.

## Overview

The ProcessManager class orchestrates the execution of Claude Code CLI processes with features including:

- **Async execution** with streaming output parsing
- **Image input support** via stream-json format
- **Session continuity** with `--resume` flag
- **Process interruption** and cleanup
- **Event emission** for lifecycle tracking
- **Usage statistics** and cost tracking

## Core Components

### ProcessConfig

Configuration dataclass for spawning Claude Code processes.

```python
from claude_agent_manager.core import ProcessConfig

config = ProcessConfig(
    prompt="Explain this code",
    cwd="/path/to/project",
    session_id="session-123",
    resume_session_id=None,
    model="claude-opus-4-5-20251101",
    max_turns=10,
    system_prompt=None,
    allowed_tools=["Read", "Write"],
    disallowed_tools=["Bash"],
    skip_permissions=True,
    read_only=False,
    timeout=120.0,
    images=None,
    env_overrides={}
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | Required | User prompt to send to Claude |
| `cwd` | str | `'.'` | Working directory for the process |
| `session_id` | Optional[str] | None | Internal session ID for tracking |
| `resume_session_id` | Optional[str] | None | Claude's session ID for continuation |
| `model` | Optional[str] | None | Model to use (e.g., 'claude-opus-4-5-20251101') |
| `max_turns` | Optional[int] | None | Maximum conversation turns |
| `system_prompt` | Optional[str] | None | Custom system prompt |
| `allowed_tools` | Optional[List[str]] | None | List of allowed tool names |
| `disallowed_tools` | Optional[List[str]] | None | List of disallowed tool names |
| `skip_permissions` | bool | True | Skip permission prompts |
| `read_only` | bool | False | Run in read-only mode (--permission-mode plan) |
| `timeout` | float | 120.0 | Process timeout in seconds |
| `images` | Optional[List[str]] | None | List of base64 data URLs for images |
| `env_overrides` | Dict[str, str] | {} | Additional environment variables |

### ProcessResult

Result dataclass returned from process execution.

```python
from claude_agent_manager.core import ProcessResult

result = await manager.execute(config)

# Access result data
print(f"Response: {result.text}")
print(f"Session ID: {result.claude_session_id}")
print(f"Exit Code: {result.exit_code}")
print(f"Duration: {result.duration_seconds}s")
print(f"Cost: ${result.usage.total_cost_usd}")
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `session_id` | str | Internal session ID |
| `claude_session_id` | Optional[str] | Claude's session ID (for future --resume) |
| `text` | str | Complete response text from Claude |
| `exit_code` | int | Process exit code |
| `usage` | UsageStats | Token usage and cost statistics |
| `duration_seconds` | float | Total execution time |
| `error` | Optional[str] | Error message if execution failed |

### ProcessManager

Main manager class for process execution.

```python
from claude_agent_manager.core import ProcessManager, AgentDetector, EventEmitter

# Create with custom detector and emitter
detector = AgentDetector()
emitter = EventEmitter()
manager = ProcessManager(detector, emitter)

# Or use defaults
manager = ProcessManager()
```

## Usage Examples

### Basic Execution

```python
import asyncio
from claude_agent_manager.core import ProcessManager, ProcessConfig

async def main():
    manager = ProcessManager()

    config = ProcessConfig(
        prompt="What is the capital of France?",
        cwd=".",
        session_id="example-1"
    )

    result = await manager.execute(config)

    print(f"Response: {result.text}")
    print(f"Cost: ${result.usage.total_cost_usd:.4f}")

asyncio.run(main())
```

### Session Continuity

```python
import asyncio
from claude_agent_manager.core import ProcessManager, ProcessConfig

async def conversation():
    manager = ProcessManager()

    # First message
    config1 = ProcessConfig(
        prompt="My favorite color is blue. Remember this.",
        session_id="msg-1"
    )
    result1 = await manager.execute(config1)

    # Second message - resume session
    config2 = ProcessConfig(
        prompt="What is my favorite color?",
        session_id="msg-2",
        resume_session_id=result1.claude_session_id  # Resume!
    )
    result2 = await manager.execute(config2)

    print(result2.text)  # Should reference blue

asyncio.run(conversation())
```

### Streaming Output

```python
import asyncio
from claude_agent_manager.core import ProcessManager, ProcessConfig

async def stream_example():
    manager = ProcessManager()

    config = ProcessConfig(
        prompt="Write a short story about a robot.",
        session_id="stream-1"
    )

    # Stream output as it arrives
    async for chunk in manager.execute_streaming(config):
        print(chunk, end="", flush=True)

    print()  # New line after streaming

asyncio.run(stream_example())
```

### Event Handling

```python
import asyncio
from claude_agent_manager.core import (
    ProcessManager,
    ProcessConfig,
    EventEmitter,
    EventType
)

async def event_example():
    emitter = EventEmitter()

    # Register event handlers
    @emitter.on(EventType.PROCESS_SPAWNED)
    async def on_spawn(event):
        print(f"Process spawned: PID {event.data['pid']}")

    @emitter.on(EventType.SESSION_STARTED)
    async def on_session(event):
        print(f"Session started: {event.data['claude_session_id']}")

    @emitter.on(EventType.USAGE_UPDATE)
    async def on_usage(event):
        usage = event.data
        print(f"Tokens: {usage['input_tokens']} in, {usage['output_tokens']} out")

    @emitter.on(EventType.SESSION_COMPLETE)
    async def on_complete(event):
        print(f"Session complete in {event.data['duration_seconds']}s")

    # Execute with event tracking
    manager = ProcessManager(emitter=emitter)
    config = ProcessConfig(prompt="Hello Claude!", session_id="event-1")
    result = await manager.execute(config)

asyncio.run(event_example())
```

### Image Input

```python
import asyncio
import base64
from claude_agent_manager.core import ProcessManager, ProcessConfig

async def image_example():
    # Load image and convert to base64 data URL
    with open("/path/to/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
        data_url = f"data:image/png;base64,{image_data}"

    manager = ProcessManager()

    config = ProcessConfig(
        prompt="What do you see in this image?",
        images=[data_url],
        session_id="image-1"
    )

    result = await manager.execute(config)
    print(result.text)

asyncio.run(image_example())
```

### Process Interruption

```python
import asyncio
from claude_agent_manager.core import ProcessManager, ProcessConfig

async def interrupt_example():
    manager = ProcessManager()

    config = ProcessConfig(
        prompt="Write a very long essay about AI.",
        session_id="long-task",
        timeout=300.0
    )

    # Start execution
    task = asyncio.create_task(manager.execute(config))

    # Wait a bit then interrupt
    await asyncio.sleep(5.0)
    await manager.interrupt("long-task")

    try:
        result = await task
    except asyncio.CancelledError:
        print("Task was interrupted")

asyncio.run(interrupt_example())
```

## CLI Argument Building

The ProcessManager builds Claude Code CLI arguments based on the configuration:

### Standard Arguments

```bash
claude \
  --print \
  --verbose \
  --output-format stream-json \
  --dangerously-skip-permissions \
  -- "Your prompt here"
```

### With Session Resume

```bash
claude \
  --print \
  --verbose \
  --output-format stream-json \
  --resume abc123-session-id \
  -- "Follow-up prompt"
```

### With Tool Control

```bash
claude \
  --print \
  --verbose \
  --output-format stream-json \
  --allowedTools Read,Write \
  --disallowedTools Bash \
  -- "Your prompt"
```

### With Images

```bash
claude \
  --print \
  --verbose \
  --output-format stream-json \
  --input-format stream-json
# Image message sent via stdin
```

## Environment Handling

The ProcessManager automatically:

1. **Expands PATH** - Includes common Claude installation locations
2. **Removes ANTHROPIC_API_KEY** - Forces OAuth authentication
3. **Applies overrides** - Custom environment variables from config

```python
config = ProcessConfig(
    prompt="Test",
    env_overrides={
        "CUSTOM_VAR": "value"
    }
)
```

## Event Types Emitted

The ProcessManager emits the following events:

| Event Type | When | Data |
|------------|------|------|
| `PROCESS_SPAWNED` | Process starts | `pid`, `cwd`, `args` |
| `SESSION_STARTED` | Session initialized | `claude_session_id` |
| `USAGE_UPDATE` | Usage data received | Token counts, cost |
| `PROCESS_EXIT` | Process terminates | `exit_code`, `duration_seconds` |
| `SESSION_COMPLETE` | Successful completion | `claude_session_id`, `usage` |
| `SESSION_ERROR` | Error occurred | `error`, `exit_code` |

## Error Handling

### Timeout Handling

```python
config = ProcessConfig(
    prompt="Complex task",
    timeout=30.0  # 30 second timeout
)

result = await manager.execute(config)

if result.exit_code == -1 and result.error:
    print(f"Timeout: {result.error}")
```

### Binary Not Found

```python
try:
    result = await manager.execute(config)
except RuntimeError as e:
    print(f"Claude CLI not available: {e}")
```

### Process Errors

```python
result = await manager.execute(config)

if result.exit_code != 0:
    print(f"Process failed with code {result.exit_code}")
    if result.error:
        print(f"Error: {result.error}")
```

## Integration with Parser

The ProcessManager uses `StreamJsonParser` internally to parse Claude Code CLI output:

```python
# Internal usage (automatic)
parser = StreamJsonParser(session_id=session_id, emitter=emitter)

while line := await process.stdout.readline():
    messages = await parser.process_chunk(line)
    for msg in messages:
        # Extract session ID, text, usage, etc.
        pass

# Get final usage statistics
usage = parser.usage
```

## Best Practices

### 1. Always Use Session Continuity

```python
# Good - maintains context
result1 = await manager.execute(config1)
config2.resume_session_id = result1.claude_session_id
result2 = await manager.execute(config2)

# Bad - loses context
result1 = await manager.execute(config1)
result2 = await manager.execute(config2)  # New session!
```

### 2. Handle Timeouts Appropriately

```python
# Set realistic timeouts based on task complexity
config = ProcessConfig(
    prompt="Simple question",
    timeout=30.0  # Short timeout for simple tasks
)

config = ProcessConfig(
    prompt="Analyze entire codebase",
    timeout=300.0  # Longer timeout for complex tasks
)
```

### 3. Use Event Handlers for Monitoring

```python
# Monitor token usage in real-time
@emitter.on(EventType.USAGE_UPDATE)
async def track_usage(event):
    cost = event.data['total_cost_usd']
    if cost > 1.0:  # Alert on high costs
        print(f"Warning: High cost detected: ${cost}")
```

### 4. Clean Up Active Processes

```python
try:
    result = await manager.execute(config)
finally:
    # Ensure all processes are cleaned up
    await manager.interrupt_all()
```

## See Also

- [Parser Module](./parser.md) - Stream-JSON output parsing
- [Events Module](./events.md) - Event system documentation
- [Detector Module](./detector.md) - Binary detection
- [Examples](../../examples/) - Complete working examples
