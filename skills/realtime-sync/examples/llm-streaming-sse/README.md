# LLM Streaming with SSE Example

**RUNNABLE** example demonstrating Server-Sent Events (SSE) for streaming LLM responses.

## Overview

This example shows how to:
1. Stream tokens from OpenAI/Anthropic APIs
2. Relay via FastAPI SSE endpoint
3. Render progressively in frontend (ai-chat skill integration)

## Architecture

```
OpenAI/Anthropic API
    ↓ (streaming tokens)
FastAPI Backend
    ↓ (SSE: text/event-stream)
Frontend (EventSource)
    ↓ (progressive rendering)
User sees tokens appear in real-time
```

## Files

- `backend.py` - FastAPI SSE server (Python 3.11+)
- `frontend.html` - EventSource client (vanilla JS)
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template

## Prerequisites

- Python 3.11+
- OpenAI API key OR Anthropic API key

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your API key
```

## Running

```bash
# Start backend
python backend.py

# Open frontend
open frontend.html
# Or visit http://localhost:8000
```

## Usage

1. Open `frontend.html` in browser
2. Enter a prompt (e.g., "Explain quantum computing")
3. Watch tokens stream in real-time
4. See progressive rendering of response

## Testing

```bash
# Test SSE endpoint directly
curl -N http://localhost:8000/chat/stream?prompt=hello

# Should see:
# event: token
# data: Hello
#
# event: token
# data: !
#
# event: done
# data: [DONE]
```

## Integration with ai-chat Skill

This backend can be used with the ai-chat skill:

```typescript
// In your ai-chat component
import { useSSEStream } from './hooks/useSSEStream'

function ChatMessage({ prompt }: { prompt: string }) {
  const { content, isDone, error } = useSSEStream(
    `/chat/stream?prompt=${encodeURIComponent(prompt)}`
  )

  return (
    <div className="chat-message">
      {content}
      {!isDone && <span className="cursor">▊</span>}
    </div>
  )
}
```

## Performance

- **Latency**: ~50-200ms for first token
- **Throughput**: 20-50 tokens/second
- **Memory**: Constant (streaming, not buffering)

## Error Handling

- Network errors: EventSource auto-reconnects
- API errors: Sent as `event: error`
- Rate limits: Exponential backoff

## Production Considerations

1. **Authentication**: Add JWT validation
2. **Rate limiting**: Limit requests per user
3. **CORS**: Configure allowed origins
4. **Monitoring**: Log request latency
5. **Scaling**: Use Redis for pub/sub across servers

## License

MIT
