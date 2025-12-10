# Delegated Execution

Delegated execution solves the context rot problem that affects long skill chains by using fresh-context sub-agents for each skill.

## The Problem: Context Rot

When executing long skill chains (4+ skills), LLM agents experience "context rot" - the accumulation of conversation history causes the model to lose focus on later steps:

**Symptoms of Context Rot:**
- Skills at the end of the chain get skipped
- Validation steps never execute
- Activation rates drop below 50% for 6+ skill chains
- The agent "forgets" the execution plan

**Real-world example:**
```
RAG Pipeline Blueprint (6 skills)

Expected: All 6 skills invoked
Actual:   Only 3/6 invoked (50% activation)

Skills executed:
  - implementing-api-patterns
  - using-vector-databases
  - ai-data-engineering
  - model-serving (SKIPPED - context rot)
  - building-ai-chat (SKIPPED - context rot)
  - implementing-observability (SKIPPED - context rot)

Validation: Never executed
```

## The Solution: Delegated Execution

Delegated execution uses the **Task tool** to spawn fresh-context sub-agents for each skill:

```
Coordinator (minimal context)
    |
    +-> Task: Sub-Agent 1 (skill-1, fresh context)
    |       Returns: files, decisions, outputs
    |
    +-> Task: Sub-Agent 2 (skill-2, fresh context)
    |       Returns: files, decisions, outputs
    |
    +-> Task: Validation Agent (fresh context)
            Returns: completeness report
```

**Key Benefits:**
- **100% activation rate** - Each skill gets dedicated focus
- **No context rot** - Fresh context per skill
- **Parallel execution** - Independent skills can run simultaneously
- **Easy recovery** - Failed skills can be re-spawned

## Architecture

### Coordinator Agent

The coordinator maintains minimal state:
- Skill sequence
- Completion status
- Output summaries

It does NOT invoke skills directly - it delegates everything.

### Skill Sub-Agents

Each sub-agent:
1. Receives skill invocation and context
2. Invokes ONE skill using the Skill tool
3. Follows all skill instructions
4. Returns structured results

### Validation Sub-Agent

After all skills complete:
1. Receives list of expected deliverables
2. Verifies files exist
3. Checks code quality
4. Reports completeness percentage

## Usage

### Automatic Recommendation

Skillchain automatically recommends delegated execution for:
- Chains with 4+ skills
- Complex blueprints (dashboard, rag-pipeline)
- Multi-domain workflows

### Manual Selection

When prompted for execution mode:

```
Choose execution mode:

1. Standard Execution
   - Single conversation flow
   - Best for: Short chains (2-3 skills)

2. Delegated Execution (RECOMMENDED)
   - Fresh sub-agent per skill
   - Best for: Complex blueprints, long chains
   - Benefit: ~100% skill activation rate

Your choice (1/2):
```

Choose `2` for delegated execution.

## Execution Flow

### Step 1: Chain Confirmation

```
DELEGATED SKILL CHAIN EXECUTION

Goal: RAG pipeline with chat interface
Skills: 6 skills in sequence
Mode: Delegated (fresh context per skill)

EXECUTION PLAN:
1. [SKILL] implementing-api-patterns
2. [SKILL] using-vector-databases
3. [SKILL] ai-data-engineering
4. [SKILL] model-serving
5. [SKILL] building-ai-chat
6. [VALIDATION] Final validation

Proceed? (yes/modify/cancel)
```

### Step 2: Skill Delegation

```
DELEGATING: ai-data-engineering
Progress: 2/6 complete

Spawning sub-agent...
```

### Step 3: Progress Updates

```
Skill complete: ai-data-engineering
  Files created: 4
  Ready for next skill.

  Progress: [3/6] ██████████░░░░░░░░ 50%
```

### Step 4: Validation Report

```
VALIDATION REPORT

FILES VERIFIED: 18/18
DELIVERABLES:
  - API endpoints - complete
  - Vector storage - complete
  - Chat interface - complete

COMPLETENESS: 100%
STATUS: PASS
```

## When to Use Delegated Execution

### Recommended For:
- Chains with 4+ skills
- Complex blueprints
- RAG pipelines
- Multi-domain workflows
- Workflows where validation is critical

### Not Needed For:
- Simple 2-3 skill chains
- Quick prototypes
- Single-domain focused work

## Performance Comparison

| Metric | Standard | Delegated |
|--------|----------|-----------|
| Short chains (2-3 skills) | 95% activation | 100% activation |
| Long chains (4-6 skills) | 50-70% activation | 100% activation |
| Very long chains (7+ skills) | 30-50% activation | 100% activation |
| Validation execution | Often skipped | Always executed |
| Recovery from failures | Difficult | Easy (re-spawn) |
| Parallel execution | Not possible | Supported |

## Technical Details

### Sub-Agent Prompt Template

Each sub-agent receives:
```
You are executing a single skill as part of a skillchain.

## Skill to Invoke
- Name: {skill_name}
- Invocation: {invocation}

## Context
- Goal: {original_goal}
- Project Path: {project_path}
- Previous Skills: {completed_skills}
- Previous Outputs: {summary}

## Instructions
1. Use the Skill tool to invoke: {invocation}
2. Follow ALL skill instructions
3. Generate all required code
4. Report what was created

## Required Output Format
SKILL COMPLETE: {skill_name}

FILES CREATED:
- {file1}
- {file2}

KEY DECISIONS:
- {decision1}

OUTPUTS FOR NEXT SKILL:
- {output1}
```

### State Tracking

The coordinator maintains:
```yaml
execution:
  - skill: implementing-api-patterns
    status: complete
    outputs: {files: [...], decisions: [...]}
  - skill: using-vector-databases
    status: in_progress
    outputs: null
  - skill: ai-data-engineering
    status: pending
    outputs: null
```

### Parallel Execution

Skills without dependencies can run simultaneously:
```
Parallel execution detected:
  - skill-a (no deps)
  - skill-b (no deps)

[Task 1: skill-a] [Task 2: skill-b]  <- same message

Both complete, now running:
  - skill-c (depends on skill-a)
```

## Error Handling

### Sub-Agent Failure

```
Sub-agent issue: model-serving

Options:
1. Retry with fresh sub-agent
2. Skip this skill (with consent)
3. Abort execution

Your choice:
```

### Partial Completion

If validation finds gaps:
```
Validation found gaps:

MISSING:
- observability dashboard

Options:
1. Generate missing components
2. Accept partial completion
3. View detailed report

Your choice:
```

## FAQ

**Q: Does delegated execution take longer?**
A: Sub-agent spawning adds minimal overhead (seconds). The total time is similar, but success rate is much higher.

**Q: Can I mix standard and delegated?**
A: Currently, you choose one mode per chain. Future versions may support hybrid modes.

**Q: What if a sub-agent hangs?**
A: The coordinator can timeout and offer retry or skip options.

**Q: Does parallel execution always work?**
A: Only for skills with no dependencies. The system automatically detects parallelization opportunities.
