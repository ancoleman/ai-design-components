# Context & Memory Management

## Table of Contents

- [Token Limit Communication](#token-limit-communication)
- [Conversation Summarization](#conversation-summarization)
- [Conversation Branching](#conversation-branching)
- [Sliding Window Strategy](#sliding-window-strategy)
- [Conversation Organization](#conversation-organization)
- [Search & Retrieval](#search--retrieval)
- [Context Persistence](#context-persistence)

## Token Limit Communication

### User-Friendly Token Display

Convert technical token counts to understandable metrics:

```tsx
function TokenDisplay({ used, total, model }) {
  // Token to word approximation (model-specific)
  const tokenToWord = {
    'gpt-4': 0.75,      // ~1.33 tokens per word
    'claude-3': 0.8,    // ~1.25 tokens per word
    'gpt-3.5': 0.7      // ~1.43 tokens per word
  };

  const ratio = tokenToWord[model] || 0.75;
  const wordsUsed = Math.floor(used * ratio);
  const wordsTotal = Math.floor(total * ratio);
  const wordsRemaining = wordsTotal - wordsUsed;
  const percentage = (used / total) * 100;

  // Convert to relatable units
  const pagesRemaining = Math.floor(wordsRemaining / 250); // ~250 words per page
  const messagesRemaining = Math.floor(wordsRemaining / 50); // ~50 words per message

  return (
    <div className="token-display">
      <div className="token-bar">
        <div
          className={`token-fill ${percentage > 80 ? 'warning' : ''} ${percentage > 95 ? 'critical' : ''}`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="token-info">
        {percentage < 50 && (
          <span className="token-status good">
            Plenty of space for conversation
          </span>
        )}

        {percentage >= 50 && percentage < 80 && (
          <span className="token-status normal">
            About {pagesRemaining} pages remaining
          </span>
        )}

        {percentage >= 80 && percentage < 95 && (
          <span className="token-status warning">
            ⚠️ About {messagesRemaining} messages left before I need to summarize
          </span>
        )}

        {percentage >= 95 && (
          <span className="token-status critical">
            🔴 Almost at limit - let me summarize our conversation to continue
          </span>
        )}
      </div>

      <details className="token-details">
        <summary>Technical details</summary>
        <ul>
          <li>Tokens used: {used.toLocaleString()} / {total.toLocaleString()}</li>
          <li>Words (approx): {wordsUsed.toLocaleString()} / {wordsTotal.toLocaleString()}</li>
          <li>Context window: {percentage.toFixed(1)}% full</li>
        </ul>
      </details>
    </div>
  );
}
```

### Progressive Warnings

Alert users before hitting limits:

```tsx
function ContextWarnings({ percentage, onSummarize, onNewChat, onExport }) {
  const [dismissed, setDismissed] = useState(false);
  const [lastWarningLevel, setLastWarningLevel] = useState(0);

  useEffect(() => {
    // Show warnings at thresholds
    if (percentage >= 80 && lastWarningLevel < 80) {
      setLastWarningLevel(80);
      setDismissed(false);
    } else if (percentage >= 90 && lastWarningLevel < 90) {
      setLastWarningLevel(90);
      setDismissed(false);
    } else if (percentage >= 95 && lastWarningLevel < 95) {
      setLastWarningLevel(95);
      setDismissed(false);
    }
  }, [percentage, lastWarningLevel]);

  if (dismissed || percentage < 80) return null;

  return (
    <div className={`context-warning level-${lastWarningLevel}`}>
      <button
        className="dismiss"
        onClick={() => setDismissed(true)}
        aria-label="Dismiss warning"
      >
        ×
      </button>

      {percentage >= 80 && percentage < 90 && (
        <>
          <h4>Conversation getting long</h4>
          <p>We're using {percentage.toFixed(0)}% of the available context.</p>
          <div className="warning-actions">
            <button onClick={onSummarize} className="primary">
              Summarize conversation
            </button>
            <button onClick={onExport} className="secondary">
              Export and continue fresh
            </button>
          </div>
        </>
      )}

      {percentage >= 90 && percentage < 95 && (
        <>
          <h4>⚠️ Approaching context limit</h4>
          <p>Only a few messages left before we need to take action.</p>
          <div className="warning-actions">
            <button onClick={onSummarize} className="primary urgent">
              Summarize now
            </button>
            <button onClick={onNewChat} className="secondary">
              Start new conversation
            </button>
          </div>
        </>
      )}

      {percentage >= 95 && (
        <>
          <h4>🔴 Context limit reached</h4>
          <p>We need to free up space to continue.</p>
          <div className="warning-actions">
            <button onClick={onSummarize} className="primary critical">
              Auto-summarize and continue
            </button>
            <button onClick={onExport} className="secondary">
              Export full history
            </button>
          </div>
        </>
      )}
    </div>
  );
}
```

## Conversation Summarization

### Automatic Summarization

Compress conversation history while preserving key information:

```tsx
interface SummarizationConfig {
  threshold: number;        // Percentage to trigger (e.g., 90)
  preserveMessages: number; // Recent messages to keep verbatim
  pinned: string[];         // Message IDs to never summarize
}

async function summarizeConversation(
  messages: Message[],
  config: SummarizationConfig
): Promise<SummarizedConversation> {
  // Identify messages to summarize
  const recentCount = config.preserveMessages;
  const recent = messages.slice(-recentCount);
  const older = messages.slice(0, -recentCount);

  // Filter out pinned messages
  const toSummarize = older.filter(m => !config.pinned.includes(m.id));
  const preserved = older.filter(m => config.pinned.includes(m.id));

  // Generate summary
  const summary = await generateSummary(toSummarize);

  return {
    summary,
    preserved,
    recent,
    metadata: {
      originalCount: messages.length,
      summarizedCount: toSummarize.length,
      timestamp: new Date().toISOString()
    }
  };
}

async function generateSummary(messages: Message[]): Promise<string> {
  // Group messages by topic/theme
  const topics = groupMessagesByTopic(messages);

  // Create structured summary
  const summaryPrompt = `
    Summarize this conversation, preserving:
    - Key decisions made
    - Important information shared
    - Unresolved questions
    - Context needed for continuation

    Format as bullet points grouped by topic.
  `;

  // Call AI to generate summary
  const summary = await ai.generateSummary(messages, summaryPrompt);

  return summary;
}
```

### User-Controlled Summarization

Let users choose what to preserve:

```tsx
function SummarizationDialog({ messages, onConfirm, onCancel }) {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [preview, setPreview] = useState<string>('');

  const toggleMessage = (id: string) => {
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const generatePreview = async () => {
    const toSummarize = messages.filter(m => !selected.has(m.id));
    const summary = await generateSummary(toSummarize);
    setPreview(summary);
  };

  return (
    <dialog className="summarization-dialog">
      <h2>Optimize Conversation Context</h2>

      <div className="dialog-content">
        <div className="message-selector">
          <h3>Select messages to keep in full</h3>
          <p>Other messages will be summarized</p>

          <div className="message-list">
            {messages.map(msg => (
              <label key={msg.id} className="message-item">
                <input
                  type="checkbox"
                  checked={selected.has(msg.id)}
                  onChange={() => toggleMessage(msg.id)}
                />
                <div className="message-preview">
                  <span className="role">{msg.role}:</span>
                  <span className="content">
                    {msg.content.substring(0, 100)}...
                  </span>
                </div>
              </label>
            ))}
          </div>
        </div>

        <div className="summary-preview">
          <h3>Summary Preview</h3>
          <button onClick={generatePreview}>Generate Preview</button>
          {preview && (
            <div className="preview-content">
              {preview}
            </div>
          )}
        </div>
      </div>

      <div className="dialog-actions">
        <button onClick={() => onConfirm(selected)}>
          Confirm Summarization
        </button>
        <button onClick={onCancel}>
          Cancel
        </button>
      </div>
    </dialog>
  );
}
```

## Conversation Branching

### Branch Management

Allow forking conversations at any point:

```tsx
interface ConversationBranch {
  id: string;
  parentId: string | null;
  branchPoint: number; // Message index where branch occurred
  name: string;
  created: Date;
  messages: Message[];
}

class ConversationTree {
  private branches: Map<string, ConversationBranch> = new Map();
  private activeBranchId: string;

  constructor(initialMessages: Message[]) {
    const mainBranch: ConversationBranch = {
      id: 'main',
      parentId: null,
      branchPoint: 0,
      name: 'Main conversation',
      created: new Date(),
      messages: initialMessages
    };

    this.branches.set('main', mainBranch);
    this.activeBranchId = 'main';
  }

  createBranch(
    fromMessageIndex: number,
    name?: string
  ): ConversationBranch {
    const parent = this.branches.get(this.activeBranchId)!;
    const branchId = `branch-${Date.now()}`;

    const newBranch: ConversationBranch = {
      id: branchId,
      parentId: this.activeBranchId,
      branchPoint: fromMessageIndex,
      name: name || `Branch from message ${fromMessageIndex + 1}`,
      created: new Date(),
      messages: parent.messages.slice(0, fromMessageIndex + 1)
    };

    this.branches.set(branchId, newBranch);
    return newBranch;
  }

  switchBranch(branchId: string): ConversationBranch | null {
    if (!this.branches.has(branchId)) return null;

    this.activeBranchId = branchId;
    return this.branches.get(branchId)!;
  }

  getActiveBranch(): ConversationBranch {
    return this.branches.get(this.activeBranchId)!;
  }

  getAllBranches(): ConversationBranch[] {
    return Array.from(this.branches.values());
  }

  mergeBranches(
    sourceBranchId: string,
    targetBranchId: string
  ): ConversationBranch {
    const source = this.branches.get(sourceBranchId)!;
    const target = this.branches.get(targetBranchId)!;

    // Find common ancestor
    const commonIndex = this.findCommonAncestor(source, target);

    // Merge messages after common point
    const mergedMessages = [
      ...target.messages.slice(0, commonIndex),
      ...source.messages.slice(commonIndex),
      ...target.messages.slice(commonIndex)
    ];

    target.messages = mergedMessages;
    return target;
  }

  private findCommonAncestor(
    branch1: ConversationBranch,
    branch2: ConversationBranch
  ): number {
    // Implementation to find where branches diverged
    // Returns the index of the last common message
    return 0; // Simplified
  }
}
```

### Branch Visualization

Show conversation tree structure:

```tsx
function ConversationTreeView({ tree, activeBranchId, onSwitchBranch }) {
  const branches = tree.getAllBranches();

  return (
    <div className="conversation-tree">
      <h3>Conversation Branches</h3>

      <svg width="300" height="400" className="tree-diagram">
        {/* Render tree structure */}
        {branches.map((branch, index) => (
          <g key={branch.id}>
            {/* Branch node */}
            <circle
              cx={50 + index * 60}
              cy={50 + branch.branchPoint * 20}
              r={20}
              className={branch.id === activeBranchId ? 'active' : ''}
              onClick={() => onSwitchBranch(branch.id)}
            />
            <text
              x={50 + index * 60}
              y={55 + branch.branchPoint * 20}
              textAnchor="middle"
            >
              {branch.name.substring(0, 3)}
            </text>

            {/* Connection to parent */}
            {branch.parentId && (
              <line
                x1={50 + (index - 1) * 60}
                y1={50 + branch.branchPoint * 20}
                x2={50 + index * 60}
                y2={50 + branch.branchPoint * 20}
                stroke="#ccc"
              />
            )}
          </g>
        ))}
      </svg>

      <div className="branch-list">
        {branches.map(branch => (
          <button
            key={branch.id}
            className={`branch-item ${branch.id === activeBranchId ? 'active' : ''}`}
            onClick={() => onSwitchBranch(branch.id)}
          >
            <div className="branch-name">{branch.name}</div>
            <div className="branch-meta">
              {branch.messages.length} messages •
              {formatRelativeTime(branch.created)}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

## Sliding Window Strategy

### Intelligent Message Pruning

Keep relevant context while dropping less important messages:

```tsx
class SlidingWindowManager {
  private maxTokens: number;
  private windowSize: number;
  private importance: Map<string, number> = new Map();

  constructor(maxTokens: number, windowSize: number) {
    this.maxTokens = maxTokens;
    this.windowSize = windowSize;
  }

  optimizeContext(
    messages: Message[],
    currentTokens: number
  ): Message[] {
    if (currentTokens <= this.maxTokens) {
      return messages; // No optimization needed
    }

    // Calculate importance scores
    this.calculateImportance(messages);

    // Keep system messages and recent messages
    const system = messages.filter(m => m.role === 'system');
    const recent = messages.slice(-this.windowSize);

    // Sort middle messages by importance
    const middle = messages.slice(
      system.length,
      messages.length - this.windowSize
    );

    const sortedMiddle = middle.sort((a, b) => {
      const scoreA = this.importance.get(a.id) || 0;
      const scoreB = this.importance.get(b.id) || 0;
      return scoreB - scoreA;
    });

    // Keep messages until we hit token limit
    let tokensUsed = this.countTokens([...system, ...recent]);
    const kept: Message[] = [];

    for (const msg of sortedMiddle) {
      const msgTokens = this.countTokens([msg]);
      if (tokensUsed + msgTokens <= this.maxTokens * 0.8) {
        kept.push(msg);
        tokensUsed += msgTokens;
      }
    }

    // Reconstruct conversation
    return [
      ...system,
      ...kept.sort((a, b) => a.timestamp - b.timestamp),
      ...recent
    ];
  }

  private calculateImportance(messages: Message[]) {
    messages.forEach((msg, index) => {
      let score = 0;

      // Recent messages more important
      const recency = 1 - (index / messages.length);
      score += recency * 10;

      // Longer messages might be more detailed
      score += Math.min(msg.content.length / 100, 10);

      // User messages that got long AI responses are important
      if (msg.role === 'user' && index < messages.length - 1) {
        const response = messages[index + 1];
        if (response.role === 'assistant') {
          score += Math.min(response.content.length / 200, 15);
        }
      }

      // Messages with code blocks
      if (msg.content.includes('```')) {
        score += 5;
      }

      // Messages with questions
      if (msg.content.includes('?')) {
        score += 3;
      }

      this.importance.set(msg.id, score);
    });
  }

  private countTokens(messages: Message[]): number {
    // Simplified token counting
    return messages.reduce((sum, msg) => {
      return sum + Math.ceil(msg.content.length / 4);
    }, 0);
  }
}
```

## Conversation Organization

### Folder and Tag System

Organize conversations for easy retrieval:

```tsx
interface ConversationFolder {
  id: string;
  name: string;
  color: string;
  icon: string;
  conversationIds: string[];
  created: Date;
  updated: Date;
}

interface ConversationTag {
  id: string;
  name: string;
  color: string;
}

function ConversationOrganizer({ conversations, folders, tags }) {
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);
  const [selectedTags, setSelectedTags] = useState<Set<string>>(new Set());
  const [sortBy, setSortBy] = useState<'date' | 'name' | 'length'>('date');

  const filteredConversations = useMemo(() => {
    let filtered = [...conversations];

    // Filter by folder
    if (selectedFolder) {
      const folder = folders.find(f => f.id === selectedFolder);
      if (folder) {
        filtered = filtered.filter(c =>
          folder.conversationIds.includes(c.id)
        );
      }
    }

    // Filter by tags
    if (selectedTags.size > 0) {
      filtered = filtered.filter(c =>
        c.tags?.some(tag => selectedTags.has(tag))
      );
    }

    // Sort
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return b.updated.getTime() - a.updated.getTime();
        case 'name':
          return a.title.localeCompare(b.title);
        case 'length':
          return b.messages.length - a.messages.length;
        default:
          return 0;
      }
    });

    return filtered;
  }, [conversations, selectedFolder, selectedTags, sortBy]);

  return (
    <div className="conversation-organizer">
      <div className="organizer-sidebar">
        {/* Folders */}
        <div className="folder-section">
          <h3>Folders</h3>
          <button
            className={`folder-item ${!selectedFolder ? 'active' : ''}`}
            onClick={() => setSelectedFolder(null)}
          >
            <FolderIcon /> All Conversations
          </button>
          {folders.map(folder => (
            <button
              key={folder.id}
              className={`folder-item ${selectedFolder === folder.id ? 'active' : ''}`}
              onClick={() => setSelectedFolder(folder.id)}
            >
              <span style={{ color: folder.color }}>{folder.icon}</span>
              {folder.name}
              <span className="count">
                {folder.conversationIds.length}
              </span>
            </button>
          ))}
        </div>

        {/* Tags */}
        <div className="tag-section">
          <h3>Tags</h3>
          <div className="tag-list">
            {tags.map(tag => (
              <label key={tag.id} className="tag-item">
                <input
                  type="checkbox"
                  checked={selectedTags.has(tag.id)}
                  onChange={() => {
                    setSelectedTags(prev => {
                      const next = new Set(prev);
                      if (next.has(tag.id)) {
                        next.delete(tag.id);
                      } else {
                        next.add(tag.id);
                      }
                      return next;
                    });
                  }}
                />
                <span
                  className="tag-label"
                  style={{ backgroundColor: tag.color }}
                >
                  {tag.name}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Sort */}
        <div className="sort-section">
          <h3>Sort By</h3>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
          >
            <option value="date">Last Updated</option>
            <option value="name">Name</option>
            <option value="length">Message Count</option>
          </select>
        </div>
      </div>

      <div className="conversation-list">
        {filteredConversations.map(conv => (
          <ConversationCard key={conv.id} conversation={conv} />
        ))}
      </div>
    </div>
  );
}
```

## Search & Retrieval

### Full-Text Search

Search across all conversations:

```tsx
function ConversationSearch({ conversations, onSelect }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);

  const search = useCallback(
    debounce(async (searchQuery: string) => {
      if (searchQuery.length < 2) {
        setResults([]);
        return;
      }

      setSearching(true);

      // Search in IndexedDB or backend
      const searchResults = await searchConversations(
        searchQuery,
        conversations
      );

      setResults(searchResults);
      setSearching(false);
    }, 300),
    [conversations]
  );

  useEffect(() => {
    search(query);
  }, [query, search]);

  return (
    <div className="conversation-search">
      <div className="search-input-wrapper">
        <SearchIcon />
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search conversations..."
          aria-label="Search conversations"
        />
        {searching && <Spinner size="small" />}
      </div>

      {results.length > 0 && (
        <div className="search-results">
          <div className="results-header">
            Found {results.length} matches
          </div>

          {results.map(result => (
            <button
              key={result.id}
              className="search-result"
              onClick={() => onSelect(result.conversationId, result.messageId)}
            >
              <div className="result-title">
                {result.conversationTitle}
              </div>
              <div className="result-excerpt">
                ...{highlightMatch(result.excerpt, query)}...
              </div>
              <div className="result-meta">
                {formatRelativeTime(result.timestamp)} •
                Message {result.messageIndex + 1}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

async function searchConversations(
  query: string,
  conversations: Conversation[]
): Promise<SearchResult[]> {
  const results: SearchResult[] = [];
  const queryLower = query.toLowerCase();

  for (const conv of conversations) {
    for (let i = 0; i < conv.messages.length; i++) {
      const msg = conv.messages[i];
      const content = msg.content.toLowerCase();

      if (content.includes(queryLower)) {
        // Extract excerpt around match
        const matchIndex = content.indexOf(queryLower);
        const excerptStart = Math.max(0, matchIndex - 50);
        const excerptEnd = Math.min(
          content.length,
          matchIndex + queryLower.length + 50
        );

        results.push({
          id: `${conv.id}-${msg.id}`,
          conversationId: conv.id,
          conversationTitle: conv.title,
          messageId: msg.id,
          messageIndex: i,
          excerpt: msg.content.substring(excerptStart, excerptEnd),
          timestamp: msg.timestamp,
          score: calculateRelevanceScore(msg.content, query)
        });
      }
    }
  }

  // Sort by relevance score
  return results.sort((a, b) => b.score - a.score).slice(0, 20);
}

function calculateRelevanceScore(content: string, query: string): number {
  let score = 0;
  const contentLower = content.toLowerCase();
  const queryLower = query.toLowerCase();

  // Exact match
  if (contentLower === queryLower) score += 100;

  // Word boundary match
  const wordRegex = new RegExp(`\\b${queryLower}\\b`, 'gi');
  const wordMatches = (contentLower.match(wordRegex) || []).length;
  score += wordMatches * 10;

  // Partial matches
  const partialMatches = (contentLower.match(new RegExp(queryLower, 'gi')) || []).length;
  score += partialMatches * 5;

  // Proximity to start
  const firstMatch = contentLower.indexOf(queryLower);
  if (firstMatch >= 0) {
    score += Math.max(0, 20 - (firstMatch / 10));
  }

  return score;
}

function highlightMatch(text: string, query: string): ReactNode {
  const parts = text.split(new RegExp(`(${query})`, 'gi'));
  return parts.map((part, i) =>
    part.toLowerCase() === query.toLowerCase() ? (
      <mark key={i}>{part}</mark>
    ) : (
      part
    )
  );
}
```

## Context Persistence

### Save and Restore Context

Persist conversation state across sessions:

```tsx
class ConversationPersistence {
  private db: IDBDatabase | null = null;
  private dbName = 'ai-chat-conversations';
  private version = 1;

  async initialize() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;

        // Create object stores
        if (!db.objectStoreNames.contains('conversations')) {
          const convStore = db.createObjectStore('conversations', {
            keyPath: 'id'
          });
          convStore.createIndex('updated', 'updated', { unique: false });
          convStore.createIndex('title', 'title', { unique: false });
        }

        if (!db.objectStoreNames.contains('messages')) {
          const msgStore = db.createObjectStore('messages', {
            keyPath: 'id'
          });
          msgStore.createIndex('conversationId', 'conversationId', {
            unique: false
          });
          msgStore.createIndex('timestamp', 'timestamp', { unique: false });
        }
      };
    });
  }

  async saveConversation(conversation: Conversation): Promise<void> {
    if (!this.db) await this.initialize();

    const transaction = this.db!.transaction(
      ['conversations', 'messages'],
      'readwrite'
    );

    // Save conversation metadata
    const convStore = transaction.objectStore('conversations');
    await convStore.put({
      id: conversation.id,
      title: conversation.title,
      created: conversation.created,
      updated: conversation.updated,
      metadata: conversation.metadata,
      tags: conversation.tags,
      tokenCount: conversation.tokenCount
    });

    // Save messages
    const msgStore = transaction.objectStore('messages');
    for (const message of conversation.messages) {
      await msgStore.put({
        ...message,
        conversationId: conversation.id
      });
    }

    return new Promise((resolve, reject) => {
      transaction.oncomplete = () => resolve();
      transaction.onerror = () => reject(transaction.error);
    });
  }

  async loadConversation(id: string): Promise<Conversation | null> {
    if (!this.db) await this.initialize();

    const transaction = this.db!.transaction(
      ['conversations', 'messages'],
      'readonly'
    );

    // Load conversation metadata
    const convStore = transaction.objectStore('conversations');
    const convRequest = convStore.get(id);

    const conversation = await new Promise<any>((resolve) => {
      convRequest.onsuccess = () => resolve(convRequest.result);
    });

    if (!conversation) return null;

    // Load messages
    const msgStore = transaction.objectStore('messages');
    const msgIndex = msgStore.index('conversationId');
    const msgRequest = msgIndex.getAll(id);

    const messages = await new Promise<Message[]>((resolve) => {
      msgRequest.onsuccess = () => resolve(msgRequest.result);
    });

    return {
      ...conversation,
      messages: messages.sort((a, b) => a.timestamp - b.timestamp)
    };
  }

  async deleteConversation(id: string): Promise<void> {
    if (!this.db) await this.initialize();

    const transaction = this.db!.transaction(
      ['conversations', 'messages'],
      'readwrite'
    );

    // Delete conversation
    const convStore = transaction.objectStore('conversations');
    await convStore.delete(id);

    // Delete messages
    const msgStore = transaction.objectStore('messages');
    const msgIndex = msgStore.index('conversationId');
    const msgRequest = msgIndex.getAllKeys(id);

    const messageIds = await new Promise<IDBValidKey[]>((resolve) => {
      msgRequest.onsuccess = () => resolve(msgRequest.result);
    });

    for (const msgId of messageIds) {
      await msgStore.delete(msgId);
    }
  }

  async exportConversation(
    id: string,
    format: 'json' | 'markdown' | 'pdf'
  ): Promise<Blob> {
    const conversation = await this.loadConversation(id);
    if (!conversation) throw new Error('Conversation not found');

    switch (format) {
      case 'json':
        return new Blob(
          [JSON.stringify(conversation, null, 2)],
          { type: 'application/json' }
        );

      case 'markdown':
        const markdown = this.convertToMarkdown(conversation);
        return new Blob([markdown], { type: 'text/markdown' });

      case 'pdf':
        // Use a library like jsPDF
        const pdf = await this.convertToPDF(conversation);
        return pdf;

      default:
        throw new Error(`Unknown format: ${format}`);
    }
  }

  private convertToMarkdown(conversation: Conversation): string {
    let markdown = `# ${conversation.title}\n\n`;
    markdown += `*Created: ${conversation.created.toLocaleString()}*\n\n`;

    for (const msg of conversation.messages) {
      markdown += `## ${msg.role.toUpperCase()}\n`;
      markdown += `*${msg.timestamp.toLocaleString()}*\n\n`;
      markdown += `${msg.content}\n\n`;
      markdown += '---\n\n';
    }

    return markdown;
  }

  private async convertToPDF(conversation: Conversation): Promise<Blob> {
    // Implementation using jsPDF or similar
    // Simplified for example
    const content = this.convertToMarkdown(conversation);
    return new Blob([content], { type: 'application/pdf' });
  }
}
```

## Best Practices Summary

1. **Make tokens understandable** - Use pages/messages, not token counts
2. **Warn progressively** - Alert at 80%, 90%, 95% thresholds
3. **Offer clear actions** - Summarize, export, or start new
4. **Let users control** - Pin important messages, choose what to keep
5. **Support branching** - Non-linear conversations are powerful
6. **Implement smart pruning** - Keep important context, drop filler
7. **Organize effectively** - Folders, tags, search are essential
8. **Persist everything** - Use IndexedDB for offline support
9. **Export options** - JSON, Markdown, PDF for different needs
10. **Visualize structure** - Show conversation trees and context usage