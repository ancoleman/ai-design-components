# Modal Dialog Implementation Patterns


## Table of Contents

- [Overview](#overview)
- [Modal Types & Use Cases](#modal-types-use-cases)
  - [Confirmation Modal](#confirmation-modal)
  - [Form Modal](#form-modal)
  - [Information Modal](#information-modal)
  - [Media Modal](#media-modal)
- [Modal Anatomy](#modal-anatomy)
  - [Standard Structure](#standard-structure)
  - [Modal Sizes](#modal-sizes)
- [Focus Management](#focus-management)
  - [Focus Trap Implementation](#focus-trap-implementation)
  - [React Hook for Focus Management](#react-hook-for-focus-management)
- [Animation Patterns](#animation-patterns)
  - [Fade + Scale Entry](#fade-scale-entry)
  - [Slide Up (Mobile)](#slide-up-mobile)
- [Scroll Management](#scroll-management)
  - [Body Scroll Lock](#body-scroll-lock)
  - [Scrollable Modal Content](#scrollable-modal-content)
- [Radix UI Implementation](#radix-ui-implementation)
  - [Basic Modal with Radix](#basic-modal-with-radix)
  - [Controlled Modal](#controlled-modal)
- [Headless UI Implementation](#headless-ui-implementation)
  - [Basic Modal with Headless UI](#basic-modal-with-headless-ui)
- [Nested Modals](#nested-modals)
  - [Stack Management](#stack-management)
- [Accessibility Patterns](#accessibility-patterns)
  - [ARIA Attributes](#aria-attributes)
  - [Screen Reader Announcements](#screen-reader-announcements)
  - [Keyboard Shortcuts](#keyboard-shortcuts)
- [Best Practices](#best-practices)

## Overview

Modal dialogs are overlays that require user interaction before returning to the main application. They create a focused experience by blocking interaction with the rest of the page.

## Modal Types & Use Cases

### Confirmation Modal
```tsx
interface ConfirmationModal {
  type: 'confirmation';
  title: string;
  message: string;
  confirmText: string;
  cancelText: string;
  destructive?: boolean; // Red confirm button for dangerous actions
  onConfirm: () => void | Promise<void>;
  onCancel: () => void;
}
```

**Use cases:**
- Delete confirmation
- Unsaved changes warning
- Logout confirmation
- Irreversible actions

### Form Modal
```tsx
interface FormModal {
  type: 'form';
  title: string;
  size: 'small' | 'medium' | 'large';
  submitText: string;
  cancelText: string;
  onSubmit: (data: FormData) => void | Promise<void>;
  validateOnSubmit?: boolean;
}
```

**Use cases:**
- Quick edits
- Create new items
- Settings/preferences
- Login/signup

### Information Modal
```tsx
interface InfoModal {
  type: 'info';
  title: string;
  content: React.ReactNode;
  size?: 'small' | 'medium' | 'large';
  dismissText: string;
  actions?: Action[];
}
```

**Use cases:**
- Help content
- Terms & conditions
- Feature announcements
- Detailed information

### Media Modal
```tsx
interface MediaModal {
  type: 'media';
  title?: string;
  media: {
    type: 'image' | 'video' | 'iframe';
    src: string;
    alt?: string;
  };
  size: 'auto' | 'fullscreen';
  showControls: boolean;
}
```

**Use cases:**
- Image galleries
- Video players
- Document viewers
- Maps/embeds

## Modal Anatomy

### Standard Structure
```tsx
function Modal({ isOpen, onClose, title, children, size = 'medium' }) {
  return (
    <div className={`modal-root ${isOpen ? 'modal-open' : ''}`}>
      {/* Backdrop/Overlay */}
      <div
        className="modal-backdrop"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal Container */}
      <div
        className={`modal-container modal-${size}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        {/* Header */}
        <div className="modal-header">
          <h2 id="modal-title" className="modal-title">
            {title}
          </h2>
          <button
            className="modal-close"
            onClick={onClose}
            aria-label="Close dialog"
          >
            <XIcon />
          </button>
        </div>

        {/* Body */}
        <div id="modal-description" className="modal-body">
          {children}
        </div>

        {/* Footer (if actions) */}
        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button className="btn-primary">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
```

### Modal Sizes
```css
.modal-small {
  max-width: 400px;
  width: 90%;
}

.modal-medium {
  max-width: 600px;
  width: 90%;
}

.modal-large {
  max-width: 900px;
  width: 90%;
}

.modal-fullscreen {
  width: 100vw;
  height: 100vh;
  max-width: none;
  margin: 0;
  border-radius: 0;
}

/* Responsive sizing */
@media (max-width: 768px) {
  .modal-container {
    width: 100%;
    height: 100%;
    max-width: none;
    margin: 0;
    border-radius: 0;
  }
}
```

## Focus Management

### Focus Trap Implementation
```typescript
class FocusTrap {
  private element: HTMLElement;
  private previousFocus: HTMLElement | null;
  private focusableElements: HTMLElement[];

  constructor(element: HTMLElement) {
    this.element = element;
    this.previousFocus = document.activeElement as HTMLElement;

    // Find all focusable elements
    this.focusableElements = Array.from(
      element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
    );

    this.init();
  }

  init() {
    // Focus first focusable element
    if (this.focusableElements.length > 0) {
      this.focusableElements[0].focus();
    }

    // Add event listeners
    this.element.addEventListener('keydown', this.handleKeyDown);
  }

  handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Tab') {
      const firstElement = this.focusableElements[0];
      const lastElement = this.focusableElements[this.focusableElements.length - 1];

      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }

    if (e.key === 'Escape') {
      this.close();
    }
  };

  close() {
    this.element.removeEventListener('keydown', this.handleKeyDown);
    this.previousFocus?.focus();
  }
}
```

### React Hook for Focus Management
```tsx
function useFocusTrap(ref: RefObject<HTMLElement>, isOpen: boolean) {
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isOpen || !ref.current) return;

    // Save current focus
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Get focusable elements
    const focusableElements = ref.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstFocusable = focusableElements[0] as HTMLElement;
    const lastFocusable = focusableElements[focusableElements.length - 1] as HTMLElement;

    // Focus first element
    firstFocusable?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable?.focus();
        } else if (!e.shiftKey && document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable?.focus();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      // Restore focus on cleanup
      previousFocusRef.current?.focus();
    };
  }, [isOpen, ref]);
}
```

## Animation Patterns

### Fade + Scale Entry
```css
@keyframes modal-enter {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes backdrop-enter {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-open .modal-backdrop {
  animation: backdrop-enter 200ms ease-out;
}

.modal-open .modal-container {
  animation: modal-enter 200ms ease-out;
}
```

### Slide Up (Mobile)
```css
@media (max-width: 768px) {
  @keyframes modal-slide-up {
    from {
      transform: translateY(100%);
    }
    to {
      transform: translateY(0);
    }
  }

  .modal-container {
    position: fixed;
    bottom: 0;
    animation: modal-slide-up 300ms ease-out;
  }
}
```

## Scroll Management

### Body Scroll Lock
```typescript
class ScrollLock {
  private scrollPosition: number = 0;

  lock() {
    // Save scroll position
    this.scrollPosition = window.scrollY;

    // Apply styles to prevent scrolling
    document.body.style.position = 'fixed';
    document.body.style.top = `-${this.scrollPosition}px`;
    document.body.style.width = '100%';
    document.body.style.overflow = 'hidden';
  }

  unlock() {
    // Remove styles
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    document.body.style.overflow = '';

    // Restore scroll position
    window.scrollTo(0, this.scrollPosition);
  }
}
```

### Scrollable Modal Content
```css
.modal-container {
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header,
.modal-footer {
  flex-shrink: 0;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  overscroll-behavior: contain;

  /* Smooth scrolling */
  scroll-behavior: smooth;

  /* Custom scrollbar */
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
}

.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: var(--scrollbar-track);
}

.modal-body::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb);
  border-radius: 4px;
}
```

## Radix UI Implementation

### Basic Modal with Radix
```tsx
import * as Dialog from '@radix-ui/react-dialog';

function RadixModal({ trigger, title, description, children }) {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        {trigger}
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="modal-overlay" />

        <Dialog.Content className="modal-content">
          <Dialog.Title className="modal-title">
            {title}
          </Dialog.Title>

          <Dialog.Description className="modal-description">
            {description}
          </Dialog.Description>

          {children}

          <div className="modal-actions">
            <Dialog.Close asChild>
              <button className="btn-secondary">Cancel</button>
            </Dialog.Close>
            <button className="btn-primary">Save</button>
          </div>

          <Dialog.Close asChild>
            <button className="modal-close-icon" aria-label="Close">
              <XIcon />
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

### Controlled Modal
```tsx
function ControlledModal() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger asChild>
        <button>Open Modal</button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay
          className="modal-overlay"
          onClick={() => setOpen(false)}
        />

        <Dialog.Content
          className="modal-content"
          onOpenAutoFocus={(event) => {
            // Prevent default focus behavior if needed
            event.preventDefault();
            // Focus specific element
            document.getElementById('first-input')?.focus();
          }}
        >
          <form
            onSubmit={(e) => {
              e.preventDefault();
              // Handle submit
              setOpen(false);
            }}
          >
            <input id="first-input" type="text" />
            <button type="submit">Submit</button>
          </form>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

## Headless UI Implementation

### Basic Modal with Headless UI
```tsx
import { Dialog, Transition } from '@headlessui/react';
import { Fragment } from 'react';

function HeadlessModal({ isOpen, onClose, title, children }) {
  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="modal-root" onClose={onClose}>
        {/* Backdrop */}
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="modal-backdrop" />
        </Transition.Child>

        {/* Modal */}
        <div className="modal-wrapper">
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0 scale-95"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-95"
          >
            <Dialog.Panel className="modal-panel">
              <Dialog.Title className="modal-title">
                {title}
              </Dialog.Title>

              <div className="modal-body">
                {children}
              </div>

              <div className="modal-footer">
                <button onClick={onClose}>Cancel</button>
                <button>Confirm</button>
              </div>
            </Dialog.Panel>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition>
  );
}
```

## Nested Modals

### Stack Management
```tsx
const ModalContext = createContext<{
  level: number;
  zIndex: number;
}>({ level: 0, zIndex: 1000 });

function NestedModal({ children, ...props }) {
  const parentContext = useContext(ModalContext);
  const level = parentContext.level + 1;
  const zIndex = parentContext.zIndex + 10;

  return (
    <ModalContext.Provider value={{ level, zIndex }}>
      <div
        className="modal"
        style={{ zIndex }}
        data-level={level}
      >
        {children}
      </div>
    </ModalContext.Provider>
  );
}
```

## Accessibility Patterns

### ARIA Attributes
```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
  aria-busy={isLoading}
>
  <h2 id="modal-title">Modal Title</h2>
  <p id="modal-description">Modal description text</p>
</div>
```

### Screen Reader Announcements
```tsx
function AccessibleModal({ title, message, isOpen }) {
  useEffect(() => {
    if (isOpen) {
      // Announce modal opening
      const announcement = `Dialog opened: ${title}`;
      announceToScreenReader(announcement);
    }
  }, [isOpen, title]);

  return (
    <div role="dialog" aria-modal="true">
      {/* Modal content */}
    </div>
  );
}

function announceToScreenReader(message: string) {
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', 'assertive');
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;

  document.body.appendChild(announcement);

  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
}
```

### Keyboard Shortcuts
```tsx
function useModalKeyboard(onClose: () => void, onConfirm?: () => void) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // ESC to close
      if (e.key === 'Escape') {
        onClose();
      }

      // Enter to confirm (if applicable)
      if (e.key === 'Enter' && onConfirm && e.ctrlKey) {
        e.preventDefault();
        onConfirm();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onClose, onConfirm]);
}
```

## Best Practices

1. **Focus management**: Always trap focus and restore on close
2. **Keyboard support**: ESC to close, Tab to navigate
3. **Scroll locking**: Prevent body scroll when modal is open
4. **Click outside**: Allow closing by clicking backdrop (when appropriate)
5. **Loading states**: Show loading indicators for async operations
6. **Error handling**: Display errors clearly within modal
7. **Mobile optimization**: Full-screen on mobile, centered on desktop
8. **Animation**: Smooth but quick transitions (200-300ms)
9. **Z-index management**: Use consistent z-index scale
10. **Accessibility**: Test with screen readers and keyboard navigation