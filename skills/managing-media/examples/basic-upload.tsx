// Basic File Upload with Drag-and-Drop
// Example implementation using react-dropzone

import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export function BasicFileUpload() {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    // Handle file upload
    acceptedFiles.forEach((file) => {
      console.log('Uploading:', file.name);
      // Add upload logic here
    });
  }, []);

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragReject
  } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    maxFiles: 5
  });

  return (
    <div
      {...getRootProps()}
      className={`
        upload-zone
        ${isDragActive ? 'drag-active' : ''}
        ${isDragReject ? 'drag-reject' : ''}
      `}
      style={{
        border: 'var(--upload-zone-border)',
        background: 'var(--upload-zone-bg)',
        padding: 'var(--upload-zone-padding)',
        borderRadius: 'var(--upload-zone-border-radius)',
        textAlign: 'center',
        cursor: 'pointer'
      }}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop files here...</p>
      ) : (
        <div>
          <p>Drag and drop files here, or click to browse</p>
          <p className="hint">Maximum 5 files, 10MB each. Accepts JPG, PNG, WebP.</p>
        </div>
      )}
    </div>
  );
}

// Example usage:
// <BasicFileUpload />
