# Skillchain Resume Command

**Purpose:** Resume an interrupted or incomplete skillchain session.

This command reads the `.skillchain-progress.json` file from the project root and continues execution from where it left off.

---

## Usage

```bash
/skillchain resume [project_path]
```

**Arguments:**
- `project_path` (optional): Path to project with progress file. Defaults to current directory.

---

## Step 1: Locate Progress File

Search for `.skillchain-progress.json`:

```
Searching for skillchain progress file...

Locations checked:
1. {project_path}/.skillchain-progress.json
2. {cwd}/.skillchain-progress.json
```

### If Not Found

```
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

Stop execution.

---

## Step 2: Load and Validate Progress File

Read and parse `.skillchain-progress.json`:

```python
# Validation checklist
- [ ] File is valid JSON
- [ ] version field exists and is "1.0"
- [ ] session_id is valid UUID
- [ ] skills array is present
- [ ] execution object is present
```

### If Invalid

```
┌────────────────────────────────────────────────────────────┐
│           INVALID PROGRESS FILE                            │
├────────────────────────────────────────────────────────────┤
│ The progress file could not be parsed.                     │
│                                                            │
│ Error: {parse_error}                                       │
│                                                            │
│ Options:                                                   │
│ 1. Delete file and start fresh: /skillchain {goal}        │
│ 2. Try to repair (if minor issue)                         │
└────────────────────────────────────────────────────────────┘
```

Stop execution.

---

## Step 3: Analyze Session State

Display session summary:

```
┌────────────────────────────────────────────────────────────┐
│           RESUMABLE SKILLCHAIN FOUND                        │
├────────────────────────────────────────────────────────────┤
│ Session ID: {session_id}                                   │
│ Goal: {goal}                                               │
│ Blueprint: {blueprint or "Custom chain"}                   │
│ Maturity: {maturity}                                       │
│                                                            │
│ Started: {started_at}                                      │
│ Last Update: {updated_at}                                  │
│                                                            │
│ PROGRESS:                                                  │
│   Total Skills: {total_skills}                             │
│   Completed:    {completed_count}                          │
│   Failed:       {failed_count}                             │
│   Remaining:    {remaining_count}                          │
│                                                            │
│ SKILL STATUS:                                              │
│   ✓ {skill_1} - complete                                   │
│   ✓ {skill_2} - complete                                   │
│   ⚙ {skill_3} - in_progress (interrupted)                  │
│   ○ {skill_4} - pending                                    │
│   ○ {skill_5} - pending                                    │
│                                                            │
│ ACCUMULATED CONTEXT:                                       │
│   - Theme: {theme_summary or "Not set"}                    │
│   - API: {api_summary or "Not set"}                        │
│   - Database: {db_summary or "Not set"}                    │
│   - Frontend: {frontend_summary or "Not set"}              │
├────────────────────────────────────────────────────────────┤
│ Resume options:                                            │
│                                                            │
│ 1. Continue from {next_skill_name}                         │
│ 2. Retry failed skill: {failed_skill_name}                 │
│ 3. Skip to validation (if enough skills complete)          │
│ 4. View detailed progress                                  │
│ 5. Cancel and keep progress file                           │
│ 6. Delete progress and start fresh                         │
└────────────────────────────────────────────────────────────┘

Your choice (1-6):
```

---

## Step 4: Resume Execution

Based on user choice:

### Option 1: Continue from Next Skill

Determine the next skill to execute:

```python
# Find resume point
if any skill has status "in_progress":
    resume_from = in_progress_skill  # Retry interrupted skill
else:
    resume_from = first pending skill  # Continue sequence
```

Then proceed as delegated.md orchestrator:

1. **Reconstruct Context**
   ```
   Loading accumulated context from progress file...

   Context restored:
   - Project path: {project_path}
   - Theme tokens: {available/not available}
   - API base: {api_base or "not set"}
   - {other relevant context}
   ```

2. **Spawn skill-executor subagent**
   ```
   Resuming execution...

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     RESUMING: {skill_name}
     Progress: {completed}/{total} complete
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

3. **Use Task tool with appropriate executor**
   ```
   Task tool parameters:
     subagent: "{executor from progress file or skill-executor}"
     description: "Resume {skill_name} skill"
     prompt: |
       Resume/Execute skill: {invocation}

       ## Context (from progress file)
       - Goal: {goal}
       - Project Path: {project_path}
       - Skills Completed: {list from progress file}

       ## Previous Skill Outputs
       {accumulated_context formatted for prompt}

       ## User Preferences
       {preferences from original session or "Use skill defaults"}

       ## Resume Note
       This skill was interrupted. Complete all instructions from the beginning.
   ```

4. **Update Progress File**

   After skill completes, update `.skillchain-progress.json`:
   - Update skill status to "complete"
   - Add skill outputs
   - Merge into accumulated_context
   - Update timestamps
   - Increment completed_count
   - Advance current_index

5. **Continue with Remaining Skills**

   Loop back to delegated.md Step 4 for remaining skills.

### Option 2: Retry Failed Skill

If a skill has status "failed":

```
Retrying failed skill: {skill_name}

Previous error: {error_message}

Spawning fresh skill-executor subagent...
```

Reset skill status to "in_progress" and proceed with execution.

### Option 3: Skip to Validation

Only available if `completed_count > 0`:

```
Skipping remaining skills and running validation...

Warning: The following skills will be skipped:
- {pending_skill_1}
- {pending_skill_2}

This may result in incomplete deliverables.

Continue? (yes/no):
```

If yes, mark remaining skills as "skipped" and spawn skillchain-validator.

### Option 4: View Detailed Progress

Display comprehensive information:

```
┌────────────────────────────────────────────────────────────┐
│           DETAILED PROGRESS REPORT                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ SKILL 1: {skill_name}                                      │
│   Status: complete                                         │
│   Executor: {executor}                                     │
│   Duration: {completed_at - started_at}                    │
│   Files Created:                                           │
│     - {file_1}                                             │
│     - {file_2}                                             │
│   Decisions:                                               │
│     - {key}: {value}                                       │
│   Exports:                                                 │
│     - {key}: {value}                                       │
│                                                            │
│ SKILL 2: {skill_name}                                      │
│   Status: in_progress                                      │
│   Started: {started_at}                                    │
│   Duration: {current_time - started_at} (interrupted)      │
│   Notes: Session ended before completion                   │
│                                                            │
│ ACCUMULATED CONTEXT:                                       │
│   {full accumulated_context as YAML}                       │
│                                                            │
└────────────────────────────────────────────────────────────┘

Press Enter to return to resume options...
```

### Option 5: Cancel

```
Keeping progress file for later resume.

To resume later: /skillchain resume

To start fresh: Delete .skillchain-progress.json and run /skillchain {goal}
```

Exit without changes.

### Option 6: Delete and Start Fresh

```
⚠ This will delete all progress for this skillchain session.

Session info:
- Goal: {goal}
- Progress: {completed}/{total} skills complete
- Started: {started_at}

Are you sure? (type "DELETE" to confirm):
```

If confirmed:
```
Progress file deleted.

To start a new skillchain: /skillchain {goal}
```

---

## Step 5: Post-Resume Completion

After all remaining skills complete:

1. **Run Validation** (via skillchain-validator subagent)
2. **Update Progress File** with validation results
3. **Display Final Report** (same as delegated.md Step 7)
4. **Cleanup Option**

```
Skillchain complete!

Options:
1. Keep progress file (for reference)
2. Delete progress file (cleanup)
3. Export progress as report

Your choice:
```

---

## Error Handling

### Interrupted During Resume

If the resume session is interrupted:

- Progress file is already being updated incrementally
- Next `/skillchain resume` will pick up from last saved state

### Context Too Large

If accumulated_context exceeds reasonable size (~50KB):

```
Warning: Accumulated context is very large ({size}KB)

This may slow down skill execution. Options:
1. Summarize older skill outputs (recommended)
2. Continue with full context
3. Reset context (lose some information)

Your choice:
```

If summarizing:
- Keep most recent skill outputs in full
- Summarize older outputs to key points only
- Note summarization in progress file

### Version Mismatch

If progress file has different schema version:

```
Progress file version: {file_version}
Current schema version: {current_version}

{migration instructions if available}
{or warning about incompatibility}
```

---

## Progress File Operations

### Reading Progress

```python
# Read and parse
with open('.skillchain-progress.json', 'r') as f:
    progress = json.load(f)

# Validate schema
assert progress.get('version') == '1.0'
assert 'session_id' in progress
assert 'skills' in progress
assert 'execution' in progress
```

### Updating Progress

```python
# Update after skill completion
progress['skills'][current_index]['status'] = 'complete'
progress['skills'][current_index]['completed_at'] = datetime.now().isoformat()
progress['skills'][current_index]['outputs'] = skill_outputs

# Update execution state
progress['execution']['completed_count'] += 1
progress['execution']['current_index'] += 1
progress['updated_at'] = datetime.now().isoformat()

# Write back
with open('.skillchain-progress.json', 'w') as f:
    json.dump(progress, f, indent=2)
```

---

## Implementation Notes

### For Orchestrator (Coordinator Agent)

When resuming, you should:

1. Read `.skillchain-progress.json` from project root
2. Parse and validate against schema
3. Present options to user
4. On continue: switch to delegated.md execution mode
5. Pass accumulated_context to skill-executors
6. Update progress file after each skill
7. Complete validation and final report

### State Persistence

The progress file IS the state. No other state needed:
- Survives context rotation
- Survives session end
- Can be version controlled (optional)
- Human readable for debugging

### Known Limitations

Per Claude Code GitHub Issue #11712:
- agent_id may not enable true agent resume
- Always re-provide full context on resume
- Don't rely solely on Task tool resume parameter

---

## Quick Reference

| Command | Effect |
|---------|--------|
| `/skillchain resume` | Resume from current directory |
| `/skillchain resume /path/to/project` | Resume from specific project |
| Option 1 | Continue from next pending skill |
| Option 2 | Retry a failed skill |
| Option 3 | Skip to validation |
| Option 4 | View detailed progress |
| Option 5 | Cancel and keep progress |
| Option 6 | Delete progress and start fresh |

---

## Related Files

- `delegated.md` - Main orchestrator that creates progress files
- `skillchain-data/shared/progress-schema.yaml` - Progress file schema
- `skill-executor.md` - Subagent that executes skills
- `skillchain-validator.md` - Subagent that validates completion
