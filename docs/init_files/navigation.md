# AI-Assisted Component Library: Navigation Patterns
## Master Plan for Navigation Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025

---

## Executive Summary

Navigation defines application structure and user wayfinding. This skill provides systematic guidance for selecting and implementing navigation patterns based on information architecture, user mental models, and device constraints.

---

## Component Taxonomy

### Primary Navigation

**Top Navigation (Horizontal)**
- Logo + menu items in header
- 5-7 primary links max
- Dropdowns for sub-navigation
- **Best for:** Shallow hierarchy, content sites, marketing pages

**Side Navigation (Vertical)**
- Fixed or collapsible sidebar
- Multi-level nested menus
- Expandable sections
- **Best for:** Deep hierarchy, apps, admin panels

**Mega Menu**
- Large dropdown panels
- Multi-column layouts
- Rich content (images, descriptions)
- **Best for:** E-commerce, content-heavy sites

---

### Secondary Navigation

**Breadcrumbs**
- Hierarchical path: Home > Category > Product
- Each level clickable
- Shows current location
- **Best for:** Deep sites, e-commerce, documentation

**Tabs**
- Horizontal navigation between views
- Content switching without page reload
- Active state indicator
- **Best for:** Section navigation, settings pages, profiles

**Pagination**
- Numbered pages: 1, 2, 3...
- Previous/Next buttons
- **Best for:** Search results, articles, product lists

---

### Specialized Navigation

**Command Palette (Cmd+K)**
- Keyboard-driven search
- Action launcher
- Quick navigation
- **Best for:** Power users, complex apps

**Stepper/Wizard**
- Linear multi-step process
- Progress indicator
- Next/Previous navigation
- **Best for:** Onboarding, checkout, complex forms

**Table of Contents**
- Page sections list
- Anchor links
- Scrollspy highlighting
- **Best for:** Long articles, documentation

---

## Decision Framework

```
Information Architecture → Navigation Pattern

Flat (1-2 levels) → Top Navigation
Deep (3+ levels) → Side Navigation
E-commerce/Large → Mega Menu
Linear Process → Stepper/Wizard
Long Content → Table of Contents
Power Users → Command Palette
Multi-section Page → Tabs
```

---

## Mobile Navigation Patterns

### Hamburger Menu
- Icon opens slide-out drawer
- Hides navigation on mobile
- Controversial but common
- **Cons:** Hidden, extra tap

### Bottom Navigation
- 3-5 primary actions
- Always visible
- Thumb-friendly
- **Best for:** Mobile apps, simple hierarchies

### Tab Bar
- Horizontal scrollable tabs
- Swipe between sections
- Natural on mobile
- **Best for:** Mobile-first apps

---

## Accessibility Requirements

**Keyboard Navigation:**
- Tab through all links
- Enter/Space activates
- Arrow keys for menus
- ESC closes dropdowns

**ARIA Patterns:**
```html
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none">
      <a role="menuitem" href="/home">Home</a>
    </li>
  </ul>
</nav>
```

**Screen Readers:**
- Skip navigation link
- Landmark roles (`<nav>`)
- Current page indicator (`aria-current="page"`)

---

## Skill Structure

```yaml
---
name: navigation-patterns
description: Component library for navigation systems and wayfinding. Covers top navigation, side navigation, mega menus, breadcrumbs, tabs, pagination, command palettes, steppers, and table of contents. Includes decision frameworks based on information architecture, mobile navigation patterns, accessibility requirements (keyboard nav, ARIA, screen readers), and responsive design strategies.
---
```

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate these library recommendations using available research tools (Google Search Grounding, Context7).

---

## Recommended Libraries & Tools

### **Primary: React Router** (Industry Standard)

**Library:** `/remix-run/react-router`
**Trust Score:** 7.5/10
**Code Snippets:** 892+

**Why React Router?**
- Industry standard for React navigation
- Type-safe routing
- Nested routes, lazy loading
- SSR support
- Accessibility built-in (`<NavLink>` active states)

**Installation:**
```bash
npm install react-router
```

**Alternative: TanStack Router** (Type-Safe)
- 100% TypeScript inference
- Built-in caching
- Search param APIs

**For Native CSS:**
- Use semantic `<nav>`, `<ul>`, `<li>` with ARIA
- No library needed for simple navigation

---

## Styling & Theming

### Design Token Integration

All navigation components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--nav-bg` - Navigation background
- `--nav-border-color` - Navigation borders
- `--nav-item-color` - Navigation link text
- `--nav-item-hover-bg` - Link hover background
- `--nav-item-hover-color` - Link hover text
- `--nav-item-active-bg` - Active link background
- `--nav-item-active-color` - Active link text
- `--breadcrumb-separator-color` - Breadcrumb divider color
- `--tab-border-color` - Tab underline/border

**Spacing Tokens:**
- `--nav-padding` - Navigation container padding
- `--nav-item-padding` - Individual nav item padding
- `--nav-item-gap` - Space between nav items
- `--breadcrumb-gap` - Space between breadcrumb items

**Typography Tokens:**
- `--nav-font-size` - Navigation text size
- `--nav-font-weight` - Navigation text weight
- `--nav-item-font-weight-active` - Active item weight

**Border & Radius:**
- `--nav-border-radius` - Navigation corner radius
- `--nav-item-border-radius` - Nav item corner radius

**Shadow Tokens:**
- `--nav-shadow` - Navigation shadow (for sticky/fixed)

### Component-Specific Tokens

```css
/* Top Navigation */
--nav-bg: var(--color-white);
--nav-border-color: var(--color-border);
--nav-item-color: var(--color-text-primary);
--nav-item-hover-bg: var(--color-gray-100);
--nav-item-active-bg: var(--color-primary-50);
--nav-item-active-color: var(--color-primary);
--nav-padding: var(--spacing-md);
--nav-item-padding: var(--spacing-sm) var(--spacing-md);
--nav-shadow: var(--shadow-sm);

/* Breadcrumbs */
--breadcrumb-separator-color: var(--color-text-tertiary);
--breadcrumb-gap: var(--spacing-xs);

/* Tabs */
--tab-border-color: var(--color-border);
--tab-active-border-color: var(--color-primary);
--tab-hover-bg: var(--color-gray-50);
```

### Theme Support

- ✅ **Light Mode** - Clean, clear navigation
- ✅ **Dark Mode** - Adjusted contrast for visibility
- ✅ **High Contrast** - Strong text/background contrast
- ✅ **Custom Brand Themes** - Match navigation to brand colors

### Accessibility via Tokens

- **High Contrast Mode**: Strong link visibility
- **Focus Indicators**: Clear focus states for keyboard navigation
- **Current Page**: Distinct active state with aria-current support
- **Screen Readers**: Token-based styling supports ARIA landmarks

---

**END OF MASTER PLAN**
