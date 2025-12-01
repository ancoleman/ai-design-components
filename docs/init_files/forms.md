# AI-Assisted Component Library: Form Systems & Input Patterns
## Master Plan for Form Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025
**Purpose:** Comprehensive research and strategic planning for building an AI-assisted component library focused on form systems, input patterns, validation, and data collection interfaces

---

## Executive Summary

Forms are the primary mechanism for user data input in web applications, yet they remain one of the most complex and error-prone aspects of UI development. This skill provides systematic guidance for selecting appropriate input types, implementing validation strategies, ensuring accessibility, and creating excellent user experiences across simple contact forms to complex multi-step workflows.

**Key Value Propositions:**
- Systematic selection framework: Data type → Input component → Validation pattern
- Comprehensive accessibility guidance (WCAG 2.1 AA compliance)
- Progressive complexity: Simple inputs → Rich controls → Multi-step workflows
- Clear decision trees for validation timing and error handling
- Modern patterns (2024-2025): Inline validation, smart defaults, progressive disclosure

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Component Taxonomy](#component-taxonomy)
3. [Selection Framework](#selection-framework)
4. [Validation Strategies](#validation-strategies)
5. [Accessibility Requirements](#accessibility-requirements)
6. [UX Patterns & Best Practices](#ux-patterns--best-practices)
7. [Implementation Approach](#implementation-approach)
8. [Skill Structure](#skill-structure)

---

## Strategic Positioning

### Why Forms Need AI-Assisted Guidance

**Complexity Factors:**
- 50+ input component variants
- 10+ validation timing strategies
- Accessibility requirements (ARIA labels, keyboard nav, screen readers)
- Error handling UX (when to show, where to place, how to phrase)
- State management complexity
- Performance considerations (large forms, conditional fields)

**Common Pain Points:**
- Choosing wrong input type for data (text field vs. select vs. autocomplete)
- Inaccessible forms (missing labels, poor keyboard support)
- Poor validation UX (blocking users, unclear errors)
- Complex multi-step forms with state management issues
- Mobile usability problems

**Skills Architecture Benefits:**
- **Progressive disclosure**: Load basic patterns, reference advanced when needed
- **Decision trees**: Clear guidance from data type to implementation
- **Accessibility checklists**: Ensure WCAG compliance
- **Code snippets**: Common patterns ready to use
- **Validation scripts**: Schema validators, rule engines

---

## Component Taxonomy

### Tier 1: Basic Input Components

**Text-Based Inputs**
- Text field (single-line)
- Text area (multi-line)
- Email input (with validation pattern)
- Password input (with visibility toggle, strength meter)
- Number input (with step controls)
- Tel input (with formatting)
- URL input (with protocol validation)
- Search input (with clear button, suggestions)

**Selection Components**
- Radio group (mutually exclusive choices, 2-7 options)
- Checkbox (single boolean or multiple selections)
- Checkbox group (multiple related choices)
- Toggle switch (clear on/off states)
- Select dropdown (many options, single selection)
- Multi-select (many options, multiple selections)

**Date & Time**
- Date picker (calendar interface)
- Time picker (hour/minute selection)
- Date range picker (start and end dates)
- Date-time picker (combined)
- Duration input (hours, minutes, seconds)

---

### Tier 2: Rich Input Components

**Advanced Selection**
- Autocomplete/Combobox (type to filter, keyboard navigation)
- Tag input (multiple freeform or predefined tags)
- Transfer list (move items between lists)
- Listbox (keyboard-navigable list)
- Button group (exclusive or multi-select)

**Specialized Inputs**
- Color picker (hex, RGB, HSL, swatches)
- File uploader (single, multiple, drag-drop, preview)
- Image uploader (crop, resize, preview)
- Slider/Range (single value or range)
- Rating input (stars, numeric, emoji)
- Rich text editor (formatting, media, links)
- Code editor (syntax highlighting, linting)
- Markdown editor (preview, toolbar)

**Structured Data**
- Address input (multi-field, autocomplete)
- Credit card input (formatted, validation)
- Phone number (international formatting)
- Currency input (symbol, decimal handling)
- Percentage input (with constraints)

---

### Tier 3: Complex Form Patterns

**Multi-Step Forms**
- Linear wizard (step 1 → 2 → 3)
- Branching wizard (conditional steps)
- Progress indicators (steps, percentage, checklist)
- Save and resume (draft state)
- Review and submit page

**Dynamic Forms**
- Conditional fields (show/hide based on answers)
- Repeating sections (add/remove items)
- Field arrays (dynamic list of inputs)
- Nested forms (complex object editing)
- Form builder (meta: building forms)

**Advanced Patterns**
- Inline editing (click to edit in table/list)
- Bulk editing (multiple records simultaneously)
- Autosave (periodic or on change)
- Optimistic updates (UI responds before server)
- Undo/redo functionality

---

## Selection Framework

### Decision Tree: Data Type → Component

```
START: What type of data are you collecting?

├─→ SHORT TEXT (<100 chars)
│   ├─ Free-form? → Text input
│   ├─ Email? → Email input (with validation)
│   ├─ Password? → Password input (with visibility toggle)
│   ├─ Phone? → Tel input (with formatting)
│   ├─ URL? → URL input
│   └─ Search? → Search input (with suggestions)

├─→ LONG TEXT (>100 chars)
│   ├─ Plain text? → Textarea
│   ├─ Rich formatting? → Rich text editor
│   ├─ Code? → Code editor (with syntax highlighting)
│   └─ Markdown? → Markdown editor

├─→ NUMERIC
│   ├─ Integer? → Number input (step=1)
│   ├─ Decimal? → Number input (step=0.01)
│   ├─ Currency? → Currency input (formatted)
│   ├─ Percentage? → Percentage input (0-100)
│   └─ Range? → Slider or dual slider

├─→ DATE/TIME
│   ├─ Single date? → Date picker
│   ├─ Date range? → Date range picker
│   ├─ Time only? → Time picker
│   ├─ Date + time? → DateTime picker
│   └─ Duration? → Duration input

├─→ BOOLEAN (Yes/No)
│   ├─ Single choice? → Checkbox
│   ├─ Clear on/off state? → Toggle switch
│   └─ Part of group? → Radio group

├─→ SINGLE CHOICE
│   ├─ 2-5 options, visible? → Radio group
│   ├─ 6-15 options? → Select dropdown
│   ├─ >15 options? → Autocomplete/Combobox
│   └─ Need search? → Autocomplete with search

├─→ MULTIPLE CHOICE
│   ├─ 2-7 options? → Checkbox group
│   ├─ 8-20 options? → Multi-select dropdown
│   ├─ >20 options? → Transfer list or autocomplete multi
│   └─ Freeform tags? → Tag input

├─→ FILE/MEDIA
│   ├─ Single file? → File upload
│   ├─ Multiple files? → Multi-file upload (drag-drop)
│   ├─ Images only? → Image upload (with preview/crop)
│   └─ Specific format? → File upload (with type restriction)

├─→ COLOR
│   └─ → Color picker (hex, RGB, or swatches)

├─→ STRUCTURED/COMPLEX
│   ├─ Address? → Address input (multi-field)
│   ├─ Credit card? → Card input (formatted)
│   ├─ List of items? → Field array (repeating section)
│   └─ Nested object? → Nested form or accordion

└─→ RATING/FEEDBACK
    ├─ Scale (1-5)? → Star rating or radio group
    ├─ Satisfaction? → Emoji rating
    └─ NPS? → 0-10 scale with labels
```

---

## Validation Strategies

### Validation Timing Patterns

**1. On Submit (Default)**
- Validate when user submits form
- Show all errors at once
- Best for: Simple forms, infrequent submissions
- Pros: Not distracting during input
- Cons: Late feedback, can be frustrating

**2. On Blur (Recommended Default)**
- Validate when user leaves field
- Show errors after user finishes typing
- Best for: Most forms, balance of UX and validation
- Pros: Immediate feedback, not while typing
- Cons: Slight delay in error visibility

**3. On Change (Real-time)**
- Validate as user types
- Show errors/success immediately
- Best for: Password strength, username availability, complex rules
- Pros: Instant feedback
- Cons: Can be distracting, annoying for slow typers

**4. Debounced On Change**
- Validate after user stops typing (300-500ms delay)
- Best for: API-based validation (username, email availability)
- Pros: Real-time feel without spam
- Cons: Slight complexity

**5. Progressive Enhancement**
- Start with on-blur, switch to on-change after first error
- Best for: Complex forms, balance UX and validation
- Pros: Best of both worlds
- Cons: More complex implementation

**6. Hybrid Approach (Modern Best Practice)**
```
Field pristine (never touched): No validation
User typing: No errors shown (maybe hints)
On blur: Validate and show errors
After first error: Switch to on-change for that field
On fix: Show success immediately
```

---

### Validation Rules Catalog

**Format Validation**
- Email: RFC 5322 compliant regex or library
- URL: Protocol + domain validation
- Phone: International formats (E.164 standard)
- Credit card: Luhn algorithm
- Postal code: Country-specific patterns
- IP address: IPv4/IPv6 validation

**Content Validation**
- Min/max length (characters, words)
- Pattern matching (regex)
- Allowed characters (alphanumeric, special chars)
- Required field
- Optional field with conditional requirement

**Logical Validation**
- Min/max value (numeric ranges)
- Date ranges (not in past, within bounds)
- Cross-field validation (password confirmation, date ranges)
- Mutual exclusivity (at least one of these fields)
- Conditional requirements (if A, then B required)

**Async Validation**
- Username availability
- Email not already registered
- Domain verification
- API-based validation
- Debounced to avoid rate limiting

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance Checklist

**Labels and Instructions**
- [ ] Every input has associated `<label>` (explicit or aria-label)
- [ ] Labels are visible and descriptive
- [ ] Required fields clearly indicated (not color alone)
- [ ] Placeholder text not used as label replacement
- [ ] Help text provided for complex inputs
- [ ] Instructions precede form (what to expect)

**Keyboard Navigation**
- [ ] Tab order is logical and sequential
- [ ] All inputs keyboard accessible
- [ ] Custom components support arrow keys
- [ ] Escape key dismisses modals/popovers
- [ ] Enter submits form from any input
- [ ] Focus visible (outline or custom indicator)

**Error Handling**
- [ ] Errors programmatically associated with inputs (aria-describedby)
- [ ] Error messages clear and actionable
- [ ] Errors announced by screen readers (aria-live)
- [ ] Error summary at top of form
- [ ] Focus moves to first error on submit
- [ ] Errors not conveyed by color alone

**ARIA Attributes**
- `aria-required="true"` for required fields
- `aria-invalid="true"` when validation fails
- `aria-describedby` linking to help/error text
- `role="group"` for related inputs
- `aria-labelledby` for fieldset legends
- `aria-live="polite"` for validation messages

**Screen Reader Support**
- Form landmarks (`<form>`, `role="form"`)
- Fieldsets group related inputs
- Legends describe fieldset purpose
- Status messages announced
- Progress indicators accessible
- Multi-step forms: current step announced

---

## UX Patterns & Best Practices

### Modern Form UX Principles (2024-2025)

**1. Progressive Disclosure**
- Show only essential fields initially
- Reveal advanced options on demand
- Use accordions or tabs for long forms
- "Show more" for optional fields

**2. Smart Defaults**
- Pre-fill known information
- Suggest values based on context
- Remember previous entries
- Auto-detect (location, timezone)

**3. Inline Validation with Positive Feedback**
- Show green checkmark on valid input
- Provide helpful error messages (not just "invalid")
- Suggest corrections (did you mean...?)
- Show password strength visually

**4. Mobile-First Considerations**
- Large touch targets (44px minimum)
- Appropriate keyboard types (email, tel, number)
- Autofocus first field on mobile (carefully)
- Single-column layout
- Sticky submit button

**5. Reduce Cognitive Load**
- One question per page (when appropriate)
- Group related fields
- Use clear, concise labels
- Provide examples (e.g., "john@example.com")
- Show character/word count for limited fields

**6. Error Prevention**
- Constraints prevent invalid input (max length, numeric only)
- Autocomplete reduces typos
- Confirmation fields for critical data
- Clear formatting hints ("MM/DD/YYYY")

**7. Autosave and Recovery**
- Save draft state automatically
- Warn before losing data (navigation, timeout)
- Resume where user left off
- Clear indication of save status

---

### Error Message Best Practices

**Anatomy of Good Error Messages:**

❌ **Bad:** "Invalid input"
✅ **Good:** "Email address must include @ symbol (e.g., name@example.com)"

❌ **Bad:** "Error"
✅ **Good:** "Password must be at least 8 characters long"

❌ **Bad:** "Field required"
✅ **Good:** "Please enter your email address so we can send order confirmation"

**Error Message Formula:**
1. **What's wrong**: "Email address is not valid"
2. **Why it matters**: "We need this to send your receipt"
3. **How to fix**: "Format: name@example.com"

**Tone Guidelines:**
- Conversational, not robotic
- Helpful, not blaming
- Specific, not generic
- Actionable, not just descriptive

---

## Implementation Approach

### Recommended Tech Stack

**Form Libraries (React)**
- **React Hook Form**: Performance-focused, minimal re-renders
- **Formik**: Feature-rich, good community
- **React Final Form**: Subscription-based rendering
- **Unform**: Performance-focused, React Native support

**Validation Libraries**
- **Zod**: TypeScript-first schema validation
- **Yup**: Schema-based, widely adopted
- **Joi**: Powerful, originally for Node.js
- **Vest**: Test-like validation syntax

**Accessibility**
- **React Aria**: Adobe's accessible component primitives
- **Radix UI**: Unstyled accessible components
- **Reach UI**: Accessible React components
- **Headless UI**: Tailwind's accessible components

---

### Component Implementation Tiers

**Tier 1: Native HTML Enhanced (Start Here)**
- Use semantic HTML (`<input>`, `<select>`, `<textarea>`)
- Enhance with validation, styling, error messages
- Minimal JavaScript, maximum accessibility
- Progressive enhancement approach

**Tier 2: Custom Components (When Needed)**
- Build when native doesn't meet needs
- Maintain accessibility parity
- Use ARIA appropriately
- Test with keyboard and screen readers

**Tier 3: Complex Patterns (Advanced Cases)**
- Multi-step wizards with state management
- Dynamic forms with conditional logic
- Rich editors and specialized inputs
- Requires comprehensive testing

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate these library recommendations using available research tools (Google Search Grounding, Context7). This ensures you're using the latest, most secure versions.

**Note:** The recommendations below were researched comprehensively in November 2025 and are production-ready. Validation is optional.

---

## Recommended Libraries & Tools

### Form Management Libraries (2025)

#### **Primary: React Hook Form** (Recommended)

**Library:** `/react-hook-form/react-hook-form`
**Trust Score:** 9.1/10
**Code Snippets:** 279+
**Weekly Downloads:** 2M+

**Why React Hook Form?**
- **Best Performance**: Minimal re-renders (30-40% fewer than Formik)
- **Small Bundle**: ~8KB (vs Formik's ~15KB)
- **Uncontrolled Components**: Better performance, less state management
- **Easy Integration**: Works with any UI library
- **TypeScript First**: Excellent type inference
- **Flexible Validation**: Integrates with Zod, Yup, built-in rules

**When to Use:**
- Performance is critical (checkout, login pages)
- Simple to complex forms
- TypeScript projects
- Want minimal bundle size
- Need flexibility

**Installation:**
```bash
npm install react-hook-form
```

**Basic Example:**
```tsx
import { useForm } from 'react-hook-form';

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm();

  const onSubmit = async (data) => {
    await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('email', {
          required: 'Email is required',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'Invalid email address'
          }
        })}
        placeholder="Email"
      />
      {errors.email && <span>{errors.email.message}</span>}

      <input
        {...register('password', {
          required: 'Password is required',
          minLength: { value: 8, message: 'Min 8 characters' }
        })}
        type="password"
        placeholder="Password"
      />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

---

#### **Schema Validation: Zod** (Recommended)

**Library:** `/colinhacks/zod`
**Trust Score:** 9.6/10
**Code Snippets:** 576+

**Why Zod?**
- **TypeScript-First**: Infer types from schema automatically
- **Runtime Validation**: Type-safe at runtime, not just compile-time
- **Composable**: Build complex schemas from simple ones
- **Excellent Error Messages**: Clear, customizable
- **Integrates with React Hook Form**: `@hookform/resolvers/zod`

**Installation:**
```bash
npm install zod @hookform/resolvers
```

**Integration with React Hook Form:**
```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

// Define schema
const userSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters'),
  email: z.string().email('Invalid email address'),
  age: z.number()
    .int('Age must be an integer')
    .min(18, 'Must be at least 18 years old'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[0-9]/, 'Must contain number'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

// Infer TypeScript type
type UserFormData = z.infer<typeof userSchema>;

function RegistrationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    mode: 'onBlur' // Validate on blur
  });

  const onSubmit = (data: UserFormData) => {
    console.log(data); // Type-safe!
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('username')} />
      {errors.username && <span>{errors.username.message}</span>}

      <input {...register('email')} type="email" />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('age', { valueAsNumber: true })} type="number" />
      {errors.age && <span>{errors.age.message}</span>}

      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}

      <input {...register('confirmPassword')} type="password" />
      {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}

      <button type="submit">Register</button>
    </form>
  );
}
```

---

#### **Alternative: Formik**

**Library:** `/jaredpalmer/formik`
**Trust Score:** 10/10
**Code Snippets:** 187+

**When to Use:**
- Complex forms with heavy validation
- Prefer controlled components
- Using Material-UI or Ant Design (good Formik examples)
- Team already familiar with Formik

**Trade-offs vs React Hook Form:**
- Larger bundle size (~15KB)
- More re-renders (controlled components)
- Slightly slower performance
- More structured, opinionated approach

---

### Accessible Component Libraries

**For building accessible form inputs from scratch:**

#### **React Aria (Adobe)**
- Headless, accessible component primitives
- WCAG compliant by default
- Keyboard navigation built-in
- Screen reader support
- No styling (bring your own CSS)

```bash
npm install react-aria
```

#### **Radix UI**
- Unstyled, accessible components
- Composable primitives
- Full keyboard support
- Compatible with any styling solution

```bash
npm install @radix-ui/react-form
```

#### **Headless UI (Tailwind)**
- Fully accessible components
- Designed for Tailwind CSS
- TypeScript support
- React and Vue versions

```bash
npm install @headlessui/react
```

---

### Library Comparison Matrix

| Library | Performance | Bundle Size | Learning Curve | TypeScript | Best For |
|---------|-------------|-------------|----------------|-----------|----------|
| **React Hook Form** | ⭐⭐⭐⭐⭐ | 8KB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Most projects |
| **Formik** | ⭐⭐⭐ | 15KB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Complex forms |
| **React Final Form** | ⭐⭐⭐⭐ | 10KB | ⭐⭐⭐ | ⭐⭐⭐ | Subscription model |
| **Zod (validation)** | ⭐⭐⭐⭐⭐ | Small | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | TypeScript projects |
| **Yup (validation)** | ⭐⭐⭐⭐ | Medium | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | JavaScript projects |

---

### Validation Strategy Recommendations

**Based on Research: "On Blur with Progressive Enhancement"**

```tsx
const { register, handleSubmit } = useForm({
  mode: 'onBlur', // Validate when field loses focus
  reValidateMode: 'onChange', // After first error, switch to onChange
});
```

**Rationale:**
- Doesn't annoy users while typing
- Immediate feedback after first error
- Best UX balance (supported by research)

**Timing Options:**
- `onSubmit`: Only on form submission (least intrusive, latest feedback)
- `onBlur`: When field loses focus (**RECOMMENDED**)
- `onChange`: As user types (good for password strength, availability checks)
- `onTouched`: After field is touched and blurred
- `all`: Combination of onChange and onBlur

---

### Async Validation (Username/Email Availability)

```tsx
import { useForm } from 'react-hook-form';

function SignupForm() {
  const { register, formState: { errors } } = useForm();

  return (
    <form>
      <input
        {...register('username', {
          required: 'Username is required',
          validate: async (value) => {
            const response = await fetch(`/api/check-username?name=${value}`);
            const { available } = await response.json();
            return available || 'Username already taken';
          }
        })}
        placeholder="Username"
      />
      {errors.username && <span>{errors.username.message}</span>}
    </form>
  );
}
```

**Debounce async validation:**
```tsx
import { useForm } from 'react-hook-form';
import debounce from 'lodash/debounce';
import { useCallback } from 'react';

function Form() {
  const debouncedCheck = useCallback(
    debounce(async (value) => {
      const response = await fetch(`/api/check?value=${value}`);
      return response.json();
    }, 500),
    []
  );

  const { register } = useForm();

  return (
    <input
      {...register('username', {
        validate: async (value) => {
          const { available } = await debouncedCheck(value);
          return available || 'Already taken';
        }
      })}
    />
  );
}
```

---

### Implementation Recommendations

**Recommended Stack:**
1. **React Hook Form** - Form state management
2. **Zod** - Schema validation
3. **React Aria** or **Radix UI** - Accessible input primitives
4. **Design Tokens** - Consistent styling

**Why This Combination:**
- Best performance (React Hook Form)
- Type-safe validation (Zod + TypeScript)
- WCAG compliant (React Aria/Radix)
- Themeable (Design Tokens)

---

## Styling & Theming

### Design Token Integration

All form components use the **design-tokens** skill for visual styling, enabling theme switching, brand customization, and consistent design across applications.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--input-bg` - Input background color
- `--input-border-color` - Default border color
- `--input-border-color-focus` - Border color when focused
- `--input-border-color-error` - Border color for validation errors
- `--input-text-color` - Input text color
- `--input-placeholder-color` - Placeholder text color
- `--label-text-color` - Label text color
- `--error-text-color` - Error message color
- `--success-color` - Success state color

**Spacing Tokens:**
- `--input-padding-x` - Horizontal padding
- `--input-padding-y` - Vertical padding
- `--form-field-gap` - Space between form fields
- `--label-margin-bottom` - Space between label and input

**Typography Tokens:**
- `--input-font-size` - Input text size
- `--input-font-weight` - Input text weight
- `--label-font-size` - Label text size
- `--label-font-weight` - Label text weight
- `--error-font-size` - Error message text size

**Border & Radius:**
- `--input-border-width` - Border thickness
- `--input-border-radius` - Corner radius
- `--input-focus-ring-width` - Focus indicator width

**Shadow Tokens:**
- `--shadow-focus-primary` - Focus ring shadow
- `--shadow-focus-error` - Error focus ring

### Component-Specific Tokens

```css
/* Text Input */
--input-height: 40px;
--input-bg: var(--color-white);
--input-border-color: var(--color-border);
--input-border-color-focus: var(--color-primary);
--input-border-color-error: var(--color-error);
--input-text-color: var(--color-text-primary);
--input-padding-x: var(--spacing-md);
--input-padding-y: var(--spacing-sm);
--input-border-radius: var(--radius-md);

/* Select Dropdown */
--select-bg: var(--color-white);
--select-border-color: var(--color-border);
--select-arrow-color: var(--color-text-secondary);

/* Checkbox/Radio */
--checkbox-size: 20px;
--checkbox-bg: var(--color-white);
--checkbox-border-color: var(--color-border);
--checkbox-checked-bg: var(--color-primary);
--checkbox-checked-icon-color: var(--color-white);

/* Button (in forms) */
--button-bg-primary: var(--color-primary);
--button-text-primary: var(--color-white);
--button-padding-x: var(--spacing-lg);
--button-padding-y: var(--spacing-sm);
```

### Theme Support

- ✅ **Light Mode** - Default theme
- ✅ **Dark Mode** - Adjusted backgrounds, borders, text colors
- ✅ **High Contrast** - WCAG AAA compliant for accessibility
- ✅ **Custom Brand Themes** - Override tokens to match brand identity

### Example: Custom Form Theming

```css
/* Custom brand theme for forms */
:root[data-theme="custom-brand"] {
  /* Override input colors */
  --input-border-color-focus: #FF6B35;
  --button-bg-primary: #FF6B35;

  /* Adjust spacing for more generous layout */
  --form-field-gap: var(--spacing-lg);

  /* Rounded corners for softer appearance */
  --input-border-radius: var(--radius-lg);
}
```

### Accessibility via Tokens

- **High Contrast Mode**: Automatically uses high-contrast token values
- **Reduced Motion**: Respects `prefers-reduced-motion` for animations
- **Color Contrast**: All token combinations tested for WCAG AA compliance
- **Focus Indicators**: Visible focus rings defined by `--shadow-focus-*` tokens

---

## Skill Structure

### Recommended File Organization

```
forms/
├── SKILL.md
│   ├── Frontmatter (name, description)
│   ├── Quick Start (decision tree)
│   ├── Common Patterns (80% use cases)
│   └── References to detailed docs
│
├── references/
│   ├── input-types.md
│   │   ├── Text-based inputs catalog
│   │   ├── Selection components
│   │   ├── Date/time pickers
│   │   └── Specialized inputs
│   │
│   ├── validation-patterns.md
│   │   ├── Timing strategies
│   │   ├── Validation rules
│   │   ├── Async validation
│   │   └── Error message guidelines
│   │
│   ├── accessibility.md
│   │   ├── WCAG 2.1 checklist
│   │   ├── ARIA patterns
│   │   ├── Keyboard navigation
│   │   └── Screen reader testing
│   │
│   ├── multi-step-forms.md
│   │   ├── Wizard patterns
│   │   ├── Progress indicators
│   │   ├── State management
│   │   └── Save and resume
│   │
│   ├── ux-patterns.md
│   │   ├── Progressive disclosure
│   │   ├── Smart defaults
│   │   ├── Inline validation
│   │   └── Mobile considerations
│   │
│   └── examples.md
│       ├── Contact form
│       ├── Registration flow
│       ├── Checkout form
│       ├── Survey/questionnaire
│       └── Settings page
│
├── scripts/
│   ├── validate_schema.py      # Schema validation testing
│   ├── generate_form.py        # Form scaffolding from schema
│   └── accessibility_check.py  # ARIA and keyboard audit
│
└── assets/
    ├── templates/
    │   ├── basic-form.tsx
    │   ├── multi-step-wizard.tsx
    │   └── inline-edit-form.tsx
    └── schemas/
        ├── user-registration.json
        ├── contact-form.json
        └── checkout.json
```

---

### SKILL.md Frontmatter

```yaml
---
name: form-systems
description: Comprehensive form component library for data collection interfaces. Use when building contact forms, registration flows, checkout processes, surveys, settings pages, or any user input interface. Includes 50+ input types, validation strategies, accessibility patterns (WCAG 2.1), multi-step wizards, and UX best practices. Provides decision trees from data type to component selection, validation timing guidance, and error handling patterns. Triggered by requests to: create forms, collect user input, build surveys, implement validation, design multi-step workflows, or ensure form accessibility.
---
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- Create SKILL.md with decision tree
- Document Tier 1 components (basic inputs)
- Validation timing strategies
- Basic accessibility checklist
- 5-7 common examples

### Phase 2: Rich Components (Week 2)
- Tier 2 components (autocomplete, file upload, rich editors)
- Advanced validation patterns
- Cross-field validation
- Async validation with debouncing
- Mobile-specific patterns

### Phase 3: Complex Patterns (Week 3)
- Multi-step wizards
- Conditional fields
- Dynamic forms
- Autosave and recovery
- Inline editing patterns

### Phase 4: Polish & Examples (Week 4)
- Complete accessibility guide
- Error message library
- Real-world examples (10+)
- Performance optimization
- Testing strategies

---

## Success Metrics

**Skill Effectiveness:**
- Reduces form implementation time by 50%
- Zero accessibility violations (automated testing)
- Consistent validation UX across projects
- Clear guidance prevents common mistakes

**User Impact:**
- Form completion rates increase
- Validation errors decrease
- Mobile usability improves
- Accessibility compliance achieved

---

## Key Takeaways

1. **Forms are universal** - Every application needs them
2. **Decision trees are powerful** - Data type → Component is highly systematic
3. **Accessibility is non-negotiable** - WCAG compliance should be default
4. **Validation timing matters** - On-blur with progressive enhancement recommended
5. **Error messages need care** - Helpful, specific, actionable
6. **Mobile-first** - Touch targets, keyboards, single-column
7. **Progressive disclosure** - Don't overwhelm users
8. **Autosave when possible** - Prevent data loss

---

**END OF MASTER PLAN**

*This document serves as the foundation for building a comprehensive, AI-assisted component library for form systems. Reference this for implementation decisions, skill structure design, and ongoing development.*
