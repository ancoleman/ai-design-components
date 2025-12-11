#!/usr/bin/env python3
"""
Example of session continuity with ProcessManager.

This example demonstrates:
- Executing an initial prompt
- Capturing the Claude session ID
- Resuming the session with a follow-up prompt
- Maintaining conversation context
"""

import asyncio
from claude_agent_manager.core import ProcessManager, ProcessConfig


async def main():
    """Execute a multi-turn conversation with session continuity."""

    manager = ProcessManager()

    # First message
    print("=" * 80)
    print("FIRST MESSAGE")
    print("=" * 80)

    config1 = ProcessConfig(
        prompt="My favorite color is blue. Remember this.",
        cwd=".",
        session_id="conversation-1",
        skip_permissions=True,
        timeout=60.0
    )

    result1 = await manager.execute(config1)

    print(f"Response: {result1.text}")
    print(f"Claude Session ID: {result1.claude_session_id}")
    print(f"Cost: ${result1.usage.total_cost_usd:.4f}")
    print()

    if not result1.claude_session_id:
        print("Error: No session ID received, cannot continue")
        return

    # Second message - resume the session
    print("=" * 80)
    print("SECOND MESSAGE (RESUMING SESSION)")
    print("=" * 80)

    config2 = ProcessConfig(
        prompt="What is my favorite color?",
        cwd=".",
        session_id="conversation-2",
        resume_session_id=result1.claude_session_id,  # Resume previous session
        skip_permissions=True,
        timeout=60.0
    )

    result2 = await manager.execute(config2)

    print(f"Response: {result2.text}")
    print(f"Claude Session ID: {result2.claude_session_id}")
    print(f"Cost: ${result2.usage.total_cost_usd:.4f}")
    print()

    # Third message - continue the conversation
    print("=" * 80)
    print("THIRD MESSAGE (CONTINUING)")
    print("=" * 80)

    config3 = ProcessConfig(
        prompt="Now change my favorite color to green and confirm.",
        cwd=".",
        session_id="conversation-3",
        resume_session_id=result2.claude_session_id,  # Continue from second message
        skip_permissions=True,
        timeout=60.0
    )

    result3 = await manager.execute(config3)

    print(f"Response: {result3.text}")
    print(f"Claude Session ID: {result3.claude_session_id}")
    print(f"Cost: ${result3.usage.total_cost_usd:.4f}")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_cost = (
        result1.usage.total_cost_usd +
        result2.usage.total_cost_usd +
        result3.usage.total_cost_usd
    )
    total_tokens = (
        result1.usage.input_tokens + result1.usage.output_tokens +
        result2.usage.input_tokens + result2.usage.output_tokens +
        result3.usage.input_tokens + result3.usage.output_tokens
    )

    print(f"Total messages: 3")
    print(f"Total tokens: {total_tokens}")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Final session ID: {result3.claude_session_id}")


if __name__ == "__main__":
    asyncio.run(main())
