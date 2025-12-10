# Dynamic Skill Chain Orchestrator

Builds and executes custom skill chains when no pre-defined blueprint matches the user's goal.

**Activation Rate Target: >80%**

---

## Step 1: Load Required Resources

Load the execution protocol (MANDATORY):

```
Read {SKILLCHAIN_DATA}/shared/execution-protocol.md
```

Load the skill registry index:

```
Read {SKILLCHAIN_DATA}/registries/_index.yaml
```

---

## Step 2: Load All Skill Registries

Load each domain registry to understand available skills:

```
Read {SKILLCHAIN_DATA}/registries/frontend.yaml
Read {SKILLCHAIN_DATA}/registries/backend.yaml
Read {SKILLCHAIN_DATA}/registries/cloud.yaml
```

Extract from each registry:
- Skill names
- Primary and secondary keywords
- Invocation strings
- Any dependency information

---

## Step 3: Score Skills Against Goal

For each skill in the registries, calculate relevance to the user's goal.

### Scoring Algorithm

```
For each skill:
  score = 0

  # Primary keywords: high weight
  For each keyword in skill.keywords.primary:
    If keyword appears in goal (case-insensitive):
      score += 3
    Else if keyword partially matches a goal word:
      score += 2

  # Secondary keywords: lower weight
  For each keyword in skill.keywords.secondary:
    If keyword appears in goal:
      score += 1

  # Record if score meets threshold
  If score >= 3:
    Add to candidate_skills with score
```

### Score Interpretation

| Score | Meaning |
|-------|---------|
| 6+ | Strong match - definitely include |
| 3-5 | Good match - likely include |
| 1-2 | Weak match - consider if related to strong matches |
| 0 | No match - exclude |

---

## Step 4: Resolve Dependencies and Order

### 4.1 Identify Skill Tiers

Classify candidate skills by tier:

| Tier | Order | Skills |
|------|-------|--------|
| Foundation | 1 | theming-components, implementing-api-patterns |
| Component | 2 | Most individual feature skills |
| Integration | 3 | implementing-observability, testing-strategies |
| Assembly | 4 | assembling-components |

### 4.2 Apply Domain Rules

**Frontend chains:**
- ALWAYS start with `theming-components`
- ALWAYS end with `assembling-components`

**Backend chains:**
- Start with database/API foundation
- End with observability (optional)

**Full-stack chains:**
- Frontend foundation first
- Backend skills
- Frontend components
- Assembly last

### 4.3 Resolve Dependencies

```
final_chain = []
added = set()

# Add foundation skills first
For each candidate where tier == "foundation":
  If not in added:
    final_chain.append(skill)
    added.add(skill.name)

# Add component skills
For each candidate where tier == "component":
  # Check dependencies
  For each dep in skill.depends_on:
    If dep not in added:
      final_chain.append(find_skill(dep))
      added.add(dep)
  If skill.name not in added:
    final_chain.append(skill)
    added.add(skill.name)

# Add integration skills
For each candidate where tier == "integration":
  final_chain.append(skill)

# Add assembly last (if frontend)
If any frontend skill in final_chain:
  final_chain.append(assembling-components)
```

---

## Step 5: Present Chain for Approval

**THIS IS PHASE 1: SELECTION. No skills are invoked yet.**

Present the proposed chain to the user:

```
Dynamic Skill Chain Generated

Goal: "{user_goal}"

No pre-defined blueprint matched your goal. I've analyzed it and
identified these relevant skills:

Foundation:
  1. theming-components (score: 6) - Design tokens and theming

Core Skills:
  2. building-forms (score: 5) - Form components and validation
  3. implementing-api-patterns (score: 4) - REST API endpoints

Assembly:
  4. assembling-components - Wire components together

Total Skills: 4
Estimated Questions: 8-12

All skills will be invoked in sequence unless you request changes.

Options:
  yes     - Proceed with this chain
  modify  - Add or remove skills
  explain - Show why each skill was selected
  cancel  - Abort skillchain
```

Wait for user response before proceeding.

---

## Step 6: Enter Execution Phase

**CRITICAL: You are now entering EXECUTION PHASE.**

### 6.1 Output Commitment Statement

```
Entering EXECUTION PHASE

I will invoke these skills using the Skill tool:
1. Skill: ui-foundation-skills:theming-components
2. Skill: ui-input-skills:building-forms
3. Skill: backend-api-skills:implementing-api-patterns
4. Skill: ui-assembly-skills:assembling-components

Beginning execution now.
```

### 6.2 Initialize Execution Tracker

```
## Skill Chain Execution Tracker

| # | Skill | Invocation | Status |
|---|-------|------------|--------|
| 1 | theming-components | ui-foundation-skills:theming-components | INVOKE NOW |
| 2 | building-forms | ui-input-skills:building-forms | PENDING |
| 3 | implementing-api-patterns | backend-api-skills:implementing-api-patterns | PENDING |
| 4 | assembling-components | ui-assembly-skills:assembling-components | PENDING |

Current: theming-components
Next Action: INVOKE
```

---

## Step 7: Execute Skills

**MANDATORY: You MUST use the Skill tool to invoke each skill.**

### Execution Loop

For EACH skill in the approved chain:

#### 7.1 Announce

```
Now invoking skill: {skill_name}
Purpose: {brief description from registry}
```

#### 7.2 Invoke

**USE THE SKILL TOOL. This is a real tool call, not pseudo-code.**

```
Skill: {invocation_string}
```

**Example invocations:**

| Skill | Tool Call |
|-------|-----------|
| theming-components | `Skill: ui-foundation-skills:theming-components` |
| building-forms | `Skill: ui-input-skills:building-forms` |
| building-tables | `Skill: ui-data-skills:building-tables` |
| creating-dashboards | `Skill: ui-data-skills:creating-dashboards` |
| implementing-api-patterns | `Skill: backend-api-skills:implementing-api-patterns` |
| using-relational-databases | `Skill: backend-data-skills:using-relational-databases` |
| assembling-components | `Skill: ui-assembly-skills:assembling-components` |

#### 7.3 Complete

Follow all instructions provided by the skill.
Answer questions, generate code, create files as directed.

#### 7.4 Report

```
Skill complete: {skill_name}
Files created: {list if any}
```

#### 7.5 Update Tracker

Update the execution tracker:

```
| # | Skill | Invocation | Status |
|---|-------|------------|--------|
| 1 | theming-components | ui-foundation-skills:theming-components | COMPLETE |
| 2 | building-forms | ui-input-skills:building-forms | INVOKE NOW |
| 3 | implementing-api-patterns | backend-api-skills:implementing-api-patterns | PENDING |
| 4 | assembling-components | ui-assembly-skills:assembling-components | PENDING |

Current: building-forms
Next Action: INVOKE
```

#### 7.6 Verify

```
Verification: Did I invoke {skill_name} using the Skill tool?
 YES - Proceeding to next skill
 NO  - Must invoke NOW before continuing
```

#### 7.7 Proceed

Move to the next skill in the chain and repeat from 7.1.

---

## Step 8: Generate Final Report

After all skills are executed:

```
Dynamic Skill Chain Complete

Goal: "{user_goal}"

Execution Summary:
  Skills Approved: {N}
  Skills Invoked: {M}
  Skills Skipped: {K}
  Activation Rate: {M/N * 100}%

Skills Executed:
  theming-components - Design tokens generated
  building-forms - Form components created
  implementing-api-patterns - API routes configured
  assembling-components - Components wired together

Files Generated:
  {list of files created}

Next Steps:
  1. Review generated files
  2. Install dependencies: {commands}
  3. Run development server: {command}
```

---

## Error Handling

### Skill Invocation Failure

```
Skill invocation failed: {skill_name}
Error: {message}

Options:
1. Retry invocation
2. Skip this skill (user must confirm)
3. Stop execution

Choice:
```

### User Requests Skip

```
Skip requested for: {skill_name}

This skill provides: {what it does}
Skipping may result in: {consequences}

Confirm skip? (yes/no)
```

Only mark as SKIPPED after user confirms. Update tracker accordingly.

---

## Skill Reference Table

Common skills and their invocations:

### Frontend Skills

| Skill | Invocation | Keywords |
|-------|------------|----------|
| theming-components | ui-foundation-skills:theming-components | theme, design tokens, dark mode |
| building-forms | ui-input-skills:building-forms | form, input, validation |
| building-tables | ui-data-skills:building-tables | table, grid, data display |
| creating-dashboards | ui-data-skills:creating-dashboards | dashboard, metrics, analytics |
| visualizing-data | ui-data-skills:visualizing-data | chart, graph, visualization |
| building-ai-chat | ui-interaction-skills:building-ai-chat | chat, AI, conversation |
| implementing-navigation | ui-structure-skills:implementing-navigation | nav, menu, routing |
| designing-layouts | ui-structure-skills:designing-layouts | layout, responsive, grid |
| assembling-components | ui-assembly-skills:assembling-components | assemble, wire, integrate |

### Backend Skills

| Skill | Invocation | Keywords |
|-------|------------|----------|
| implementing-api-patterns | backend-api-skills:implementing-api-patterns | API, REST, endpoints |
| using-relational-databases | backend-data-skills:using-relational-databases | database, SQL, postgres |
| using-vector-databases | backend-data-skills:using-vector-databases | vector, embeddings, RAG |
| securing-authentication | backend-platform-skills:securing-authentication | auth, login, JWT |
| implementing-observability | backend-platform-skills:implementing-observability | logging, metrics, tracing |

### Infrastructure Skills

| Skill | Invocation | Keywords |
|-------|------------|----------|
| kubernetes-operations | infrastructure-skills:kubernetes-operations | k8s, kubernetes, deploy |
| infrastructure-as-code | infrastructure-skills:infrastructure-as-code | terraform, IaC, AWS |
| building-ci-pipelines | devops-skills:building-ci-pipelines | CI/CD, pipeline, GitHub Actions |

---

## Summary

The dynamic orchestrator:

1. **Loads** all skill registries
2. **Scores** skills against user goal
3. **Resolves** dependencies and ordering
4. **Presents** chain for user approval
5. **Executes** each skill using the Skill tool
6. **Tracks** progress throughout
7. **Verifies** each invocation
8. **Reports** final activation rate

**Key principle:** Every approved skill MUST be invoked. No exceptions without explicit user consent.
