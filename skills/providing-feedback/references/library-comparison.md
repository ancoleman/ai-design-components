# Feedback Library Comparison Guide

## Toast/Notification Libraries

### Sonner (Recommended for Modern React)

**Library:** `/emilkowalski/sonner`
**Trust Score:** 7.6/10
**Bundle Size:** ~5KB gzipped
**Dependencies:** Zero

**Strengths:**
- Built for React 18+ with modern patterns
- Zero dependencies
- Beautiful default styling
- Promise-based API for async operations
- Excellent accessibility out of the box
- Headless mode available
- Smooth animations

**Weaknesses:**
- Requires React 18+
- Limited browser support for older versions
- Less customization than some alternatives

**Best For:**
- Modern React applications
- Projects prioritizing accessibility
- Teams wanting beautiful defaults
- Applications using shadcn/ui

**Installation & Usage:**
```bash
npm install sonner
```

```tsx
import { Toaster, toast } from 'sonner';

// App root
<Toaster position="bottom-right" />

// Trigger notifications
toast.success('Operation completed');
toast.promise(fetchData(), {
  loading: 'Loading...',
  success: 'Data loaded',
  error: 'Failed to load'
});

// With action
toast('Message sent', {
  action: {
    label: 'Undo',
    onClick: () => console.log('Undo')
  }
});
```

---

### react-hot-toast (Lightweight Champion)

**Library:** `/timolins/react-hot-toast`
**Trust Score:** 9.5/10
**Bundle Size:** <5KB gzipped (including styles!)
**Dependencies:** Zero

**Strengths:**
- Ultra-lightweight
- Simple, intuitive API
- Highly customizable
- Good TypeScript support
- Headless mode available
- Fast performance

**Weaknesses:**
- Less feature-rich than alternatives
- Basic default styling
- Limited animation options

**Best For:**
- Bundle size critical applications
- Minimalist projects
- Custom design systems
- Performance-focused apps

**Installation & Usage:**
```bash
npm install react-hot-toast
```

```tsx
import toast, { Toaster } from 'react-hot-toast';

// App root
<Toaster
  position="bottom-right"
  toastOptions={{
    duration: 4000,
    style: {
      background: '#363636',
      color: '#fff'
    }
  }}
/>

// Trigger notifications
toast.success('Successfully saved!');
toast.error('Error occurred');
toast.loading('Loading...');

// Custom JSX
toast.custom((t) => (
  <div className={`${t.visible ? 'animate-enter' : 'animate-leave'}`}>
    Custom notification
  </div>
));
```

---

### react-toastify (Feature-Rich Veteran)

**Library:** `/fkhadra/react-toastify`
**Trust Score:** 10/10
**Bundle Size:** ~16KB gzipped
**Dependencies:** 1 (clsx)

**Strengths:**
- Most mature and battle-tested
- Extensive features
- RTL language support
- Swipe to dismiss on mobile
- Pause on hover/focus
- Multiple containers
- Detailed documentation

**Weaknesses:**
- Larger bundle size
- More complex API
- Older styling approach
- Can be overkill for simple needs

**Best For:**
- Enterprise applications
- RTL/international support needed
- Mobile-first applications
- Complex notification requirements

**Installation & Usage:**
```bash
npm install react-toastify
```

```tsx
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// App root
<ToastContainer
  position="bottom-right"
  autoClose={5000}
  hideProgressBar={false}
  newestOnTop
  closeOnClick
  rtl={false}
  pauseOnFocusLoss
  draggable
  pauseOnHover
/>

// Trigger notifications
toast.success('Success!', {
  position: "bottom-right",
  autoClose: 5000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true
});

// Update existing toast
const toastId = toast.loading("Loading...");
toast.update(toastId, {
  render: "Success!",
  type: "success",
  isLoading: false
});
```

---

## Modal/Dialog Libraries

### Radix UI Dialog (Headless Powerhouse)

**Library:** `/radix-ui/primitives`
**Trust Score:** 8.7/10
**Bundle Size:** ~15KB for dialog
**Dependencies:** Multiple Radix primitives

**Strengths:**
- Completely unstyled (headless)
- WAI-ARIA compliant
- Excellent focus management
- Portal rendering
- Composable architecture
- Works with any styling solution

**Weaknesses:**
- No default styles
- Requires more setup
- Steeper learning curve

**Best For:**
- Design systems
- Custom styling requirements
- Accessibility-critical applications
- Teams wanting full control

**Installation & Usage:**
```bash
npm install @radix-ui/react-dialog
```

```tsx
import * as Dialog from '@radix-ui/react-dialog';

function RadixModal() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button>Open modal</button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content">
          <Dialog.Title>Modal Title</Dialog.Title>
          <Dialog.Description>
            Modal description here
          </Dialog.Description>

          <form>
            {/* Form fields */}
          </form>

          <Dialog.Close asChild>
            <button className="close-button">×</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

### Headless UI Dialog (Tailwind Official)

**Library:** `/tailwindlabs/headlessui`
**Trust Score:** 8/10
**Bundle Size:** ~12KB for dialog
**Dependencies:** None

**Strengths:**
- Designed for Tailwind CSS
- Excellent accessibility
- Simple API
- Built-in transitions
- Official Tailwind support
- Good documentation

**Weaknesses:**
- Best with Tailwind
- Less composable than Radix
- Fewer features

**Best For:**
- Tailwind CSS projects
- Rapid prototyping
- Teams familiar with Tailwind
- Simple modal needs

**Installation & Usage:**
```bash
npm install @headlessui/react
```

```tsx
import { Dialog, Transition } from '@headlessui/react';
import { Fragment, useState } from 'react';

function HeadlessModal() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>
        Open modal
      </button>

      <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" onClose={() => setIsOpen(false)}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black bg-opacity-25" />
          </Transition.Child>

          <div className="fixed inset-0 overflow-y-auto">
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
                <Dialog.Title>Modal Title</Dialog.Title>
                <Dialog.Description>
                  Modal description
                </Dialog.Description>

                <button onClick={() => setIsOpen(false)}>
                  Close
                </button>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </Dialog>
      </Transition>
    </>
  );
}
```

---

### react-modal (Classic Choice)

**Library:** `/reactjs/react-modal`
**Trust Score:** 9/10
**Bundle Size:** ~14KB gzipped
**Dependencies:** 2

**Strengths:**
- Mature and stable
- Good accessibility
- Simple API
- Well documented
- Wide browser support

**Weaknesses:**
- Older patterns
- Less flexible
- Requires app element setup
- Not headless

**Best For:**
- Legacy projects
- Simple modal needs
- Quick implementation
- Wide browser support needed

---

## Comparison Matrix

### Toast Libraries

| Feature | Sonner | react-hot-toast | react-toastify |
|---------|--------|-----------------|----------------|
| **Bundle Size** | ~5KB | <5KB | ~16KB |
| **Dependencies** | 0 | 0 | 1 |
| **React Version** | 18+ | 16.8+ | 16.8+ |
| **TypeScript** | ✅ Excellent | ✅ Good | ✅ Good |
| **Promise API** | ✅ Built-in | ✅ Built-in | ✅ Available |
| **Accessibility** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Customization** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Default Styling** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Mobile Support** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **RTL Support** | ❌ | ❌ | ✅ |
| **Learning Curve** | Easy | Very Easy | Moderate |

### Modal Libraries

| Feature | Radix UI | Headless UI | react-modal |
|---------|----------|-------------|-------------|
| **Bundle Size** | ~15KB | ~12KB | ~14KB |
| **Dependencies** | Multiple | 0 | 2 |
| **Headless** | ✅ | ✅ | ❌ |
| **TypeScript** | ✅ Excellent | ✅ Excellent | ✅ Good |
| **Accessibility** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Focus Management** | ✅ Auto | ✅ Auto | ✅ Manual setup |
| **Portal Rendering** | ✅ | ✅ | ✅ |
| **Composability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Animation Support** | Via CSS | Built-in | Via CSS |
| **Learning Curve** | Moderate | Easy | Easy |

---

## Decision Framework

### Choose Sonner if:
- Building modern React 18+ application
- Want beautiful defaults with minimal setup
- Accessibility is a priority
- Using shadcn/ui components
- Need promise-based notifications

### Choose react-hot-toast if:
- Bundle size is critical (<5KB)
- Need simple, lightweight solution
- Want full customization control
- Building minimalist interface

### Choose react-toastify if:
- Need RTL language support
- Building mobile app with swipe gestures
- Want most features out of the box
- Have complex notification requirements

### Choose Radix UI Dialog if:
- Building a design system
- Need complete styling control
- Want composable primitives
- Accessibility is critical

### Choose Headless UI Dialog if:
- Using Tailwind CSS
- Want official Tailwind support
- Need quick implementation
- Like utility-first CSS

---

## Recommended Stacks

### Modern Stack (Best Overall)
```bash
npm install sonner @radix-ui/react-dialog
```
- Sonner for toasts (modern, accessible, beautiful)
- Radix UI for modals (headless, composable)

### Minimal Stack (Smallest Bundle)
```bash
npm install react-hot-toast @headlessui/react
```
- react-hot-toast (<5KB for toasts)
- Headless UI (lightweight modals)

### Feature-Rich Stack (Everything Included)
```bash
npm install react-toastify react-modal
```
- react-toastify (all toast features)
- react-modal (stable, documented)

### Tailwind Stack (Best DX with Tailwind)
```bash
npm install sonner @headlessui/react
```
- Sonner (works great with Tailwind)
- Headless UI (designed for Tailwind)

---

## Migration Guides

### From react-toastify to Sonner
```tsx
// Before (react-toastify)
toast.success('Success!', {
  position: "bottom-right",
  autoClose: 5000
});

// After (Sonner)
toast.success('Success!', {
  duration: 5000
});
```

### From react-modal to Radix UI
```tsx
// Before (react-modal)
<Modal isOpen={isOpen} onRequestClose={onClose}>
  <h2>Title</h2>
  <p>Content</p>
</Modal>

// After (Radix UI)
<Dialog.Root open={isOpen} onOpenChange={setIsOpen}>
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Title>Title</Dialog.Title>
      <Dialog.Description>Content</Dialog.Description>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

---

## Performance Considerations

### Bundle Size Impact
- **Smallest:** react-hot-toast (<5KB)
- **Small:** Sonner (~5KB)
- **Medium:** Headless UI (~12KB), react-modal (~14KB), Radix UI (~15KB)
- **Large:** react-toastify (~16KB)

### Runtime Performance
- **Fastest:** react-hot-toast (minimal overhead)
- **Fast:** Sonner, Headless UI
- **Good:** Radix UI, react-modal
- **Moderate:** react-toastify (more features = more overhead)

### Tree-Shaking
- **Best:** Radix UI (import only what you need)
- **Good:** Headless UI, Sonner
- **Limited:** react-toastify, react-modal

---

## Accessibility Scores

Based on WAI-ARIA compliance and screen reader testing:

1. **Radix UI Dialog:** 10/10 - Perfect accessibility
2. **Headless UI Dialog:** 10/10 - Perfect accessibility
3. **Sonner:** 9/10 - Excellent ARIA support
4. **react-modal:** 8/10 - Good with proper setup
5. **react-toastify:** 8/10 - Good built-in support
6. **react-hot-toast:** 7/10 - Basic ARIA support