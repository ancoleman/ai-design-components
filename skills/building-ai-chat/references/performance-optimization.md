# Performance Optimization for AI Chat

## Table of Contents

- [Streaming Optimization](#streaming-optimization)
- [Memoization Strategies](#memoization-strategies)
- [Virtual Scrolling](#virtual-scrolling)
- [Code Splitting](#code-splitting)
- [Bundle Optimization](#bundle-optimization)
- [Memory Management](#memory-management)
- [Network Optimization](#network-optimization)
- [Rendering Performance](#rendering-performance)

## Streaming Optimization

### Chunk Processing Optimization

Efficiently process streaming tokens:

```tsx
// Optimized stream processor with batching
class StreamProcessor {
  private buffer: string[] = [];
  private batchTimer: NodeJS.Timeout | null = null;
  private readonly batchSize = 10;
  private readonly batchDelay = 50; // ms

  constructor(
    private onBatch: (content: string) => void,
    private onComplete: () => void
  ) {}

  addChunk(chunk: string) {
    this.buffer.push(chunk);

    // Process immediately if buffer is full
    if (this.buffer.length >= this.batchSize) {
      this.flush();
    } else {
      // Schedule batch processing
      this.scheduleBatch();
    }
  }

  private scheduleBatch() {
    if (this.batchTimer) return;

    this.batchTimer = setTimeout(() => {
      this.flush();
    }, this.batchDelay);
  }

  private flush() {
    if (this.buffer.length === 0) return;

    const content = this.buffer.join('');
    this.buffer = [];

    if (this.batchTimer) {
      clearTimeout(this.batchTimer);
      this.batchTimer = null;
    }

    this.onBatch(content);
  }

  complete() {
    this.flush();
    this.onComplete();
  }
}

// Usage with React
function useStreamProcessor() {
  const [content, setContent] = useState('');
  const processorRef = useRef<StreamProcessor | null>(null);

  useEffect(() => {
    processorRef.current = new StreamProcessor(
      (batch) => setContent(prev => prev + batch),
      () => console.log('Stream complete')
    );

    return () => {
      processorRef.current?.complete();
    };
  }, []);

  const processChunk = useCallback((chunk: string) => {
    processorRef.current?.addChunk(chunk);
  }, []);

  return { content, processChunk };
}
```

### Markdown Parsing Optimization

Optimize markdown rendering during streaming:

```tsx
// Incremental markdown parser
class IncrementalMarkdownParser {
  private lastParsedContent = '';
  private lastParsedResult: ParsedContent[] = [];
  private parseCache = new Map<string, ParsedContent>();

  parse(content: string): ParsedContent[] {
    // Check if content is just appended to last
    if (content.startsWith(this.lastParsedContent)) {
      const newContent = content.slice(this.lastParsedContent.length);
      const newBlocks = this.parseNewContent(newContent);
      this.lastParsedResult = [...this.lastParsedResult, ...newBlocks];
    } else {
      // Full reparse needed
      this.lastParsedResult = this.fullParse(content);
    }

    this.lastParsedContent = content;
    return this.lastParsedResult;
  }

  private parseNewContent(content: string): ParsedContent[] {
    // Parse only the new content
    const blocks: ParsedContent[] = [];
    const lines = content.split('\n');

    for (const line of lines) {
      const cached = this.parseCache.get(line);
      if (cached) {
        blocks.push(cached);
      } else {
        const parsed = this.parseLine(line);
        this.parseCache.set(line, parsed);
        blocks.push(parsed);
      }
    }

    return blocks;
  }

  private fullParse(content: string): ParsedContent[] {
    // Implementation
    return marked.lexer(content).map(token => ({
      type: token.type,
      content: token.raw,
      rendered: this.renderToken(token)
    }));
  }

  private parseLine(line: string): ParsedContent {
    // Simplified line parser
    return {
      type: 'text',
      content: line,
      rendered: line
    };
  }

  private renderToken(token: any): string {
    // Token rendering logic
    return marked.parser([token]);
  }
}
```

## Memoization Strategies

### Component Memoization

Prevent unnecessary re-renders:

```tsx
// Memoized message component
const Message = memo(
  ({ message, isStreaming }: MessageProps) => {
    // Heavy computation memoized
    const processedContent = useMemo(
      () => processMarkdown(message.content),
      [message.content]
    );

    // Expensive formatting memoized
    const formattedTime = useMemo(
      () => formatRelativeTime(message.timestamp),
      [message.timestamp]
    );

    return (
      <div className="message">
        <time>{formattedTime}</time>
        <div className="content">{processedContent}</div>
      </div>
    );
  },
  // Custom comparison function
  (prevProps, nextProps) => {
    // Don't re-render if only isStreaming changed for other messages
    if (prevProps.message.id !== nextProps.message.id) {
      return true; // Props are equal, skip re-render
    }

    // Re-render if content changed
    if (prevProps.message.content !== nextProps.message.content) {
      return false; // Props differ, re-render needed
    }

    // Re-render if this message's streaming state changed
    if (prevProps.isStreaming !== nextProps.isStreaming) {
      return false;
    }

    return true; // Skip re-render
  }
);
```

### Hook Memoization

Optimize expensive hook computations:

```tsx
// Memoized search hook
function useMessageSearch(messages: Message[], query: string) {
  // Memoize search index creation
  const searchIndex = useMemo(() => {
    return messages.map((msg, index) => ({
      id: msg.id,
      index,
      content: msg.content.toLowerCase(),
      tokens: tokenize(msg.content.toLowerCase())
    }));
  }, [messages]);

  // Memoize search results
  const results = useMemo(() => {
    if (!query) return [];

    const queryLower = query.toLowerCase();
    const queryTokens = tokenize(queryLower);

    return searchIndex
      .filter(item => {
        // Quick exact match
        if (item.content.includes(queryLower)) return true;

        // Token-based match
        return queryTokens.every(token =>
          item.tokens.some(t => t.includes(token))
        );
      })
      .map(item => messages[item.index])
      .slice(0, 50); // Limit results
  }, [searchIndex, query, messages]);

  return results;
}

// Token cache to avoid re-tokenization
const tokenCache = new LRUCache<string, string[]>({ max: 1000 });

function tokenize(text: string): string[] {
  const cached = tokenCache.get(text);
  if (cached) return cached;

  const tokens = text.split(/\s+/).filter(Boolean);
  tokenCache.set(text, tokens);
  return tokens;
}
```

## Virtual Scrolling

### Large Conversation Handling

Efficiently render thousands of messages:

```tsx
import { VariableSizeList } from 'react-window';
import AutoSizer from 'react-virtualized-auto-sizer';

function VirtualizedChat({ messages }) {
  const listRef = useRef<VariableSizeList>(null);
  const rowHeights = useRef<Map<number, number>>(new Map());

  // Calculate and cache row heights
  const getItemSize = useCallback((index: number) => {
    return rowHeights.current.get(index) || estimateHeight(messages[index]);
  }, [messages]);

  const setItemSize = useCallback((index: number, size: number) => {
    if (rowHeights.current.get(index) !== size) {
      rowHeights.current.set(index, size);
      listRef.current?.resetAfterIndex(index);
    }
  }, []);

  // Estimate height based on content
  const estimateHeight = (message: Message) => {
    const lineCount = message.content.split('\n').length;
    const charCount = message.content.length;
    const baseHeight = 60; // padding + metadata
    const lineHeight = 24;
    const estimatedLines = Math.ceil(charCount / 80); // ~80 chars per line

    return baseHeight + Math.max(lineCount, estimatedLines) * lineHeight;
  };

  // Row component
  const Row = useCallback(({ index, style }: { index: number; style: any }) => {
    const message = messages[index];
    const rowRef = useRef<HTMLDivElement>(null);

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
  }, [messages, setItemSize]);

  // Auto-scroll to bottom
  useEffect(() => {
    if (messages.length > 0) {
      listRef.current?.scrollToItem(messages.length - 1, 'end');
    }
  }, [messages.length]);

  return (
    <AutoSizer>
      {({ height, width }) => (
        <VariableSizeList
          ref={listRef}
          height={height}
          width={width}
          itemCount={messages.length}
          itemSize={getItemSize}
          overscanCount={5}
          estimatedItemSize={150}
        >
          {Row}
        </VariableSizeList>
      )}
    </AutoSizer>
  );
}
```

## Code Splitting

### Dynamic Imports for Heavy Components

Split code for better initial load:

```tsx
// Lazy load heavy components
const SyntaxHighlighter = lazy(() =>
  import('react-syntax-highlighter').then(module => ({
    default: module.Prism
  }))
);

const ImageLightbox = lazy(() => import('./ImageLightbox'));
const VideoPlayer = lazy(() => import('./VideoPlayer'));
const FileViewer = lazy(() => import('./FileViewer'));

// Component with lazy loaded features
function MessageContent({ message }) {
  const [showLightbox, setShowLightbox] = useState(false);

  return (
    <div className="message-content">
      {/* Regular content always loaded */}
      <Streamdown>{message.text}</Streamdown>

      {/* Code blocks loaded on demand */}
      {message.codeBlocks && (
        <Suspense fallback={<div>Loading code...</div>}>
          {message.codeBlocks.map((code, i) => (
            <SyntaxHighlighter key={i} language={code.language}>
              {code.content}
            </SyntaxHighlighter>
          ))}
        </Suspense>
      )}

      {/* Images with lazy lightbox */}
      {message.images && message.images.map((img, i) => (
        <div key={i}>
          <img
            src={img.thumbnail}
            onClick={() => setShowLightbox(true)}
            loading="lazy"
          />
          {showLightbox && (
            <Suspense fallback={<div>Loading...</div>}>
              <ImageLightbox
                image={img}
                onClose={() => setShowLightbox(false)}
              />
            </Suspense>
          )}
        </div>
      ))}
    </div>
  );
}
```

### Route-Based Splitting

Split by features:

```tsx
// Route configuration with lazy loading
const routes = [
  {
    path: '/chat',
    component: lazy(() => import('./pages/Chat')),
    preload: true // Preload critical routes
  },
  {
    path: '/history',
    component: lazy(() => import('./pages/History'))
  },
  {
    path: '/settings',
    component: lazy(() => import('./pages/Settings'))
  },
  {
    path: '/analytics',
    component: lazy(() => import('./pages/Analytics'))
  }
];

// Preload critical routes
routes.filter(r => r.preload).forEach(route => {
  route.component.preload();
});
```

## Bundle Optimization

### Tree Shaking Configuration

Optimize bundle size:

```javascript
// webpack.config.js
module.exports = {
  optimization: {
    usedExports: true,
    sideEffects: false,
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        },
        ai: {
          test: /[\\/]node_modules[\\/](@ai-sdk|ai|openai|anthropic)/,
          name: 'ai-sdk',
          priority: 20
        },
        markdown: {
          test: /[\\/]node_modules[\\/](marked|remark|rehype|react-markdown)/,
          name: 'markdown',
          priority: 15
        },
        common: {
          minChunks: 2,
          priority: -10,
          reuseExistingChunk: true
        }
      }
    }
  }
};
```

### Import Optimization

Reduce bundle size with specific imports:

```tsx
// ❌ Bad - imports entire library
import _ from 'lodash';
const debounced = _.debounce(fn, 100);

// ✅ Good - imports only what's needed
import debounce from 'lodash/debounce';
const debounced = debounce(fn, 100);

// ❌ Bad - imports all icons
import * as Icons from 'lucide-react';

// ✅ Good - imports specific icons
import { Send, Copy, RefreshCw } from 'lucide-react';

// For dynamic icons
const iconMap = {
  send: lazy(() => import('lucide-react').then(m => ({ default: m.Send }))),
  copy: lazy(() => import('lucide-react').then(m => ({ default: m.Copy })))
};
```

## Memory Management

### Cleanup Strategies

Prevent memory leaks:

```tsx
function ChatSession() {
  const [messages, setMessages] = useState<Message[]>([]);
  const cleanupRefs = useRef<(() => void)[]>([]);

  // Cleanup old messages to prevent memory bloat
  useEffect(() => {
    const MAX_MESSAGES = 1000;

    if (messages.length > MAX_MESSAGES) {
      setMessages(prev => {
        // Clean up old message resources
        const toRemove = prev.slice(0, prev.length - MAX_MESSAGES);
        toRemove.forEach(msg => {
          // Revoke object URLs
          if (msg.images) {
            msg.images.forEach(img => URL.revokeObjectURL(img.url));
          }
          // Clear cached data
          messageCache.delete(msg.id);
        });

        return prev.slice(-MAX_MESSAGES);
      });
    }
  }, [messages.length]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanupRefs.current.forEach(cleanup => cleanup());
      // Clear all caches
      messageCache.clear();
      markdownCache.clear();
    };
  }, []);

  return <Chat messages={messages} />;
}
```

### Cache Management

Implement LRU caches:

```tsx
class LRUCache<K, V> {
  private cache = new Map<K, V>();
  private maxSize: number;

  constructor(maxSize: number) {
    this.maxSize = maxSize;
  }

  get(key: K): V | undefined {
    const value = this.cache.get(key);
    if (value) {
      // Move to end (most recently used)
      this.cache.delete(key);
      this.cache.set(key, value);
    }
    return value;
  }

  set(key: K, value: V): void {
    // Remove if exists (to update position)
    this.cache.delete(key);

    // Check size limit
    if (this.cache.size >= this.maxSize) {
      // Remove least recently used (first item)
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }

    this.cache.set(key, value);
  }

  clear(): void {
    this.cache.clear();
  }
}

// Use caches for expensive operations
const markdownCache = new LRUCache<string, string>(100);
const tokenCountCache = new LRUCache<string, number>(200);
const searchIndexCache = new LRUCache<string, any>(50);
```

## Network Optimization

### Request Batching

Batch multiple requests:

```tsx
class RequestBatcher {
  private queue: Array<{
    prompt: string;
    resolve: (response: any) => void;
    reject: (error: any) => void;
  }> = [];
  private timer: NodeJS.Timeout | null = null;
  private readonly batchSize = 5;
  private readonly batchDelay = 100;

  async add(prompt: string): Promise<any> {
    return new Promise((resolve, reject) => {
      this.queue.push({ prompt, resolve, reject });

      if (this.queue.length >= this.batchSize) {
        this.flush();
      } else {
        this.scheduleBatch();
      }
    });
  }

  private scheduleBatch() {
    if (this.timer) return;

    this.timer = setTimeout(() => {
      this.flush();
    }, this.batchDelay);
  }

  private async flush() {
    if (this.queue.length === 0) return;

    const batch = this.queue.splice(0, this.batchSize);

    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }

    try {
      // Send batch request
      const responses = await fetch('/api/batch', {
        method: 'POST',
        body: JSON.stringify({
          requests: batch.map(item => item.prompt)
        })
      }).then(r => r.json());

      // Resolve individual promises
      batch.forEach((item, i) => {
        item.resolve(responses[i]);
      });
    } catch (error) {
      batch.forEach(item => item.reject(error));
    }
  }
}
```

### Connection Pooling

Reuse connections efficiently:

```tsx
// Connection pool for WebSocket/SSE
class ConnectionPool {
  private connections = new Map<string, EventSource>();
  private readonly maxConnections = 5;

  getConnection(url: string): EventSource {
    // Reuse existing connection
    let connection = this.connections.get(url);

    if (!connection || connection.readyState === EventSource.CLOSED) {
      // Clean up closed connections
      if (this.connections.size >= this.maxConnections) {
        const oldestKey = this.connections.keys().next().value;
        this.connections.get(oldestKey)?.close();
        this.connections.delete(oldestKey);
      }

      // Create new connection
      connection = new EventSource(url);
      this.connections.set(url, connection);
    }

    return connection;
  }

  closeAll() {
    this.connections.forEach(conn => conn.close());
    this.connections.clear();
  }
}
```

## Rendering Performance

### Frame Rate Optimization

Maintain 60fps during streaming:

```tsx
// Use RAF for smooth updates
function useRAFUpdate(callback: (delta: number) => void) {
  const frameRef = useRef<number>();
  const previousTimeRef = useRef<number>();

  useEffect(() => {
    const animate = (time: number) => {
      if (previousTimeRef.current !== undefined) {
        const delta = time - previousTimeRef.current;
        callback(delta);
      }

      previousTimeRef.current = time;
      frameRef.current = requestAnimationFrame(animate);
    };

    frameRef.current = requestAnimationFrame(animate);

    return () => {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current);
      }
    };
  }, [callback]);
}

// Smooth streaming text updates
function StreamingText({ text }) {
  const [displayText, setDisplayText] = useState('');
  const targetRef = useRef(text);
  const currentRef = useRef('');

  targetRef.current = text;

  useRAFUpdate(useCallback((delta) => {
    if (currentRef.current.length < targetRef.current.length) {
      // Add characters at consistent rate
      const charsPerFrame = Math.ceil(delta / 16) * 2; // ~120 chars/sec
      const nextLength = Math.min(
        currentRef.current.length + charsPerFrame,
        targetRef.current.length
      );

      currentRef.current = targetRef.current.substring(0, nextLength);
      setDisplayText(currentRef.current);
    }
  }, []));

  return <div>{displayText}</div>;
}
```

### CSS Optimization

Optimize rendering with CSS:

```css
/* Use CSS containment for better performance */
.message {
  contain: layout style paint;
}

/* Use GPU acceleration for animations */
.streaming-cursor {
  transform: translateZ(0);
  will-change: opacity;
}

/* Optimize scrolling */
.chat-container {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
}

/* Reduce paint areas */
.message-content {
  isolation: isolate;
}

/* Use CSS Grid for layout (more performant than flexbox for large lists) */
.message-list {
  display: grid;
  grid-auto-rows: min-content;
  gap: 1rem;
}
```

## Performance Monitoring

### Performance Metrics

Track key metrics:

```tsx
function usePerformanceMonitor() {
  const metrics = useRef({
    fps: 0,
    memoryUsage: 0,
    renderTime: 0,
    streamLatency: 0
  });

  useEffect(() => {
    let frameCount = 0;
    let lastTime = performance.now();

    const measureFPS = () => {
      frameCount++;
      const currentTime = performance.now();

      if (currentTime >= lastTime + 1000) {
        metrics.current.fps = Math.round(
          (frameCount * 1000) / (currentTime - lastTime)
        );
        frameCount = 0;
        lastTime = currentTime;
      }

      requestAnimationFrame(measureFPS);
    };

    measureFPS();

    // Memory monitoring
    const measureMemory = () => {
      if ('memory' in performance) {
        metrics.current.memoryUsage = (performance as any).memory.usedJSHeapSize;
      }
    };

    const interval = setInterval(measureMemory, 1000);

    return () => clearInterval(interval);
  }, []);

  return metrics.current;
}
```

## Best Practices Summary

1. **Batch stream processing** - Process chunks in groups
2. **Memoize aggressively** - Cache expensive computations
3. **Use virtual scrolling** - For conversations >100 messages
4. **Split code smartly** - Lazy load heavy components
5. **Optimize bundles** - Tree shake and split chunks
6. **Manage memory** - Clean up old data and URLs
7. **Pool connections** - Reuse WebSocket/SSE connections
8. **Maintain 60fps** - Use RAF for smooth animations
9. **Monitor performance** - Track FPS, memory, latency
10. **Profile regularly** - Use Chrome DevTools Performance tab