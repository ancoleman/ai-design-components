import React, { useState, useEffect, useRef } from 'react';

/**
 * File Upload Progress Examples
 *
 * Demonstrates various progress indicators for file uploads
 * including single and multiple file upload with progress tracking
 */

// Single File Upload with Progress
export function FileUploadProgress({ file, onComplete, onError }) {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('pending'); // pending, uploading, complete, error
  const [uploadSpeed, setUploadSpeed] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(null);
  const xhrRef = useRef(null);
  const startTimeRef = useRef(null);
  const lastProgressRef = useRef({ loaded: 0, time: Date.now() });

  useEffect(() => {
    if (status === 'pending') {
      startUpload();
    }

    return () => {
      // Cleanup: abort upload if component unmounts
      if (xhrRef.current) {
        xhrRef.current.abort();
      }
    };
  }, []);

  const startUpload = () => {
    setStatus('uploading');
    startTimeRef.current = Date.now();

    const xhr = new XMLHttpRequest();
    xhrRef.current = xhr;

    // Track upload progress
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percentComplete = (e.loaded / e.total) * 100;
        setProgress(Math.round(percentComplete));

        // Calculate upload speed
        const currentTime = Date.now();
        const timeDiff = (currentTime - lastProgressRef.current.time) / 1000; // seconds
        const bytesDiff = e.loaded - lastProgressRef.current.loaded;
        const speed = bytesDiff / timeDiff; // bytes per second
        setUploadSpeed(speed);

        // Calculate time remaining
        const remaining = e.total - e.loaded;
        const timeLeft = remaining / speed; // seconds
        setTimeRemaining(Math.round(timeLeft));

        lastProgressRef.current = { loaded: e.loaded, time: currentTime };
      }
    });

    // Handle completion
    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        setStatus('complete');
        setProgress(100);
        onComplete?.(xhr.response);
      } else {
        setStatus('error');
        onError?.(new Error(`Upload failed with status ${xhr.status}`));
      }
    });

    // Handle errors
    xhr.addEventListener('error', () => {
      setStatus('error');
      onError?.(new Error('Network error during upload'));
    });

    // Prepare and send request
    const formData = new FormData();
    formData.append('file', file);

    xhr.open('POST', '/api/upload');
    xhr.send(formData);
  };

  const handleCancel = () => {
    if (xhrRef.current) {
      xhrRef.current.abort();
      setStatus('cancelled');
    }
  };

  const handleRetry = () => {
    setProgress(0);
    setStatus('pending');
    startUpload();
  };

  const formatFileSize = (bytes) => {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }

    return `${size.toFixed(1)} ${units[unitIndex]}`;
  };

  const formatTime = (seconds) => {
    if (!seconds || seconds < 0) return '';
    if (seconds < 60) return `${seconds}s remaining`;
    const minutes = Math.floor(seconds / 60);
    return `${minutes}m ${seconds % 60}s remaining`;
  };

  const formatSpeed = (bytesPerSecond) => {
    return `${formatFileSize(bytesPerSecond)}/s`;
  };

  return (
    <div className="upload-progress-container">
      {/* File info */}
      <div className="upload-header">
        <div className="file-icon">
          {getFileIcon(file.type)}
        </div>
        <div className="file-info">
          <div className="file-name">{file.name}</div>
          <div className="file-meta">
            <span>{formatFileSize(file.size)}</span>
            {status === 'uploading' && uploadSpeed > 0 && (
              <>
                <span className="separator">•</span>
                <span>{formatSpeed(uploadSpeed)}</span>
                <span className="separator">•</span>
                <span>{formatTime(timeRemaining)}</span>
              </>
            )}
          </div>
        </div>
        <div className="upload-actions">
          {status === 'uploading' && (
            <button onClick={handleCancel} className="btn-icon">
              ✕
            </button>
          )}
          {status === 'error' && (
            <button onClick={handleRetry} className="btn-icon">
              ↻
            </button>
          )}
          {status === 'complete' && (
            <span className="success-icon">✓</span>
          )}
        </div>
      </div>

      {/* Progress bar */}
      <div className="progress-container">
        <div className="progress-track">
          <div
            className={`progress-bar progress-${status}`}
            style={{ width: `${progress}%` }}
            role="progressbar"
            aria-valuenow={progress}
            aria-valuemin={0}
            aria-valuemax={100}
          />
        </div>
        <span className="progress-label">{progress}%</span>
      </div>

      {/* Status message */}
      {status === 'error' && (
        <div className="upload-error">
          Upload failed. <button onClick={handleRetry}>Try again</button>
        </div>
      )}
      {status === 'complete' && (
        <div className="upload-success">
          Upload complete!
        </div>
      )}
    </div>
  );
}

// Multiple File Upload Queue
export function MultiFileUploadQueue({ files, onAllComplete }) {
  const [uploads, setUploads] = useState(
    files.map((file, index) => ({
      id: `${file.name}-${index}`,
      file,
      progress: 0,
      status: 'queued', // queued, uploading, complete, error
      speed: 0,
      error: null
    }))
  );
  const [currentUploadIndex, setCurrentUploadIndex] = useState(0);
  const [parallelUploads, setParallelUploads] = useState(3); // Upload 3 files at once

  useEffect(() => {
    // Start initial uploads
    for (let i = 0; i < Math.min(parallelUploads, files.length); i++) {
      if (uploads[i]?.status === 'queued') {
        startUpload(i);
      }
    }
  }, []);

  const startUpload = (index) => {
    const upload = uploads[index];
    if (!upload || upload.status !== 'queued') return;

    setUploads(prev => prev.map((u, i) =>
      i === index ? { ...u, status: 'uploading' } : u
    ));

    // Simulate upload with progress
    const interval = setInterval(() => {
      setUploads(prev => {
        const current = prev[index];
        if (!current || current.status !== 'uploading') {
          clearInterval(interval);
          return prev;
        }

        const newProgress = Math.min(current.progress + Math.random() * 20, 100);

        if (newProgress >= 100) {
          clearInterval(interval);
          // Start next upload in queue
          const nextIndex = prev.findIndex(u => u.status === 'queued');
          if (nextIndex !== -1) {
            setTimeout(() => startUpload(nextIndex), 100);
          }

          return prev.map((u, i) =>
            i === index ? { ...u, progress: 100, status: 'complete' } : u
          );
        }

        return prev.map((u, i) =>
          i === index ? { ...u, progress: newProgress } : u
        );
      });
    }, 500);
  };

  const handleCancel = (id) => {
    setUploads(prev => prev.map(u =>
      u.id === id && u.status === 'uploading'
        ? { ...u, status: 'cancelled' }
        : u
    ));
  };

  const handleRetry = (id) => {
    const index = uploads.findIndex(u => u.id === id);
    if (index !== -1) {
      setUploads(prev => prev.map((u, i) =>
        i === index ? { ...u, progress: 0, status: 'queued', error: null } : u
      ));
      startUpload(index);
    }
  };

  const handleRemove = (id) => {
    setUploads(prev => prev.filter(u => u.id !== id));
  };

  // Calculate overall progress
  const totalProgress = uploads.reduce((sum, u) => sum + u.progress, 0) / uploads.length;
  const completedCount = uploads.filter(u => u.status === 'complete').length;
  const errorCount = uploads.filter(u => u.status === 'error').length;

  return (
    <div className="multi-upload-container">
      {/* Summary header */}
      <div className="upload-summary">
        <h3>Uploading {uploads.length} files</h3>
        <div className="summary-stats">
          <span>{completedCount} complete</span>
          {errorCount > 0 && <span className="error-count">{errorCount} failed</span>}
        </div>
        <div className="overall-progress">
          <div className="progress-track">
            <div
              className="progress-bar"
              style={{ width: `${totalProgress}%` }}
            />
          </div>
          <span className="progress-label">{Math.round(totalProgress)}%</span>
        </div>
      </div>

      {/* Upload list */}
      <div className="upload-list">
        {uploads.map(upload => (
          <UploadItem
            key={upload.id}
            upload={upload}
            onCancel={() => handleCancel(upload.id)}
            onRetry={() => handleRetry(upload.id)}
            onRemove={() => handleRemove(upload.id)}
          />
        ))}
      </div>

      {/* Actions */}
      <div className="upload-queue-actions">
        <button className="btn-secondary">
          Pause All
        </button>
        <button className="btn-primary">
          Add More Files
        </button>
      </div>
    </div>
  );
}

// Individual Upload Item Component
function UploadItem({ upload, onCancel, onRetry, onRemove }) {
  const getStatusIcon = () => {
    switch (upload.status) {
      case 'queued':
        return '⏳';
      case 'uploading':
        return '↑';
      case 'complete':
        return '✓';
      case 'error':
        return '✕';
      case 'cancelled':
        return '⊘';
      default:
        return '';
    }
  };

  return (
    <div className={`upload-item upload-${upload.status}`}>
      <div className="upload-item-icon">
        {getStatusIcon()}
      </div>

      <div className="upload-item-content">
        <div className="upload-item-name">{upload.file.name}</div>
        <div className="upload-item-progress">
          <div className="progress-track-small">
            <div
              className="progress-bar-small"
              style={{ width: `${upload.progress}%` }}
            />
          </div>
          <span className="progress-text-small">
            {upload.status === 'uploading' && `${Math.round(upload.progress)}%`}
            {upload.status === 'complete' && 'Complete'}
            {upload.status === 'error' && 'Failed'}
            {upload.status === 'queued' && 'Waiting...'}
          </span>
        </div>
      </div>

      <div className="upload-item-actions">
        {upload.status === 'uploading' && (
          <button onClick={onCancel} className="btn-icon-small">✕</button>
        )}
        {upload.status === 'error' && (
          <button onClick={onRetry} className="btn-icon-small">↻</button>
        )}
        {(upload.status === 'complete' || upload.status === 'error') && (
          <button onClick={onRemove} className="btn-icon-small">🗑</button>
        )}
      </div>
    </div>
  );
}

// Drag and Drop Upload with Progress
export function DragDropUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState([]);
  const dropZoneRef = useRef(null);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.target === dropZoneRef.current) {
      setIsDragging(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(prev => [...prev, ...droppedFiles]);
  };

  return (
    <div className="drag-drop-container">
      <div
        ref={dropZoneRef}
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <div className="drop-zone-content">
          <div className="drop-icon">📁</div>
          <p>Drag and drop files here</p>
          <p className="drop-hint">or</p>
          <label className="file-input-label">
            <input
              type="file"
              multiple
              onChange={(e) => setFiles(prev => [...prev, ...Array.from(e.target.files)])}
              className="file-input-hidden"
            />
            Browse Files
          </label>
        </div>
      </div>

      {files.length > 0 && (
        <MultiFileUploadQueue
          files={files}
          onAllComplete={() => console.log('All uploads complete')}
        />
      )}
    </div>
  );
}

// Helper function for file icons
function getFileIcon(mimeType) {
  if (!mimeType) return '📄';

  if (mimeType.startsWith('image/')) return '🖼️';
  if (mimeType.startsWith('video/')) return '🎬';
  if (mimeType.startsWith('audio/')) return '🎵';
  if (mimeType.includes('pdf')) return '📑';
  if (mimeType.includes('zip') || mimeType.includes('compressed')) return '🗜️';
  if (mimeType.includes('text')) return '📝';
  if (mimeType.includes('spreadsheet') || mimeType.includes('excel')) return '📊';
  if (mimeType.includes('presentation') || mimeType.includes('powerpoint')) return '📈';

  return '📄';
}

// Styles
const styles = `
  .upload-progress-container {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
  }

  .upload-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
  }

  .file-icon {
    font-size: 32px;
  }

  .file-info {
    flex: 1;
  }

  .file-name {
    font-weight: 500;
    margin-bottom: 4px;
  }

  .file-meta {
    font-size: 14px;
    color: #6b7280;
  }

  .separator {
    margin: 0 8px;
  }

  .progress-container {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .progress-track {
    flex: 1;
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-bar {
    height: 100%;
    background: #3b82f6;
    transition: width 0.3s ease;
  }

  .progress-bar.progress-complete {
    background: #10b981;
  }

  .progress-bar.progress-error {
    background: #ef4444;
  }

  .progress-label {
    font-size: 14px;
    font-weight: 500;
    min-width: 40px;
  }

  .upload-error {
    color: #ef4444;
    font-size: 14px;
    margin-top: 8px;
  }

  .upload-success {
    color: #10b981;
    font-size: 14px;
    margin-top: 8px;
  }

  /* Multi-upload styles */
  .multi-upload-container {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 24px;
  }

  .upload-summary {
    margin-bottom: 24px;
  }

  .summary-stats {
    display: flex;
    gap: 16px;
    margin: 8px 0;
    font-size: 14px;
    color: #6b7280;
  }

  .error-count {
    color: #ef4444;
  }

  .overall-progress {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 12px;
  }

  .upload-list {
    space-y: 8px;
    max-height: 400px;
    overflow-y: auto;
  }

  .upload-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: #f9fafb;
    border-radius: 6px;
    margin-bottom: 8px;
  }

  .upload-item-icon {
    font-size: 20px;
  }

  .upload-item-content {
    flex: 1;
  }

  .upload-item-name {
    font-size: 14px;
    margin-bottom: 4px;
  }

  .progress-track-small {
    height: 4px;
    background: #e5e7eb;
    border-radius: 2px;
    overflow: hidden;
    margin-top: 4px;
  }

  .progress-bar-small {
    height: 100%;
    background: #3b82f6;
    transition: width 0.3s ease;
  }

  .progress-text-small {
    font-size: 12px;
    color: #6b7280;
  }

  /* Drag and drop styles */
  .drop-zone {
    border: 2px dashed #cbd5e1;
    border-radius: 8px;
    padding: 48px;
    text-align: center;
    transition: all 0.3s ease;
  }

  .drop-zone.dragging {
    border-color: #3b82f6;
    background: #eff6ff;
  }

  .drop-zone-content {
    pointer-events: none;
  }

  .drop-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }

  .drop-hint {
    color: #6b7280;
    margin: 8px 0;
  }

  .file-input-label {
    display: inline-block;
    padding: 8px 16px;
    background: #3b82f6;
    color: white;
    border-radius: 6px;
    cursor: pointer;
    pointer-events: auto;
  }

  .file-input-hidden {
    display: none;
  }
`;