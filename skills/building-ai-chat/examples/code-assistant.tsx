import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import ReactMarkdown from 'react-markdown';

/**
 * Code Assistant Chat Example
 *
 * Specialized chat for code-related tasks with:
 * - Syntax highlighting for code blocks
 * - Copy code button
 * - Language detection
 * - File context (show current file)
 * - Code suggestions
 */

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export function CodeAssistant() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [currentFile, setCurrentFile] = useState('app/main.py');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');

    // Include file context
    const context = `Current file: ${currentFile}\n\n${input}`;

    // Simulate API call
    const response = await mockCodeResponse(context);
    setMessages((prev) => [...prev, { role: 'assistant', content: response }]);
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      {/* Sidebar with file context */}
      <div style={{ width: '250px', borderRight: '1px solid #e2e8f0', padding: '16px', backgroundColor: '#f9fafb' }}>
        <h3 style={{ fontSize: '14px', fontWeight: 600, marginBottom: '12px' }}>Current File</h3>
        <div style={{ padding: '8px', backgroundColor: '#fff', borderRadius: '6px', border: '1px solid #e2e8f0', fontFamily: 'monospace', fontSize: '13px' }}>
          {currentFile}
        </div>

        <h3 style={{ fontSize: '14px', fontWeight: 600, marginTop: '24px', marginBottom: '12px' }}>Quick Actions</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <button style={{ padding: '8px', textAlign: 'left', fontSize: '13px', border: '1px solid #e2e8f0', borderRadius: '6px', backgroundColor: '#fff', cursor: 'pointer' }}>
            💡 Explain this code
          </button>
          <button style={{ padding: '8px', textAlign: 'left', fontSize: '13px', border: '1px solid #e2e8f0', borderRadius: '6px', backgroundColor: '#fff', cursor: 'pointer' }}>
            🐛 Debug this function
          </button>
          <button style={{ padding: '8px', textAlign: 'left', fontSize: '13px', border: '1px solid #e2e8f0', borderRadius: '6px', backgroundColor: '#fff', cursor: 'pointer' }}>
            ✨ Add docstring
          </button>
          <button style={{ padding: '8px', textAlign: 'left', fontSize: '13px', border: '1px solid #e2e8f0', borderRadius: '6px', backgroundColor: '#fff', cursor: 'pointer' }}>
            🔄 Refactor code
          </button>
        </div>
      </div>

      {/* Chat area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', padding: '48px', color: '#64748b' }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>👨‍💻</div>
              <h2 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '8px' }}>Code Assistant</h2>
              <p>Ask me to explain, debug, refactor, or generate code</p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                marginBottom: '24px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start',
              }}
            >
              <div
                style={{
                  maxWidth: '80%',
                  backgroundColor: msg.role === 'user' ? '#3b82f6' : '#fff',
                  color: msg.role === 'user' ? '#fff' : '#1f2937',
                  padding: msg.role === 'user' ? '12px 16px' : '0',
                  borderRadius: msg.role === 'user' ? '18px' : '0',
                  border: msg.role === 'assistant' ? '1px solid #e2e8f0' : 'none',
                }}
              >
                {msg.role === 'assistant' ? (
                  <ReactMarkdown
                    components={{
                      code({ node, inline, className, children, ...props }) {
                        const match = /language-(\w+)/.exec(className || '');
                        const code = String(children).replace(/\n$/, '');

                        return !inline ? (
                          <CodeBlock code={code} language={match ? match[1] : 'text'} />
                        ) : (
                          <code
                            style={{
                              backgroundColor: '#f3f4f6',
                              padding: '2px 6px',
                              borderRadius: '4px',
                              fontSize: '0.9em',
                              fontFamily: 'monospace',
                            }}
                          >
                            {children}
                          </code>
                        );
                      },
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                ) : (
                  msg.content
                )}
              </div>
            </div>
          ))}
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
              placeholder="Ask about code..."
              style={{
                flex: 1,
                padding: '12px',
                borderRadius: '12px',
                border: '1px solid #e2e8f0',
                resize: 'none',
                minHeight: '52px',
                fontFamily: 'inherit',
              }}
            />
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
          </div>
        </div>
      </div>
    </div>
  );
}

function CodeBlock({ code, language }: { code: string; language: string }) {
  const [copied, setCopied] = useState(false);

  return (
    <div style={{ margin: '12px 0', borderRadius: '8px', overflow: 'hidden' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 16px', backgroundColor: '#1e293b', color: '#fff', fontSize: '13px' }}>
        <span>{language}</span>
        <button
          onClick={() => {
            navigator.clipboard.writeText(code);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
          }}
          style={{ background: 'none', border: 'none', color: '#fff', cursor: 'pointer', fontSize: '13px' }}
        >
          {copied ? '✓ Copied' : '📋 Copy'}
        </button>
      </div>
      <SyntaxHighlighter language={language} style={vscDarkPlus} customStyle={{ margin: 0 }}>
        {code}
      </SyntaxHighlighter>
    </div>
  );
}

async function mockCodeResponse(prompt: string): Promise<string> {
  return `Here's a Python function to solve that:

\`\`\`python
def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number using dynamic programming"""
    if n <= 1:
        return n

    dp = [0, 1]
    for i in range(2, n + 1):
        dp.append(dp[i-1] + dp[i-2])

    return dp[n]
\`\`\`

This implementation:
- Uses dynamic programming for O(n) time complexity
- Includes type hints for clarity
- Has a docstring explaining the function
- Handles edge cases (n <= 1)

Would you like me to add unit tests or optimize further?`;
}

export default StreamingChat;
