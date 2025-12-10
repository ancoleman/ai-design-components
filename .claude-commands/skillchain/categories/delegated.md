# Delegated Execution Orchestrator

**Purpose:** Solve context rot by delegating skill execution to fresh-context sub-agents.

This orchestrator uses the Task tool to spawn sub-agents for each skill, ensuring 100% skill activation regardless of chain length.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     COORDINATOR (This Agent)                     │
│  - Manages execution state                                       │
│  - Spawns sub-agents via Task tool                              │
│  - Collects results                                             │
│  - Never invokes skills directly (no context accumulation)      │
└─────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │  Sub-Agent  │    │  Sub-Agent  │    │  Sub-Agent  │
    │   Skill 1   │    │   Skill 2   │    │   Skill N   │
    │ (fresh ctx) │    │ (fresh ctx) │    │ (fresh ctx) │
    └─────────────┘    └─────────────┘    └─────────────┘
```

**Key Benefits:**
- Each skill gets fresh context (no rot)
- Sub-agents focus on ONE skill only
- Coordinator tracks state compactly
- Works for chains of any length

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

Use the Task tool to spawn a fresh-context sub-agent:

```
Task tool parameters:
  subagent_type: "general-purpose"
  description: "Execute {skill_name} skill"
  prompt: |
    You are executing a single skill as part of a skillchain.

    ## Your Task
    Invoke the skill and complete ALL its instructions.

    ## Skill to Invoke
    - Name: {skill_name}
    - Invocation: {invocation}

    ## Context
    - Goal: {original_goal}
    - Project Path: {project_path}
    - Previous Skills Completed: {list of completed skills}
    - Previous Outputs: {summary of previous outputs}

    ## Instructions
    1. Use the Skill tool to invoke: {invocation}
    2. Follow ALL instructions provided by the skill
    3. Answer any questions the skill asks (use reasonable defaults or provided preferences)
    4. Generate all required code/files
    5. Report back what was created

    ## User Preferences (apply where applicable)
    {user_prefs or "None provided - use skill defaults"}

    ## Required Output Format
    When complete, report:
    ```
    SKILL COMPLETE: {skill_name}

    FILES CREATED:
    - {file1}
    - {file2}

    KEY DECISIONS:
    - {decision1}
    - {decision2}

    OUTPUTS FOR NEXT SKILL:
    - {output1}
    - {output2}
    ```
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

For skills WITHOUT dependencies on each other, spawn multiple sub-agents in parallel:

```
Parallel execution opportunity detected:
  - skill-a (no deps)
  - skill-b (no deps)
  - skill-c (depends on skill-a)

Executing skill-a and skill-b in parallel...
```

Use multiple Task tool calls in a SINGLE message to run in parallel:

```
[Task 1: Execute skill-a]
[Task 2: Execute skill-b]

Wait for both to complete...

[Task 3: Execute skill-c (now that skill-a is done)]
```

---

## Step 6: Validation Sub-Agent

After all skills complete, spawn a validation sub-agent:

```
Task tool parameters:
  subagent_type: "general-purpose"
  description: "Validate skillchain completion"
  prompt: |
    You are validating a completed skillchain.

    ## Goal
    {original_goal}

    ## Project Path
    {project_path}

    ## Skills Executed
    {list of all skills with their outputs}

    ## Validation Tasks
    1. Check that all expected files exist
    2. Verify code compiles/lints (if applicable)
    3. Check that deliverables match the goal
    4. Report any gaps or issues

    ## Blueprint Expected Deliverables (if applicable)
    {blueprint deliverables list}

    ## Required Output Format
    ```
    VALIDATION REPORT

    FILES VERIFIED: {count}/{expected}
    ✓ {file1} - exists
    ✓ {file2} - exists
    ✗ {file3} - MISSING

    DELIVERABLES:
    ✓ {deliverable1} - complete
    ✓ {deliverable2} - complete
    ○ {deliverable3} - optional, skipped

    ISSUES FOUND:
    - {issue1}
    - {issue2}

    COMPLETENESS: {X}%
    STATUS: {PASS/PARTIAL/FAIL}
    ```
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

If validation reports < 100% completeness:

```
Validation found gaps:

MISSING:
- {missing_item_1}
- {missing_item_2}

Options:
1. Generate missing components (spawn additional sub-agents)
2. Accept partial completion
3. View detailed gap analysis

Your choice (1/2/3):
```

If user chooses 1, spawn additional sub-agents to fill gaps.

---

## Sub-Agent Prompt Templates

### Template: Component Skill

```
You are executing a UI component skill.

## Skill
Invoke: {invocation}

## Context
- Goal: {goal}
- Project: {project_path}
- Theme: {theme from previous skill or default}

## Instructions
1. Invoke the skill using: Skill tool with "{invocation}"
2. When skill asks questions, use these preferences: {prefs}
3. Generate all code to: {project_path}
4. Report files created

## Output Format
Report: FILES_CREATED, KEY_DECISIONS, NEXT_SKILL_INPUTS
```

### Template: Backend Skill

```
You are executing a backend skill.

## Skill
Invoke: {invocation}

## Context
- Goal: {goal}
- Project: {project_path}
- Frontend Integration: {frontend outputs if any}

## Instructions
1. Invoke the skill using: Skill tool with "{invocation}"
2. When skill asks questions, use these preferences: {prefs}
3. Ensure API endpoints align with frontend expectations
4. Generate all code to: {project_path}

## Output Format
Report: FILES_CREATED, API_ENDPOINTS, DATABASE_SCHEMA, NEXT_SKILL_INPUTS
```

### Template: Integration Skill

```
You are executing an integration skill.

## Skill
Invoke: {invocation}

## Context
- Goal: {goal}
- Project: {project_path}
- Components to Integrate: {list from previous skills}

## Instructions
1. Invoke the skill using: Skill tool with "{invocation}"
2. Wire together outputs from previous skills
3. Ensure all pieces connect properly

## Output Format
Report: FILES_CREATED, INTEGRATIONS_COMPLETED, VERIFICATION_STATUS
```

---

## Error Handling

### Sub-Agent Failure

If a sub-agent fails or returns incomplete results:

```
Sub-agent execution issue: {skill_name}

Issue: {error description}

Options:
1. Retry with fresh sub-agent
2. Skip this skill (user consent required)
3. Abort execution

Your choice:
```

### Sub-Agent Timeout

If sub-agent takes too long:

```
Sub-agent timeout: {skill_name}

The skill is taking longer than expected.

Options:
1. Continue waiting
2. Check partial progress
3. Spawn new sub-agent

Your choice:
```

---

## Key Differences from Standard Execution

| Aspect | Standard Execution | Delegated Execution |
|--------|-------------------|---------------------|
| Context | Single conversation, accumulates | Fresh per skill |
| Skill Invocation | Direct | Via sub-agent |
| Context Rot | High risk for long chains | No risk |
| Activation Rate | ~50% for long chains | ~100% |
| Parallelization | Not possible | Possible for independent skills |
| Recovery | Difficult | Easy (re-spawn sub-agent) |
| Progress Tracking | May be lost | Always maintained |

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
  - [ ] Spawn sub-agent via Task tool
  - [ ] Pass skill invocation and context
  - [ ] Collect results
  - [ ] Update state
- [ ] Spawn validation sub-agent
- [ ] Present final report
- [ ] Handle gaps if any
- [ ] Offer to save preferences

---

## Quick Start

To use delegated execution:

1. Run `/skillchain {goal}`
2. When offered execution modes, choose "delegated"
3. Confirm the skill chain
4. Watch sub-agents execute each skill
5. Review final validation report
