# Multi-Modal Input & Output Patterns

## Table of Contents

- [Image Handling](#image-handling)
- [File Attachments](#file-attachments)
- [Voice Input & Output](#voice-input--output)
- [Screen Sharing & Recording](#screen-sharing--recording)
- [Collaborative Whiteboard](#collaborative-whiteboard)
- [Video Input](#video-input)
- [Multi-Modal Message Display](#multi-modal-message-display)
- [Drag & Drop Support](#drag--drop-support)

## Image Handling

### Image Upload Interface

Support multiple ways to add images:

```tsx
function ImageUploadInterface({ onImagesAdded, maxSize = 10 * 1024 * 1024 }) {
  const [previews, setPreviews] = useState<ImagePreview[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file selection
  const handleFileSelect = async (files: FileList | File[]) => {
    const validImages: File[] = [];
    const errors: string[] = [];

    for (const file of Array.from(files)) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        errors.push(`${file.name} is not an image`);
        continue;
      }

      // Validate file size
      if (file.size > maxSize) {
        errors.push(`${file.name} exceeds ${maxSize / 1024 / 1024}MB limit`);
        continue;
      }

      validImages.push(file);
    }

    // Show errors if any
    if (errors.length > 0) {
      showToast(errors.join('\n'), 'error');
    }

    // Create previews
    const newPreviews = await Promise.all(
      validImages.map(async (file) => ({
        id: crypto.randomUUID(),
        file,
        url: URL.createObjectURL(file),
        name: file.name,
        size: file.size,
        dimensions: await getImageDimensions(file)
      }))
    );

    setPreviews(prev => [...prev, ...newPreviews]);
  };

  // Paste from clipboard
  const handlePaste = useCallback((e: ClipboardEvent) => {
    const items = Array.from(e.clipboardData?.items || []);
    const imageItems = items.filter(item => item.type.startsWith('image/'));

    if (imageItems.length > 0) {
      e.preventDefault();
      const files = imageItems.map(item => item.getAsFile()).filter(Boolean) as File[];
      handleFileSelect(files);
    }
  }, []);

  // Camera capture (mobile)
  const handleCameraCapture = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.capture = 'environment'; // or 'user' for front camera
    input.onchange = (e) => {
      const files = (e.target as HTMLInputElement).files;
      if (files) handleFileSelect(files);
    };
    input.click();
  };

  // URL input
  const handleURLInput = async (url: string) => {
    try {
      setUploading(true);
      const response = await fetch(url);
      const blob = await response.blob();

      if (!blob.type.startsWith('image/')) {
        throw new Error('URL does not point to an image');
      }

      const file = new File([blob], getFilenameFromURL(url), { type: blob.type });
      handleFileSelect([file]);
    } catch (error) {
      showToast(`Failed to load image from URL: ${error.message}`, 'error');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="image-upload-interface">
      {/* Preview Gallery */}
      {previews.length > 0 && (
        <div className="image-preview-gallery">
          {previews.map(preview => (
            <ImagePreviewCard
              key={preview.id}
              preview={preview}
              onRemove={() => {
                setPreviews(prev => prev.filter(p => p.id !== preview.id));
                URL.revokeObjectURL(preview.url);
              }}
              onEdit={() => openImageEditor(preview)}
            />
          ))}
        </div>
      )}

      {/* Upload Controls */}
      <div className="upload-controls">
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          hidden
          onChange={(e) => e.target.files && handleFileSelect(e.target.files)}
        />

        <button
          onClick={() => fileInputRef.current?.click()}
          className="upload-btn"
        >
          <UploadIcon /> Upload Images
        </button>

        <button onClick={handleCameraCapture} className="camera-btn">
          <CameraIcon /> Take Photo
        </button>

        <button
          onClick={() => {
            const url = prompt('Enter image URL:');
            if (url) handleURLInput(url);
          }}
          className="url-btn"
        >
          <LinkIcon /> From URL
        </button>
      </div>

      {/* Paste hint */}
      <div className="paste-hint">
        <KeyboardIcon /> Press Ctrl+V to paste images from clipboard
      </div>
    </div>
  );
}
```

### Image Preview Component

Display images with zoom and metadata:

```tsx
function ImagePreviewCard({ preview, onRemove, onEdit }) {
  const [showLightbox, setShowLightbox] = useState(false);

  return (
    <>
      <div className="image-preview-card">
        <img
          src={preview.url}
          alt={preview.name}
          onClick={() => setShowLightbox(true)}
          className="preview-thumbnail"
        />

        <div className="preview-overlay">
          <button onClick={onEdit} aria-label="Edit image">
            <EditIcon />
          </button>
          <button onClick={onRemove} aria-label="Remove image">
            <CloseIcon />
          </button>
        </div>

        <div className="preview-info">
          <span className="filename">{truncate(preview.name, 20)}</span>
          <span className="filesize">{formatBytes(preview.size)}</span>
          {preview.dimensions && (
            <span className="dimensions">
              {preview.dimensions.width}×{preview.dimensions.height}
            </span>
          )}
        </div>
      </div>

      {showLightbox && (
        <ImageLightbox
          image={preview}
          onClose={() => setShowLightbox(false)}
        />
      )}
    </>
  );
}

function ImageLightbox({ image, onClose }) {
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  return (
    <div className="image-lightbox" onClick={onClose}>
      <div className="lightbox-content" onClick={e => e.stopPropagation()}>
        <img
          src={image.url}
          alt={image.name}
          style={{
            transform: `scale(${scale}) translate(${position.x}px, ${position.y}px)`
          }}
        />

        <div className="lightbox-controls">
          <button onClick={() => setScale(s => Math.min(s + 0.25, 3))}>
            <ZoomInIcon />
          </button>
          <span>{Math.round(scale * 100)}%</span>
          <button onClick={() => setScale(s => Math.max(s - 0.25, 0.5))}>
            <ZoomOutIcon />
          </button>
          <button onClick={() => { setScale(1); setPosition({ x: 0, y: 0 }); }}>
            Reset
          </button>
        </div>

        <button className="lightbox-close" onClick={onClose}>
          <CloseIcon />
        </button>
      </div>
    </div>
  );
}
```

### AI Image Analysis Display

Show AI's understanding of images:

```tsx
function ImageAnalysisDisplay({ image, analysis }) {
  return (
    <div className="image-analysis">
      <div className="analysis-header">
        <ImageIcon />
        <span>Analyzing image: {image.name}</span>
      </div>

      <div className="analysis-content">
        <div className="image-section">
          <img src={image.url} alt="Analyzed image" />
        </div>

        <div className="analysis-section">
          {analysis.isAnalyzing ? (
            <div className="analyzing">
              <Spinner />
              <span>Analyzing image content...</span>
            </div>
          ) : (
            <>
              {analysis.description && (
                <div className="description">
                  <h4>What I see:</h4>
                  <p>{analysis.description}</p>
                </div>
              )}

              {analysis.objects && (
                <div className="detected-objects">
                  <h4>Detected objects:</h4>
                  <ul>
                    {analysis.objects.map((obj, i) => (
                      <li key={i}>
                        {obj.label} ({Math.round(obj.confidence * 100)}% confident)
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {analysis.text && (
                <div className="extracted-text">
                  <h4>Text in image:</h4>
                  <pre>{analysis.text}</pre>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
```

## File Attachments

### Multi-Format File Handler

Support various file types with appropriate previews:

```tsx
interface FileAttachment {
  id: string;
  file: File;
  type: 'document' | 'code' | 'data' | 'archive' | 'unknown';
  preview?: string;
  metadata?: Record<string, any>;
}

function FileAttachmentHandler({ onFilesAttached }) {
  const [attachments, setAttachments] = useState<FileAttachment[]>([]);
  const [processing, setProcessing] = useState<Set<string>>(new Set());

  const classifyFile = (file: File): FileAttachment['type'] => {
    const extension = file.name.split('.').pop()?.toLowerCase();

    const typeMap: Record<string, FileAttachment['type']> = {
      // Documents
      pdf: 'document', doc: 'document', docx: 'document',
      txt: 'document', md: 'document', rtf: 'document',

      // Code
      js: 'code', ts: 'code', jsx: 'code', tsx: 'code',
      py: 'code', java: 'code', cpp: 'code', c: 'code',
      go: 'code', rs: 'code', rb: 'code', php: 'code',

      // Data
      json: 'data', csv: 'data', xml: 'data', yaml: 'data',
      sql: 'data', xlsx: 'data', xls: 'data',

      // Archives
      zip: 'archive', tar: 'archive', gz: 'archive',
      rar: 'archive', '7z': 'archive'
    };

    return typeMap[extension || ''] || 'unknown';
  };

  const processFile = async (file: File): Promise<FileAttachment> => {
    const id = crypto.randomUUID();
    const type = classifyFile(file);
    const attachment: FileAttachment = { id, file, type };

    setProcessing(prev => new Set(prev).add(id));

    try {
      // Generate preview based on type
      switch (type) {
        case 'document':
          if (file.type === 'application/pdf') {
            attachment.preview = await generatePDFPreview(file);
            attachment.metadata = await extractPDFMetadata(file);
          } else if (file.name.endsWith('.md')) {
            const text = await file.text();
            attachment.preview = text.substring(0, 500);
          }
          break;

        case 'code':
          const codeText = await file.text();
          attachment.preview = codeText.substring(0, 1000);
          attachment.metadata = {
            lines: codeText.split('\n').length,
            language: detectLanguage(file.name)
          };
          break;

        case 'data':
          if (file.name.endsWith('.csv')) {
            const csvPreview = await generateCSVPreview(file);
            attachment.preview = csvPreview;
            attachment.metadata = await analyzeCSV(file);
          } else if (file.name.endsWith('.json')) {
            const jsonText = await file.text();
            const json = JSON.parse(jsonText);
            attachment.preview = JSON.stringify(json, null, 2).substring(0, 500);
          }
          break;

        case 'archive':
          attachment.metadata = await listArchiveContents(file);
          break;
      }
    } catch (error) {
      console.error(`Error processing file ${file.name}:`, error);
    } finally {
      setProcessing(prev => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }

    return attachment;
  };

  const handleFiles = async (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    const processed = await Promise.all(fileArray.map(processFile));
    setAttachments(prev => [...prev, ...processed]);
    onFilesAttached(processed);
  };

  return (
    <div className="file-attachment-handler">
      <FileDropZone onDrop={handleFiles} />

      {attachments.length > 0 && (
        <div className="attachment-list">
          {attachments.map(attachment => (
            <FileAttachmentCard
              key={attachment.id}
              attachment={attachment}
              isProcessing={processing.has(attachment.id)}
              onRemove={() => {
                setAttachments(prev => prev.filter(a => a.id !== attachment.id));
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

### File Attachment Display

Show attached files with appropriate icons and previews:

```tsx
function FileAttachmentCard({ attachment, isProcessing, onRemove }) {
  const [expanded, setExpanded] = useState(false);

  const getIcon = () => {
    const icons = {
      document: <DocumentIcon />,
      code: <CodeIcon />,
      data: <DatabaseIcon />,
      archive: <ArchiveIcon />,
      unknown: <FileIcon />
    };
    return icons[attachment.type];
  };

  return (
    <div className="file-attachment-card">
      <div className="attachment-header">
        <div className="attachment-icon">{getIcon()}</div>

        <div className="attachment-info">
          <div className="attachment-name">{attachment.file.name}</div>
          <div className="attachment-meta">
            {formatBytes(attachment.file.size)}
            {attachment.metadata?.lines && ` • ${attachment.metadata.lines} lines`}
            {attachment.metadata?.pages && ` • ${attachment.metadata.pages} pages`}
          </div>
        </div>

        <div className="attachment-actions">
          {attachment.preview && (
            <button
              onClick={() => setExpanded(!expanded)}
              aria-label={expanded ? 'Collapse preview' : 'Expand preview'}
            >
              {expanded ? <ChevronUpIcon /> : <ChevronDownIcon />}
            </button>
          )}
          <button onClick={onRemove} aria-label="Remove attachment">
            <CloseIcon />
          </button>
        </div>
      </div>

      {isProcessing && (
        <div className="processing-indicator">
          <Spinner size="small" />
          <span>Processing file...</span>
        </div>
      )}

      {expanded && attachment.preview && (
        <div className="attachment-preview">
          {attachment.type === 'code' ? (
            <SyntaxHighlighter
              language={attachment.metadata?.language || 'text'}
              style={dark}
            >
              {attachment.preview}
            </SyntaxHighlighter>
          ) : attachment.type === 'document' && attachment.file.type === 'application/pdf' ? (
            <img src={attachment.preview} alt="PDF preview" />
          ) : (
            <pre>{attachment.preview}</pre>
          )}
        </div>
      )}

      {attachment.type === 'archive' && attachment.metadata?.contents && (
        <div className="archive-contents">
          <h5>Archive contains:</h5>
          <ul>
            {attachment.metadata.contents.slice(0, 10).map((item, i) => (
              <li key={i}>{item}</li>
            ))}
            {attachment.metadata.contents.length > 10 && (
              <li>...and {attachment.metadata.contents.length - 10} more files</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
```

## Voice Input & Output

### Voice Recording Interface

Push-to-talk and continuous recording modes:

```tsx
function VoiceInput({ onTranscription, mode = 'push-to-talk' }) {
  const [isRecording, setIsRecording] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [transcription, setTranscription] = useState('');
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      // Setup audio analyzer for level meter
      audioContextRef.current = new AudioContext();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);

      // Start level monitoring
      monitorAudioLevel();

      // Setup media recorder
      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      });

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);

        // Real-time transcription for continuous mode
        if (mode === 'continuous') {
          transcribeChunk(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: 'audio/webm'
        });

        // Transcribe full recording
        const text = await transcribeAudio(audioBlob);
        setTranscription(text);
        onTranscription(text);

        // Cleanup
        audioChunksRef.current = [];
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start(mode === 'continuous' ? 1000 : undefined);
      setIsRecording(true);
      setError(null);
    } catch (err) {
      setError('Microphone access denied');
      console.error('Recording error:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current?.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }

    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
  };

  const monitorAudioLevel = () => {
    if (!analyserRef.current) return;

    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
    analyserRef.current.getByteFrequencyData(dataArray);

    const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
    setAudioLevel(average / 255);

    if (isRecording) {
      requestAnimationFrame(monitorAudioLevel);
    }
  };

  return (
    <div className="voice-input">
      {mode === 'push-to-talk' ? (
        <button
          onMouseDown={startRecording}
          onMouseUp={stopRecording}
          onTouchStart={startRecording}
          onTouchEnd={stopRecording}
          className={`voice-button ${isRecording ? 'recording' : ''}`}
          aria-label="Hold to record"
        >
          <MicrophoneIcon />
          {isRecording && <span className="recording-text">Recording...</span>}
        </button>
      ) : (
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`voice-button ${isRecording ? 'recording' : ''}`}
          aria-label={isRecording ? 'Stop recording' : 'Start recording'}
        >
          {isRecording ? <StopIcon /> : <MicrophoneIcon />}
        </button>
      )}

      {isRecording && (
        <div className="audio-visualizer">
          <AudioLevelMeter level={audioLevel} />
          <div className="recording-time">
            <RecordingTimer startTime={Date.now()} />
          </div>
        </div>
      )}

      {transcription && (
        <div className="transcription-preview">
          <h4>Transcription:</h4>
          <p>{transcription}</p>
          <button onClick={() => setTranscription('')}>Clear</button>
        </div>
      )}

      {error && (
        <div className="voice-error">
          <ErrorIcon />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}

function AudioLevelMeter({ level }) {
  return (
    <div className="audio-level-meter">
      <div
        className="level-bar"
        style={{
          width: `${level * 100}%`,
          backgroundColor: level > 0.7 ? '#ff4444' : level > 0.4 ? '#ffaa00' : '#44ff44'
        }}
      />
    </div>
  );
}
```

### Text-to-Speech Output

Read AI responses aloud:

```tsx
function TextToSpeech({ text, autoPlay = false, voice = 'default' }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [rate, setRate] = useState(1.0);
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  useEffect(() => {
    // Load available voices
    const loadVoices = () => {
      setVoices(window.speechSynthesis.getVoices());
    };

    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;

    return () => {
      window.speechSynthesis.cancel();
    };
  }, []);

  useEffect(() => {
    if (autoPlay && text) {
      speak();
    }
  }, [text, autoPlay]);

  const speak = () => {
    if (!text) return;

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    utteranceRef.current = new SpeechSynthesisUtterance(text);
    utteranceRef.current.rate = rate;

    // Set voice if specified
    if (voice !== 'default' && voices.length > 0) {
      const selectedVoice = voices.find(v => v.name === voice);
      if (selectedVoice) {
        utteranceRef.current.voice = selectedVoice;
      }
    }

    // Event handlers
    utteranceRef.current.onstart = () => setIsPlaying(true);
    utteranceRef.current.onend = () => {
      setIsPlaying(false);
      setProgress(0);
    };

    utteranceRef.current.onboundary = (event) => {
      if (event.charIndex && text) {
        setProgress((event.charIndex / text.length) * 100);
      }
    };

    window.speechSynthesis.speak(utteranceRef.current);
  };

  const pause = () => window.speechSynthesis.pause();
  const resume = () => window.speechSynthesis.resume();
  const stop = () => {
    window.speechSynthesis.cancel();
    setIsPlaying(false);
    setProgress(0);
  };

  return (
    <div className="text-to-speech">
      <div className="tts-controls">
        {!isPlaying ? (
          <button onClick={speak} aria-label="Play">
            <PlayIcon />
          </button>
        ) : (
          <>
            <button onClick={pause} aria-label="Pause">
              <PauseIcon />
            </button>
            <button onClick={stop} aria-label="Stop">
              <StopIcon />
            </button>
          </>
        )}

        <select
          value={voice}
          onChange={(e) => utteranceRef.current && (utteranceRef.current.voice = voices.find(v => v.name === e.target.value) || null)}
        >
          <option value="default">Default Voice</option>
          {voices.map(v => (
            <option key={v.name} value={v.name}>
              {v.name} ({v.lang})
            </option>
          ))}
        </select>

        <label className="rate-control">
          Speed:
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={rate}
            onChange={(e) => setRate(parseFloat(e.target.value))}
          />
          <span>{rate}x</span>
        </label>
      </div>

      {isPlaying && (
        <div className="tts-progress">
          <div
            className="progress-bar"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}
```

## Screen Sharing & Recording

### Screen Share Component

Share screen with AI for context:

```tsx
function ScreenShare({ onScreenCapture }) {
  const [isSharing, setIsSharing] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const startScreenShare = async () => {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: {
          cursor: 'always',
          displaySurface: 'monitor'
        },
        audio: false
      });

      streamRef.current = stream;
      setIsSharing(true);

      // Display preview
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      // Handle stream end
      stream.getVideoTracks()[0].onended = () => {
        stopScreenShare();
      };

      // Capture screenshots periodically
      captureScreenshots(stream);
    } catch (error) {
      console.error('Screen share error:', error);
      showToast('Screen sharing was cancelled or failed', 'error');
    }
  };

  const stopScreenShare = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsSharing(false);
    setPreview(null);
  };

  const captureScreenshots = (stream: MediaStream) => {
    const video = document.createElement('video');
    video.srcObject = stream;
    video.play();

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    const captureFrame = () => {
      if (!isSharing || !ctx) return;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);

      canvas.toBlob((blob) => {
        if (blob) {
          const url = URL.createObjectURL(blob);
          setPreview(url);
          onScreenCapture(blob);
        }
      }, 'image/png');

      // Capture every 5 seconds
      setTimeout(captureFrame, 5000);
    };

    video.onloadedmetadata = () => {
      captureFrame();
    };
  };

  return (
    <div className="screen-share">
      {!isSharing ? (
        <button onClick={startScreenShare} className="share-button">
          <ScreenShareIcon />
          Share Screen
        </button>
      ) : (
        <div className="sharing-container">
          <div className="sharing-header">
            <span className="sharing-indicator">
              <RecordIcon className="blink" />
              Sharing Screen
            </span>
            <button onClick={stopScreenShare}>
              Stop Sharing
            </button>
          </div>

          <video
            ref={videoRef}
            autoPlay
            muted
            className="screen-preview"
          />

          {preview && (
            <div className="screenshot-preview">
              <h4>Latest Screenshot:</h4>
              <img src={preview} alt="Screen capture" />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

## Collaborative Whiteboard

### Interactive Drawing Canvas

Collaborate with AI on visual content:

```tsx
function CollaborativeWhiteboard({ onCanvasUpdate }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [tool, setTool] = useState<'pen' | 'eraser' | 'text' | 'shape'>('pen');
  const [color, setColor] = useState('#000000');
  const [lineWidth, setLineWidth] = useState(2);
  const [history, setHistory] = useState<ImageData[]>([]);

  const startDrawing = (e: React.MouseEvent | React.TouchEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = ('touches' in e) ? e.touches[0].clientX - rect.left : e.clientX - rect.left;
    const y = ('touches' in e) ? e.touches[0].clientY - rect.top : e.clientY - rect.top;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    setIsDrawing(true);
    ctx.beginPath();
    ctx.moveTo(x, y);
  };

  const draw = (e: React.MouseEvent | React.TouchEvent) => {
    if (!isDrawing) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = ('touches' in e) ? e.touches[0].clientX - rect.left : e.clientX - rect.left;
    const y = ('touches' in e) ? e.touches[0].clientY - rect.top : e.clientY - rect.top;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';

    if (tool === 'pen') {
      ctx.globalCompositeOperation = 'source-over';
      ctx.strokeStyle = color;
    } else if (tool === 'eraser') {
      ctx.globalCompositeOperation = 'destination-out';
    }

    ctx.lineTo(x, y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    if (!isDrawing) return;
    setIsDrawing(false);

    // Save to history
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        setHistory(prev => [...prev, imageData]);

        // Send update to AI
        canvas.toBlob(blob => {
          if (blob) onCanvasUpdate(blob);
        }, 'image/png');
      }
    }
  };

  const undo = () => {
    if (history.length === 0) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const previousState = history[history.length - 2];
    if (previousState) {
      ctx.putImageData(previousState, 0, 0);
    } else {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    setHistory(prev => prev.slice(0, -1));
  };

  const clear = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setHistory([]);
  };

  return (
    <div className="collaborative-whiteboard">
      <div className="whiteboard-toolbar">
        <div className="tool-group">
          <button
            className={tool === 'pen' ? 'active' : ''}
            onClick={() => setTool('pen')}
          >
            <PenIcon />
          </button>
          <button
            className={tool === 'eraser' ? 'active' : ''}
            onClick={() => setTool('eraser')}
          >
            <EraserIcon />
          </button>
          <button
            className={tool === 'text' ? 'active' : ''}
            onClick={() => setTool('text')}
          >
            <TextIcon />
          </button>
          <button
            className={tool === 'shape' ? 'active' : ''}
            onClick={() => setTool('shape')}
          >
            <ShapeIcon />
          </button>
        </div>

        <div className="color-group">
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
          />
          <input
            type="range"
            min="1"
            max="20"
            value={lineWidth}
            onChange={(e) => setLineWidth(parseInt(e.target.value))}
          />
        </div>

        <div className="action-group">
          <button onClick={undo} disabled={history.length === 0}>
            <UndoIcon /> Undo
          </button>
          <button onClick={clear}>
            <ClearIcon /> Clear
          </button>
        </div>
      </div>

      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
        onTouchStart={startDrawing}
        onTouchMove={draw}
        onTouchEnd={stopDrawing}
        className="drawing-canvas"
      />
    </div>
  );
}
```

## Video Input

### Video Upload and Processing

Handle video files for AI analysis:

```tsx
function VideoInput({ onVideoProcessed }) {
  const [video, setVideo] = useState<File | null>(null);
  const [frames, setFrames] = useState<string[]>([]);
  const [processing, setProcessing] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const extractFrames = async (videoFile: File, frameCount = 10) => {
    setProcessing(true);
    const url = URL.createObjectURL(videoFile);
    const video = document.createElement('video');
    video.src = url;

    await new Promise(resolve => {
      video.onloadedmetadata = resolve;
    });

    const duration = video.duration;
    const interval = duration / frameCount;
    const extractedFrames: string[] = [];

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    for (let i = 0; i < frameCount; i++) {
      video.currentTime = i * interval;

      await new Promise(resolve => {
        video.onseeked = resolve;
      });

      if (ctx) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);

        const frameDataUrl = canvas.toDataURL('image/jpeg', 0.7);
        extractedFrames.push(frameDataUrl);
      }
    }

    URL.revokeObjectURL(url);
    setFrames(extractedFrames);
    setProcessing(false);

    onVideoProcessed({
      file: videoFile,
      frames: extractedFrames,
      duration,
      metadata: {
        width: video.videoWidth,
        height: video.videoHeight,
        frameRate: video.playbackRate
      }
    });
  };

  return (
    <div className="video-input">
      <input
        type="file"
        accept="video/*"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) {
            setVideo(file);
            extractFrames(file);
          }
        }}
      />

      {video && (
        <div className="video-preview">
          <video
            ref={videoRef}
            src={URL.createObjectURL(video)}
            controls
            width="400"
          />

          {processing && (
            <div className="processing">
              <Spinner />
              <span>Extracting frames for analysis...</span>
            </div>
          )}

          {frames.length > 0 && (
            <div className="frame-gallery">
              <h4>Extracted Frames:</h4>
              <div className="frames">
                {frames.map((frame, i) => (
                  <img
                    key={i}
                    src={frame}
                    alt={`Frame ${i + 1}`}
                    className="frame-thumbnail"
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

## Multi-Modal Message Display

### Unified Multi-Modal Message

Display messages with mixed content types:

```tsx
interface MultiModalContent {
  type: 'text' | 'image' | 'file' | 'audio' | 'video' | 'code';
  content: any;
  metadata?: Record<string, any>;
}

function MultiModalMessage({ message }) {
  const renderContent = (content: MultiModalContent) => {
    switch (content.type) {
      case 'text':
        return <Streamdown>{content.content}</Streamdown>;

      case 'image':
        return (
          <img
            src={content.content}
            alt={content.metadata?.alt || 'Image'}
            className="message-image"
          />
        );

      case 'file':
        return (
          <FileAttachment
            file={content.content}
            metadata={content.metadata}
          />
        );

      case 'audio':
        return (
          <audio controls src={content.content}>
            Your browser does not support audio playback.
          </audio>
        );

      case 'video':
        return (
          <video controls width="100%">
            <source src={content.content} />
            Your browser does not support video playback.
          </video>
        );

      case 'code':
        return (
          <SyntaxHighlighter
            language={content.metadata?.language || 'text'}
            style={dark}
          >
            {content.content}
          </SyntaxHighlighter>
        );

      default:
        return null;
    }
  };

  return (
    <div className={`multi-modal-message ${message.role}`}>
      <div className="message-header">
        <span className="role">{message.role}</span>
        <time>{formatTime(message.timestamp)}</time>
      </div>

      <div className="message-content">
        {Array.isArray(message.content) ? (
          message.content.map((item, i) => (
            <div key={i} className={`content-block ${item.type}`}>
              {renderContent(item)}
            </div>
          ))
        ) : (
          renderContent(message.content)
        )}
      </div>

      {message.attachments && message.attachments.length > 0 && (
        <div className="message-attachments">
          {message.attachments.map((attachment, i) => (
            <AttachmentThumbnail key={i} attachment={attachment} />
          ))}
        </div>
      )}
    </div>
  );
}
```

## Drag & Drop Support

### Universal Drop Zone

Accept any file type via drag and drop:

```tsx
function UniversalDropZone({ onDrop, children }) {
  const [isDragging, setIsDragging] = useState(false);
  const dragCounter = useRef(0);

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    dragCounter.current++;
    if (dragCounter.current === 1) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    dragCounter.current--;
    if (dragCounter.current === 0) {
      setIsDragging(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    dragCounter.current = 0;

    const items: Array<File | string> = [];

    // Handle file drops
    if (e.dataTransfer.files.length > 0) {
      items.push(...Array.from(e.dataTransfer.files));
    }

    // Handle text drops
    const text = e.dataTransfer.getData('text');
    if (text) {
      items.push(text);
    }

    // Handle HTML drops (rich text)
    const html = e.dataTransfer.getData('text/html');
    if (html && html !== text) {
      items.push(html);
    }

    // Handle URL drops
    const url = e.dataTransfer.getData('URL');
    if (url) {
      items.push(url);
    }

    if (items.length > 0) {
      onDrop(items);
    }
  };

  return (
    <div
      className={`universal-drop-zone ${isDragging ? 'dragging' : ''}`}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      {children}

      {isDragging && (
        <div className="drop-overlay">
          <div className="drop-message">
            <UploadIcon size="large" />
            <h3>Drop files here</h3>
            <p>Images, documents, audio, video, or any file type</p>
          </div>
        </div>
      )}
    </div>
  );
}
```

## Best Practices Summary

1. **Multiple input methods** - Paste, drag-drop, file picker, camera, URL
2. **Preview everything** - Images, PDFs, code, data files
3. **Process asynchronously** - Don't block UI during file processing
4. **Show progress** - Uploading, processing, analyzing indicators
5. **Graceful degradation** - Handle unsupported formats/browsers
6. **Size validation** - Check file sizes before upload
7. **Type detection** - Classify files and render appropriately
8. **Metadata extraction** - Show relevant info (dimensions, pages, duration)
9. **Voice feedback** - Visual audio levels, transcription preview
10. **Accessibility** - Keyboard support, ARIA labels, focus management