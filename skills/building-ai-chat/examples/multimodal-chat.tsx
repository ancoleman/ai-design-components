import React, { useState } from 'react';
import { Camera, Paperclip, Mic, X } from 'lucide-react';

/**
 * Multimodal Chat Example
 *
 * Chat interface supporting multiple input types:
 * - Text messages
 * - Image upload with preview
 * - Voice input
 * - File attachments
 *
 * For models like GPT-4 Vision, Claude 3, Gemini Pro Vision
 */

interface Attachment {
  id: string;
  type: 'image' | 'audio' | 'file';
  url: string;
  name: string;
  preview?: string;
}

export function MultimodalChat() {
  const [input, setInput] = useState('');
  const [attachments, setAttachments] = useState<Attachment[]>([]);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const preview = e.target?.result as string;
      setAttachments((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          type: 'image',
          url: preview,
          name: file.name,
          preview,
        },
      ]);
    };
    reader.readAsDataURL(file);
  };

  const removeAttachment = (id: string) => {
    setAttachments((prev) => prev.filter((a) => a.id !== id));
  };

  const sendMessage = async () => {
    if (!input.trim() && attachments.length === 0) return;

    const message = {
      text: input,
      attachments,
    };

    console.log('Sending multimodal message:', message);

    // Send to API (GPT-4 Vision, Claude 3, etc.)
    // const response = await fetch('/api/chat/multimodal', {
    //   method: 'POST',
    //   body: JSON.stringify(message),
    // });

    setInput('');
    setAttachments([]);
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <div style={{ padding: '16px', borderBottom: '1px solid #e2e8f0', backgroundColor: '#fff' }}>
        <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 600 }}>Multi-Modal AI Assistant</h1>
        <p style={{ margin: '4px 0 0 0', fontSize: '14px', color: '#64748b' }}>Upload images, audio, or files</p>
      </div>

      {/* Messages area */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', backgroundColor: '#f9fafb' }}>
        <div style={{ textAlign: 'center', padding: '48px', color: '#64748b' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>🎨</div>
          <p>Upload an image and ask me about it!</p>
        </div>
      </div>

      {/* Attachment previews */}
      {attachments.length > 0 && (
        <div style={{ padding: '16px', borderTop: '1px solid #e2e8f0', backgroundColor: '#f9fafb' }}>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            {attachments.map((attachment) => (
              <div
                key={attachment.id}
                style={{
                  position: 'relative',
                  width: '120px',
                  height: '120px',
                  borderRadius: '8px',
                  overflow: 'hidden',
                  border: '1px solid #e2e8f0',
                }}
              >
                {attachment.type === 'image' && (
                  <img
                    src={attachment.preview}
                    alt={attachment.name}
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  />
                )}

                <button
                  onClick={() => removeAttachment(attachment.id)}
                  style={{
                    position: 'absolute',
                    top: '4px',
                    right: '4px',
                    width: '24px',
                    height: '24px',
                    borderRadius: '50%',
                    backgroundColor: 'rgba(0, 0, 0, 0.6)',
                    color: '#fff',
                    border: 'none',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <X size={14} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Input area */}
      <div style={{ padding: '16px', borderTop: '1px solid #e2e8f0', backgroundColor: '#fff' }}>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-end' }}>
          {/* Attachment buttons */}
          <div style={{ display: 'flex', gap: '4px' }}>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              id="image-upload"
              style={{ display: 'none' }}
            />
            <label
              htmlFor="image-upload"
              style={{
                width: '40px',
                height: '40px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '8px',
                border: '1px solid #e2e8f0',
                cursor: 'pointer',
                backgroundColor: '#fff',
              }}
            >
              <Camera size={20} color="#64748b" />
            </label>

            <button
              style={{
                width: '40px',
                height: '40px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '8px',
                border: '1px solid #e2e8f0',
                cursor: 'pointer',
                backgroundColor: '#fff',
              }}
            >
              <Mic size={20} color="#64748b" />
            </button>

            <button
              style={{
                width: '40px',
                height: '40px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '8px',
                border: '1px solid #e2e8f0',
                cursor: 'pointer',
                backgroundColor: '#fff',
              }}
            >
              <Paperclip size={20} color="#64748b" />
            </button>
          </div>

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder={
              attachments.length > 0
                ? 'Ask about the uploaded image...'
                : 'Type a message or upload an image...'
            }
            style={{
              flex: 1,
              padding: '12px',
              borderRadius: '12px',
              border: '1px solid #e2e8f0',
              resize: 'none',
              minHeight: '52px',
              fontFamily: 'inherit',
            }}
          />

          <button
            onClick={sendMessage}
            disabled={!input.trim() && attachments.length === 0}
            style={{
              padding: '12px 24px',
              backgroundColor: (input.trim() || attachments.length > 0) ? '#3b82f6' : '#e2e8f0',
              color: '#fff',
              border: 'none',
              borderRadius: '12px',
              cursor: (input.trim() || attachments.length > 0) ? 'pointer' : 'not-allowed',
              fontWeight: 600,
              height: '52px',
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

async function mockCodeResponse(prompt: string): Promise<string> {
  return 'Mock response for code assistant';
}

export default MultimodalChat;
