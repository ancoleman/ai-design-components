# Skillchain Resume Test Scenarios

**Purpose:** Test the `/skillchain resume` command's ability to recover and continue interrupted skillchain sessions.

**Version:** 1.0
**Created:** 2025-12-10
**Related Files:**
- `.claude-commands/skillchain/resume.md` - Resume command implementation
- `.claude-commands/skillchain-data/shared/progress-schema.yaml` - Progress file schema
- `evaluation/subagent-tests/resume/test-progress.json` - Sample progress file

---

## Test Environment Setup

**Prerequisites:**
- Feature branch: `feature/subagent-architecture`
- Test project directory: Create temporary directory for each test
- Sample progress file: `test-progress.json` in this directory

**Setup Steps:**
1. Create test project directory: `mkdir -p /tmp/skillchain-resume-test`
2. Copy appropriate progress file to project: `cp test-progress.json /tmp/skillchain-resume-test/.skillchain-progress.json`
3. Run resume command: `/skillchain resume /tmp/skillchain-resume-test`

---

## Scenario 1: Basic Resume Test

**Goal:** Verify resume continues from in_progress skill.

### Setup
Create `.skillchain-progress.json` with:
- **2 complete skills**: theming-components, building-forms
- **1 in_progress skill**: building-tables (interrupted)
- **2 pending skills**: creating-dashboards, implementing-observability

### Expected Behavior

1. **File Detection**
   ```
   Searching for skillchain progress file...
   ✓ Found: /tmp/skillchain-resume-test/.skillchain-progress.json
   ```

2. **Session Summary**
   ```
   ┌────────────────────────────────────────────────────────────┐
   │           RESUMABLE SKILLCHAIN FOUND                        │
   ├────────────────────────────────────────────────────────────┤
   │ Session ID: 550e8400-e29b-41d4-a716-446655440000           │
   │ Goal: Build a dashboard with data visualization            │
   │ Blueprint: Custom chain                                    │
   │ Maturity: intermediate                                     │
   │                                                            │
   │ PROGRESS:                                                  │
   │   Total Skills: 5                                          │
   │   Completed:    2                                          │
   │   Failed:       0                                          │
   │   Remaining:    3                                          │
   │                                                            │
   │ SKILL STATUS:                                              │
   │   ✓ theming-components - complete                          │
   │   ✓ building-forms - complete                              │
   │   ⚙ building-tables - in_progress (interrupted)            │
   │   ○ creating-dashboards - pending                          │
   │   ○ implementing-observability - pending                   │
   └────────────────────────────────────────────────────────────┘
   ```

3. **Resume Execution**
   - User selects Option 1: "Continue from building-tables"
   - System loads accumulated context (theme + forms data)
   - Spawns skill-executor subagent for building-tables
   - Displays progress: "Resuming execution... Progress: 2/5 complete"

4. **After Skill Completion**
   - Progress file updated: building-tables marked "complete"
   - Continues to creating-dashboards automatically
   - Updates accumulated_context with tables outputs

### Success Criteria
- [x] Progress file detected and parsed
- [x] Correct resume point identified (building-tables)
- [x] Accumulated context properly loaded
- [x] Skill executes with full context
- [x] Progress file updated after completion
- [x] Chain continues to next pending skill

---

## Scenario 2: Failed Skill Retry

**Goal:** Verify retry mechanism for failed skills.

### Setup
Create `.skillchain-progress.json` with:
- **1 complete skill**: theming-components
- **1 failed skill**: building-forms (error: "Missing user input for validation rules")
- **2 pending skills**: building-tables, creating-dashboards

### Expected Behavior

1. **Session Summary Shows Failure**
   ```
   │ PROGRESS:                                                  │
   │   Total Skills: 4                                          │
   │   Completed:    1                                          │
   │   Failed:       1                                          │
   │   Remaining:    2                                          │
   │                                                            │
   │ SKILL STATUS:                                              │
   │   ✓ theming-components - complete                          │
   │   ✗ building-forms - failed                                │
   │   ○ building-tables - pending                              │
   │   ○ creating-dashboards - pending                          │
   │                                                            │
   │ Resume options:                                            │
   │ 1. Continue from building-tables (skip failed)             │
   │ 2. Retry failed skill: building-forms                      │
   ```

2. **Retry Flow**
   - User selects Option 2: "Retry failed skill"
   - System displays previous error:
     ```
     Retrying failed skill: building-forms

     Previous error: Missing user input for validation rules

     Spawning fresh skill-executor subagent...
     ```
   - Skill status reset to "in_progress"
   - Fresh execution attempt with same context

3. **After Successful Retry**
   - Progress file updated: building-forms status = "complete"
   - Failed count decremented: 0
   - Completed count incremented: 2
   - Chain continues to building-tables

### Success Criteria
- [x] Failed skill identified in summary
- [x] Retry option presented
- [x] Previous error message displayed
- [x] Fresh execution with clean state
- [x] Progress file updated on success
- [x] Counters (failed/completed) updated correctly

---

## Scenario 3: Skip to Validation

**Goal:** Verify partial completion validation.

### Setup
Create `.skillchain-progress.json` with:
- **3 complete skills**: theming-components, building-forms, building-tables
- **2 pending skills**: creating-dashboards, implementing-observability

### Expected Behavior

1. **Skip Option Available**
   ```
   │ Resume options:                                            │
   │ 1. Continue from creating-dashboards                       │
   │ 2. Skip to validation (if enough skills complete)          │
   │ 3. View detailed progress                                  │
   ```

2. **Skip Confirmation**
   ```
   Skipping remaining skills and running validation...

   Warning: The following skills will be skipped:
   - creating-dashboards
   - implementing-observability

   This may result in incomplete deliverables.

   Continue? (yes/no):
   ```

3. **If User Confirms**
   - Remaining skills marked as "skipped"
   - Skipped count: 2
   - Spawn skillchain-validator subagent
   - Validator runs on partial deliverables (theme + forms + tables only)

4. **Validation Results**
   ```
   ┌────────────────────────────────────────────────────────────┐
   │           VALIDATION REPORT (Partial)                       │
   ├────────────────────────────────────────────────────────────┤
   │ Completeness: 60% (3/5 skills executed)                    │
   │ Status: PARTIAL                                            │
   │                                                            │
   │ Verified Deliverables:                                     │
   │   ✓ Theme tokens and context                              │
   │   ✓ Form components with validation                       │
   │   ✓ Table components with sorting                         │
   │                                                            │
   │ Missing (Skipped):                                         │
   │   ✗ Dashboard layouts                                      │
   │   ✗ Observability instrumentation                         │
   └────────────────────────────────────────────────────────────┘
   ```

### Success Criteria
- [x] Skip option only available when completed_count > 0
- [x] Warning displayed with skipped skill list
- [x] Confirmation required before skipping
- [x] Skipped skills marked correctly in progress file
- [x] Validator receives accumulated_context
- [x] Validation report indicates PARTIAL status

---

## Scenario 4: No Progress File

**Goal:** Verify graceful handling when progress file doesn't exist.

### Setup
- Empty test directory (no `.skillchain-progress.json`)
- Run: `/skillchain resume /tmp/empty-test-dir`

### Expected Behavior

```
Searching for skillchain progress file...

Locations checked:
1. /tmp/empty-test-dir/.skillchain-progress.json
2. {current_working_directory}/.skillchain-progress.json

┌────────────────────────────────────────────────────────────┐
│           NO SKILLCHAIN SESSION FOUND                       │
├────────────────────────────────────────────────────────────┤
│ Could not find .skillchain-progress.json                    │
│                                                            │
│ This file is created when you start a skillchain in        │
│ delegated execution mode.                                  │
│                                                            │
│ To start a new skillchain:                                 │
│   /skillchain {your goal}                                  │
│                                                            │
│ Then choose "delegated" execution mode when prompted.      │
└────────────────────────────────────────────────────────────┘
```

### Success Criteria
- [x] No crash or error thrown
- [x] Helpful error message displayed
- [x] Multiple search locations checked and listed
- [x] Clear instructions for creating new skillchain
- [x] Execution stops gracefully

---

## Scenario 5: Corrupted Progress File

**Goal:** Verify graceful error handling for malformed JSON.

### Setup
Create `.skillchain-progress.json` with invalid JSON:
```json
{
  "version": "1.0",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "goal": "Build dashboard"
  "skills": [  // <-- Missing comma (syntax error)
    {"name": "theming-components"}
  ]
}
```

### Expected Behavior

1. **Parse Error Detected**
   ```
   Searching for skillchain progress file...
   ✓ Found: /tmp/skillchain-resume-test/.skillchain-progress.json

   Parsing progress file...
   ```

2. **Error Message**
   ```
   ┌────────────────────────────────────────────────────────────┐
   │           INVALID PROGRESS FILE                            │
   ├────────────────────────────────────────────────────────────┤
   │ The progress file could not be parsed.                     │
   │                                                            │
   │ Error: Expecting ',' delimiter: line 4 column 3 (char 123) │
   │                                                            │
   │ Options:                                                   │
   │ 1. Delete file and start fresh: /skillchain {goal}        │
   │ 2. Try to repair (if minor issue)                         │
   └────────────────────────────────────────────────────────────┘
   ```

3. **Repair Option (Advanced)**
   - If user selects "Try to repair"
   - System attempts basic fixes:
     - Add missing commas
     - Fix unescaped strings
     - Balance brackets
   - If successful, show diff and ask for confirmation
   - If unsuccessful, suggest manual editing or deletion

### Success Criteria
- [x] JSON parse error caught
- [x] Specific error message displayed (line/column)
- [x] File not corrupted further by failed read
- [x] Clear options presented (delete or repair)
- [x] No execution attempted with invalid data

---

## Scenario 6: Version Mismatch

**Goal:** Verify version compatibility checking.

### Setup
Create `.skillchain-progress.json` with future schema version:
```json
{
  "version": "2.0",
  "session_id": "...",
  ...
}
```

### Expected Behavior

1. **Version Check**
   ```
   Searching for skillchain progress file...
   ✓ Found: /tmp/skillchain-resume-test/.skillchain-progress.json

   Validating schema version...
   ```

2. **Version Warning**
   ```
   ┌────────────────────────────────────────────────────────────┐
   │           VERSION MISMATCH WARNING                          │
   ├────────────────────────────────────────────────────────────┤
   │ Progress file version: 2.0                                 │
   │ Current schema version: 1.0                                │
   │                                                            │
   │ This progress file was created with a newer version.       │
   │ Some fields may not be recognized or may behave            │
   │ differently.                                               │
   │                                                            │
   │ Options:                                                   │
   │ 1. Continue anyway (may lose data)                         │
   │ 2. Cancel and update your Claude Code installation        │
   │ 3. Export data and start fresh session                     │
   └────────────────────────────────────────────────────────────┘
   ```

3. **If User Continues**
   - Parse what's compatible
   - Log warnings for unknown fields
   - Proceed with caution

4. **Version Too Old (Reverse)**
   If progress file is version "0.9" and current is "1.0":
   ```
   │ Progress file version: 0.9                                 │
   │ Current schema version: 1.0                                │
   │                                                            │
   │ This is an older format. Attempting automatic migration... │
   │                                                            │
   │ Migration steps:                                           │
   │ - Add execution.activation_rate field (default: 100.0)     │
   │ - Add executor field to skills (default: skill-executor)   │
   │ - Update timestamps to ISO8601 format                      │
   │                                                            │
   │ Backup created: .skillchain-progress.json.backup           │
   ```

### Success Criteria
- [x] Version field validated
- [x] Mismatch detected and displayed
- [x] Forward compatibility warning (newer version)
- [x] Backward compatibility migration (older version)
- [x] User choice required before proceeding
- [x] Backup created before migration

---

## Additional Test Cases

### Edge Cases to Consider

**7. Multiple Skills In Progress**
- Progress file has 2 skills with status "in_progress"
- System should warn about inconsistent state
- Offer to reset both to pending or pick one

**8. All Skills Complete**
- All skills have status "complete"
- Validation already run
- Offer to:
  - View final report
  - Re-run validation
  - Delete progress file

**9. Large Accumulated Context (>50KB)**
- Progress file with extensive accumulated_context
- System warns about large context size
- Offers summarization before resume

**10. Resume After User Interrupt**
- User cancels during skill execution (Ctrl+C)
- Progress file shows in_progress but no agent_id
- Resume should restart that skill from beginning

---

## Testing Checklist

Before considering resume functionality complete:

**Core Functionality:**
- [ ] Basic resume from in_progress skill
- [ ] Resume from first pending skill
- [ ] Retry failed skill
- [ ] Skip to validation with partial results
- [ ] View detailed progress report
- [ ] Cancel and keep progress
- [ ] Delete progress and start fresh

**Error Handling:**
- [ ] No progress file found
- [ ] Corrupted/invalid JSON
- [ ] Missing required fields
- [ ] Version mismatch (newer)
- [ ] Version mismatch (older with migration)

**Context Management:**
- [ ] Accumulated context properly loaded
- [ ] Context passed to skill-executor
- [ ] Context updated after skill completion
- [ ] Large context handled gracefully

**Progress File Operations:**
- [ ] Read without corruption
- [ ] Update incrementally
- [ ] Atomic writes (no partial saves)
- [ ] Timestamps updated correctly
- [ ] Counters (completed/failed/skipped) accurate

**User Experience:**
- [ ] Clear status summaries
- [ ] Helpful error messages
- [ ] Confirmation for destructive actions
- [ ] Progress indicators during execution
- [ ] Final report matches validation results

---

## Manual Testing Procedure

### Quick Test (5 minutes)
1. Use `test-progress.json` from this directory
2. Copy to test project: `cp test-progress.json /tmp/test/.skillchain-progress.json`
3. Run: `/skillchain resume /tmp/test`
4. Select Option 1 (continue)
5. Verify skill-executor spawns with context

### Full Test Suite (30 minutes)
1. Run all 6 scenarios above
2. Document any deviations from expected behavior
3. Check progress file after each operation
4. Verify no data loss on errors

### Stress Test (15 minutes)
1. Create progress file with 20+ skills
2. Test with large accumulated_context (add verbose outputs)
3. Interrupt and resume multiple times
4. Verify performance remains acceptable

---

## Validation Criteria

Resume functionality is considered working when:

1. **Reliability**: Can resume any valid session without data loss
2. **Clarity**: Users understand current state and available options
3. **Safety**: No accidental data deletion; confirmations for destructive actions
4. **Compatibility**: Handles version mismatches gracefully
5. **Performance**: Loads and parses progress files quickly (<1 second)
6. **Robustness**: Handles corrupted files without crashing

---

## Related Documentation

- **Resume Command**: `.claude-commands/skillchain/resume.md`
- **Delegated Execution**: `.claude-commands/skillchain/delegated.md`
- **Progress Schema**: `.claude-commands/skillchain-data/shared/progress-schema.yaml`
- **Skill Executor**: `.claude-commands/skillchain-data/subagents/skill-executor.md`
- **Validator**: `.claude-commands/skillchain-data/subagents/skillchain-validator.md`

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-10 | Initial test scenarios for Task 3.4 |
