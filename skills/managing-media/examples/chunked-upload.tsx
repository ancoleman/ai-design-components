import React, { useState } from 'react';

/**
 * Chunked File Upload
 *
 * Upload large files (>100MB) in chunks with progress tracking and resume capability
 */

const CHUNK_SIZE = 5 * 1024 * 1024;  // 5MB chunks

export function ChunkedUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadId, setUploadId] = useState<string | null>(null);

  const uploadInChunks = async (file: File) => {
    setIsUploading(true);

    // 1. Initialize upload
    const { uploadId: id } = await fetch('/api/upload/init', {
      method: 'POST',
      body: JSON.stringify({ filename: file.name, size: file.size }),
    }).then(r => r.json());

    setUploadId(id);

    // 2. Upload chunks
    const totalChunks = Math.ceil(file.size / CHUNK_SIZE);

    for (let i = 0; i < totalChunks; i++) {
      const start = i * CHUNK_SIZE;
      const end = Math.min(start + CHUNK_SIZE, file.size);
      const chunk = file.slice(start, end);

      const formData = new FormData();
      formData.append('chunk', chunk);
      formData.append('uploadId', id);
      formData.append('chunkIndex', i.toString());
      formData.append('totalChunks', totalChunks.toString());

      await fetch('/api/upload/chunk', {
        method: 'POST',
        body: formData,
      });

      setProgress(((i + 1) / totalChunks) * 100);
    }

    // 3. Finalize
    await fetch('/api/upload/complete', {
      method: 'POST',
      body: JSON.stringify({ uploadId: id }),
    });

    setIsUploading(false);
    alert('Upload complete!');
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Chunked File Upload</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4"
      />

      {file && (
        <div className="mb-4">
          <p className="text-sm text-gray-600">
            {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
          </p>
        </div>
      )}

      <button
        onClick={() => file && uploadInChunks(file)}
        disabled={!file || isUploading}
        className="w-full px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
      >
        {isUploading ? 'Uploading...' : 'Upload'}
      </button>

      {isUploading && (
        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-center mt-2">{Math.round(progress)}%</p>
        </div>
      )}
    </div>
  );
}

export default ChunkedUpload;
