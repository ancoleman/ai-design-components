# Skill Execution Protocol

**Purpose:** Guarantee >80% skill activation rate during skillchain execution.

This protocol defines mandatory behaviors for skill invocation. Deviation from this protocol results in incomplete implementations.

---

## 1. Execution Phases

Skillchain execution has TWO distinct phases. Never mix them.

### Phase 1: SELECTION (No Invocations)

During selection phase, you:
- Analyze the user's goal
- Identify relevant skills
- Score and rank skills
- Resolve dependencies
- Build the skill chain
- Present chain for user approval

**You do NOT invoke skills during this phase.**

### Phase 2: EXECUTION (Invocations Only)

During execution phase, you:
- Invoke each approved skill in order
- Complete skill instructions
- Track progress
- Report completion

**Every skill in the approved chain MUST be invoked.**

---

## 2. Execution Contract

Upon entering EXECUTION PHASE, you are bound by these rules:

### Mandatory Behaviors

1. **INVOKE** every skill in the approved chain
2. **ANNOUNCE** each skill before invocation
3. **USE THE SKILL TOOL** - actual tool call, not description
4. **COMPLETE** skill instructions before proceeding
5. **TRACK** progress using the execution tracker

### Prohibited Behaviors

1. **NO** skipping skills without user consent
2. **NO** combining multiple skills into one
3. **NO** describing skills instead of invoking
4. **NO** deferring invocations for explanations
5. **NO** deciding on your own to omit skills

### Violation Consequences

Failure to invoke a skill in the approved chain = incomplete implementation.
The user expects all approved skills to be invoked.

---

## 3. Invocation Protocol

For EACH skill in the chain, follow this exact sequence:

### Step 1: Announce
```
Now invoking skill: {skill_name}
Purpose: {brief purpose}
```

### Step 2: Invoke
Use the Skill tool with the exact invocation string:
```
Skill: {plugin-name}:{skill-name}
```

**Example:**
```
Skill: ui-foundation-skills:theming-components
```

### Step 3: Complete
Follow all instructions provided by the skill.
Answer any questions the skill asks.
Generate any code the skill requires.

### Step 4: Report
```
Skill complete: {skill_name}
Files created: {list files if any}
Moving to next skill.
```

### Step 5: Update Tracker
Mark the skill as complete in the execution tracker.
Identify the next skill to invoke.

---

## 4. Execution Tracker

Maintain this tracker throughout execution. Update after EACH skill.

```
## Skill Chain Execution

| # | Skill | Invocation | Status |
|---|-------|------------|--------|
| 1 | theming-components | ui-foundation-skills:theming-components | [STATUS] |
| 2 | building-forms | ui-input-skills:building-forms | [STATUS] |
| 3 | assembling-components | ui-assembly-skills:assembling-components | [STATUS] |

Current: [skill name]
Next Action: [INVOKE / COMPLETE / REPORT]
```

### Status Values

- `INVOKE NOW` - This skill must be invoked immediately
- `IN PROGRESS` - Skill invoked, completing instructions
- `COMPLETE` - Skill finished, ready for next
- `PENDING` - Not yet reached
- `SKIPPED` - User explicitly requested skip

---

## 5. Verification Checkpoints

After each skill SHOULD have been invoked, verify:

```
Verification Checkpoint
Did I just use the Skill tool for {skill_name}?

 YES -> Update tracker, proceed to next skill
 NO  -> STOP. Invoke the skill NOW before continuing.
```

**Never proceed past a checkpoint without verification.**

---

## 6. Error Handling

### Skill Load Failure

If a skill fails to load:

```
Skill invocation failed: {skill_name}
Error: {error message}

Options:
1. Retry invocation
2. Skip with user consent
3. Stop execution

User choice required.
```

### User Requests Skip

If user asks to skip a skill:

```
User requested skip: {skill_name}

Confirming: This skill will not be invoked.
The final output may be missing {what the skill provides}.

Continue without {skill_name}? (yes/no)
```

Mark as `SKIPPED` in tracker only after user confirms.

---

## 7. Activation Rate Target

**Target: >80% skill activation rate**

This means: For every 10 skills in an approved chain, at least 8 must be actually invoked using the Skill tool.

### How to Achieve This

1. **Always invoke** - Don't skip unless user explicitly requests
2. **Verify invocations** - Use checkpoints after each skill
3. **Track progress** - Maintain execution tracker throughout
4. **Report completeness** - Show final activation stats

### Final Report Format

After execution completes:

```
Execution Complete

Skills Approved: {N}
Skills Invoked: {M}
Skills Skipped: {K} (user requested)
Activation Rate: {M/N * 100}%

[List of invoked skills]
[List of skipped skills with reasons]
```

---

## 8. Dynamic Chain Execution

When executing a dynamically-generated skill chain (no blueprint):

### Pre-Execution Confirmation

```
Dynamic Skill Chain Ready

The following skills will be invoked in order:

1. {skill_1} - {purpose}
2. {skill_2} - {purpose}
3. {skill_3} - {purpose}

Estimated questions: {X}
All skills will be invoked unless you request a skip.

Proceed with execution? (yes / modify / cancel)
```

### Commitment Statement

Before starting execution, output:

```
Entering EXECUTION PHASE

I will invoke these skills in sequence:
1. Skill tool call: {invocation_1}
2. Skill tool call: {invocation_2}
3. Skill tool call: {invocation_3}

Beginning with skill #1.
```

Then immediately invoke the first skill.

---

## 9. Quick Reference

### Invocation Syntax
```
Skill: {plugin-name}:{skill-name}
```

### Common Invocations
| Skill | Invocation |
|-------|------------|
| theming-components | `ui-foundation-skills:theming-components` |
| building-forms | `ui-input-skills:building-forms` |
| building-tables | `ui-data-skills:building-tables` |
| creating-dashboards | `ui-data-skills:creating-dashboards` |
| implementing-api-patterns | `backend-api-skills:implementing-api-patterns` |
| using-relational-databases | `backend-data-skills:using-relational-databases` |
| assembling-components | `ui-assembly-skills:assembling-components` |

### Execution Loop
```
FOR EACH skill in approved_chain:
  1. ANNOUNCE skill
  2. INVOKE using Skill tool
  3. COMPLETE skill instructions
  4. REPORT completion
  5. UPDATE tracker
  6. VERIFY invocation
  7. PROCEED to next
END FOR
```

---

## Summary

**The execution protocol guarantees high skill activation by:**

1. Separating selection from execution
2. Defining mandatory invocation behaviors
3. Prohibiting common failure modes
4. Requiring progress tracking
5. Adding verification checkpoints
6. Targeting >80% activation rate

**Remember:** Every approved skill should be invoked. No exceptions without explicit user consent.
