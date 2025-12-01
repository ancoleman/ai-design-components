/**
 * File Upload with Preview Example
 *
 * Demonstrates:
 * - Image upload with preview
 * - File type validation
 * - File size validation
 * - Drag-and-drop support
 * - Multiple file handling
 * - Accessibility (keyboard, screen readers)
 */

import { useForm, Controller } from 'react-hook-form';
import { useState } from 'react';

interface FileWithPreview extends File {
  preview?: string;
}

interface FormData {
  images: FileList;
  title: string;
  description: string;
}

export default function FileUploadForm() {
  const [previews, setPreviews] = useState<string[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    setValue,
    watch,
  } = useForm<FormData>();

  const files = watch('images');

  const handleFileChange = (fileList: FileList | null) => {
    if (!fileList || fileList.length === 0) {
      setPreviews([]);
      return;
    }

    // Validate file types and sizes
    const validFiles: File[] = [];
    const newPreviews: string[] = [];

    Array.from(fileList).forEach((file) => {
      // Check file type
      if (!file.type.startsWith('image/')) {
        alert(`${file.name} is not an image file`);
        return;
      }

      // Check file size (5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        alert(`${file.name} is too large. Maximum size is 5MB`);
        return;
      }

      validFiles.push(file);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        newPreviews.push(reader.result as string);
        setPreviews([...newPreviews]);
      };
      reader.readAsDataURL(file);
    });
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFiles = e.dataTransfer.files;
    setValue('images', droppedFiles);
    handleFileChange(droppedFiles);
  };

  const removeImage = (index: number) => {
    const newPreviews = previews.filter((_, i) => i !== index);
    setPreviews(newPreviews);

    // Note: Removing from FileList is complex, better to track separately
    // In production, maintain separate array of File objects
  };

  const onSubmit = (data: FormData) => {
    console.log('Form data:', data);
    console.log('Files:', Array.from(data.images));
    // Upload files to server...
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <h2>Upload Images</h2>

      {/* Title */}
      <div style={{ marginBottom: '24px' }}>
        <label htmlFor="title" style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          Title *
        </label>
        <input
          id="title"
          {...register('title', {
            required: 'Title is required',
            minLength: { value: 3, message: 'Title must be at least 3 characters' },
          })}
          style={{
            width: '100%',
            padding: '12px',
            border: `2px solid ${errors.title ? '#EF4444' : '#D1D5DB'}`,
            borderRadius: '8px',
          }}
        />
        {errors.title && (
          <p role="alert" style={{ color: '#EF4444', fontSize: '14px', marginTop: '8px' }}>
            {errors.title.message}
          </p>
        )}
      </div>

      {/* File Upload */}
      <div style={{ marginBottom: '24px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          Images * (Max 5MB each, JPG/PNG only)
        </label>

        {/* Drag-and-drop zone */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          style={{
            border: `2px dashed ${isDragging ? '#3B82F6' : '#D1D5DB'}`,
            borderRadius: '8px',
            padding: '32px',
            textAlign: 'center',
            backgroundColor: isDragging ? '#EFF6FF' : '#F9FAFB',
            cursor: 'pointer',
            transition: 'all 0.2s',
          }}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <input
            id="file-input"
            type="file"
            accept="image/*"
            multiple
            {...register('images', {
              required: 'At least one image is required',
              onChange: (e) => handleFileChange(e.target.files),
            })}
            style={{ display: 'none' }}
          />

          <div style={{ fontSize: '48px', marginBottom: '16px' }}>📁</div>
          <p style={{ margin: 0, fontSize: '16px', color: '#6B7280' }}>
            {isDragging ? 'Drop files here' : 'Drag and drop images here, or click to browse'}
          </p>
          <p style={{ margin: '8px 0 0 0', fontSize: '14px', color: '#9CA3AF' }}>
            Supports: JPG, PNG, GIF (Max 5MB per file)
          </p>
        </div>

        {errors.images && (
          <p role="alert" style={{ color: '#EF4444', fontSize: '14px', marginTop: '8px' }}>
            {errors.images.message}
          </p>
        )}
      </div>

      {/* Image Previews */}
      {previews.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <p style={{ fontWeight: '500', marginBottom: '12px' }}>
            Previews ({previews.length} image{previews.length > 1 ? 's' : ''})
          </p>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
            gap: '16px',
          }}>
            {previews.map((preview, index) => (
              <div
                key={index}
                style={{
                  position: 'relative',
                  aspectRatio: '1',
                  borderRadius: '8px',
                  overflow: 'hidden',
                  border: '2px solid #D1D5DB',
                }}
              >
                <img
                  src={preview}
                  alt={`Preview ${index + 1}`}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                  }}
                />
                <button
                  type="button"
                  onClick={() => removeImage(index)}
                  aria-label={`Remove image ${index + 1}`}
                  style={{
                    position: 'absolute',
                    top: '8px',
                    right: '8px',
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    border: 'none',
                    backgroundColor: 'rgba(0, 0, 0, 0.6)',
                    color: 'white',
                    fontSize: '18px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Description */}
      <div style={{ marginBottom: '24px' }}>
        <label htmlFor="description" style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          Description
        </label>
        <textarea
          id="description"
          {...register('description')}
          rows={4}
          placeholder="Describe your images..."
          style={{
            width: '100%',
            padding: '12px',
            border: '2px solid #D1D5DB',
            borderRadius: '8px',
            fontSize: '16px',
            resize: 'vertical',
          }}
        />
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={isSubmitting}
        style={{
          width: '100%',
          padding: '12px 24px',
          backgroundColor: '#3B82F6',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          fontSize: '16px',
          fontWeight: '500',
          cursor: 'pointer',
          opacity: isSubmitting ? 0.6 : 1,
        }}
      >
        {isSubmitting ? 'Uploading...' : 'Upload Images'}
      </button>
    </form>
  );
}
```
