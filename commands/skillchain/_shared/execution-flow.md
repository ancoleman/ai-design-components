# Execution Flow Guidelines

Guidelines for skill invocation order, question asking strategy, and workflow management during skillchain execution.

---

## 1. Skill Invocation Order

Follow these ordering principles when invoking skills:

### 1.1 Foundation First
- **Frontend:** `theming-components` always runs first
- **Backend:** Database/API foundation skills before dependent services
- Establish core systems before building on them

### 1.2 Structure Before Content
- Layout systems before individual components
- Navigation structure before content pages
- Database schema before API endpoints

### 1.3 Data Before Display
- Database configuration before API patterns
- Data ingestion before visualization
- Backend data models before frontend displays

### 1.4 Assembly Last
- `assembling-components` (frontend) or equivalent always runs last
- Integration step comes after all individual skills
- Validation happens at the final assembly stage

---

## 2. Question Asking Strategy

### 2.1 Context-Aware Questions
Present questions with context from:
- User's original goal
- Previously answered questions from other skills
- Detected keywords and patterns
- Dependencies between skills

**Example:**
```
Since you selected "bar chart" in visualizing-data,
should the table export include chart data? (yes/no)
```

### 2.2 Smart Defaults
Provide intelligent defaults based on:
- User goal keywords
- Common patterns for the category
- Previously selected options
- Industry best practices

**Example:**
```
Color scheme: [blue-gray] (professional, matches "dashboard" goal)
Theme modes: [light, dark] (recommended for accessibility)
```

### 2.3 Progressive Disclosure
- Ask essential questions first
- Offer "skip" for any question
- Group related questions together
- Show optional vs required clearly

### 2.4 Confirmation Before Execution
Always confirm the full skill chain with estimated:
- Time to complete
- Number of questions
- Skills that will be invoked

---

## 3. Workflow Commands

Available during skill execution:

### 3.1 Navigation Commands

**`back`** - Return to previous skill
- Re-displays previous questions
- Preserves current answers as defaults
- Updates progress indicator

**`skip`** - Use defaults for current skill
- Applies all default values for remaining questions in this skill
- Moves to next skill immediately
- Useful for rapid prototyping

### 3.2 Status Commands

**`status`** - Show current progress
- Displays: "Step X/Y complete"
- Shows completed skills (✓)
- Shows current skill (◆)
- Shows remaining skills
- Re-displays current question

**Example output:**
```
═══════════════════════════════════════════
PROGRESS: Step 3/6
═══════════════════════════════════════════
✓ theming-components (complete)
✓ visualizing-data (complete)
◆ building-tables (current: question 2/5)
  creating-dashboards (pending)
  providing-feedback (pending)
  assembling-components (pending)
═══════════════════════════════════════════
```

### 3.3 Control Commands

**`done`** - Finish early with current configuration
- Skips remaining skills
- Uses defaults for unanswered questions
- Proceeds directly to assembly
- Useful when user has enough configured

**`restart`** - Start over from beginning
- Clears all answers
- Returns to skill chain confirmation
- Allows re-selection of skills
- Preserves original goal

### 3.4 Help Commands

**`help`** - Display workflow commands
- Shows all available commands
- Explains each command's behavior
- Returns to current question after display

---

## 4. Error Handling Patterns

### 4.1 Skill Invocation Failures

When a skill fails to invoke:

```
⚠️  ERROR: Skill 'visualizing-data' failed to load

Reason: [error message]

Options:
1. Continue with remaining skills (skip this one)
2. Retry this skill
3. Stop workflow and show partial progress

Your choice (1/2/3):
```

### 4.2 Invalid Answers

When user provides invalid input:

```
❌ Invalid answer: "{user_input}"

Expected: One of [option1, option2, option3] or "skip"

Please try again, or type "help" for workflow commands:
```

### 4.3 Dependency Failures

When a dependent skill was skipped/failed:

```
⚠️  WARNING: This skill depends on 'theming-components' which was skipped.

We'll use default theming values. Continue? (yes/no)
```

### 4.4 Assembly Failures

When final assembly encounters issues:

```
⚠️  Assembly validation failed:

Issues found:
- Missing tokens.css import
- Hardcoded color values in Button.css

Auto-fix these issues? (yes/no)
```

---

## 5. User Experience Principles

### 5.1 Clear Progress Indicators
- Always show current step number and total
- Use visual separators between skills
- Highlight current position in chain

### 5.2 Reversible Actions
- All navigation supports "back"
- Preserve answers when revisiting
- Allow restart without penalty

### 5.3 Escape Hatches
- "skip" available for every question
- "done" available to finish early
- Clear abort mechanism if needed

### 5.4 Helpful Feedback
- Explain why questions are asked
- Show how answers affect output
- Provide examples when helpful
- Acknowledge user commands immediately

---

## 6. Special Handling Cases

### 6.1 Required Skills
Some skills are always included:
- **Frontend:** `theming-components`, `assembling-components`
- **Backend:** Platform-specific foundation skills

Never allow skipping required skills entirely, but allow skipping individual questions within them (using defaults).

### 6.2 Conditional Skills
Some skills only trigger with specific keywords:
- Vector databases require AI/RAG context
- Real-time sync requires collaboration keywords

If conditionally included, explain WHY to the user.

### 6.3 Conflicting Configurations
When answers conflict across skills:
- Detect conflicts before assembly
- Present conflict to user
- Suggest resolution
- Allow user to choose priority

**Example:**
```
⚠️  CONFLICT DETECTED

visualizing-data specified: library="d3"
creating-dashboards specified: library="recharts"

Which should we use for consistency?
1. D3 (more flexible, higher complexity)
2. Recharts (simpler, better for dashboards)
3. Use both (components will differ)
```

---

## Summary

**Execution flow priorities:**
1. Foundation → Structure → Content → Assembly
2. Context-aware questions with smart defaults
3. Full navigation support (back, skip, status, done, restart)
4. Clear error handling with recovery options
5. User-friendly progress indicators
6. Reversible actions and escape hatches
