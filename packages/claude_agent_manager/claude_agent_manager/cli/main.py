"""
CLI module for Claude Agent Manager.

Provides a command-line interface for managing Claude agent sessions,
executing prompts, and monitoring session files.
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from claude_agent_manager.core import (
    AgentDetector,
    EventEmitter,
    EventType,
    ProcessConfig,
    ProcessManager,
)
from claude_agent_manager.session import SessionManager, SessionWatcher
from claude_agent_manager.session.types import SessionState
from claude_agent_manager.utils.logging import Colors, log

# Import skillchain components (optional - may not exist in all installs)
try:
    from claude_agent_manager.skillchain import (
        SkillchainExecutor,
        ProgressManager,
        RegistryManager,
    )
    SKILLCHAIN_AVAILABLE = True
except ImportError:
    SKILLCHAIN_AVAILABLE = False


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog='claude-agent',
        description='Claude Agent Manager - Manage and execute Claude agent sessions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run a single prompt
  claude-agent run "Write a hello world program"

  # Run with streaming output
  claude-agent run "Explain this code" --stream

  # Resume a previous session
  claude-agent run "Add tests" --resume abc123def456

  # Run in read-only mode
  claude-agent run "Analyze the codebase" --read-only

  # List all sessions
  claude-agent sessions list

  # Show session details
  claude-agent sessions show abc123def456

  # Watch for session changes
  claude-agent watch

  # Check Claude CLI installation
  claude-agent check
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # -------------------------------------------------------------------------
    # run - Execute a single agent
    # -------------------------------------------------------------------------
    run_parser = subparsers.add_parser(
        'run',
        help='Execute a single agent prompt',
        description='Execute a prompt using Claude Code CLI'
    )
    run_parser.add_argument(
        'prompt',
        type=str,
        help='The prompt to send to Claude'
    )
    run_parser.add_argument(
        '--cwd',
        type=str,
        default=os.getcwd(),
        help='Working directory (default: current directory)'
    )
    run_parser.add_argument(
        '--stream',
        action='store_true',
        help='Stream output tokens in real-time'
    )
    run_parser.add_argument(
        '--resume',
        type=str,
        metavar='SESSION_ID',
        help='Resume a Claude session ID'
    )
    run_parser.add_argument(
        '--model',
        type=str,
        help='Model to use (e.g., claude-opus-4-5-20251101)'
    )
    run_parser.add_argument(
        '--max-turns',
        type=int,
        help='Maximum conversation turns'
    )
    run_parser.add_argument(
        '--read-only',
        action='store_true',
        help='Read-only mode (--permission-mode plan)'
    )
    run_parser.add_argument(
        '--timeout',
        type=float,
        default=120.0,
        help='Timeout in seconds (default: 120)'
    )
    run_parser.add_argument(
        '--json',
        action='store_true',
        help='Output result as JSON'
    )

    # -------------------------------------------------------------------------
    # sessions - Manage sessions
    # -------------------------------------------------------------------------
    sessions_parser = subparsers.add_parser(
        'sessions',
        help='Manage Claude agent sessions',
        description='List, show, and delete Claude agent sessions'
    )
    sessions_subparsers = sessions_parser.add_subparsers(
        dest='sessions_command',
        help='Sessions subcommand'
    )

    # sessions list
    list_parser = sessions_subparsers.add_parser(
        'list',
        help='List all sessions'
    )
    list_parser.add_argument(
        '--cwd',
        type=str,
        default=os.getcwd(),
        help='Working directory (default: current directory)'
    )
    list_parser.add_argument(
        '--state',
        type=str,
        choices=['idle', 'busy', 'error', 'closed'],
        help='Filter by session state'
    )

    # sessions show
    show_parser = sessions_subparsers.add_parser(
        'show',
        help='Show session details'
    )
    show_parser.add_argument(
        'session_id',
        type=str,
        help='Session ID to show'
    )

    # sessions delete
    delete_parser = sessions_subparsers.add_parser(
        'delete',
        help='Delete a session'
    )
    delete_parser.add_argument(
        'session_id',
        type=str,
        help='Session ID to delete'
    )

    # -------------------------------------------------------------------------
    # watch - Watch session files
    # -------------------------------------------------------------------------
    watch_parser = subparsers.add_parser(
        'watch',
        help='Watch session files for changes',
        description='Monitor Claude session files for changes'
    )
    watch_parser.add_argument(
        '--cwd',
        type=str,
        default=os.getcwd(),
        help='Working directory (default: current directory)'
    )
    watch_parser.add_argument(
        '--interval',
        type=float,
        default=1.0,
        help='Poll interval in seconds (default: 1.0)'
    )

    # -------------------------------------------------------------------------
    # check - Check Claude CLI installation
    # -------------------------------------------------------------------------
    check_parser = subparsers.add_parser(
        'check',
        help='Check Claude CLI installation',
        description='Check if Claude Code CLI is installed and available'
    )

    # -------------------------------------------------------------------------
    # skillchain - Execute skillchains
    # -------------------------------------------------------------------------
    if SKILLCHAIN_AVAILABLE:
        skillchain_parser = subparsers.add_parser(
            'skillchain',
            help='Execute skillchain workflows',
            description='Execute multi-skill workflows using delegated agents'
        )
        skillchain_subparsers = skillchain_parser.add_subparsers(
            dest='skillchain_command',
            help='Skillchain subcommand'
        )

        # skillchain run
        sc_run_parser = skillchain_subparsers.add_parser(
            'run',
            help='Execute a skillchain'
        )
        sc_run_parser.add_argument(
            'goal',
            type=str,
            help='Goal description (e.g., "dashboard with charts")'
        )
        sc_run_parser.add_argument(
            '--project',
            type=str,
            default=os.getcwd(),
            help='Project directory (default: current directory)'
        )
        sc_run_parser.add_argument(
            '--blueprint',
            type=str,
            help='Blueprint to use (dashboard, crud-api, rag-pipeline, etc.)'
        )
        sc_run_parser.add_argument(
            '--maturity',
            type=str,
            choices=['starter', 'intermediate', 'advanced'],
            default='intermediate',
            help='Skill detail level (default: intermediate)'
        )
        sc_run_parser.add_argument(
            '--repo',
            type=str,
            help='Path to ai-design-components repo (auto-detected if not set)'
        )

        # skillchain route
        sc_route_parser = skillchain_subparsers.add_parser(
            'route',
            help='Preview skill routing without executing'
        )
        sc_route_parser.add_argument(
            'goal',
            type=str,
            help='Goal description to route'
        )
        sc_route_parser.add_argument(
            '--repo',
            type=str,
            help='Path to ai-design-components repo'
        )

        # skillchain resume
        sc_resume_parser = skillchain_subparsers.add_parser(
            'resume',
            help='Resume an interrupted skillchain'
        )
        sc_resume_parser.add_argument(
            '--project',
            type=str,
            default=os.getcwd(),
            help='Project directory with .skillchain-progress.json'
        )
        sc_resume_parser.add_argument(
            '--repo',
            type=str,
            help='Path to ai-design-components repo'
        )

        # skillchain status
        sc_status_parser = skillchain_subparsers.add_parser(
            'status',
            help='Show skillchain progress'
        )
        sc_status_parser.add_argument(
            '--project',
            type=str,
            default=os.getcwd(),
            help='Project directory'
        )

        # skillchain blueprints
        sc_blueprints_parser = skillchain_subparsers.add_parser(
            'blueprints',
            help='List available blueprints'
        )

    return parser


async def cmd_run(args: argparse.Namespace) -> int:
    """Execute the 'run' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Create components
    emitter = EventEmitter()
    detector = AgentDetector()
    process_manager = ProcessManager(detector=detector, emitter=emitter)

    # Set up streaming handler if requested
    if args.stream:
        @emitter.on(EventType.MESSAGE_CHUNK)
        async def on_chunk(event):
            chunk = event.data.get('chunk', '')
            print(chunk, end='', flush=True)

    try:
        # Build process config
        config = ProcessConfig(
            prompt=args.prompt,
            cwd=args.cwd,
            resume_session_id=args.resume,
            model=args.model,
            max_turns=args.max_turns,
            read_only=args.read_only,
            timeout=args.timeout
        )

        # Execute
        result = await process_manager.execute(config)

        # Handle streaming output newline
        if args.stream and result.text:
            print()  # Newline after streaming

        # Handle errors
        if result.error:
            log(f"Error: {result.error}", "ERROR")
            if args.json:
                print(json.dumps({
                    "success": False,
                    "error": result.error,
                    "exit_code": result.exit_code
                }))
            return 1

        # Output results
        if args.json:
            output = {
                "success": True,
                "text": result.text,
                "session_id": result.session_id,
                "claude_session_id": result.claude_session_id,
                "usage": {
                    "input_tokens": result.usage.input_tokens,
                    "output_tokens": result.usage.output_tokens,
                    "total_cost_usd": result.usage.total_cost_usd
                },
                "duration_seconds": result.duration_seconds
            }
            print(json.dumps(output, indent=2))
        else:
            # Print response text (if not streaming)
            if not args.stream:
                print(result.text)

            # Print summary
            print()
            cost_str = f"${result.usage.total_cost_usd:.4f}"
            tokens_str = f"{result.usage.input_tokens} in, {result.usage.output_tokens} out"
            session_str = result.claude_session_id[:10] + "..." if result.claude_session_id else "N/A"

            print(f"{Colors.CYAN}Cost:{Colors.RESET} {cost_str} | "
                  f"{Colors.CYAN}Tokens:{Colors.RESET} {tokens_str} | "
                  f"{Colors.CYAN}Session:{Colors.RESET} {session_str}")

        return 0

    except KeyboardInterrupt:
        log("Interrupted by user", "WARNING")
        return 1
    except Exception as e:
        log(f"Unexpected error: {e}", "ERROR")
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}))
        return 1


async def cmd_sessions_list(args: argparse.Namespace) -> int:
    """Execute the 'sessions list' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Create watcher to list sessions
        watcher = SessionWatcher(args.cwd)
        sessions = watcher.list_sessions()

        # Filter by state if requested
        if args.state:
            state_map = {
                'idle': SessionState.IDLE,
                'busy': SessionState.BUSY,
                'error': SessionState.ERROR,
                'closed': SessionState.CLOSED
            }
            # Note: Watcher sessions don't have state, so we skip filtering for now
            # This would require integrating with SessionManager

        if not sessions:
            log(f"No sessions found in {args.cwd}", "INFO")
            return 0

        # Print header
        print(f"{Colors.BOLD}Sessions in {args.cwd}:{Colors.RESET}")
        print()

        # Sort by modification time (newest first)
        sessions.sort(key=lambda s: s.modified_at, reverse=True)

        # Print each session
        for session in sessions:
            # Format time ago
            now = datetime.now()
            delta = now - session.modified_at
            if delta.total_seconds() < 60:
                time_ago = f"{int(delta.total_seconds())}s ago"
            elif delta.total_seconds() < 3600:
                time_ago = f"{int(delta.total_seconds() / 60)}m ago"
            elif delta.total_seconds() < 86400:
                time_ago = f"{int(delta.total_seconds() / 3600)}h ago"
            else:
                time_ago = f"{int(delta.total_seconds() / 86400)}d ago"

            # Format first message
            first_msg = session.first_message or "N/A"
            if len(first_msg) > 60:
                first_msg = first_msg[:57] + "..."

            # Print session info
            session_id = session.session_id[:10] + "..."
            print(f"  {Colors.CYAN}{session_id}{Colors.RESET} "
                  f"({Colors.YELLOW}{time_ago}{Colors.RESET}) - "
                  f'"{first_msg}"')

        return 0

    except Exception as e:
        log(f"Error listing sessions: {e}", "ERROR")
        return 1


async def cmd_sessions_show(args: argparse.Namespace) -> int:
    """Execute the 'sessions show' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        manager = SessionManager()
        session = manager.get_session(args.session_id)

        if not session:
            log(f"Session not found: {args.session_id}", "ERROR")
            return 1

        # Print session details
        print(f"{Colors.BOLD}Session: {session.id}{Colors.RESET}")
        print(f"  State: {session.state.name}")
        print(f"  CWD: {session.cwd}")
        print(f"  Claude Session ID: {session.claude_session_id or 'N/A'}")
        print(f"  Created: {session.created_at.isoformat()}")
        print(f"  Updated: {session.updated_at.isoformat()}")
        print(f"  Messages: {len(session.messages)}")
        print(f"  Cost: ${session.total_cost_usd:.4f}")
        print(f"  Tokens: {session.total_input_tokens} in, {session.total_output_tokens} out")

        if session.metadata:
            print(f"  Metadata: {json.dumps(session.metadata, indent=4)}")

        # Print message history
        if session.messages:
            print(f"\n{Colors.BOLD}Message History:{Colors.RESET}")
            for i, msg in enumerate(session.messages, 1):
                role_color = Colors.GREEN if msg.role == 'assistant' else Colors.BLUE
                print(f"\n  {role_color}[{msg.role}]{Colors.RESET}")

                # Truncate long messages
                content = msg.content
                if len(content) > 200:
                    content = content[:197] + "..."

                print(f"  {content}")

        return 0

    except Exception as e:
        log(f"Error showing session: {e}", "ERROR")
        return 1


async def cmd_sessions_delete(args: argparse.Namespace) -> int:
    """Execute the 'sessions delete' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        manager = SessionManager()

        if manager.delete_session(args.session_id):
            log(f"Session deleted: {args.session_id}", "SUCCESS")
            return 0
        else:
            log(f"Session not found: {args.session_id}", "ERROR")
            return 1

    except Exception as e:
        log(f"Error deleting session: {e}", "ERROR")
        return 1


async def cmd_watch(args: argparse.Namespace) -> int:
    """Execute the 'watch' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Create emitter and watcher
        emitter = EventEmitter()
        watcher = SessionWatcher(
            cwd=args.cwd,
            emitter=emitter,
            poll_interval=args.interval
        )

        # Set up event handlers
        @emitter.on(EventType.FILE_CREATED)
        async def on_created(event):
            session_id = event.data.get('session_id', 'unknown')[:10] + "..."
            first_msg = event.data.get('first_message', 'N/A')
            if len(first_msg) > 60:
                first_msg = first_msg[:57] + "..."

            log(f"New session: {session_id} - \"{first_msg}\"", "SUCCESS")

        @emitter.on(EventType.FILE_MODIFIED)
        async def on_modified(event):
            session_id = event.data.get('session_id', 'unknown')[:10] + "..."
            msg_count = event.data.get('message_count', 0)

            log(f"Updated: {session_id} ({msg_count} messages)", "INFO")

        @emitter.on(EventType.FILE_DELETED)
        async def on_deleted(event):
            session_id = event.data.get('session_id', 'unknown')[:10] + "..."

            log(f"Deleted: {session_id}", "WARNING")

        # Start watching
        log(f"Watching sessions in {args.cwd} (poll interval: {args.interval}s)", "INFO")
        log("Press Ctrl+C to stop", "INFO")
        print()

        await watcher.start()

        # Keep running until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print()
            log("Stopping watcher...", "INFO")

        await watcher.stop()
        return 0

    except Exception as e:
        log(f"Error watching sessions: {e}", "ERROR")
        return 1


async def cmd_check(args: argparse.Namespace) -> int:
    """Execute the 'check' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        detector = AgentDetector()
        detection = await detector.detect()

        print(f"{Colors.BOLD}Claude Code CLI Status{Colors.RESET}")
        print()

        if detection.available:
            log(f"Claude Code CLI: {detection.path}", "SUCCESS")
            if detection.version:
                log(f"Version: {detection.version}", "INFO")
            log("Status: Ready", "SUCCESS")
            return 0
        else:
            log("Claude Code CLI: Not found", "ERROR")
            if detection.error:
                print()
                print(detection.error)
            log("Status: Not available", "ERROR")
            return 1

    except Exception as e:
        log(f"Error checking installation: {e}", "ERROR")
        return 1


# -------------------------------------------------------------------------
# Skillchain Commands
# -------------------------------------------------------------------------

def _find_repo_root(start_path: str = None) -> Optional[str]:
    """Find ai-design-components repo root by looking for CLAUDE.md."""
    start = Path(start_path) if start_path else Path.cwd()

    # Check current and parent directories
    for path in [start] + list(start.parents):
        if (path / "CLAUDE.md").exists() and (path / ".claude-commands").exists():
            return str(path)

    return None


async def cmd_skillchain_run(args: argparse.Namespace) -> int:
    """Execute the 'skillchain run' command."""
    try:
        # Find repo root
        repo_root = args.repo or _find_repo_root()
        if not repo_root:
            log("Could not find ai-design-components repo. Use --repo to specify.", "ERROR")
            return 1

        log(f"Using repo: {repo_root}", "INFO")
        log(f"Goal: {args.goal}", "INFO")
        if args.blueprint:
            log(f"Blueprint: {args.blueprint}", "INFO")
        print()

        # Create executor
        executor = SkillchainExecutor(repo_root)

        # Callbacks for progress
        def on_skill_start(skill, index, total):
            log(f"[{index + 1}/{total}] Starting: {skill.name}", "INFO")

        def on_skill_complete(result, index, total):
            if result.success:
                log(f"[{index + 1}/{total}] Complete: {result.skill_name} "
                    f"(${result.cost_usd:.4f})", "SUCCESS")
                if result.files_created:
                    for f in result.files_created[:3]:
                        print(f"    {Colors.CYAN}+{Colors.RESET} {f}")
                    if len(result.files_created) > 3:
                        print(f"    ... and {len(result.files_created) - 3} more")
            else:
                log(f"[{index + 1}/{total}] Failed: {result.skill_name} - {result.error}", "ERROR")

        # Execute
        result = await executor.execute(
            goal=args.goal,
            project_path=args.project,
            blueprint=args.blueprint,
            maturity=args.maturity,
            on_skill_start=on_skill_start,
            on_skill_complete=on_skill_complete,
        )

        # Summary
        print()
        print(f"{Colors.BOLD}Skillchain Complete{Colors.RESET}")
        print(f"  Skills: {result.skills_completed}/{result.skills_planned} completed")
        print(f"  Activation Rate: {result.activation_rate * 100:.0f}%")
        print(f"  Total Cost: ${result.total_cost_usd:.4f}")
        print(f"  Duration: {result.total_duration_seconds:.1f}s")
        print(f"  Files Created: {len(result.total_files_created)}")

        if result.error:
            log(f"Error: {result.error}", "ERROR")
            return 1

        return 0 if result.skills_failed == 0 else 1

    except Exception as e:
        log(f"Error executing skillchain: {e}", "ERROR")
        return 1


async def cmd_skillchain_route(args: argparse.Namespace) -> int:
    """Execute the 'skillchain route' command."""
    try:
        repo_root = args.repo or _find_repo_root()
        if not repo_root:
            log("Could not find ai-design-components repo. Use --repo to specify.", "ERROR")
            return 1

        registry = RegistryManager(repo_root)
        route = registry.route_goal(args.goal)

        print(f"{Colors.BOLD}Skill Routing for:{Colors.RESET} {args.goal}")
        print()

        if route.blueprint:
            print(f"{Colors.CYAN}Detected Blueprint:{Colors.RESET} {route.blueprint} "
                  f"(confidence: {route.confidence * 100:.0f}%)")
            print()

        print(f"{Colors.CYAN}Detected Domains:{Colors.RESET}")
        for domain in route.domains:
            marker = "*" if domain == route.primary_domain else " "
            print(f"  {marker} {domain}")
        print()

        print(f"{Colors.CYAN}Matched Skills ({len(route.matched_skills)}):{Colors.RESET}")
        for i, skill in enumerate(route.matched_skills, 1):
            print(f"  {i}. {Colors.GREEN}{skill.name}{Colors.RESET}")
            print(f"     Invocation: {skill.invocation}")
            if skill.dependencies:
                print(f"     Dependencies: {', '.join(skill.dependencies)}")
        print()

        exec_mode = "delegated" if len(route.matched_skills) >= 4 else "standard"
        print(f"{Colors.CYAN}Execution Mode:{Colors.RESET} {exec_mode}")

        return 0

    except Exception as e:
        log(f"Error routing goal: {e}", "ERROR")
        return 1


async def cmd_skillchain_resume(args: argparse.Namespace) -> int:
    """Execute the 'skillchain resume' command."""
    try:
        repo_root = args.repo or _find_repo_root()
        if not repo_root:
            log("Could not find ai-design-components repo. Use --repo to specify.", "ERROR")
            return 1

        progress_mgr = ProgressManager()
        progress = progress_mgr.load(args.project)

        if not progress:
            log(f"No progress file found in {args.project}", "ERROR")
            return 1

        remaining = progress_mgr.get_resumable_skills(progress)
        if not remaining:
            log("No skills remaining to execute", "INFO")
            return 0

        log(f"Resuming skillchain: {progress.goal}", "INFO")
        log(f"Remaining skills: {len(remaining)}", "INFO")
        print()

        executor = SkillchainExecutor(repo_root)

        def on_skill_start(skill, index, total):
            log(f"[{index + 1}/{total}] Starting: {skill.name}", "INFO")

        def on_skill_complete(result, index, total):
            if result.success:
                log(f"[{index + 1}/{total}] Complete: {result.skill_name}", "SUCCESS")
            else:
                log(f"[{index + 1}/{total}] Failed: {result.skill_name}", "ERROR")

        result = await executor.resume(
            project_path=args.project,
            on_skill_start=on_skill_start,
            on_skill_complete=on_skill_complete,
        )

        print()
        print(f"{Colors.BOLD}Resume Complete{Colors.RESET}")
        print(f"  Skills: {result.skills_completed}/{result.skills_planned}")

        return 0 if result.skills_failed == 0 else 1

    except Exception as e:
        log(f"Error resuming skillchain: {e}", "ERROR")
        return 1


async def cmd_skillchain_status(args: argparse.Namespace) -> int:
    """Execute the 'skillchain status' command."""
    try:
        progress_mgr = ProgressManager()
        progress = progress_mgr.load(args.project)

        if not progress:
            log(f"No skillchain in progress at {args.project}", "INFO")
            return 0

        print(f"{Colors.BOLD}Skillchain Status{Colors.RESET}")
        print()
        print(f"  Goal: {progress.goal}")
        print(f"  Blueprint: {progress.blueprint or 'None'}")
        print(f"  Maturity: {progress.maturity}")
        print(f"  Mode: {progress.execution.mode}")
        print(f"  Started: {progress.started_at}")
        print(f"  Updated: {progress.updated_at}")
        print()

        print(f"{Colors.BOLD}Skills ({progress.execution.total_skills}):{Colors.RESET}")
        for i, skill in enumerate(progress.skills):
            if skill.status == "complete":
                status_icon = f"{Colors.GREEN}[x]{Colors.RESET}"
            elif skill.status == "running":
                status_icon = f"{Colors.YELLOW}[>]{Colors.RESET}"
            elif skill.status == "failed":
                status_icon = f"{Colors.RED}[!]{Colors.RESET}"
            else:
                status_icon = "[ ]"

            print(f"  {status_icon} {skill.name}")
            if skill.files_created:
                print(f"       Files: {len(skill.files_created)}")

        print()
        print(f"  Completed: {progress.execution.completed_count}")
        print(f"  Failed: {progress.execution.failed_count}")
        print(f"  Remaining: {len(progress_mgr.get_resumable_skills(progress))}")
        print(f"  Activation Rate: {progress.execution.activation_rate * 100:.0f}%")

        return 0

    except Exception as e:
        log(f"Error getting status: {e}", "ERROR")
        return 1


async def cmd_skillchain_blueprints(args: argparse.Namespace) -> int:
    """Execute the 'skillchain blueprints' command."""
    print(f"{Colors.BOLD}Available Blueprints:{Colors.RESET}")
    print()

    blueprints = {
        "dashboard": "UI dashboard with charts, tables, KPI cards",
        "crud-api": "REST API with database and authentication",
        "rag-pipeline": "RAG pipeline with vector DB and embeddings",
        "ci-cd": "CI/CD pipeline with GitHub Actions",
        "k8s": "Kubernetes deployment with Helm",
        "security": "Security hardening and compliance",
        "observability": "Monitoring, logging, and tracing",
        "data-pipeline": "ETL/ELT data pipeline",
        "ml-pipeline": "MLOps pipeline for model training",
        "cloud": "Cloud infrastructure (AWS/GCP/Azure)",
        "cost": "FinOps cost optimization",
        "api-first": "API-first design with OpenAPI",
    }

    for name, desc in blueprints.items():
        print(f"  {Colors.CYAN}{name}{Colors.RESET}")
        print(f"    {desc}")
        print()

    return 0


def main():
    """Main CLI entry point (called by `claude-agent` command)."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle no command
    if not args.command:
        parser.print_help()
        return 0

    # Route to appropriate command handler
    try:
        if args.command == 'run':
            exit_code = asyncio.run(cmd_run(args))
        elif args.command == 'sessions':
            if not args.sessions_command:
                parser.parse_args(['sessions', '--help'])
                return 0

            if args.sessions_command == 'list':
                exit_code = asyncio.run(cmd_sessions_list(args))
            elif args.sessions_command == 'show':
                exit_code = asyncio.run(cmd_sessions_show(args))
            elif args.sessions_command == 'delete':
                exit_code = asyncio.run(cmd_sessions_delete(args))
            else:
                parser.print_help()
                exit_code = 1
        elif args.command == 'watch':
            exit_code = asyncio.run(cmd_watch(args))
        elif args.command == 'check':
            exit_code = asyncio.run(cmd_check(args))
        elif args.command == 'skillchain' and SKILLCHAIN_AVAILABLE:
            if not args.skillchain_command:
                parser.parse_args(['skillchain', '--help'])
                return 0

            if args.skillchain_command == 'run':
                exit_code = asyncio.run(cmd_skillchain_run(args))
            elif args.skillchain_command == 'route':
                exit_code = asyncio.run(cmd_skillchain_route(args))
            elif args.skillchain_command == 'resume':
                exit_code = asyncio.run(cmd_skillchain_resume(args))
            elif args.skillchain_command == 'status':
                exit_code = asyncio.run(cmd_skillchain_status(args))
            elif args.skillchain_command == 'blueprints':
                exit_code = asyncio.run(cmd_skillchain_blueprints(args))
            else:
                parser.print_help()
                exit_code = 1
        else:
            parser.print_help()
            exit_code = 1

        sys.exit(exit_code)

    except KeyboardInterrupt:
        print()
        log("Interrupted", "WARNING")
        sys.exit(1)
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        sys.exit(1)


if __name__ == '__main__':
    main()
