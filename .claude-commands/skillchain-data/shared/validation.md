# Skillchain Validation Logic

**Purpose:** Post-generation validation to verify that skillchains deliver on blueprint promises and produce complete, functional outputs.

**Version:** 1.0.0
**Last Updated:** 2024-12-08

---

## Overview

This document provides shared validation logic that orchestrators (categories/*.md) use to validate skillchain outputs. Validation occurs in two phases:

1. **During execution** - Track what each skill creates
2. **Post-generation** - Validate deliverables against blueprint promises

### Validation Goals

- **Verify completeness:** All required files exist and have content
- **Check functionality:** Required patterns/imports are present
- **Report gaps:** Identify missing deliverables before declaring success
- **Enable remediation:** Offer to generate missing components

---

## Skill Output Declarations (outputs.yaml)

Each skill declares its expected outputs in an `outputs.yaml` file. This enables:
1. **Per-skill validation** - Verify each skill produced what it promised
2. **Blueprint mapping** - Connect skill outputs to blueprint deliverables
3. **Completeness tracking** - Track which skills contributed which files

### outputs.yaml Structure

```yaml
skill: skill-name
version: "1.0"
domain: "category"  # e.g., devops, security, data

base_outputs:
  - path: "path/to/file.py"
    reason: "Why this file is generated"
    must_contain:
      - "expected_import"
      - "expected_function"

  - path: "config/settings.yaml"
    reason: "Configuration for the feature"

conditional_outputs:
  - condition: "if user selected streaming"
    outputs:
      - path: "streaming/consumer.py"
        reason: "Kafka consumer implementation"
```

### Per-Skill Validation

After each skill executes, validate its declared outputs:

```markdown
## validate_skill_outputs(skill_name, project_path)

1. **Load skill outputs declaration:**
   ```
   outputs_path = "{SKILLS_DIR}/{skill_name}/outputs.yaml"
   Use Read tool to load outputs_path
   Parse YAML content
   ```

2. **Validate base outputs:**
   ```
   skill_results = {
     skill: skill_name,
     expected: [],
     found: [],
     missing: []
   }

   For each output in base_outputs:
     skill_results.expected.append(output.path)
     full_path = join(project_path, output.path)

     If exists(full_path):
       skill_results.found.append(output.path)

       # Optionally check must_contain patterns
       If output.must_contain exists:
         content = Read(full_path)
         For each pattern in output.must_contain:
           If pattern NOT in content:
             Log warning: "File {output.path} missing expected content: {pattern}"
     Else:
       skill_results.missing.append(output.path)
   ```

3. **Track conditional outputs:**
   ```
   For each conditional in conditional_outputs:
     If user_context matches conditional.condition:
       For each output in conditional.outputs:
         # Same validation as base_outputs
   ```

4. **Return skill validation result:**
   ```
   Return {
     skill: skill_name,
     completeness: length(found) / length(expected) * 100,
     found: skill_results.found,
     missing: skill_results.missing
   }
   ```
```

### Runtime Validation Script

For programmatic validation, use the completeness checker script:

```bash
# Validate entire generated project against blueprint
python scripts/runtime/completeness_checker.py \
  {project_path} \
  --blueprint {blueprint_name} \
  --maturity {maturity_level}

# Example:
python scripts/runtime/completeness_checker.py \
  ./my-data-pipeline \
  --blueprint data-pipeline \
  --maturity intermediate
```

The script reads blueprint deliverables and validates all required files exist with expected content patterns.

---

## Validation Functions

Orchestrators should follow these validation procedures. Each function is described in markdown pseudo-code that Claude can execute.

### Function 1: `validate_deliverable`

Validates a single deliverable from a blueprint specification.

**Parameters:**
- `deliverable_spec` - The deliverable definition from blueprint
- `project_path` - Absolute path to the generated project
- `maturity` - Current maturity level (starter/intermediate/advanced)

**Returns:**
- `validation_result` - Object with status, errors, warnings

**Pseudo-code:**

```markdown
## validate_deliverable(deliverable_spec, project_path, maturity)

1. **Check maturity requirements:**
   ```
   If deliverable_spec.maturity_required exists:
     If maturity NOT in deliverable_spec.maturity_required:
       Return {
         status: "skipped",
         reason: "Not required for {maturity} maturity",
         alternative: deliverable_spec.starter_alternative (if exists)
       }
   ```

2. **Check required files exist:**
   ```
   missing_files = []
   For each file_path in deliverable_spec.required_files:
     full_path = join(project_path, file_path)

     If file_path contains glob pattern (* or **):
       matched_files = glob(full_path)
       If matched_files is empty:
         missing_files.append(file_path)
     Else:
       If NOT exists(full_path):
         missing_files.append(file_path)
       Else if file_size(full_path) == 0:
         missing_files.append(file_path + " (empty)")
   ```

3. **Run content checks:**
   ```
   failed_checks = []
   For each check in deliverable_spec.content_checks:
     pattern = check.pattern
     search_in = check.in
     full_path = join(project_path, search_in)

     If search_in ends with "/" (directory):
       # Search all files in directory
       Use Grep tool with:
         pattern: pattern
         path: full_path
         output_mode: "files_with_matches"

       If no matches found:
         failed_checks.append({
           pattern: pattern,
           location: search_in,
           reason: "Pattern not found in any file"
         })

     Else (specific file):
       Use Read tool to read file at full_path
       Search file content for pattern (regex match)

       If pattern not found:
         failed_checks.append({
           pattern: pattern,
           location: search_in,
           reason: "Pattern not found in file"
         })
   ```

4. **Determine status:**
   ```
   If missing_files is empty AND failed_checks is empty:
     status = "fulfilled"
   Else if missing_files is NOT empty:
     status = "missing"
   Else if failed_checks is NOT empty:
     status = "incomplete"

   Return {
     status: status,
     missing_files: missing_files,
     failed_checks: failed_checks,
     primary_skill: deliverable_spec.primary_skill
   }
   ```
```

---

### Function 2: `check_files_exist`

Checks if a list of files/directories exist in the project.

**Parameters:**
- `file_list` - Array of file paths (can include glob patterns)
- `project_path` - Absolute path to project root

**Returns:**
- `check_result` - Object with existing/missing files

**Pseudo-code:**

```markdown
## check_files_exist(file_list, project_path)

1. **Initialize results:**
   ```
   existing = []
   missing = []
   empty = []
   ```

2. **Check each file:**
   ```
   For each file_path in file_list:
     full_path = join(project_path, file_path)

     If file_path contains glob pattern (* or **):
       Use Glob tool with pattern: file_path in path: project_path
       matched = glob results

       If matched is empty:
         missing.append(file_path)
       Else:
         For each match in matched:
           If is_directory(match):
             contents = list_directory_contents(match)
             If contents is empty OR only contains __init__.py:
               empty.append(match)
             Else:
               existing.append(match)
           Else if file_size(match) == 0:
             empty.append(match)
           Else:
             existing.append(match)

     Else (specific path):
       If NOT exists(full_path):
         missing.append(file_path)
       Else if is_directory(full_path):
         contents = list_directory_contents(full_path)
         If contents is empty OR only contains __init__.py:
           empty.append(file_path)
         Else:
           existing.append(file_path)
       Else if file_size(full_path) == 0:
         empty.append(file_path)
       Else:
         existing.append(file_path)
   ```

3. **Return results:**
   ```
   Return {
     existing: existing,
     missing: missing,
     empty: empty,
     total: length(file_list),
     found: length(existing),
     completeness: length(existing) / length(file_list) * 100
   }
   ```
```

---

### Function 3: `run_content_checks`

Runs pattern matching checks against files to verify functionality.

**Parameters:**
- `checks` - Array of check specifications with pattern and location
- `project_path` - Absolute path to project root

**Returns:**
- `check_results` - Array of results for each check

**Pseudo-code:**

```markdown
## run_content_checks(checks, project_path)

1. **Initialize results:**
   ```
   results = []
   ```

2. **Execute each check:**
   ```
   For each check in checks:
     pattern = check.pattern
     location = check.in  # File or directory path
     full_path = join(project_path, location)

     check_result = {
       pattern: pattern,
       location: location,
       passed: false,
       matches: []
     }

     If location ends with "/" (directory search):
       # Use Grep to search all files in directory
       Use Grep tool with:
         pattern: pattern
         path: full_path
         output_mode: "files_with_matches"

       matches = grep results
       If matches is NOT empty:
         check_result.passed = true
         check_result.matches = matches

     Else (specific file):
       If NOT exists(full_path):
         check_result.error = "File does not exist"
       Else:
         Use Read tool to read file at full_path
         content = file contents

         Use regex to search for pattern in content
         If pattern found:
           check_result.passed = true
           check_result.matches = [location]

     results.append(check_result)
   ```

3. **Return results:**
   ```
   Return {
     total: length(checks),
     passed: count(r for r in results if r.passed),
     failed: count(r for r in results if NOT r.passed),
     details: results
   }
   ```
```

---

### Function 4: `validate_chain`

Validates all deliverables for a complete skillchain execution.

**Parameters:**
- `chain_context` - The chain context object from orchestrator
- `project_path` - Absolute path to generated project

**Returns:**
- `validation_report` - Complete validation report

**Pseudo-code:**

```markdown
## validate_chain(chain_context, project_path)

1. **Load blueprint deliverables:**
   ```
   If chain_context.blueprint is null:
     Return run_basic_completeness_check(project_path)

   blueprint_name = chain_context.blueprint
   blueprint_path = "{SKILLCHAIN_CMD}/blueprints/{blueprint_name}.md"

   Use Read tool to read blueprint_path
   Parse deliverables section from blueprint

   If no deliverables section found:
     Return run_basic_completeness_check(project_path)
   ```

2. **Get maturity level:**
   ```
   maturity = chain_context.maturity OR "intermediate"

   # Load maturity profile if exists
   maturity_profile = parse maturity_profiles section from blueprint
   skip_deliverables = maturity_profile[maturity].skip_deliverables OR []
   required_additions = maturity_profile[maturity].required_additions OR []
   empty_dirs_allowed = maturity_profile[maturity].empty_dirs_allowed OR []
   ```

3. **Validate each deliverable:**
   ```
   deliverable_results = {}

   For each (deliverable_name, spec) in blueprint.deliverables:
     If deliverable_name in skip_deliverables:
       deliverable_results[deliverable_name] = {
         status: "skipped",
         reason: "Not required for {maturity} maturity"
       }
       Continue to next deliverable

     # Validate this deliverable
     result = validate_deliverable(spec, project_path, maturity)
     deliverable_results[deliverable_name] = result
   ```

4. **Check required additions:**
   ```
   For each file_path in required_additions:
     If file_path NOT in any deliverable.required_files:
       # This is an additional requirement
       deliverable_results["Additional: {file_path}"] = {
         status: "fulfilled" if exists(join(project_path, file_path)) else "missing",
         primary_skill: "unknown",
         file_path: file_path
       }
   ```

5. **Calculate metrics:**
   ```
   total_required = count(d for d in deliverable_results if d.status != "skipped")
   fulfilled = count(d for d in deliverable_results if d.status == "fulfilled")
   missing = count(d for d in deliverable_results if d.status == "missing")
   incomplete = count(d for d in deliverable_results if d.status == "incomplete")

   completeness_score = (fulfilled / total_required) * 100 if total_required > 0 else 0
   ```

6. **Return validation report:**
   ```
   Return {
     blueprint: blueprint_name,
     maturity: maturity,
     project_path: project_path,
     deliverables: deliverable_results,
     metrics: {
       total_required: total_required,
       fulfilled: fulfilled,
       missing: missing,
       incomplete: incomplete,
       skipped: count(d for d in deliverable_results if d.status == "skipped"),
       completeness: completeness_score
     },
     passed: completeness_score >= 80
   }
   ```
```

---

### Function 5: `run_basic_completeness_check`

Runs basic checks when no blueprint is used (fallback validation).

**Parameters:**
- `project_path` - Absolute path to generated project

**Returns:**
- `basic_report` - Simple completeness report

**Pseudo-code:**

```markdown
## run_basic_completeness_check(project_path)

1. **Check directory structure:**
   ```
   Use Bash to run: find {project_path} -type d | wc -l
   total_dirs = result

   Use Bash to run: find {project_path} -type f | wc -l
   total_files = result
   ```

2. **Identify empty directories:**
   ```
   empty_dirs = []
   Use Bash to run: find {project_path} -type d -empty
   For each dir in results:
     empty_dirs.append(dir)

   # Also check directories with only __init__.py
   Use Bash to run:
     find {project_path} -type d -exec sh -c
       'ls -A {} | grep -v __init__.py | wc -l' \;

   For directories with count == 0:
     If NOT already in empty_dirs:
       empty_dirs.append(dir + " (only __init__.py)")
   ```

3. **Check for README:**
   ```
   readme_exists = exists(join(project_path, "README.md"))
   If readme_exists:
     Use Read tool to check if README has content
     readme_has_content = file_size > 100 bytes
   ```

4. **Calculate completeness:**
   ```
   dirs_with_content = total_dirs - length(empty_dirs)
   directory_completeness = (dirs_with_content / total_dirs) * 100

   completeness_score = directory_completeness
   ```

5. **Return report:**
   ```
   Return {
     project_path: project_path,
     metrics: {
       total_directories: total_dirs,
       total_files: total_files,
       empty_directories: length(empty_dirs),
       readme_exists: readme_exists,
       directory_completeness: directory_completeness,
       completeness: completeness_score
     },
     empty_dirs: empty_dirs,
     passed: completeness_score >= 60
   }
   ```
```

---

## Report Generation

### Function: `generate_validation_report`

Formats validation results for user presentation.

**Parameters:**
- `validation_result` - Result from validate_chain or run_basic_completeness_check

**Output Format:**

```markdown
## generate_validation_report(validation_result)

**For blueprint-based validation:**

```
┌────────────────────────────────────────────────────┐
│ SKILLCHAIN COMPLETION REPORT                        │
│                                                     │
│ Blueprint: {blueprint}                              │
│ Maturity: {maturity}                                │
│ Project: {project_path}                             │
├────────────────────────────────────────────────────┤
│                                                     │
│ DELIVERABLES:                                       │
│                                                     │
│ ✓ MLflow experiment tracking                        │
│ ✓ Training pipeline                                 │
│ ✓ Model serving API                                 │
│ ○ Feature store (skipped - starter)                 │
│ ✗ Grafana dashboards - MISSING                      │
│   └─ Expected files:                                │
│      • monitoring/grafana/dashboards/*.json         │
│   └─ Primary skill: implementing-observability      │
│ ⚠ Sample data script - INCOMPLETE                   │
│   └─ File exists but missing pattern: "def generate"│
│ ○ Kubernetes (skipped - starter)                    │
│                                                     │
├────────────────────────────────────────────────────┤
│ SUMMARY:                                            │
│                                                     │
│ Required: {total_required}                          │
│ Fulfilled: {fulfilled}                              │
│ Missing: {missing}                                  │
│ Incomplete: {incomplete}                            │
│ Skipped: {skipped}                                  │
│                                                     │
│ Completeness: {completeness}%                       │
│ Status: {PASSED / NEEDS ATTENTION}                  │
└────────────────────────────────────────────────────┘
```

**For basic completeness check:**

```
┌────────────────────────────────────────────────────┐
│ SKILLCHAIN COMPLETENESS REPORT                      │
│                                                     │
│ Project: {project_path}                             │
├────────────────────────────────────────────────────┤
│                                                     │
│ METRICS:                                            │
│                                                     │
│ Total directories: {total_directories}              │
│ Total files: {total_files}                          │
│ Empty directories: {empty_directories}              │
│ README exists: {yes/no}                             │
│                                                     │
│ Directory completeness: {directory_completeness}%   │
│                                                     │
├────────────────────────────────────────────────────┤
│ EMPTY DIRECTORIES:                                  │
│                                                     │
│ • src/features/ (only __init__.py)                  │
│ • monitoring/grafana/dashboards/                    │
│ • data/raw/                                         │
│                                                     │
├────────────────────────────────────────────────────┤
│ Overall completeness: {completeness}%               │
│ Status: {PASSED / NEEDS ATTENTION}                  │
└────────────────────────────────────────────────────┘
```
```

---

## Remediation Flow

### Function: `handle_missing_deliverables`

Offers to generate missing components when validation fails.

**Parameters:**
- `validation_result` - Result from validate_chain

**Pseudo-code:**

```markdown
## handle_missing_deliverables(validation_result)

1. **Check if remediation needed:**
   ```
   If validation_result.passed is true:
     Output: "✓ All required components generated successfully!"
     Return
   ```

2. **Identify missing items:**
   ```
   missing_deliverables = []
   incomplete_deliverables = []

   For each (name, result) in validation_result.deliverables:
     If result.status == "missing":
       missing_deliverables.append({
         name: name,
         skill: result.primary_skill,
         files: result.missing_files
       })
     Else if result.status == "incomplete":
       incomplete_deliverables.append({
         name: name,
         skill: result.primary_skill,
         checks: result.failed_checks
       })
   ```

3. **Present to user:**
   ```
   Output:
   "⚠️ Some features weren't fully generated:

   MISSING COMPONENTS:
   {For each item in missing_deliverables}
   • {item.name}
     Expected files: {item.files}
     Primary skill: {item.skill}

   INCOMPLETE COMPONENTS:
   {For each item in incomplete_deliverables}
   • {item.name}
     Missing patterns: {item.checks}
     Primary skill: {item.skill}

   Completeness: {validation_result.metrics.completeness}%

   Would you like me to:
   A) Generate the missing components
   B) Generate specific components (tell me which)
   C) Continue without them
   D) See detailed validation report"
   ```

4. **Handle user response:**
   ```
   If user chooses A (generate all):
     For each missing_deliverable:
       Re-invoke skill: {missing_deliverable.skill}
       Pass context about what's missing
       Validate again after generation

   If user chooses B (specific):
     Ask: "Which components would you like me to generate?"
     For each selected component:
       Re-invoke appropriate skill
       Validate after generation

   If user chooses C (skip):
     Output: "Proceeding with partial implementation. You can generate missing components later by running individual skills."

   If user chooses D (detailed report):
     Call generate_validation_report(validation_result)
     Then re-present options A-C
   ```

5. **Re-validate after remediation:**
   ```
   If any skills were re-invoked:
     new_validation = validate_chain(chain_context, project_path)

     If new_validation.passed:
       Output: "✓ All components generated successfully!"
       Output: generate_validation_report(new_validation)
     Else:
       Output: "Some components still incomplete:"
       Output: generate_validation_report(new_validation)
       Ask if user wants to try again
   ```
```

---

## Integration with Orchestrators

Orchestrators (categories/*.md) should call validation in Step 5.5:

```markdown
## Step 5.5: Validate Chain Outputs (in categories/*.md)

After all skills complete:

1. **Import validation logic:**
   ```
   Reference: {SKILLCHAIN_DATA}/shared/validation.md
   ```

2. **Run validation:**
   ```
   validation_result = validate_chain(chain_context, project_path)
   ```

3. **Handle results:**
   ```
   If validation_result.passed:
     Output: generate_validation_report(validation_result)
   Else:
     handle_missing_deliverables(validation_result)
   ```
```

---

## Example Validation Scenario

### Scenario: ML Pipeline (Starter Maturity)

**Input:**
- Blueprint: ml-pipeline
- Maturity: starter
- Project: ~/Documents/repos/ml-pipeline-project

**Validation Process:**

1. Load ml-pipeline.md deliverables
2. Apply starter maturity adjustments (skip Feature store, K8s)
3. Required deliverables:
   - MLflow experiment tracking
   - Training pipeline
   - Model serving API
   - Sample data script (starter addition)
   - Starter notebook (starter addition)

4. Validate each:
   ```
   MLflow: ✓ (src/models/train.py exists, has "import mlflow")
   Training: ✓ (pipelines/training_pipeline.py exists)
   Serving: ✓ (src/serving/api.py exists, has "FastAPI")
   Sample data: ✗ (scripts/generate_sample_data.py missing)
   Notebook: ✗ (notebooks/01_quickstart.ipynb missing)
   ```

5. Calculate: 3/5 = 60% completeness

6. Report to user with remediation options

7. If user accepts, generate missing files

8. Re-validate: 5/5 = 100% completeness

---

## Notes for Orchestrators

### When to Run Validation

**Always run validation:**
- After all skills in chain complete
- Before declaring skillchain success
- Before saving preferences

**Never skip validation:**
- Even if all skills reported success
- Even if no errors occurred during generation

### Error Handling

If validation throws errors:
1. Catch and log the error
2. Fall back to basic completeness check
3. Report validation failure to user
4. Offer to proceed without validation

### Performance Considerations

- Use Glob instead of Bash find for file searches
- Use Grep for pattern matching (faster than reading all files)
- Cache blueprint deliverables (don't re-read blueprint)
- Batch file existence checks when possible

---

## Changelog

**1.0.0 (2024-12-08):**
- Initial validation logic implementation
- Five core validation functions
- Report generation format
- Remediation flow
- Integration guide for orchestrators
