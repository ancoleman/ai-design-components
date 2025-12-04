import React, { useState } from 'react';
import { Search, Calculator, Database, Code } from 'lucide-react';

/**
 * Tool-Calling Chat Example
 *
 * AI chat with function calling capabilities:
 * - Weather lookup
 * - Calculator
 * - Database query
 * - Code execution
 *
 * Demonstrates OpenAI function calling / Anthropic tool use pattern.
 */

interface Tool {
  name: string;
  description: string;
  icon: React.ReactNode;
}

const AVAILABLE_TOOLS: Tool[] = [
  { name: 'search_web', description: 'Search the web', icon: <Search size={16} /> },
  { name: 'calculate', description: 'Perform calculations', icon: <Calculator size={16} /> },
  { name: 'query_database', description: 'Query database', icon: <Database size={16} /> },
  { name: 'execute_code', description: 'Run Python code', icon: <Code size={16} /> },
];

interface Message {
  role: 'user' | 'assistant' | 'tool';
  content: string;
  toolCall?: {
    name: string;
    arguments: any;
    result?: any;
  };
}

export function ToolCallingChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');

    // Simulate AI deciding to use a tool
    const needsTool = input.toLowerCase().includes('weather') ||
                       input.toLowerCase().includes('calculate');

    if (needsTool) {
      // AI decides to call a tool
      const toolCall = {
        name: input.includes('weather') ? 'get_weather' : 'calculate',
        arguments: input.includes('weather')
          ? { location: 'San Francisco' }
          : { expression: '15 * 23' },
      };

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `I'll use the ${toolCall.name} tool to answer that.`,
          toolCall,
        },
      ]);

      // Execute tool
      const result = await executeTool(toolCall.name, toolCall.arguments);

      setMessages((prev) => [
        ...prev,
        {
          role: 'tool',
          content: JSON.stringify(result, null, 2),
          toolCall: { ...toolCall, result },
        },
      ]);

      // AI generates final response using tool result
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: generateResponseWithToolResult(toolCall.name, result),
        },
      ]);
    } else {
      // Regular response without tools
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'This is a regular response without using any tools.',
        },
      ]);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header with available tools */}
      <div style={{ padding: '16px', borderBottom: '1px solid #e2e8f0', backgroundColor: '#fff' }}>
        <h1 style={{ margin: '0 0 8px 0', fontSize: '20px', fontWeight: 600 }}>AI Assistant with Tools</h1>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {AVAILABLE_TOOLS.map((tool) => (
            <div
              key={tool.name}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                padding: '4px 12px',
                backgroundColor: '#f3f4f6',
                borderRadius: '12px',
                fontSize: '12px',
                color: '#64748b',
              }}
            >
              {tool.icon}
              <span>{tool.description}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', backgroundColor: '#f9fafb' }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ marginBottom: '16px' }}>
            {msg.role === 'user' && (
              <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                <div style={{ maxWidth: '70%', padding: '12px 16px', borderRadius: '18px', backgroundColor: '#3b82f6', color: '#fff' }}>
                  {msg.content}
                </div>
              </div>
            )}

            {msg.role === 'assistant' && (
              <div>
                <div style={{ padding: '12px 16px', borderRadius: '18px', backgroundColor: '#fff', border: '1px solid #e2e8f0', maxWidth: '70%' }}>
                  {msg.content}
                </div>

                {msg.toolCall && !msg.toolCall.result && (
                  <div style={{ marginTop: '8px', padding: '8px 12px', backgroundColor: '#fef3c7', borderRadius: '8px', fontSize: '13px', display: 'inline-block' }}>
                    🔧 Calling tool: <code>{msg.toolCall.name}</code>
                  </div>
                )}
              </div>
            )}

            {msg.role === 'tool' && msg.toolCall && (
              <div style={{ marginTop: '8px', padding: '12px', backgroundColor: '#f3f4f6', borderRadius: '8px', fontSize: '13px', fontFamily: 'monospace', maxWidth: '70%' }}>
                <div style={{ fontWeight: 600, marginBottom: '8px', color: '#64748b' }}>
                  Tool Result: {msg.toolCall.name}
                </div>
                <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                  {msg.content}
                </pre>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Attachment previews */}
      {attachments.length > 0 && (
        <div style={{ padding: '16px', borderTop: '1px solid #e2e8f0', backgroundColor: '#f9fafb' }}>
          <div style={{ display: 'flex', gap: '8px' }}>
            {attachments.map((att) => (
              <div
                key={att.id}
                style={{
                  position: 'relative',
                  width: '80px',
                  height: '80px',
                  borderRadius: '8px',
                  overflow: 'hidden',
                  border: '1px solid #e2e8f0',
                }}
              >
                <img src={att.preview} alt={att.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                <button
                  onClick={() => removeAttachment(att.id)}
                  style={{
                    position: 'absolute',
                    top: '4px',
                    right: '4px',
                    width: '20px',
                    height: '20px',
                    borderRadius: '50%',
                    backgroundColor: 'rgba(0,0,0,0.6)',
                    color: '#fff',
                    border: 'none',
                    cursor: 'pointer',
                  }}
                >
                  <X size={12} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div style={{ padding: '16px', borderTop: '1px solid #e2e8f0', backgroundColor: '#fff' }}>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-end' }}>
          <div style={{ display: 'flex', gap: '4px' }}>
            <input type="file" accept="image/*" onChange={handleImageUpload} id="img-upload" style={{ display: 'none' }} />
            <label htmlFor="img-upload" style={{ cursor: 'pointer', padding: '8px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
              <Camera size={20} color="#64748b" />
            </label>
          </div>

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder="Ask me to search, calculate, or query data..."
            style={{ flex: 1, padding: '12px', borderRadius: '12px', border: '1px solid #e2e8f0', resize: 'none', minHeight: '52px' }}
          />

          <button
            onClick={sendMessage}
            disabled={!input.trim() && attachments.length === 0}
            style={{
              padding: '12px 24px',
              backgroundColor: (input.trim() || attachments.length > 0) ? '#3b82f6' : '#e2e8f0',
              color: '#fff',
              border: 'none',
              borderRadius: '12px',
              cursor: (input.trim() || attachments.length > 0) ? 'pointer' : 'not-allowed',
              fontWeight: 600,
              height: '52px',
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

async function executeTool(name: string, args: any): Promise<any> {
  // Mock tool execution
  const tools = {
    get_weather: ({ location }: any) => ({
      location,
      temperature: 72,
      condition: 'Sunny',
      humidity: 45,
    }),
    calculate: ({ expression }: any) => ({
      expression,
      result: eval(expression),
    }),
    query_database: ({ query }: any) => ({
      query,
      results: [{ id: 1, name: 'Sample' }],
      count: 1,
    }),
  };

  return tools[name]?.(args) || { error: 'Tool not found' };
}

function generateResponseWithToolResult(toolName: string, result: any): string {
  if (toolName === 'get_weather') {
    return `The weather in ${result.location} is ${result.temperature}°F and ${result.condition}. Humidity is ${result.humidity}%.`;
  }
  if (toolName === 'calculate') {
    return `The result of ${result.expression} is ${result.result}.`;
  }
  return JSON.stringify(result);
}

export default ToolCallingChat;
