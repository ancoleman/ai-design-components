/**
 * Basic ChatGPT-style interface implementation
 * Uses Vercel AI SDK for streaming responses
 */

import React from 'react';
import { useChat } from 'ai/react';
import { Streamdown } from '@vercel/streamdown';

export function BasicChat() {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    error,
    reload,
    stop
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
      {/* Header */}
      <header className="chat-header">
        <h1>AI Assistant</h1>
        <span className="status">
          {isLoading ? 'AI is thinking...' : 'Ready'}
        </span>
      </header>

      {/* Messages */}
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>Start a conversation by typing a message below</p>
          </div>
        )}

        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}

        {/* Scroll anchor */}
        <div className="scroll-anchor" />
      </div>

      {/* Error display */}
      {error && (
        <div className="error-banner">
          <span>Error: {error.message}</span>
          <button onClick={reload} className="retry-btn">
            Retry
          </button>
        </div>
      )}

      {/* Input form */}
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <textarea
            value={input}
            onChange={handleInputChange}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e as any);
              }
            }}
            placeholder="Type your message... (Shift+Enter for new line)"
            disabled={isLoading}
            rows={1}
            className="message-input"
          />

          {isLoading ? (
            <button type="button" onClick={stop} className="stop-btn">
              <StopIcon />
              Stop
            </button>
          ) : (
            <button
              type="submit"
              disabled={!input.trim()}
              className="send-btn"
            >
              <SendIcon />
              Send
            </button>
          )}
        </div>

        <div className="input-hints">
          <span>Press Enter to send, Shift+Enter for new line</span>
        </div>
      </form>
    </div>
  );
}

/**
 * Individual message component
 */
function Message({ message }: { message: any }) {
  const isUser = message.role === 'user';
  const isAssistant = message.role === 'assistant';

  return (
    <div className={`message ${message.role}`}>
      {/* Avatar */}
      <div className="message-avatar">
        {isUser ? <UserIcon /> : isAssistant ? <BotIcon /> : <SystemIcon />}
      </div>

      {/* Content */}
      <div className="message-content">
        {/* Role label */}
        <div className="message-role">
          {isUser ? 'You' : isAssistant ? 'Assistant' : 'System'}
        </div>

        {/* Message text with markdown support */}
        <div className="message-text">
          <Streamdown>{message.content}</Streamdown>
        </div>

        {/* Timestamp */}
        <div className="message-time">
          {formatTime(message.createdAt)}
        </div>
      </div>

      {/* Actions */}
      {isAssistant && (
        <MessageActions message={message} />
      )}
    </div>
  );
}

/**
 * Message action buttons
 */
function MessageActions({ message }: { message: any }) {
  const [feedback, setFeedback] = React.useState<'positive' | 'negative' | null>(null);
  const [copied, setCopied] = React.useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleFeedback = (type: 'positive' | 'negative') => {
    setFeedback(feedback === type ? null : type);
    // Send feedback to backend
    sendFeedback(message.id, type);
  };

  return (
    <div className="message-actions">
      <button
        onClick={() => handleFeedback('positive')}
        className={`action-btn ${feedback === 'positive' ? 'selected' : ''}`}
        aria-label="Good response"
      >
        <ThumbsUpIcon />
      </button>

      <button
        onClick={() => handleFeedback('negative')}
        className={`action-btn ${feedback === 'negative' ? 'selected' : ''}`}
        aria-label="Bad response"
      >
        <ThumbsDownIcon />
      </button>

      <button
        onClick={handleCopy}
        className="action-btn"
        aria-label="Copy to clipboard"
      >
        {copied ? <CheckIcon /> : <CopyIcon />}
      </button>
    </div>
  );
}

/**
 * Icon components
 */
const SendIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const StopIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <rect x="6" y="6" width="12" height="12" rx="2"/>
  </svg>
);

const UserIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z" strokeWidth="2"/>
  </svg>
);

const BotIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <rect x="3" y="11" width="18" height="10" rx="2" ry="2" strokeWidth="2"/>
    <circle cx="12" cy="5" r="2" strokeWidth="2"/>
    <path d="M12 7v4" strokeWidth="2"/>
  </svg>
);

const SystemIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <circle cx="12" cy="12" r="10" strokeWidth="2"/>
    <path d="M12 8v4M12 16h.01" strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

const ThumbsUpIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" strokeWidth="2"/>
  </svg>
);

const ThumbsDownIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17" strokeWidth="2"/>
  </svg>
);

const CopyIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" strokeWidth="2"/>
    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" strokeWidth="2"/>
  </svg>
);

const CheckIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <polyline points="20 6 9 17 4 12" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

/**
 * Utility functions
 */
function formatTime(date: Date | string) {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

async function sendFeedback(messageId: string, type: 'positive' | 'negative') {
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messageId, type })
    });
  } catch (error) {
    console.error('Failed to send feedback:', error);
  }
}

/**
 * Styles (using CSS modules or styled-components in production)
 */
const styles = `
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--chat-bg, #f5f5f5);
}

.chat-header {
  padding: 1rem;
  background: var(--header-bg, white);
  border-bottom: 1px solid var(--border-color, #e0e0e0);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  scroll-behavior: smooth;
}

.empty-state {
  text-align: center;
  color: var(--text-secondary, #666);
  margin-top: 2rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  animation: slideIn 0.3s ease-out;
}

.message.user {
  flex-direction: row-reverse;
}

.message.user .message-content {
  background: var(--message-user-bg, #007AFF);
  color: var(--message-user-text, white);
}

.message.assistant .message-content {
  background: var(--message-ai-bg, white);
  color: var(--message-ai-text, black);
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--avatar-bg, #e0e0e0);
}

.message-content {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: var(--message-radius, 12px);
  box-shadow: var(--message-shadow, 0 1px 2px rgba(0,0,0,0.1));
}

.message-role {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-bottom: 0.25rem;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.5;
  margin-top: 0.25rem;
}

.message-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.action-btn {
  padding: 0.25rem;
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.action-btn:hover {
  opacity: 1;
}

.action-btn.selected {
  opacity: 1;
  color: var(--primary-color, #007AFF);
}

.input-form {
  padding: 1rem;
  background: var(--input-bg, white);
  border-top: 1px solid var(--border-color, #e0e0e0);
}

.input-container {
  display: flex;
  gap: 0.5rem;
}

.message-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--input-border, #e0e0e0);
  border-radius: var(--input-radius, 8px);
  resize: none;
  font-family: inherit;
}

.message-input:focus {
  outline: none;
  border-color: var(--primary-color, #007AFF);
}

.send-btn, .stop-btn {
  padding: 0.75rem 1.5rem;
  background: var(--primary-color, #007AFF);
  color: white;
  border: none;
  border-radius: var(--button-radius, 8px);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.stop-btn {
  background: var(--danger-color, #dc3545);
}

.error-banner {
  padding: 1rem;
  background: var(--error-bg, #fee);
  color: var(--error-color, #c00);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .message-content {
    max-width: 85%;
  }
}
`;