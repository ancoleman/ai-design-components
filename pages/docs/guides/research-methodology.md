---
sidebar_position: 2
title: Research Methodology
description: How we validate library recommendations
---

# Research Methodology

Learn how to validate library recommendations and component patterns before implementing skills.

## Overview

This guide explains the research methodology used to evaluate libraries and patterns for Claude Skills. Use this whenever you're about to implement a skill to ensure you're using the latest, most secure, and best-maintained libraries.

**Last Updated:** November 13, 2025

## When to Use This Guide

**Use this guide when:**
- About to implement a component skill for the first time
- Library recommendations are >6 months old
- Concerned about security vulnerabilities
- Want to validate current best practices
- New alternatives may have emerged

**Skip this guide if:**
- Library recommendations are recent (&lt;3 months)
- Prototyping/experimenting (not production)
- No research tools available in your environment
- Time-sensitive implementation

## Available Research Tools

Your environment may have different research capabilities. Use whatever is available:

### Tool 1: Google Search Grounding (Preferred)

**MCP Tool Names:**
- `mcp__litellm__gs-google_search_grounding` (LiteLLM environments)
- May have other variants depending on MCP server

**When Available:**
- Most reliable for technical queries
- AI-grounded search results
- Provides sources
- Handles complex queries well

**Known Issues:**
- May return HTTP 500 errors (Vertex AI DSQ 429 errors)
- **Solution:** Retry up to 4 times per query
- If all retries fail, fall back to Context7 only

### Tool 2: Context7 (Library Documentation)

**MCP Tool Names:**
- `mcp__context7__resolve-library-id` and `mcp__context7__get-library-docs`
- OR `mcp__litellm__context7-resolve-library-id` and `mcp__litellm__context7-get-library-docs`

**When Available:**
- Excellent for getting official documentation
- Up-to-date library docs
- Code examples from actual repos
- Trust scores and snippet counts

**Two-Step Process:**
1. **Resolve Library ID** (find the library)
2. **Get Documentation** (fetch specific docs)

### Tool 3: WebSearch (Legacy - Often Unavailable)

**Tool Name:** `WebSearch`

**Availability:**
- Often NOT available in MCP-configured environments
- May be available in standard Claude.ai
- Check before attempting to use

**Recommendation:** Try Google Search Grounding first. WebSearch is likely unavailable.

## Research Methodology

### Step 1: Understand the Component Domain

**Before searching, consider:**
- What is this component for? (forms, charts, tables, etc.)
- What are the key challenges? (performance, accessibility, complexity)
- What features are critical? (validation, virtualization, streaming)
- What are common pain points? (bundle size, learning curve, maintenance)

### Step 2: Formulate Search Queries

**Query Pattern:**
```
[component type] [framework] library [year] [key concerns] comparison best practices
```

**Key Concerns by Component Type:**

- **Forms:** validation, performance, accessibility, bundle size, TypeScript
- **Data Visualization:** accessibility, WCAG, colorblind, performance, chart types
- **Tables:** virtualization, performance, sorting, filtering, accessibility
- **AI Chat:** streaming, markdown rendering, security, memoization
- **Dashboards:** KPI components, grid layouts, real-time updates
- **Navigation:** accessibility, keyboard, mobile, responsive

### Step 3: Execute Research

**Recommended Approach:**

**A. Start with Google Search Grounding** (if available)

Query examples:
- Library comparison: "[component] React library 2025 [top libraries] comparison"
- Best practices: "[component] accessibility WCAG 2.1 best practices 2025"
- Security: "[primary library] security vulnerabilities CVE latest version"

**Retry Logic for 500 Errors:**
- Attempt 1 → 500 error → Wait 2s
- Attempt 2 → 500 error → Wait 4s
- Attempt 3 → 500 error → Wait 8s
- Attempt 4 → 500 error → Fall back to Context7 only

**B. Get Library Documentation via Context7** (if available)

For each library:
1. Resolve library ID
2. Select best match (highest trust score + most snippets)
3. Get documentation with relevant topics

**C. Synthesize Findings**
- Compare trust scores
- Evaluate code snippet availability
- Assess bundle sizes
- Check maintenance status
- Consider accessibility support
- Evaluate learning curve

### Step 4: Evaluation Criteria

**Trust Score (from Context7):**
- 9-10: Highly trusted, well-maintained
- 7-9: Good, reliable
- 5-7: Acceptable, verify further
- &lt;5: Caution, may be immature

**Code Snippet Count:**
- 500+: Excellent documentation
- 100-500: Good documentation
- 50-100: Adequate documentation
- &lt;50: Limited examples

**Maintenance:**
- Check GitHub: Commits in last 3 months?
- Active issues being addressed?
- Regular releases?

**Bundle Size:**
- &lt;10KB: Excellent
- 10-50KB: Good
- 50-100KB: Acceptable
- >100KB: Evaluate if features justify size

**Accessibility:**
- ARIA support built-in?
- Keyboard navigation?
- Screen reader tested?
- WCAG 2.1 AA compliant?

**TypeScript:**
- Native TypeScript?
- Type inference quality?
- Type definitions included?

**Community:**
- GitHub stars (>5K good, >10K excellent)
- Weekly downloads (npm)
- Active community discussions?

## Query Patterns for Common Scenarios

### Pattern 1: Library Comparison

```
"[component type] React library 2025 [lib1] vs [lib2] vs [lib3] comparison"

Examples:
"React form library 2025 React Hook Form vs Formik comparison"
"data visualization library 2025 D3.js vs Recharts accessibility"
"React table library 2025 TanStack Table vs AG Grid performance"
```

### Pattern 2: Best Practices

```
"[component type] [key concern] best practices 2025 React"

Examples:
"form validation best practices 2025 React accessibility"
"data visualization accessibility WCAG 2.1 best practices"
"table virtualization performance best practices React 2025"
```

### Pattern 3: Security & Updates

```
"[library name] security vulnerabilities CVE latest version 2025"
"[library name] breaking changes migration guide"

Examples:
"React Hook Form security vulnerabilities CVE 2025"
"Recharts breaking changes migration guide v2 to v3"
```

## Context7 Research Pattern

### For Each Primary Library:

**1. Resolve Library ID**

Evaluate results by:
- Looking for highest Trust Score
- Checking Code Snippet count (more = better docs)
- Verifying description matches your need
- Choosing official org over forks

**2. Get Documentation**

Topic formulation guide:
- **Forms**: "validation integration getting started accessibility"
- **Data Viz**: "charts accessibility getting started customization"
- **Tables**: "sorting filtering pagination virtualization"
- **AI Chat**: "streaming responses markdown rendering"
- **Dashboards**: "KPI cards grid layout real-time updates"

## Evaluation Decision Tree

```
Start: Researching libraries for [component]
│
├─→ Google Search Grounding Available?
│   ├─ YES → Search for comparisons and best practices
│   │   ├─ Success → Extract library names
│   │   └─ 500 Error → Retry up to 4 times → Fall back to Context7
│   └─ NO → Proceed to Context7
│
├─→ Context7 Available?
│   ├─ YES → For each library:
│   │   ├─ Resolve library ID
│   │   ├─ Check trust score and snippets
│   │   ├─ Get documentation
│   │   └─ Extract patterns and examples
│   └─ NO → Use existing recommendations from init.md
│
└─→ Synthesize:
    ├─ Compare trust scores
    ├─ Evaluate features vs needs
    ├─ Consider bundle size
    ├─ Check accessibility support
    └─ Make recommendation
```

## Common Pitfalls to Avoid

### Don't:
- Use hardcoded queries (adapt to component domain)
- Ignore trust scores (low trust = risky)
- Skip accessibility validation
- Forget bundle size consideration
- Overlook maintenance status

### Do:
- Formulate queries based on component needs
- Prioritize high trust scores (>7.0)
- Verify accessibility support
- Consider bundle size trade-offs
- Check recent commit activity
- Look for TypeScript support
- Evaluate code snippet availability

## Handling Tool Unavailability

### If NO Research Tools Available:

**The library recommendations in each init.md are:**
- ✅ Researched comprehensively (November 2025)
- ✅ Based on trust scores and code snippets
- ✅ Validated with working examples
- ✅ Production-ready and battle-tested

**You can confidently use them without additional research.**

## Research Workflow Example

### Scenario: Researching Form Libraries

**1. Formulate Queries**

Forms need: validation, performance, accessibility, ease of use

Queries:
- "React form library 2025 React Hook Form Formik performance validation comparison"
- "form validation library 2025 Zod Yup TypeScript best practices"
- "React form accessibility WCAG 2.1 ARIA patterns best practices"

**2. Execute Google Search Grounding**

Extract: React Hook Form has best performance, Zod for validation

**3. Resolve Library IDs via Context7**

- React Hook Form: /react-hook-form/react-hook-form (Trust: 9.1, Snippets: 279)
- Zod: /colinhacks/zod (Trust: 9.6, Snippets: 576)

**4. Get Documentation**

Fetch documentation with relevant topics for each library

**5. Synthesize Findings**

**React Hook Form:**
- Trust: 9.1/10 ✅
- Snippets: 279+ ✅
- Performance: Best in class ✅
- Bundle: 8KB ✅
- TypeScript: Excellent ✅
- **Recommendation:** Primary choice

**Zod:**
- Trust: 9.6/10 ✅
- Snippets: 576+ ✅
- TypeScript: First-class ✅
- Integration: Works seamlessly with React Hook Form ✅
- **Recommendation:** Pair with React Hook Form

**6. Document in init.md**

Add library recommendations section with findings.

## Key Questions to Answer

### For Each Library, Determine:

**1. Maturity & Maintenance**
- Is it actively maintained?
- Recent commits/releases?
- Responsive to issues?

**2. Performance**
- Bundle size acceptable?
- Runtime performance benchmarks?
- Handles scale?

**3. Accessibility**
- WCAG 2.1 AA compliant?
- ARIA patterns implemented?
- Keyboard navigation?

**4. Developer Experience**
- TypeScript support?
- Good documentation?
- Code examples available?

**5. Integration**
- Works with React 18+?
- Compatible with frameworks?
- Plays well with other libraries?

**6. Security**
- Recent CVEs?
- Security advisories?
- Regular security updates?

## Summary

**This guide teaches:**
- ✅ How to formulate effective queries
- ✅ How to use available research tools
- ✅ How to evaluate libraries systematically
- ✅ How to synthesize findings
- ✅ How to handle tool unavailability

**Not:**
- ❌ Specific queries to run (you formulate based on component)
- ❌ Which library to choose (you decide based on criteria)
- ❌ Hardcoded recommendations (those are in init.md as starting point)

**Remember:** The init.md recommendations are already excellent. This research is for validation and ensuring you have the latest information for your specific environment and requirements.

## Next Steps

- [Creating Skills](./creating-skills.md) - Learn how to implement skills
- [Best Practices](./best-practices.md) - Anthropic's official guidelines
- [Skills Overview](../skills/overview.md) - Explore existing skills

---

**Use your understanding of the component domain, available tools, and project requirements to conduct thorough, effective library research.**
