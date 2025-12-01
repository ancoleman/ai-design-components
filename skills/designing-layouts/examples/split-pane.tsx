import React, { useState, useRef, useEffect, useCallback } from 'react';

/**
 * Resizable Split-Pane Interface
 * Features: Mouse/touch dragging, keyboard control, min/max constraints
 */

interface SplitPaneProps {
  left: React.ReactNode;
  right: React.ReactNode;
  orientation?: 'horizontal' | 'vertical';
  defaultPosition?: number; // Percentage
  minPosition?: number; // Percentage
  maxPosition?: number; // Percentage
  resizerWidth?: number; // Pixels
  onResize?: (position: number) => void;
  storageKey?: string; // Save position to localStorage
}

export function SplitPane({
  left,
  right,
  orientation = 'horizontal',
  defaultPosition = 50,
  minPosition = 20,
  maxPosition = 80,
  resizerWidth = 4,
  onResize,
  storageKey
}: SplitPaneProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState(() => {
    if (storageKey) {
      const saved = localStorage.getItem(`splitpane-${storageKey}`);
      return saved ? parseFloat(saved) : defaultPosition;
    }
    return defaultPosition;
  });
  const [isDragging, setIsDragging] = useState(false);

  // Save position to localStorage
  useEffect(() => {
    if (storageKey) {
      localStorage.setItem(`splitpane-${storageKey}`, position.toString());
    }
  }, [position, storageKey]);

  // Handle mouse/touch move
  const handleMove = useCallback((clientX: number, clientY: number) => {
    if (!isDragging || !containerRef.current) return;

    const rect = containerRef.current.getBoundingClientRect();
    let newPosition: number;

    if (orientation === 'horizontal') {
      const x = clientX - rect.left;
      newPosition = (x / rect.width) * 100;
    } else {
      const y = clientY - rect.top;
      newPosition = (y / rect.height) * 100;
    }

    // Apply constraints
    newPosition = Math.max(minPosition, Math.min(maxPosition, newPosition));
    setPosition(newPosition);
    onResize?.(newPosition);
  }, [isDragging, orientation, minPosition, maxPosition, onResize]);

  // Mouse events
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => handleMove(e.clientX, e.clientY);
    const handleMouseUp = () => setIsDragging(false);

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = orientation === 'horizontal' ? 'col-resize' : 'row-resize';
      document.body.style.userSelect = 'none';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
  }, [isDragging, handleMove, orientation]);

  // Touch events
  const handleTouchMove = (e: React.TouchEvent) => {
    if (e.touches.length === 1) {
      handleMove(e.touches[0].clientX, e.touches[0].clientY);
    }
  };

  // Keyboard control
  const handleKeyDown = (e: React.KeyboardEvent) => {
    const step = 5; // 5% per key press
    let newPosition = position;

    switch (e.key) {
      case 'ArrowLeft':
      case 'ArrowUp':
        e.preventDefault();
        newPosition = Math.max(minPosition, position - step);
        break;
      case 'ArrowRight':
      case 'ArrowDown':
        e.preventDefault();
        newPosition = Math.min(maxPosition, position + step);
        break;
      case 'Home':
        e.preventDefault();
        newPosition = minPosition;
        break;
      case 'End':
        e.preventDefault();
        newPosition = maxPosition;
        break;
      default:
        return;
    }

    setPosition(newPosition);
    onResize?.(newPosition);
  };

  const isHorizontal = orientation === 'horizontal';

  return (
    <div
      ref={containerRef}
      className={`split-pane split-pane--${orientation}`}
      style={{
        display: 'flex',
        flexDirection: isHorizontal ? 'row' : 'column',
        height: '100%',
        width: '100%',
        position: 'relative'
      }}
    >
      {/* First Pane */}
      <div
        className="split-pane__first"
        style={{
          [isHorizontal ? 'width' : 'height']: `${position}%`,
          overflow: 'auto',
          flexShrink: 0
        }}
      >
        {left}
      </div>

      {/* Resizer */}
      <div
        className={`split-pane__resizer ${isDragging ? 'dragging' : ''}`}
        style={{
          [isHorizontal ? 'width' : 'height']: `${resizerWidth}px`,
          cursor: isHorizontal ? 'col-resize' : 'row-resize',
          flexShrink: 0
        }}
        role="separator"
        tabIndex={0}
        aria-valuenow={Math.round(position)}
        aria-valuemin={minPosition}
        aria-valuemax={maxPosition}
        aria-label={`Resize panes, current position ${Math.round(position)}%`}
        onMouseDown={() => setIsDragging(true)}
        onTouchStart={() => setIsDragging(true)}
        onTouchMove={handleTouchMove}
        onTouchEnd={() => setIsDragging(false)}
        onKeyDown={handleKeyDown}
      />

      {/* Second Pane */}
      <div
        className="split-pane__second"
        style={{
          flex: 1,
          overflow: 'auto',
          minWidth: 0,
          minHeight: 0
        }}
      >
        {right}
      </div>
    </div>
  );
}

/**
 * Code Editor Split Pane Example
 */
export function CodeEditorLayout() {
  const [activeFile, setActiveFile] = useState('index.tsx');

  const fileTree = (
    <div className="file-tree">
      <h3>Files</h3>
      <ul>
        <li>
          <button
            className={activeFile === 'index.tsx' ? 'active' : ''}
            onClick={() => setActiveFile('index.tsx')}
          >
            📄 index.tsx
          </button>
        </li>
        <li>
          <button
            className={activeFile === 'styles.css' ? 'active' : ''}
            onClick={() => setActiveFile('styles.css')}
          >
            🎨 styles.css
          </button>
        </li>
        <li>
          <button
            className={activeFile === 'README.md' ? 'active' : ''}
            onClick={() => setActiveFile('README.md')}
          >
            📝 README.md
          </button>
        </li>
      </ul>
    </div>
  );

  const editor = (
    <div className="code-editor">
      <div className="editor-header">
        <span className="editor-title">{activeFile}</span>
        <div className="editor-actions">
          <button aria-label="Format code">Format</button>
          <button aria-label="Save file">Save</button>
        </div>
      </div>
      <div className="editor-content">
        <pre>
          <code>{`// ${activeFile} content would go here
export function Component() {
  return <div>Hello World</div>;
}`}</code>
        </pre>
      </div>
    </div>
  );

  const preview = (
    <div className="preview-pane">
      <h3>Preview</h3>
      <div className="preview-content">
        <p>Live preview would render here</p>
      </div>
    </div>
  );

  return (
    <div style={{ height: '600px' }}>
      <SplitPane
        left={
          <SplitPane
            left={fileTree}
            right={editor}
            defaultPosition={25}
            minPosition={15}
            maxPosition={40}
            storageKey="file-tree"
          />
        }
        right={preview}
        defaultPosition={60}
        minPosition={40}
        maxPosition={80}
        storageKey="editor-preview"
      />
    </div>
  );
}

/**
 * Comparison View Example
 */
export function ComparisonView({
  before,
  after
}: {
  before: React.ReactNode;
  after: React.ReactNode;
}) {
  const [syncScroll, setSyncScroll] = useState(true);
  const leftRef = useRef<HTMLDivElement>(null);
  const rightRef = useRef<HTMLDivElement>(null);

  // Sync scrolling between panes
  const handleScroll = (source: 'left' | 'right') => {
    if (!syncScroll) return;

    const sourceRef = source === 'left' ? leftRef : rightRef;
    const targetRef = source === 'left' ? rightRef : leftRef;

    if (sourceRef.current && targetRef.current) {
      targetRef.current.scrollTop = sourceRef.current.scrollTop;
      targetRef.current.scrollLeft = sourceRef.current.scrollLeft;
    }
  };

  return (
    <div className="comparison-view">
      <div className="comparison-header">
        <button
          className={`sync-button ${syncScroll ? 'active' : ''}`}
          onClick={() => setSyncScroll(!syncScroll)}
          aria-pressed={syncScroll}
        >
          🔗 Sync Scroll
        </button>
      </div>

      <SplitPane
        left={
          <div className="comparison-pane">
            <h3 className="comparison-title">Before</h3>
            <div
              ref={leftRef}
              className="comparison-content"
              onScroll={() => handleScroll('left')}
            >
              {before}
            </div>
          </div>
        }
        right={
          <div className="comparison-pane">
            <h3 className="comparison-title">After</h3>
            <div
              ref={rightRef}
              className="comparison-content"
              onScroll={() => handleScroll('right')}
            >
              {after}
            </div>
          </div>
        }
        defaultPosition={50}
        minPosition={30}
        maxPosition={70}
      />
    </div>
  );
}

// CSS Styles
const styles = `
/* Split Pane Base Styles */
.split-pane {
  display: flex;
  height: 100%;
  width: 100%;
  position: relative;
}

.split-pane--horizontal {
  flex-direction: row;
}

.split-pane--vertical {
  flex-direction: column;
}

.split-pane__first,
.split-pane__second {
  overflow: auto;
}

/* Resizer Styles */
.split-pane__resizer {
  background: var(--border-color);
  position: relative;
  flex-shrink: 0;
  transition: background-color 0.2s;
}

.split-pane--horizontal .split-pane__resizer {
  width: 4px;
  cursor: col-resize;
}

.split-pane--vertical .split-pane__resizer {
  height: 4px;
  cursor: row-resize;
}

.split-pane__resizer:hover,
.split-pane__resizer:focus {
  background: var(--color-primary);
}

.split-pane__resizer.dragging {
  background: var(--color-primary);
}

/* Increase hit area for better UX */
.split-pane__resizer::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: -8px;
  right: -8px;
}

.split-pane--vertical .split-pane__resizer::after {
  left: 0;
  right: 0;
  top: -8px;
  bottom: -8px;
}

/* Focus styles */
.split-pane__resizer:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Code Editor Example Styles */
.file-tree {
  background: var(--color-background);
  padding: var(--spacing-md);
  height: 100%;
}

.file-tree h3 {
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--text-sm);
  text-transform: uppercase;
  opacity: 0.7;
}

.file-tree ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.file-tree button {
  width: 100%;
  text-align: left;
  padding: var(--spacing-sm);
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: background-color 0.2s;
}

.file-tree button:hover {
  background: var(--color-hover);
}

.file-tree button.active {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: 500;
}

.code-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  background: var(--color-background);
}

.editor-content {
  flex: 1;
  padding: var(--spacing-md);
  overflow: auto;
  font-family: 'Courier New', monospace;
}

.preview-pane {
  padding: var(--spacing-md);
  height: 100%;
  background: var(--color-surface);
}

/* Comparison View Styles */
.comparison-view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.comparison-header {
  padding: var(--spacing-sm);
  background: var(--color-background);
  border-bottom: 1px solid var(--border-color);
}

.sync-button {
  padding: var(--spacing-xs) var(--spacing-sm);
  border: 1px solid var(--border-color);
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s;
}

.sync-button.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.comparison-pane {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.comparison-title {
  margin: 0;
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-background);
  border-bottom: 1px solid var(--border-color);
  font-size: var(--text-sm);
  text-transform: uppercase;
  opacity: 0.7;
}

.comparison-content {
  flex: 1;
  padding: var(--spacing-md);
  overflow: auto;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .split-pane__resizer {
    background: rgba(255, 255, 255, 0.1);
  }

  .split-pane__resizer:hover,
  .split-pane__resizer.dragging {
    background: rgba(255, 255, 255, 0.3);
  }
}

/* Mobile responsive */
@media (max-width: 768px) {
  .split-pane--horizontal {
    flex-direction: column;
  }

  .split-pane__first {
    width: 100% !important;
    height: 50%;
  }

  .split-pane__resizer {
    display: none;
  }
}
`;