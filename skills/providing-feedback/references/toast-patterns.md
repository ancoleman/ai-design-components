# Toast & Snackbar Implementation Patterns


## Table of Contents

- [Overview](#overview)
- [Positioning Strategies](#positioning-strategies)
  - [Bottom-Right (Recommended)](#bottom-right-recommended)
  - [Top-Center](#top-center)
  - [Top-Right](#top-right)
- [Stacking Behavior](#stacking-behavior)
  - [Queue Pattern](#queue-pattern)
  - [Stack Pattern (Max 5)](#stack-pattern-max-5)
  - [Replace Pattern](#replace-pattern)
- [Animation Patterns](#animation-patterns)
  - [Slide + Fade Enter](#slide-fade-enter)
  - [Slide + Fade Exit](#slide-fade-exit)
  - [Scale + Fade (Alternative)](#scale-fade-alternative)
- [Timing Strategies](#timing-strategies)
  - [Auto-dismiss Calculation](#auto-dismiss-calculation)
  - [Progressive Timing](#progressive-timing)
- [Toast Types & Styles](#toast-types-styles)
  - [Success Toast](#success-toast)
  - [Error Toast](#error-toast)
  - [Toast with Action](#toast-with-action)
- [Mobile Considerations](#mobile-considerations)
  - [Touch-Friendly Sizing](#touch-friendly-sizing)
  - [Swipe to Dismiss](#swipe-to-dismiss)
  - [Safe Area Positioning (iOS)](#safe-area-positioning-ios)
- [Implementation with Sonner](#implementation-with-sonner)
  - [Basic Setup](#basic-setup)
  - [Custom Toast Component](#custom-toast-component)
  - [Promise-Based Toasts](#promise-based-toasts)
- [Accessibility Patterns](#accessibility-patterns)
  - [ARIA Announcements](#aria-announcements)
  - [Keyboard Interactions](#keyboard-interactions)
- [Best Practices](#best-practices)

## Overview

Toasts (also called snackbars) are temporary notifications that appear at the edge of the screen to provide feedback without interrupting the user's workflow.

## Positioning Strategies

### Bottom-Right (Recommended)
```css
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: var(--z-index-toast, 9999);
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  margin-top: 12px; /* Space between stacked toasts */
}
```

**Advantages:**
- Doesn't cover navigation or header
- Natural reading flow
- Easy stacking behavior
- Mobile-friendly (thumb reach)

### Top-Center
```css
.toast-container {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: var(--z-index-toast, 9999);
}
```

**Use when:**
- Need high visibility
- Critical information
- Single toast at a time

### Top-Right
```css
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: var(--z-index-toast, 9999);
}
```

**Use when:**
- Consistency with existing patterns
- Right-to-left languages (mirror to top-left)

## Stacking Behavior

### Queue Pattern
```typescript
class ToastQueue {
  private queue: Toast[] = [];
  private current: Toast | null = null;

  add(toast: Toast) {
    this.queue.push(toast);
    if (!this.current) {
      this.showNext();
    }
  }

  private showNext() {
    if (this.queue.length === 0) {
      this.current = null;
      return;
    }

    this.current = this.queue.shift()!;
    this.display(this.current);

    setTimeout(() => {
      this.dismiss();
      this.showNext();
    }, this.current.duration);
  }
}
```

### Stack Pattern (Max 5)
```typescript
class ToastStack {
  private stack: Toast[] = [];
  private readonly MAX_VISIBLE = 5;

  add(toast: Toast) {
    this.stack.push(toast);

    if (this.stack.length > this.MAX_VISIBLE) {
      const oldest = this.stack.shift()!;
      this.dismiss(oldest);
    }

    this.render();
  }

  render() {
    this.stack.forEach((toast, index) => {
      toast.element.style.transform = `translateY(${index * -72}px)`;
      toast.element.style.opacity = index < 3 ? '1' : '0.7';
    });
  }
}
```

### Replace Pattern
```typescript
class ToastReplace {
  private current: Toast | null = null;
  private fadeTimeout: number | null = null;

  show(toast: Toast) {
    if (this.fadeTimeout) {
      clearTimeout(this.fadeTimeout);
    }

    if (this.current) {
      this.dismiss(this.current);
    }

    this.current = toast;
    this.display(toast);

    this.fadeTimeout = setTimeout(() => {
      this.dismiss(toast);
      this.current = null;
    }, toast.duration);
  }
}
```

## Animation Patterns

### Slide + Fade Enter
```css
@keyframes toast-enter {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast {
  animation: toast-enter var(--toast-enter-duration, 300ms) ease-out;
}
```

### Slide + Fade Exit
```css
@keyframes toast-exit {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

.toast.dismissing {
  animation: toast-exit var(--toast-exit-duration, 200ms) ease-in;
}
```

### Scale + Fade (Alternative)
```css
@keyframes toast-scale-enter {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
```

## Timing Strategies

### Auto-dismiss Calculation
```javascript
function calculateDuration(toast) {
  const baseDuration = {
    success: 3000,
    info: 4000,
    warning: 5000,
    error: 7000
  };

  let duration = baseDuration[toast.type] || 4000;

  // Adjust for content length
  const wordCount = toast.message.split(' ').length;
  const readingTime = wordCount * 200; // 200ms per word
  duration = Math.max(duration, readingTime);

  // Never auto-dismiss if action present
  if (toast.action) {
    duration = Infinity;
  }

  // Cap maximum duration
  return Math.min(duration, 10000);
}
```

### Progressive Timing
```javascript
function getProgressiveDuration(toastCount) {
  const base = 3000;

  // Increase duration when multiple toasts
  if (toastCount === 1) return base;
  if (toastCount === 2) return base + 1000;
  if (toastCount >= 3) return base + 2000;
}
```

## Toast Types & Styles

### Success Toast
```typescript
interface SuccessToast {
  type: 'success';
  message: string;
  icon: '✓' | '✅' | CheckIcon;
  duration: 3000 | 4000;
  style: {
    background: 'var(--color-success-bg)',
    color: 'var(--color-success-text)',
    borderLeft: '4px solid var(--color-success)'
  };
}
```

### Error Toast
```typescript
interface ErrorToast {
  type: 'error';
  message: string;
  icon: '✕' | '⚠️' | ErrorIcon;
  duration: 7000 | Infinity;
  dismissible: true;
  style: {
    background: 'var(--color-error-bg)',
    color: 'var(--color-error-text)',
    borderLeft: '4px solid var(--color-error)'
  };
}
```

### Toast with Action
```typescript
interface ActionToast {
  message: string;
  action: {
    label: string;
    onClick: () => void;
  };
  duration: Infinity; // Never auto-dismiss
  dismissible: true;
}

// Example usage
toast({
  message: 'Item deleted',
  action: {
    label: 'Undo',
    onClick: () => restoreItem()
  }
});
```

## Mobile Considerations

### Touch-Friendly Sizing
```css
.toast {
  min-height: 48px; /* Touch target minimum */
  padding: 12px 16px;
  font-size: 16px; /* Prevent zoom on iOS */
}

.toast-close {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Swipe to Dismiss
```javascript
class SwipeableToast {
  constructor(element) {
    let startX = 0;
    let currentX = 0;

    element.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
    });

    element.addEventListener('touchmove', (e) => {
      currentX = e.touches[0].clientX;
      const diff = currentX - startX;

      if (diff > 0) {
        element.style.transform = `translateX(${diff}px)`;
        element.style.opacity = 1 - (diff / 200);
      }
    });

    element.addEventListener('touchend', (e) => {
      const diff = currentX - startX;

      if (diff > 100) {
        this.dismiss();
      } else {
        element.style.transform = 'translateX(0)';
        element.style.opacity = '1';
      }
    });
  }
}
```

### Safe Area Positioning (iOS)
```css
.toast-container {
  bottom: 24px;
  bottom: calc(24px + env(safe-area-inset-bottom));
  right: 24px;
  right: calc(24px + env(safe-area-inset-right));
}
```

## Implementation with Sonner

### Basic Setup
```tsx
import { Toaster, toast } from 'sonner';

function App() {
  return (
    <>
      <Toaster
        position="bottom-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'var(--toast-bg)',
            color: 'var(--toast-text)',
            border: '1px solid var(--toast-border)'
          }
        }}
      />
      {/* Your app */}
    </>
  );
}
```

### Custom Toast Component
```tsx
import { toast } from 'sonner';

function CustomToast({ title, description, type }) {
  return (
    <div className={`custom-toast toast-${type}`}>
      <div className="toast-icon">
        {type === 'success' && <CheckIcon />}
        {type === 'error' && <ErrorIcon />}
      </div>
      <div className="toast-content">
        <h4>{title}</h4>
        <p>{description}</p>
      </div>
    </div>
  );
}

// Usage
toast.custom((t) => (
  <CustomToast
    title="Upload Complete"
    description="Your file has been uploaded"
    type="success"
  />
));
```

### Promise-Based Toasts
```tsx
const uploadFile = async (file) => {
  const response = await fetch('/upload', {
    method: 'POST',
    body: file
  });

  if (!response.ok) throw new Error('Upload failed');
  return response.json();
};

function UploadButton() {
  const handleUpload = () => {
    toast.promise(uploadFile(file), {
      loading: 'Uploading file...',
      success: (data) => `${data.filename} uploaded successfully`,
      error: (err) => `Upload failed: ${err.message}`
    });
  };

  return <button onClick={handleUpload}>Upload</button>;
}
```

## Accessibility Patterns

### ARIA Announcements
```html
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
  className="sr-only"
>
  {toastMessage}
</div>
```

### Keyboard Interactions
```javascript
class AccessibleToast {
  constructor(element) {
    // ESC to dismiss
    element.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.dismiss();
      }
    });

    // Tab trap when action present
    if (this.hasAction) {
      this.trapFocus(element);
    }
  }

  trapFocus(element) {
    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable.focus();
        } else if (!e.shiftKey && document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable.focus();
        }
      }
    });
  }
}
```

## Best Practices

1. **Consistent positioning**: Pick one position and stick with it
2. **Clear hierarchy**: Use color and icons to indicate type
3. **Readable duration**: Ensure enough time to read
4. **Action clarity**: Make action buttons obvious
5. **Dismissible errors**: Always allow manual dismissal for errors
6. **Mobile testing**: Test swipe gestures and touch targets
7. **Accessibility**: Test with screen readers
8. **Performance**: Limit concurrent toasts to prevent overflow
9. **Context**: Keep messages concise and actionable
10. **Feedback timing**: Show immediately after user action