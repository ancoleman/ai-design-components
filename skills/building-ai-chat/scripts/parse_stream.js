#!/usr/bin/env node

/**
 * Parse incomplete markdown during streaming
 * Handles partial blocks and ensures valid markdown output
 */

class StreamParser {
  constructor() {
    this.buffer = '';
    this.openBlocks = {
      codeBlock: false,
      table: false,
      list: false,
      blockquote: false
    };
  }

  /**
   * Parse a chunk of streaming text
   * @param {string} chunk - New text chunk
   * @returns {Object} Parsed result with complete and incomplete parts
   */
  parseChunk(chunk) {
    this.buffer += chunk;

    const result = {
      complete: '',
      incomplete: '',
      warnings: []
    };

    // Check for incomplete code blocks
    const codeBlockMatches = this.buffer.match(/```/g) || [];
    if (codeBlockMatches.length % 2 !== 0) {
      this.openBlocks.codeBlock = true;
      result.warnings.push('Incomplete code block detected');
    } else {
      this.openBlocks.codeBlock = false;
    }

    // Check for incomplete tables
    const tableRows = this.buffer.split('\n').filter(line => line.includes('|'));
    if (tableRows.length > 0) {
      const lastRow = tableRows[tableRows.length - 1];
      if (!lastRow.endsWith('|')) {
        this.openBlocks.table = true;
        result.warnings.push('Incomplete table row detected');
      }
    }

    // Check for incomplete lists
    const lines = this.buffer.split('\n');
    const lastLine = lines[lines.length - 1];
    if (/^[\s]*[-*+]\s/.test(lastLine) && lastLine.trim().length <= 2) {
      this.openBlocks.list = true;
      result.warnings.push('Incomplete list item detected');
    }

    // Split complete and incomplete parts
    const blocks = this.splitIntoBlocks(this.buffer);

    result.complete = blocks.complete.join('\n\n');
    result.incomplete = blocks.incomplete;

    return result;
  }

  /**
   * Split content into complete and incomplete blocks
   */
  splitIntoBlocks(content) {
    const blocks = {
      complete: [],
      incomplete: ''
    };

    // If we're in a code block, everything is incomplete
    if (this.openBlocks.codeBlock) {
      blocks.incomplete = content;
      return blocks;
    }

    const paragraphs = content.split('\n\n');

    // All but the last paragraph are complete
    if (paragraphs.length > 1) {
      blocks.complete = paragraphs.slice(0, -1);
      blocks.incomplete = paragraphs[paragraphs.length - 1];
    } else {
      blocks.incomplete = content;
    }

    return blocks;
  }

  /**
   * Close any open blocks and return final markdown
   */
  finalize() {
    let finalContent = this.buffer;

    // Close unclosed code blocks
    if (this.openBlocks.codeBlock) {
      finalContent += '\n```';
    }

    // Close unclosed blockquotes
    const blockquoteLines = finalContent.split('\n').filter(line => line.startsWith('>'));
    if (blockquoteLines.length > 0 && !finalContent.endsWith('\n')) {
      finalContent += '\n';
    }

    // Ensure lists end properly
    if (this.openBlocks.list) {
      finalContent += '\n';
    }

    // Clean up any double newlines
    finalContent = finalContent.replace(/\n{3,}/g, '\n\n');

    return {
      content: finalContent,
      closedBlocks: Object.keys(this.openBlocks).filter(key => this.openBlocks[key])
    };
  }

  /**
   * Reset the parser state
   */
  reset() {
    this.buffer = '';
    this.openBlocks = {
      codeBlock: false,
      table: false,
      list: false,
      blockquote: false
    };
  }
}

// Utility functions for markdown processing

/**
 * Extract code blocks from markdown
 */
function extractCodeBlocks(markdown) {
  const codeBlocks = [];
  const regex = /```(\w+)?\n([\s\S]*?)```/g;
  let match;

  while ((match = regex.exec(markdown)) !== null) {
    codeBlocks.push({
      language: match[1] || 'text',
      code: match[2].trim(),
      startIndex: match.index,
      endIndex: match.index + match[0].length
    });
  }

  return codeBlocks;
}

/**
 * Fix common markdown issues
 */
function fixMarkdownIssues(markdown) {
  let fixed = markdown;

  // Fix unclosed bold/italic
  const boldCount = (fixed.match(/\*\*/g) || []).length;
  if (boldCount % 2 !== 0) {
    fixed += '**';
  }

  const italicCount = (fixed.match(/(?<!\*)\*(?!\*)/g) || []).length;
  if (italicCount % 2 !== 0) {
    fixed += '*';
  }

  // Fix broken links
  fixed = fixed.replace(/\[([^\]]*)\]\(([^\)]*)/g, (match, text, url) => {
    if (!match.endsWith(')')) {
      return `[${text}](${url})`;
    }
    return match;
  });

  // Fix incomplete headers
  fixed = fixed.replace(/^(#{1,6})\s*$/gm, '');

  // Fix table formatting
  const tableLines = fixed.split('\n').map(line => {
    if (line.includes('|')) {
      // Ensure line starts and ends with |
      if (!line.startsWith('|')) line = '|' + line;
      if (!line.endsWith('|')) line = line + '|';

      // Fix separator rows
      if (line.match(/^\|[\s\-:|]+\|$/)) {
        const cells = line.split('|').filter(c => c);
        line = '|' + cells.map(c => c.replace(/[^:\-]/g, '-')).join('|') + '|';
      }
    }
    return line;
  });
  fixed = tableLines.join('\n');

  return fixed;
}

/**
 * Validate markdown structure
 */
function validateMarkdown(markdown) {
  const issues = [];

  // Check code blocks
  const codeBlockCount = (markdown.match(/```/g) || []).length;
  if (codeBlockCount % 2 !== 0) {
    issues.push({
      type: 'error',
      message: 'Unclosed code block',
      suggestion: 'Add ``` to close the code block'
    });
  }

  // Check for empty headers
  if (markdown.match(/^#{1,6}\s*$/m)) {
    issues.push({
      type: 'warning',
      message: 'Empty header detected',
      suggestion: 'Add header text or remove the header'
    });
  }

  // Check for broken tables
  const tableLines = markdown.split('\n').filter(line => line.includes('|'));
  tableLines.forEach(line => {
    const cellCount = line.split('|').filter(c => c).length;
    if (tableLines.length > 0 && cellCount < 2) {
      issues.push({
        type: 'warning',
        message: 'Malformed table row',
        line: line,
        suggestion: 'Ensure table rows have consistent column count'
      });
    }
  });

  return issues;
}

// CLI interface
if (require.main === module) {
  const parser = new StreamParser();

  // Read from stdin if piped
  if (!process.stdin.isTTY) {
    let input = '';

    process.stdin.on('data', chunk => {
      input += chunk.toString();
      const result = parser.parseChunk(chunk.toString());

      if (result.warnings.length > 0) {
        console.error('Warnings:', result.warnings);
      }
    });

    process.stdin.on('end', () => {
      const final = parser.finalize();
      const fixed = fixMarkdownIssues(final.content);
      const issues = validateMarkdown(fixed);

      console.log(JSON.stringify({
        content: fixed,
        closedBlocks: final.closedBlocks,
        issues: issues
      }, null, 2));
    });
  } else {
    // Test mode with sample input
    const testInput = `
# Test Header

This is a paragraph with **bold text.

\`\`\`javascript
function test() {
  console.log('incomplete
    `;

    const result = parser.parseChunk(testInput);
    console.log('Parse result:', result);

    const final = parser.finalize();
    console.log('Final result:', final);

    const fixed = fixMarkdownIssues(final.content);
    console.log('Fixed markdown:', fixed);

    const issues = validateMarkdown(fixed);
    console.log('Validation issues:', issues);
  }
}

// Export for use as module
module.exports = {
  StreamParser,
  extractCodeBlocks,
  fixMarkdownIssues,
  validateMarkdown
};