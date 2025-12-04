---
sidebar_position: 3
title: Building Forms
description: Form systems with 50+ input types, validation strategies, and accessibility patterns
tags: [frontend, forms, validation, accessibility]
---

# Building Forms

Build accessible, user-friendly forms with systematic component selection, validation strategies, and UX best practices.

## When to Use

Use this skill when:
- Creating forms, collecting user input, or building surveys
- Implementing validation or error handling patterns
- Building contact forms, registration flows, or checkout processes
- Designing multi-step workflows or wizards
- Ensuring form accessibility (WCAG 2.1 AA)
- Collecting structured data (addresses, credit cards, dates)

## Overview

Forms are the primary mechanism for user data input in web applications. This skill provides systematic guidance for:
- Selecting appropriate input types based on data requirements
- Implementing validation strategies that enhance user experience
- Ensuring WCAG 2.1 AA accessibility compliance
- Creating complex patterns (multi-step wizards, conditional fields, dynamic forms)

## Component Selection Framework

**The Golden Rule:** Data Type → Input Component → Validation Pattern

### Quick Reference

- **Short text** (&lt;100 chars) → Text input, Email input, Password input
- **Long text** (>100 chars) → Textarea, Rich text editor
- **Numeric** → Number input, Currency input, Slider
- **Date/Time** → Date picker, Time picker, Date range picker
- **Boolean** → Checkbox, Toggle switch
- **Single choice** → Radio group (2-7 options), Select dropdown (>7 options)
- **Multiple choice** → Checkbox group, Multi-select, Tag input
- **File/Media** → File upload, Image upload
- **Structured** → Address input, Credit card input, Phone number input

## Validation Timing Strategies

### Recommended Default: On Blur with Progressive Enhancement

```
Field pristine (never touched): No validation
User typing: No errors shown
On blur (field loses focus): Validate and show errors
After first error: Switch to onChange for that field
On fix: Show success immediately
```

### Validation Modes
1. **On Submit** - Simple forms
2. **On Blur** - RECOMMENDED for most forms
3. **On Change** - Password strength, availability checks
4. **Debounced** - API-based validation
5. **Progressive** - Start on-blur, switch to on-change after first error

## Accessibility Requirements (WCAG 2.1 AA)

### Critical Patterns

**Labels and Instructions:**
- Every input must have an associated `&lt;label>` or `aria-label`
- Labels must be visible and descriptive
- Required fields clearly indicated (not by color alone)
- Never use placeholder text as label replacement

**Keyboard Navigation:**
- Logical, sequential tab order
- All inputs keyboard accessible
- Custom components support arrow keys
- Escape key dismisses modals/popovers

**Error Handling:**
- Errors programmatically associated (`aria-describedby`)
- Error messages clear and actionable
- Errors announced by screen readers (`aria-live`)
- Focus moves to first error on submit

## Quick Start (React + Zod)

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
    mode: 'onBlur',
  });

  return (
    &lt;form onSubmit={handleSubmit(onSubmit)}>
      &lt;label htmlFor="email">Email&lt;/label>
      &lt;input id="email" {...register('email')} type="email" />
      {errors.email && &lt;span role="alert">{errors.email.message}&lt;/span>}

      &lt;button type="submit">Login&lt;/button>
    &lt;/form>
  );
}
```

## Component Tiers

### Tier 1: Basic Input Components
- Text field, Textarea, Email input, Password input
- Number input, Tel input, URL input, Search input
- Radio group, Checkbox, Toggle switch, Select dropdown
- Date picker, Time picker, Date range picker

### Tier 2: Rich Input Components
- Autocomplete/Combobox, Tag input, Transfer list
- Color picker, File uploader, Image uploader
- Slider/Range, Rating input, Rich text editor
- Address input, Credit card input, Phone number input

### Tier 3: Complex Form Patterns
- Linear wizard, Branching wizard, Progress indicators
- Conditional fields, Repeating sections, Field arrays
- Inline editing, Bulk editing, Autosave, Undo/redo

## Error Message Best Practices

### Good Error Message Formula
1. **What's wrong** - "Email address is not valid"
2. **Why it matters** - "We need this to send your receipt"
3. **How to fix** - "Format: name@example.com"

✅ **Good:** "Email address must include @ symbol (e.g., name@example.com)"
❌ **Bad:** "Invalid input"

## Related Skills

- [Theming Components](./theming-components.md) - Form styling with design tokens
- [Providing Feedback](./providing-feedback.md) - Validation feedback and success messages
- [Implementing Navigation](./implementing-navigation.md) - Multi-step wizard navigation

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/building-forms)
- Decision Framework: `references/decision-tree.md`
- Validation: `references/validation-concepts.md`
- Accessibility: `references/accessibility-forms.md`
- UX Patterns: `references/ux-patterns.md`
- Implementation: `references/javascript/react-hook-form.md`, `references/python/pydantic-forms.md`
