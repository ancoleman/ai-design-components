# Streaming Response UX Patterns

## Table of Contents

- [Progressive Text Rendering](#progressive-text-rendering)
- [Handling Incomplete Markdown](#handling-incomplete-markdown)
- [Auto-Scroll Management](#auto-scroll-management)
- [Stop Generation Controls](#stop-generation-controls)
- [Loading & Thinking States](#loading--thinking-states)
- [Performance Optimization](#performance-optimization)
- [Streaming Cursor Behavior](#streaming-cursor-behavior)

## Progressive Text Rendering

### Token-by-Token Updates

Stream tokens as they arrive from the AI model:

```tsx
import { useChat } from 'ai/react';
import { Streamdown } from '@vercel/streamdown';

function StreamingMessage({ message }) {
  return (
    <div className="message ai">
      <Streamdown>
        {message.content}
      </Streamdown>
      {message.isStreaming && <StreamingCursor />}
    </div>
  );
}

function StreamingCursor() {
  return <span className="streaming-cursor">▊</span>;
}

// CSS for blinking cursor
const cursorStyles = `
.streaming-cursor {
  animation: blink 1s infinite;
  color: var(--cursor-color, currentColor);
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
`;
```

### Debounced Rendering

Batch rapid token updates for performance:

```tsx
import { useMemo, useCallback } from 'react';
import debounce from 'lodash/debounce';

function useStreamingMessage(initialContent = '') {
  const [content, setContent] = useState(initialContent);
  const [displayContent, setDisplayContent] = useState(initialContent);

  // Debounce display updates to 50ms
  const updateDisplay = useMemo(
    () => debounce((newContent: string) => {
      setDisplayContent(newContent);
    }, 50),
    []
  );

  const appendToken = useCallback((token: string) => {
    setContent(prev => {
      const updated = prev + token;
      updateDisplay(updated);
      return updated;
    });
  }, [updateDisplay]);

  return { content: displayContent, appendToken };
}
```

## Handling Incomplete Markdown

### Buffering Strategy

Buffer incomplete syntax elements:

```tsx
class MarkdownBuffer {
  private buffer = '';
  private completeBlocks: string[] = [];

  append(text: string): { complete: string; incomplete: string } {
    this.buffer += text;

    // Check for complete code blocks
    const codeBlockRegex = /```[\s\S]*?```/g;
    const matches = this.buffer.match(codeBlockRegex);

    if (matches) {
      matches.forEach(match => {
        this.completeBlocks.push(match);
        this.buffer = this.buffer.replace(match, '');
      });
    }

    // Check for complete paragraphs
    const paragraphs = this.buffer.split('\n\n');
    if (paragraphs.length > 1) {
      this.completeBlocks.push(...paragraphs.slice(0, -1));
      this.buffer = paragraphs[paragraphs.length - 1];
    }

    return {
      complete: this.completeBlocks.join('\n\n'),
      incomplete: this.buffer
    };
  }

  flush(): string {
    const result = [...this.completeBlocks, this.buffer].join('\n\n');
    this.buffer = '';
    this.completeBlocks = [];
    return result;
  }
}
```

### Graceful Partial Rendering

Render partial markdown without breaking:

```tsx
import { marked } from 'marked';

function SafeMarkdownRenderer({ content, isStreaming }) {
  const renderMarkdown = useCallback((text: string) => {
    try {
      // Add closing tags for incomplete blocks if streaming
      let safeText = text;

      if (isStreaming) {
        // Close unclosed code blocks
        const openBackticks = (text.match(/```/g) || []).length;
        if (openBackticks % 2 !== 0) {
          safeText += '\n```';
        }

        // Close unclosed bold/italic
        const openBold = (text.match(/\*\*/g) || []).length;
        if (openBold % 2 !== 0) {
          safeText += '**';
        }

        const openItalic = (text.match(/(?<!\*)\*(?!\*)/g) || []).length;
        if (openItalic % 2 !== 0) {
          safeText += '*';
        }
      }

      return marked(safeText);
    } catch (error) {
      // Fallback to plain text if parsing fails
      return text;
    }
  }, [isStreaming]);

  return (
    <div
      className="markdown-content"
      dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
    />
  );
}
```

## Auto-Scroll Management

### Intelligent Auto-Scroll Heuristic

Only auto-scroll when appropriate:

```tsx
function useAutoScroll(messagesContainerRef: RefObject<HTMLDivElement>) {
  const [userScrolledUp, setUserScrolledUp] = useState(false);
  const [lastScrollTime, setLastScrollTime] = useState(Date.now());
  const scrollTimeoutRef = useRef<NodeJS.Timeout>();

  const handleScroll = useCallback(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const { scrollTop, scrollHeight, clientHeight } = container;
    const isAtBottom = scrollHeight - scrollTop - clientHeight < 100;

    setUserScrolledUp(!isAtBottom);
    setLastScrollTime(Date.now());

    // Reset after 3 seconds of no scrolling
    clearTimeout(scrollTimeoutRef.current);
    scrollTimeoutRef.current = setTimeout(() => {
      if (!isAtBottom) {
        setUserScrolledUp(false);
      }
    }, 3000);
  }, [messagesContainerRef]);

  const shouldAutoScroll = useCallback(() => {
    const container = messagesContainerRef.current;
    if (!container) return false;

    // Don't auto-scroll if:
    // 1. User has scrolled up
    // 2. User is selecting text
    // 3. User scrolled in last 3 seconds
    const isSelecting = window.getSelection()?.toString().length > 0;
    const recentlyScrolled = Date.now() - lastScrollTime < 3000;

    return !userScrolledUp && !isSelecting && !recentlyScrolled;
  }, [userScrolledUp, lastScrollTime, messagesContainerRef]);

  const scrollToBottom = useCallback((smooth = true) => {
    const container = messagesContainerRef.current;
    if (!container) return;

    container.scrollTo({
      top: container.scrollHeight,
      behavior: smooth ? 'smooth' : 'instant'
    });
  }, [messagesContainerRef]);

  return {
    handleScroll,
    shouldAutoScroll,
    scrollToBottom,
    userScrolledUp
  };
}
```

### New Messages Indicator

Show when new messages arrive off-screen:

```tsx
function NewMessagesIndicator({ show, onClick, count }) {
  if (!show) return null;

  return (
    <button
      className="new-messages-indicator"
      onClick={onClick}
      aria-label={`${count} new messages, click to scroll down`}
    >
      <ChevronDownIcon />
      {count > 0 && <span className="count">{count} new</span>}
    </button>
  );
}

// CSS
const indicatorStyles = `
.new-messages-indicator {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-primary);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}
`;
```

## Stop Generation Controls

### Stop Button Implementation

Always-visible stop control during streaming:

```tsx
function StopGenerationButton({ isStreaming, onStop }) {
  const [showConfirm, setShowConfirm] = useState(false);
  const messageLength = useMessageLength(); // Hook to track current message length

  const handleStop = useCallback(() => {
    // Confirm if message is >50% complete (estimate)
    if (messageLength > 500 && !showConfirm) {
      setShowConfirm(true);
      setTimeout(() => setShowConfirm(false), 3000);
      return;
    }

    onStop();
    setShowConfirm(false);
  }, [messageLength, showConfirm, onStop]);

  if (!isStreaming) return null;

  return (
    <div className="stop-generation-container">
      <button
        className="stop-button"
        onClick={handleStop}
        aria-label="Stop AI response generation"
      >
        <StopIcon />
        {showConfirm ? 'Click again to confirm' : 'Stop generating'}
      </button>

      {/* Keyboard shortcut hint */}
      <span className="keyboard-hint">Press Esc</span>
    </div>
  );
}

// Keyboard shortcut hook
function useStopShortcut(onStop: () => void, isStreaming: boolean) {
  useEffect(() => {
    if (!isStreaming) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        onStop();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isStreaming, onStop]);
}
```

### Post-Stop Actions

After stopping generation:

```tsx
function PostStopActions({ message, onContinue, onRegenerate, onEdit }) {
  return (
    <div className="post-stop-actions">
      <div className="stop-indicator">
        <InfoIcon />
        <span>Response stopped</span>
      </div>

      <div className="action-buttons">
        <button onClick={onContinue} className="continue-btn">
          <PlayIcon />
          Continue from here
        </button>

        <button onClick={onRegenerate} className="regenerate-btn">
          <RefreshIcon />
          Start over
        </button>

        <button onClick={onEdit} className="edit-btn">
          <EditIcon />
          Edit prompt
        </button>
      </div>
    </div>
  );
}
```

## Loading & Thinking States

### Progressive Loading States

Show appropriate feedback at each stage:

```tsx
function LoadingStates({ status, duration }) {
  return (
    <div className="loading-states" role="status" aria-live="polite">
      {status === 'connecting' && (
        <div className="connecting">
          <Spinner size="small" />
          <span>Connecting...</span>
        </div>
      )}

      {status === 'thinking' && (
        <div className="thinking">
          <ThinkingDots />
          <span>AI is thinking...</span>
          {duration > 5000 && (
            <span className="duration-hint">Complex request, this may take a moment</span>
          )}
        </div>
      )}

      {status === 'streaming' && (
        <div className="streaming-indicator">
          <StreamIcon />
          <span>Generating response...</span>
        </div>
      )}

      {status === 'tooluse' && (
        <div className="tool-use">
          <ToolIcon />
          <span>Using tools...</span>
        </div>
      )}
    </div>
  );
}

function ThinkingDots() {
  return (
    <span className="thinking-dots">
      <span>●</span>
      <span>●</span>
      <span>●</span>
    </span>
  );
}

// CSS for animated dots
const thinkingDotsStyles = `
.thinking-dots span {
  animation: pulse 1.4s infinite ease-in-out;
}

.thinking-dots span:nth-child(2) {
  animation-delay: 0.16s;
}

.thinking-dots span:nth-child(3) {
  animation-delay: 0.32s;
}

@keyframes pulse {
  0%, 60%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  30% {
    opacity: 1;
    transform: scale(1);
  }
}
`;
```

### Timeout Handling

Handle long-running requests:

```tsx
function useRequestTimeout(onTimeout: () => void, timeoutMs = 30000) {
  const timeoutRef = useRef<NodeJS.Timeout>();
  const [isTimedOut, setIsTimedOut] = useState(false);

  const startTimeout = useCallback(() => {
    clearTimeout(timeoutRef.current);
    setIsTimedOut(false);

    timeoutRef.current = setTimeout(() => {
      setIsTimedOut(true);
      onTimeout();
    }, timeoutMs);
  }, [onTimeout, timeoutMs]);

  const clearTimeout = useCallback(() => {
    clearTimeout(timeoutRef.current);
    setIsTimedOut(false);
  }, []);

  return { startTimeout, clearTimeout, isTimedOut };
}

// Usage
function TimeoutWarning({ show, onRetry, onCancel }) {
  if (!show) return null;

  return (
    <div className="timeout-warning">
      <WarningIcon />
      <p>This is taking longer than usual</p>
      <div className="timeout-actions">
        <button onClick={onRetry}>Keep waiting</button>
        <button onClick={onCancel}>Cancel</button>
      </div>
    </div>
  );
}
```

## Performance Optimization

### Memoization for Streaming

Critical for smooth 60fps streaming:

```tsx
import { memo, useMemo } from 'react';
import { marked } from 'marked';

// Parse markdown into blocks for individual memoization
function parseIntoBlocks(markdown: string): Block[] {
  const tokens = marked.lexer(markdown);
  return tokens.map((token, index) => ({
    id: `block-${index}`,
    type: token.type,
    content: token.raw,
    hash: hashString(token.raw) // Simple hash for comparison
  }));
}

// Memoize individual blocks
const MemoizedBlock = memo(
  ({ block }: { block: Block }) => {
    const rendered = useMemo(
      () => marked.parse(block.content),
      [block.hash]
    );

    return (
      <div
        className={`markdown-block ${block.type}`}
        dangerouslySetInnerHTML={{ __html: rendered }}
      />
    );
  },
  (prev, next) => prev.block.hash === next.block.hash
);

// Main streaming component with memoization
export const OptimizedStreamingMessage = memo(({ content, id }) => {
  const blocks = useMemo(
    () => parseIntoBlocks(content),
    [content]
  );

  return (
    <div className="streaming-message">
      {blocks.map(block => (
        <MemoizedBlock key={block.id} block={block} />
      ))}
    </div>
  );
});

// Simple hash function for block comparison
function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return hash;
}
```

### Virtual Scrolling for Long Conversations

Handle thousands of messages efficiently:

```tsx
import { VariableSizeList } from 'react-window';

function VirtualizedMessageList({ messages }) {
  const listRef = useRef<VariableSizeList>();
  const rowHeights = useRef({});

  const getItemSize = useCallback((index: number) => {
    return rowHeights.current[index] || 100; // Default height
  }, []);

  const setItemSize = useCallback((index: number, size: number) => {
    rowHeights.current[index] = size;
    listRef.current?.resetAfterIndex(index);
  }, []);

  const Row = ({ index, style }) => {
    const message = messages[index];
    const rowRef = useRef<HTMLDivElement>();

    useEffect(() => {
      if (rowRef.current) {
        const height = rowRef.current.getBoundingClientRect().height;
        setItemSize(index, height);
      }
    }, [index, message.content]);

    return (
      <div style={style}>
        <div ref={rowRef}>
          <Message message={message} />
        </div>
      </div>
    );
  };

  return (
    <VariableSizeList
      ref={listRef}
      height={600}
      itemCount={messages.length}
      itemSize={getItemSize}
      width="100%"
    >
      {Row}
    </VariableSizeList>
  );
}
```

### Web Worker for Heavy Processing

Offload markdown parsing to worker:

```javascript
// markdown-worker.js
import { marked } from 'marked';

self.addEventListener('message', (event) => {
  const { id, content } = event.data;

  try {
    const parsed = marked.parse(content);
    self.postMessage({ id, parsed, error: null });
  } catch (error) {
    self.postMessage({ id, parsed: null, error: error.message });
  }
});

// Main thread usage
function useMarkdownWorker() {
  const workerRef = useRef<Worker>();
  const [parsed, setParsed] = useState('');

  useEffect(() => {
    workerRef.current = new Worker('/markdown-worker.js');

    workerRef.current.addEventListener('message', (event) => {
      const { parsed, error } = event.data;
      if (!error) {
        setParsed(parsed);
      }
    });

    return () => workerRef.current?.terminate();
  }, []);

  const parse = useCallback((content: string) => {
    workerRef.current?.postMessage({ id: Date.now(), content });
  }, []);

  return { parse, parsed };
}
```

## Streaming Cursor Behavior

### Smooth Cursor Animation

Create a natural typing feel:

```tsx
function StreamingCursor({ color = 'currentColor' }) {
  return (
    <span
      className="streaming-cursor"
      style={{ color }}
      aria-hidden="true"
    >
      ▊
    </span>
  );
}

// Advanced cursor with typing simulation
function TypingCursor({ speed = 'normal' }) {
  const speeds = {
    slow: 1500,
    normal: 1000,
    fast: 500
  };

  return (
    <span
      className="typing-cursor"
      style={{ animationDuration: `${speeds[speed]}ms` }}
    />
  );
}

// CSS for different cursor styles
const cursorStyles = `
/* Block cursor */
.streaming-cursor {
  display: inline-block;
  width: 2px;
  height: 1.2em;
  background-color: currentColor;
  animation: blink 1s infinite;
  margin-left: 1px;
}

/* Line cursor */
.typing-cursor {
  display: inline-block;
  width: 2px;
  height: 1em;
  background-color: var(--cursor-color);
  animation: blink var(--cursor-speed, 1s) infinite;
}

/* Underscore cursor */
.underscore-cursor {
  display: inline-block;
  width: 0.6em;
  height: 2px;
  background-color: currentColor;
  animation: blink 1s infinite;
  vertical-align: text-bottom;
}

@keyframes blink {
  0%, 49% { opacity: 1; }
  50%, 100% { opacity: 0; }
}

/* Smooth fade instead of blink */
@keyframes fade {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 1; }
}
`;
```

## Best Practices Summary

1. **Always use Streamdown or similar** for AI streaming (handles incomplete markdown)
2. **Implement smart auto-scroll** - Respect user intent
3. **Debounce updates** - Batch tokens for performance
4. **Memoize aggressively** - Prevent unnecessary re-renders
5. **Show clear loading states** - Users need feedback
6. **Make stop button prominent** - Always accessible during streaming
7. **Handle timeouts gracefully** - Long requests happen
8. **Use virtual scrolling** for conversations >100 messages
9. **Consider Web Workers** for heavy markdown processing
10. **Test with slow connections** - Ensure graceful degradation