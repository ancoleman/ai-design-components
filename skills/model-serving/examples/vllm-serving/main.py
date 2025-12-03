"""
FastAPI + vLLM Streaming Example

Complete implementation of streaming LLM responses using Server-Sent Events (SSE).
Integrates with ai-chat skill frontend for production-ready chat interfaces.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="vLLM Streaming API")

# CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to vLLM server (must be running separately)
# Start vLLM with: vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # vLLM doesn't require API key
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.7
    max_tokens: int = 512
    system_prompt: str = "You are a helpful AI assistant."

class ChatResponse(BaseModel):
    response: str
    tokens: int

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers."""
    try:
        # Verify vLLM is accessible
        client.models.list()
        return {"status": "healthy", "vllm_connected": True}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="vLLM server unavailable")

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Non-streaming chat endpoint.

    Returns complete response after generation finishes.
    Use /chat/stream for real-time streaming.
    """
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False
        )

        content = response.choices[0].message.content
        tokens = response.usage.total_tokens

        return ChatResponse(response=content, tokens=tokens)

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint using Server-Sent Events (SSE).

    Streams tokens as they're generated for real-time UX.
    Integrates with ai-chat skill frontend.
    """

    async def generate():
        try:
            logger.info(f"Starting stream for message: {request.message[:50]}...")

            stream = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=[
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.message}
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True
            )

            total_tokens = 0

            for chunk in stream:
                # Extract token from chunk
                if chunk.choices[0].delta.content is not None:
                    token = chunk.choices[0].delta.content
                    total_tokens += 1

                    # Send token in SSE format
                    data = json.dumps({
                        "token": token,
                        "total_tokens": total_tokens
                    })
                    yield f"data: {data}\n\n"

            # Signal completion
            completion_data = json.dumps({
                "done": True,
                "total_tokens": total_tokens
            })
            yield f"data: {completion_data}\n\n"

            logger.info(f"Stream completed. Total tokens: {total_tokens}")

        except Exception as e:
            logger.error(f"Streaming error: {e}")
            error_data = json.dumps({
                "error": str(e),
                "done": True
            })
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@app.get("/models")
async def list_models():
    """List available models from vLLM server."""
    try:
        models = client.models.list()
        return {"models": [model.id for model in models.data]}
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3000,
        log_level="info"
    )
