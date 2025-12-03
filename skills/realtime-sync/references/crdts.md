# CRDTs (Conflict-Free Replicated Data Types) Reference Guide

CRDTs enable conflict-free collaborative editing across distributed systems.

## The Collaboration Problem

**Traditional Operational Transform (OT):**
```
User A at position 5: Insert "hello"
User B at position 5: Insert "world" (simultaneously)

Server must choose:
- Transform A's operation relative to B's? "worldhello"
- Transform B's operation relative to A's? "helloworld"
- Error and ask user to retry?

Problems:
- Complex transformation functions
- Central server required
- Race conditions
- Order-dependent
```

**CRDT Solution:**
```
User A: Insert "hello" with unique ID A1
User B: Insert "world" with unique ID B1

Merge rule: Sort by ID
Result: Deterministic (always "helloworld" if A1 < B1)

Benefits:
- No central server needed
- Eventually consistent
- Order-independent
- Commutative and associative
```

## CRDT Types

### G-Counter (Grow-Only Counter)

Each replica maintains its own counter. Total is sum of all replicas.

```typescript
class GCounter {
  private counts = new Map<string, number>()

  increment(replicaId: string, amount: number = 1) {
    const current = this.counts.get(replicaId) || 0
    this.counts.set(replicaId, current + amount)
  }

  value(): number {
    return Array.from(this.counts.values()).reduce((a, b) => a + b, 0)
  }

  merge(other: GCounter) {
    for (const [id, count] of other.counts) {
      const current = this.counts.get(id) || 0
      this.counts.set(id, Math.max(current, count))
    }
  }
}

// Usage
const counter1 = new GCounter()
counter1.increment('replica1', 5)

const counter2 = new GCounter()
counter2.increment('replica2', 3)

counter1.merge(counter2)
console.log(counter1.value())  // 8 (5 + 3)
```

### LWW-Register (Last-Write-Wins)

Store value with timestamp. Latest timestamp wins on merge.

```typescript
class LWWRegister<T> {
  private value: T
  private timestamp: number

  set(value: T, timestamp: number = Date.now()) {
    if (timestamp > this.timestamp) {
      this.value = value
      this.timestamp = timestamp
    }
  }

  get(): T {
    return this.value
  }

  merge(other: LWWRegister<T>) {
    if (other.timestamp > this.timestamp) {
      this.value = other.value
      this.timestamp = other.timestamp
    }
  }
}
```

### OR-Set (Observed-Remove Set)

Add and remove elements with unique IDs.

```typescript
type ElementId = string

class ORSet<T> {
  private elements = new Map<T, Set<ElementId>>()
  private tombstones = new Map<T, Set<ElementId>>()

  add(element: T, elementId: ElementId = crypto.randomUUID()) {
    if (!this.elements.has(element)) {
      this.elements.set(element, new Set())
    }
    this.elements.get(element)!.add(elementId)
  }

  remove(element: T) {
    const ids = this.elements.get(element)
    if (ids) {
      if (!this.tombstones.has(element)) {
        this.tombstones.set(element, new Set())
      }
      ids.forEach(id => this.tombstones.get(element)!.add(id))
    }
  }

  has(element: T): boolean {
    const ids = this.elements.get(element)
    const removed = this.tombstones.get(element)

    if (!ids) return false
    if (!removed) return ids.size > 0

    // Element exists if any ID not in tombstones
    return Array.from(ids).some(id => !removed.has(id))
  }

  merge(other: ORSet<T>) {
    // Merge elements
    for (const [element, ids] of other.elements) {
      if (!this.elements.has(element)) {
        this.elements.set(element, new Set())
      }
      ids.forEach(id => this.elements.get(element)!.add(id))
    }

    // Merge tombstones
    for (const [element, ids] of other.tombstones) {
      if (!this.tombstones.has(element)) {
        this.tombstones.set(element, new Set())
      }
      ids.forEach(id => this.tombstones.get(element)!.add(id))
    }
  }
}
```

## Yjs - Production CRDT Library

Yjs is the most mature CRDT library for collaborative editing.

### Architecture

```
┌─────────────────────────────────────────┐
│         Yjs Document (Y.Doc)            │
│  ┌──────────────────────────────────┐   │
│  │  Shared Types                     │   │
│  │  - Y.Text    (collaborative text) │   │
│  │  - Y.Array   (collaborative list) │   │
│  │  - Y.Map     (collaborative map)  │   │
│  │  - Y.XmlFragment (rich text)      │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │  Providers (Network Layer)        │   │
│  │  - y-websocket (WebSocket sync)   │   │
│  │  - y-webrtc    (P2P sync)         │   │
│  │  - y-indexeddb (local storage)    │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Basic Usage

```typescript
import * as Y from 'yjs'

// Create shared document
const doc = new Y.Doc()

// Shared text
const ytext = doc.getText('content')

// Insert text
ytext.insert(0, 'Hello ')
ytext.insert(6, 'world!')

console.log(ytext.toString())  // "Hello world!"

// Listen for changes
ytext.observe(event => {
  event.changes.delta.forEach(change => {
    if (change.insert) {
      console.log('Inserted:', change.insert)
    }
    if (change.delete) {
      console.log('Deleted:', change.delete, 'characters')
    }
  })
})
```

### Network Sync with y-websocket

```typescript
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'

const doc = new Y.Doc()

// WebSocket provider connects to server
const provider = new WebsocketProvider(
  'ws://localhost:1234',           // WebSocket server
  'my-document-id',                // Document ID (room)
  doc,                             // Yjs document
  { connect: true }                // Auto-connect
)

// Provider events
provider.on('status', (event) => {
  console.log('Connection status:', event.status)  // 'connected' | 'disconnected'
})

provider.on('sync', (isSynced) => {
  console.log('Synced with server:', isSynced)
})

// Shared text
const ytext = doc.getText('content')

// Changes automatically sync to all connected peers
ytext.insert(0, 'This syncs across all users!')
```

### Backend (y-sweet server)

Yjs WebSocket server in Rust for production deployments.

**Run y-sweet:**
```bash
# Via npx
npx y-sweet serve

# Via Docker
docker run -p 1234:1234 ysweet/y-sweet

# With persistence
docker run -p 1234:1234 -v $(pwd)/data:/data ysweet/y-sweet
```

**Environment configuration:**
```bash
# .env
YSWEETD_HOST=0.0.0.0
YSWEETD_PORT=1234
YSWEETD_DATA_DIR=/data
YSWEETD_AUTH=none  # or 'token' for authentication
```

### Local Persistence (IndexedDB)

Store document offline for PWA/mobile apps.

```typescript
import * as Y from 'yjs'
import { IndexeddbPersistence } from 'y-indexeddb'
import { WebsocketProvider } from 'y-websocket'

const doc = new Y.Doc()

// Local persistence first
const indexeddbProvider = new IndexeddbPersistence('my-doc', doc)

indexeddbProvider.on('synced', () => {
  console.log('Loaded from IndexedDB')
})

// Then connect to server (syncs changes)
const wsProvider = new WebsocketProvider(
  'wss://api.example.com/sync',
  'my-doc',
  doc
)

// Workflow:
// 1. Load from IndexedDB (instant)
// 2. Connect to server (background)
// 3. Sync differences (automatic)
// 4. All changes saved to IndexedDB + server
```

### Rich Text Editing

Integrate with ProseMirror, Monaco, CodeMirror, or Quill.

**Quill Integration:**
```typescript
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'
import { QuillBinding } from 'y-quill'
import Quill from 'quill'

const doc = new Y.Doc()
const ytext = doc.getText('quill')

const provider = new WebsocketProvider('ws://localhost:1234', 'quill-doc', doc)

// Initialize Quill
const quill = new Quill('#editor', {
  theme: 'snow',
  modules: { toolbar: [['bold', 'italic', 'underline']] }
})

// Bind Yjs to Quill
const binding = new QuillBinding(ytext, quill, provider.awareness)

// Now multiple users can edit the same document!
```

**ProseMirror Integration:**
```typescript
import { ySyncPlugin, yCursorPlugin, yUndoPlugin } from 'y-prosemirror'
import { EditorState } from 'prosemirror-state'
import { EditorView } from 'prosemirror-view'

const yXmlFragment = doc.getXmlFragment('prosemirror')

const state = EditorState.create({
  schema,
  plugins: [
    ySyncPlugin(yXmlFragment),
    yCursorPlugin(provider.awareness),
    yUndoPlugin(),
  ]
})

const view = new EditorView(document.querySelector('#editor'), { state })
```

### Awareness (Presence)

Track online users, cursor positions, selections.

```typescript
import { WebsocketProvider } from 'y-websocket'

const provider = new WebsocketProvider('ws://localhost:1234', 'doc', doc)
const awareness = provider.awareness

// Set local state
awareness.setLocalState({
  user: {
    name: 'Alice',
    color: '#FF5733',
    avatar: 'https://...'
  },
  cursor: {
    anchor: 10,
    head: 15
  }
})

// Get all connected users
awareness.getStates().forEach((state, clientId) => {
  console.log(`User ${state.user.name} is at position ${state.cursor.anchor}`)
})

// Listen for changes
awareness.on('change', (changes) => {
  // changes.added: Array<clientId> (new users)
  // changes.updated: Array<clientId> (state changed)
  // changes.removed: Array<clientId> (users left)

  changes.added.forEach(clientId => {
    const state = awareness.getStates().get(clientId)
    console.log(`${state.user.name} joined`)
  })

  changes.updated.forEach(clientId => {
    const state = awareness.getStates().get(clientId)
    console.log(`${state.user.name} moved cursor`)
  })

  changes.removed.forEach(clientId => {
    console.log(`User ${clientId} left`)
  })
})
```

### Cursor Rendering

```typescript
function renderCursors(awareness: Awareness) {
  const cursors = document.getElementById('cursors')
  cursors.innerHTML = ''

  awareness.getStates().forEach((state, clientId) => {
    if (clientId === awareness.clientID) return  // Skip self

    const cursor = document.createElement('div')
    cursor.className = 'remote-cursor'
    cursor.style.left = `${state.cursor.x}px`
    cursor.style.top = `${state.cursor.y}px`
    cursor.style.backgroundColor = state.user.color

    const label = document.createElement('span')
    label.textContent = state.user.name
    cursor.appendChild(label)

    cursors.appendChild(cursor)
  })
}

awareness.on('change', () => renderCursors(awareness))
```

## Automerge - Alternative CRDT

Automerge is Rust-first CRDT for JSON-like data structures.

### When to Use Automerge

- Need full Rust implementation (Yjs is TypeScript-first)
- JSON-like data structures (not just text)
- Time-travel / history playback
- Local-first architecture

### Basic Usage (Rust)

```rust
use automerge::{AutoCommit, transaction::Transactable, ObjType, ROOT};

fn main() {
    let mut doc = AutoCommit::new();

    // Create a map
    let mut tx = doc.transaction();
    let map = tx.put_object(ROOT, "notes", ObjType::Map).unwrap();

    // Add properties
    tx.put(&map, "title", "Meeting Notes").unwrap();
    tx.put(&map, "date", "2025-12-02").unwrap();

    // Create nested list
    let list = tx.put_object(&map, "items", ObjType::List).unwrap();
    tx.insert(&list, 0, "Item 1").unwrap();
    tx.insert(&list, 1, "Item 2").unwrap();

    tx.commit();

    // Generate binary update (send over network)
    let changes = doc.get_changes(&[]).unwrap();

    // Other peer can apply changes
    // doc2.apply_changes(changes).unwrap();
}
```

### Network Sync (Rust)

```rust
use automerge::{AutoCommit, sync};

// Peer A
let mut doc1 = AutoCommit::new();
let mut sync_state1 = sync::State::new();

// Peer B
let mut doc2 = AutoCommit::new();
let mut sync_state2 = sync::State::new();

// Peer A generates sync message
let message = doc1.sync().generate_sync_message(&mut sync_state1);

// Send message to Peer B (over WebSocket, HTTP, etc.)
// ...

// Peer B receives and applies
doc2.sync().receive_sync_message(&mut sync_state2, message).unwrap();

// Both docs are now in sync
```

### TypeScript (via WASM)

```typescript
import * as Automerge from '@automerge/automerge'

let doc = Automerge.init()

doc = Automerge.change(doc, 'Add data', doc => {
  doc.notes = { title: 'Meeting Notes', items: [] }
  doc.notes.items.push('Item 1')
  doc.notes.items.push('Item 2')
})

// Generate changes
const changes = Automerge.getChanges(Automerge.init(), doc)

// Apply to another doc
let doc2 = Automerge.init()
doc2 = Automerge.applyChanges(doc2, changes)

console.log(doc2.notes.title)  // "Meeting Notes"
```

## Yjs vs Automerge Comparison

| Feature | Yjs | Automerge |
|---------|-----|-----------|
| **Language** | TypeScript (Rust WASM in progress) | Rust (TypeScript WASM bindings) |
| **Best For** | Text editing, rich text | JSON-like data structures |
| **Performance** | Faster for text operations | Slower but more flexible |
| **Ecosystem** | Mature (ProseMirror, Monaco, Quill) | Growing (still maturing) |
| **Network** | y-websocket, y-webrtc | DIY sync protocol |
| **Persistence** | y-indexeddb | DIY storage |
| **Awareness** | Built-in (y-protocols) | Manual implementation |
| **Time Travel** | No built-in support | First-class feature |
| **Binary Format** | Custom (efficient) | Custom (flexible) |
| **Bundle Size** | ~60KB | ~200KB |

**Recommendation:**
- **Use Yjs** for collaborative text editing (documents, code, spreadsheets)
- **Use Automerge** for JSON data structures with history/time-travel

## Conflict Resolution Strategies

### Merge Strategy

Both Yjs and Automerge use deterministic merge rules:

**Text (Yjs):**
- Each character has unique position ID
- Merge based on ID ordering
- Always produces same result regardless of order

**Lists (Automerge):**
- Each list insertion has unique ID
- Concurrent insertions at same position are ordered by ID
- Deletions are tombstones (preserved for sync)

**Maps:**
- Last-write-wins with vector clock timestamps
- Concurrent updates to same key: highest timestamp wins

### Custom Conflict Resolution

For application-specific logic, wrap CRDT operations:

```typescript
// Example: Conflict-free task priority
class TaskList {
  private yarray: Y.Array<any>

  constructor(doc: Y.Doc) {
    this.yarray = doc.getArray('tasks')
  }

  addTask(task: Task) {
    // Generate unique ID for deterministic ordering
    task.id = `${task.priority}_${Date.now()}_${Math.random()}`
    this.yarray.push([task])
  }

  getTasks(): Task[] {
    // Sort by priority (deterministic)
    return this.yarray.toArray().sort((a, b) => {
      return b.priority - a.priority || a.id.localeCompare(b.id)
    })
  }
}
```

## Best Practices

1. **Use Yjs for text editing** - Most mature, best ecosystem
2. **Use Automerge for JSON data** - Better for structured data
3. **Always include awareness** - Track online users and cursors
4. **Enable local persistence** - IndexedDB for offline support
5. **Test conflict scenarios** - Simulate simultaneous edits
6. **Monitor CRDT size** - Garbage collect tombstones periodically
7. **Use binary encoding** - Smaller than JSON for network sync
8. **Version your schema** - Plan for data structure changes
9. **Implement heartbeat** - Detect disconnected users
10. **Test with poor networks** - Ensure sync works with delays
