# Library Research & Validation Guide

**Purpose:** This guide teaches the methodology for researching and validating library recommendations before implementing component skills. Use this whenever you're about to implement a skill to ensure you're using the latest, most secure, and best-maintained libraries.

**Audience:** Claude Code, Claude API, or any AI agent implementing these skills

**Last Updated:** November 13, 2025

---

## When to Use This Guide

**Use this guide when:**
- About to implement a component skill for the first time
- Library recommendations are >6 months old
- Concerned about security vulnerabilities
- Want to validate current best practices
- New alternatives may have emerged

**Skip this guide if:**
- Library recommendations are recent (<3 months)
- Prototyping/experimenting (not production)
- No research tools available in your environment
- Time-sensitive implementation

---

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

**Example Usage:**
```typescript
mcp__litellm__gs-google_search_grounding({
  query: "React form library 2025 React Hook Form vs Formik security performance",
  max_results: 8
})
```

---

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

**Example Workflow:**
```typescript
// Step 1: Find library
resolve-library-id({
  libraryName: "React Hook Form"
})
// Returns: /react-hook-form/react-hook-form (Trust: 9.1, Snippets: 279)

// Step 2: Get docs
get-library-docs({
  context7CompatibleLibraryID: "/react-hook-form/react-hook-form",
  topic: "validation integration getting started",
  tokens: 6000
})
// Returns: Official documentation with code examples
```

---

### Tool 3: WebSearch (Legacy - Often Unavailable)

**Tool Name:** `WebSearch`

**Availability:**
- Often NOT available in MCP-configured environments
- May be available in standard Claude.ai
- Check before attempting to use

**Known Issues:**
- Blocked in many environments (like LiteLLM with MCP)
- Less reliable than Google Search Grounding
- May return "not available" errors

**Recommendation:** Try Google Search Grounding first. WebSearch is likely unavailable.

---

## Research Methodology

### Step 1: Understand the Component Domain

**Before searching, consider:**
- What is this component for? (forms, charts, tables, etc.)
- What are the key challenges? (performance, accessibility, complexity)
- What features are critical? (validation, virtualization, streaming)
- What are common pain points? (bundle size, learning curve, maintenance)

---

### Step 2: Formulate Search Queries

**Query Pattern:**
```
[component type] [framework] library [year] [key concerns] comparison best practices
```

**Key Concerns by Component Type:**

**Forms:**
- validation, performance, accessibility, bundle size, TypeScript

**Data Visualization:**
- accessibility, WCAG, colorblind, performance, chart types, SVG vs Canvas

**Tables:**
- virtualization, performance, sorting, filtering, accessibility, large datasets

**AI Chat:**
- streaming, markdown rendering, security, memoization, real-time

**Dashboards:**
- KPI components, grid layouts, real-time updates, responsive

**Feedback (Toasts/Modals):**
- accessibility, ARIA, keyboard navigation, animations, bundle size

**Navigation:**
- accessibility, keyboard, mobile, responsive, SEO

**Search/Filter:**
- performance, debouncing, accessibility, faceting

**Layout:**
- CSS Grid, Flexbox, responsive, container queries

**Media:**
- lazy loading, optimization, accessibility, responsive images

**Timeline:**
- accessibility, performance, real-time updates

**Drag-Drop:**
- accessibility, touch support, keyboard alternatives, mobile

**Onboarding:**
- accessibility, skip options, progress tracking

---

### Step 3: Execute Research

**Recommended Approach:**

**A. Start with Google Search Grounding** (if available)
```typescript
// Query 1: Library comparison
query: "[component] React library 2025 [top 2-3 libraries] comparison"

// Query 2: Best practices
query: "[component] accessibility WCAG 2.1 best practices 2025"

// Query 3: Security (if applicable)
query: "[primary library] security vulnerabilities CVE latest version"
```

**Retry Logic for 500 Errors:**
```
Attempt 1 → 500 error → Wait 2s
Attempt 2 → 500 error → Wait 4s
Attempt 3 → 500 error → Wait 8s
Attempt 4 → 500 error → Fall back to Context7 only
```

**B. Get Library Documentation via Context7** (if available)
```typescript
// For each library identified:
// 1. Resolve
resolve-library-id({ libraryName: "[Library Name]" })

// 2. Select best match (highest trust score + most snippets)

// 3. Get docs
get-library-docs({
  context7CompatibleLibraryID: "/org/project",
  topic: "[relevant topics for this component]",
  tokens: 6000
})
```

**C. Synthesize Findings**
- Compare trust scores
- Evaluate code snippet availability
- Assess bundle sizes
- Check maintenance status
- Consider accessibility support
- Evaluate learning curve

---

### Step 4: Evaluation Criteria

**Rate each library on:**

**Trust Score (from Context7):**
- 9-10: Highly trusted, well-maintained
- 7-9: Good, reliable
- 5-7: Acceptable, verify further
- <5: Caution, may be immature

**Code Snippet Count:**
- 500+: Excellent documentation
- 100-500: Good documentation
- 50-100: Adequate documentation
- <50: Limited examples

**Maintenance:**
- Check GitHub: Commits in last 3 months?
- Active issues being addressed?
- Regular releases?

**Bundle Size:**
- <10KB: Excellent
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

---

## Query Patterns for Common Scenarios

### Pattern 1: Library Comparison

```
"[component type] React library 2025 [lib1] vs [lib2] vs [lib3] comparison"

Examples:
"React form library 2025 React Hook Form vs Formik vs React Final Form comparison"
"data visualization library 2025 D3.js vs Recharts vs Plotly accessibility"
"React table library 2025 TanStack Table vs AG Grid performance virtualization"
```

### Pattern 2: Best Practices

```
"[component type] [key concern] best practices 2025 React"

Examples:
"form validation best practices 2025 React accessibility"
"data visualization accessibility WCAG 2.1 colorblind best practices"
"table virtualization performance best practices React 2025"
```

### Pattern 3: Security & Updates

```
"[library name] security vulnerabilities CVE latest version 2025"
"[library name] breaking changes migration guide [old version] to [new version]"

Examples:
"React Hook Form security vulnerabilities CVE 2025"
"Recharts breaking changes migration guide v2 to v3"
```

### Pattern 4: Integration & Compatibility

```
"[library1] integration with [library2] 2025 TypeScript"

Examples:
"React Hook Form integration with Zod TypeScript validation"
"Recharts integration with design tokens theming customization"
```

---

## Context7 Research Pattern

### For Each Primary Library:

**1. Resolve Library ID**
```typescript
resolve-library-id({
  libraryName: "[Library Name]"
  // Claude: Use the exact name from search results
})
```

**Evaluate Results:**
- Look for highest Trust Score
- Check Code Snippet count (more = better docs)
- Verify description matches your need
- If multiple matches, choose official org (e.g., /vercel/ai over forks)

**2. Get Documentation**
```typescript
get-library-docs({
  context7CompatibleLibraryID: "/org/project",  // From step 1
  topic: "[relevant topics]",  // Claude: Formulate based on component needs
  tokens: 6000  // Adjust based on complexity
})
```

**Topic Formulation Guide:**
- **Forms**: "validation integration getting started accessibility"
- **Data Viz**: "charts accessibility getting started customization"
- **Tables**: "sorting filtering pagination virtualization"
- **AI Chat**: "streaming responses markdown rendering"
- **Dashboards**: "KPI cards grid layout real-time updates"

**Claude: Formulate topics that answer:**
- How to get started?
- How to use key features?
- How to ensure accessibility?
- How to optimize performance?

---

## Synthesizing Research Results

### Creating Library Recommendations Section

**Structure:**
```markdown
## Recommended Libraries & Tools

### [Component Type] Libraries (2025)

#### **Primary: [Library Name]** ([Key Benefit])

**Library:** `/org/project`
**Trust Score:** X.X/10
**Code Snippets:** XXX+

**Why [Library]?**
- [Key benefit 1]
- [Key benefit 2]
- [Key benefit 3]

**When to Use:**
- [Use case 1]
- [Use case 2]

**Installation:**
```bash
npm install [package-name]
```

**Example:**
[Working code example from Context7 docs]

---

#### **Alternative: [Library Name]**
[Same structure]

---

### Library Comparison Matrix

| Library | [Criterion 1] | [Criterion 2] | Best For |
|---------|---------------|---------------|----------|
| **Lib 1** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | [Use case] |

---

### Recommendations by Use Case

**[Use Case 1] → [Library]**
- [Why]

**[Use Case 2] → [Library]**
- [Why]
```

---

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

---

## Common Pitfalls to Avoid

### ❌ Don't:
- Use hardcoded queries (adapt to component domain)
- Ignore trust scores (low trust = risky)
- Skip accessibility validation
- Forget bundle size consideration
- Overlook maintenance status

### ✅ Do:
- Formulate queries based on component needs
- Prioritize high trust scores (>7.0)
- Verify accessibility support
- Consider bundle size trade-offs
- Check recent commit activity
- Look for TypeScript support
- Evaluate code snippet availability

---

## Environment-Specific Guidance

### Claude Code Client (Desktop)

**Typically Available:**
- Google Search Grounding (via LiteLLM MCP)
- Context7 (via LiteLLM MCP)

**Typically NOT Available:**
- WebSearch (blocked in MCP-configured environments)

**Configuration:**
- Check `.claude/mcp-config.json` for enabled servers
- LiteLLM integration provides Vertex AI grounding

---

### Claude API (Programmatic)

**Depends on Configuration:**
- MCP tools available if server configured
- No search tools by default
- Context7 if MCP server set up

**Fallback:**
- Use existing recommendations from init.md
- They are comprehensive and production-ready

---

### Claude.ai (Web)

**May Have:**
- Web search capabilities (check environment)
- Limited MCP support (check release notes)

**Fallback:**
- Existing recommendations are valid
- Can implement without additional research

---

## Research Workflow Example

### Scenario: Researching Form Libraries

**1. Formulate Queries (Component Understanding)**

Forms need: validation, performance, accessibility, ease of use

**Queries:**
```
"React form library 2025 React Hook Form Formik performance validation comparison"
"form validation library 2025 Zod Yup TypeScript best practices"
"React form accessibility WCAG 2.1 ARIA patterns best practices"
```

**2. Execute Google Search Grounding**

```typescript
// Query 1: Library comparison
mcp__litellm__gs-google_search_grounding({
  query: "React form library 2025 React Hook Form Formik performance validation",
  max_results: 8
})

// Extract: React Hook Form has best performance, Zod for validation

// Query 2: Accessibility
mcp__litellm__gs-google_search_grounding({
  query: "React form accessibility WCAG ARIA validation error messages",
  max_results: 8
})

// Extract: onBlur validation recommended, ARIA-live for errors
```

**3. Resolve Library IDs via Context7**

```typescript
// For React Hook Form
mcp__context7__resolve-library-id({
  libraryName: "React Hook Form"
})
// Returns: /react-hook-form/react-hook-form (Trust: 9.1, Snippets: 279)

// For Zod
mcp__context7__resolve-library-id({
  libraryName: "Zod"
})
// Returns: /colinhacks/zod (Trust: 9.6, Snippets: 576)
```

**4. Get Documentation**

```typescript
// React Hook Form docs
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/react-hook-form/react-hook-form",
  topic: "validation integration TypeScript getting started",
  tokens: 6000
})

// Zod docs
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/colinhacks/zod",
  topic: "schema validation form integration",
  tokens: 6000
})
```

**5. Synthesize Findings**

**React Hook Form:**
- Trust: 9.1/10 ✅
- Snippets: 279+ ✅
- Performance: Best in class (30-40% fewer re-renders than Formik) ✅
- Bundle: 8KB (smallest) ✅
- TypeScript: Excellent ✅
- **Recommendation:** Primary choice

**Zod:**
- Trust: 9.6/10 ✅
- Snippets: 576+ ✅
- TypeScript: First-class (type inference) ✅
- Integration: Works seamlessly with React Hook Form ✅
- **Recommendation:** Pair with React Hook Form

**6. Document in init.md**

Add library recommendations section with findings.

---

## Key Questions to Answer

### For Each Library, Determine:

**1. Maturity & Maintenance**
- Is it actively maintained?
- Recent commits/releases?
- Responsive to issues?
- Long-term support?

**2. Performance**
- Bundle size acceptable?
- Runtime performance benchmarks?
- Optimization strategies documented?
- Handles scale (for data-heavy components)?

**3. Accessibility**
- WCAG 2.1 AA compliant?
- ARIA patterns implemented?
- Keyboard navigation?
- Screen reader tested?

**4. Developer Experience**
- TypeScript support?
- Good documentation?
- Code examples available?
- Active community?

**5. Integration**
- Works with React 18+?
- Compatible with Next.js/Remix/etc?
- Plays well with other libraries?
- Headless/flexible?

**6. Security**
- Recent CVEs?
- Security advisories?
- Regular security updates?
- Sandboxed/safe?

---

## Comparison Matrix Template

Create a comparison matrix for evaluated libraries:

| Library | Trust | Snippets | Bundle | Accessibility | TypeScript | Best For |
|---------|-------|----------|--------|---------------|-----------|----------|
| **Lib 1** | 9.1 | 279+ | 8KB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Most projects |
| **Lib 2** | 8.5 | 150+ | 15KB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Complex cases |

**Star Rating Guide:**
- ⭐⭐⭐⭐⭐ Excellent
- ⭐⭐⭐⭐ Good
- ⭐⭐⭐ Acceptable
- ⭐⭐ Limited
- ⭐ Poor

---

## Handling Tool Unavailability

### If NO Research Tools Available:

**The library recommendations in each init.md are:**
- ✅ Researched comprehensively (November 2025)
- ✅ Based on trust scores and code snippets
- ✅ Validated with working examples
- ✅ Production-ready and battle-tested

**You can confidently use them without additional research.**

**Validate later:**
- Check npm for latest versions
- Review GitHub for recent activity
- Scan for CVEs manually
- Read changelogs for breaking changes

---

## Special Considerations

### Security-Critical Components

**For components handling user data:**
- Forms (user input, validation)
- AI Chat (LLM output, prompt injection)
- File Upload (malicious files)

**Extra validation:**
- Search for recent CVEs
- Check security advisories
- Verify sanitization practices
- Look for penetration test results

---

### Performance-Critical Components

**For components rendering large data:**
- Tables (virtualization needed >10K rows)
- Data Viz (Canvas needed >1K points)
- AI Chat (memoization for streaming)

**Extra validation:**
- Benchmark data available?
- Virtualization support?
- Lazy loading patterns?
- Memory leak prevention?

---

### Accessibility-Critical Components

**For public-facing applications:**
- All components (WCAG 2.1 AA minimum)
- Forms (keyboard, validation, errors)
- Data Viz (text alternatives, color contrast)
- Modals (focus management, ESC key)

**Extra validation:**
- ARIA patterns documented?
- Keyboard navigation complete?
- Screen reader tested?
- Contrast ratios validated?

---

## Example: Complete Research for Tables

**1. Google Search Grounding:**
```
Query: "React table library 2025 TanStack Table AG Grid Material-UI virtualization performance"
Result: TanStack Table popular, AG Grid enterprise, virtualization critical
```

**2. Context7 Resolution:**
```
Library: "TanStack Table"
Result: /tanstack/table (Trust: 8.0, Snippets: 661)

Library: "AG Grid"
Result: Multiple options, choose based on need (Community vs Enterprise)
```

**3. Context7 Documentation:**
```
Library: /tanstack/table
Topic: "sorting filtering pagination virtualization"
Result: Comprehensive docs with examples
```

**4. Synthesis:**
```
Primary: TanStack Table
- Trust: 8.0/10
- Headless (complete styling control)
- Works with design tokens
- Virtual scrolling support
- Framework agnostic

Alternative: AG Grid
- Enterprise features (pivoting, charts)
- More opinionated
- Commercial license for advanced features
```

**5. Document:**
Add to tables/init.md with comparison matrix and use cases.

---

## Research Output Template

### Document Your Findings:

```markdown
## Recommended Libraries & Tools

**Research Date:** [Date]
**Research Tools Used:** [Google Search Grounding, Context7, etc.]
**Libraries Evaluated:** [Count]

### [Component Type] Libraries (2025)

#### **Primary: [Library]** ([Key Advantage])

**Library:** `/org/project`
**Trust Score:** X.X/10
**Code Snippets:** XXX+
**Bundle Size:** XKB
**Research Notes:** [Key findings from search]

[Rest of structure...]
```

---

## FAQ

**Q: What if Google Search fails 4 times?**
A: Fall back to Context7 only. Use library IDs to get documentation directly.

**Q: What if no research tools available?**
A: Use existing recommendations from init.md. They're comprehensive and production-ready.

**Q: How often should I re-research?**
A: Every 6-12 months, or when major versions release, or for security-critical updates.

**Q: Should I research ALL libraries or just primary?**
A: Research primary + top 2-3 alternatives. Gives you options and comparison data.

**Q: What if Context7 doesn't have the library?**
A: Search for similar libraries, check GitHub directly, or use alternative with good Context7 coverage.

---

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

---

**Use your understanding of the component domain, available tools, and project requirements to conduct thorough, effective library research.**
