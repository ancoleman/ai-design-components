# Claude Skills Development: Best Practices by Anthropic

## Table of Contents

1. [Introduction to Skills](#introduction-to-skills)
2. [Core Principles](#core-principles)
3. [Skill Structure and Requirements](#skill-structure-and-requirements)
4. [Writing Effective Skills](#writing-effective-skills)
5. [Progressive Disclosure Patterns](#progressive-disclosure-patterns)
6. [Content Organization](#content-organization)
7. [Workflows and Feedback Loops](#workflows-and-feedback-loops)
8. [Skills with Executable Code](#skills-with-executable-code)
9. [Development Process](#development-process)
10. [Testing and Evaluation](#testing-and-evaluation)
11. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
12. [Checklist for Effective Skills](#checklist-for-effective-skills)

---

## Introduction to Skills

**What are Skills?**

Skills are folders containing instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. They teach Claude how to complete specific tasks in a repeatable way, whether creating documents with brand guidelines, analyzing data using organizational workflows, or automating tasks.

**Key Characteristics:**

- **Progressive Disclosure**: Claude determines which Skills are relevant and loads only the information needed for the current task
- **Composable**: Skills stack together - Claude automatically identifies needed skills and coordinates their use
- **Token Efficient**: At startup, only metadata (name and description) from all Skills is pre-loaded. SKILL.md is read only when relevant
- **Universal**: Skills work across Claude.ai, Claude Code, and the API

**How Skills Work:**

1. Metadata from all Skills' YAML frontmatter is loaded into the system prompt at startup
2. When a task matches a Skill's description, Claude reads the SKILL.md file
3. Claude can then access additional bundled files and scripts as needed
4. Only accessed content consumes context tokens

---

## Core Principles

### 1. Concise is Key

**The Context Window is a Public Good**

Your Skill shares the context window with:
- The system prompt
- Conversation history  
- Other Skills' metadata
- The user's actual request

**Ask yourself:**
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Best Practice**: Remove any content Claude likely already knows. Claude has extensive general knowledge - your Skill should only add specialized information.

### 2. Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability.

**High Freedom (Text-Based Instructions)**

Use when:
- Multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach
- A preferred pattern exists
- Some variation is acceptable

**Medium Freedom (Configuration/Templates)**

Use when:
- Configuration affects behavior
- A template provides structure
- Consistency helps but variation is allowed

**Low Freedom (Executable Scripts)**

Use when:
- Operations are fragile and error-prone
- Consistency is critical
- A specific sequence must be followed

**Mental Model:**
- **Narrow bridge with cliffs**: Provide specific guardrails and exact instructions (low freedom)
- **Open field with no hazards**: Give general direction and trust Claude to find the best route (high freedom)

### 3. Test with All Target Models

Skills act as additions to models, so effectiveness depends on the underlying model.

**Testing Considerations:**
- **Claude Haiku** (fast, economical): Does the Skill provide enough guidance?
- **Claude Sonnet** (balanced): Is the Skill clear and efficient?
- **Claude Opus** (powerful reasoning): Does the Skill avoid over-explaining?

---

## Skill Structure and Requirements

### Basic File Structure

```
my-skill-name/
├── SKILL.md          # Required: Main instructions with YAML frontmatter
├── reference/        # Optional: Additional documentation
│   ├── examples.md
│   └── guidelines.md
└── scripts/          # Optional: Executable utilities
    └── helper.py
```

### SKILL.md Requirements

#### YAML Frontmatter

```yaml
---
name: skill-name
description: A clear description of what this skill does and when to use it
---
```

**Field Requirements:**

**`name`:**
- Maximum 64 characters
- Must contain only lowercase letters, numbers, and hyphens
- Cannot contain XML tags
- Cannot contain reserved words: "anthropic", "claude"

**`description`:**
- Must be non-empty
- Maximum 1024 characters
- Cannot contain XML tags
- Should describe both what the Skill does AND when to use it

#### Body Content

- Keep under 500 lines for optimal performance
- Use progressive disclosure for longer content
- Write in clear, concise markdown

---

## Writing Effective Skills

### Naming Conventions

**Recommended: Gerund Form (verb + -ing)**

This clearly describes the activity or capability the Skill provides.

**Good Examples:**
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`
- `writing-documentation`

**Avoid:**
- Noun phrases: `pdf-processing`, `spreadsheet-analysis`
- Vague names: `helper`, `utils`, `tools`
- Overly generic: `documents`, `data`, `files`
- Reserved words: `anthropic-helper`, `claude-tools`
- Inconsistent patterns within your skill collection

**Why This Matters:**
- Makes Skills easy to reference in documentation and conversations
- Helps understand what a Skill does at a glance
- Facilitates organization and search through multiple Skills
- Maintains a professional, cohesive skill library

### Writing Effective Descriptions

The description field enables Skill discovery and should include:
1. What the Skill does
2. When to use it

**Good Examples:**
- ✓ "Processes Excel files and generates reports"
- ✓ "Creates branded PowerPoint presentations following company style guidelines"
- ✓ "Analyzes customer data and identifies churn patterns"

**Avoid:**
- ✗ "I can help you process Excel files"
- ✗ "You can use this to process Excel files"
- ✗ "Helpful utilities for data analysis"

### Content Guidelines

#### Avoid Time-Sensitive Information

Don't include information that will become outdated.

**Bad Example:**
```markdown
Current API version: v2.1 (as of January 2025)
Latest rate limit: 100 requests/minute
```

**Good Example:**
```markdown
Check the API documentation for the current version and rate limits.
```

Or if the information is likely to remain stable, include it in an "older patterns" section with context.

#### Use Consistent Terminology

Choose one term and use it throughout the Skill.

**Good - Consistent:**
- Always "API endpoint"
- Always "field"
- Always "extract"

**Bad - Inconsistent:**
- Mix "API endpoint", "URL", "API route", "path"
- Mix "field", "box", "element", "control"
- Mix "extract", "pull", "get", "retrieve"

---

## Progressive Disclosure Patterns

SKILL.md serves as an overview that points Claude to detailed materials as needed, like a table of contents in an onboarding guide.

### Visual Overview: From Simple to Complex

**Level 1: Simple Skill**
- Single SKILL.md file
- Metadata and instructions only
- Best for straightforward tasks

**Level 2: Bundled References**
- SKILL.md as main guide
- Additional reference files (reference.md, examples.md)
- Claude reads additional files as needed

**Level 3: Executable Scripts**
- SKILL.md with instructions
- Reference documentation
- Utility scripts for deterministic operations
- Claude executes scripts without loading them into context

### Pattern 1: High-Level Guide with References

**SKILL.md:**
```markdown
# Data Analysis Skill

## Overview
This skill helps with analyzing customer data.

## Common Workflows
See workflows.md for detailed step-by-step guides.

## Data Schemas
See schemas.md for complete field definitions.
```

**Benefits:**
- Keeps main file concise
- Detailed information loaded only when needed
- Easy to maintain and update specific sections

### Pattern 2: Domain-Specific Organization

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context.

**Example Structure:**
```
data-analysis/
├── SKILL.md           # Overview and domain guide
├── sales/
│   ├── metrics.md
│   └── reports.md
├── finance/
│   ├── budgets.md
│   └── forecasts.md
└── marketing/
    ├── campaigns.md
    └── attribution.md
```

**In SKILL.md:**
```markdown
# Data Analysis

For sales-related analysis: See sales/metrics.md
For financial analysis: See finance/budgets.md
For marketing analysis: See marketing/campaigns.md
```

**Benefits:**
- When user asks about sales metrics, only sales files are read
- Keeps token usage low and context focused
- Scales well as domains expand

### Pattern 3: Conditional Details

Show basic content, link to advanced content.

```markdown
# API Integration

## Basic Usage
[Basic instructions here]

## Advanced
For error handling strategies, see advanced/error-handling.md
For performance optimization, see advanced/optimization.md
```

### Critical: Avoid Deeply Nested References

❌ **Bad - Too Deep:**
```
SKILL.md references advanced.md
advanced.md references troubleshooting.md  # ← Problem!
```

Claude may partially read files when they're referenced from other referenced files, resulting in incomplete information.

✅ **Good - One Level Deep:**
```
SKILL.md references:
- advanced.md
- troubleshooting.md
- examples.md
```

All reference files should link directly from SKILL.md to ensure Claude reads complete files when needed.

### Structure Longer Reference Files

For reference files longer than 100 lines, include a table of contents at the top.

**Example:**
```markdown
# Advanced API Usage

## Table of Contents
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Retry Logic](#retry-logic)

## Authentication
[Content here]

## Error Handling
[Content here]
```

**Why This Helps:**
Claude can see the full scope of available information even when previewing with partial reads.

---

## Content Organization

### Common Patterns

#### Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

**For Strict Requirements (like API responses or data formats):**

```markdown
Use this exact JSON structure:
{
  "status": "success|error",
  "data": {},
  "timestamp": "ISO 8601 format"
}
```

**For General Guidance:**

```markdown
Reports should include:
- Executive summary
- Key findings
- Supporting data
- Recommendations
```

#### Examples Pattern

For Skills where output quality depends on seeing examples, provide input/output pairs.

```markdown
# Report Generation

## Examples

### Example 1: Sales Report
**Input:**
Q4 revenue: $1.2M
Growth: 15%
Top product: Widget Pro

**Output:**
Q4 PERFORMANCE SUMMARY
Revenue reached $1.2M, representing 15% growth YoY.
Widget Pro emerged as the leading product...

### Example 2: Marketing Report
[Another complete example]
```

#### Conditional Workflow Pattern

Guide Claude through decision points.

```markdown
# Customer Support Response

1. Analyze the customer's issue
2. Check issue severity:
   - If urgent: Follow escalation/urgent.md
   - If technical: Follow technical/troubleshooting.md  
   - If billing: Follow billing/resolution.md
3. Draft response using appropriate template
4. Validate response against tone guidelines
```

---

## Workflows and Feedback Loops

### Use Workflows for Complex Tasks

Break complex operations into clear, sequential steps.

**Example 1: Research Synthesis (No Code)**

```markdown
# Research Workflow

1. **Gather**: Collect relevant sources and documents
2. **Extract**: Pull key findings from each source  
3. **Synthesize**: Identify patterns and themes across sources
4. **Draft**: Write synthesis following template
5. **Review**: Check against quality criteria before finalizing
```

**For Complex Tasks, Provide a Checklist:**

```markdown
## Project Analysis Checklist

Copy this checklist and check off items as you complete them:

- [ ] Load project documentation
- [ ] Identify key stakeholders
- [ ] Review technical requirements
- [ ] Assess risks and dependencies
- [ ] Draft recommendations
- [ ] Validate against criteria
- [ ] Format final report
```

### Implement Feedback Loops

**Common Pattern**: Run validator → fix errors → repeat

This pattern greatly improves output quality.

**Example 1: Style Guide Compliance (No Code)**

```markdown
# Brand Voice Guidelines

## Workflow
1. Draft content following brand guidelines
2. Review against checklist:
   - Uses conversational tone?
   - Avoids jargon?
   - Includes benefit statements?
3. If any item fails, revise and review again
4. When all items pass, content is ready
```

**Example 2: Data Validation (With Code)**

```markdown
# Data Processing Workflow

1. Process data following transformation rules
2. Run validation script: `python scripts/validate.py`
3. Review validation output:
   - If errors found: Fix issues and return to step 2
   - If warnings: Assess whether to proceed
   - If clean: Continue to next step
4. Generate final report
```

---

## Skills with Executable Code

### When to Use Scripts

**Benefits of Utility Scripts:**
- More reliable than generated code
- Save tokens (no need to include code in context)
- Save time (no code generation required)
- Ensure consistency across uses

**When to Prefer Scripts:**
- Deterministic operations (sorting, validation, transformation)
- Complex algorithms
- Operations that must be consistent
- Error-prone processes

### Best Practices for Scripts

#### 1. Solve, Don't Punt

Handle error conditions rather than punting to Claude.

**Bad Example:**
```python
def process_data(file_path):
    if not os.path.exists(file_path):
        return "File not found"  # Punts to Claude
```

**Good Example:**
```python
def process_data(file_path):
    if not os.path.exists(file_path):
        return {
            "error": "File not found",
            "suggestion": f"Available files in directory: {os.listdir('.')}"
        }
```

#### 2. Provide Clear Execution Intent

Make it clear whether Claude should execute or read the script.

```markdown
# PDF Form Processing

To extract form fields: **Run** `scripts/extract_fields.py path/to/form.pdf`

To understand the extraction algorithm: **Read** `scripts/extract_fields.py`
```

#### 3. No "Voodoo Constants"

Document all magic numbers and configuration values.

**Bad:**
```python
threshold = 0.85  # Why 0.85?
```

**Good:**
```python
# Confidence threshold for classification
# Based on validation testing showing 95% accuracy at 0.85
# Lower values increase false positives
threshold = 0.85
```

### Advanced Patterns

#### Use Visual Analysis

When inputs can be rendered as images, have Claude analyze them.

**Example:**
```markdown
# PDF Form Analysis

1. Convert PDF to images using `scripts/pdf_to_images.py`
2. Analyze the rendered form visually to identify field types
3. Extract field metadata using `scripts/extract_fields.py`
4. Validate extracted data
```

#### Create Verifiable Intermediate Outputs

Use the "plan-validate-execute" pattern to catch errors early.

**Example: PDF Form Filling**

```markdown
# Workflow

1. **Analyze**: Extract form structure
2. **Plan**: Create changes.json with proposed updates
3. **Validate**: Run `python scripts/validate_changes.py changes.json`
4. **Review validation output**:
   - If errors: Fix changes.json and return to step 3
   - If warnings: Assess whether to proceed
   - If clean: Continue to step 5
5. **Execute**: Apply changes using `scripts/apply_changes.py`
6. **Verify**: Confirm all fields updated correctly
```

**Why This Works:**
- Catches errors early before changes are applied
- Machine-verifiable through scripts
- Reversible planning - Claude can iterate without touching originals
- Clear debugging with specific error messages

### Package Dependencies

Skills run in the code execution environment with platform-specific limitations.

**claude.ai:**
- Can install packages from npm and PyPI
- Can pull from GitHub repositories

**Anthropic API:**
- No network access
- No runtime package installation

**Best Practice:**
- List all required packages in SKILL.md
- Verify packages are available in the code execution tool documentation
- Don't assume packages are installed

**Example:**
```markdown
# Dependencies

This skill requires:
- Python: pandas, numpy, openpyxl
- Node: xlsx, chalk

On Claude.ai, these will be installed automatically when needed.
On API, ensure these are pre-installed in your environment.
```

### Runtime Environment

**How Claude Accesses Skills:**

1. **Metadata pre-loaded**: Name and description from YAML frontmatter loaded into system prompt at startup
2. **Files read on-demand**: Claude uses bash tools to read SKILL.md and other files when needed
3. **Scripts executed efficiently**: Utility scripts run via bash without loading full contents into context - only output consumes tokens
4. **No context penalty for large files**: Reference files don't consume context tokens until actually read

**Authoring Implications:**

- **File paths matter**: Use forward slashes (`reference/guide.md`), not backslashes
- **Name files descriptively**: `form_validation_rules.md`, not `doc2.md`
- **Organize for discovery**: 
  - Good: `reference/finance.md`, `reference/sales.md`
  - Bad: `docs/file1.md`, `docs/file2.md`
- **Bundle comprehensive resources**: Include complete docs, extensive examples, large datasets - no context penalty until accessed
- **Prefer scripts for deterministic operations**: Write `validate_form.py` rather than asking Claude to generate validation code

---

## Development Process

### Evaluation-Driven Development

**Create evaluations BEFORE writing extensive documentation.** This ensures your Skill solves real problems rather than documenting imagined ones.

#### Process:

1. **Identify gaps**: Run Claude on representative tasks without a Skill. Document specific failures or missing context.

2. **Create evaluations**: Build three scenarios that test these gaps.

3. **Establish baseline**: Measure Claude's performance without the Skill.

4. **Write minimal instructions**: Create just enough content to address the gaps and pass evaluations.

5. **Iterate**: Execute evaluations, compare against baseline, and refine.

### Develop Skills Iteratively with Claude

**The Two-Claude Method:**

Work with one instance of Claude ("Claude A") to create a Skill that will be used by other instances ("Claude B").

- **Claude A**: Expert who helps design and refine the Skill
- **Claude B**: Agent using the Skill to perform real work

This works because Claude models understand both how to write effective agent instructions and what information agents need.

#### Creating a New Skill:

**Step 1: Complete a task without a Skill**

Work through a problem with Claude A using normal prompting. As you work, you'll naturally provide context, explain preferences, and share procedural knowledge. Notice what information you repeatedly provide.

**Step 2: Identify the reusable pattern**

After completing the task, identify what context you provided that would be useful for similar future tasks.

**Example:**
If you worked through a BigQuery analysis, you might have provided:
- Table names
- Field definitions
- Filtering rules (like "always exclude test accounts")
- Common query patterns

**Step 3: Ask Claude A to create a Skill**

```
Create a Skill that captures this BigQuery analysis pattern we just used. 
Include the table schemas, naming conventions, and the rule about 
filtering test accounts.
```

Claude models understand the Skill format natively. You don't need special system prompts or a "writing skills" skill.

**Step 4: Review for conciseness**

Check that Claude A hasn't added unnecessary explanations.

Ask: "Remove the explanation about what win rate means - Claude already knows that."

**Step 5: Improve information architecture**

Ask Claude A to organize content more effectively.

Example: "Organize this so the table schema is in a separate reference file. We might add more tables later."

**Step 6: Test on similar tasks**

Use the Skill with Claude B (a fresh instance with the Skill loaded) on related use cases. Observe whether Claude B:
- Finds the right information
- Applies rules correctly
- Handles the task successfully

**Step 7: Iterate based on observation**

If Claude B struggles or misses something, return to Claude A with specifics.

Example: "When Claude used this Skill, it forgot to filter by date for Q4. Should we add a section about date filtering patterns?"

#### The Observation Loop:

```
┌─────────────────────────────────────────┐
│ 1. Use Skill with Claude B on real task │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 2. Observe where Claude B succeeds      │
│    or struggles                          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 3. Return to Claude A with observations │
│    and current SKILL.md                  │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 4. Claude A suggests improvements       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 5. Apply changes and test again         │
└────────────────┬────────────────────────┘
                 │
                 └─────────────────────────┘
```

#### Real Usage Testing:

- **Give Claude B actual tasks**, not test scenarios
- **Observe Claude B's behavior**: Note where it struggles, succeeds, or makes unexpected choices
- **Example observation**: "When I asked Claude B for a regional sales report, it wrote the query but forgot to filter out test accounts, even though the Skill mentions this rule."

#### Collaborative Refinement:

- Share Skills with teammates and observe their usage
- Ask: Does the Skill activate when expected? Are instructions clear? What's missing?
- Incorporate feedback to address blind spots in your own usage patterns

### Observe How Claude Navigates Skills

As you iterate, pay attention to how Claude actually uses Skills in practice. Watch for:

- **Unexpected exploration paths**: Does Claude read files in an order you didn't anticipate? Your structure might not be as intuitive as you thought.

- **Missed connections**: Does Claude fail to follow references to important files? Your links might need to be more explicit or prominent.

- **Overreliance on certain sections**: If Claude repeatedly reads the same file, consider whether that content should be in the main SKILL.md instead.

- **Ignored content**: If Claude never accesses a bundled file, it might be unnecessary or poorly signaled in the main instructions.

---

## Testing and Evaluation

### Build Evaluations First

Before writing extensive documentation:

1. Run Claude on representative tasks without a Skill
2. Document specific failures or missing context
3. Create at least three test scenarios
4. Establish performance baseline
5. Write minimal Skill content to pass evaluations
6. Iterate based on evaluation results

### Test Across Models

Test your Skill with all models you plan to use:

**Haiku Testing:**
- Does it provide enough guidance?
- Are instructions clear and unambiguous?
- Does it avoid assuming too much knowledge?

**Sonnet Testing:**
- Is the Skill clear and efficient?
- Is the right balance of detail provided?
- Does it work smoothly for typical use cases?

**Opus Testing:**
- Does it avoid over-explaining?
- Can Opus handle it with less guidance?
- Is token usage optimal for this powerful model?

### Real-World Testing

- Test with actual use cases, not just hypotheticals
- Observe Claude's behavior patterns
- Note any confusion or misinterpretation
- Track when Skill is invoked vs. when it should be
- Monitor token usage and performance

---

## Anti-Patterns to Avoid

### ❌ Avoid Windows-Style Paths

Always use forward slashes in file paths, even on Windows.

**Good:**
- `scripts/helper.py`
- `reference/guide.md`

**Bad:**
- `scripts\helper.py`
- `reference\guide.md`

### ❌ Avoid Offering Too Many Options

Don't present multiple approaches unless necessary.

**Bad:**
```markdown
You can either:
A. Use approach 1 with method X
B. Use approach 2 with method Y
C. Use approach 3 with method Z
```

**Good:**
```markdown
Use this approach for standard cases: [clear instructions]

For special cases, see advanced/edge-cases.md
```

### ❌ Avoid Deeply Nested References

Keep references one level deep from SKILL.md.

**Bad:**
```
SKILL.md → advanced.md → troubleshooting.md
```

**Good:**
```
SKILL.md → advanced.md
SKILL.md → troubleshooting.md
```

### ❌ Don't Assume Package Availability

Always list required packages and verify availability.

**Bad:**
```markdown
Run the analysis script.
```

**Good:**
```markdown
# Dependencies
This skill requires: pandas, numpy, matplotlib

Run the analysis script: python scripts/analyze.py
```

### ❌ Don't Include Unnecessary Context

If Claude already knows it, don't include it.

**Bad:**
```markdown
Python is a programming language. To use it, you write code
in .py files. Variables store data...
```

**Good:**
```markdown
Use these specific pandas operations for our data format:
[specific, specialized instructions]
```

### ❌ Don't Use Time-Sensitive Information

Avoid content that will become outdated.

**Bad:**
```markdown
Current rate limit: 100/min (as of Jan 2025)
```

**Good:**
```markdown
Check current rate limits in the API documentation
```

### ❌ Don't Mix Terminology

Choose one term and stick with it.

**Bad:**
- Mix "API endpoint", "URL", "route"
- Mix "field", "box", "element"

**Good:**
- Always "API endpoint"
- Always "field"

---

## Checklist for Effective Skills

Use this checklist before sharing a Skill:

### ✅ Core Quality

- [ ] Description is specific and includes key terms
- [ ] Description includes both what the Skill does AND when to use it
- [ ] SKILL.md body is under 500 lines
- [ ] Additional details are in separate files (if needed)
- [ ] No time-sensitive information (or clearly marked as older patterns)
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep from SKILL.md
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear, sequential steps

### ✅ Naming and Structure

- [ ] Name uses gerund form (verb + -ing)
- [ ] Name contains only lowercase letters, numbers, and hyphens
- [ ] Name is under 64 characters
- [ ] Description is under 1024 characters and non-empty
- [ ] YAML frontmatter is properly formatted
- [ ] File paths use forward slashes
- [ ] Files are named descriptively

### ✅ Code and Scripts

- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" - all values justified
- [ ] Required packages listed and verified as available
- [ ] Scripts have clear documentation
- [ ] Execution intent is clear (run vs. read)
- [ ] Validation/verification steps for critical operations
- [ ] Feedback loops included for quality-critical tasks

### ✅ Testing and Validation

- [ ] At least three evaluations created
- [ ] Tested with Haiku, Sonnet, and Opus (for applicable use cases)
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated (if applicable)
- [ ] Skill activates when expected
- [ ] Performance is acceptable
- [ ] Token usage is reasonable

### ✅ Documentation and References

- [ ] Reference files longer than 100 lines have a table of contents
- [ ] Progressive disclosure patterns used effectively
- [ ] Examples are provided where output quality matters
- [ ] Templates provided for structured outputs
- [ ] Conditional workflows documented clearly

### ✅ MCP Integration (if applicable)

- [ ] Fully qualified tool names used (ServerName:tool_name)
- [ ] Tool availability is not assumed
- [ ] Clear documentation of which MCP servers are required

---

## Additional Resources

### Official Documentation

- **Anthropic Skills Documentation**: https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills
- **Skills Best Practices**: https://anthropic.mintlify.app/en/docs/agents-and-tools/agent-skills/best-practices
- **Skills Cookbook**: https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/cookbook
- **GitHub Repository**: https://github.com/anthropics/skills

### Example Skills

Anthropic provides several reference skills:

**Document Skills:**
- `docx` - Word document creation and editing
- `pdf` - PDF manipulation and form filling
- `pptx` - PowerPoint presentation creation
- `xlsx` - Excel spreadsheet creation and analysis

**Utility Skills:**
- `skill-creator` - Guides you through creating new skills
- `template-skill` - Basic starting point for new skills

### Key Takeaways

1. **Start Simple**: Begin with minimal content that solves the core problem
2. **Test Early**: Build evaluations before extensive documentation
3. **Iterate with Claude**: Use the two-Claude method for development
4. **Progressive Disclosure**: Keep main file under 500 lines, reference additional content
5. **Be Concise**: Only include what Claude doesn't already know
6. **Use Scripts**: Prefer executable code for deterministic operations
7. **Observe Usage**: Watch how Claude navigates your Skill and adjust
8. **Test Across Models**: Verify effectiveness with Haiku, Sonnet, and Opus

---

## Version Information

This document is based on Anthropic's official Skills documentation and best practices as of November 2025. For the most current information, always refer to the official Anthropic documentation.

---

*This best practices guide is designed to help you create effective, maintainable, and efficient Claude Skills. Remember: the best Skills are concise, well-tested, and solve real problems.*