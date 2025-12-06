# Advanced Upload Patterns

Chunked uploads, resumable uploads, and multi-file queue management for large files.


## Table of Contents

- [Chunked Upload (Large Files >100MB)](#chunked-upload-large-files-100mb)
- [Resumable Upload](#resumable-upload)
- [Parallel Upload Queue](#parallel-upload-queue)
- [Best Practices](#best-practices)
- [Resources](#resources)

## Chunked Upload (Large Files >100MB)

```tsx
async function uploadInChunks(file: File, chunkSize = 5 * 1024 * 1024) {  // 5MB chunks
  const totalChunks = Math.ceil(file.size / chunkSize);

  for (let i = 0; i < totalChunks; i++) {
    const start = i * chunkSize;
    const end = Math.min(start + chunkSize, file.size);
    const chunk = file.slice(start, end);

    await fetch('/api/upload/chunk', {
      method: 'POST',
      headers: {
        'X-Upload-ID': uploadId,
        'X-Chunk-Index': i.toString(),
        'X-Total-Chunks': totalChunks.toString(),
      },
      body: chunk,
    });

    setProgress(((i + 1) / totalChunks) * 100);
  }
}
```

## Resumable Upload

```tsx
function ResumableUpload({ file }: { file: File }) {
  const [uploadedChunks, setUploadedChunks] = useState<Set<number>>(new Set());

  const resume = async () => {
    // Get already uploaded chunks from server
    const { uploadedChunks: existing } = await fetch(`/api/upload/status/${uploadId}`).then(r => r.json());

    setUploadedChunks(new Set(existing));

    // Upload remaining chunks
    for (let i = 0; i < totalChunks; i++) {
      if (!uploadedChunks.has(i)) {
        await uploadChunk(i);
      }
    }
  };

  return (
    <div>
      <button onClick={resume}>Resume Upload</button>
      <span>{uploadedChunks.size} / {totalChunks} chunks uploaded</span>
    </div>
  );
}
```

## Parallel Upload Queue

```tsx
import PQueue from 'p-queue';

function MultiFileUpload({ files }: { files: File[] }) {
  const [queue] = useState(() => new PQueue({ concurrency: 3 }));  // 3 simultaneous uploads
  const [progress, setProgress] = useState<Map<string, number>>(new Map());

  const uploadFiles = async () => {
    const tasks = files.map((file) =>
      queue.add(async () => {
        await uploadFile(file, (percent) => {
          setProgress((prev) => new Map(prev).set(file.name, percent));
        });
      })
    );

    await Promise.all(tasks);
  };

  return (
    <div>
      {files.map((file) => (
        <div key={file.name}>
          <span>{file.name}</span>
          <progress value={progress.get(file.name) || 0} max={100} />
        </div>
      ))}
    </div>
  );
}
```

## Best Practices

1. **Chunk large files** - >100MB files into 5-10MB chunks
2. **Resume capability** - Track uploaded chunks
3. **Parallel uploads** - Limit concurrency (3-5 max)
4. **Progress tracking** - Per-file and overall
5. **Error retry** - Exponential backoff
6. **Cancel capability** - Allow user to abort

## Resources

- tus.js (resumable): https://github.com/tus/tus-js-client
- Uppy: https://uppy.io/
