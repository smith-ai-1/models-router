"""OpenAI-compatible API server for model routing."""

import os
import time
from typing import Any

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
)
from pydantic import BaseModel

from .providers.openai_provider import OpenAIProvider

load_dotenv()

app = FastAPI(
    title="Model Router",
    description="OpenAI-compatible API for model routing"
)


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatCompletionMessageParam]
    temperature: float | None = 1.0
    max_tokens: int | None = None
    top_p: float | None = 1.0
    frequency_penalty: float | None = 0.0
    presence_penalty: float | None = 0.0
    stream: bool | None = False
    stop: str | list[str] | None = None
    n: int | None = 1


class ModelsResponse(BaseModel):
    object: str = "list"
    data: list[dict[str, Any]]


# Model provider mapping
MODEL_PROVIDERS = {
    "gpt-3.5-turbo": "openai",
    "gpt-4": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4o": "openai",
    "gpt-4o-mini": "openai",
    "claude-3-sonnet": "anthropic",
    "claude-3-opus": "anthropic",
    "claude-3-haiku": "anthropic",
    "claude-3-5-sonnet": "anthropic",
    "llama-3.1-70b": "groq",
    "llama-3.1-8b": "groq",
    "mixtral-8x7b": "groq",
    "deepseek-chat": "deepseek",
    "deepseek-coder": "deepseek",
}


def get_provider(provider_name: str):
    """Get provider instance."""
    if provider_name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=401, detail="OpenAI API key not configured")
        return OpenAIProvider(api_key)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Provider {provider_name} not implemented"
        )


@app.get("/v1/models")
async def list_models():
    """List available models."""
    models = [
        {
            "id": model_id,
            "object": "model",
            "created": int(time.time()),
            "owned_by": provider,
            "permission": [],
            "root": model_id,
            "parent": None,
        }
        for model_id, provider in MODEL_PROVIDERS.items()
    ]

    return ModelsResponse(data=models)


@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatCompletionRequest,
    authorization: str | None = Header(None)
) -> ChatCompletion:
    """Create chat completion."""

    # Validate API key
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    # Get provider for model
    provider = MODEL_PROVIDERS.get(request.model)
    if not provider:
        raise HTTPException(status_code=404, detail=f"Model {request.model} not found")

    # Get provider instance and route request
    provider_instance = get_provider(provider)

    return await provider_instance.create_chat_completion(
        model=request.model,
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        frequency_penalty=request.frequency_penalty,
        presence_penalty=request.presence_penalty,
        stream=request.stream,
        stop=request.stop,
        n=request.n,
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
