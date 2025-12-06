# Message Component Patterns

Reusable component patterns for AI chat messages including bubbles, avatars, actions, and formatting.


## Table of Contents

- [Basic Message Structure](#basic-message-structure)
- [Message Bubble Variants](#message-bubble-variants)
  - [Minimal (iMessage-style)](#minimal-imessage-style)
  - [Card-based (ChatGPT-style)](#card-based-chatgpt-style)
- [Avatar Components](#avatar-components)
- [Message Actions](#message-actions)
- [Code Block Component](#code-block-component)
- [Markdown Rendering](#markdown-rendering)
- [Timestamp Display](#timestamp-display)
- [Suggested Actions (Quick Replies)](#suggested-actions-quick-replies)
- [Loading Skeleton](#loading-skeleton)
- [Message Grouping](#message-grouping)
- [Empty State](#empty-state)
- [Best Practices](#best-practices)
- [Component Library Integration](#component-library-integration)
  - [shadcn/ui](#shadcnui)
- [Resources](#resources)

## Basic Message Structure

```tsx
interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    model?: string;
    tokenCount?: number;
    latency?: number;
  };
}

function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <Avatar role={message.role} />
      <div className="message-content">
        <MessageBubble content={message.content} role={message.role} />
        <MessageMetadata {...message.metadata} />
        <MessageActions messageId={message.id} />
      </div>
    </div>
  );
}
```

## Message Bubble Variants

### Minimal (iMessage-style)

```tsx
function MessageBubble({ content, role }: Props) {
  return (
    <div
      style={{
        backgroundColor: role === 'user' ? '#3b82f6' : '#f3f4f6',
        color: role === 'user' ? '#fff' : '#1f2937',
        padding: '12px 16px',
        borderRadius: '18px',
        maxWidth: '70%',
        wordWrap: 'break-word',
      }}
    >
      {content}
    </div>
  );
}
```

### Card-based (ChatGPT-style)

```tsx
function MessageCard({ message }: Props) {
  return (
    <div
      style={{
        backgroundColor: message.role === 'user' ? 'transparent' : '#f7f7f8',
        padding: '24px',
        borderBottom: '1px solid #e5e5e5',
      }}
    >
      <div style={{ display: 'flex', gap: '16px', maxWidth: '800px', margin: '0 auto' }}>
        <Avatar role={message.role} size="md" />
        <div style={{ flex: 1 }}>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
```

## Avatar Components

```tsx
function Avatar({ role, size = 'sm' }: { role: string; size?: 'sm' | 'md' | 'lg' }) {
  const sizes = { sm: 32, md: 40, lg: 48 };
  const dimension = sizes[size];

  const avatarContent = {
    user: { icon: '👤', bg: '#3b82f6' },
    assistant: { icon: '🤖', bg: '#8b5cf6' },
    system: { icon: 'ℹ️', bg: '#6b7280' },
  }[role];

  return (
    <div
      style={{
        width: dimension,
        height: dimension,
        borderRadius: '50%',
        backgroundColor: avatarContent.bg,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: size === 'lg' ? '24px' : '18px',
        flexShrink: 0,
      }}
    >
      {avatarContent.icon}
    </div>
  );
}
```

## Message Actions

```tsx
function MessageActions({ messageId, content, onRegenerate }: Props) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex gap-2 mt-2 opacity-0 group-hover:opacity-100 transition">
      <button
        onClick={copyToClipboard}
        className="text-xs px-2 py-1 rounded hover:bg-gray-100"
        aria-label={copied ? 'Copied' : 'Copy message'}
      >
        {copied ? '✓ Copied' : '📋 Copy'}
      </button>

      <button
        onClick={() => onRegenerate(messageId)}
        className="text-xs px-2 py-1 rounded hover:bg-gray-100"
      >
        🔄 Regenerate
      </button>

      <button className="text-xs px-2 py-1 rounded hover:bg-gray-100">
        👍 Good
      </button>

      <button className="text-xs px-2 py-1 rounded hover:bg-gray-100">
        👎 Bad
      </button>
    </div>
  );
}
```

## Code Block Component

```tsx
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

function CodeBlock({ code, language }: { code: string; language: string }) {
  const [copied, setCopied] = useState(false);

  return (
    <div className="code-block-container">
      <div className="code-header">
        <span className="language-label">{language}</span>
        <button
          onClick={() => {
            navigator.clipboard.writeText(code);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
          }}
        >
          {copied ? '✓ Copied' : 'Copy code'}
        </button>
      </div>

      <SyntaxHighlighter
        language={language}
        style={vscDarkPlus}
        customStyle={{
          margin: 0,
          borderRadius: '0 0 8px 8px',
        }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}
```

## Markdown Rendering

```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function MessageContent({ content }: { content: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code: CodeBlock,
        a: ({ href, children }) => (
          <a href={href} target="_blank" rel="noopener noreferrer">
            {children} ↗
          </a>
        ),
        table: ({ children }) => (
          <div className="overflow-x-auto">
            <table className="min-w-full">{children}</table>
          </div>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
```

## Timestamp Display

```tsx
function MessageTimestamp({ timestamp }: { timestamp: Date }) {
  const formatTime = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();

    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return date.toLocaleDateString();
  };

  return (
    <time
      dateTime={timestamp.toISOString()}
      className="text-xs text-gray-500"
    >
      {formatTime(timestamp)}
    </time>
  );
}
```

## Suggested Actions (Quick Replies)

```tsx
function SuggestedActions({ suggestions, onSelect }: Props) {
  return (
    <div
      role="group"
      aria-label="Suggested prompts"
      className="flex flex-wrap gap-2 mt-4"
    >
      {suggestions.map((suggestion) => (
        <button
          key={suggestion.id}
          onClick={() => onSelect(suggestion.prompt)}
          className="px-3 py-2 bg-white border rounded-lg text-sm hover:bg-gray-50"
        >
          {suggestion.label}
        </button>
      ))}
    </div>
  );
}

// Usage
const suggestions = [
  { id: '1', label: 'Explain more', prompt: 'Can you explain that in more detail?' },
  { id: '2', label: 'Give example', prompt: 'Can you provide a code example?' },
  { id: '3', label: 'Simplify', prompt: 'Can you explain it more simply?' },
];
```

## Loading Skeleton

```tsx
function MessageSkeleton() {
  return (
    <div className="flex gap-4 animate-pulse">
      <div className="w-10 h-10 bg-gray-200 rounded-full" />
      <div className="flex-1 space-y-2">
        <div className="h-4 bg-gray-200 rounded w-3/4" />
        <div className="h-4 bg-gray-200 rounded w-1/2" />
      </div>
    </div>
  );
}
```

## Message Grouping

```tsx
// Group consecutive messages from same role
function MessageGroup({ messages }: { messages: Message[] }) {
  return (
    <div className="message-group">
      <Avatar role={messages[0].role} />
      <div className="message-stack">
        {messages.map((msg) => (
          <div key={msg.id} className="message-content">
            {msg.content}
            <MessageTimestamp timestamp={msg.timestamp} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Empty State

```tsx
function EmptyChat() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-8">
      <div className="text-6xl mb-4">💬</div>
      <h2 className="text-2xl font-semibold mb-2">Start a Conversation</h2>
      <p className="text-gray-600 mb-6">
        Ask me anything or try one of these suggestions:
      </p>
      <SuggestedActions
        suggestions={[
          { id: '1', label: 'Explain quantum computing', prompt: '...' },
          { id: '2', label: 'Write a Python function', prompt: '...' },
          { id: '3', label: 'Debug this code', prompt: '...' },
        ]}
      />
    </div>
  );
}
```

## Best Practices

1. **Use semantic HTML** - `<article>`, `<time>`, `<button>`, not `<div onclick>`
2. **ARIA roles and labels** - For screen reader context
3. **Keyboard navigation** - All actions accessible without mouse
4. **Focus management** - Return focus after actions
5. **Announce updates** - Use `aria-live` for new messages
6. **High contrast** - Minimum 4.5:1 text contrast
7. **Visible focus** - Clear focus indicators
8. **Alternative content** - Descriptions for images, code
9. **Error announcements** - `role="alert"` for errors
10. **Responsive text** - Allow font scaling

## Component Library Integration

### shadcn/ui

```tsx
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

function Message({ message }: Props) {
  return (
    <Card className="p-4">
      <div className="flex gap-4">
        <Avatar>
          <AvatarFallback>{message.role === 'user' ? 'U' : 'AI'}</AvatarFallback>
        </Avatar>
        <div className="flex-1">{message.content}</div>
      </div>
    </Card>
  );
}
```

## Resources

- React Aria: https://react-spectrum.adobe.com/react-aria/
- Radix UI Primitives: https://www.radix-ui.com/primitives
- ARIA Patterns: https://www.w3.org/WAI/ARIA/apg/patterns/
