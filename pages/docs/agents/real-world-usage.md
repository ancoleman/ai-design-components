---
sidebar_position: 5
title: Real-World Usage
description: Practical examples and patterns for using Claude Agent Manager
---

# Real-World Usage

This guide provides practical examples showing how to use Claude Agent Manager in real-world scenarios.

## Scenario 1: Automated Code Generation Pipeline

Generate code across multiple files with coordinated agents:

```python
import asyncio
from claude_agent_manager import (
    AgentCoordinator,
    AgentConfig,
    AgentRole,
    EventEmitter,
    EventType,
)

async def code_generation_pipeline():
    """Generate a feature with code, tests, and documentation."""

    emitter = EventEmitter()

    @emitter.on(EventType.MESSAGE_CHUNK)
    async def log_progress(event):
        print(event.data['chunk'], end='', flush=True)

    coordinator = AgentCoordinator(
        emitter=emitter,
        max_concurrent=1  # Sequential for this pipeline
    )

    # Register specialized agents
    coordinator.register_agent(AgentConfig(
        name="planner",
        role=AgentRole.PLANNER,
        cwd="/my/project",
        metadata={"focus": "architecture"}
    ))

    coordinator.register_agent(AgentConfig(
        name="coder",
        role=AgentRole.CODER,
        cwd="/my/project",
        metadata={"focus": "implementation"}
    ))

    coordinator.register_agent(AgentConfig(
        name="tester",
        role=AgentRole.TESTER,
        cwd="/my/project",
        metadata={"focus": "testing"}
    ))

    # Execute pipeline with context passing
    results = await coordinator.execute_pipeline([
        {
            "agent": "planner",
            "task": """
            Plan the implementation of a user authentication system.
            Include:
            - File structure
            - Key components
            - API endpoints
            Return a structured plan.
            """
        },
        {
            "agent": "coder",
            "task": """
            Implement the authentication system based on this plan:
            {prev_result}

            Create all necessary files.
            """
        },
        {
            "agent": "tester",
            "task": """
            Write comprehensive tests for the authentication system.
            The implementation details:
            {prev_result}

            Include unit tests and integration tests.
            """
        }
    ])

    # Summary
    total_cost = sum(r.result.usage.total_cost_usd for r in results)
    print(f"\n\nPipeline Complete!")
    print(f"Total Cost: ${total_cost:.4f}")
    for r in results:
        print(f"  {r.agent_name}: {'SUCCESS' if r.success else 'FAILED'}")

asyncio.run(code_generation_pipeline())
```

## Scenario 2: Skillchain-Driven Project Bootstrap

Bootstrap a complete project using skillchain:

```python
import asyncio
from pathlib import Path
from claude_agent_manager import SkillchainExecutor, ProgressManager

async def bootstrap_project(
    project_name: str,
    project_type: str,
    output_dir: str
):
    """Bootstrap a new project using skillchain."""

    project_path = Path(output_dir) / project_name
    project_path.mkdir(parents=True, exist_ok=True)

    # Map project types to blueprints
    blueprint_map = {
        "dashboard": "dashboard",
        "api": "crud-api",
        "fullstack": None,  # Will use goal-based routing
        "ml": "ml-pipeline",
        "data": "data-pipeline",
    }

    blueprint = blueprint_map.get(project_type)

    # Goal based on project type
    goals = {
        "dashboard": f"Create a {project_name} dashboard with charts, tables, and KPI cards",
        "api": f"Create a {project_name} REST API with database and authentication",
        "fullstack": f"Create a {project_name} fullstack application with frontend and backend",
        "ml": f"Create a {project_name} ML pipeline with model training and serving",
        "data": f"Create a {project_name} data pipeline with ETL and analytics",
    }

    goal = goals.get(project_type, f"Create a {project_name} application")

    executor = SkillchainExecutor("/path/to/ai-design-components")

    print(f"Bootstrapping {project_name} ({project_type})...")
    print(f"Output: {project_path}")
    print(f"Goal: {goal}")
    print()

    # Progress tracking
    def on_skill_start(skill, index, total):
        print(f"[{index + 1}/{total}] {skill.name}")

    def on_skill_complete(result, index, total):
        status = "OK" if result.success else "FAILED"
        print(f"         {status} - ${result.cost_usd:.4f}")
        if result.files_created:
            for f in result.files_created[:3]:
                print(f"         + {f}")
            if len(result.files_created) > 3:
                print(f"         + ... and {len(result.files_created) - 3} more")

    result = await executor.execute(
        goal=goal,
        project_path=str(project_path),
        blueprint=blueprint,
        maturity="intermediate",
        on_skill_start=on_skill_start,
        on_skill_complete=on_skill_complete,
    )

    print()
    print("=" * 50)
    print(f"Project {project_name} bootstrapped!")
    print(f"Skills: {result.skills_completed}/{result.skills_planned}")
    print(f"Files: {len(result.total_files_created)}")
    print(f"Cost: ${result.total_cost_usd:.4f}")
    print(f"Duration: {result.total_duration_seconds:.1f}s")

    return result

# Usage
asyncio.run(bootstrap_project(
    project_name="my-sales-dashboard",
    project_type="dashboard",
    output_dir="/projects"
))
```

## Scenario 3: Batch Processing with Rate Limiting

Process multiple tasks with rate limiting and error handling:

```python
import asyncio
from claude_agent_manager import (
    ProcessManager,
    ProcessConfig,
    CircuitBreaker,
    CircuitState,
    EventEmitter,
)

class BatchProcessor:
    def __init__(self, max_concurrent: int = 3, rate_limit_delay: float = 1.0):
        self.emitter = EventEmitter()
        self.manager = ProcessManager(emitter=self.emitter)
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=60.0
        )
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.rate_limit_delay = rate_limit_delay
        self.results = []

    async def process_item(self, item: dict) -> dict:
        """Process a single item with circuit breaker protection."""

        if self.circuit_breaker.state == CircuitState.OPEN:
            return {
                "item": item,
                "success": False,
                "error": "Circuit breaker open"
            }

        async with self.semaphore:
            try:
                # Rate limiting
                await asyncio.sleep(self.rate_limit_delay)

                result = await self.manager.execute(ProcessConfig(
                    prompt=item["prompt"],
                    cwd=item.get("cwd", "."),
                    timeout=item.get("timeout", 60.0),
                ))

                self.circuit_breaker.record_success()

                return {
                    "item": item,
                    "success": True,
                    "result": result.text,
                    "cost": result.usage.total_cost_usd,
                    "session_id": result.claude_session_id,
                }

            except Exception as e:
                self.circuit_breaker.record_failure()
                return {
                    "item": item,
                    "success": False,
                    "error": str(e),
                }

    async def process_batch(self, items: list) -> list:
        """Process a batch of items concurrently."""

        tasks = [self.process_item(item) for item in items]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions that weren't caught
        processed = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed.append({
                    "item": items[i],
                    "success": False,
                    "error": str(result)
                })
            else:
                processed.append(result)

        return processed

# Usage
async def main():
    processor = BatchProcessor(max_concurrent=3, rate_limit_delay=0.5)

    items = [
        {"prompt": "Explain Python decorators", "cwd": "/docs"},
        {"prompt": "Explain async/await", "cwd": "/docs"},
        {"prompt": "Explain generators", "cwd": "/docs"},
        {"prompt": "Explain context managers", "cwd": "/docs"},
        {"prompt": "Explain metaclasses", "cwd": "/docs"},
    ]

    results = await processor.process_batch(items)

    # Summary
    successful = sum(1 for r in results if r["success"])
    total_cost = sum(r.get("cost", 0) for r in results if r["success"])

    print(f"Processed: {successful}/{len(items)}")
    print(f"Total Cost: ${total_cost:.4f}")

asyncio.run(main())
```

## Scenario 4: Session-Based Conversation

Maintain context across multiple interactions:

```python
import asyncio
from claude_agent_manager import SessionManager, ProcessConfig

async def interactive_session():
    """Maintain a conversation with context."""

    manager = SessionManager()

    # Create a new session
    session = await manager.create_session(
        cwd="/my/project",
        metadata={"purpose": "code-review"}
    )

    print(f"Session created: {session.id}")

    # First interaction
    result1 = await manager.execute(
        session.id,
        "Review the authentication module in src/auth/"
    )
    print(f"Review: {result1.text[:200]}...")

    # Follow-up (maintains context)
    result2 = await manager.execute(
        session.id,
        "What security improvements would you recommend?",
        resume=True
    )
    print(f"Recommendations: {result2.text[:200]}...")

    # Another follow-up
    result3 = await manager.execute(
        session.id,
        "Implement the top 3 recommendations",
        resume=True
    )
    print(f"Implementation: {result3.text[:200]}...")

    # Session summary
    print(f"\nSession Summary:")
    print(f"  Messages: {len(session.messages)}")
    print(f"  Total Cost: ${session.total_cost_usd:.4f}")
    print(f"  Claude Session: {session.claude_session_id}")

asyncio.run(interactive_session())
```

## Scenario 5: Watching and Reacting to Sessions

Monitor session activity and react to events:

```python
import asyncio
from claude_agent_manager import (
    SessionWatcher,
    EventEmitter,
    EventType,
)

async def session_monitor():
    """Monitor sessions and react to activity."""

    emitter = EventEmitter()

    @emitter.on(EventType.FILE_CREATED)
    async def on_new_session(event):
        print(f"[NEW] Session: {event.data['session_id'][:8]}...")
        print(f"      First message: {event.data.get('first_message', 'N/A')[:50]}")

    @emitter.on(EventType.FILE_MODIFIED)
    async def on_session_update(event):
        print(f"[UPDATE] Session: {event.data['session_id'][:8]}...")
        print(f"         Messages: {event.data.get('message_count', 'N/A')}")

    @emitter.on(EventType.FILE_DELETED)
    async def on_session_deleted(event):
        print(f"[DELETED] Session: {event.data['session_id'][:8]}...")

    watcher = SessionWatcher(
        cwd="/my/project",
        emitter=emitter,
        poll_interval=1.0
    )

    print("Watching sessions... (Ctrl+C to stop)")

    await watcher.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        await watcher.stop()

asyncio.run(session_monitor())
```

## Scenario 6: CI/CD Integration

Integrate with CI/CD pipelines:

```python
#!/usr/bin/env python3
"""CI/CD script for automated code review and testing."""

import asyncio
import sys
import json
from claude_agent_manager import ProcessManager, ProcessConfig

async def ci_code_review(changed_files: list) -> dict:
    """Review changed files in CI."""

    manager = ProcessManager()

    files_list = "\n".join(f"- {f}" for f in changed_files)

    result = await manager.execute(ProcessConfig(
        prompt=f"""
        Review these changed files for:
        1. Code quality issues
        2. Security vulnerabilities
        3. Performance concerns
        4. Missing tests

        Changed files:
        {files_list}

        Output a JSON report with:
        {{
          "issues": [
            {{"file": "...", "line": N, "severity": "high|medium|low", "message": "..."}}
          ],
          "summary": "...",
          "approved": true|false
        }}
        """,
        cwd=".",
        timeout=120.0,
        read_only=True,  # Don't modify files in CI
    ))

    # Parse JSON from response
    try:
        # Extract JSON from response
        text = result.text
        start = text.find('{')
        end = text.rfind('}') + 1
        report = json.loads(text[start:end])
    except:
        report = {
            "issues": [],
            "summary": result.text,
            "approved": True  # Default to approved if can't parse
        }

    return {
        "report": report,
        "cost": result.usage.total_cost_usd,
        "session_id": result.claude_session_id,
    }

async def ci_generate_tests(source_file: str) -> dict:
    """Generate tests for a source file."""

    manager = ProcessManager()

    result = await manager.execute(ProcessConfig(
        prompt=f"""
        Generate comprehensive tests for: {source_file}

        Include:
        - Unit tests for each function
        - Edge cases
        - Error handling tests

        Write the tests to an appropriate test file.
        """,
        cwd=".",
        timeout=180.0,
    ))

    return {
        "output": result.text,
        "cost": result.usage.total_cost_usd,
    }

# CLI usage
async def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["review", "test"])
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--output", default="report.json")
    args = parser.parse_args()

    if args.command == "review":
        result = await ci_code_review(args.files)
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)

        if not result["report"]["approved"]:
            print("Review FAILED")
            for issue in result["report"]["issues"]:
                print(f"  [{issue['severity']}] {issue['file']}:{issue.get('line', '?')} - {issue['message']}")
            sys.exit(1)
        else:
            print("Review PASSED")

    elif args.command == "test":
        for file in args.files:
            result = await ci_generate_tests(file)
            print(f"Generated tests for {file}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Scenario 7: Custom Event Processing

Build custom event processing pipelines:

```python
import asyncio
from datetime import datetime
from claude_agent_manager import (
    ProcessManager,
    ProcessConfig,
    EventEmitter,
    EventType,
)

class MetricsCollector:
    """Collect metrics from agent executions."""

    def __init__(self):
        self.executions = []
        self.total_tokens_in = 0
        self.total_tokens_out = 0
        self.total_cost = 0.0
        self.tools_used = {}

    def record_usage(self, event):
        self.total_tokens_in += event.data.get('input_tokens', 0)
        self.total_tokens_out += event.data.get('output_tokens', 0)
        self.total_cost += event.data.get('total_cost_usd', 0)

    def record_tool(self, event):
        tool = event.data.get('tool', 'unknown')
        self.tools_used[tool] = self.tools_used.get(tool, 0) + 1

    def summary(self) -> dict:
        return {
            "total_tokens_in": self.total_tokens_in,
            "total_tokens_out": self.total_tokens_out,
            "total_cost": self.total_cost,
            "tools_used": self.tools_used,
        }

async def run_with_metrics():
    emitter = EventEmitter()
    metrics = MetricsCollector()

    @emitter.on(EventType.USAGE_UPDATE)
    async def on_usage(event):
        metrics.record_usage(event)

    @emitter.on(EventType.TOOL_CALLED)
    async def on_tool(event):
        metrics.record_tool(event)

    manager = ProcessManager(emitter=emitter)

    # Run some executions
    await manager.execute(ProcessConfig(
        prompt="Write a Python function to calculate fibonacci numbers",
        cwd="."
    ))

    await manager.execute(ProcessConfig(
        prompt="Write tests for the fibonacci function",
        cwd="."
    ))

    # Get metrics
    summary = metrics.summary()
    print(f"Total Cost: ${summary['total_cost']:.4f}")
    print(f"Tokens: {summary['total_tokens_in']} in, {summary['total_tokens_out']} out")
    print(f"Tools Used: {summary['tools_used']}")

asyncio.run(run_with_metrics())
```

## Next Steps

- [CLI Reference](./cli-reference) - Complete command reference
- [Architecture](./architecture) - System design details
- [Skillchain Integration](./skillchain-integration) - Using with skillchain
