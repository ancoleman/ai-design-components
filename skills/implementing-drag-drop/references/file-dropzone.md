# File Upload Dropzone Implementation

## Table of Contents
- [Basic Dropzone](#basic-dropzone)
- [Visual Feedback States](#visual-feedback-states)
- [File Type Validation](#file-type-validation)
- [Multi-File Handling](#multi-file-handling)
- [Progress Indicators](#progress-indicators)
- [Advanced Features](#advanced-features)

## Basic Dropzone

### Core Implementation

```tsx
import { useDropzone } from 'react-dropzone';

function BasicDropzone({ onFilesAdded }) {
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
    acceptedFiles,
    rejectedFiles
  } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif'],
      'application/pdf': ['.pdf']
    },
    maxFiles: 10,
    maxSize: 5 * 1024 * 1024, // 5MB
    onDrop: (acceptedFiles, rejectedFiles) => {
      onFilesAdded(acceptedFiles);

      if (rejectedFiles.length > 0) {
        handleRejectedFiles(rejectedFiles);
      }
    }
  });

  return (
    <div
      {...getRootProps()}
      className={`dropzone
        ${isDragActive ? 'dropzone--active' : ''}
        ${isDragAccept ? 'dropzone--accept' : ''}
        ${isDragReject ? 'dropzone--reject' : ''}
      `}
    >
      <input {...getInputProps()} />

      {isDragActive ? (
        <p>Drop the files here...</p>
      ) : (
        <p>Drag 'n' drop files here, or click to select</p>
      )}

      <div className="dropzone-info">
        <span>Accepted: Images, PDFs</span>
        <span>Max size: 5MB</span>
        <span>Max files: 10</span>
      </div>
    </div>
  );
}
```

### Native HTML5 Implementation

```tsx
function NativeDropzone({ onFilesAdded }) {
  const [dragActive, setDragActive] = useState(false);
  const [dragCounter, setDragCounter] = useState(0);
  const dropRef = useRef<HTMLDivElement>(null);

  const handleDrag = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragIn = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragCounter(prev => prev + 1);

    if (e.dataTransfer?.items && e.dataTransfer.items.length > 0) {
      setDragActive(true);
    }
  };

  const handleDragOut = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragCounter(prev => prev - 1);

    if (dragCounter === 1) {
      setDragActive(false);
    }
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    setDragCounter(0);

    if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
      const files = Array.from(e.dataTransfer.files);
      onFilesAdded(files);
      e.dataTransfer.clearData();
    }
  };

  useEffect(() => {
    const div = dropRef.current;
    if (!div) return;

    div.addEventListener('dragenter', handleDragIn);
    div.addEventListener('dragleave', handleDragOut);
    div.addEventListener('dragover', handleDrag);
    div.addEventListener('drop', handleDrop);

    return () => {
      div.removeEventListener('dragenter', handleDragIn);
      div.removeEventListener('dragleave', handleDragOut);
      div.removeEventListener('dragover', handleDrag);
      div.removeEventListener('drop', handleDrop);
    };
  }, []);

  return (
    <div
      ref={dropRef}
      className={`native-dropzone ${dragActive ? 'drag-active' : ''}`}
    >
      <input
        type="file"
        id="file-input"
        multiple
        onChange={(e) => {
          if (e.target.files) {
            onFilesAdded(Array.from(e.target.files));
          }
        }}
        style={{ display: 'none' }}
      />

      <label htmlFor="file-input" className="dropzone-label">
        {dragActive ? (
          <div className="drag-active-content">
            <span>📥</span>
            <p>Release to upload</p>
          </div>
        ) : (
          <div className="default-content">
            <span>📁</span>
            <p>Drag files here or click to browse</p>
          </div>
        )}
      </label>
    </div>
  );
}
```

## Visual Feedback States

### State-Based Styling

```css
/* Base dropzone styles */
.dropzone {
  border: 2px dashed var(--drop-zone-border);
  border-radius: var(--drop-zone-border-radius);
  padding: var(--drop-zone-padding);
  background: var(--drop-zone-bg);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* Hovering with files */
.dropzone--active {
  border-color: var(--drop-zone-border-active);
  background: var(--drop-zone-bg-active);
  transform: scale(1.02);
  box-shadow: var(--shadow-lg);
}

/* Valid files being dragged */
.dropzone--accept {
  border-color: var(--color-success);
  background: var(--color-success-50);
}

/* Invalid files being dragged */
.dropzone--reject {
  border-color: var(--color-danger);
  background: var(--color-danger-50);
  animation: shake 0.5s;
}

/* Shake animation for rejection */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* File type indicators */
.file-type-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
}

.file-type-indicator--image {
  background: var(--color-blue-100);
  color: var(--color-blue-700);
}

.file-type-indicator--pdf {
  background: var(--color-red-100);
  color: var(--color-red-700);
}

.file-type-indicator--video {
  background: var(--color-purple-100);
  color: var(--color-purple-700);
}
```

### Enhanced Visual Feedback Component

```tsx
function EnhancedDropzone({ onFilesAdded, accept, maxSize }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [validationStatus, setValidationStatus] = useState<'valid' | 'invalid' | null>(null);

  const validateDraggedItems = (e: DragEvent) => {
    if (!e.dataTransfer?.items) return null;

    setIsValidating(true);

    const items = Array.from(e.dataTransfer.items);
    const hasValidFiles = items.some(item => {
      if (item.kind !== 'file') return false;

      const type = item.type;
      if (accept) {
        return Object.keys(accept).some(acceptType => {
          if (acceptType === '*/*') return true;
          return type.match(new RegExp(acceptType.replace('*', '.*')));
        });
      }
      return true;
    });

    setValidationStatus(hasValidFiles ? 'valid' : 'invalid');
    setIsValidating(false);

    return hasValidFiles;
  };

  return (
    <div
      className={`enhanced-dropzone
        ${isDragging ? 'dragging' : ''}
        ${validationStatus === 'valid' ? 'valid' : ''}
        ${validationStatus === 'invalid' ? 'invalid' : ''}
        ${isValidating ? 'validating' : ''}
      `}
      onDragEnter={(e) => {
        e.preventDefault();
        setIsDragging(true);
        validateDraggedItems(e);
      }}
      onDragLeave={(e) => {
        e.preventDefault();
        if (e.currentTarget === e.target) {
          setIsDragging(false);
          setValidationStatus(null);
        }
      }}
      onDragOver={(e) => {
        e.preventDefault();
      }}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        setValidationStatus(null);

        const files = Array.from(e.dataTransfer.files);
        onFilesAdded(files);
      }}
    >
      {/* Visual indicators */}
      <div className="dropzone-indicators">
        {isDragging && (
          <div className="drag-indicator">
            {isValidating && <span className="spinner" />}
            {validationStatus === 'valid' && <span className="checkmark">✓</span>}
            {validationStatus === 'invalid' && <span className="cross">✗</span>}
          </div>
        )}
      </div>

      {/* Content */}
      <div className="dropzone-content">
        {isDragging ? (
          <>
            {validationStatus === 'valid' && <p>Drop files to upload</p>}
            {validationStatus === 'invalid' && <p>Invalid file type</p>}
            {isValidating && <p>Checking files...</p>}
          </>
        ) : (
          <p>Drag and drop files here</p>
        )}
      </div>
    </div>
  );
}
```

## File Type Validation

### Comprehensive Validation

```tsx
interface FileValidationRules {
  accept?: Record<string, string[]>;
  maxSize?: number;
  minSize?: number;
  maxFiles?: number;
  validator?: (file: File) => boolean | Promise<boolean>;
}

function useFileValidation(rules: FileValidationRules) {
  const validateFile = async (file: File): Promise<{
    valid: boolean;
    errors: string[];
  }> => {
    const errors: string[] = [];

    // Type validation
    if (rules.accept) {
      const isValidType = Object.entries(rules.accept).some(([type, extensions]) => {
        if (type === '*/*') return true;

        // Check MIME type
        if (file.type.match(new RegExp(type.replace('*', '.*')))) {
          return true;
        }

        // Check extension
        const fileName = file.name.toLowerCase();
        return extensions.some(ext => fileName.endsWith(ext));
      });

      if (!isValidType) {
        errors.push(`File type not accepted: ${file.type || 'unknown'}`);
      }
    }

    // Size validation
    if (rules.maxSize && file.size > rules.maxSize) {
      errors.push(`File too large: ${formatFileSize(file.size)} (max: ${formatFileSize(rules.maxSize)})`);
    }

    if (rules.minSize && file.size < rules.minSize) {
      errors.push(`File too small: ${formatFileSize(file.size)} (min: ${formatFileSize(rules.minSize)})`);
    }

    // Custom validation
    if (rules.validator) {
      try {
        const isValid = await rules.validator(file);
        if (!isValid) {
          errors.push('File failed custom validation');
        }
      } catch (error) {
        errors.push(`Validation error: ${error.message}`);
      }
    }

    return {
      valid: errors.length === 0,
      errors
    };
  };

  const validateFiles = async (files: File[]): Promise<{
    accepted: File[];
    rejected: Array<{ file: File; errors: string[] }>;
  }> => {
    // Check max files
    if (rules.maxFiles && files.length > rules.maxFiles) {
      return {
        accepted: [],
        rejected: files.map(file => ({
          file,
          errors: [`Too many files. Maximum allowed: ${rules.maxFiles}`]
        }))
      };
    }

    const results = await Promise.all(
      files.map(async (file) => {
        const validation = await validateFile(file);
        return { file, ...validation };
      })
    );

    return {
      accepted: results.filter(r => r.valid).map(r => r.file),
      rejected: results.filter(r => !r.valid).map(r => ({
        file: r.file,
        errors: r.errors
      }))
    };
  };

  return { validateFile, validateFiles };
}
```

### Image-Specific Validation

```tsx
async function validateImage(file: File): Promise<boolean> {
  return new Promise((resolve) => {
    const img = new Image();
    const url = URL.createObjectURL(file);

    img.onload = () => {
      URL.revokeObjectURL(url);

      // Check dimensions
      const maxWidth = 4000;
      const maxHeight = 4000;
      const minWidth = 100;
      const minHeight = 100;

      if (img.width > maxWidth || img.height > maxHeight) {
        console.error(`Image too large: ${img.width}x${img.height}`);
        resolve(false);
      } else if (img.width < minWidth || img.height < minHeight) {
        console.error(`Image too small: ${img.width}x${img.height}`);
        resolve(false);
      } else {
        resolve(true);
      }
    };

    img.onerror = () => {
      URL.revokeObjectURL(url);
      resolve(false);
    };

    img.src = url;
  });
}
```

## Multi-File Handling

### File List Management

```tsx
interface FileWithMeta extends File {
  id: string;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress: number;
  error?: string;
  preview?: string;
}

function MultiFileDropzone() {
  const [files, setFiles] = useState<FileWithMeta[]>([]);

  const addFiles = (newFiles: File[]) => {
    const filesWithMeta: FileWithMeta[] = newFiles.map(file => ({
      ...file,
      id: generateId(),
      status: 'pending',
      progress: 0,
      preview: file.type.startsWith('image/')
        ? URL.createObjectURL(file)
        : undefined
    }));

    setFiles(prev => [...prev, ...filesWithMeta]);
  };

  const removeFile = (id: string) => {
    setFiles(prev => {
      const file = prev.find(f => f.id === id);
      if (file?.preview) {
        URL.revokeObjectURL(file.preview);
      }
      return prev.filter(f => f.id !== id);
    });
  };

  const updateFileStatus = (id: string, updates: Partial<FileWithMeta>) => {
    setFiles(prev =>
      prev.map(f => f.id === id ? { ...f, ...updates } : f)
    );
  };

  return (
    <div className="multi-file-dropzone">
      <BasicDropzone onFilesAdded={addFiles} />

      <div className="file-list">
        {files.map(file => (
          <FileItem
            key={file.id}
            file={file}
            onRemove={() => removeFile(file.id)}
            onRetry={() => uploadFile(file)}
          />
        ))}
      </div>

      {files.length > 0 && (
        <div className="file-actions">
          <button onClick={() => uploadAllFiles(files)}>
            Upload All
          </button>
          <button onClick={() => setFiles([])}>
            Clear All
          </button>
        </div>
      )}
    </div>
  );
}
```

### File Item Component

```tsx
function FileItem({ file, onRemove, onRetry }) {
  return (
    <div className={`file-item status-${file.status}`}>
      {/* Preview */}
      {file.preview && (
        <div className="file-preview">
          <img src={file.preview} alt={file.name} />
        </div>
      )}

      {/* File icon for non-images */}
      {!file.preview && (
        <div className="file-icon">
          {getFileIcon(file.type)}
        </div>
      )}

      {/* File info */}
      <div className="file-info">
        <div className="file-name">{file.name}</div>
        <div className="file-size">{formatFileSize(file.size)}</div>

        {/* Status indicator */}
        <div className="file-status">
          {file.status === 'uploading' && (
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${file.progress}%` }}
              />
            </div>
          )}
          {file.status === 'success' && <span className="success">✓ Uploaded</span>}
          {file.status === 'error' && (
            <span className="error">✗ {file.error}</span>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="file-actions">
        {file.status === 'error' && (
          <button onClick={onRetry} aria-label="Retry upload">
            🔄
          </button>
        )}
        <button onClick={onRemove} aria-label="Remove file">
          ✗
        </button>
      </div>
    </div>
  );
}
```

## Progress Indicators

### Upload Progress Tracking

```tsx
function useFileUpload() {
  const uploadFile = async (
    file: FileWithMeta,
    onProgress: (progress: number) => void
  ): Promise<void> => {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const formData = new FormData();
      formData.append('file', file);

      // Track upload progress
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const progress = (e.loaded / e.total) * 100;
          onProgress(progress);
        }
      });

      // Handle completion
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve();
        } else {
          reject(new Error(`Upload failed: ${xhr.status}`));
        }
      });

      // Handle errors
      xhr.addEventListener('error', () => {
        reject(new Error('Upload failed'));
      });

      // Send request
      xhr.open('POST', '/api/upload');
      xhr.send(formData);
    });
  };

  const uploadWithProgress = async (
    file: FileWithMeta,
    updateProgress: (id: string, progress: number) => void
  ) => {
    try {
      await uploadFile(file, (progress) => {
        updateProgress(file.id, progress);
      });
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  return { uploadFile, uploadWithProgress };
}
```

### Progress UI Components

```tsx
function CircularProgress({ progress, size = 60 }) {
  const circumference = 2 * Math.PI * 20;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <svg width={size} height={size} className="circular-progress">
      <circle
        cx={size / 2}
        cy={size / 2}
        r="20"
        fill="none"
        stroke="var(--color-gray-300)"
        strokeWidth="4"
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r="20"
        fill="none"
        stroke="var(--color-primary)"
        strokeWidth="4"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        style={{ transition: 'stroke-dashoffset 0.3s' }}
      />
      <text
        x={size / 2}
        y={size / 2}
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize="12"
      >
        {Math.round(progress)}%
      </text>
    </svg>
  );
}
```

## Advanced Features

### Paste from Clipboard

```tsx
function PasteableDropzone({ onFilesAdded }) {
  useEffect(() => {
    const handlePaste = async (e: ClipboardEvent) => {
      const items = Array.from(e.clipboardData?.items || []);
      const files: File[] = [];

      for (const item of items) {
        if (item.kind === 'file') {
          const file = item.getAsFile();
          if (file) files.push(file);
        } else if (item.type === 'text/html') {
          // Extract images from HTML
          const html = await new Promise<string>(resolve => {
            item.getAsString(resolve);
          });

          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          const images = doc.querySelectorAll('img');

          for (const img of images) {
            const response = await fetch(img.src);
            const blob = await response.blob();
            const file = new File([blob], 'pasted-image.png', { type: blob.type });
            files.push(file);
          }
        }
      }

      if (files.length > 0) {
        onFilesAdded(files);
      }
    };

    document.addEventListener('paste', handlePaste);
    return () => document.removeEventListener('paste', handlePaste);
  }, [onFilesAdded]);

  return (
    <div className="pasteable-dropzone">
      <p>Drag files here or paste from clipboard (Ctrl/Cmd+V)</p>
    </div>
  );
}
```

### Camera Capture

```tsx
function CameraDropzone({ onFilesAdded }) {
  const [showCamera, setShowCamera] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setShowCamera(true);
      }
    } catch (error) {
      console.error('Camera access denied:', error);
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context?.drawImage(video, 0, 0);

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `photo-${Date.now()}.jpg`, {
          type: 'image/jpeg'
        });
        onFilesAdded([file]);
        stopCamera();
      }
    }, 'image/jpeg', 0.9);
  };

  const stopCamera = () => {
    const stream = videoRef.current?.srcObject as MediaStream;
    stream?.getTracks().forEach(track => track.stop());
    setShowCamera(false);
  };

  return (
    <div className="camera-dropzone">
      <BasicDropzone onFilesAdded={onFilesAdded} />

      <button onClick={startCamera} className="camera-button">
        📷 Take Photo
      </button>

      {showCamera && (
        <div className="camera-modal">
          <video ref={videoRef} autoPlay playsInline />
          <canvas ref={canvasRef} style={{ display: 'none' }} />

          <div className="camera-controls">
            <button onClick={capturePhoto}>Capture</button>
            <button onClick={stopCamera}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}
```