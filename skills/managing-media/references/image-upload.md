# Image Upload Patterns

Client-side image upload with validation, preview, and optimization.


## Table of Contents

- [Basic Upload with Preview](#basic-upload-with-preview)
- [Drag and Drop](#drag-and-drop)
- [Client-Side Compression](#client-side-compression)
- [Multiple File Upload](#multiple-file-upload)
- [Progress Indicator](#progress-indicator)
- [Best Practices](#best-practices)

## Basic Upload with Preview

```tsx
function ImageUpload({ onUpload }: { onUpload: (file: File) => void }) {
  const [preview, setPreview] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {  // 10MB
      alert('Image must be <10MB');
      return;
    }

    // Preview
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target?.result as string);
    reader.readAsDataURL(file);

    onUpload(file);
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {preview && <img src={preview} alt="Preview" style={{ maxWidth: '300px' }} />}
    </div>
  );
}
```

## Drag and Drop

```tsx
function DragDropUpload({ onUpload }: Props) {
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        const files = Array.from(e.dataTransfer.files);
        files.forEach(onUpload);
      }}
      className={`border-2 border-dashed p-8 ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
    >
      Drag images here or click to upload
    </div>
  );
}
```

## Client-Side Compression

```tsx
async function compressImage(file: File, maxWidth: number = 1920): Promise<Blob> {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const scale = Math.min(1, maxWidth / img.width);

      canvas.width = img.width * scale;
      canvas.height = img.height * scale;

      const ctx = canvas.getContext('2d')!;
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => resolve(blob!), 'image/jpeg', 0.85);
    };
    img.src = URL.createObjectURL(file);
  });
}
```

## Multiple File Upload

```tsx
function MultipleImageUpload() {
  const [files, setFiles] = useState<File[]>([]);

  const handleMultipleFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = Array.from(e.target.files || []);
    setFiles((prev) => [...prev, ...selected]);
  };

  return (
    <div>
      <input type="file" multiple accept="image/*" onChange={handleMultipleFiles} />

      <div className="grid grid-cols-3 gap-4 mt-4">
        {files.map((file, i) => (
          <div key={i} className="relative">
            <img src={URL.createObjectURL(file)} alt={file.name} />
            <button
              onClick={() => setFiles(files.filter((_, idx) => idx !== i))}
              className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6"
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Progress Indicator

```tsx
function UploadWithProgress({ file }: { file: File }) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        setProgress((e.loaded / e.total) * 100);
      }
    });

    const formData = new FormData();
    formData.append('file', file);

    xhr.open('POST', '/api/upload');
    xhr.send(formData);
  }, [file]);

  return (
    <div className="w-full bg-gray-200 rounded">
      <div
        className="bg-blue-500 h-2 rounded transition-all"
        style={{ width: `${progress}%` }}
      />
      <span className="text-sm">{Math.round(progress)}%</span>
    </div>
  );
}
```

## Best Practices

1. **Validate client-side** - File type, size, dimensions
2. **Show preview** - Let users confirm before upload
3. **Compress images** - Reduce bandwidth
4. **Progress indicator** - For uploads >1MB
5. **Allow removal** - Before submission
6. **Handle errors** - Network failures, validation
7. **Multiple files** - Support batch upload
8. **Drag and drop** - Better UX than file picker
