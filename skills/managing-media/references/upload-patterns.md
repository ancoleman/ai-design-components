# File Upload Patterns

## Basic Drag-and-Drop Upload

### HTML Structure
```html
<div class="upload-zone" ondrop ondragover>
  <input type="file" id="file-input" hidden />
  <label for="file-input">
    Click to browse or drag and drop
  </label>
</div>
```

### Features
- Visual feedback on drag over
- File type validation
- Size validation
- Preview thumbnails
- Progress indicator

## Multi-File Upload

### Queue Management
- Parallel uploads (max 3-5 concurrent)
- Individual progress tracking
- Cancel individual uploads
- Retry failed uploads

### UI Components
- File list with status
- Overall progress
- Bulk actions (cancel all, retry all)

## Validation Patterns

### Client-Side Validation
```javascript
const validateFile = (file) => {
  const maxSize = 10 * 1024 * 1024; // 10MB
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];

  if (file.size > maxSize) {
    return { valid: false, error: 'File too large (max 10MB)' };
  }

  if (!allowedTypes.includes(file.type)) {
    return { valid: false, error: 'Invalid file type' };
  }

  return { valid: true };
};
```

## Chunked Upload

For files >10MB:
1. Split file into chunks (1-5MB each)
2. Upload chunks sequentially or parallel
3. Track progress across chunks
4. Resume from last successful chunk on failure

### Implementation
```javascript
const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB
const chunks = Math.ceil(file.size / CHUNK_SIZE);

for (let i = 0; i < chunks; i++) {
  const chunk = file.slice(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE);
  await uploadChunk(chunk, i, chunks);
}
```

## Accessibility

- Keyboard accessible file input
- ARIA labels for buttons
- Status announcements via aria-live
- Clear error messages
- Focus management

## See Also
- `advanced-upload.md` - Chunked and resumable uploads
- `image-upload.md` - Image-specific patterns
- `cloud-storage.md` - Direct cloud uploads
