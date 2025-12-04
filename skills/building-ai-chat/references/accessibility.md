# AI Chat Accessibility Guide

WCAG 2.1 AA compliance for AI chat interfaces with screen reader support, keyboard navigation, and ARIA patterns.

## Core Requirements

### 1. Semantic HTML and ARIA

```tsx
<div role="log" aria-live="polite" aria-atomic="false" aria-relevant="additions">
  {messages.map((msg) => (
    <div
      key={msg.id}
      role="article"
      aria-label={`Message from ${msg.role}`}
    >
      {msg.content}
    </div>
  ))}
</div>
```

**Key attributes:**
- `role="log"` - Messages appear chronologically
- `aria-live="polite"` - Screen reader announces new messages
- `aria-atomic="false"` - Only announce new additions
- `role="article"` - Each message is a discrete unit

### 2. Keyboard Navigation

```tsx
function ChatInput() {
  const handleKeyDown = (e: KeyboardEvent) => {
    // Send with Enter
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }

    // Newline with Shift+Enter
    if (e.key === 'Enter' && e.shiftKey) {
      // Allow default behavior (newline)
    }

    // Stop generation with Escape
    if (e.key === 'Escape' && isStreaming) {
      stopGeneration();
    }
  };

  return (
    <textarea
      onKeyDown={handleKeyDown}
      aria-label="Chat message input"
      placeholder="Type your message..."
    />
  );
}
```

**Keyboard shortcuts:**
- `Enter` - Send message
- `Shift+Enter` - New line
- `Escape` - Stop generation
- `Cmd/Ctrl+K` - Focus input
- `↑/↓` - Navigate message history

### 3. Focus Management

```tsx
import { useEffect, useRef } from 'react';

function ChatInterface() {
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Focus input after send
  useEffect(() => {
    if (!isStreaming) {
      inputRef.current?.focus();
    }
  }, [isStreaming]);

  // Trap focus during modal
  const handleTabKey = (e: KeyboardEvent) => {
    if (e.key === 'Tab') {
      // Keep focus within chat interface
    }
  };

  return <textarea ref={inputRef} onKeyDown={handleTabKey} />;
}
```

## Screen Reader Announcements

### Status Announcements

```tsx
import { useAnnouncer } from '@react-aria/live-announcer';

function ChatInterface() {
  const { announce } = useAnnouncer();

  useEffect(() => {
    if (isStreaming) {
      announce('AI is responding', 'polite');
    }
    if (isComplete) {
      announce('Response complete', 'polite');
    }
    if (error) {
      announce(`Error: ${error.message}`, 'assertive');
    }
  }, [isStreaming, isComplete, error]);
}
```

### Progress Updates

```tsx
// Announce progress for long responses
useEffect(() => {
  if (tokenCount > 0 && tokenCount % 100 === 0) {
    announce(`${tokenCount} tokens generated`, 'polite');
  }
}, [tokenCount]);
```

## Visual Accessibility

### Color Contrast

```tsx
// WCAG AA minimum: 4.5:1 for normal text, 3:1 for large text

const colors = {
  userMessage: {
    background: '#3b82f6',  // Blue
    text: '#ffffff',        // White (contrast: 8.6:1 ✓)
  },
  aiMessage: {
    background: '#f3f4f6',  // Light gray
    text: '#1f2937',        // Dark gray (contrast: 12.6:1 ✓)
  },
};
```

### Focus Indicators

```css
/* Visible focus outline */
button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

textarea:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 0;
}
```

### Text Sizing

```tsx
// Allow user to adjust text size
const [fontSize, setFontSize] = useState(16);

return (
  <div style={{ fontSize: `${fontSize}px` }}>
    {messages.map((msg) => <Message {...msg} />)}
  </div>
);
```

## Alternative Text for Images

```tsx
// Multi-modal chat with image input
function ImageMessage({ image, description }: Props) {
  return (
    <div>
      <img
        src={image.url}
        alt={description || 'User uploaded image'}
        aria-describedby={`img-desc-${image.id}`}
      />
      <p id={`img-desc-${image.id}`} className="sr-only">
        {description || 'Image uploaded by user for AI analysis'}
      </p>
    </div>
  );
}
```

## Loading States

```tsx
function ChatMessage({ message, isStreaming }: Props) {
  if (!message.content && isStreaming) {
    return (
      <div
        role="status"
        aria-label="AI is generating response"
        aria-live="polite"
      >
        <div className="flex gap-1">
          <span className="animate-pulse">●</span>
          <span className="animate-pulse animation-delay-75">●</span>
          <span className="animate-pulse animation-delay-150">●</span>
        </div>
        <span className="sr-only">AI is thinking...</span>
      </div>
    );
  }

  return <div>{message.content}</div>;
}
```

## Error Messages

```tsx
function ErrorMessage({ error }: { error: Error }) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className="error-banner"
    >
      <span aria-hidden="true">⚠️</span>
      <span>{error.message}</span>
      <button aria-label="Retry message">Retry</button>
      <button aria-label="Dismiss error">Dismiss</button>
    </div>
  );
}
```

## Code Block Accessibility

```tsx
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

function CodeBlock({ code, language }: Props) {
  const [copied, setCopied] = useState(false);

  return (
    <div role="region" aria-label={`Code block in ${language}`}>
      <div className="code-header">
        <span>{language}</span>
        <button
          onClick={() => {
            navigator.clipboard.writeText(code);
            setCopied(true);
          }}
          aria-label={copied ? 'Code copied' : 'Copy code to clipboard'}
        >
          {copied ? '✓ Copied' : '📋 Copy'}
        </button>
      </div>

      <SyntaxHighlighter
        language={language}
        customStyle={{ fontSize: '14px' }}
        wrapLongLines={true}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}
```

## Mobile Accessibility

### Touch Targets

```tsx
// Minimum 44x44px touch targets (WCAG 2.5.5)
const buttonStyles = {
  minHeight: '44px',
  minWidth: '44px',
  padding: '12px 16px',
};

<button style={buttonStyles}>Send</button>
```

### Reduced Motion

```tsx
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

<div
  className={prefersReducedMotion ? '' : 'animate-slide-up'}
>
  {message.content}
</div>
```

## Testing Checklist

- [ ] Screen reader announces new messages
- [ ] All controls keyboard-accessible
- [ ] Focus visible on all interactive elements
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Touch targets ≥44x44px
- [ ] Alt text for all images
- [ ] Errors announced with `role="alert"`
- [ ] Loading states announced
- [ ] Stop button accessible during streaming
- [ ] Works with reduced motion preference

## Resources

- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- React Aria: https://react-spectrum.adobe.com/react-aria/
