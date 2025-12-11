"""Process management for Claude Code CLI execution.

This module provides process management functionality for spawning and controlling
Claude Code CLI processes. It handles argument building, environment setup, streaming
output parsing, and process lifecycle management.

Key features:
- Async process execution with streaming output
- Image input support via stream-json format
- Session continuity with --resume
- Process interruption and cleanup
- Event emission for process lifecycle
- Usage tracking and statistics
"""

import asyncio
import json
import os
import signal
import time
from dataclasses import dataclass, field
from typing import AsyncIterator, Dict, List, Optional

from .detector import AgentDetector
from .events import Event, EventEmitter, EventType
from .parser import ParsedMessage, StreamJsonParser, UsageStats


@dataclass
class ProcessConfig:
    """Configuration for spawning a Claude Code CLI process.

    Attributes:
        prompt: User prompt to send to Claude
        cwd: Working directory for the process (default: current directory)
        session_id: Our internal session ID for tracking
        resume_session_id: Claude's session ID for --resume continuation
        model: Model to use (e.g., 'claude-opus-4-5-20251101')
        max_turns: Maximum conversation turns
        system_prompt: Custom system prompt
        allowed_tools: List of allowed tool names
        disallowed_tools: List of disallowed tool names
        skip_permissions: Skip permission prompts (default: True)
        read_only: Run in read-only mode (--permission-mode plan)
        timeout: Process timeout in seconds (default: 120.0)
        images: List of base64 data URLs for image inputs
        env_overrides: Additional environment variables to set
    """
    prompt: str
    cwd: str = '.'
    session_id: Optional[str] = None
    resume_session_id: Optional[str] = None
    model: Optional[str] = None
    max_turns: Optional[int] = None
    system_prompt: Optional[str] = None
    allowed_tools: Optional[List[str]] = None
    disallowed_tools: Optional[List[str]] = None
    skip_permissions: bool = True
    read_only: bool = False
    timeout: float = 120.0
    images: Optional[List[str]] = None
    env_overrides: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProcessResult:
    """Result of a Claude Code CLI process execution.

    Attributes:
        session_id: Our internal session ID
        claude_session_id: Claude's session ID (for future --resume)
        text: Complete response text from Claude
        exit_code: Process exit code
        usage: Token usage and cost statistics
        duration_seconds: Total execution time
        error: Error message if execution failed
    """
    session_id: str
    claude_session_id: Optional[str]
    text: str
    exit_code: int
    usage: UsageStats
    duration_seconds: float
    error: Optional[str] = None


class ProcessManager:
    """Manager for Claude Code CLI process execution.

    Handles process spawning, argument building, output parsing, and lifecycle management.
    Emits events for process state changes and integrates with the event system.

    Usage:
        >>> detector = AgentDetector()
        >>> emitter = EventEmitter()
        >>> manager = ProcessManager(detector, emitter)
        >>>
        >>> config = ProcessConfig(
        ...     prompt="Explain this code",
        ...     cwd="/path/to/project",
        ...     session_id="session-123"
        ... )
        >>>
        >>> result = await manager.execute(config)
        >>> print(result.text)
        >>> print(f"Cost: ${result.usage.total_cost_usd}")
    """

    def __init__(
        self,
        detector: Optional[AgentDetector] = None,
        emitter: Optional[EventEmitter] = None
    ):
        """Initialize the process manager.

        Args:
            detector: AgentDetector for binary location (creates new if None)
            emitter: EventEmitter for lifecycle events (creates new if None)
        """
        self.detector = detector or AgentDetector()
        self.emitter = emitter or EventEmitter()
        self._active_processes: Dict[str, asyncio.subprocess.Process] = {}

    def _build_args(self, config: ProcessConfig) -> List[str]:
        """Build command-line arguments for Claude Code CLI.

        Args:
            config: Process configuration

        Returns:
            List of command-line arguments
        """
        args = [
            '--print',                    # Batch mode (exit after response)
            '--verbose',                  # Detailed output
            '--output-format', 'stream-json'  # JSONL output for parsing
        ]

        # Permission handling
        if config.skip_permissions:
            args.append('--dangerously-skip-permissions')

        if config.read_only:
            args.extend(['--permission-mode', 'plan'])

        # Session resumption
        if config.resume_session_id:
            args.extend(['--resume', config.resume_session_id])

        # Model selection
        if config.model:
            args.extend(['--model', config.model])

        # Max turns
        if config.max_turns is not None:
            args.extend(['--max-turns', str(config.max_turns)])

        # System prompt
        if config.system_prompt:
            args.extend(['--system-prompt', config.system_prompt])

        # Allowed tools
        if config.allowed_tools:
            args.extend(['--allowedTools', ','.join(config.allowed_tools)])

        # Disallowed tools
        if config.disallowed_tools:
            args.extend(['--disallowedTools', ','.join(config.disallowed_tools)])

        # Image input requires stream-json format
        if config.images:
            args.extend(['--input-format', 'stream-json'])
        else:
            # Prompt as positional argument
            args.extend(['--', config.prompt])

        return args

    def _build_env(self, config: ProcessConfig) -> Dict[str, str]:
        """Build environment variables for the process.

        Removes ANTHROPIC_API_KEY to ensure OAuth authentication is used.

        Args:
            config: Process configuration

        Returns:
            Environment dictionary
        """
        env = self.detector.get_env_with_expanded_path()

        # Remove API key to force OAuth authentication
        env.pop('ANTHROPIC_API_KEY', None)

        # Apply overrides
        env.update(config.env_overrides)

        return env

    def _build_image_message(self, prompt: str, images: List[str]) -> str:
        """Build stream-json message with image attachments.

        Args:
            prompt: Text prompt
            images: List of base64 data URLs (e.g., 'data:image/png;base64,...')

        Returns:
            JSON string in stream-json format
        """
        content = []

        # Add images first
        for data_url in images:
            # Parse data URL: data:image/png;base64,<data>
            if data_url.startswith('data:'):
                try:
                    # Split on comma to get media type and data
                    header, base64_data = data_url.split(',', 1)
                    # Extract media type from header
                    media_type = header.split(';')[0].replace('data:', '')

                    content.append({
                        'type': 'image',
                        'source': {
                            'type': 'base64',
                            'media_type': media_type,
                            'data': base64_data
                        }
                    })
                except (ValueError, IndexError):
                    # Skip malformed data URLs
                    continue

        # Add text prompt last
        content.append({
            'type': 'text',
            'text': prompt
        })

        # Build stream-json message
        message = {
            'type': 'user',
            'message': {
                'role': 'user',
                'content': content
            }
        }

        return json.dumps(message)

    async def execute(self, config: ProcessConfig) -> ProcessResult:
        """Execute a Claude Code CLI process and wait for completion.

        Args:
            config: Process configuration

        Returns:
            ProcessResult with execution outcome

        Raises:
            RuntimeError: If Claude binary is not available
            TimeoutError: If process exceeds timeout
        """
        # Detect binary
        detection = await self.detector.detect()
        if not detection.available:
            raise RuntimeError(
                f"Claude Code CLI not available: {detection.error}"
            )

        # Build arguments and environment
        args = self._build_args(config)
        env = self._build_env(config)

        # Session ID for tracking
        session_id = config.session_id or f"process-{int(time.time())}"

        # Start timing
        start_time = time.time()

        # Spawn process
        try:
            process = await asyncio.create_subprocess_exec(
                detection.path,
                *args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=config.cwd,
                env=env
            )

            # Track active process
            self._active_processes[session_id] = process

            # Emit process spawned event
            await self.emitter.emit(Event(
                type=EventType.PROCESS_SPAWNED,
                session_id=session_id,
                data={
                    'pid': process.pid,
                    'cwd': config.cwd,
                    'args': args
                }
            ))

            # Handle image input
            if config.images:
                image_message = self._build_image_message(config.prompt, config.images)
                process.stdin.write((image_message + '\n').encode('utf-8'))
                await process.stdin.drain()

            # Close stdin
            process.stdin.close()

            # Collect output
            parser = StreamJsonParser(session_id=session_id, emitter=self.emitter)
            claude_session_id = None
            response_text = ''

            # Read stdout with timeout
            try:
                async def read_output():
                    nonlocal claude_session_id, response_text

                    # Read in chunks to avoid line length limits
                    # readline() has a 64KB default limit which Claude's output can exceed
                    buffer = ""
                    while True:
                        try:
                            # Read chunks instead of lines to handle long outputs
                            chunk = await process.stdout.read(8192)
                            if not chunk:
                                break

                            buffer += chunk.decode('utf-8')

                            # Process complete lines from buffer
                            while '\n' in buffer:
                                line, buffer = buffer.split('\n', 1)
                                if line.strip():
                                    messages = await parser.process_chunk(line + '\n')
                                    for msg in messages:
                                        if msg.session_id and not claude_session_id:
                                            claude_session_id = msg.session_id
                                        if msg.result:
                                            response_text = msg.result
                        except Exception as read_err:
                            # Log but continue on read errors
                            break

                    # Process any remaining buffer content
                    if buffer.strip():
                        messages = await parser.process_chunk(buffer)
                        for msg in messages:
                            if msg.session_id and not claude_session_id:
                                claude_session_id = msg.session_id
                            if msg.result:
                                response_text = msg.result

                    # Flush any remaining parser buffer
                    final_msg = await parser.flush()
                    if final_msg:
                        if final_msg.session_id and not claude_session_id:
                            claude_session_id = final_msg.session_id
                        if final_msg.result:
                            response_text = final_msg.result

                await asyncio.wait_for(read_output(), timeout=config.timeout)

            except asyncio.TimeoutError:
                # Kill process on timeout
                process.kill()
                await process.wait()

                duration = time.time() - start_time

                # Emit timeout error event
                await self.emitter.emit(Event(
                    type=EventType.SESSION_ERROR,
                    session_id=session_id,
                    data={'error': f'Process timed out after {config.timeout}s'}
                ))

                return ProcessResult(
                    session_id=session_id,
                    claude_session_id=claude_session_id,
                    text=response_text,
                    exit_code=-1,
                    usage=parser.usage,
                    duration_seconds=duration,
                    error=f'Process timed out after {config.timeout}s'
                )

            # Wait for process to complete
            exit_code = await process.wait()
            duration = time.time() - start_time

            # Read stderr
            stderr = await process.stderr.read()
            stderr_text = stderr.decode('utf-8').strip() if stderr else None

            # Get final usage from parser
            usage = parser.usage

            # Emit process exit event
            await self.emitter.emit(Event(
                type=EventType.PROCESS_EXIT,
                session_id=session_id,
                data={
                    'exit_code': exit_code,
                    'duration_seconds': duration,
                    'stderr': stderr_text
                }
            ))

            # Emit session complete or error
            if exit_code == 0:
                await self.emitter.emit(Event(
                    type=EventType.SESSION_COMPLETE,
                    session_id=session_id,
                    data={
                        'claude_session_id': claude_session_id,
                        'duration_seconds': duration,
                        'usage': usage.to_dict()
                    }
                ))
            else:
                error_msg = stderr_text or f'Process exited with code {exit_code}'
                await self.emitter.emit(Event(
                    type=EventType.SESSION_ERROR,
                    session_id=session_id,
                    data={'error': error_msg, 'exit_code': exit_code}
                ))

            return ProcessResult(
                session_id=session_id,
                claude_session_id=claude_session_id,
                text=response_text,
                exit_code=exit_code,
                usage=usage,
                duration_seconds=duration,
                error=stderr_text if exit_code != 0 else None
            )

        except Exception as e:
            duration = time.time() - start_time

            # Emit error event
            await self.emitter.emit(Event(
                type=EventType.SESSION_ERROR,
                session_id=session_id,
                data={'error': str(e)}
            ))

            return ProcessResult(
                session_id=session_id,
                claude_session_id=None,
                text='',
                exit_code=-1,
                usage=UsageStats(),
                duration_seconds=duration,
                error=str(e)
            )

        finally:
            # Remove from active processes
            self._active_processes.pop(session_id, None)

    async def execute_streaming(self, config: ProcessConfig) -> AsyncIterator[str]:
        """Execute a Claude Code CLI process with streaming output.

        Yields response text as it becomes available. Useful for real-time UI updates.

        Args:
            config: Process configuration

        Yields:
            Response text chunks

        Raises:
            RuntimeError: If Claude binary is not available
        """
        # Detect binary
        detection = await self.detector.detect()
        if not detection.available:
            raise RuntimeError(
                f"Claude Code CLI not available: {detection.error}"
            )

        # Build arguments and environment
        args = self._build_args(config)
        env = self._build_env(config)

        # Session ID for tracking
        session_id = config.session_id or f"process-{int(time.time())}"

        # Spawn process
        process = await asyncio.create_subprocess_exec(
            detection.path,
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=config.cwd,
            env=env
        )

        # Track active process
        self._active_processes[session_id] = process

        # Emit process spawned event
        await self.emitter.emit(Event(
            type=EventType.PROCESS_SPAWNED,
            session_id=session_id,
            data={'pid': process.pid, 'cwd': config.cwd, 'args': args}
        ))

        try:
            # Handle image input
            if config.images:
                image_message = self._build_image_message(config.prompt, config.images)
                process.stdin.write((image_message + '\n').encode('utf-8'))
                await process.stdin.drain()

            # Close stdin
            process.stdin.close()

            # Stream output
            parser = StreamJsonParser(session_id=session_id, emitter=self.emitter)
            claude_session_id = None
            buffer = ""

            # Read in chunks to avoid line length limits
            while True:
                try:
                    chunk = await process.stdout.read(8192)
                    if not chunk:
                        break

                    buffer += chunk.decode('utf-8')

                    # Process complete lines from buffer
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if line.strip():
                            messages = await parser.process_chunk(line + '\n')
                            for msg in messages:
                                if msg.session_id and not claude_session_id:
                                    claude_session_id = msg.session_id
                                if msg.result:
                                    yield msg.result
                except Exception:
                    break

            # Process remaining buffer
            if buffer.strip():
                messages = await parser.process_chunk(buffer)
                for msg in messages:
                    if msg.result:
                        yield msg.result

            # Wait for completion
            await process.wait()

        finally:
            # Remove from active processes
            self._active_processes.pop(session_id, None)

    async def interrupt(self, session_id: str, timeout: float = 5.0) -> bool:
        """Interrupt a running process gracefully.

        Sends SIGINT for graceful shutdown, then SIGTERM after timeout.

        Args:
            session_id: Session ID of the process to interrupt
            timeout: Seconds to wait before escalating to SIGTERM

        Returns:
            True if process was interrupted, False if not found
        """
        process = self._active_processes.get(session_id)
        if not process:
            return False

        try:
            # Send SIGINT for graceful shutdown
            process.send_signal(signal.SIGINT)

            # Wait for timeout
            try:
                await asyncio.wait_for(process.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                # Force kill with SIGTERM
                process.terminate()
                await process.wait()

            return True

        except ProcessLookupError:
            # Process already terminated
            return False

        finally:
            # Remove from active processes
            self._active_processes.pop(session_id, None)

    async def interrupt_all(self) -> int:
        """Interrupt all active processes.

        Returns:
            Number of processes interrupted
        """
        session_ids = list(self._active_processes.keys())
        count = 0

        for session_id in session_ids:
            if await self.interrupt(session_id):
                count += 1

        return count
