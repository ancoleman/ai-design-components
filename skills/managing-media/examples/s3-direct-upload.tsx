import React, { useState } from 'react';

/**
 * S3 Direct Upload Example
 *
 * Upload files directly to S3 using pre-signed URLs (bypasses backend)
 */

export function S3DirectUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const uploadToS3 = async () => {
    if (!file) return;

    setUploading(true);

    try {
      // 1. Get pre-signed URL from backend
      const { url, fields, key } = await fetch('/api/upload/presign', {
        method: 'POST',
        body: JSON.stringify({
          filename: file.name,
          contentType: file.type,
        }),
      }).then(r => r.json());

      // 2. Upload directly to S3
      const formData = new FormData();
      Object.entries(fields).forEach(([k, v]) => formData.append(k, v as string));
      formData.append('file', file);

      const xhr = new XMLHttpRequest();

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          setProgress((e.loaded / e.total) * 100);
        }
      });

      xhr.addEventListener('load', () => {
        if (xhr.status === 204) {
          alert('Upload successful!');
          console.log('File key:', key);
        }
      });

      xhr.open('POST', url);
      xhr.send(formData);

    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">S3 Direct Upload</h2>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="mb-4"
        />

        {file && <p className="text-sm text-gray-600 mb-4">{file.name}</p>}

        <button
          onClick={uploadToS3}
          disabled={!file || uploading}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
        >
          {uploading ? `Uploading... ${Math.round(progress)}%` : 'Upload to S3'}
        </button>
      </div>

      {uploading && (
        <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-500 h-2 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}

export default S3DirectUpload;
