# Skill Chain: AI Chat Interface

**Themed conversational AI interface with form inputs**

Status: 🚧 Future (Requires: ai-chat skill) - STRATEGIC PRIORITY 🚀

---

## Overview

**Chain:** `design-tokens` → `ai-chat` + `forms`

**Purpose:** Build production-ready AI chat interfaces with consistent theming, form inputs, and accessibility

**Use Cases:**
- Customer support chatbots
- AI assistants (like ChatGPT, Claude)
- Conversational forms
- Interactive AI tools
- Virtual assistants

---

## Strategic Importance

### Why This is a Priority Chain

**1. Market Timing (2025)**
- Every app is adding AI features
- No established UI patterns yet
- Emerging market opportunity

**2. Meta-Advantage**
- Building AI chat interfaces WITH Claude
- Claude understands chat UX better than anyone
- First-mover advantage on patterns

**3. High Business Value**
- Universal demand (chatbots everywhere)
- Competitive differentiator
- Premium feature set

**4. Unique Position**
- Claude skills for building Claude-like interfaces
- Self-referential opportunity
- Can demonstrate with Claude itself

---

## Chain Architecture

### Pattern: Hub-and-Spoke

```
    design-tokens (HUB)
          ↓
      ┌───┴───┐
      ↓       ↓
   ai-chat  forms
      ↓       ↓
   Chat UI  Inputs
      └───┬───┘
          ↓
  AI Interface
```

**Coordination:**
- design-tokens: Message bubbles, input styling, loading states
- ai-chat: Conversation logic, message display, streaming responses
- forms: Input controls, send button, file upload

---

## Expected User Request

> "Build a chat interface like ChatGPT with message history, streaming responses, and file upload support"

---

## Expected Token Integration

### Chat Message Tokens (design-tokens)

**Future tokens in:** `tokens/components/chat.json`

```json
{
  "chat": {
    "message": {
      "bg-user": {
        "$value": "{semantic.color.primary}",
        "$type": "color",
        "$description": "User message background"
      },
      "bg-assistant": {
        "$value": "{semantic.color.bg-secondary}",
        "$type": "color"
      },
      "text-user": {
        "$value": "{semantic.color.text-inverse}",
        "$type": "color"
      },
      "text-assistant": {
        "$value": "{semantic.color.text-primary}",
        "$type": "color"
      },
      "padding-inline": {
        "$value": "{semantic.spacing.md}",
        "$type": "dimension"
      },
      "padding-block": {
        "$value": "{semantic.spacing.sm}",
        "$type": "dimension"
      },
      "border-radius": {
        "$value": "{semantic.radius.lg}",
        "$type": "dimension"
      }
    },
    "input": {
      "bg": {
        "$value": "{semantic.color.bg-primary}",
        "$type": "color"
      },
      "border-color": {
        "$value": "{semantic.color.border}",
        "$type": "color"
      }
    },
    "loading": {
      "dot-color": {
        "$value": "{semantic.color.text-tertiary}",
        "$type": "color"
      }
    }
  }
}
```

---

## Expected Implementation

### Message Display (ai-chat skill)

```tsx
function ChatMessage({ message, role }) {
  return (
    <div style={{
      display: 'flex',
      justifyContent: role === 'user' ? 'flex-end' : 'flex-start',
      marginBlockEnd: 'var(--spacing-md)'
    }}>
      <div style={{
        maxWidth: '70%',
        backgroundColor: `var(--chat-message-bg-${role})`,
        color: `var(--chat-message-text-${role})`,
        paddingInline: 'var(--chat-message-padding-inline)',
        paddingBlock: 'var(--chat-message-padding-block)',
        borderRadius: 'var(--chat-message-border-radius)',
        boxShadow: 'var(--shadow-sm)'
      }}>
        {message.content}
      </div>
    </div>
  );
}
```

### Input Area (forms skill)

```tsx
function ChatInput({ onSend }) {
  const [message, setMessage] = useState('');

  return (
    <div style={{
      display: 'flex',
      gap: 'var(--spacing-sm)',
      padding: 'var(--spacing-md)',
      backgroundColor: 'var(--chat-input-bg)',
      borderBlockStart: '1px solid var(--color-border)'
    }}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
        style={{
          flex: 1,
          height: 'var(--input-height)',
          paddingInline: 'var(--input-padding-inline)',
          backgroundColor: 'var(--input-bg)',
          border: '1px solid var(--chat-input-border-color)',
          borderRadius: 'var(--radius-md)',
          fontSize: 'var(--font-size-base)',
          color: 'var(--input-text-color)'
        }}
      />

      <button
        onClick={() => onSend(message)}
        style={{
          backgroundColor: 'var(--button-bg-primary)',
          color: 'var(--button-text-primary)',
          paddingInline: 'var(--button-padding-inline)',
          paddingBlock: 'var(--button-padding-block)',
          border: 'none',
          borderRadius: 'var(--button-border-radius)',
          fontSize: 'var(--font-size-base)',
          fontWeight: 'var(--font-weight-medium)',
          cursor: 'pointer'
        }}
      >
        Send
      </button>
    </div>
  );
}
```

### Loading State (ai-chat skill)

```tsx
function TypingIndicator() {
  return (
    <div style={{
      display: 'flex',
      gap: 'var(--spacing-xs)',
      padding: 'var(--chat-message-padding-inline)',
      backgroundColor: 'var(--chat-message-bg-assistant)',
      borderRadius: 'var(--chat-message-border-radius)',
      width: 'fit-content'
    }}>
      {[1, 2, 3].map(i => (
        <div
          key={i}
          style={{
            width: '8px',
            height: '8px',
            borderRadius: 'var(--radius-full)',
            backgroundColor: 'var(--chat-loading-dot-color)',
            animation: `pulse var(--duration-slow) ease-in-out infinite ${i * 0.2}s`
          }}
        />
      ))}
    </div>
  );
}
```

---

## Theme Switching Benefits

**Light mode:**
- User messages: Blue bubbles
- Assistant messages: Light gray bubbles
- High contrast on white background

**Dark mode:**
- User messages: Lighter blue bubbles
- Assistant messages: Dark gray bubbles
- Optimized for dark background

**Brand theme:**
- User messages: Brand color bubbles
- Consistent with app theme
- Professional appearance

---

## RTL Support (From design-tokens)

**Automatic message alignment:**

```tsx
// Same component code
<ChatMessage message={msg} role="user" />

// LTR (English): Aligns right
// RTL (Arabic): Aligns left (auto-flipped via justifyContent)
```

**Text alignment:**
```css
.message-content {
  text-align: start;  /* Left in LTR, right in RTL */
}
```

---

## Accessibility Features

**From design-tokens:**
- ✅ Focus indicators on input
- ✅ High-contrast theme option
- ✅ Reduced motion for animations
- ✅ WCAG 2.1 AA color contrast

**From ai-chat:**
- ✅ Screen reader announcements
- ✅ Keyboard navigation
- ✅ Message roles (aria-label)

---

## Token Efficiency

**Expected chain cost:**
```
design-tokens: 5,000 tokens (hub)
ai-chat: 5,000 tokens
forms: 5,000 tokens (already loaded in many cases)

TOTAL: 15,000 tokens
```

**Without chaining:**
```
ai-chat with inline theming + forms guidance:
= 50,000 tokens

TOTAL: 50,000 tokens
```

**Expected savings: 70%**

---

## Dependencies

**Required skills:**
- ✅ design-tokens (complete)
- ✅ forms (complete)
- 🚧 ai-chat (planned - PRIORITY)

**Blocking factor:** ai-chat skill implementation

**Estimated availability:** Q2 2026

---

## Priority Justification

**Business Case:**
1. **Market demand:** Every app adding AI (2025-2026)
2. **No established patterns:** First-mover opportunity
3. **Meta-advantage:** Claude building Claude-like UIs
4. **High value:** Premium feature set
5. **Universal need:** Chatbots, assistants, support

**Recommendation:** **Prioritize ai-chat skill development** 🚀

---

**Status:** 🚧 Planned (HIGH PRIORITY)
**Token Efficiency:** 70% estimated
**Business Value:** Very High
**Strategic Importance:** CRITICAL
**ETA:** Q2 2026
