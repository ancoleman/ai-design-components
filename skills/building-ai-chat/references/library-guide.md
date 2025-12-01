# AI Chat Library Guide

## Table of Contents

- [Vercel AI SDK](#vercel-ai-sdk)
- [Streamdown](#streamdown)
- [React Integration](#react-integration)
- [Alternative Libraries](#alternative-libraries)
- [Framework-Specific Solutions](#framework-specific-solutions)
- [Production Deployment](#production-deployment)

## Vercel AI SDK

### Installation & Setup

The industry-standard SDK for AI chat interfaces:

```bash
# Core packages
npm install ai @ai-sdk/react

# Provider-specific packages
npm install @ai-sdk/openai     # For OpenAI/GPT
npm install @ai-sdk/anthropic   # For Claude
npm install @ai-sdk/google      # For Gemini
npm install @ai-sdk/mistral     # For Mistral
```

### Basic Implementation

Complete chat implementation with Vercel AI SDK:

```tsx
// app/api/chat/route.ts (Next.js App Router)
import { openai } from '@ai-sdk/openai';
import { streamText, convertToUIStream } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4-turbo'),
    messages,
    system: 'You are a helpful AI assistant.',
    temperature: 0.7,
    maxTokens: 2000,
  });

  return result.toUIMessageStreamResponse();
}
```

```tsx
// app/chat/page.tsx (Client Component)
'use client';

import { useChat } from '@ai-sdk/react';

export default function ChatPage() {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    error,
    reload,
    stop,
    append
  } = useChat({
    api: '/api/chat',
    onFinish: (message) => {
      console.log('Message complete:', message);
    },
    onError: (error) => {
      console.error('Chat error:', error);
    }
  });

  return (
    <div className="chat-container">
      {/* Messages */}
      <div className="messages">
        {messages.map(m => (
          <div key={m.id} className={`message ${m.role}`}>
            <div className="role">{m.role}</div>
            <div className="content">{m.content}</div>
          </div>
        ))}
      </div>

      {/* Error display */}
      {error && (
        <div className="error">
          Error: {error.message}
          <button onClick={reload}>Retry</button>
        </div>
      )}

      {/* Input form */}
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Say something..."
          disabled={isLoading}
        />
        {isLoading ? (
          <button type="button" onClick={stop}>Stop</button>
        ) : (
          <button type="submit">Send</button>
        )}
      </form>
    </div>
  );
}
```

### Advanced Features

#### Tool Calling / Function Calling

```tsx
// API Route with tools
import { tool } from 'ai';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4-turbo'),
    messages,
    tools: {
      weather: tool({
        description: 'Get current weather for a location',
        parameters: z.object({
          location: z.string().describe('City name'),
          unit: z.enum(['celsius', 'fahrenheit']).optional()
        }),
        execute: async ({ location, unit = 'celsius' }) => {
          const weather = await fetchWeather(location, unit);
          return weather;
        }
      }),

      calculate: tool({
        description: 'Perform mathematical calculations',
        parameters: z.object({
          expression: z.string().describe('Math expression to evaluate')
        }),
        execute: async ({ expression }) => {
          return eval(expression); // Use a safe eval library in production
        }
      })
    },
    toolChoice: 'auto', // or 'required' or specific tool name
  });

  return result.toUIMessageStreamResponse();
}
```

#### Multi-Modal Support (Images)

```tsx
// Client component with image support
import { useChat } from '@ai-sdk/react';

function MultiModalChat() {
  const { messages, input, handleSubmit, handleInputChange } = useChat();
  const [images, setImages] = useState<string[]>([]);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);

    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImages(prev => [...prev, e.target?.result as string]);
      };
      reader.readAsDataURL(file);
    });
  };

  const sendWithImages = (e: React.FormEvent) => {
    e.preventDefault();

    const messageWithImages = {
      role: 'user',
      content: [
        { type: 'text', text: input },
        ...images.map(img => ({ type: 'image', image: img }))
      ]
    };

    handleSubmit(e, {
      data: { images }
    });

    setImages([]);
  };

  return (
    <form onSubmit={sendWithImages}>
      <input
        type="file"
        accept="image/*"
        multiple
        onChange={handleImageUpload}
      />
      {images.map((img, i) => (
        <img key={i} src={img} alt="" width="100" />
      ))}
      <input
        value={input}
        onChange={handleInputChange}
        placeholder="Describe the images..."
      />
      <button type="submit">Send</button>
    </form>
  );
}
```

#### Streaming with Metadata

```tsx
// Stream with additional metadata
const result = streamText({
  model: openai('gpt-4-turbo'),
  messages,
  onChunk: ({ chunk, delta }) => {
    // Process each chunk
    console.log('Token:', delta);
  },
  onFinish: ({ text, usage, finishReason }) => {
    // Log usage stats
    console.log('Tokens used:', usage);
    console.log('Finish reason:', finishReason);
  },
  // Experimental features
  experimental_streamData: true,
});

// Add data to stream
result.dataStream.write({ progress: 50 });
result.dataStream.write({ status: 'Processing images...' });
```

## Streamdown

### Installation

Optimized markdown renderer for streaming AI responses:

```bash
npm install @vercel/streamdown
```

### Basic Usage

```tsx
import { Streamdown } from '@vercel/streamdown';

function StreamingMessage({ content, isStreaming }) {
  return (
    <Streamdown
      // Handle incomplete markdown gracefully
      allowDangerousHtml={false}

      // Custom components for rendering
      components={{
        // Override default renderers
        h1: ({ children }) => (
          <h1 className="text-2xl font-bold">{children}</h1>
        ),

        code: ({ inline, className, children }) => {
          const language = className?.replace('language-', '');

          if (inline) {
            return <code className="inline-code">{children}</code>;
          }

          return (
            <SyntaxHighlighter language={language} style={dark}>
              {children}
            </SyntaxHighlighter>
          );
        },

        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            {children}
            <ExternalLinkIcon />
          </a>
        )
      }}

      // Streaming-specific options
      options={{
        // Buffer incomplete blocks
        bufferIncompleteTables: true,
        bufferIncompleteCodeblocks: true,
        bufferIncompleteLists: true,

        // Performance optimizations
        memoize: true,
        throttle: 50, // ms
      }}
    >
      {content}
    </Streamdown>
  );
}
```

### Advanced Streamdown Patterns

```tsx
// Custom Streamdown wrapper with all features
function EnhancedStreamdown({ content, isStreaming }) {
  const [processedContent, setProcessedContent] = useState('');

  useEffect(() => {
    if (isStreaming) {
      // Pre-process content for better streaming
      const processed = preprocessMarkdown(content);
      setProcessedContent(processed);
    } else {
      setProcessedContent(content);
    }
  }, [content, isStreaming]);

  const preprocessMarkdown = (text: string) => {
    let processed = text;

    // Close unclosed code blocks
    const codeBlockCount = (processed.match(/```/g) || []).length;
    if (codeBlockCount % 2 !== 0) {
      processed += '\n```';
    }

    // Close unclosed bold/italic
    const boldCount = (processed.match(/\*\*/g) || []).length;
    if (boldCount % 2 !== 0) {
      processed += '**';
    }

    // Close unclosed lists
    if (processed.match(/^[\*\-\+]\s/m) && !processed.endsWith('\n')) {
      processed += '\n';
    }

    return processed;
  };

  return (
    <Streamdown
      components={{
        // Math rendering
        math: ({ value }) => (
          <KaTeX math={value} displayMode={false} />
        ),

        // Tables with sorting
        table: ({ children }) => (
          <div className="table-wrapper">
            <table className="data-table">{children}</table>
          </div>
        ),

        // Copy button for code blocks
        pre: ({ children }) => (
          <div className="code-block-wrapper">
            <button
              className="copy-button"
              onClick={() => copyCode(children)}
            >
              <CopyIcon />
            </button>
            <pre>{children}</pre>
          </div>
        ),

        // Collapsible details
        details: ({ children, summary }) => (
          <details className="expandable">
            <summary>{summary}</summary>
            {children}
          </details>
        )
      }}

      plugins={[
        // GitHub Flavored Markdown
        remarkGfm,
        // Math support
        remarkMath,
        // Emoji support
        remarkEmoji,
      ]}
    >
      {processedContent}
    </Streamdown>
  );
}
```

## React Integration

### Custom Hooks

Essential hooks for AI chat:

```tsx
// useStreamingMessage hook
function useStreamingMessage(initialContent = '') {
  const [content, setContent] = useState(initialContent);
  const [isStreaming, setIsStreaming] = useState(false);
  const contentRef = useRef('');

  const startStreaming = useCallback(() => {
    setIsStreaming(true);
    contentRef.current = '';
    setContent('');
  }, []);

  const appendChunk = useCallback((chunk: string) => {
    contentRef.current += chunk;
    setContent(contentRef.current);
  }, []);

  const endStreaming = useCallback(() => {
    setIsStreaming(false);
  }, []);

  return {
    content,
    isStreaming,
    startStreaming,
    appendChunk,
    endStreaming
  };
}

// useConversation hook
function useConversation(conversationId?: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [context, setContext] = useState({ tokens: 0, maxTokens: 4000 });

  // Load conversation
  useEffect(() => {
    if (conversationId) {
      loadConversation(conversationId).then(setMessages);
    }
  }, [conversationId]);

  // Auto-save
  useEffect(() => {
    const saveTimer = setTimeout(() => {
      if (messages.length > 0) {
        saveConversation(conversationId, messages);
      }
    }, 1000);

    return () => clearTimeout(saveTimer);
  }, [messages, conversationId]);

  const addMessage = useCallback((message: Message) => {
    setMessages(prev => [...prev, message]);
    updateTokenCount(message);
  }, []);

  const updateMessage = useCallback((id: string, updates: Partial<Message>) => {
    setMessages(prev =>
      prev.map(msg => msg.id === id ? { ...msg, ...updates } : msg)
    );
  }, []);

  const deleteMessage = useCallback((id: string) => {
    setMessages(prev => prev.filter(msg => msg.id !== id));
  }, []);

  return {
    messages,
    context,
    addMessage,
    updateMessage,
    deleteMessage,
    clearConversation: () => setMessages([])
  };
}
```

### Component Library

Reusable chat components:

```tsx
// Message component library
const ChatComponents = {
  Message: ({ message, onAction }) => (
    <div className={`message ${message.role}`}>
      <Avatar role={message.role} />
      <div className="message-content">
        <Streamdown>{message.content}</Streamdown>
      </div>
      <MessageActions message={message} onAction={onAction} />
    </div>
  ),

  Input: ({ onSubmit, disabled, placeholder }) => {
    const [value, setValue] = useState('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    // Auto-resize textarea
    useEffect(() => {
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
        textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
      }
    }, [value]);

    return (
      <form onSubmit={(e) => {
        e.preventDefault();
        if (value.trim()) {
          onSubmit(value);
          setValue('');
        }
      }}>
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              onSubmit(value);
              setValue('');
            }
          }}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
        />
        <button type="submit" disabled={disabled || !value.trim()}>
          Send
        </button>
      </form>
    );
  },

  Thread: ({ messages, currentBranch, onBranchSwitch }) => (
    <div className="thread">
      {messages.map((msg, i) => (
        <React.Fragment key={msg.id}>
          {msg.branches && msg.branches.length > 1 && (
            <BranchSelector
              branches={msg.branches}
              current={currentBranch}
              onSelect={onBranchSwitch}
            />
          )}
          <ChatComponents.Message message={msg} />
        </React.Fragment>
      ))}
    </div>
  )
};
```

## Alternative Libraries

### Other AI SDKs

```tsx
// OpenAI SDK (direct)
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function chat(messages: any[]) {
  const stream = await openai.chat.completions.create({
    model: 'gpt-4-turbo',
    messages,
    stream: true,
  });

  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}

// Anthropic SDK
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function claudeChat(prompt: string) {
  const message = await anthropic.messages.create({
    model: 'claude-3-opus-20240229',
    max_tokens: 1000,
    messages: [{ role: 'user', content: prompt }],
  });

  return message.content;
}

// LangChain
import { ChatOpenAI } from '@langchain/openai';
import { HumanMessage, SystemMessage } from '@langchain/core/messages';

const model = new ChatOpenAI({
  modelName: 'gpt-4-turbo',
  temperature: 0.7,
  streaming: true,
});

const response = await model.invoke([
  new SystemMessage('You are a helpful assistant'),
  new HumanMessage('Hello!')
]);
```

### Markdown Renderers

```tsx
// react-markdown (alternative to Streamdown)
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

function MarkdownRenderer({ content }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');
          return !inline && match ? (
            <SyntaxHighlighter
              language={match[1]}
              style={dark}
              {...props}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>
              {children}
            </code>
          );
        }
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
```

## Framework-Specific Solutions

### Next.js Integration

```tsx
// app/api/chat/route.ts (App Router)
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  // Auth check
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { messages } = await req.json();

  // Rate limiting
  const rateLimitResult = await checkRateLimit(session.userId);
  if (!rateLimitResult.allowed) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    );
  }

  try {
    const result = streamText({
      model: openai('gpt-4-turbo'),
      messages,
      // User-specific context
      system: `User preferences: ${session.preferences}`,
    });

    return result.toUIMessageStreamResponse();
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### Vue.js Integration

```vue
<!-- ChatComponent.vue -->
<template>
  <div class="chat">
    <div v-for="message in messages" :key="message.id" :class="`message ${message.role}`">
      <div class="content" v-html="renderMarkdown(message.content)" />
    </div>

    <form @submit.prevent="sendMessage">
      <input
        v-model="input"
        :disabled="isLoading"
        placeholder="Type a message..."
      />
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Sending...' : 'Send' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useChat } from '@ai-sdk/vue';
import { marked } from 'marked';

const { messages, input, isLoading, sendMessage } = useChat({
  api: '/api/chat'
});

const renderMarkdown = (content) => {
  return marked(content);
};
</script>
```

## Production Deployment

### Environment Setup

```bash
# .env.local
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_AI_API_KEY=...

# Rate limiting
UPSTASH_REDIS_URL=...
UPSTASH_REDIS_TOKEN=...

# Database
DATABASE_URL=postgresql://...

# Auth
NEXTAUTH_URL=https://yourdomain.com
NEXTAUTH_SECRET=...
```

### Production Checklist

```tsx
// Production configuration
const productionConfig = {
  // Error boundaries
  errorHandling: {
    onError: (error) => {
      console.error('Chat error:', error);
      trackError(error);
      showUserFriendlyError();
    },
    retry: {
      maxAttempts: 3,
      backoff: 'exponential'
    }
  },

  // Rate limiting
  rateLimit: {
    requests: 100,
    window: '1h',
    byUser: true
  },

  // Security
  security: {
    sanitizeOutput: true,
    validateInput: true,
    maxMessageLength: 10000,
    allowedFileTypes: ['image/png', 'image/jpeg', 'application/pdf']
  },

  // Performance
  performance: {
    streamingChunkSize: 10,
    debounceMs: 50,
    virtualScrollThreshold: 100,
    lazyLoadImages: true
  },

  // Analytics
  analytics: {
    trackEvents: true,
    collectFeedback: true,
    monitorLatency: true
  }
};
```

## Best Practices Summary

1. **Use Vercel AI SDK** - Industry standard, best DX
2. **Implement streaming properly** - Use Streamdown for markdown
3. **Handle errors gracefully** - Network, rate limits, etc.
4. **Optimize performance** - Memoization, debouncing, virtual scroll
5. **Add auth & rate limiting** - Protect your API endpoints
6. **Monitor usage** - Track tokens, costs, performance
7. **Test across providers** - OpenAI, Anthropic, Google
8. **Implement feedback loops** - Collect user feedback
9. **Use proper TypeScript** - Type safety throughout
10. **Follow accessibility guidelines** - ARIA, keyboard support