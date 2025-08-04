"""OpenAI-compatible API server for model routing."""

import time
from typing import Any

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
)
from pydantic import BaseModel

from .config import config
from .providers.anthropic_provider import AnthropicProvider
from .providers.deepseek_provider import DeepSeekProvider
from .providers.groq_provider import GroqProvider
from .providers.openai_provider import OpenAIProvider

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


# Model provider prefixes
PROVIDER_PREFIXES = {
    "openai/": "openai",
    "anthropic/": "anthropic",
    "groq/": "groq",
    "deepseek/": "deepseek",
}




def get_provider(provider_name: str):
    """Get provider instance."""
    if provider_name == "openai":
        if not config.openai_api_key:
            raise HTTPException(status_code=401, detail="OpenAI API key not configured")
        return OpenAIProvider(config.openai_api_key)
    elif provider_name == "anthropic":
        if not config.anthropic_api_key:
            raise HTTPException(
            status_code=401, detail="Anthropic API key not configured"
        )
        return AnthropicProvider(config.anthropic_api_key)
    elif provider_name == "groq":
        if not config.groq_api_key:
            raise HTTPException(status_code=401, detail="Groq API key not configured")
        return GroqProvider(config.groq_api_key)
    elif provider_name == "deepseek":
        if not config.deepseek_api_key:
            raise HTTPException(
            status_code=401, detail="DeepSeek API key not configured"
        )
        return DeepSeekProvider(config.deepseek_api_key)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Provider {provider_name} not implemented"
        )


def get_provider_for_model(model_name: str) -> str:
    """Get provider for a model based on prefix."""
    for prefix, provider in PROVIDER_PREFIXES.items():
        if model_name.startswith(prefix):
            return provider

    raise HTTPException(status_code=404, detail=f"Model {model_name} not found")


def get_actual_model_name(model_name: str) -> str:
    """Get the actual model name to send to provider (strip prefix if present)."""
    for prefix in PROVIDER_PREFIXES:
        if model_name.startswith(prefix):
            return model_name[len(prefix):]
    return model_name


@app.get("/v1/models")
async def list_models():
    """List available models from all providers."""
    models = []

    # Get models from each provider
    for prefix, provider_name in PROVIDER_PREFIXES.items():
        try:
            # Try to get provider instance (this will check API keys)
            provider_instance = get_provider(provider_name)
            available_models = provider_instance.get_available_models()

            # Add models with prefix
            for model_name in available_models:
                models.append({
                    "id": f"{prefix}{model_name}",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": provider_name,
                    "permission": [],
                    "root": f"{prefix}{model_name}",
                    "parent": None,
                })
        except HTTPException:
            # Skip providers that don't have API keys configured
            continue

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

    # Get provider for model using new routing logic
    provider = get_provider_for_model(request.model)

    # Get provider instance and route request
    provider_instance = get_provider(provider)

    # Get actual model name to send to provider (strip prefix)
    actual_model_name = get_actual_model_name(request.model)

    try:
        return await provider_instance.create_chat_completion(
            model=actual_model_name,
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
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e)) from e


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
