# Presence Patterns Reference Guide

Real-time awareness of other users: online status, cursors, selections, typing indicators.


## Table of Contents

- [What is Presence?](#what-is-presence)
- [Yjs Awareness API](#yjs-awareness-api)
  - [Basic Setup](#basic-setup)
  - [User State Structure](#user-state-structure)
  - [Tracking Users](#tracking-users)
  - [Listening for Changes](#listening-for-changes)
  - [Cleanup on Page Unload](#cleanup-on-page-unload)
- [Cursor Tracking](#cursor-tracking)
  - [Mouse Cursor Position](#mouse-cursor-position)
  - [Text Cursor Position](#text-cursor-position)
- [Selection Tracking](#selection-tracking)
- [Typing Indicator](#typing-indicator)
- [Active View Tracking](#active-view-tracking)
- [Last Seen Timestamp](#last-seen-timestamp)
- [User Avatar List](#user-avatar-list)
- [Focus Indicator](#focus-indicator)
- [Performance Optimization](#performance-optimization)
  - [Throttling Updates](#throttling-updates)
  - [Debouncing Typing Indicator](#debouncing-typing-indicator)
  - [Cleanup Stale State](#cleanup-stale-state)
- [Best Practices](#best-practices)

## What is Presence?

Presence provides awareness of other users in collaborative applications:

- **Who's online** - Active users list
- **Cursor positions** - Where others are editing
- **Selections** - What others have selected
- **Typing indicators** - Who's currently typing
- **Active view** - What page/document others are viewing

**Key Characteristics:**
- **Ephemeral** - Not persisted (unlike CRDT document state)
- **Fast updates** - High-frequency position changes
- **Eventually consistent** - Can tolerate temporary inconsistency

## Yjs Awareness API

Yjs includes built-in presence via Awareness API.

### Basic Setup

```typescript
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'

const doc = new Y.Doc()
const provider = new WebsocketProvider('ws://localhost:1234', 'doc-id', doc)

// Awareness automatically created by provider
const awareness = provider.awareness

// Get local client ID
const localClientId = awareness.clientID

// Set local state
awareness.setLocalState({
  user: {
    name: 'Alice',
    email: 'alice@example.com',
    color: '#FF5733',
    avatar: 'https://example.com/alice.jpg'
  },
  cursor: null,  // null when not active
  selection: null
})
```

### User State Structure

```typescript
interface UserState {
  user: {
    name: string
    email?: string
    color: string  // For cursor/avatar rendering
    avatar?: string
  }
  cursor?: {
    x: number
    y: number
    // Or for text:
    anchor: number  // Cursor position in document
    head: number    // Selection end (anchor === head if no selection)
  }
  selection?: {
    ranges: Array<{ from: number; to: number }>
  }
  typing?: boolean
  lastSeen?: number  // Timestamp
}
```

### Tracking Users

```typescript
// Get all connected users
const users = Array.from(awareness.getStates().entries())
  .filter(([clientId]) => clientId !== awareness.clientID)
  .map(([clientId, state]) => ({
    id: clientId,
    ...state
  }))

console.log(`${users.length} other users online`)

// Get specific user
const userId = 123
const userState = awareness.getStates().get(userId)
if (userState) {
  console.log(`${userState.user.name} is online`)
}
```

### Listening for Changes

```typescript
awareness.on('change', (changes: {
  added: number[]    // New users
  updated: number[]  // State changed
  removed: number[]  // Users left
}) => {
  // Handle new users
  changes.added.forEach(clientId => {
    const state = awareness.getStates().get(clientId)
    console.log(`${state.user.name} joined`)
    showNotification(`${state.user.name} joined the document`)
  })

  // Handle updates (cursor moved, typing status, etc.)
  changes.updated.forEach(clientId => {
    const state = awareness.getStates().get(clientId)
    updateCursor(clientId, state.cursor)
    updateTypingIndicator(clientId, state.typing)
  })

  // Handle users leaving
  changes.removed.forEach(clientId => {
    console.log(`User ${clientId} left`)
    removeCursor(clientId)
  })
})
```

### Cleanup on Page Unload

```typescript
window.addEventListener('beforeunload', () => {
  // Clear local state (notifies others you're leaving)
  awareness.setLocalState(null)
})

// Or destroy awareness entirely
window.addEventListener('beforeunload', () => {
  awareness.destroy()
})
```

## Cursor Tracking

### Mouse Cursor Position

Track mouse position and broadcast to others.

**Tracking:**
```typescript
import throttle from 'lodash.throttle'

const awareness = provider.awareness

// Throttle cursor updates to 60 FPS (16ms)
const updateCursor = throttle((event: MouseEvent) => {
  const state = awareness.getLocalState()

  awareness.setLocalState({
    ...state,
    cursor: {
      x: event.clientX,
      y: event.clientY
    }
  })
}, 16)

document.addEventListener('mousemove', updateCursor)

// Clear cursor when mouse leaves
document.addEventListener('mouseleave', () => {
  const state = awareness.getLocalState()
  awareness.setLocalState({
    ...state,
    cursor: null
  })
})
```

**Rendering:**
```typescript
function renderCursors() {
  const cursorsContainer = document.getElementById('cursors')
  cursorsContainer.innerHTML = ''

  awareness.getStates().forEach((state, clientId) => {
    // Skip own cursor
    if (clientId === awareness.clientID) return

    // Skip if no cursor position
    if (!state.cursor) return

    const cursor = document.createElement('div')
    cursor.className = 'remote-cursor'
    cursor.style.position = 'absolute'
    cursor.style.left = `${state.cursor.x}px`
    cursor.style.top = `${state.cursor.y}px`
    cursor.style.pointerEvents = 'none'

    // Cursor shape
    cursor.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24">
        <path d="M5.65376 12.3673H5.46026L5.31717 12.4976L0.500002 16.8829L0.500002 1.19841L11.7841 12.3673H5.65376Z"
              fill="${state.user.color}"/>
      </svg>
      <div class="cursor-label" style="background: ${state.user.color}">
        ${state.user.name}
      </div>
    `

    cursorsContainer.appendChild(cursor)
  })
}

awareness.on('change', renderCursors)
```

**CSS:**
```css
.remote-cursor {
  position: absolute;
  z-index: 9999;
  pointer-events: none;
  transition: left 0.1s ease-out, top 0.1s ease-out;
}

.cursor-label {
  position: absolute;
  left: 20px;
  top: 0;
  padding: 2px 6px;
  border-radius: 3px;
  color: white;
  font-size: 12px;
  white-space: nowrap;
}
```

### Text Cursor Position

Track cursor in text editor (ProseMirror, Monaco, CodeMirror).

**ProseMirror Integration:**
```typescript
import { yCursorPlugin } from 'y-prosemirror'
import { EditorState } from 'prosemirror-state'

const state = EditorState.create({
  schema,
  plugins: [
    ySyncPlugin(yXmlFragment),
    yCursorPlugin(provider.awareness, {
      cursorBuilder: (user) => {
        const cursor = document.createElement('span')
        cursor.className = 'remote-cursor'
        cursor.style.borderLeft = `2px solid ${user.color}`
        return cursor
      },
      selectionBuilder: (user) => {
        return {
          style: `background-color: ${user.color}30`,  // 30 = 20% opacity
          class: 'remote-selection'
        }
      }
    })
  ]
})
```

**Monaco Integration:**
```typescript
import * as monaco from 'monaco-editor'
import { MonacoBinding } from 'y-monaco'

const editor = monaco.editor.create(document.getElementById('editor'), {
  value: '',
  language: 'typescript'
})

const ytext = doc.getText('monaco')

const binding = new MonacoBinding(
  ytext,
  editor.getModel(),
  new Set([editor]),
  provider.awareness
)

// Cursors and selections automatically rendered
```

## Selection Tracking

Track text selection ranges.

```typescript
document.addEventListener('selectionchange', throttle(() => {
  const selection = window.getSelection()

  if (!selection || selection.rangeCount === 0) {
    awareness.setLocalState({
      ...awareness.getLocalState(),
      selection: null
    })
    return
  }

  const range = selection.getRangeAt(0)

  awareness.setLocalState({
    ...awareness.getLocalState(),
    selection: {
      ranges: [{
        from: range.startOffset,
        to: range.endOffset
      }]
    }
  })
}, 100))
```

**Render Selections:**
```typescript
function renderSelections() {
  // Remove old selections
  document.querySelectorAll('.remote-selection').forEach(el => el.remove())

  awareness.getStates().forEach((state, clientId) => {
    if (clientId === awareness.clientID) return
    if (!state.selection) return

    state.selection.ranges.forEach(range => {
      const span = document.createElement('span')
      span.className = 'remote-selection'
      span.style.backgroundColor = `${state.user.color}30`

      // Position span over selected text
      // (Implementation depends on text editor)
    })
  })
}
```

## Typing Indicator

Show when users are typing.

**Tracking:**
```typescript
let typingTimeout: NodeJS.Timeout | null = null

const textarea = document.getElementById('message-input') as HTMLTextAreaElement

textarea.addEventListener('input', () => {
  // Set typing = true
  awareness.setLocalState({
    ...awareness.getLocalState(),
    typing: true
  })

  // Clear after 1 second of no input
  if (typingTimeout) clearTimeout(typingTimeout)

  typingTimeout = setTimeout(() => {
    awareness.setLocalState({
      ...awareness.getLocalState(),
      typing: false
    })
  }, 1000)
})

textarea.addEventListener('blur', () => {
  awareness.setLocalState({
    ...awareness.getLocalState(),
    typing: false
  })
})
```

**Rendering:**
```typescript
function renderTypingIndicators() {
  const typingUsers = Array.from(awareness.getStates().entries())
    .filter(([clientId, state]) =>
      clientId !== awareness.clientID && state.typing
    )
    .map(([, state]) => state.user.name)

  const indicator = document.getElementById('typing-indicator')

  if (typingUsers.length === 0) {
    indicator.textContent = ''
  } else if (typingUsers.length === 1) {
    indicator.textContent = `${typingUsers[0]} is typing...`
  } else if (typingUsers.length === 2) {
    indicator.textContent = `${typingUsers[0]} and ${typingUsers[1]} are typing...`
  } else {
    indicator.textContent = `${typingUsers[0]}, ${typingUsers[1]}, and ${typingUsers.length - 2} others are typing...`
  }
}

awareness.on('change', renderTypingIndicators)
```

## Active View Tracking

Track which page/section users are viewing.

```typescript
// Update when route changes
router.afterEach((to) => {
  awareness.setLocalState({
    ...awareness.getLocalState(),
    activeView: {
      path: to.path,
      title: to.meta.title
    }
  })
})

// Show users on same page
function getUsersOnSamePage(currentPath: string) {
  return Array.from(awareness.getStates().entries())
    .filter(([clientId, state]) =>
      clientId !== awareness.clientID &&
      state.activeView?.path === currentPath
    )
    .map(([, state]) => state.user)
}

// Render user list
function renderUsersHere() {
  const users = getUsersOnSamePage(window.location.pathname)

  const list = document.getElementById('users-here')
  list.innerHTML = users.map(user => `
    <div class="user-badge">
      <img src="${user.avatar}" alt="${user.name}" />
      <span>${user.name}</span>
    </div>
  `).join('')
}

awareness.on('change', renderUsersHere)
```

## Last Seen Timestamp

Track when users were last active.

```typescript
// Update on any interaction
function updateLastSeen() {
  awareness.setLocalState({
    ...awareness.getLocalState(),
    lastSeen: Date.now()
  })
}

document.addEventListener('mousemove', throttle(updateLastSeen, 5000))
document.addEventListener('keydown', throttle(updateLastSeen, 5000))

// Show inactive users
function getInactiveUsers(thresholdMs: number = 60000) {
  const now = Date.now()

  return Array.from(awareness.getStates().entries())
    .filter(([clientId, state]) =>
      clientId !== awareness.clientID &&
      state.lastSeen &&
      now - state.lastSeen > thresholdMs
    )
    .map(([, state]) => state.user)
}

// Mark inactive users with visual cue
setInterval(() => {
  const inactiveUsers = getInactiveUsers()

  inactiveUsers.forEach(user => {
    const element = document.getElementById(`user-${user.email}`)
    if (element) {
      element.classList.add('inactive')
    }
  })
}, 10000)
```

## User Avatar List

Display all online users with avatars.

```typescript
function renderUserList() {
  const container = document.getElementById('user-list')

  const users = Array.from(awareness.getStates().entries())
    .map(([clientId, state]) => ({
      id: clientId,
      isMe: clientId === awareness.clientID,
      ...state.user,
      lastSeen: state.lastSeen
    }))
    .sort((a, b) => {
      // Sort: active first, then by name
      const aActive = Date.now() - (a.lastSeen || 0) < 60000
      const bActive = Date.now() - (b.lastSeen || 0) < 60000

      if (aActive && !bActive) return -1
      if (!aActive && bActive) return 1

      return a.name.localeCompare(b.name)
    })

  container.innerHTML = users.map(user => `
    <div class="user-item ${user.isMe ? 'me' : ''}">
      <div class="avatar" style="border-color: ${user.color}">
        <img src="${user.avatar}" alt="${user.name}" />
        ${isUserActive(user) ? '<div class="status-dot"></div>' : ''}
      </div>
      <div class="user-info">
        <div class="name">${user.name} ${user.isMe ? '(you)' : ''}</div>
        <div class="email">${user.email}</div>
      </div>
    </div>
  `).join('')
}

function isUserActive(user: { lastSeen?: number }): boolean {
  if (!user.lastSeen) return false
  return Date.now() - user.lastSeen < 60000  // Active within 1 minute
}

awareness.on('change', renderUserList)
```

**CSS:**
```css
.user-item {
  display: flex;
  align-items: center;
  padding: 8px;
  border-radius: 4px;
}

.user-item.me {
  background: #f0f0f0;
}

.avatar {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid transparent;
}

.avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 12px;
  height: 12px;
  background: #00cc00;
  border: 2px solid white;
  border-radius: 50%;
}

.user-info {
  margin-left: 12px;
}

.name {
  font-weight: 500;
}

.email {
  font-size: 12px;
  color: #666;
}
```

## Focus Indicator

Show which element/field users are focused on.

```typescript
document.addEventListener('focusin', (event) => {
  const target = event.target as HTMLElement

  awareness.setLocalState({
    ...awareness.getLocalState(),
    focus: {
      elementId: target.id,
      elementType: target.tagName,
      label: target.getAttribute('aria-label') || target.getAttribute('name')
    }
  })
})

document.addEventListener('focusout', () => {
  awareness.setLocalState({
    ...awareness.getLocalState(),
    focus: null
  })
})

// Show who's editing what field
function renderFieldOccupancy() {
  document.querySelectorAll('input, textarea').forEach(element => {
    const id = element.id

    const occupants = Array.from(awareness.getStates().entries())
      .filter(([clientId, state]) =>
        clientId !== awareness.clientID &&
        state.focus?.elementId === id
      )
      .map(([, state]) => state.user)

    if (occupants.length > 0) {
      // Show indicator
      const indicator = document.createElement('div')
      indicator.className = 'field-occupant'
      indicator.textContent = occupants.map(u => u.name).join(', ')
      indicator.style.color = occupants[0].color
      element.parentElement?.appendChild(indicator)
    }
  })
}

awareness.on('change', renderFieldOccupancy)
```

## Performance Optimization

### Throttling Updates

Don't send awareness updates on every pixel movement.

```typescript
import throttle from 'lodash.throttle'

// 60 FPS = ~16ms
const updateCursor = throttle((x: number, y: number) => {
  awareness.setLocalState({
    ...awareness.getLocalState(),
    cursor: { x, y }
  })
}, 16)

// Or 30 FPS = ~33ms for less network traffic
const updateCursorSlow = throttle(updateCursor, 33)
```

### Debouncing Typing Indicator

```typescript
import debounce from 'lodash.debounce'

const stopTyping = debounce(() => {
  awareness.setLocalState({
    ...awareness.getLocalState(),
    typing: false
  })
}, 1000)

textarea.addEventListener('input', () => {
  awareness.setLocalState({
    ...awareness.getLocalState(),
    typing: true
  })

  stopTyping()
})
```

### Cleanup Stale State

Remove old state to prevent memory leaks.

```typescript
// Clean up users inactive for >5 minutes
setInterval(() => {
  const now = Date.now()
  const threshold = 5 * 60 * 1000  // 5 minutes

  awareness.getStates().forEach((state, clientId) => {
    if (state.lastSeen && now - state.lastSeen > threshold) {
      // Manually remove stale state
      awareness.states.delete(clientId)
      awareness.emit('change', {
        added: [],
        updated: [],
        removed: [clientId]
      })
    }
  })
}, 60000)  // Check every minute
```

## Best Practices

1. **Throttle frequent updates** - Cursor movements, scrolling (16-33ms)
2. **Debounce typing indicators** - Stop typing after 1 second of inactivity
3. **Include last seen timestamp** - Track user activity
4. **Clear state on page unload** - Notify others when leaving
5. **Show inactive users differently** - Visual cue after 1+ minute
6. **Limit awareness data size** - Don't include large objects
7. **Use color coding** - Assign each user a distinct color
8. **Render cursors efficiently** - Use CSS transforms, not DOM manipulation
9. **Test with many users** - Ensure performance with 50+ users
10. **Provide privacy controls** - Let users hide their presence
