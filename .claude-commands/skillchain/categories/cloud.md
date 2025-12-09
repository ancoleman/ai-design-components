# Cloud Deployment Workflow Orchestrator

**Context Received:**
- Goal: {original_goal}
- Skills: {matched_skills}
- Category: cloud
- Estimated: {estimated_time}, {estimated_questions} questions

---

## Step 1: Load Shared Resources

Read `{SKILLCHAIN_DIR}/_shared/execution-flow.md`

Store in context for all skills.

**Note:** Cloud workflows do not require theming-rules.md (frontend-only).

---

## Step 2: Confirm Skill Chain with User

Present detected chain:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  SKILL CHAIN DETECTED FOR: "{original_goal}"             Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  MATCHED CLOUD PROVIDER SKILLS:                          Q
{for each matched skill with score > 0:}
Q    {n}. � {skill.name} (matched: "{keyword}")            Q
Q          Plugin: cloud-skills                           Q
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

**Important:** Users should typically only select ONE cloud provider skill per workflow.
If multiple cloud providers are detected, warn:

```
L WARNING: Multiple cloud providers detected

You've selected:
  - {provider_1}
  - {provider_2}

This will create deployment configurations for multiple clouds.
Is this intentional? (yes/no)

If "no" � Prompt user to select primary cloud provider
```

---

## Step 3: Skill Invocation Loop

**CRITICAL: You MUST use the Skill tool to invoke each skill. This is not documentation - it is a required action.**

Initialize:
```
skill_configs = {}
current_skill_index = 1
total_skills = len(confirmed_skills)
```

For each skill in confirmed_skills:

### 3.1 Announce Skill

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
 STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
 Plugin: cloud-provider-skills:{skill.name}
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

### 3.2 Invoke Skill Using the Skill Tool

**THIS IS A REQUIRED ACTION, NOT DOCUMENTATION.**

You MUST call the Skill tool for each cloud skill:

| Order | Skill | Tool Invocation | When |
|-------|-------|----------------|------|
| 1 | AWS Deployment | `Skill({ skill: "cloud-provider-skills:deploying-on-aws" })` | For AWS infrastructure |
| 2 | GCP Deployment | `Skill({ skill: "cloud-provider-skills:deploying-on-gcp" })` | For Google Cloud infrastructure |
| 3 | Azure Deployment | `Skill({ skill: "cloud-provider-skills:deploying-on-azure" })` | For Microsoft Azure infrastructure |

**Cloud skill invocation format (use plugin prefix `cloud-provider-skills:`):**
- `cloud-provider-skills:deploying-on-aws`
- `cloud-provider-skills:deploying-on-gcp`
- `cloud-provider-skills:deploying-on-azure`

**Execution Loop:**
1. **ANNOUNCE** the skill (print box above)
2. **INVOKE** using `Skill({ skill: "cloud-provider-skills:{skill.name}" })`
3. **FOLLOW** the skill's instructions when it loads
4. **TRACK** configuration answers in `skill_configs`
5. **PROCEED** to next skill

### 3.3 Load Questions

All cloud skills use `questions.source: "skill"` format.

Extract questions from the skill's "## Skillchain Configuration" section.

### 3.4 Ask User (unless skip_all_questions)

If skip_all_questions:
  Use defaults for all questions
Else:
  For each question in questions:
    Present question with:
      - Context from previous skills
      - Smart defaults based on goal keywords
      - Current answer if revisiting (for "back" command)
      - Cloud-specific best practices

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
  plugin: "cloud-skills",
  cloud_provider: skill.provider  # aws, gcp, or azure
}

current_skill_index += 1
```

---

## Step 4: Generate Cloud Deployment Output

**IMPORTANT:** Cloud workflows DO NOT use `assembling-components` skill (frontend-only).

Instead, generate cloud-specific Infrastructure as Code (IaC):

### 4.1 Analyze Collected Configurations

Review all `skill_configs` to identify:
- Target cloud provider(s) (AWS, GCP, Azure)
- Compute services (Lambda, Cloud Functions, Azure Functions, etc.)
- Storage services (S3, GCS, Blob Storage)
- Database services (RDS, Cloud SQL, Cosmos DB)
- Networking requirements (VPC, VNet, load balancers)
- Security configurations (IAM, roles, policies)
- Monitoring and logging setup

### 4.2 Identify Integration Points

Detect where cloud services need to interact:
- Application connections to cloud databases
- Storage integration with compute services
- IAM roles and permission policies
- Networking and security group configurations
- CI/CD pipeline integration
- Monitoring and alerting setup

### 4.3 Generate Production-Ready IaC

Create complete cloud deployment configuration:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  GENERATING CLOUD DEPLOYMENT FOR: "{original_goal}"      Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Cloud Provider: {cloud_provider}                        Q
Q  Based on configurations:                                Q
{for each skill in skill_configs:}
Q     {skill.name}: {summary of choices}                  Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]

Generating:
  1. Infrastructure as Code (Terraform/CloudFormation/ARM)
  2. Compute service configurations
  3. Database and storage setup
  4. Networking and security rules
  5. IAM roles and policies
  6. Monitoring and logging
  7. CI/CD pipeline configuration
  8. Environment-specific configs (dev/staging/prod)
```

### 4.4 Output Organization

Organize by cloud provider:

**For AWS:**
```
aws-deployment/
   terraform/               # Or cloudformation/
      main.tf
      variables.tf
      outputs.tf
      lambda.tf             # If using Lambda
      rds.tf                # If using RDS
      s3.tf                 # If using S3
   iam/
      policies.json
      roles.json
   scripts/
      deploy.sh
      teardown.sh
   .env.example
   README.md
```

**For GCP:**
```
gcp-deployment/
   terraform/               # Or deployment-manager/
      main.tf
      variables.tf
      outputs.tf
      cloud-functions.tf
      cloud-sql.tf
      gcs.tf
   iam/
      service-accounts.json
   scripts/
      deploy.sh
      teardown.sh
   .env.example
   README.md
```

**For Azure:**
```
azure-deployment/
   terraform/               # Or ARM templates/
      main.tf
      variables.tf
      outputs.tf
      functions.tf
      cosmos-db.tf
      blob-storage.tf
   rbac/
      roles.json
   scripts/
      deploy.sh
      teardown.sh
   .env.example
   README.md
```

### 4.5 Validation Checklist

Verify generated code includes:
- [ ] Infrastructure as Code files (Terraform/CloudFormation/ARM)
- [ ] Environment-specific variables
- [ ] IAM/RBAC configuration
- [ ] Networking and security groups
- [ ] Database connection strings and credentials management
- [ ] Storage bucket policies
- [ ] Monitoring and logging configuration
- [ ] CI/CD pipeline integration
- [ ] Cost optimization tags
- [ ] Deployment scripts
- [ ] README with deployment instructions

### 4.6 Present Output

Display generated artifacts with explanations:

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
  CLOUD DEPLOYMENT CONFIGURATION COMPLETE
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

Generated {file_count} files for {cloud_provider} deployment:

KEY FILES:
  =� {iac_main_file}            - Main infrastructure config
  =� {iam_config}               - IAM/RBAC permissions
  =� {network_config}           - VPC/networking setup
  =� {deploy_script}            - Deployment automation
  =� {env_example}              - Environment variables

ESTIMATED MONTHLY COST: ${estimated_cost}

NEXT STEPS:
  1. Review and customize infrastructure configuration
  2. Configure cloud provider credentials
  3. Update .env with your values
  4. Initialize IaC: {init_command}
  5. Plan deployment: {plan_command}
  6. Deploy: {deploy_command}

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
│ CLOUD SKILLCHAIN VALIDATION            │
├────────────────────────────────────────┤
│ Blueprint: {chain_context.blueprint}   │
│ Maturity: {chain_context.maturity}     │
│ Provider: {chain_context.cloud_provider}│
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
  "⚠️ Some cloud infrastructure components weren't fully generated:

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

### Cloud-Specific Validation Notes

When validating cloud deployments, pay special attention to:

**Infrastructure as Code:**
- Terraform/CloudFormation/ARM templates exist and have valid syntax
- Variable files include all required configuration
- Output files define necessary exports

**IAM/RBAC:**
- Role definitions exist for all services
- Policy documents have required permissions
- Service account configurations are present

**Networking:**
- VPC/VNet configurations exist
- Security group rules are defined
- Load balancer configurations are present (if required)

**Cost Optimization:**
- Resource tags are present for cost tracking
- Auto-scaling configurations exist (where applicable)
- Reserved instance recommendations included (for production)

---

## Error Handling

### Skill Invocation Failure

If skill invocation fails:

```
�  ERROR: Skill '{skill.name}' failed to load

Plugin: cloud-skills:{skill.name}
Reason: {error_message}

Options:
1. Continue with remaining skills (skip this one)
2. Retry this skill
3. Stop workflow and show partial progress

Your choice (1/2/3):
```

Handle user choice:
- 1 � Mark skill as skipped, continue to next skill
- 2 � Re-invoke skill
- 3 � Stop loop, proceed to Step 4 with partial configs

### Cloud Provider Conflicts

Detect when user has selected conflicting cloud providers:

```
�  CLOUD PROVIDER CONFLICT DETECTED

Multiple exclusive cloud providers selected:
  - AWS
  - GCP

These cannot be used together in a single deployment.

Options:
1. Deploy to AWS only
2. Deploy to GCP only
3. Create separate deployments for each provider
4. Go back and reconfigure

Your choice (1/2/3/4):
```

### Missing Cloud Credentials

When generating deployment scripts:

```
L REMINDER: Cloud Credentials Required

To deploy, you'll need to configure credentials for {cloud_provider}.

Instructions included in:
  - README.md � "Setting up credentials" section
  - .env.example � Required environment variables

Continue? (yes/no)
```

---

**Orchestrator Complete**
