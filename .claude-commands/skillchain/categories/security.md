# Security Workflow Orchestrator

**Context Received:**
- Goal: {original_goal}
- Skills: {matched_skills}
- Category: security
- Estimated: {estimated_time}, {estimated_questions} questions

---

## Step 1: Load Shared Resources

Read `{SKILLCHAIN_DIR}/_shared/execution-flow.md`

Store in context for all skills.

**Note:** Security workflows do not require theming-rules.md (frontend-only).

---

## Step 2: Confirm Skill Chain with User

Present detected chain:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  SKILL CHAIN DETECTED FOR: "{original_goal}"             Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  MATCHED SECURITY SKILLS:                                Q
{for each matched skill with score > 0:}
Q    {n}. � {skill.name} (matched: "{keyword}")            Q
Q          Plugin: {skill.plugin_namespace}               Q
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

**THIS IS A REQUIRED ACTION, NOT DOCUMENTATION.**

Each skill invocation loads specialized security knowledge and capabilities. You must actively call the Skill tool for each matched skill in the chain.

Initialize:
```
skill_configs = {}
current_skill_index = 1
total_skills = len(confirmed_skills)
```

### Security Skills Execution Table

| Order | Skill | Tool Invocation | When |
|-------|-------|-----------------|------|
| 1 | Architecting Security | `Skill({ skill: "security-skills:architecting-security" })` | Zero trust, defense-in-depth, security principles |
| 2 | Implementing Compliance | `Skill({ skill: "security-skills:implementing-compliance" })` | SOC 2, HIPAA, GDPR, PCI-DSS requirements |
| 3 | Managing Vulnerabilities | `Skill({ skill: "security-skills:managing-vulnerabilities" })` | Scanning, patching, disclosure processes |
| 4 | Implementing TLS | `Skill({ skill: "security-skills:implementing-tls" })` | Certificate management, SSL/TLS configuration |
| 5 | Configuring Firewalls | `Skill({ skill: "security-skills:configuring-firewalls" })` | Network policies, security groups, iptables |
| 6 | SIEM Logging | `Skill({ skill: "security-skills:siem-logging" })` | Log aggregation, monitoring, alerting |
| 7 | Security Hardening | `Skill({ skill: "security-skills:security-hardening" })` | CIS benchmarks, system hardening, baseline configs |

### Execution Loop for Each Skill

For each skill in confirmed_skills:

#### 3.1 ANNOUNCE - Display Current Skill

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
 STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
 Plugin: {skill.plugin_namespace}:{skill.name}
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

#### 3.2 INVOKE - Call the Skill Tool

**YOU MUST EXECUTE THIS TOOL CALL:**

```
Skill({ skill: "{skill.invocation}" })
```

Example actual invocations:
```python
# For architecting security
Skill({ skill: "security-skills:architecting-security" })

# For implementing compliance
Skill({ skill: "security-skills:implementing-compliance" })

# For managing vulnerabilities
Skill({ skill: "security-skills:managing-vulnerabilities" })

# For implementing TLS
Skill({ skill: "security-skills:implementing-tls" })

# For configuring firewalls
Skill({ skill: "security-skills:configuring-firewalls" })

# For SIEM logging
Skill({ skill: "security-skills:siem-logging" })

# For security hardening
Skill({ skill: "security-skills:security-hardening" })
```

**This is not documentation - you must actually invoke the Skill tool using the exact format above.**

#### 3.3 FOLLOW - Process Skill Instructions

After invoking the skill:
1. Read the skill's expanded instructions
2. Follow the skill's workflow (usually asking configuration questions)
3. Collect answers and generate outputs as directed by the skill

#### 3.4 TRACK - Store Configuration

After skill completes:
```
skill_configs[skill.name] = {
  answers: user_answers,
  invocation: skill.invocation,
  priority: skill.priority,
  plugin: skill.plugin_namespace,
  dependencies: skill.dependencies,
  outputs: generated_files
}

current_skill_index += 1
```

#### 3.5 PROCEED - Continue to Next Skill

Move to next skill in confirmed_skills list and repeat: ANNOUNCE → INVOKE → FOLLOW → TRACK → PROCEED

---

**Note:** The skill invocation process above (ANNOUNCE → INVOKE → FOLLOW → TRACK → PROCEED) must be executed for EVERY skill in the confirmed chain. Do not skip skill invocations.

---

## Step 4: Generate Security Output

**IMPORTANT:** Security workflows generate security implementation plans, configurations, and hardening scripts.

### 4.1 Analyze Collected Configurations

Review all `skill_configs` to identify:
- Security architecture patterns (zero trust, defense-in-depth)
- Compliance requirements (SOC 2, HIPAA, GDPR, PCI-DSS)
- Vulnerability management processes
- TLS/SSL certificate strategies
- Firewall and network security rules
- SIEM logging and monitoring setup
- System hardening requirements

### 4.2 Identify Integration Points

Detect where security skills need to interact:
- Architecture principles informing compliance controls
- Compliance requirements driving hardening configurations
- Vulnerability scanning integrated with SIEM alerts
- TLS certificates managed by security architecture
- Firewall rules supporting defense-in-depth strategy
- SIEM logging capturing security events across all systems

### 4.3 Generate Production-Ready Security Implementation

Create complete security configuration:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  GENERATING SECURITY IMPLEMENTATION FOR: "{original_goal}" Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Based on configurations:                                Q
{for each skill in skill_configs:}
Q     {skill.name}: {summary of choices}                  Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]

Generating:
  1. Security architecture documentation
  2. Compliance control matrices
  3. Vulnerability management procedures
  4. TLS/SSL certificate configurations
  5. Firewall rules and network policies
  6. SIEM logging configurations
  7. System hardening scripts
  8. Security playbooks and runbooks
```

### 4.4 Output Organization

Organize by security domain:

```
security/
   architecture/
      threat-model.md
      security-principles.md
      zero-trust-design.md
   compliance/
      controls/
         soc2-controls.yaml
         gdpr-controls.yaml
      audit/
         evidence-collection.md
         audit-procedures.md
   vulnerability/
      scanning/
         trivy-config.yaml
         snyk-config.yaml
      remediation/
         patching-policy.md
         disclosure-process.md
   tls/
      cert-manager/
         cluster-issuer.yaml
         certificates.yaml
      nginx/
         tls-config.conf
   firewall/
      iptables/
         rules.sh
      kubernetes/
         network-policies.yaml
      cloud/
         security-groups.tf
   siem/
      elk-stack/
         logstash-pipelines.conf
         elasticsearch-config.yaml
      splunk/
         inputs.conf
         alerts.yaml
   hardening/
      scripts/
         linux-hardening.sh
         kubernetes-hardening.sh
      benchmarks/
         cis-compliance-check.sh
   runbooks/
      incident-response.md
      security-playbooks.md
   README.md
```

### 4.5 Validation Checklist

Verify generated security implementation includes:
- [ ] Security architecture aligned with best practices
- [ ] Compliance controls mapped to requirements
- [ ] Vulnerability scanning automated and scheduled
- [ ] TLS certificates properly configured and rotated
- [ ] Firewall rules follow least privilege principle
- [ ] SIEM logging captures critical security events
- [ ] System hardening scripts tested and documented
- [ ] Incident response procedures defined
- [ ] Security documentation complete and actionable
- [ ] Configuration files validated (YAML, JSON, scripts)

### 4.6 Present Output

Display generated security configuration with explanations:

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
  SECURITY IMPLEMENTATION COMPLETE
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

Generated {file_count} files across {skill_count} security domains:

KEY FILES:
  =� {architecture_doc}          - Security architecture design
  =� {compliance_matrix}         - Compliance control mappings
  =� {vulnerability_config}      - Vulnerability scanning setup
  =� {tls_config}                - TLS/SSL certificate config
  =� {firewall_rules}            - Firewall and network policies
  =� {siem_config}               - SIEM logging configuration
  =� {hardening_script}          - System hardening automation

NEXT STEPS:
  1. Review security architecture documentation
  2. Implement compliance controls: {compliance_command}
  3. Deploy vulnerability scanning: {scanning_command}
  4. Configure TLS certificates: {tls_command}
  5. Apply firewall rules: {firewall_command}
  6. Set up SIEM logging: {siem_command}
  7. Run hardening scripts: {hardening_command}

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

---

## Step 5.5: Validate Chain Outputs

After all skills have executed, validate the combined security implementation:

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
│ SECURITY SKILLCHAIN VALIDATION         │
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
  "⚠️ Some security components weren't fully generated:

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

Plugin: {skill.invocation}
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

### Configuration Conflicts

Detect incompatible security choices:

```
�  CONFIGURATION CONFLICT DETECTED

architecting-security specified: Zero Trust architecture
configuring-firewalls specified: Traditional perimeter firewall

Zero Trust minimizes perimeter reliance. Recommendation:
1. Use micro-segmentation with network policies (aligns with Zero Trust)
2. Keep traditional firewall (add network policies later)
3. Go back and reconfigure

Your choice (1/2/3):
```

### Missing Critical Security Controls

If critical security configuration is missing:

```
�  WARNING: No compliance framework selected

For production systems, compliance is recommended.

Options:
1. Add implementing-compliance skill (SOC 2 recommended)
2. Continue anyway (no compliance framework)
3. Restart workflow

Your choice (1/2/3):
```

---

**Orchestrator Complete**
