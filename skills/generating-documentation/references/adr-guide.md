# Architecture Decision Records (ADR) Guide

Guide to documenting architectural decisions using MADR (Markdown Any Decision Records).

## Table of Contents

1. [When to Write an ADR](#when-to-write-an-adr)
2. [MADR Template Format](#madr-template-format)
3. [ADR Workflow](#adr-workflow)
4. [ADR Lifecycle](#adr-lifecycle)
5. [Best Practices](#best-practices)
6. [Tools](#tools)
7. [Integration with Documentation Sites](#integration-with-documentation-sites)
8. [Common Patterns](#common-patterns)

## When to Write an ADR

### Write an ADR for:

✅ **Significant Architectural Decisions**
- Database selection (PostgreSQL vs MySQL vs MongoDB)
- Framework choice (React vs Vue vs Angular)
- Cloud provider selection (AWS vs GCP vs Azure)
- Architecture pattern (microservices vs monolith)
- Communication protocol (REST vs GraphQL vs gRPC)

✅ **Decisions with Trade-Offs**
- Multiple viable options exist
- Significant pros and cons to consider
- Future developers need context for the choice

✅ **Team Alignment Decisions**
- Affects multiple teams or services
- Requires buy-in from stakeholders
- Long-term commitment (hard to reverse)

✅ **Compliance or Security**
- Regulatory requirements
- Security architecture choices
- Data handling policies

### Don't Write an ADR for:

❌ **Trivial Decisions**
- Variable naming conventions
- Code formatting preferences
- Temporary workarounds

❌ **Easily Reversible Decisions**
- Library version updates (use package.json/requirements.txt)
- Configuration tweaks
- Feature flags

❌ **Implementation Details**
- Function implementations (document in code comments)
- Algorithm choices for small utilities
- Private API designs

## MADR Template Format

The MADR (Markdown Any Decision Records) template is the recommended format.

### Template Structure

```markdown
# [Title: Short noun phrase]

* Status: [proposed | rejected | accepted | deprecated | superseded]
* Deciders: [list everyone involved]
* Date: [YYYY-MM-DD]

Technical Story: [description or link to ticket]

## Context and Problem Statement

[2-3 sentences describing the context and problem]

## Decision Drivers

* [Force, concern, or requirement that influenced the decision]
* [Another driver]

## Considered Options

* [Option 1]
* [Option 2]
* [Option 3]

## Decision Outcome

Chosen option: "[Option X]", because [justification].

### Positive Consequences

* [Improvement or benefit]
* [Another positive consequence]

### Negative Consequences

* [Compromise or limitation]
* [Another negative consequence]

## Pros and Cons of the Options

### [Option 1]

* Good, because [argument]
* Good, because [argument]
* Bad, because [argument]

### [Option 2]

* Good, because [argument]
* Bad, because [argument]
* Bad, because [argument]

## Links

* [Related ADR or resource]
```

## ADR Workflow

### 1. Create ADR Directory

```bash
mkdir -p docs/adr
```

### 2. Copy Template

```bash
cp templates/adr-template.md docs/adr/0001-database-selection.md
```

### 3. Fill in Template

Complete all sections with specific information.

### 4. Review and Discuss

- Share with team for feedback
- Update based on discussion
- Iterate until consensus

### 5. Finalize

- Set status to "accepted" (or "rejected")
- Commit to version control
- Reference in main documentation

### 6. Link from Documentation

```markdown
# Architecture

For architectural decisions, see [ADR directory](adr/).

Recent decisions:
- [ADR-0001: Use PostgreSQL](adr/0001-use-postgresql.md)
- [ADR-0002: Adopt Microservices](adr/0002-microservices.md)
```

## Example ADR: Database Selection

See `examples/adr/0001-database-selection.md` for a complete real-world example.

## ADR Lifecycle

### Status Values

- **proposed**: Under discussion, not yet decided
- **accepted**: Decision approved and implemented
- **rejected**: Considered but not chosen
- **deprecated**: Previously accepted, now obsolete
- **superseded by [ADR-XXXX]**: Replaced by newer decision

### Updating ADRs

When a decision changes:

1. Create new ADR for the new decision
2. Update old ADR status to "superseded by [ADR-XXXX]"
3. Link both ADRs bidirectionally

Example:

```markdown
# ADR-0001: Use REST API

* Status: superseded by [ADR-0012](0012-graphql-migration.md)
* Date: 2024-01-15

[Original content...]
```

```markdown
# ADR-0012: Migrate to GraphQL

* Status: accepted
* Date: 2025-03-20
* Supersedes: [ADR-0001](0001-rest-api.md)

[New content...]
```

## Best Practices

1. **Number ADRs sequentially**: 0001, 0002, 0003...
2. **Use descriptive titles**: "Use PostgreSQL" not "Database"
3. **Be specific**: Concrete examples over abstract descriptions
4. **Document alternatives**: Show what was considered
5. **Explain trade-offs**: Honest assessment of pros and cons
6. **Keep it brief**: 1-2 pages maximum
7. **Date decisions**: Track when decisions were made
8. **Name deciders**: Who was involved in the decision
9. **Link related ADRs**: Build a decision graph
10. **Review regularly**: Deprecate outdated decisions

## Tools

### adr-tools

Command-line tool for managing ADRs:

```bash
# Install
brew install adr-tools

# Initialize ADR directory
adr init docs/adr

# Create new ADR
adr new "Use PostgreSQL for primary database"

# Create ADR that supersedes another
adr new -s 1 "Migrate to MongoDB"

# Generate table of contents
adr generate toc > docs/adr/README.md
```

### log4brains

Documentation site with ADR support:

```bash
# Install
npm install -g log4brains

# Initialize
log4brains init

# Preview
log4brains preview

# Build
log4brains build
```

## Integration with Documentation Sites

### Docusaurus Integration

```javascript
// docusaurus.config.js
module.exports = {
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          path: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
        },
      },
    ],
  ],
};

// sidebars.js
module.exports = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'Architecture Decisions',
      items: [
        'adr/0001-database-selection',
        'adr/0002-microservices',
      ],
    },
  ],
};
```

### MkDocs Integration

```yaml
# mkdocs.yml
nav:
  - Home: index.md
  - Architecture Decisions:
    - ADR-0001 Database Selection: adr/0001-database-selection.md
    - ADR-0002 Microservices: adr/0002-microservices.md
```

## Common Patterns

### Pattern 1: Technology Selection

Template for choosing technologies (databases, frameworks, languages):

1. **Context**: Current state and requirements
2. **Drivers**: Performance, cost, developer experience, ecosystem
3. **Options**: 3-5 alternatives considered
4. **Decision**: Chosen option with justification
5. **Consequences**: Trade-offs accepted

### Pattern 2: Architecture Pattern

Template for architectural style decisions:

1. **Context**: System requirements and constraints
2. **Drivers**: Scalability, maintainability, team structure
3. **Options**: Monolith, microservices, serverless, etc.
4. **Decision**: Pattern chosen with rationale
5. **Consequences**: Implementation requirements

### Pattern 3: Migration Decision

Template for migration or refactoring:

1. **Context**: Problems with current approach
2. **Drivers**: Pain points, new requirements
3. **Options**: Stay, migrate, hybrid approach
4. **Decision**: Migration path chosen
5. **Consequences**: Migration effort, timeline, risks
