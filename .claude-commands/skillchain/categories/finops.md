# FinOps Category Orchestrator

Handles cloud cost optimization and financial operations workflows.

---

## Step 1: Load Shared Resources

Read execution-flow.md for general workflow guidance:

```
Read {SKILLCHAIN_DIR}/_shared/execution-flow.md
```

**Note:** FinOps workflows focus on cost optimization and do not require theming-rules.md.

---

## Step 2: Detect FinOps Pattern

Analyze the user goal to determine the FinOps pattern:

### Pattern Detection Rules

**Cost Optimization Only:**
- Cost reduction
- Right-sizing resources
- Reserved instances
- Spot instances
- Waste identification

**Tagging Strategy Only:**
- Tag implementation
- Cost allocation
- Chargeback/showback setup
- Resource metadata

**Combined FinOps (Both Skills):**
- Complete cost management
- Cost visibility + optimization
- Budget enforcement with tagging

### Pattern-Specific Skill Chains

**Pattern: Cost Optimization**
```
Skills: optimizing-costs
Optional: resource-tagging (for cost attribution)
```

**Pattern: Tagging Strategy**
```
Skills: resource-tagging
Optional: optimizing-costs (for cost-aware tagging)
```

**Pattern: Complete FinOps**
```
Skills: optimizing-costs → resource-tagging
```

---

## Step 3: Confirm Chain

Present the detected pattern and skill chain to the user:

```
>═ FinOps Skill Chain Detected

Pattern: [Cost Optimization / Tagging Strategy / Complete FinOps]

I'll guide you through these skills:

[If cost optimization only:]
1. optimizing-costs → Configure cost reduction strategies

[If tagging only:]
1. resource-tagging → Set up tag strategy and enforcement

[If complete FinOps:]
1. optimizing-costs → Configure cost reduction strategies
2. resource-tagging → Set up tag strategy for cost allocation

Estimated questions: [X]
Estimated time: [Y] minutes

Options:
  • Type "confirm" to proceed
  • Type "skip" to use all defaults (faster)
  • Type "customize" to add/remove skills
  • Type "help" to see workflow commands

Your choice:
```

Wait for user response:
- "confirm" → Proceed to Step 4
- "skip" → Set skip_all_questions = true, proceed to Step 4
- "customize" → Allow skill additions/removals, then proceed
- "help" → Show workflow commands from execution-flow.md

---

## Step 4: Execute Skills

**CRITICAL: You MUST use the Skill tool to invoke each skill. This is NOT documentation - you MUST execute these tool calls.**

Initialize:
```
skill_configs = {}
current_skill_index = 1
total_skills = len(confirmed_skills)
skip_all_questions = false
```

### FinOps Skills Reference

| Order | Skill | Tool Invocation | When |
|-------|-------|-----------------|------|
| 1 | Optimizing Costs | `Skill({ skill: "finops-skills:optimizing-costs" })` | Cost reduction, right-sizing, RI/Spot, waste |
| 2 | Resource Tagging | `Skill({ skill: "finops-skills:resource-tagging" })` | Cost allocation, chargeback, tag enforcement |

**THIS IS A REQUIRED ACTION, NOT DOCUMENTATION. You MUST invoke each skill using the Skill tool.**

For each skill in confirmed_skills:

### 4.1 Announce Skill

```
═══════════════════════════════════════════════════════════
 FINOPS STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
 Plugin: finops-skills:{skill.name}
═══════════════════════════════════════════════════════════
```

### 4.2 Invoke Skill (REQUIRED ACTION)

**YOU MUST USE THE SKILL TOOL NOW. This is the execution phase.**

For each skill, follow this execution loop:

1. **ANNOUNCE**: Print the skill step header (Step 4.1)
2. **INVOKE**: Use the Skill tool with the exact invocation from the table above
3. **FOLLOW**: Process the skill's instructions when they load
4. **TRACK**: Store configuration in skill_configs
5. **PROCEED**: Move to next skill

**Example execution for optimizing-costs:**
```
Step 1 - ANNOUNCE:
═══════════════════════════════════════════════════════════
 FINOPS STEP 1/2: OPTIMIZING COSTS
 Plugin: finops-skills:optimizing-costs
═══════════════════════════════════════════════════════════

Step 2 - INVOKE (USE THE SKILL TOOL):
Skill({ skill: "finops-skills:optimizing-costs" })

Step 3 - FOLLOW:
[Process the skill's loaded instructions]

Step 4 - TRACK:
skill_configs["optimizing-costs"] = {...}

Step 5 - PROCEED:
Move to finops-skills:resource-tagging
```

**FinOps skill invocations (copy exactly):**
- `finops-skills:optimizing-costs`
- `finops-skills:resource-tagging`

### 4.3 Load Questions

All FinOps skills use `questions.source: "skill"` format.

```python
# Read from SKILL.md in the plugin
skill_md_path = f"/mnt/skills/public/finops-skills/{skill.name}/SKILL.md"
skill_md = Read(skill_md_path)

# Extract section specified in registry
section_name = "## Skillchain Configuration"
section_content = extract_section(skill_md, section_name)

# Parse questions from markdown
questions = parse_questions(section_content)
```

### 4.4 Ask User (unless skip_all_questions)

If skip_all_questions:
  Use defaults for all questions
Else:
  For each question in questions:
    Present question with:
      - Context from previous skills
      - Smart defaults based on goal keywords
      - Cloud provider detection from goal
      - Current answer if revisiting (for "back" command)

    Wait for answer or workflow command:
      - Answer → Store and continue
      - "skip" → Use default for this question
      - "back" → Return to previous skill
      - "status" → Show progress, re-ask question
      - "done" → Break loop, proceed to output generation
      - "restart" → Go back to Step 3

### 4.5 Store Configuration

```
skill_configs[skill.name] = {
  answers: user_answers,
  invocation: skill.invocation,
  priority: skill.priority,
  plugin: skill.plugin_namespace
}

current_skill_index += 1
```

---

## Step 5: Generate FinOps Output

After all skills are configured, generate FinOps-specific deliverables:

### For Cost Optimization

Generate:
1. **Cost analysis report** - Current spend breakdown
2. **Right-sizing recommendations** - Instance/resource changes
3. **Reserved instance plan** - RI/SP purchase strategy
4. **Spot instance integration** - Fault-tolerant workload migration
5. **Waste identification** - Idle/unused resources
6. **Implementation scripts** - Automation for cost reductions

### For Tagging Strategy

Generate:
1. **Tag schema definition** - Required and optional tags
2. **Tag policies** - AWS/Azure/GCP policy-as-code
3. **Enforcement automation** - Lambda/Functions for compliance
4. **Cost allocation reports** - Tag-based cost attribution
5. **Chargeback/showback templates** - Business reporting

### For Complete FinOps

Combine outputs from both skills with integration:
1. Cost optimization strategies tagged by initiative
2. Tag-based cost tracking for optimization impact
3. Automated reporting combining spend and allocation

### Output Format

```
═ FinOps Skill Chain Complete!

Summary:
- Cloud Provider: [AWS/Azure/GCP/Multi-cloud]
- Cost Optimization Focus: [Right-sizing/RI/Spot/Waste]
- Tagging Strategy: [Cost allocation/Chargeback/Compliance]
- Estimated Monthly Savings: [X%] (~$Y/month)

Generated:
═► finops/
     cost-optimization/
        analysis-report.md        # Current cost breakdown
        recommendations.csv       # Action items with savings
        rightsizing-script.py     # Automation for resizing
        ri-purchase-plan.md       # RI/SP strategy
        spot-migration.yaml       # Spot integration config
     tagging/
        tag-schema.yaml           # Tag definitions
        tag-policies/
           aws-policy.json        # AWS tag enforcement
           azure-policy.json      # Azure tag policy
           gcp-policy.yaml        # GCP org policy
        enforcement/
           tag-enforcer.py        # Auto-tagging Lambda
           compliance-check.py    # Tag compliance scanner
     reports/
        cost-allocation.sql       # Tag-based cost queries
        chargeback-template.xlsx  # Business reporting

Key Metrics:
✓ Identified $X/month in savings opportunities
✓ [Y] resources recommended for right-sizing
✓ [Z] idle resources for decommissioning
✓ Tag schema covers [N] cost dimensions
✓ Compliance enforcement: [automated/manual]

Implementation Steps:
1. Review cost analysis report and validate findings
2. Approve right-sizing recommendations
3. Execute RI/SP purchase plan (if applicable)
4. Deploy tag policies to cloud accounts
5. Run tag enforcement automation
6. Set up cost allocation reports
7. Monitor savings and tag compliance weekly

Would you like me to:
A) Generate the full implementation code
B) Explain any recommendation in detail
C) Modify cost thresholds or tag schema
D) Add observability for FinOps metrics
```

---

## Step 5.5: Validate Chain Outputs

After all skills have executed, validate the combined output:

### Load Validation Logic

```
Read {SKILLCHAIN_DATA}/shared/validation.md
```

### Per-Skill Output Validation

For each skill that was invoked:
```
skill_outputs = Read {SKILLS_DIR}/{skill_name}/outputs.yaml
For each output in skill_outputs.base_outputs:
  If NOT exists {project_path}/{output.path}:
    Mark as missing, log for user
  Else if output.must_contain exists:
    Check file contains expected patterns
```

### Run Chain Validation

```
If chain_context.blueprint exists:
  # Option 1: Use completeness checker script
  Run: python scripts/runtime/completeness_checker.py {project_path} --blueprint {blueprint} --maturity {maturity}

  # Option 2: Manual validation (if script not available)
  # Load blueprint deliverables
  Read {SKILLCHAIN_CMD}/blueprints/{chain_context.blueprint}.md
  Parse "## Deliverables Specification" section

  # Apply maturity adjustments
  For each deliverable in deliverables:
    If deliverable.maturity_required exists:
      If chain_context.maturity NOT in deliverable.maturity_required:
        Mark deliverable as "skipped"

  # Validate each required deliverable
  For each deliverable NOT skipped:
    result = validate_deliverable(deliverable, chain_context.project_path)
    chain_context.deliverables_status[deliverable.name] = result

  # Calculate completeness
  required_count = count(deliverables where status != "skipped")
  fulfilled_count = count(deliverables where status == "fulfilled")
  completeness = fulfilled_count / required_count

Else:
  # No blueprint - run basic completeness check
  Run run_basic_completeness_check(chain_context.project_path)
```

### Generate Validation Report

```
┌────────────────────────────────────────┐
│ FINOPS SKILLCHAIN VALIDATION           │
├────────────────────────────────────────┤
│ Blueprint: {chain_context.blueprint}   │
│ Maturity: {chain_context.maturity}     │
├────────────────────────────────────────┤
For each deliverable in chain_context.deliverables_status:
  If status == "fulfilled": │ ✓ {name}
  If status == "missing":   │ ✗ {name} - MISSING
  If status == "skipped":   │ ○ {name} (skipped - {maturity})
├────────────────────────────────────────┤
│ Required: {required_count}             │
│ Fulfilled: {fulfilled_count}           │
│ Completeness: {completeness}%          │
└────────────────────────────────────────┘
```

### Handle Missing Deliverables

```
If completeness < 80%:
  "⚠️ Some FinOps components weren't fully generated:

   Missing:
   [list deliverables where status == "missing"]

   Would you like me to:
   A) Generate the missing components
   B) Continue without them
   C) See detailed validation report"

  If user chooses A:
    For each missing deliverable:
      Invoke primary_skill for that deliverable
    Re-run validation (go back to "Run Chain Validation")
```

---

## Error Handling

### Skill Load Failures

If a FinOps skill fails to load:

```
⚠ ERROR: Skill '[skill-name]' failed to load

Reason: [error message]

Options:
1. Retry this skill
2. Continue without (manual FinOps analysis)
3. Stop and investigate

Your choice (1/2/3):
```

### Cloud Provider Detection

If cloud provider is unclear from goal:

```
⚠ Cloud Provider Unclear

Your goal mentions: "[user keywords]"

Which cloud provider(s) are you using?
A) AWS
B) Azure
C) GCP
D) Multi-cloud (select which)

Choose A/B/C/D:
```

### Configuration Conflicts

If user selections conflict (e.g., AWS-specific + GCP goal):

```
⚠ CONFIGURATION CONFLICT

optimizing-costs: AWS-specific recommendations (Reserved Instances)
User goal: "reduce GCP costs"

Recommendation:
- Use GCP-appropriate cost optimization (Committed Use Discounts)
- Adjust recommendations for GCP pricing model

Which approach?
A) Switch to GCP cost optimization strategies
B) Keep AWS focus (ignore GCP mention)
C) Generate multi-cloud cost optimization
```

---

## FinOps-Specific Guidelines

### 1. Cloud Provider Consistency
Ensure all FinOps recommendations match the detected cloud provider(s).

### 2. Savings Estimates
Always provide conservative savings estimates with confidence ranges.

### 3. Tag Schema Design
- Include mandatory tags: cost-center, environment, owner, project
- Support custom business dimensions
- Enforce at infrastructure deployment time

### 4. Cost Allocation Hierarchy
Align tags with organizational structure for accurate chargeback/showback.

### 5. Automation First
Generate scripts/policies for enforcement, not just documentation.

### 6. Integration with Existing Workflows
Reference infrastructure-as-code practices for tag enforcement at deployment.

---

## Summary

**FinOps orchestrator responsibilities:**
1. Detect cost optimization vs tagging vs complete FinOps patterns
2. Load execution-flow.md for workflow guidance
3. Present appropriate skill chain for FinOps use case
4. Execute skills in logical order (optimization → tagging)
5. Generate actionable FinOps deliverables (reports, scripts, policies)
6. Validate chain outputs against blueprint deliverables (Step 5.5)
7. Validate configurations for cloud provider consistency
8. Provide implementation guidance and savings estimates

**Key differences from other categories:**
- Focus on cost savings and financial accountability
- Cloud provider-specific recommendations
- Generates policies and enforcement automation
- Includes savings estimates and ROI calculations
- Integration with business reporting requirements
