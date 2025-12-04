---
sidebar_position: 9
title: Providing Feedback
description: Feedback and notification systems including toasts, alerts, modals, and progress indicators
tags: [frontend, feedback, notifications, toasts, modals]
---

# Providing User Feedback and Notifications

Implements comprehensive feedback and notification systems that communicate system state, display messages, and handle user confirmations.

## When to Use

Use this skill when:
- Implementing toast notifications or snackbars
- Displaying success, error, warning, or info messages
- Creating modal dialogs or confirmation dialogs
- Implementing progress indicators (spinners, progress bars, skeleton screens)
- Designing empty states or zero-result displays
- Adding tooltips or contextual help
- Determining notification timing, stacking, or positioning
- Implementing accessible feedback patterns with ARIA
- Communicating any system state to users

## Feedback Type Decision Matrix

Choose the appropriate feedback mechanism based on urgency and attention requirements:

```
Critical + Blocking       → Modal Dialog
Important + Non-blocking  → Alert Banner
Success/Info + Temporary  → Toast/Snackbar
Contextual Help          → Tooltip/Popover
In-progress              → Progress Indicator
No Data                  → Empty State
```

### Quick Reference by Urgency

| Urgency Level | Component | Duration | Blocks Interaction |
|---------------|-----------|----------|-------------------|
| **Critical** | Modal Dialog | Until action | Yes |
| **Important** | Alert Banner | Until dismissed | No |
| **Standard** | Toast | 3-7 seconds | No |
| **Contextual** | Inline Message | Persistent | No |
| **Help** | Tooltip | On hover | No |
| **Progress** | Spinner/Bar | During operation | Optional |

## Implementation Approach

### Step 1: Determine Feedback Type

Assess the situation:
1. **Urgency**: How critical is the information?
2. **Duration**: How long should it persist?
3. **Action Required**: Does user need to respond?
4. **Context**: Is it related to specific UI element?

### Step 2: Choose Implementation Pattern

**For Toasts/Snackbars:**
- Position: Bottom-right (recommended)
- Duration: 3-4s (success), 5-7s (warning), 7-10s (error)
- Stack limit: 3-5 maximum

**For Modal Dialogs:**
- Focus management: Trap focus within modal
- Accessibility: ESC to close, proper ARIA labels
- Backdrop: Click outside to close (optional)

**For Progress Indicators:**
- &lt;100ms: No indicator needed
- 100ms-5s: Spinner with message
- 5s-30s: Progress bar (determinate if possible)
- >30s: Progress bar + time estimate + cancel

### Step 3: Implement with Recommended Libraries

**Modern React Stack (Recommended):**
```bash
npm install sonner @radix-ui/react-dialog
```

**For Toasts - Use Sonner:**
```tsx
import { Toaster, toast } from 'sonner';

// In your app root
&lt;Toaster position="bottom-right" />

// Trigger notifications
toast.success('Changes saved successfully');
toast.promise(saveData(), {
  loading: 'Saving...',
  success: 'Saved!',
  error: 'Failed to save'
});
```

**For Modals - Use Radix UI:**
```tsx
import * as Dialog from '@radix-ui/react-dialog';

&lt;Dialog.Root>
  &lt;Dialog.Trigger>Open&lt;/Dialog.Trigger>
  &lt;Dialog.Portal>
    &lt;Dialog.Overlay />
    &lt;Dialog.Content>
      &lt;Dialog.Title>Confirm Action&lt;/Dialog.Title>
      &lt;Dialog.Description>Are you sure?&lt;/Dialog.Description>
      &lt;Dialog.Close>Cancel&lt;/Dialog.Close>
    &lt;/Dialog.Content>
  &lt;/Dialog.Portal>
&lt;/Dialog.Root>
```

### Step 4: Apply Accessibility Patterns

**ARIA Live Regions for Announcements:**
```html
&lt;!-- For non-critical notifications -->
&lt;div role="status" aria-live="polite">
  File uploaded successfully
&lt;/div>

&lt;!-- For critical alerts -->
&lt;div role="alert" aria-live="assertive">
  Error: Failed to save
&lt;/div>
```

**Focus Management for Modals:**
1. Save current focus before opening
2. Move focus to first interactive element in modal
3. Trap focus within modal (Tab cycles)
4. Restore focus to trigger on close

## Notification Timing Guidelines

**Auto-dismiss durations:**
- Success: 3-4 seconds
- Info: 4-5 seconds
- Warning: 5-7 seconds
- Error: 7-10 seconds or manual dismiss
- With action button: 10+ seconds or no auto-dismiss

**Progress indicator thresholds:**
- &lt;100ms: No indicator
- 100ms-5s: Spinner
- 5s-30s: Progress bar
- >30s: Progress bar + cancel option

## Library Quick Comparison

| Library | Type | Size | Best For |
|---------|------|------|----------|
| **Sonner** | Toast | Small | Modern React 18+, accessibility |
| **react-hot-toast** | Toast | &lt;5KB | Minimal bundle size |
| **react-toastify** | Toast | ~16KB | RTL support, mobile |
| **Radix UI** | Modal | Small | Design systems, headless |
| **Headless UI** | Modal | Small | Tailwind projects |

## Cross-Skill Integration

This skill enhances all other component skills:

- **Forms**: Validation feedback, success confirmations
- **Data Visualization**: Loading states, error messages
- **Tables**: Bulk operation feedback, action confirmations
- **AI Chat**: Streaming indicators, rate limit warnings
- **Dashboards**: Widget loading, system status
- **Search/Filter**: Zero results, search progress
- **Media**: Upload progress, processing status

## Key Principles

1. **Match urgency to attention**: Don't use modals for non-critical info
2. **Be consistent**: Same feedback type for similar actions
3. **Provide context**: Explain what happened and what to do
4. **Enable recovery**: Include undo, retry, or help options
5. **Respect preferences**: Honor reduced motion settings
6. **Test accessibility**: Verify with screen readers and keyboard

## Related Skills

- [Theming Components](./theming-components.md) - Toast and modal styling
- [Building Forms](./building-forms.md) - Form validation feedback
- [Creating Dashboards](./creating-dashboards.md) - Dashboard loading states
- [Building AI Chat](./building-ai-chat.md) - AI response feedback

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/providing-feedback)
- Patterns: `references/toast-patterns.md`, `references/modal-patterns.md`
- Components: `references/progress-indicators.md`, `references/empty-states.md`
- Accessibility: `references/accessibility-feedback.md`
- Libraries: `references/library-comparison.md`
- Examples: `examples/success-toast.tsx`, `examples/confirmation-modal.tsx`
