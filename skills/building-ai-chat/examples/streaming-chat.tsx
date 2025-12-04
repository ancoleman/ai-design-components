import React, { useState, useRef, useEffect } from 'react';

/**
 * Streaming Chat Example
 *
 * Complete chat interface with SSE streaming, message history, and auto-scroll.
 * Demonstrates best practices for streaming LLM responses.
 */

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export function StreamingChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentResponse, setCurrentResponse] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages, currentResponse]);

  const sendMessage = async () => {
    if (!input.trim() || isStreaming) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsStreaming(true);
    setCurrentResponse('');

    // Start SSE stream
    const es = new EventSource(
      `/api/chat/stream?message=${encodeURIComponent(userMessage.content)}`
    );

    eventSourceRef.current = es;

    es.addEventListener('token', (e) => {
      const token = JSON.parse(e.data).token;
      setCurrentResponse((prev) => prev + token);
    });

    es.addEventListener('done', () => {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: currentResponse,
          timestamp: new Date(),
        },
      ]);
      setCurrentResponse('');
      setIsStreaming(false);
      es.close();
    });

    es.onerror = () => {
      console.error('SSE error');
      setIsStreaming(false);
      es.close();
    };
  };

  const stopGeneration = () => {
    eventSourceRef.current?.close();
    if (currentResponse) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: currentResponse + ' [stopped]',
          timestamp: new Date(),
        },
      ]);
    }
    setCurrentResponse('');
    setIsStreaming(false);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', maxWidth: '800px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ padding: '16px', borderBottom: '1px solid #e2e8f0', backgroundColor: '#fff' }}>
        <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 600 }}>AI Assistant</h1>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', backgroundColor: '#f9fafb' }}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            style={{
              display: 'flex',
              justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
              marginBottom: '16px',
            }}
          >
            <div
              style={{
                maxWidth: '70%',
                padding: '12px 16px',
                borderRadius: '18px',
                backgroundColor: msg.role === 'user' ? '#3b82f6' : '#fff',
                color: msg.role === 'user' ? '#fff' : '#1f2937',
                border: msg.role === 'assistant' ? '1px solid #e2e8f0' : 'none',
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
              }}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {/* Streaming message */}
        {currentResponse && (
          <div style={{ display: 'flex', marginBottom: '16px' }}>
            <div
              style={{
                maxWidth: '70%',
                padding: '12px 16px',
                borderRadius: '18px',
                backgroundColor: '#fff',
                color: '#1f2937',
                border: '1px solid #e2e8f0',
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
              }}
            >
              {currentResponse}
              <span style={{ display: 'inline-block', width: '2px', height: '16px', backgroundColor: '#3b82f6', animation: 'blink 1s infinite', marginLeft: '2px' }} />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{ padding: '16px', borderTop: '1px solid #e2e8f0', backgroundColor: '#fff' }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder="Type your message..."
            disabled={isStreaming}
            style={{
              flex: 1,
              padding: '12px',
              borderRadius: '12px',
              border: '1px solid #e2e8f0',
              resize: 'none',
              minHeight: '52px',
              maxHeight: '200px',
              fontFamily: 'inherit',
            }}
          />
          {isStreaming ? (
            <button
              onClick={stopGeneration}
              style={{
                padding: '12px 24px',
                backgroundColor: '#ef4444',
                color: '#fff',
                border: 'none',
                borderRadius: '12px',
                cursor: 'pointer',
                fontWeight: 600,
              }}
            >
              ⬛ Stop
            </button>
          ) : (
            <button
              onClick={sendMessage}
              disabled={!input.trim()}
              style={{
                padding: '12px 24px',
                backgroundColor: input.trim() ? '#3b82f6' : '#e2e8f0',
                color: '#fff',
                border: 'none',
                borderRadius: '12px',
                cursor: input.trim() ? 'pointer' : 'not-allowed',
                fontWeight: 600,
              }}
            >
              Send
            </button>
          )}
        </div>
      </div>

      <style>{`
        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0; }
        }
      `}</style>
    </div>
  );
}

export default StreamingChat;
