# Claude Agent Manager CLI

Command-line interface for managing Claude agent sessions and executing prompts.

## Installation

The CLI is installed as part of the `claude-agent-manager` package:

```bash
pip install claude-agent-manager
```

This installs the `claude-agent` command globally.

## Commands

### `run` - Execute a single agent

Execute a prompt using Claude Code CLI.

```bash
# Basic execution
claude-agent run "Write a hello world program"

# With custom working directory
claude-agent run "Explain this code" --cwd /path/to/project

# Stream output in real-time
claude-agent run "Add tests" --stream

# Resume a previous Claude session
claude-agent run "Continue working" --resume abc123def456

# Specify model
claude-agent run "Analyze code" --model claude-opus-4-5-20251101

# Read-only mode (no file modifications)
claude-agent run "Review the codebase" --read-only

# JSON output
claude-agent run "Calculate sum" --json

# Custom timeout
claude-agent run "Long task" --timeout 300
```

**Options:**
- `prompt` (required) - The prompt to send to Claude
- `--cwd PATH` - Working directory (default: current directory)
- `--stream` - Stream output tokens in real-time
- `--resume SESSION_ID` - Resume a Claude session ID
- `--model MODEL` - Model to use (e.g., claude-opus-4-5-20251101)
- `--max-turns N` - Maximum conversation turns
- `--read-only` - Read-only mode (--permission-mode plan)
- `--timeout SECONDS` - Timeout in seconds (default: 120)
- `--json` - Output result as JSON

**Example Output:**

```
$ claude-agent run "Say hello"
Hello! How can I help you today?

Cost: $0.0023 | Tokens: 150 in, 45 out | Session: abc123...
```

### `sessions` - Manage sessions

Manage Claude agent sessions stored locally.

#### `sessions list` - List all sessions

```bash
# List all sessions in current directory
claude-agent sessions list

# List sessions in specific directory
claude-agent sessions list --cwd /path/to/project

# Filter by state
claude-agent sessions list --state idle
claude-agent sessions list --state busy
```

**Example Output:**

```
$ claude-agent sessions list
Sessions in /my/project:
  abc123... (2m ago) - "Write hello world"
  def456... (1h ago) - "Add tests"
  ghi789... (2d ago) - "Explain this code"
```

#### `sessions show` - Show session details

```bash
claude-agent sessions show abc123def456
```

**Example Output:**

```
$ claude-agent sessions show session_abc123
Session: session_abc123
  State: IDLE
  CWD: /Users/user/project
  Claude Session ID: abc123def456
  Created: 2025-12-10T12:00:00
  Updated: 2025-12-10T12:05:00
  Messages: 4
  Cost: $0.0156
  Tokens: 1200 in, 350 out

Message History:

  [user]
  Write a hello world program

  [assistant]
  Here's a simple hello world program in Python:
  ...
```

#### `sessions delete` - Delete a session

```bash
claude-agent sessions delete abc123def456
```

### `watch` - Watch session files

Monitor Claude session files for changes in real-time.

```bash
# Watch current directory
claude-agent watch

# Watch specific directory
claude-agent watch --cwd /path/to/project

# Custom poll interval
claude-agent watch --interval 2.0
```

**Options:**
- `--cwd PATH` - Working directory (default: current directory)
- `--interval SECONDS` - Poll interval in seconds (default: 1.0)

**Example Output:**

```
$ claude-agent watch
[INFO] Watching sessions in /my/project (poll interval: 1.0s)
[INFO] Press Ctrl+C to stop

[SUCCESS] New session: abc123... - "Write a hello world program"
[INFO] Updated: abc123... (2 messages)
[INFO] Updated: abc123... (4 messages)
```

### `check` - Check Claude CLI installation

Verify that Claude Code CLI is installed and accessible.

```bash
claude-agent check
```

**Example Output (Success):**

```
$ claude-agent check
Claude Code CLI Status

[SUCCESS] Claude Code CLI: /Users/user/.local/bin/claude
[INFO] Version: 2.0.64 (Claude Code)
[SUCCESS] Status: Ready
```

**Example Output (Not Found):**

```
$ claude-agent check
Claude Code CLI Status

[ERROR] Claude Code CLI: Not found

claude CLI not found. Please install it:
  npm install -g @anthropic-ai/claude-code
  # or
  brew install claude-code

Then authenticate:
  claude login

[ERROR] Status: Not available
```

## Exit Codes

All commands follow standard Unix exit code conventions:

- `0` - Success
- `1` - Error

## Environment

The CLI uses the following environment conventions:

- Removes `ANTHROPIC_API_KEY` to ensure OAuth authentication
- Expands `PATH` to include common Claude installation locations
- Uses current working directory as default for `--cwd`

## Integration

The CLI can be integrated into scripts and automation:

```bash
#!/bin/bash

# Run analysis and capture JSON output
RESULT=$(claude-agent run "Analyze this code" --json)

# Extract cost
COST=$(echo "$RESULT" | jq -r '.usage.total_cost_usd')

echo "Analysis cost: \$${COST}"
```

## Programmatic Usage

The CLI can also be used programmatically:

```python
from claude_agent_manager.cli.main import main
import sys

# Run CLI with arguments
sys.argv = ['claude-agent', 'run', 'Hello world']
main()
```
