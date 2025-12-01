#!/usr/bin/env node

/**
 * Format message history for export to various formats
 * Supports Markdown, JSON, HTML, and plain text
 */

const fs = require('fs');
const path = require('path');

class MessageFormatter {
  constructor(messages = []) {
    this.messages = messages;
  }

  /**
   * Format messages as Markdown
   */
  toMarkdown() {
    let markdown = '# Chat Conversation\n\n';

    // Add metadata
    const timestamp = new Date().toISOString();
    markdown += `*Exported: ${timestamp}*\n\n`;
    markdown += `*Messages: ${this.messages.length}*\n\n`;
    markdown += '---\n\n';

    // Format each message
    this.messages.forEach((msg, index) => {
      const role = msg.role.charAt(0).toUpperCase() + msg.role.slice(1);
      const time = msg.timestamp ? new Date(msg.timestamp).toLocaleString() : '';

      markdown += `## ${role}\n`;
      if (time) {
        markdown += `*${time}*\n\n`;
      }

      // Handle content (can be string or array for multi-modal)
      if (typeof msg.content === 'string') {
        markdown += `${msg.content}\n\n`;
      } else if (Array.isArray(msg.content)) {
        msg.content.forEach(item => {
          if (item.type === 'text') {
            markdown += `${item.text}\n\n`;
          } else if (item.type === 'image') {
            markdown += `![Image](${item.image})\n\n`;
          } else if (item.type === 'code') {
            markdown += `\`\`\`${item.language || ''}\n${item.code}\n\`\`\`\n\n`;
          }
        });
      }

      // Add feedback if present
      if (msg.feedback) {
        markdown += `*Feedback: ${msg.feedback}*\n\n`;
      }

      markdown += '---\n\n';
    });

    return markdown;
  }

  /**
   * Format messages as HTML
   */
  toHTML() {
    const escapeHtml = (text) => {
      const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      };
      return text.replace(/[&<>"']/g, m => map[m]);
    };

    let html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Conversation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .conversation {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .message {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
        }
        .message.user {
            background: #007AFF;
            color: white;
            margin-left: 20%;
        }
        .message.assistant {
            background: #E5E5EA;
            color: #000;
            margin-right: 20%;
        }
        .message.system {
            background: #FFF3CD;
            color: #856404;
            text-align: center;
        }
        .message-header {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .message-time {
            font-size: 0.8em;
            opacity: 0.7;
        }
        .message-content {
            line-height: 1.5;
            white-space: pre-wrap;
        }
        code {
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        pre code {
            background: none;
            color: inherit;
        }
        .metadata {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="conversation">
        <h1>Chat Conversation</h1>
        <div class="metadata">
            <p>Exported: ${new Date().toLocaleString()}</p>
            <p>Total Messages: ${this.messages.length}</p>
        </div>
`;

    this.messages.forEach(msg => {
      const role = msg.role;
      const time = msg.timestamp ? new Date(msg.timestamp).toLocaleString() : '';

      html += `        <div class="message ${role}">
            <div class="message-header">
                ${role.charAt(0).toUpperCase() + role.slice(1)}
                ${time ? `<span class="message-time">${time}</span>` : ''}
            </div>
            <div class="message-content">`;

      if (typeof msg.content === 'string') {
        // Convert markdown to HTML (simplified)
        let content = escapeHtml(msg.content);

        // Code blocks
        content = content.replace(/```(\w+)?\n([\s\S]*?)```/g,
          '<pre><code>$2</code></pre>');

        // Inline code
        content = content.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Bold
        content = content.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Italic
        content = content.replace(/\*([^*]+)\*/g, '<em>$1</em>');

        // Links
        content = content.replace(/\[([^\]]+)\]\(([^)]+)\)/g,
          '<a href="$2" target="_blank">$1</a>');

        html += content;
      } else if (Array.isArray(msg.content)) {
        msg.content.forEach(item => {
          if (item.type === 'text') {
            html += escapeHtml(item.text);
          } else if (item.type === 'image') {
            html += `<img src="${item.image}" style="max-width: 100%; border-radius: 5px;" />`;
          } else if (item.type === 'code') {
            html += `<pre><code>${escapeHtml(item.code)}</code></pre>`;
          }
        });
      }

      html += `</div>
        </div>
`;
    });

    html += `    </div>
</body>
</html>`;

    return html;
  }

  /**
   * Format messages as plain text
   */
  toPlainText() {
    let text = 'CHAT CONVERSATION\n';
    text += '=' .repeat(50) + '\n';
    text += `Exported: ${new Date().toLocaleString()}\n`;
    text += `Messages: ${this.messages.length}\n`;
    text += '=' .repeat(50) + '\n\n';

    this.messages.forEach((msg, index) => {
      const role = msg.role.toUpperCase();
      const time = msg.timestamp ? new Date(msg.timestamp).toLocaleString() : '';

      text += `[${role}]${time ? ` - ${time}` : ''}\n`;
      text += '-' .repeat(30) + '\n';

      if (typeof msg.content === 'string') {
        text += msg.content + '\n';
      } else if (Array.isArray(msg.content)) {
        msg.content.forEach(item => {
          if (item.type === 'text') {
            text += item.text + '\n';
          } else if (item.type === 'image') {
            text += `[Image: ${item.image}]\n`;
          } else if (item.type === 'code') {
            text += `[Code Block - ${item.language || 'plain'}]:\n${item.code}\n`;
          }
        });
      }

      text += '\n';
    });

    return text;
  }

  /**
   * Format messages as JSON
   */
  toJSON(pretty = true) {
    const data = {
      metadata: {
        exported: new Date().toISOString(),
        messageCount: this.messages.length,
        version: '1.0'
      },
      messages: this.messages
    };

    return pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data);
  }

  /**
   * Format messages for CSV export
   */
  toCSV() {
    const escapeCSV = (text) => {
      if (typeof text !== 'string') text = JSON.stringify(text);
      if (text.includes('"') || text.includes(',') || text.includes('\n')) {
        return '"' + text.replace(/"/g, '""') + '"';
      }
      return text;
    };

    let csv = 'Timestamp,Role,Content,Tokens,Feedback\n';

    this.messages.forEach(msg => {
      const timestamp = msg.timestamp || '';
      const role = msg.role || '';
      const content = typeof msg.content === 'string'
        ? msg.content
        : JSON.stringify(msg.content);
      const tokens = msg.tokens || '';
      const feedback = msg.feedback || '';

      csv += `${escapeCSV(timestamp)},${escapeCSV(role)},${escapeCSV(content)},${escapeCSV(tokens)},${escapeCSV(feedback)}\n`;
    });

    return csv;
  }

  /**
   * Create a summary of the conversation
   */
  createSummary() {
    const summary = {
      messageCount: this.messages.length,
      participants: [...new Set(this.messages.map(m => m.role))],
      timeRange: {
        start: null,
        end: null
      },
      statistics: {
        userMessages: 0,
        assistantMessages: 0,
        systemMessages: 0,
        averageLength: 0,
        totalTokens: 0
      },
      topics: [],
      codeBlocks: 0,
      images: 0,
      feedback: {
        positive: 0,
        negative: 0
      }
    };

    let totalLength = 0;

    this.messages.forEach(msg => {
      // Count by role
      if (msg.role === 'user') summary.statistics.userMessages++;
      else if (msg.role === 'assistant') summary.statistics.assistantMessages++;
      else if (msg.role === 'system') summary.statistics.systemMessages++;

      // Time range
      if (msg.timestamp) {
        const time = new Date(msg.timestamp);
        if (!summary.timeRange.start || time < summary.timeRange.start) {
          summary.timeRange.start = time;
        }
        if (!summary.timeRange.end || time > summary.timeRange.end) {
          summary.timeRange.end = time;
        }
      }

      // Content analysis
      const content = typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content);
      totalLength += content.length;

      // Count code blocks
      const codeBlocks = (content.match(/```/g) || []).length / 2;
      summary.codeBlocks += Math.floor(codeBlocks);

      // Count images
      if (Array.isArray(msg.content)) {
        msg.content.forEach(item => {
          if (item.type === 'image') summary.images++;
        });
      }

      // Feedback
      if (msg.feedback === 'positive') summary.feedback.positive++;
      else if (msg.feedback === 'negative') summary.feedback.negative++;

      // Tokens
      if (msg.tokens) summary.statistics.totalTokens += msg.tokens;
    });

    // Calculate average length
    summary.statistics.averageLength = Math.round(totalLength / this.messages.length);

    // Extract potential topics (simplified - looks for questions and key phrases)
    const allContent = this.messages.map(m =>
      typeof m.content === 'string' ? m.content : ''
    ).join(' ');

    const questions = allContent.match(/[^.!?]*\?/g) || [];
    summary.topics = questions.slice(0, 5).map(q => q.trim());

    return summary;
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const format = args[0] || 'markdown';
  const inputFile = args[1];
  const outputFile = args[2];

  if (!inputFile) {
    console.log(`
Usage: node format_messages.js <format> <input.json> [output]

Formats:
  - markdown (default)
  - html
  - text
  - json
  - csv
  - summary

Example:
  node format_messages.js markdown chat.json export.md
  node format_messages.js html chat.json export.html
  node format_messages.js summary chat.json
    `);
    process.exit(1);
  }

  try {
    const messagesData = fs.readFileSync(inputFile, 'utf8');
    const messages = JSON.parse(messagesData);

    // Handle both array and object with messages property
    const messageArray = Array.isArray(messages) ? messages : messages.messages || [];

    const formatter = new MessageFormatter(messageArray);
    let output;

    switch (format.toLowerCase()) {
      case 'html':
        output = formatter.toHTML();
        break;
      case 'text':
      case 'txt':
        output = formatter.toPlainText();
        break;
      case 'json':
        output = formatter.toJSON();
        break;
      case 'csv':
        output = formatter.toCSV();
        break;
      case 'summary':
        output = JSON.stringify(formatter.createSummary(), null, 2);
        break;
      case 'markdown':
      case 'md':
      default:
        output = formatter.toMarkdown();
    }

    if (outputFile) {
      fs.writeFileSync(outputFile, output);
      console.log(`✓ Exported to ${outputFile}`);
    } else {
      console.log(output);
    }

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Export for use as module
module.exports = MessageFormatter;