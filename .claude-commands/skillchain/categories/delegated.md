# Delegated Execution Orchestrator

**Purpose:** Solve context rot by delegating skill execution to fresh-context sub-agents.

This orchestrator uses the Task tool to spawn sub-agents for each skill, ensuring 100% skill activation regardless of chain length.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     COORDINATOR (This Agent)                     │
│  - Manages execution state                                       │
│  - Spawns specialized subagents via Task tool                   │
│  - Collects results                                             │
│  - Never invokes skills directly (no context accumulation)      │
└─────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │skill-executor│   │skill-executor│   │skill-executor│
    │   Skill 1   │    │   Skill 2   │    │   Skill N   │
    │ (fresh ctx) │    │ (fresh ctx) │    │ (fresh ctx) │
    └─────────────┘    └─────────────┘    └─────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │skillchain-       │
                    │validator         │
                    │(validation only) │
                    └──────────────────┘
```

**Key Benefits:**
- Each skill gets fresh context (no rot)
- Specialized subagents (skill-executor, skillchain-validator)
- skill-executor focuses on ONE skill only
- Coordinator tracks state compactly
- Works for chains of any length
- Guaranteed >80% skill activation rate

---

## Step 1: Receive Context from Router

Received from router or blueprint:

```yaml
chain_context:
  blueprint: "{blueprint_name}" or null
  original_goal: "{user's goal}"
  skills_sequence:
    - name: skill-1
      invocation: plugin-1:skill-1
      provides: [capability-a, capability-b]
    - name: skill-2
      invocation: plugin-2:skill-2
      provides: [capability-c]
  project_path: "{path}" or null
  user_prefs: {preferences} or null
```

---

## Step 2: Initialize Execution State

Create a compact state tracker (this is ALL the context this orchestrator maintains):

```yaml
# Delegated Execution State
goal: "{original_goal}"
project_path: "{project_path}"
total_skills: {N}

execution:
  - skill: skill-1
    invocation: plugin-1:skill-1
    status: pending
    outputs: null
  - skill: skill-2
    invocation: plugin-2:skill-2
    status: pending
    outputs: null

current_index: 0
completed: 0
failed: 0
```

---

## Step 3: Present Execution Plan

Display to user:

```
┌────────────────────────────────────────────────────────────┐
│           DELEGATED SKILL CHAIN EXECUTION                  │
├────────────────────────────────────────────────────────────┤
│ Goal: {original_goal}                                      │
│ Skills: {N} skills in sequence                             │
│ Mode: Delegated (fresh context per skill)                  │
├────────────────────────────────────────────────────────────┤
│ EXECUTION PLAN:                                            │
│                                                            │
│ 1. [SKILL] skill-1                                         │
│    Provides: capability-a, capability-b                    │
│                                                            │
│ 2. [SKILL] skill-2                                         │
│    Provides: capability-c                                  │
│                                                            │
│ N. [VALIDATION] Final validation                           │
│    Verifies: All deliverables complete                     │
├────────────────────────────────────────────────────────────┤
│ Each skill runs in a fresh sub-agent context.              │
│ Results are collected and passed forward.                  │
└────────────────────────────────────────────────────────────┘

Proceed with delegated execution? (yes / modify / cancel)
```

---

## Step 4: Execute Skills via Sub-Agents

For EACH skill in the sequence:

### 4.1 Announce Delegation

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DELEGATING: skill-{N}
  Progress: {completed}/{total} complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Spawning sub-agent for: {skill_name}
Invocation: {invocation}
```

### 4.2 Spawn Sub-Agent Using Task Tool

Use the Task tool to spawn the skill-executor subagent:

```
Task tool parameters:
  subagent: "skill-executor"
  description: "Execute {skill_name} skill"
  prompt: |
    Execute skill: {invocation}

    ## Context
    - Goal: {original_goal}
    - Project Path: {project_path}
    - Skills Completed: {list of completed skills}

    ## Previous Skill Outputs
    {summary of previous outputs from execution state}

    ## User Preferences
    {user_prefs or "None provided - use skill defaults"}
```

### 4.3 Collect Results

After sub-agent returns:

```yaml
# Update execution state
execution[current_index]:
  status: complete
  outputs:
    files: [list from sub-agent]
    decisions: [list from sub-agent]
    key_outputs: [list from sub-agent]

current_index: current_index + 1
completed: completed + 1
```

### 4.4 Progress Report

```
✓ Skill complete: {skill_name}
  Files created: {count}
  Ready for next skill.

  Progress: [{completed}/{total}] ████████░░░░░░░░ {percentage}%
```

---

## Step 5: Parallel Execution (Optional)

For skills WITHOUT dependencies on each other, spawn multiple skill-executor subagents in parallel:

```
Parallel execution opportunity detected:
  - skill-a (no deps)
  - skill-b (no deps)
  - skill-c (depends on skill-a)

Executing skill-a and skill-b in parallel...
```

Use multiple Task tool calls in a SINGLE message to run in parallel:

```
[Task 1: skill-executor for skill-a]
[Task 2: skill-executor for skill-b]

Wait for both to complete...

[Task 3: skill-executor for skill-c (now that skill-a is done)]
```

---

## Step 6: Validation Sub-Agent

After all skills complete, spawn the skillchain-validator subagent:

```
Task tool parameters:
  subagent: "skillchain-validator"
  description: "Validate skillchain completion"
  prompt: |
    Validate the completed skillchain.

    ## Context
    - Blueprint: {blueprint_name or "custom chain"}
    - Maturity Level: {maturity_level or "intermediate"}
    - Project Path: {project_path}

    ## Skills Executed
    {list of all skills with their invocation strings}

    ## Expected Deliverables (from blueprint)
    {blueprint deliverables list if blueprint, otherwise skill-declared outputs}

    ## Skill Outputs Summary
    {summary of what each skill created}
```

---

## Step 7: Final Report

After validation completes, present final report:

```
┌────────────────────────────────────────────────────────────┐
│           DELEGATED EXECUTION COMPLETE                     │
├────────────────────────────────────────────────────────────┤
│ Goal: {original_goal}                                      │
│                                                            │
│ SKILL EXECUTION:                                           │
│   Total Skills: {N}                                        │
│   Completed:    {completed}                                │
│   Failed:       {failed}                                   │
│   Activation:   {activation_rate}%                         │
│                                                            │
│ SKILLS EXECUTED:                                           │
│   ✓ skill-1 - {brief output summary}                       │
│   ✓ skill-2 - {brief output summary}                       │
│   ✓ skill-N - {brief output summary}                       │
│                                                            │
│ VALIDATION:                                                │
│   Completeness: {completeness}%                            │
│   Status: {PASS/PARTIAL/FAIL}                              │
│                                                            │
│ FILES CREATED:                                             │
│   {total_files} files across {directories} directories     │
│                                                            │
│ NEXT STEPS:                                                │
│   - {next_step_1}                                          │
│   - {next_step_2}                                          │
└────────────────────────────────────────────────────────────┘
```

---

## Step 8: Handle Gaps (If Validation Found Issues)

If skillchain-validator reports < 100% completeness:

```
Validation found gaps:

MISSING:
- {missing_item_1} (primary skill: {skill_name})
- {missing_item_2} (primary skill: {skill_name})

Options:
1. Generate missing components (spawn additional skill-executor subagents)
2. Accept partial completion
3. View detailed gap analysis

Your choice (1/2/3):
```

If user chooses 1, spawn skill-executor subagents for the identified missing skills.

---

## Sub-Agent Prompt Templates

The skill-executor subagent handles execution logic internally. The coordinator just needs to pass context.

### Standard Prompt Template

Use this template for all skill executions:

```
Execute skill: {invocation}

## Context
- Goal: {original_goal}
- Project Path: {project_path}
- Skills Completed: {list of completed skills}

## Previous Skill Outputs
{key outputs from previous skills that this skill may need}

Examples:
  - design_tokens_path: {path}
  - theme_context: {context export}
  - api_endpoints: {list}
  - database_schema: {schema file}

## User Preferences
{user_prefs or "None provided - use skill defaults"}

Examples:
  - framework: React
  - styling: Tailwind CSS
  - database: PostgreSQL
  - theme: Blue-gray with light/dark modes
```

### Notes

- skill-executor knows to invoke the skill using the Skill tool
- skill-executor knows to complete all instructions
- skill-executor knows to report in standardized format
- Coordinator just provides context for informed decision-making

---

## Error Handling

### Sub-Agent Failure

If skill-executor fails or returns incomplete results:

```
Skill execution issue: {skill_name}

Issue: {error description from skill-executor}

Options:
1. Retry with fresh skill-executor subagent
2. Skip this skill (user consent required)
3. Abort execution

Your choice:
```

### Sub-Agent Timeout

If skill-executor takes too long:

```
Skill execution timeout: {skill_name}

The skill is taking longer than expected.

Options:
1. Continue waiting
2. Check partial progress (if skill-executor reported any)
3. Spawn new skill-executor subagent

Your choice:
```

---

## Key Differences from Standard Execution

| Aspect | Standard Execution | Delegated Execution |
|--------|-------------------|---------------------|
| Context | Single conversation, accumulates | Fresh per skill |
| Skill Invocation | Direct | Via skill-executor subagent |
| Validation | Manual or inline | Via skillchain-validator subagent |
| Context Rot | High risk for long chains | No risk |
| Activation Rate | ~50% for long chains | >80% guaranteed |
| Parallelization | Not possible | Possible for independent skills |
| Recovery | Difficult | Easy (re-spawn subagent) |
| Progress Tracking | May be lost | Always maintained |
| Specialization | General Claude agent | Specialized subagents with protocols |

---

## When to Use Delegated Execution

**Recommended for:**
- Chains with 4+ skills
- Complex blueprints (dashboard, RAG pipeline, etc.)
- Multi-domain workflows
- Workflows where validation is critical

**Not needed for:**
- Simple 2-3 skill chains
- Quick prototypes
- Single-domain focused work

---

## Implementation Checklist

- [ ] Parse skill sequence from router context
- [ ] Initialize execution state
- [ ] Present execution plan
- [ ] For each skill:
  - [ ] Spawn skill-executor subagent via Task tool
  - [ ] Pass skill invocation and context (goal, project path, previous outputs, preferences)
  - [ ] Collect standardized results (FILES CREATED, KEY DECISIONS, OUTPUTS FOR NEXT SKILL)
  - [ ] Update state
- [ ] Spawn skillchain-validator subagent via Task tool
- [ ] Pass validation context (blueprint, maturity, project path, skills executed)
- [ ] Present validation report
- [ ] Handle gaps if any (spawn additional skill-executor subagents)
- [ ] Present final report
- [ ] Offer to save preferences

---

## Quick Start

To use delegated execution:

1. Run `/skillchain {goal}`
2. When offered execution modes, choose "delegated"
3. Confirm the skill chain
4. Watch sub-agents execute each skill
5. Review final validation report
