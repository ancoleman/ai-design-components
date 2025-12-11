#!/usr/bin/env python3
"""
Basic example of using ProcessManager to execute Claude Code CLI.

This example demonstrates:
- Creating a ProcessConfig
- Executing a simple prompt
- Handling the result
- Accessing usage statistics
"""

import asyncio
from claude_agent_manager.core import (
    ProcessManager,
    ProcessConfig,
    EventEmitter,
    EventType,
)


async def main():
    """Execute a simple Claude Code prompt."""

    # Set up event handling
    emitter = EventEmitter()

    @emitter.on(EventType.PROCESS_SPAWNED)
    async def on_spawn(event):
        print(f"[Process] Spawned PID: {event.data.get('pid')}")

    @emitter.on(EventType.SESSION_STARTED)
    async def on_session_start(event):
        print(f"[Session] Started: {event.data.get('claude_session_id')}")

    @emitter.on(EventType.USAGE_UPDATE)
    async def on_usage(event):
        usage = event.data
        print(f"[Usage] Input: {usage['input_tokens']}, Output: {usage['output_tokens']}")
        print(f"[Usage] Cost: ${usage['total_cost_usd']:.4f}")

    @emitter.on(EventType.PROCESS_EXIT)
    async def on_exit(event):
        print(f"[Process] Exited with code: {event.data.get('exit_code')}")

    # Create process manager
    manager = ProcessManager(emitter=emitter)

    # Configure the process
    config = ProcessConfig(
        prompt="What is the capital of France? Please answer in one sentence.",
        cwd=".",
        session_id="example-session-1",
        skip_permissions=True,
        timeout=60.0
    )

    print("Executing Claude Code CLI...")
    print(f"Prompt: {config.prompt}")
    print()

    # Execute
    try:
        result = await manager.execute(config)

        print()
        print("=" * 80)
        print("RESULT")
        print("=" * 80)
        print(f"Session ID: {result.session_id}")
        print(f"Claude Session ID: {result.claude_session_id}")
        print(f"Exit Code: {result.exit_code}")
        print(f"Duration: {result.duration_seconds:.2f}s")
        print()
        print("Response:")
        print(result.text)
        print()
        print("Usage Statistics:")
        print(f"  Input Tokens: {result.usage.input_tokens}")
        print(f"  Output Tokens: {result.usage.output_tokens}")
        print(f"  Cache Read Tokens: {result.usage.cache_read_tokens}")
        print(f"  Cache Creation Tokens: {result.usage.cache_creation_tokens}")
        print(f"  Total Cost: ${result.usage.total_cost_usd:.4f}")

        if result.error:
            print(f"Error: {result.error}")

    except Exception as e:
        print(f"Error executing: {e}")


if __name__ == "__main__":
    asyncio.run(main())
