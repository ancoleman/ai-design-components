import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

// File type with additional metadata
interface FileWithMeta extends File {
  id: string;
  preview?: string;
  progress: number;
  status: 'pending' | 'uploading' | 'success' | 'error';
  error?: string;
}

// File Dropzone Component
export function FileDropzone() {
  const [files, setFiles] = useState<FileWithMeta[]>([]);

  // Handle file drop
  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    // Process accepted files
    const newFiles: FileWithMeta[] = acceptedFiles.map((file) => ({
      ...file,
      id: `${file.name}-${Date.now()}`,
      preview: file.type.startsWith('image/')
        ? URL.createObjectURL(file)
        : undefined,
      progress: 0,
      status: 'pending' as const,
    } as FileWithMeta));

    setFiles((prev) => [...prev, ...newFiles]);

    // Handle rejected files
    if (rejectedFiles.length > 0) {
      const errors = rejectedFiles.map((rejection) => {
        const errors = rejection.errors.map((e: any) => e.message).join(', ');
        return `${rejection.file.name}: ${errors}`;
      });
      alert(`Some files were rejected:\n${errors.join('\n')}`);
    }

    // Start upload simulation
    newFiles.forEach((file) => {
      simulateUpload(file);
    });
  }, []);

  // Configure dropzone
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
    open,
  } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
      'application/pdf': ['.pdf'],
      'text/*': ['.txt', '.md', '.csv'],
      'application/vnd.openxmlformats-officedocument.*': ['.docx', '.xlsx'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    maxFiles: 10,
    multiple: true,
  });

  // Simulate file upload with progress
  const simulateUpload = (file: FileWithMeta) => {
    // Update status to uploading
    updateFileStatus(file.id, 'uploading');

    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 30;

      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);

        // Randomly succeed or fail (90% success rate)
        if (Math.random() > 0.1) {
          updateFileStatus(file.id, 'success');
        } else {
          updateFileStatus(file.id, 'error', 'Upload failed');
        }
      }

      updateFileProgress(file.id, Math.min(progress, 100));
    }, 500);
  };

  // Update file status
  const updateFileStatus = (
    id: string,
    status: FileWithMeta['status'],
    error?: string
  ) => {
    setFiles((prev) =>
      prev.map((file) =>
        file.id === id ? { ...file, status, error } : file
      )
    );
  };

  // Update file progress
  const updateFileProgress = (id: string, progress: number) => {
    setFiles((prev) =>
      prev.map((file) =>
        file.id === id ? { ...file, progress } : file
      )
    );
  };

  // Remove file
  const removeFile = (id: string) => {
    setFiles((prev) => {
      const file = prev.find((f) => f.id === id);
      if (file?.preview) {
        URL.revokeObjectURL(file.preview);
      }
      return prev.filter((f) => f.id !== id);
    });
  };

  // Retry failed upload
  const retryUpload = (file: FileWithMeta) => {
    updateFileStatus(file.id, 'pending');
    updateFileProgress(file.id, 0);
    simulateUpload(file);
  };

  // Clear all files
  const clearAll = () => {
    files.forEach((file) => {
      if (file.preview) {
        URL.revokeObjectURL(file.preview);
      }
    });
    setFiles([]);
  };

  return (
    <div className="dropzone-container">
      <h2>File Upload</h2>

      {/* Dropzone Area */}
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'drag-active' : ''} ${
          isDragAccept ? 'drag-accept' : ''
        } ${isDragReject ? 'drag-reject' : ''}`}
      >
        <input {...getInputProps()} />

        <div className="dropzone-content">
          {isDragActive ? (
            <>
              {isDragAccept && (
                <div className="drop-message accept">
                  <span className="drop-icon">📥</span>
                  <p>Drop files here to upload</p>
                </div>
              )}
              {isDragReject && (
                <div className="drop-message reject">
                  <span className="drop-icon">🚫</span>
                  <p>Some files are not accepted</p>
                </div>
              )}
            </>
          ) : (
            <div className="default-message">
              <span className="upload-icon">☁️</span>
              <h3>Drag & drop files here</h3>
              <p className="help-text">or click to browse</p>

              <div className="file-info">
                <span>Accepted: Images, PDFs, Documents</span>
                <span>Max size: 10MB per file</span>
                <span>Max files: 10</span>
              </div>

              <button
                type="button"
                onClick={open}
                className="browse-btn"
              >
                Browse Files
              </button>
            </div>
          )}
        </div>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="file-list">
          <div className="file-list-header">
            <h3>Files ({files.length})</h3>
            <button onClick={clearAll} className="clear-btn">
              Clear All
            </button>
          </div>

          {files.map((file) => (
            <FileItem
              key={file.id}
              file={file}
              onRemove={() => removeFile(file.id)}
              onRetry={() => retryUpload(file)}
            />
          ))}
        </div>
      )}

      {/* Upload Summary */}
      {files.length > 0 && (
        <UploadSummary files={files} />
      )}
    </div>
  );
}

// Individual File Item
function FileItem({
  file,
  onRemove,
  onRetry,
}: {
  file: FileWithMeta;
  onRemove: () => void;
  onRetry: () => void;
}) {
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const getFileIcon = (type: string) => {
    if (type.startsWith('image/')) return '🖼️';
    if (type === 'application/pdf') return '📄';
    if (type.startsWith('text/')) return '📝';
    return '📎';
  };

  return (
    <div className={`file-item status-${file.status}`}>
      {/* Preview or Icon */}
      <div className="file-preview">
        {file.preview ? (
          <img src={file.preview} alt={file.name} />
        ) : (
          <span className="file-icon">{getFileIcon(file.type)}</span>
        )}
      </div>

      {/* File Info */}
      <div className="file-info">
        <div className="file-name">{file.name}</div>
        <div className="file-meta">
          <span className="file-size">{formatFileSize(file.size)}</span>
          {file.status === 'success' && (
            <span className="success-badge">✓ Uploaded</span>
          )}
          {file.status === 'error' && (
            <span className="error-badge">✗ {file.error}</span>
          )}
        </div>

        {/* Progress Bar */}
        {file.status === 'uploading' && (
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${file.progress}%` }}
            />
            <span className="progress-text">{Math.round(file.progress)}%</span>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="file-actions">
        {file.status === 'error' && (
          <button
            onClick={onRetry}
            className="action-btn retry"
            aria-label="Retry upload"
          >
            🔄
          </button>
        )}
        <button
          onClick={onRemove}
          className="action-btn remove"
          aria-label="Remove file"
        >
          ✕
        </button>
      </div>
    </div>
  );
}

// Upload Summary
function UploadSummary({ files }: { files: FileWithMeta[] }) {
  const stats = {
    pending: files.filter((f) => f.status === 'pending').length,
    uploading: files.filter((f) => f.status === 'uploading').length,
    success: files.filter((f) => f.status === 'success').length,
    error: files.filter((f) => f.status === 'error').length,
  };

  const totalSize = files.reduce((sum, file) => sum + file.size, 0);

  return (
    <div className="upload-summary">
      <div className="stat">
        <span className="stat-label">Total Size:</span>
        <span className="stat-value">
          {(totalSize / (1024 * 1024)).toFixed(2)} MB
        </span>
      </div>
      {stats.pending > 0 && (
        <div className="stat">
          <span className="stat-label">Pending:</span>
          <span className="stat-value">{stats.pending}</span>
        </div>
      )}
      {stats.uploading > 0 && (
        <div className="stat">
          <span className="stat-label">Uploading:</span>
          <span className="stat-value">{stats.uploading}</span>
        </div>
      )}
      {stats.success > 0 && (
        <div className="stat success">
          <span className="stat-label">Completed:</span>
          <span className="stat-value">{stats.success}</span>
        </div>
      )}
      {stats.error > 0 && (
        <div className="stat error">
          <span className="stat-label">Failed:</span>
          <span className="stat-value">{stats.error}</span>
        </div>
      )}
    </div>
  );
}

// Styles
const styles = `
.dropzone-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.dropzone {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--color-white);
}

.dropzone:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-50);
}

.dropzone.drag-active {
  border-color: var(--color-primary);
  background: var(--color-primary-50);
  transform: scale(1.02);
}

.dropzone.drag-accept {
  border-color: var(--color-success);
  background: var(--color-success-50);
}

.dropzone.drag-reject {
  border-color: var(--color-danger);
  background: var(--color-danger-50);
  animation: shake 0.5s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.dropzone-content {
  pointer-events: none;
}

.drop-message {
  animation: fadeIn 0.3s;
}

.drop-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.upload-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
}

.help-text {
  color: var(--color-text-secondary);
  margin: 0.5rem 0 1.5rem;
}

.file-info {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 1rem 0;
  font-size: 0.875rem;
  color: var(--color-text-tertiary);
}

.browse-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.browse-btn:hover {
  background: var(--color-primary-600);
  transform: translateY(-2px);
}

.file-list {
  margin-top: 2rem;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 1rem;
}

.file-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 1rem;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: var(--color-gray-50);
  border-radius: var(--radius-md);
  margin-bottom: 0.5rem;
  transition: all 0.2s;
}

.file-item:hover {
  background: var(--color-gray-100);
}

.file-preview {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-white);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.file-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-icon {
  font-size: 1.5rem;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.file-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.progress-bar {
  position: relative;
  height: 4px;
  background: var(--color-gray-200);
  border-radius: 2px;
  margin-top: 0.5rem;
  overflow: hidden;
}

.progress-fill {
  position: absolute;
  height: 100%;
  background: var(--color-primary);
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  right: 0;
  top: -20px;
  font-size: 0.75rem;
  color: var(--color-text-tertiary);
}

.file-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.25rem 0.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.25rem;
  transition: all 0.2s;
}

.action-btn:hover {
  transform: scale(1.1);
}

.upload-summary {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  margin-top: 1rem;
  background: var(--color-gray-50);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
}

.stat {
  display: flex;
  gap: 0.5rem;
}

.stat-label {
  color: var(--color-text-secondary);
}

.stat-value {
  font-weight: 600;
}

.stat.success .stat-value {
  color: var(--color-success);
}

.stat.error .stat-value {
  color: var(--color-danger);
}
`;