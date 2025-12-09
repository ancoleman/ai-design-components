# Infrastructure Workflow Orchestrator

**Context Received:**
- Goal: {original_goal}
- Skills: {matched_skills}
- Category: infrastructure
- Estimated: {estimated_time}, {estimated_questions} questions

---

## Step 1: Load Shared Resources

Read `{SKILLCHAIN_DIR}/_shared/execution-flow.md`

Store in context for all skills.

**Note:** Infrastructure workflows do not require theming-rules.md (frontend-only).

---

## Step 2: Confirm Skill Chain with User

Present detected chain:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  SKILL CHAIN DETECTED FOR: "{original_goal}"             Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  MATCHED INFRASTRUCTURE SKILLS:                          Q
{for each matched skill with score > 0:}
Q    {n}. � {skill.name} (matched: "{keyword}")            Q
Q          Priority: {skill.priority}                      Q
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
 Namespace: infrastructure-skills:{skill.name}
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

### 3.2 Invoke Skill

**CRITICAL: YOU MUST USE THE SKILL TOOL TO INVOKE EACH SKILL.**

**THIS IS A REQUIRED ACTION, NOT DOCUMENTATION.**

Use the Skill tool with the exact plugin-prefixed skill name:

| Skill Name | Tool Invocation |
|------------|----------------|
| operating-kubernetes | `Skill({ skill: "infrastructure-skills:operating-kubernetes" })` |
| writing-infrastructure-code | `Skill({ skill: "infrastructure-skills:writing-infrastructure-code" })` |
| administering-linux | `Skill({ skill: "infrastructure-skills:administering-linux" })` |
| architecting-networks | `Skill({ skill: "infrastructure-skills:architecting-networks" })` |
| load-balancing-patterns | `Skill({ skill: "infrastructure-skills:load-balancing-patterns" })` |
| planning-disaster-recovery | `Skill({ skill: "infrastructure-skills:planning-disaster-recovery" })` |
| configuring-nginx | `Skill({ skill: "infrastructure-skills:configuring-nginx" })` |
| shell-scripting | `Skill({ skill: "infrastructure-skills:shell-scripting" })` |
| managing-dns | `Skill({ skill: "infrastructure-skills:managing-dns" })` |
| implementing-service-mesh | `Skill({ skill: "infrastructure-skills:implementing-service-mesh" })` |
| managing-configuration | `Skill({ skill: "infrastructure-skills:managing-configuration" })` |
| designing-distributed-systems | `Skill({ skill: "infrastructure-skills:designing-distributed-systems" })` |

**EXECUTION SEQUENCE (MANDATORY):**

1. **ANNOUNCE** - Display skill header box (3.1)
2. **INVOKE** - Call Skill tool with "devops-skills:{skill-name}"
3. **FOLLOW** - Execute ALL instructions from loaded skill
4. **TRACK** - Store configuration in skill_configs (3.5)
5. **PROCEED** - Move to next skill or Step 4

**Example for operating-kubernetes:**
```
Step 1/3: ANNOUNCE
┌─────────────────────────────────────────────┐
│ STEP 1/3: operating-kubernetes              │
│ Namespace: infrastructure-skills:operating-kubernetes│
└─────────────────────────────────────────────┘

Step 2/3: INVOKE
Skill({ skill: "infrastructure-skills:operating-kubernetes" })

Step 3/3: FOLLOW
[Execute all instructions from skill's SKILL.md]
[Ask configuration questions if not skip_all_questions]

Step 4/3: TRACK
skill_configs["operating-kubernetes"] = { ... }

Step 5/3: PROCEED
current_skill_index = 2
[Move to next skill]
```

**FAILURE TO INVOKE = WORKFLOW FAILURE**

### 3.3 Load Questions

All infrastructure skills use `questions.source: "skill"` format.

```python
# Read from SKILL.md in the plugin
skill_md_path = f"/mnt/skills/public/infrastructure-skills/{skill.name}/SKILL.md"
skill_md = Read(skill_md_path)

# Extract "## Skillchain Configuration" section
section_content = extract_section(skill_md, "## Skillchain Configuration")

# Parse questions from markdown
questions = parse_questions(section_content)
```

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
  dependencies: skill.dependencies
}

current_skill_index += 1
```

---

## Step 4: Generate Infrastructure Output

**IMPORTANT:** Infrastructure workflows generate declarative configuration files and automation scripts.

### 4.1 Analyze Collected Configurations

Review all `skill_configs` to identify:
- Infrastructure provisioning tools (Terraform, Ansible, Pulumi)
- Kubernetes manifests and Helm charts
- Network architecture and segmentation
- Load balancing and traffic management
- DNS and service discovery configuration
- Disaster recovery and backup strategies
- Linux system configuration and services
- Shell automation scripts
- Service mesh configuration (if applicable)

### 4.2 Identify Integration Points

Detect where infrastructure components interact:
- Kubernetes clusters and networking (VPC, subnets)
- Load balancers and ingress controllers
- DNS records and service endpoints
- Service mesh and Kubernetes services
- IaC modules and network resources
- Configuration management and Linux hosts
- Disaster recovery and backup automation

### 4.3 Generate Production-Ready Infrastructure

Create complete infrastructure configuration:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  GENERATING INFRASTRUCTURE FOR: "{original_goal}"        Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Based on configurations:                                Q
{for each skill in skill_configs:}
Q     {skill.name}: {summary of choices}                  Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]

Generating:
  1. Infrastructure as Code (Terraform/Ansible)
  2. Kubernetes manifests and Helm charts
  3. Network configuration and security groups
  4. Load balancer and ingress configuration
  5. DNS records and zone files
  6. Shell automation scripts
  7. Service mesh configuration (if applicable)
  8. Disaster recovery runbooks
```

### 4.4 Output Organization

Organize infrastructure code by component type:

**For Kubernetes-focused infrastructure:**
```
infrastructure/
   terraform/         # Cloud resource provisioning
      main.tf
      network.tf
      kubernetes.tf
      variables.tf
   k8s/               # Kubernetes manifests
      base/
      overlays/
      helm/
   scripts/           # Automation scripts
      setup.sh
      backup.sh
      deploy.sh
   docs/
      architecture.md
      runbooks/
```

**For Multi-tier infrastructure:**
```
infrastructure/
   terraform/         # IaC modules
      network/
      compute/
      storage/
   ansible/           # Configuration management
      playbooks/
      roles/
      inventory/
   nginx/             # Web server configs
      conf.d/
      ssl/
   dns/               # DNS zone files
   scripts/           # Shell automation
   disaster-recovery/ # DR plans and scripts
```

### 4.5 Validation Checklist

Verify generated infrastructure includes:
- [ ] All resources properly namespaced/tagged
- [ ] Network segmentation and security groups
- [ ] High availability and redundancy where needed
- [ ] Monitoring and health checks configured
- [ ] Secrets management (not hardcoded)
- [ ] Disaster recovery procedures documented
- [ ] Automation scripts are idempotent
- [ ] Documentation for runbooks and operations
- [ ] Cost optimization considerations noted
- [ ] Compliance and security best practices

### 4.6 Present Output

Display generated files with explanations:

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
  INFRASTRUCTURE CONFIGURATION COMPLETE
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

Generated {file_count} files across {skill_count} infrastructure skills:

KEY FILES:
  =� {terraform_main}            - Core infrastructure resources
  =� {k8s_manifests}             - Kubernetes deployment specs
  =� {network_config}            - Network architecture
  =� {lb_config}                 - Load balancer configuration
  =� {automation_scripts}        - Setup and deployment scripts

NEXT STEPS:
  1. Review generated configurations
  2. Update variables.tf with your values
  3. Initialize: {init_command}
  4. Plan: {plan_command}
  5. Apply: {apply_command}

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
│ INFRASTRUCTURE SKILLCHAIN VALIDATION   │
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
  "⚠️ Some infrastructure components weren't fully generated:

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

### Skill Invocation Failure

If skill invocation fails:

```
�  ERROR: Skill '{skill.name}' failed to load

Invocation: {skill.invocation}
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

Example: implementing-service-mesh requires operating-kubernetes

We'll note this dependency in the generated configuration.
Continue? (yes/no)
```

If "no" � Allow user to go back and configure dependency

### Configuration Conflicts

Detect incompatible infrastructure choices:

```
�  CONFIGURATION CONFLICT DETECTED

writing-infrastructure-code specified: Terraform
managing-configuration specified: Ansible

For consistency, consider:
1. Use Terraform for all provisioning (recommended for cloud)
2. Use Ansible for all configuration (recommended for on-prem)
3. Use both (Terraform for infra, Ansible for config)

Your choice (1/2/3):
```

### Missing Critical Configuration

If essential infrastructure components are missing:

```
�  WARNING: Kubernetes manifests without network configuration

architecting-networks was not selected. This may cause issues with:
- Pod networking and CNI plugins
- Service discovery and DNS
- Ingress and load balancer connectivity

Options:
1. Add architecting-networks skill (recommended)
2. Continue (assume default network configuration)
3. Go back and review skill selection

Your choice (1/2/3):
```

---

**Orchestrator Complete - Lines: ~195**
