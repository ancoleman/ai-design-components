# AI-Assisted Component Library: Feedback & Notification Systems
## Master Plan for User Feedback Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025
**Purpose:** Systematic guidance for implementing toasts, alerts, modals, progress indicators, empty states, and user communication patterns

---

## Executive Summary

User feedback components communicate system state, errors, success, and important information. Poor feedback UX is a common source of frustration. This skill provides clear decision frameworks for choosing appropriate feedback mechanisms and implementing them accessibly.

**Core Question:** What level of user attention is required?

```
Critical + Blocking → Modal Dialog
Important + Non-blocking → Alert Banner
Success/Info + Temporary → Toast/Snackbar
Contextual Help → Tooltip/Popover
In-progress → Progress Indicator
No Data → Empty State
```

---

## Component Taxonomy

### Tier 1: Alerts & Notifications

**Toast/Snackbar**
- Temporary message (3-7 seconds)
- Bottom or top corner
- Non-blocking
- Auto-dismiss or manual close
- Stack multiple toasts
- **Use for:** Success confirmations, info updates, minor errors

**Alert Banner**
- Persistent until dismissed
- Top of page or section
- Prominent but non-blocking
- Color-coded (info, success, warning, error)
- Optional action button
- **Use for:** Important announcements, warnings, persistent errors

**Modal Dialog**
- Blocks interaction with rest of page
- Center of screen
- Requires user action (confirm, cancel, close)
- Focus trap
- **Use for:** Critical decisions, errors requiring action, confirmations

**Inline Message**
- Within content/form
- Field-level or section-level
- Contextual to specific element
- **Use for:** Form validation, field-specific help

---

### Tier 2: Progress & Loading

**Spinner**
- Indeterminate progress
- Unknown duration
- Simple animation
- **Use for:** Quick operations (<5s expected)

**Progress Bar**
- Determinate progress (0-100%)
- Shows completion percentage
- Optional time estimate
- **Use for:** File uploads, long operations, multi-step processes

**Skeleton Screen**
- Placeholder matching final layout
- Pulsing/shimmering animation
- Better UX than spinner
- **Use for:** Initial page load, content loading

**Linear Progress (Top Bar)**
- Thin bar at top of page
- Indeterminate or determinate
- Non-intrusive
- **Use for:** Page transitions, background operations

---

### Tier 3: Contextual Feedback

**Tooltip**
- Small popup on hover/focus
- Brief help text
- Non-blocking
- Auto-position to stay in viewport
- **Use for:** Icon labels, brief explanations

**Popover**
- Larger than tooltip
- Can contain rich content
- Click to open, click/ESC to close
- Arrow pointing to trigger
- **Use for:** Contextual help, additional options, forms

**Empty State**
- No data to display
- Illustration + message + action
- Encourage user action
- **Use for:** First use, zero results, cleared list

**Error State**
- Operation failed
- Explain what happened
- Suggest solution
- Retry button
- **Use for:** Failed API calls, broken components

---

## Decision Framework

### Notification Level Matrix

| Scenario | Component | Duration | Blocking |
|----------|-----------|----------|----------|
| Item saved successfully | Toast | 3-5s | No |
| Item deleted (undo option) | Toast + Action | 7-10s | No |
| Form has errors | Inline Messages | Persistent | No |
| Internet disconnected | Alert Banner | Until fixed | No |
| Confirm delete operation | Modal Dialog | Until action | Yes |
| Background task running | Progress Bar | Until complete | No |
| Loading page content | Skeleton Screen | Until loaded | No |
| Uploading file | Progress Bar | Until complete | No |
| Quick API call | Spinner (small) | <5s | Maybe |
| What does this icon mean? | Tooltip | On hover | No |

---

## Toast/Snackbar Patterns

### Positioning

**Bottom Right (Recommended):**
- Doesn't cover important content
- Natural reading flow
- Stack vertically

**Top Center:**
- More noticeable
- Good for critical info
- Can block navigation

**Top Right:**
- Common pattern
- Less intrusive than center
- Can stack

### Timing

**Auto-Dismiss Guidelines:**
- Success: 3-4 seconds
- Info: 4-5 seconds
- Warning: 5-7 seconds
- Error: 7-10 seconds (or manual dismiss only)
- With action button: No auto-dismiss or 10+ seconds

### Stacking Behavior

**Option 1: Queue**
- Show one at a time
- Next appears after dismiss
- Prevents clutter

**Option 2: Stack**
- Multiple visible simultaneously
- Limit to 3-5 max
- Oldest auto-dismisses first

**Option 3: Replace**
- New toast replaces old
- Only one visible
- Simple but can miss messages

---

## Modal Dialog Best Practices

### Anatomy

```
┌─────────────────────────────────┐
│ [X]                             │ ← Close button
│                                 │
│  Confirm Deletion               │ ← Title
│                                 │
│  Are you sure you want to       │ ← Message
│  delete "Report.pdf"? This      │
│  action cannot be undone.       │
│                                 │
│  [Cancel]  [Delete]             │ ← Actions
└─────────────────────────────────┘
```

### Accessibility

- **Focus trap**: Tab cycles within modal
- **Focus management**: Focus first interactive element on open
- **ESC to close**: Always (unless critical warning)
- **Click backdrop**: Close on click outside (optional)
- **ARIA**: `role="dialog"`, `aria-labelledby`, `aria-describedby`
- **Screen reader**: Announce modal opened

### Sizing

- **Small**: Simple confirmations (400px)
- **Medium**: Forms, content (600px)
- **Large**: Complex forms, images (800px)
- **Full screen**: Mobile, very complex content

---

## Progress Indicators

### When to Show

**Immediate (<100ms):** No indicator needed
**Quick (100ms-1s):** Small spinner
**Moderate (1-5s):** Spinner + "Loading..." text
**Long (5s-30s):** Progress bar (determinate if possible)
**Very Long (>30s):** Progress bar + time estimate + cancel option

### Determinate vs Indeterminate

**Determinate (0-100%):**
```javascript
<ProgressBar value={progress} max={100} />
// Show percentage: 45%
// Show estimate: About 2 minutes remaining
```

**Indeterminate (unknown):**
```javascript
<Spinner />
// Show message: Processing...
// Show elapsed time if >10s: Processing... (15 seconds)
```

---

## Empty State Design

### Effective Empty States

**Elements:**
1. **Illustration**: Simple, relevant, friendly
2. **Headline**: Clear, concise explanation
3. **Body text**: Why it's empty, what user can do
4. **Call-to-action**: Primary action to populate
5. **Optional**: Secondary actions, help links

**Example:**
```
┌─────────────────────────────────┐
│                                 │
│         [illustration]          │ ← Empty folder icon
│                                 │
│   No projects yet               │ ← Headline
│                                 │
│   Create your first project     │ ← Body
│   to get started                │
│                                 │
│   [+ New Project]               │ ← CTA
│                                 │
│   Import existing project       │ ← Secondary
└─────────────────────────────────┘
```

### Types of Empty States

**First Use:** User hasn't created anything yet
**Zero Results:** Search/filter returned nothing
**Cleared:** User deleted all items
**Error State:** Failed to load data
**Permission Denied:** User lacks access

---

## Accessibility Requirements

### ARIA Live Regions

```html
<!-- For toast notifications -->
<div role="status" aria-live="polite" aria-atomic="true">
  File uploaded successfully
</div>

<!-- For errors -->
<div role="alert" aria-live="assertive" aria-atomic="true">
  Error: Failed to save changes
</div>
```

**aria-live values:**
- `off`: Not announced (default)
- `polite`: Announced when user pauses
- `assertive`: Announced immediately (use sparingly)

### Focus Management

**Modal opens:**
1. Save current focus
2. Move focus to modal (first interactive element)
3. Trap focus within modal
4. On close, restore focus to trigger element

**Toast appears:**
- Don't steal focus
- Use aria-live for announcement
- Keep focus on current task

---

## Skill Structure

```yaml
---
name: feedback-notifications
description: Comprehensive component library for user feedback and notification systems. Use when communicating system state, displaying alerts, showing progress, handling errors, or providing contextual help. Covers toasts/snackbars, alert banners, modal dialogs, inline messages, progress indicators (spinners, progress bars, skeletons), tooltips, popovers, empty states, and error states. Includes decision frameworks for choosing appropriate feedback mechanisms, timing strategies, accessibility patterns (ARIA live regions, focus management), and UX best practices. Triggered by requests to: show notifications, display alerts, create modals, implement progress indicators, design empty states, or handle user feedback.
---
```

```
feedback/
├── SKILL.md
├── references/
│   ├── toasts-snackbars.md
│   ├── alert-banners.md
│   ├── modal-dialogs.md
│   ├── progress-indicators.md
│   ├── empty-states.md
│   ├── tooltips-popovers.md
│   └── accessibility-feedback.md
├── examples/
│   ├── toast-system.tsx
│   ├── modal-examples.tsx
│   ├── progress-examples.tsx
│   └── empty-state-gallery.tsx
└── assets/
    └── empty-state-illustrations/
```

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate these library recommendations using available research tools (Google Search Grounding, Context7). This ensures you're using the latest, most secure versions.

**Note:** The recommendations below were researched comprehensively in November 2025 and are production-ready. Validation is optional.

---

## Recommended Libraries & Tools

### Toast/Notification Libraries (2025)

#### **Primary: Sonner** (Modern, Lightweight, Accessible)

**Library:** `/emilkowalski/sonner`
**Trust Score:** 7.6/10
**Code Snippets:** 67+

**Why Sonner?**
- **Modern**: Built for React 18+, latest patterns
- **Zero Dependencies**: Completely standalone
- **Lightweight**: Small bundle size
- **Accessible**: Built-in ARIA, keyboard nav, screen reader support
- **Beautiful**: Smooth animations, polished design
- **Promise API**: Built-in loading/success/error states
- **Headless Mode**: Unstyled for custom designs

**When to Use:**
- Modern React projects (18+)
- Want beautiful toasts out-of-box
- Using shadcn/ui
- Accessibility is priority
- Need promise-based toasts

**Installation:**
```bash
npm install sonner
```

**Basic Usage:**
```tsx
import { Toaster, toast } from 'sonner';

function App() {
  return (
    <div>
      <Toaster position="bottom-right" />
      <button onClick={() => toast('Event created successfully')}>
        Create Event
      </button>
    </div>
  );
}
```

**Promise-Based Toast:**
```tsx
import { toast } from 'sonner';

function UploadButton() {
  const handleUpload = async () => {
    toast.promise(uploadFile(), {
      loading: 'Uploading...',
      success: (data) => `${data.name} uploaded`,
      error: 'Upload failed',
    });
  };

  return <button onClick={handleUpload}>Upload</button>;
}
```

**With Action Button:**
```tsx
toast('Event created', {
  action: {
    label: 'Undo',
    onClick: () => console.log('Undo'),
  },
});
```

---

#### **Alternative: react-hot-toast** (Lightweight Champion)

**Library:** `/timolins/react-hot-toast`
**Trust Score:** 9.5/10
**Code Snippets:** 48+

**Why react-hot-toast?**
- **Ultra-Lightweight**: <5KB gzipped (including styles!)
- **Simple API**: Easy to learn and use
- **Customizable**: Full control over appearance
- **Accessible**: ARIA support built-in
- **Promise API**: Loading states handled
- **Headless Mode**: Build your own toast UI

**When to Use:**
- Bundle size is critical
- Need simple, straightforward toasts
- Want full customization
- Minimalist approach preferred

**Installation:**
```bash
npm install react-hot-toast
```

**Basic Usage:**
```tsx
import toast, { Toaster } from 'react-hot-toast';

function App() {
  return (
    <div>
      <Toaster />
      <button onClick={() => toast.success('Saved successfully!')}>
        Save
      </button>
    </div>
  );
}
```

**Custom Styling:**
```tsx
toast.success('Saved!', {
  style: {
    border: '1px solid #10b981',
    padding: '16px',
    color: '#10b981',
  },
  icon: '✅',
});
```

---

#### **Alternative: react-toastify** (Feature-Rich)

**Library:** `/fkhadra/react-toastify`
**Trust Score:** 10/10
**Code Snippets:** 4+

**Why react-toastify?**
- **Mature**: Battle-tested, widely adopted
- **Feature-Complete**: Everything built-in
- **RTL Support**: International apps
- **Swipe-to-Dismiss**: Mobile-friendly
- **Extensive Customization**: Many options

**When to Use:**
- Need every feature
- RTL language support required
- Mobile apps (swipe gestures)
- Team familiar with it

**Trade-offs:**
- Larger bundle (~16KB)
- More complex API
- Potentially overkill for simple use cases

**Installation:**
```bash
npm install react-toastify
```

---

### Modal/Dialog Libraries

#### **Primary: Radix UI Dialog** (Headless, Accessible)

**Library:** `/radix-ui/primitives`
**Trust Score:** 8.7/10
**Code Snippets:** 4+ (core primitives)

**Why Radix UI?**
- **Headless**: Complete styling control
- **Accessible**: WAI-ARIA compliant
- **Focus Management**: Auto focus, focus trap
- **Keyboard**: ESC to close, Tab navigation
- **Portal**: Renders outside DOM tree
- **Composable**: Build complex dialogs easily

**When to Use:**
- Want complete styling control
- Building design system
- Accessibility is critical
- Need composable primitives

**Installation:**
```bash
npm install @radix-ui/react-dialog
```

**Example:**
```tsx
import * as Dialog from '@radix-ui/react-dialog';

function MyDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button>Open Dialog</button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content">
          <Dialog.Title>Confirm Action</Dialog.Title>
          <Dialog.Description>
            Are you sure you want to proceed?
          </Dialog.Description>

          <div>
            <Dialog.Close asChild>
              <button>Cancel</button>
            </Dialog.Close>
            <button>Confirm</button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

#### **Alternative: Headless UI Dialog** (Tailwind-Friendly)

**Library:** `/tailwindlabs/headlessui`
**Trust Score:** 8/10
**Code Snippets:** 455+

**Why Headless UI?**
- **Designed for Tailwind**: Perfect integration
- **Accessible**: Full WAI-ARIA support
- **Focus Management**: Built-in
- **Portal**: Auto background inert
- **Official**: Made by Tailwind team

**When to Use:**
- Using Tailwind CSS
- Want official Tailwind components
- Need accessible modals quickly

**Installation:**
```bash
npm install @headlessui/react
```

**Example:**
```tsx
import { Dialog } from '@headlessui/react';
import { useState } from 'react';

function MyDialog() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open</button>

      <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Dialog.Panel className="bg-white rounded p-6">
            <Dialog.Title>Confirm</Dialog.Title>
            <Dialog.Description>
              Are you sure?
            </Dialog.Description>

            <button onClick={() => setIsOpen(false)}>Cancel</button>
            <button onClick={() => setIsOpen(false)}>Confirm</button>
          </Dialog.Panel>
        </div>
      </Dialog>
    </>
  );
}
```

---

### Library Comparison Matrix

| Library | Type | Size | Accessibility | Customization | Best For |
|---------|------|------|---------------|---------------|----------|
| **Sonner** | Toast | Small | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Modern React 18+ |
| **react-hot-toast** | Toast | <5KB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Minimal bundle |
| **react-toastify** | Toast | ~16KB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Feature-rich |
| **Radix UI Dialog** | Modal | Small | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Design systems |
| **Headless UI Dialog** | Modal | Small | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Tailwind projects |

---

### Recommendations by Use Case

**Modern React App → Sonner**
- Beautiful by default
- Excellent accessibility
- Zero dependencies
- Promise API

**Minimal Bundle Size → react-hot-toast**
- <5KB total
- Simple API
- Highly customizable

**RTL/International → react-toastify**
- RTL support built-in
- Mature and stable
- Mobile gestures

**Design System Modals → Radix UI**
- Complete control
- Headless architecture
- Composable primitives

**Tailwind Modals → Headless UI**
- Official Tailwind library
- Great integration
- Accessible by default

---

### Implementation Recommendations

**Recommended Stack (Modern):**
```bash
npm install sonner @radix-ui/react-dialog
```
- Sonner for toasts
- Radix UI for modals
- Both headless/flexible
- Excellent accessibility

**Recommended Stack (Tailwind):**
```bash
npm install react-hot-toast @headlessui/react
```
- react-hot-toast (minimal)
- Headless UI (Tailwind-designed)
- Perfect for Tailwind projects

**Recommended Stack (Feature-Rich):**
```bash
npm install react-toastify react-modal
```
- Everything built-in
- Less customization work
- Mature libraries

---

## Styling & Theming

### Design Token Integration

All feedback and notification components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--toast-bg` - Toast/snackbar background
- `--toast-text` - Toast text color
- `--alert-success-bg` - Success alert background
- `--alert-warning-bg` - Warning alert background
- `--alert-error-bg` - Error alert background
- `--alert-info-bg` - Info alert background
- `--modal-backdrop-bg` - Modal overlay background
- `--modal-bg` - Modal dialog background
- `--tooltip-bg` - Tooltip background
- `--tooltip-text` - Tooltip text color

**Spacing Tokens:**
- `--toast-padding` - Toast internal padding
- `--modal-padding` - Modal internal padding
- `--alert-padding` - Alert banner padding
- `--tooltip-padding` - Tooltip padding

**Typography Tokens:**
- `--toast-font-size` - Toast text size
- `--modal-title-font-size` - Modal title size
- `--alert-font-size` - Alert message size

**Border & Radius:**
- `--toast-border-radius` - Toast corner radius
- `--modal-border-radius` - Modal corner radius
- `--alert-border-radius` - Alert corner radius

**Shadow Tokens:**
- `--toast-shadow` - Toast elevation
- `--modal-shadow` - Modal elevation
- `--tooltip-shadow` - Tooltip shadow

**Motion Tokens:**
- `--toast-enter-duration` - Toast slide-in animation
- `--modal-enter-duration` - Modal fade-in animation

### Component-Specific Tokens

```css
/* Toasts/Snackbars */
--toast-bg: var(--color-gray-900);
--toast-text: var(--color-white);
--toast-padding: var(--spacing-md);
--toast-border-radius: var(--radius-md);
--toast-shadow: var(--shadow-xl);
--toast-enter-duration: var(--duration-normal);

/* Alerts */
--alert-success-bg: var(--color-success-bg);
--alert-warning-bg: var(--color-warning-bg);
--alert-error-bg: var(--color-error-bg);
--alert-info-bg: var(--color-info-bg);
--alert-padding: var(--spacing-md);
--alert-border-radius: var(--radius-md);

/* Modals */
--modal-backdrop-bg: rgba(0, 0, 0, 0.5);
--modal-bg: var(--color-white);
--modal-padding: var(--spacing-xl);
--modal-border-radius: var(--radius-lg);
--modal-shadow: var(--shadow-2xl);

/* Tooltips */
--tooltip-bg: var(--color-gray-900);
--tooltip-text: var(--color-white);
--tooltip-padding: var(--spacing-sm);
--tooltip-border-radius: var(--radius-sm);
--tooltip-shadow: var(--shadow-md);
```

### Theme Support

- ✅ **Light Mode** - Subtle, non-intrusive notifications
- ✅ **Dark Mode** - Adjusted contrast for visibility
- ✅ **High Contrast** - Strong visibility for critical alerts
- ✅ **Custom Brand Themes** - Match notification style to brand

### Accessibility via Tokens

- **High Contrast Mode**: Enhanced visibility for critical messages
- **Reduced Motion**: Disable slide/fade animations
- **ARIA Live Regions**: Tokens support screenreader announcements
- **Color Independence**: Icons + text, not color alone

---

**END OF MASTER PLAN**
