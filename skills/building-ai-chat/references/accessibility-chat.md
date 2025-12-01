# Accessibility Patterns for AI Chat

## Table of Contents

- [Screen Reader Support](#screen-reader-support)
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Live Regions](#aria-live-regions)
- [Focus Management](#focus-management)
- [Visual Indicators](#visual-indicators)
- [Voice Control](#voice-control)
- [Reduced Motion](#reduced-motion)
- [High Contrast Support](#high-contrast-support)

## Screen Reader Support

### Message Announcement Strategy

Properly announce new AI messages to screen readers:

```tsx
function AccessibleMessage({ message, isStreaming }) {
  // Use appropriate ARIA roles
  const getAriaRole = () => {
    if (message.role === 'system') return 'status';
    if (message.role === 'error') return 'alert';
    return 'article';
  };

  // Provide context for screen readers
  const getAriaLabel = () => {
    const role = message.role === 'assistant' ? 'AI' : message.role;
    const time = formatTime(message.timestamp);
    const status = isStreaming ? 'streaming' : 'complete';
    return `${role} message from ${time}, ${status}`;
  };

  return (
    <article
      role={getAriaRole()}
      aria-label={getAriaLabel()}
      aria-live={isStreaming ? 'off' : 'polite'}
      aria-busy={isStreaming}
      className={`message ${message.role}`}
    >
      {/* Hidden label for screen readers */}
      <h3 className="sr-only">
        {message.role === 'assistant' ? 'AI Response' : 'Your Message'}
      </h3>

      {/* Message metadata */}
      <div className="message-meta" aria-hidden="true">
        <span className="role">{message.role}</span>
        <time dateTime={message.timestamp.toISOString()}>
          {formatTime(message.timestamp)}
        </time>
      </div>

      {/* Message content */}
      <div className="message-content">
        {isStreaming ? (
          <div aria-live="off" aria-busy="true">
            {message.content}
            <span className="sr-only">Message still being typed</span>
          </div>
        ) : (
          <div>{message.content}</div>
        )}
      </div>

      {/* Actions with proper labels */}
      <div className="message-actions" role="toolbar" aria-label="Message actions">
        <button aria-label="Copy message to clipboard">
          <CopyIcon aria-hidden="true" />
          <span className="sr-only">Copy</span>
        </button>
        <button aria-label="Regenerate this response">
          <RefreshIcon aria-hidden="true" />
          <span className="sr-only">Regenerate</span>
        </button>
      </div>
    </article>
  );
}
```

### Conversation Structure

Semantic HTML for better screen reader navigation:

```tsx
function AccessibleConversation({ messages }) {
  return (
    <main className="conversation" role="main">
      <h1 className="sr-only">AI Chat Conversation</h1>

      {/* Conversation navigation for screen readers */}
      <nav aria-label="Conversation navigation" className="sr-only">
        <ul>
          <li><a href="#messages">Jump to messages</a></li>
          <li><a href="#input">Jump to message input</a></li>
          <li><a href="#actions">Jump to conversation actions</a></li>
        </ul>
      </nav>

      {/* Messages region */}
      <section
        id="messages"
        role="log"
        aria-label="Conversation messages"
        aria-live="polite"
        aria-relevant="additions"
      >
        <h2 className="sr-only">Messages</h2>

        {/* Group messages by time period for easier navigation */}
        {groupMessagesByTime(messages).map((group, i) => (
          <section key={i} aria-label={`Messages from ${group.label}`}>
            <h3 className="time-divider">
              <span>{group.label}</span>
            </h3>
            {group.messages.map(msg => (
              <AccessibleMessage key={msg.id} message={msg} />
            ))}
          </section>
        ))}

        {/* Loading indicator */}
        <div
          role="status"
          aria-live="assertive"
          aria-atomic="true"
          className="sr-only"
        >
          {isLoading && "AI is typing a response"}
        </div>
      </section>

      {/* Input region */}
      <section id="input" aria-label="Message input">
        <h2 className="sr-only">Send a message</h2>
        <MessageInput />
      </section>
    </main>
  );
}
```

## Keyboard Navigation

### Complete Keyboard Support

Enable full keyboard control:

```tsx
function KeyboardNavigableChat() {
  const [focusedMessage, setFocusedMessage] = useState(-1);
  const messagesRef = useRef<HTMLDivElement[]>([]);

  // Keyboard navigation handlers
  const handleKeyDown = (e: KeyboardEvent) => {
    // Navigate messages with arrow keys
    if (e.key === 'ArrowUp' && focusedMessage > 0) {
      e.preventDefault();
      setFocusedMessage(prev => prev - 1);
    } else if (e.key === 'ArrowDown' && focusedMessage < messages.length - 1) {
      e.preventDefault();
      setFocusedMessage(prev => prev + 1);
    }

    // Quick actions
    if (e.key === 'r' && e.ctrlKey) {
      e.preventDefault();
      regenerateLastMessage();
    }

    if (e.key === 'Enter' && e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }

    // Jump to input
    if (e.key === 'i' && e.ctrlKey) {
      e.preventDefault();
      inputRef.current?.focus();
    }

    // Stop generation
    if (e.key === 'Escape' && isStreaming) {
      e.preventDefault();
      stopGeneration();
    }
  };

  useEffect(() => {
    // Focus management
    if (focusedMessage >= 0 && messagesRef.current[focusedMessage]) {
      messagesRef.current[focusedMessage].focus();
    }
  }, [focusedMessage]);

  return (
    <div
      className="keyboard-navigable-chat"
      onKeyDown={handleKeyDown}
      role="application"
      aria-label="AI Chat Application"
    >
      {/* Keyboard shortcuts help */}
      <div className="sr-only" role="region" aria-label="Keyboard shortcuts">
        <h2>Keyboard Shortcuts</h2>
        <dl>
          <dt>Arrow Up/Down</dt>
          <dd>Navigate through messages</dd>
          <dt>Ctrl+R</dt>
          <dd>Regenerate last AI response</dd>
          <dt>Shift+Enter</dt>
          <dd>Send message</dd>
          <dt>Ctrl+I</dt>
          <dd>Jump to message input</dd>
          <dt>Escape</dt>
          <dd>Stop AI response generation</dd>
        </dl>
      </div>

      {/* Skip links */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <a href="#message-input" className="skip-link">
        Skip to message input
      </a>

      {/* Messages with keyboard navigation */}
      <div id="main-content">
        {messages.map((msg, i) => (
          <div
            key={msg.id}
            ref={el => messagesRef.current[i] = el}
            tabIndex={0}
            role="article"
            aria-label={`Message ${i + 1} of ${messages.length}`}
            className={`message ${focusedMessage === i ? 'focused' : ''}`}
          >
            {msg.content}
          </div>
        ))}
      </div>

      {/* Input with proper labels */}
      <div id="message-input">
        <label htmlFor="chat-input" className="sr-only">
          Type your message
        </label>
        <textarea
          id="chat-input"
          ref={inputRef}
          aria-label="Message input"
          aria-describedby="input-help"
          placeholder="Type a message... (Shift+Enter to send)"
        />
        <span id="input-help" className="sr-only">
          Press Shift+Enter to send, or use the send button
        </span>
      </div>
    </div>
  );
}
```

### Focus Trap for Modals

Trap focus in dialogs and modals:

```tsx
function FocusTrap({ children, isActive }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isActive) return;

    // Store current focus
    previousFocus.current = document.activeElement as HTMLElement;

    // Get all focusable elements
    const focusableElements = containerRef.current?.querySelectorAll(
      'a[href], button:not([disabled]), textarea:not([disabled]), ' +
      'input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );

    if (!focusableElements || focusableElements.length === 0) return;

    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    // Focus first element
    firstElement.focus();

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        // Shift+Tab (backwards)
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        // Tab (forwards)
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose?.();
      }
    };

    document.addEventListener('keydown', handleTabKey);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('keydown', handleTabKey);
      document.removeEventListener('keydown', handleEscape);

      // Restore previous focus
      previousFocus.current?.focus();
    };
  }, [isActive]);

  return (
    <div ref={containerRef} role="dialog" aria-modal="true">
      {children}
    </div>
  );
}
```

## ARIA Live Regions

### Dynamic Content Announcements

Announce streaming and status changes:

```tsx
function LiveRegionAnnouncer() {
  return (
    <>
      {/* Polite announcements for non-critical updates */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
        id="polite-announcer"
      />

      {/* Assertive announcements for important updates */}
      <div
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
        id="assertive-announcer"
      />

      {/* Log region for message history */}
      <div
        role="log"
        aria-live="polite"
        aria-relevant="additions"
        className="sr-only"
        id="message-log"
      />
    </>
  );
}

// Helper function to announce content
function announce(message: string, priority: 'polite' | 'assertive' = 'polite') {
  const announcer = document.getElementById(
    priority === 'assertive' ? 'assertive-announcer' : 'polite-announcer'
  );

  if (announcer) {
    // Clear and set to ensure announcement
    announcer.textContent = '';
    setTimeout(() => {
      announcer.textContent = message;
    }, 100);
  }
}

// Usage in components
function StreamingIndicator({ isStreaming }) {
  useEffect(() => {
    if (isStreaming) {
      announce('AI is typing a response', 'polite');
    } else {
      announce('AI has finished responding', 'polite');
    }
  }, [isStreaming]);

  return (
    <div aria-hidden="true" className="streaming-indicator">
      {isStreaming && <Spinner />}
    </div>
  );
}
```

## Focus Management

### Smart Focus Control

Manage focus during interactions:

```tsx
function FocusManager({ children }) {
  const lastFocusedElement = useRef<HTMLElement | null>(null);

  // Track focus for restoration
  const saveFocus = () => {
    lastFocusedElement.current = document.activeElement as HTMLElement;
  };

  const restoreFocus = () => {
    lastFocusedElement.current?.focus();
  };

  // Focus on new messages
  const focusNewMessage = (messageId: string) => {
    const element = document.getElementById(`message-${messageId}`);
    if (element) {
      // Announce to screen reader
      announce('New message received');

      // Move focus if user preference allows
      if (getUserPreference('autoFocusNewMessages')) {
        element.focus();
      }
    }
  };

  // Focus management for different scenarios
  const focusStrategies = {
    afterSend: () => {
      // Keep focus on input after sending
      const input = document.querySelector('.message-input') as HTMLElement;
      input?.focus();
    },

    afterRegenerate: () => {
      // Focus on regenerated message
      const lastMessage = document.querySelector('.message:last-child') as HTMLElement;
      lastMessage?.focus();
    },

    afterError: () => {
      // Focus on error message
      const error = document.querySelector('.error-message') as HTMLElement;
      error?.focus();
    },

    afterModalClose: () => {
      // Restore focus to trigger element
      restoreFocus();
    }
  };

  return (
    <FocusContext.Provider value={{ saveFocus, restoreFocus, ...focusStrategies }}>
      {children}
    </FocusContext.Provider>
  );
}
```

## Visual Indicators

### Clear Visual Feedback

Provide visual cues for all users:

```tsx
function VisualIndicators() {
  return (
    <style jsx>{`
      /* Focus indicators */
      *:focus {
        outline: 2px solid var(--focus-color, #0066cc);
        outline-offset: 2px;
      }

      /* High contrast focus */
      @media (prefers-contrast: high) {
        *:focus {
          outline: 3px solid currentColor;
          outline-offset: 3px;
        }
      }

      /* Focus visible only for keyboard */
      *:focus:not(:focus-visible) {
        outline: none;
      }

      *:focus-visible {
        outline: 2px solid var(--focus-color);
        outline-offset: 2px;
      }

      /* Loading states */
      .loading {
        position: relative;
      }

      .loading::after {
        content: '';
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
          45deg,
          transparent,
          transparent 10px,
          rgba(0, 0, 0, 0.05) 10px,
          rgba(0, 0, 0, 0.05) 20px
        );
        animation: loading-stripes 1s linear infinite;
      }

      @keyframes loading-stripes {
        to {
          background-position: 20px 0;
        }
      }

      /* Status indicators */
      .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
      }

      .status-indicator::before {
        content: '';
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--status-color);
      }

      .status-indicator.success::before {
        background-color: #10b981;
      }

      .status-indicator.warning::before {
        background-color: #f59e0b;
      }

      .status-indicator.error::before {
        background-color: #ef4444;
      }

      .status-indicator.info::before {
        background-color: #3b82f6;
      }
    `}</style>
  );
}
```

## Voice Control

### Voice Command Integration

Enable voice control for accessibility:

```tsx
function VoiceControl({ onCommand }) {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  const commands = {
    'send message': () => document.querySelector('.send-button')?.click(),
    'regenerate': () => document.querySelector('.regenerate-button')?.click(),
    'stop': () => document.querySelector('.stop-button')?.click(),
    'clear': () => clearConversation(),
    'scroll up': () => window.scrollBy(0, -200),
    'scroll down': () => window.scrollBy(0, 200),
    'go to top': () => window.scrollTo(0, 0),
    'go to bottom': () => window.scrollTo(0, document.body.scrollHeight),
    'read last message': () => readLastMessage(),
    'help': () => showVoiceHelp()
  };

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window)) return;

    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = (event: any) => {
      const last = event.results.length - 1;
      const command = event.results[last][0].transcript.toLowerCase().trim();

      // Check for matching command
      for (const [phrase, action] of Object.entries(commands)) {
        if (command.includes(phrase)) {
          action();
          announce(`Executed: ${phrase}`, 'polite');
          break;
        }
      }
    };

    recognition.onerror = (event: any) => {
      console.error('Voice recognition error:', event.error);
      setIsListening(false);
    };

    recognitionRef.current = recognition;

    return () => {
      recognition.stop();
    };
  }, []);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      recognitionRef.current?.start();
      setIsListening(true);
    }
  };

  return (
    <div className="voice-control">
      <button
        onClick={toggleListening}
        aria-label={isListening ? 'Stop voice control' : 'Start voice control'}
        className={`voice-button ${isListening ? 'listening' : ''}`}
      >
        <MicrophoneIcon />
        {isListening && <span className="listening-indicator">Listening...</span>}
      </button>

      <div className="sr-only" role="status" aria-live="polite">
        {isListening ? 'Voice control active' : 'Voice control inactive'}
      </div>
    </div>
  );
}
```

## Reduced Motion

### Respect Motion Preferences

Honor prefers-reduced-motion:

```tsx
function useReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (e: MediaQueryListEvent) => {
      setPrefersReducedMotion(e.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
}

// Apply reduced motion styles
function ReducedMotionStyles() {
  return (
    <style jsx global>{`
      @media (prefers-reduced-motion: reduce) {
        * {
          animation-duration: 0.01ms !important;
          animation-iteration-count: 1 !important;
          transition-duration: 0.01ms !important;
          scroll-behavior: auto !important;
        }

        /* Keep essential animations but make them instant */
        .streaming-cursor {
          animation: none;
          opacity: 1;
        }

        .loading-spinner {
          animation: none;
          border-color: var(--primary-color) transparent;
        }

        /* Remove parallax and smooth scrolling */
        .smooth-scroll {
          scroll-behavior: auto;
        }

        /* Simplify complex transitions */
        .message-appear {
          opacity: 1;
          transform: none;
        }
      }
    `}</style>
  );
}

// Component usage
function AnimatedMessage({ message }) {
  const prefersReducedMotion = useReducedMotion();

  return (
    <div
      className={`message ${!prefersReducedMotion ? 'animated' : ''}`}
      style={{
        animation: prefersReducedMotion ? 'none' : 'slideIn 0.3s ease-out'
      }}
    >
      {message.content}
    </div>
  );
}
```

## High Contrast Support

### High Contrast Mode

Support Windows High Contrast and forced colors:

```tsx
function HighContrastStyles() {
  return (
    <style jsx global>{`
      /* High contrast mode support */
      @media (prefers-contrast: high) {
        .message {
          border: 2px solid currentColor;
        }

        .button {
          border: 2px solid currentColor;
          font-weight: bold;
        }

        .input {
          border: 2px solid currentColor;
          background: transparent;
        }

        /* Ensure focus indicators are visible */
        *:focus {
          outline: 3px solid currentColor;
          outline-offset: 3px;
        }

        /* Make sure icons are visible */
        .icon {
          filter: none;
          opacity: 1;
        }
      }

      /* Forced colors mode (Windows High Contrast) */
      @media (forced-colors: active) {
        .message {
          border: 1px solid ButtonText;
        }

        .message.user {
          background: Canvas;
          color: CanvasText;
          border-color: Highlight;
        }

        .message.assistant {
          background: Canvas;
          color: CanvasText;
          border-color: LinkText;
        }

        .button {
          background: ButtonFace;
          color: ButtonText;
          border: 1px solid ButtonText;
        }

        .button:hover {
          background: Highlight;
          color: HighlightText;
        }

        .button:disabled {
          color: GrayText;
          border-color: GrayText;
        }

        /* Ensure status indicators work */
        .status-success {
          color: LinkText;
        }

        .status-error {
          color: VisitedText;
        }
      }

      /* Custom high contrast theme */
      [data-theme="high-contrast"] {
        --background: #000;
        --foreground: #fff;
        --primary: #0ff;
        --secondary: #ff0;
        --border: #fff;
        --focus: #0ff;

        * {
          font-weight: 500;
        }

        .message {
          border: 2px solid var(--border);
        }
      }
    `}</style>
  );
}
```

### Color Contrast Validation

Ensure WCAG compliance:

```tsx
function ContrastChecker({ foreground, background }) {
  const getContrast = (fg: string, bg: string): number => {
    // Calculate relative luminance
    const getLuminance = (color: string): number => {
      const rgb = hexToRgb(color);
      const [r, g, b] = rgb.map(val => {
        val = val / 255;
        return val <= 0.03928
          ? val / 12.92
          : Math.pow((val + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };

    const l1 = getLuminance(foreground);
    const l2 = getLuminance(background);

    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  };

  const ratio = getContrast(foreground, background);
  const meetsAA = ratio >= 4.5;
  const meetsAAA = ratio >= 7;

  return (
    <div className="contrast-checker">
      <div className="contrast-ratio">
        Contrast: {ratio.toFixed(2)}:1
      </div>
      <div className="wcag-compliance">
        <span className={meetsAA ? 'pass' : 'fail'}>
          WCAG AA: {meetsAA ? '✓' : '✗'}
        </span>
        <span className={meetsAAA ? 'pass' : 'fail'}>
          WCAG AAA: {meetsAAA ? '✓' : '✗'}
        </span>
      </div>
    </div>
  );
}
```

## Best Practices Summary

1. **Semantic HTML** - Use proper roles and landmarks
2. **ARIA labels** - Provide context for screen readers
3. **Keyboard navigation** - Everything accessible via keyboard
4. **Focus management** - Logical focus order and restoration
5. **Live regions** - Announce dynamic changes appropriately
6. **High contrast** - Support forced colors and high contrast modes
7. **Reduced motion** - Respect user preferences for animation
8. **Voice control** - Alternative input methods
9. **Clear indicators** - Visual, auditory, and haptic feedback
10. **WCAG compliance** - Meet AA standards minimum