---
sidebar_position: 6
title: CLI Reference
description: Complete reference for the claude-agent command-line interface
---

# CLI Reference

The `claude-agent` command provides a command-line interface for managing and executing Claude agents.

## Installation

```bash
pip install claude-agent-manager
```

## Global Options

```bash
claude-agent --help
```

## Commands

### check

Check if Claude Code CLI is installed and available.

```bash
claude-agent check
```

**Output:**
```
Claude Code CLI Status

[SUCCESS] Claude Code CLI: /Users/you/.local/bin/claude
[INFO] Version: 2.0.64 (Claude Code)
[SUCCESS] Status: Ready
```

**Exit Codes:**
- `0` - Claude CLI found and ready
- `1` - Claude CLI not found or not working

---

### run

Execute a single agent prompt.

```bash
claude-agent run <prompt> [options]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `prompt` | Yes | The prompt to send to Claude |

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--cwd` | string | current dir | Working directory |
| `--stream` | flag | false | Stream output tokens in real-time |
| `--resume` | string | - | Resume a Claude session ID |
| `--model` | string | - | Model to use (e.g., claude-opus-4-5-20251101) |
| `--max-turns` | int | - | Maximum conversation turns |
| `--read-only` | flag | false | Read-only mode (--permission-mode plan) |
| `--timeout` | float | 120.0 | Timeout in seconds |
| `--json` | flag | false | Output result as JSON |

**Examples:**

```bash
# Simple prompt
claude-agent run "Explain recursion"

# With streaming output
claude-agent run "Write a sorting algorithm" --stream

# Resume previous session
claude-agent run "Add error handling" --resume abc123-def456

# Read-only mode for analysis
claude-agent run "Analyze the codebase" --read-only --cwd /project

# JSON output for scripting
claude-agent run "List all functions" --json | jq '.text'

# Custom timeout
claude-agent run "Complex refactoring task" --timeout 300
```

**Output (default):**
```
Hello! I'm ready to help you with your coding tasks.

Cost: $0.0209 | Tokens: 9 in, 35 out | Session: abc123de-f...
```

**Output (--json):**
```json
{
  "success": true,
  "text": "Hello! I'm ready to help you with your coding tasks.",
  "session_id": "process-1733840000",
  "claude_session_id": "abc123de-f456-7890-abcd-ef1234567890",
  "usage": {
    "input_tokens": 9,
    "output_tokens": 35,
    "total_cost_usd": 0.0209
  },
  "duration_seconds": 2.5
}
```

---

### sessions

Manage Claude agent sessions.

#### sessions list

List all sessions.

```bash
claude-agent sessions list [options]
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--cwd` | string | current dir | Working directory |
| `--state` | choice | - | Filter by state (idle, busy, error, closed) |

**Example:**
```bash
claude-agent sessions list --cwd /my/project
```

**Output:**
```
Sessions in /my/project:

  abc123de-f... (5m ago) - "Write a function..."
  def456gh-i... (1h ago) - "Review the code..."
  ghi789jk-l... (2d ago) - "Explain recursion..."
```

#### sessions show

Show session details.

```bash
claude-agent sessions show <session_id>
```

**Example:**
```bash
claude-agent sessions show abc123de-f456-7890
```

**Output:**
```
Session: abc123de-f456-7890
  State: IDLE
  CWD: /my/project
  Claude Session ID: abc123de-f456-7890-abcd-ef1234567890
  Created: 2025-12-10T10:00:00
  Updated: 2025-12-10T10:05:00
  Messages: 4
  Cost: $0.0832
  Tokens: 120 in, 450 out

Message History:

  [user]
  Write a function to calculate factorial

  [assistant]
  Here's a factorial function...
```

#### sessions delete

Delete a session.

```bash
claude-agent sessions delete <session_id>
```

**Example:**
```bash
claude-agent sessions delete abc123de-f456-7890
```

**Output:**
```
[SUCCESS] Session deleted: abc123de-f456-7890
```

---

### watch

Watch session files for changes.

```bash
claude-agent watch [options]
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--cwd` | string | current dir | Working directory |
| `--interval` | float | 1.0 | Poll interval in seconds |

**Example:**
```bash
claude-agent watch --cwd /my/project --interval 0.5
```

**Output:**
```
[INFO] Watching sessions in /my/project (poll interval: 0.5s)
[INFO] Press Ctrl+C to stop

[SUCCESS] New session: abc123de-f... - "Write a function..."
[INFO] Updated: abc123de-f... (5 messages)
[WARNING] Deleted: def456gh-i...
```

---

### skillchain

Execute skillchain workflows.

#### skillchain blueprints

List available blueprints.

```bash
claude-agent skillchain blueprints
```

**Output:**
```
Available Blueprints:

  dashboard
    UI dashboard with charts, tables, KPI cards

  crud-api
    REST API with database and authentication

  rag-pipeline
    RAG pipeline with vector DB and embeddings

  ci-cd
    CI/CD pipeline with GitHub Actions

  k8s
    Kubernetes deployment with Helm

  security
    Security hardening and compliance

  observability
    Monitoring, logging, and tracing

  data-pipeline
    ETL/ELT data pipeline

  ml-pipeline
    MLOps pipeline for model training

  cloud
    Cloud infrastructure (AWS/GCP/Azure)

  cost
    FinOps cost optimization

  api-first
    API-first design with OpenAPI
```

#### skillchain route

Preview skill routing without executing.

```bash
claude-agent skillchain route <goal> [options]
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--repo` | string | auto | Path to ai-design-components repo |

**Example:**
```bash
claude-agent skillchain route "dashboard with charts and postgres"
```

**Output:**
```
Skill Routing for: dashboard with charts and postgres

Detected Blueprint: dashboard (confidence: 75%)

Detected Domains:
  * frontend
    backend

Matched Skills (5):
  1. theming-components
     Invocation: ui-foundation-skills:theming-components
  2. visualizing-data
     Invocation: ui-data-skills:visualizing-data
     Dependencies: theming-components
  3. creating-dashboards
     Invocation: ui-data-skills:creating-dashboards
     Dependencies: theming-components, designing-layouts
  4. using-relational-databases
     Invocation: backend-data-skills:using-relational-databases
  5. assembling-components
     Invocation: ui-assembly-skills:assembling-components
     Dependencies: *

Execution Mode: delegated
```

#### skillchain run

Execute a skillchain.

```bash
claude-agent skillchain run <goal> [options]
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--project` | string | current dir | Project directory |
| `--blueprint` | string | - | Blueprint to use |
| `--maturity` | choice | intermediate | Skill detail level (starter, intermediate, advanced) |
| `--repo` | string | auto | Path to ai-design-components repo |

**Example:**
```bash
claude-agent skillchain run "Build a sales dashboard" \
  --project /my/project \
  --blueprint dashboard \
  --maturity intermediate
```

**Output:**
```
[INFO] Using repo: /path/to/ai-design-components
[INFO] Goal: Build a sales dashboard
[INFO] Blueprint: dashboard

[INFO] [1/5] Starting: theming-components
[SUCCESS] [1/5] Complete: theming-components ($0.0521)
    + src/tokens.css
    + src/theme.ts
[INFO] [2/5] Starting: designing-layouts
[SUCCESS] [2/5] Complete: designing-layouts ($0.0423)
    + src/layouts/DashboardLayout.tsx
...

Skillchain Complete
  Skills: 5/5 completed
  Activation Rate: 100%
  Total Cost: $0.2341
  Duration: 45.2s
  Files Created: 12
```

#### skillchain status

Show skillchain progress.

```bash
claude-agent skillchain status [options]
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--project` | string | current dir | Project directory |

**Example:**
```bash
claude-agent skillchain status --project /my/project
```

**Output:**
```
Skillchain Status

  Goal: Build a sales dashboard
  Blueprint: dashboard
  Maturity: intermediate
  Mode: delegated
  Started: 2025-12-10T10:00:00
  Updated: 2025-12-10T10:15:00

Skills (5):
  [x] theming-components
       Files: 2
  [x] designing-layouts
       Files: 1
  [>] creating-dashboards
       Files: 0
  [ ] visualizing-data
  [ ] assembling-components

  Completed: 2
  Failed: 0
  Remaining: 3
  Activation Rate: 100%
```

#### skillchain resume

Resume an interrupted skillchain.

```bash
claude-agent skillchain resume [options]
```

**Options:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--project` | string | current dir | Project directory with .skillchain-progress.json |
| `--repo` | string | auto | Path to ai-design-components repo |

**Example:**
```bash
claude-agent skillchain resume --project /my/project
```

**Output:**
```
[INFO] Resuming skillchain: Build a sales dashboard
[INFO] Remaining skills: 3

[INFO] [1/3] Starting: creating-dashboards
[SUCCESS] [1/3] Complete: creating-dashboards
...

Resume Complete
  Skills: 3/3
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (check stderr for details) |
| `130` | Interrupted by user (Ctrl+C) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_CLI_PATH` | Override path to claude binary |
| `CLAUDE_AGENT_LOG_LEVEL` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `CLAUDE_AGENT_TIMEOUT` | Default timeout in seconds |

## Shell Completion

For bash completion, add to `~/.bashrc`:

```bash
eval "$(_CLAUDE_AGENT_COMPLETE=bash_source claude-agent)"
```

For zsh completion, add to `~/.zshrc`:

```bash
eval "$(_CLAUDE_AGENT_COMPLETE=zsh_source claude-agent)"
```

## Next Steps

- [Architecture](./architecture) - System design
- [Real-World Usage](./real-world-usage) - Practical examples
- [Skillchain Integration](./skillchain-integration) - Using with skillchain
