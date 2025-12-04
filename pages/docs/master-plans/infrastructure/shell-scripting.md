---
sidebar_position: 11
title: Shell Scripting
description: Master plan for robust shell scripting with error handling, argument parsing, portability, and best practices
tags: [master-plan, infrastructure, shell, bash, scripting, automation]
---

# Shell Scripting

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Shell scripting remains indispensable for system automation. This skill covers robust bash/sh scripting with proper error handling, argument parsing, portability (POSIX sh vs Bash), testing, and integration with common utilities.

## Scope

This skill teaches:

- **Error Handling** - `set -euo pipefail`, trap handlers, defensive programming
- **Argument Parsing** - getopts, long options, usage messages
- **Parameter Expansion** - String manipulation, default values, arrays
- **Portability** - POSIX sh vs Bash, cross-platform scripting
- **Utility Integration** - jq, yq, awk, sed, grep, find
- **Testing and Linting** - shellcheck, bats testing framework

## Key Components

### Error Handling Patterns

**Fail-Fast with `set` Options:**
```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures
```

- `-e` Exit immediately if command fails
- `-u` Treat unset variables as errors
- `-o pipefail` Return exit code from failed pipe command

**Trap Handlers for Cleanup:**
```bash
cleanup() {
    rm -f "$temp_file"
    echo "Cleanup completed"
}
trap cleanup EXIT  # Always run cleanup
trap 'echo "Error on line $LINENO"' ERR
```

**Explicit Error Checking:**
```bash
if ! command_that_might_fail; then
    echo "Error: command failed" >&2
    exit 1
fi
```

### Argument Parsing

**Basic getopts:**
```bash
while getopts "f:v" opt; do
    case $opt in
        f) file="$OPTARG" ;;
        v) verbose=true ;;
        *) usage; exit 1 ;;
    esac
done
```

**Long Options (Bash):**
```bash
while [[ $# -gt 0 ]]; do
    case $1 in
        --file) file="$2"; shift 2 ;;
        --verbose) verbose=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done
```

### Parameter Expansion

**String Manipulation:**
```bash
${var#pattern}     # Remove shortest match from beginning
${var##pattern}    # Remove longest match from beginning
${var%pattern}     # Remove shortest match from end
${var%%pattern}    # Remove longest match from end
${var/old/new}     # Replace first occurrence
${var//old/new}    # Replace all occurrences
```

**Default Values:**
```bash
${var:-default}    # Use default if var is unset
${var:=default}    # Set var to default if unset
${var:?error}      # Exit with error if var is unset
${var:+value}      # Use value if var is set
```

### Utility Integration

**jq - JSON Processing:**
```bash
curl -s api.example.com/data | jq '.results[] | .name'
```

**yq - YAML Processing:**
```bash
yq eval '.services.webapp.image' docker-compose.yml
```

**awk - Text Processing:**
```bash
ps aux | awk '$3 > 50 { print $2, $11 }'  # High CPU processes
```

**sed - Stream Editing:**
```bash
sed -i 's/old/new/g' file.txt  # Replace in-place
```

## Decision Framework

**POSIX sh vs Bash?**

```
Need portability (Alpine, embedded)?
  YES → Use POSIX sh (#!/bin/sh)
        Avoid: arrays, [[, ${var//}, process substitution

Need advanced features?
  YES → Use Bash (#!/usr/bin/env bash)
        Available: arrays, [[, ${var//}, <()

CI/CD environment controlled?
  YES → Bash usually available
        → Use Bash for richer features

Docker/container context?
  Alpine base? → POSIX sh (no bash by default)
  Debian/Ubuntu base? → Bash available
```

**When to Use Shell vs Python/Go?**

```
Use Shell when:
  - System commands are 80%+ of logic
  - Rapid prototyping/throwaway scripts
  - Zero dependencies required
  - Pipeline composition (cmd1 | cmd2)

Use Python/Go when:
  - Complex data structures needed
  - Network/API heavy operations
  - Long-lived daemon processes
  - Unit testing critical
  - Team unfamiliar with shell
```

## Tool Recommendations

### Linting and Testing

**shellcheck** - Static analysis for shell scripts
```bash
shellcheck script.sh  # Find bugs and portability issues
```

Common issues detected:
- Unquoted variables
- Useless uses of cat
- Incorrect test operators
- Portability warnings

**bats** - Bash Automated Testing System
```bash
# test/script.bats
@test "addition works" {
    result="$(echo '2 + 2' | bc)"
    [ "$result" -eq 4 ]
}

bats test/script.bats  # Run tests
```

**shfmt** - Shell script formatter
```bash
shfmt -w script.sh  # Format in-place
```

### Utility Tools

**jq** - JSON processor
**yq** - YAML processor
**fzf** - Fuzzy finder for interactive selection
**parallel** - Run commands in parallel
**envsubst** - Environment variable substitution

## Integration Points

**With Other Skills:**
- `linux-administration` - Automate system tasks
- `building-ci-pipelines` - CI/CD build scripts
- `configuration-management` - Wrapper scripts for Ansible/Terraform
- `kubernetes-operations` - kubectl automation scripts
- `infrastructure-as-code` - IaC helper scripts

**Use Cases:**
- Docker entrypoint scripts
- CI/CD pipeline steps (GitHub Actions, GitLab CI)
- Cron jobs and scheduled tasks
- System initialization scripts
- Deployment automation

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/shell-scripting/init.md)
- Related: `linux-administration`, `building-ci-pipelines`, `configuration-management`
