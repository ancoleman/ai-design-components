# Multi-Modal AI Chat Patterns

Implement chat interfaces that handle text, images, audio, video, and file uploads for AI models like GPT-4 Vision, Gemini, and Claude.


## Table of Contents

- [Supported Modalities](#supported-modalities)
- [Image Input](#image-input)
  - [Upload + Preview](#upload-preview)
  - [Send to API](#send-to-api)
- [Audio Input (Voice)](#audio-input-voice)
  - [Record Audio](#record-audio)
- [File Upload (Documents)](#file-upload-documents)
- [Multi-Modal Message Display](#multi-modal-message-display)
- [Camera Capture (Mobile)](#camera-capture-mobile)
- [Drag-and-Drop Upload](#drag-and-drop-upload)
- [Best Practices](#best-practices)
- [Resources](#resources)

## Supported Modalities

| Modality | Use Case | Models Supporting | Max Size |
|----------|----------|-------------------|----------|
| **Text** | Standard chat | All | N/A |
| **Images** | Image analysis, OCR, visual QA | GPT-4V, Claude 3, Gemini Pro Vision | 20MB |
| **Audio** | Voice input, transcription | Whisper, Gemini | 25MB |
| **Video** | Video analysis, frame extraction | Gemini Pro Vision | 100MB |
| **Documents** | PDF/DOCX analysis | Claude (via RAG), GPT-4V (images) | Varies |

## Image Input

### Upload + Preview

```tsx
function ImageInput({ onImageSelect }: Props) {
  const [preview, setPreview] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file');
      return;
    }

    if (file.size > 20 * 1024 * 1024) {
      alert('Image must be <20MB');
      return;
    }

    // Preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64 = e.target?.result as string;
      setPreview(base64);
      onImageSelect(base64);
    };
    reader.readAsDataURL(file);
  };

  return (
    <div>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
        id="image-upload"
      />
      <label
        htmlFor="image-upload"
        className="cursor-pointer px-4 py-2 bg-blue-500 text-white rounded"
      >
        📷 Upload Image
      </label>

      {preview && (
        <div className="mt-4">
          <img
            src={preview}
            alt="Preview"
            className="max-w-sm rounded-lg border"
          />
          <button onClick={() => setPreview(null)}>Remove</button>
        </div>
      )}
    </div>
  );
}
```

### Send to API

```tsx
async function sendImageMessage(text: string, imageBase64: string) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text },
            {
              type: 'image_url',
              image_url: { url: imageBase64 },
            },
          ],
        },
      ],
    }),
  });

  return response.json();
}
```

## Audio Input (Voice)

### Record Audio

```tsx
import { useState, useRef } from 'react';

function VoiceInput({ onTranscript }: Props) {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (e) => {
      chunksRef.current.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
      chunksRef.current = [];

      // Send to Whisper API for transcription
      const transcript = await transcribeAudio(audioBlob);
      onTranscript(transcript);

      stream.getTracks().forEach((track) => track.stop());
    };

    mediaRecorder.start();
    mediaRecorderRef.current = mediaRecorder;
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  return (
    <button
      onClick={isRecording ? stopRecording : startRecording}
      className={isRecording ? 'recording' : ''}
    >
      {isRecording ? '⬛ Stop' : '🎤 Record'}
    </button>
  );
}

async function transcribeAudio(audioBlob: Blob): Promise<string> {
  const formData = new FormData();
  formData.append('file', audioBlob, 'audio.webm');
  formData.append('model', 'whisper-1');

  const response = await fetch('https://api.openai.com/v1/audio/transcriptions', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${process.env.OPENAI_API_KEY}` },
    body: formData,
  });

  const data = await response.json();
  return data.text;
}
```

## File Upload (Documents)

```tsx
function FileInput({ onFileSelect }: Props) {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    // Validate file type
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain',
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      alert('Unsupported file type');
      return;
    }

    setFile(selectedFile);
    onFileSelect(selectedFile);
  };

  return (
    <div>
      <input
        type="file"
        accept=".pdf,.doc,.docx,.txt"
        onChange={handleFileChange}
        id="file-upload"
        className="hidden"
      />
      <label htmlFor="file-upload" className="cursor-pointer">
        📎 Attach File
      </label>

      {file && (
        <div className="file-preview">
          <span>{file.name}</span>
          <span>{(file.size / 1024).toFixed(1)} KB</span>
          <button onClick={() => setFile(null)}>×</button>
        </div>
      )}
    </div>
  );
}
```

## Multi-Modal Message Display

```tsx
function MultiModalMessage({ message }: { message: Message }) {
  return (
    <div className="message">
      {/* Text content */}
      {message.text && <div className="prose">{message.text}</div>}

      {/* Images */}
      {message.images?.map((img, i) => (
        <img
          key={i}
          src={img.url}
          alt={img.description || 'User uploaded image'}
          className="max-w-md rounded-lg mt-2"
        />
      ))}

      {/* Audio */}
      {message.audio && (
        <audio controls className="mt-2">
          <source src={message.audio.url} type="audio/mpeg" />
        </audio>
      )}

      {/* File attachments */}
      {message.files?.map((file) => (
        <div key={file.id} className="file-attachment">
          <span>{file.name}</span>
          <a href={file.url} download>
            Download
          </a>
        </div>
      ))}
    </div>
  );
}
```

## Camera Capture (Mobile)

```tsx
function CameraInput({ onCapture }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);

  const startCamera = async () => {
    const mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment' },  // Back camera on mobile
    });

    if (videoRef.current) {
      videoRef.current.srcObject = mediaStream;
      setStream(mediaStream);
    }
  };

  const capturePhoto = () => {
    const canvas = document.createElement('canvas');
    const video = videoRef.current!;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d')!;
    ctx.drawImage(video, 0, 0);

    canvas.toBlob((blob) => {
      onCapture(blob!);
      stopCamera();
    }, 'image/jpeg', 0.9);
  };

  const stopCamera = () => {
    stream?.getTracks().forEach((track) => track.stop());
    setStream(null);
  };

  return (
    <div>
      <button onClick={startCamera}>📷 Open Camera</button>

      {stream && (
        <div>
          <video ref={videoRef} autoPlay playsInline />
          <button onClick={capturePhoto}>Capture</button>
          <button onClick={stopCamera}>Cancel</button>
        </div>
      )}
    </div>
  );
}
```

## Drag-and-Drop Upload

```tsx
function DragDropUpload({ onFilesSelected }: Props) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    onFilesSelected(files);
  };

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      className={isDragging ? 'border-blue-500 bg-blue-50' : ''}
    >
      Drop files here or click to upload
    </div>
  );
}
```

## Best Practices

1. **Validate file types** - Check MIME type and extension
2. **Enforce size limits** - Prevent large uploads
3. **Show previews** - Let users confirm before sending
4. **Compress images** - Client-side compression before upload
5. **Handle errors** - Clear messages for unsupported formats
6. **Loading states** - Show progress during upload
7. **Allow removal** - Users can remove attachments before send
8. **Mobile-friendly** - Camera access, photo library
9. **Accessibility** - Alt text, ARIA labels
10. **Secure upload** - Validate server-side, scan for malware

## Resources

- GPT-4 Vision: https://platform.openai.com/docs/guides/vision
- Claude Vision: https://docs.anthropic.com/claude/docs/vision
- Gemini Multimodal: https://ai.google.dev/gemini-api/docs/vision
