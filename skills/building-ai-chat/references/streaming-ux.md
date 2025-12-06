# Streaming UX Patterns for AI Chat

Best practices for user experience when streaming LLM responses token-by-token.


## Table of Contents

- [Core Principles](#core-principles)
- [Visual Patterns](#visual-patterns)
  - [Loading States](#loading-states)
  - [Progressive Token Display](#progressive-token-display)
  - [Markdown Rendering While Streaming](#markdown-rendering-while-streaming)
- [Interaction Patterns](#interaction-patterns)
  - [Stop Generation Button](#stop-generation-button)
  - [Regenerate Response](#regenerate-response)
  - [Typing Indicator (User)](#typing-indicator-user)
- [Performance Optimizations](#performance-optimizations)
  - [Throttle Re-renders](#throttle-re-renders)
  - [Virtual Scrolling for Long Responses](#virtual-scrolling-for-long-responses)
  - [Debounced Auto-scroll](#debounced-auto-scroll)
- [Error Handling](#error-handling)
  - [Network Error Display](#network-error-display)
  - [Partial Response Recovery](#partial-response-recovery)
- [Accessibility](#accessibility)
  - [Screen Reader Announcements](#screen-reader-announcements)
  - [Keyboard Shortcuts](#keyboard-shortcuts)
- [Best Practices](#best-practices)
- [Anti-Patterns](#anti-patterns)

## Core Principles

1. **Show immediate feedback** - Don't wait for first token
2. **Stream progressively** - Append tokens as they arrive
3. **Indicate completion** - Clear visual cue when done
4. **Handle errors gracefully** - Don't leave users hanging
5. **Enable interruption** - Allow users to stop generation

## Visual Patterns

### Loading States

**Before first token arrives:**
```tsx
{isLoading && !response && (
  <div className="flex items-center gap-2">
    <div className="animate-pulse">●</div>
    <span className="text-gray-500">Thinking...</span>
  </div>
)}
```

**While streaming:**
```tsx
{isStreaming && (
  <div className="inline-block animate-pulse ml-1">▊</div>
)}
```

**Completion indicator:**
```tsx
{!isStreaming && response && (
  <div className="text-xs text-gray-400 mt-1">
    ✓ Complete • {tokenCount} tokens
  </div>
)}
```

### Progressive Token Display

```tsx
import { useState } from 'react';

function StreamingMessage({ message }: { message: string }) {
  return (
    <div className="prose">
      {message}
      <span className="inline-block w-1 h-4 bg-blue-500 animate-pulse ml-1" />
    </div>
  );
}
```

### Markdown Rendering While Streaming

```tsx
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

function StreamingMarkdown({ content }: { content: string }) {
  return (
    <ReactMarkdown
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');

          return !inline && match ? (
            <SyntaxHighlighter
              language={match[1]}
              PreTag="div"
              {...props}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>
              {children}
            </code>
          );
        },
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
```

## Interaction Patterns

### Stop Generation Button

```tsx
function ChatInterface() {
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const stopGeneration = () => {
    abortControllerRef.current?.abort();
    setIsStreaming(false);
  };

  const sendMessage = async (prompt: string) => {
    abortControllerRef.current = new AbortController();
    setIsStreaming(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        signal: abortControllerRef.current.signal,
        body: JSON.stringify({ prompt }),
      });

      const reader = response.body.getReader();
      // ... streaming logic
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('Generation stopped by user');
      }
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div>
      {isStreaming && (
        <button onClick={stopGeneration} className="stop-button">
          ⬛ Stop Generating
        </button>
      )}
    </div>
  );
}
```

### Regenerate Response

```tsx
function MessageActions({ messageId, onRegenerate }: Props) {
  return (
    <div className="flex gap-2 mt-2 opacity-0 group-hover:opacity-100 transition">
      <button onClick={() => onRegenerate(messageId)} className="text-sm">
        🔄 Regenerate
      </button>
      <button className="text-sm">📋 Copy</button>
      <button className="text-sm">👍 Good</button>
      <button className="text-sm">👎 Bad</button>
    </div>
  );
}
```

### Typing Indicator (User)

```tsx
function TypingIndicator({ isTyping }: { isTyping: boolean }) {
  if (!isTyping) return null;

  return (
    <div className="flex items-center gap-2 text-gray-500 text-sm">
      <div className="flex gap-1">
        <span className="animate-bounce" style={{ animationDelay: '0ms' }}>●</span>
        <span className="animate-bounce" style={{ animationDelay: '150ms' }}>●</span>
        <span className="animate-bounce" style={{ animationDelay: '300ms' }}>●</span>
      </div>
      AI is typing...
    </div>
  );
}
```

## Performance Optimizations

### Throttle Re-renders

```tsx
import { useMemo } from 'react';

function StreamingChat() {
  const [tokens, setTokens] = useState<string[]>([]);

  // Only update every 50ms (not every token)
  const displayText = useMemo(() => {
    return tokens.join('');
  }, [tokens]);

  return <div>{displayText}</div>;
}
```

### Virtual Scrolling for Long Responses

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function MessageList({ messages }: { messages: Message[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: messages.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 100,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((item) => (
          <div
            key={item.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${item.start}px)`,
            }}
          >
            <MessageComponent message={messages[item.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Debounced Auto-scroll

```tsx
import { useEffect, useRef } from 'react';

function ChatContainer({ messages, isStreaming }: Props) {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isStreaming) {
      endRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isStreaming]);

  return (
    <div className="messages">
      {messages.map((msg) => <Message key={msg.id} {...msg} />)}
      <div ref={endRef} />
    </div>
  );
}
```

## Error Handling

### Network Error Display

```tsx
{error && (
  <div className="error-message">
    <span>⚠️ Connection error. </span>
    <button onClick={retry}>Try again</button>
  </div>
)}
```

### Partial Response Recovery

```tsx
async function streamWithRecovery(prompt: string) {
  let partialResponse = '';

  try {
    for await (const token of streamTokens(prompt)) {
      partialResponse += token;
      setResponse(partialResponse);
    }
  } catch (error) {
    // Keep partial response, allow retry
    console.error('Stream interrupted:', error);
    setError('Connection lost. Partial response saved.');
    // partialResponse is still available
  }
}
```

## Accessibility

### Screen Reader Announcements

```tsx
import { useAnnouncer } from '@react-aria/live-announcer';

function StreamingChat() {
  const { announce } = useAnnouncer();

  useEffect(() => {
    if (isComplete) {
      announce('Response complete', 'polite');
    }
  }, [isComplete]);

  return <div role="log" aria-live="polite" aria-atomic="false">
    {response}
  </div>;
}
```

### Keyboard Shortcuts

```tsx
useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && isStreaming) {
      stopGeneration();
    }
    if (e.metaKey && e.key === 'k') {
      e.preventDefault();
      focusInput();
    }
  };

  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, [isStreaming]);
```

## Best Practices

1. **Show loading state immediately** - Don't wait for first token
2. **Use cursor/pulse animation** - Indicates active streaming
3. **Auto-scroll to bottom** - Keep latest content visible
4. **Allow stopping** - ESC key or stop button
5. **Preserve partial responses** - On error, don't lose what's streamed
6. **Throttle updates** - Update UI every 50ms, not every token
7. **Visual completion** - Clear indicator when done
8. **Enable regeneration** - Let users retry bad responses
9. **Format incrementally** - Render markdown as it streams
10. **Provide feedback actions** - Good/bad buttons, copy, share

## Anti-Patterns

**❌ Don't:**
- Wait for complete response before displaying
- Re-render entire component on every token
- Scroll to top on each update
- Block UI during streaming
- Hide partial responses on error
- Use polling instead of streaming

**✅ Do:**
- Stream progressively with SSE/WebSocket
- Update UI efficiently (throttle, memo)
- Auto-scroll smoothly to bottom
- Allow interaction during streaming
- Preserve partial content
- Use proper streaming protocols
