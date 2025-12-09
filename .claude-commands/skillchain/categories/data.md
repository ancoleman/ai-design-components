# Data Engineering Workflow Orchestrator

**Context Received:**
- Goal: {original_goal}
- Skills: {matched_skills}
- Category: data-engineering
- Estimated: {estimated_time}, {estimated_questions} questions

---

## Step 1: Load Shared Resources

Read `{SKILLCHAIN_DIR}/_shared/execution-flow.md`

Store in context for all skills.

**Note:** Data engineering workflows do not require theming-rules.md (frontend-only).

---

## Step 2: Confirm Skill Chain with User

Present detected chain:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  SKILL CHAIN DETECTED FOR: "{original_goal}"             Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  MATCHED DATA ENGINEERING SKILLS:                        Q
{for each matched skill with score > 0:}
Q    {n}. � {skill.name} (matched: "{keyword}")            Q
Q          Plugin: data-engineering-skills                Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Estimated time: {estimated_time}                        Q
Q  Estimated questions: {estimated_questions}              Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  OPTIONS:                                                Q
Q    " Type "confirm" to proceed                           Q
Q    " Type "skip" to use all defaults (faster)            Q
Q    " Type "customize" to add/remove skills               Q
Q    " Type "help" to see workflow commands                Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]
```

Wait for user response:
- "confirm" � Proceed to Step 3
- "skip" � Set skip_all_questions = true, proceed to Step 3
- "customize" � Allow skill additions/removals, then proceed
- "help" � Show workflow commands from execution-flow.md

---

## Step 3: Skill Invocation Loop

**CRITICAL: You MUST use the Skill tool to invoke each skill.**

This is NOT documentation about skills. This is a REQUIRED ACTION.
You MUST execute: `Skill({ skill: "data-engineering-skills:{skill-name}" })`

Initialize:
```
skill_configs = {}
current_skill_index = 1
total_skills = len(confirmed_skills)
```

### Available Data Engineering Skills

**THIS IS A REQUIRED ACTION, NOT DOCUMENTATION.**

| Order | Skill Name | Tool Invocation | When |
|-------|------------|----------------|------|
| 1 | Architecting Data | `Skill({ skill: "data-engineering-skills:architecting-data" })` | Data warehouse/lake design |
| 2 | Streaming Data | `Skill({ skill: "data-engineering-skills:streaming-data" })` | Kafka, Kinesis, real-time pipelines |
| 3 | Transforming Data | `Skill({ skill: "data-engineering-skills:transforming-data" })` | ETL/ELT, dbt, Airflow |
| 4 | Optimizing SQL | `Skill({ skill: "data-engineering-skills:optimizing-sql" })` | Query tuning, indexes |
| 5 | Secret Management | `Skill({ skill: "data-engineering-skills:secret-management" })` | Vault, credentials |
| 6 | Performance Engineering | `Skill({ skill: "data-engineering-skills:performance-engineering" })` | Monitoring, scaling |

For each skill in confirmed_skills:

### 3.1 Announce Skill

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
 STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
 Plugin: data-engineering-skills:{skill.name}
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

### 3.2 Invoke Skill (REQUIRED ACTION)

**YOU MUST EXECUTE THE SKILL TOOL NOW:**

```
Skill({ skill: "data-engineering-skills:{skill.name}" })
```

**Example invocations (pick the correct one for current skill):**
- `Skill({ skill: "data-engineering-skills:architecting-data" })`
- `Skill({ skill: "data-engineering-skills:streaming-data" })`
- `Skill({ skill: "data-engineering-skills:transforming-data" })`
- `Skill({ skill: "data-engineering-skills:optimizing-sql" })`
- `Skill({ skill: "data-engineering-skills:secret-management" })`
- `Skill({ skill: "data-engineering-skills:performance-engineering" })`

**THIS IS NOT OPTIONAL. You must invoke the Skill tool before proceeding.**

### 3.3 Follow Skill Instructions

After invoking the skill:
1. **Read** the loaded skill content carefully
2. **Extract** questions from "## Skillchain Configuration" section
3. **Follow** any skill-specific instructions
4. **Use** skill-provided references/scripts as directed

### 3.4 Ask User (unless skip_all_questions)

If skip_all_questions:
  Use defaults for all questions
Else:
  For each question in questions:
    Present question with:
      - Context from previous skills
      - Smart defaults based on goal keywords
      - Current answer if revisiting (for "back" command)
      - Dependency information if applicable

    Wait for answer or workflow command:
      - Answer � Store and continue
      - "skip" � Use default for this question
      - "back" � Return to previous skill
      - "status" � Show progress, re-ask question
      - "done" � Break loop, proceed to assembly
      - "restart" � Go back to Step 2

### 3.5 Store Configuration

```
skill_configs[skill.name] = {
  answers: user_answers,
  invocation: skill.invocation,
  priority: skill.priority,
  plugin: "data-engineering-skills",
  dependencies: skill.dependencies
}

current_skill_index += 1
```

---

### Execution Loop Summary

For each skill, follow this pattern:

1. **ANNOUNCE** the skill (Step 3.1)
2. **INVOKE** using Skill tool (Step 3.2) ← **REQUIRED ACTION**
3. **FOLLOW** the loaded skill instructions (Step 3.3)
4. **TRACK** configuration answers (Step 3.4-3.5)
5. **PROCEED** to next skill

**Remember:** The Skill tool invocation is NOT documentation. It is a REQUIRED ACTION that loads the skill into context.

---

## Step 4: Generate Data Pipeline Output

**IMPORTANT:** Data engineering workflows DO NOT use `assembling-components` skill (frontend-only).

Instead, generate data pipeline code directly:

### 4.1 Analyze Collected Configurations

Review all `skill_configs` to identify:
- Data architecture patterns (warehouse, lake, lakehouse)
- Streaming requirements (Kafka, Kinesis, Pub/Sub)
- Transformation workflows (dbt, Airflow, Dagster)
- SQL optimization needs (indexes, query tuning)
- Secret management approach (Vault, AWS Secrets Manager)
- Performance optimization strategies

### 4.2 Identify Integration Points

Detect where skills need to interact:
- Data ingestion feeding into warehouse/lake
- Streaming data connecting to transformation pipelines
- Secret management for database credentials
- Performance tuning for SQL-based transformations
- Orchestration patterns across all components

### 4.3 Generate Production-Ready Code

Create complete data engineering implementation:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  GENERATING DATA PIPELINE FOR: "{original_goal}"         Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Based on configurations:                                Q
{for each skill in skill_configs:}
Q     {skill.name}: {summary of choices}                  Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]

Generating:
  1. Data architecture schemas and DDL
  2. Streaming pipeline configuration
  3. ETL/ELT transformation jobs
  4. SQL optimization scripts
  5. Secret management configuration
  6. Performance monitoring setup
  7. Orchestration DAGs
  8. Docker/K8s deployment configs
```

### 4.4 Output Organization

Organize by data engineering pattern:

```
data-pipeline/
   architecture/       # Schemas, ER diagrams
   streaming/          # Kafka/Kinesis configs
   transforms/         # dbt, Airflow, Dagster
   sql/                # Optimized queries, procedures
   config/             # Environment, secrets
   monitoring/         # Performance dashboards
   tests/              # Data quality tests
   docker-compose.yml
   k8s/                # Kubernetes manifests
   .env.example
   README.md
```

### 4.5 Validation Checklist

Verify generated code includes:
- [ ] Data architecture documentation (schemas, relationships)
- [ ] Streaming pipelines properly configured
- [ ] Transformation logic tested and validated
- [ ] SQL queries optimized with explain plans
- [ ] Secrets properly externalized
- [ ] Performance monitoring instrumentation
- [ ] Data quality checks and tests
- [ ] Orchestration DAGs for scheduling
- [ ] Environment variables documented
- [ ] Docker/K8s configs if requested

### 4.6 Present Output

Display generated artifacts with explanations:

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
  DATA PIPELINE IMPLEMENTATION COMPLETE
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

Generated {file_count} files across {skill_count} data engineering skills:

KEY FILES:
  =� {architecture_file}       - Data warehouse/lake design
  =� {streaming_config}         - Kafka/Kinesis setup
  =� {transform_dag}            - Airflow/dbt pipeline
  =� {sql_optimizations}        - Tuned queries and indexes
  =� {secrets_config}           - Secret management setup

NEXT STEPS:
  1. Review data architecture and schemas
  2. Configure environment variables and secrets
  3. Test streaming pipeline: {stream_test_cmd}
  4. Run transformations: {transform_cmd}
  5. Monitor performance: {monitoring_url}

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

---

## Step 5: Finalize and Document

After generating the data pipeline, complete the skillchain:

### Present Final Summary

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
  DATA ENGINEERING SKILLCHAIN COMPLETE
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

Goal: "{original_goal}"

Skills executed: {total_skills}
{for each skill in skill_configs:}
  {n}. {skill.name}
      Plugin: data-engineering-skills

Generated output:
  {file_count} files
  {dir_count} directories

Key deliverables:
  - Data architecture: {architecture_summary}
  - Streaming pipelines: {streaming_summary}
  - Transformation jobs: {transform_summary}
  - SQL optimizations: {sql_summary}
  - Secret management: {secrets_summary}

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
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
│ DATA SKILLCHAIN VALIDATION             │
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
  "⚠️ Some data pipeline components weren't fully generated:

   Missing:
   [list deliverables where status == "missing"]

   Common missing items:
   - Data architecture schemas/ERDs
   - dbt transformation models
   - Airflow DAGs or orchestration configs
   - Kafka/streaming pipeline setup
   - Data quality test suites
   - SQL query optimization scripts

   Would you like me to:
   A) Generate the missing components
   B) Continue without them
   C) See detailed validation report"

  If user chooses A:
    For each missing deliverable:
      Invoke primary_skill for that deliverable
    Re-run validation (go back to "Run Chain Validation")
```

**Data-specific validation notes:**

- **dbt models:** Check for models/*.sql files with proper {{ref()}} syntax
- **Airflow DAGs:** Verify DAG files have proper imports and task definitions
- **Kafka configs:** Validate topic configurations and consumer/producer setup
- **Data quality:** Look for dbt tests or Great Expectations suites
- **Schemas:** Verify SQL DDL files or schema.yml definitions

---

## Error Handling

### Skill Invocation Failure

If skill invocation fails:

```
�  ERROR: Skill '{skill.name}' failed to load

Plugin: data-engineering-skills:{skill.name}
Reason: {error_message}

Options:
1. Continue with remaining skills (skip this one)
2. Retry this skill
3. Stop workflow and show partial progress

Your choice (1/2/3):
```

Handle user choice:
- 1 � Mark skill as skipped, continue to next skill
- 2 � Re-invoke skill, reset current_skill_index
- 3 � Stop loop, proceed to Step 4 with partial configs

### Dependency Failures

When a dependent skill was skipped/failed:

```
�  WARNING: '{skill.name}' depends on '{dependency}' which was skipped.

We'll use default configuration for {dependency} integration.
Continue? (yes/no)
```

If "no" � Allow user to go back and configure dependency

### Invalid Configuration Combinations

Detect incompatible choices:

```
�  CONFIGURATION CONFLICT DETECTED

architecting-data specified: Data Lake (S3)
transforming-data specified: dbt (requires warehouse)

Recommendation:
1. Use data lakehouse (best of both)
2. Keep separate architectures
3. Go back and reconfigure

Your choice (1/2/3):
```

---

**Orchestrator Complete**
