"""API routes for model router."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict

from model_router.config import config
from model_router.domain.models import ChatCompletionRequest, ChatCompletionResponse, ProviderInfo
from model_router.domain.providers import ProviderName
from model_router.domain.exceptions import (
    ProviderNotFoundError,
    ProviderNotConfiguredError,
    ModelNotSupportedError,
    ProviderAPIError,
)
from model_router.services.model_router import ModelRouterService
from model_router.services.adapters.openai import OpenAIAdapter, MockOpenAIAdapter
from model_router.services.adapters.anthropic import AnthropicAdapter, MockAnthropicAdapter
from model_router.services.adapters.groq import GroqAdapter, MockGroqAdapter
from model_router.services.adapters.deepseek import DeepSeekAdapter, MockDeepSeekAdapter


# Create router service instance
def create_router_service() -> ModelRouterService:
    """Create router service with appropriate adapters."""
    if config.testing:
        providers = {
            ProviderName.OPENAI: MockOpenAIAdapter(),
            ProviderName.ANTHROPIC: MockAnthropicAdapter(),
            ProviderName.GROQ: MockGroqAdapter(),
            ProviderName.DEEPSEEK: MockDeepSeekAdapter(),
        }
    else:
        providers = {
            ProviderName.OPENAI: OpenAIAdapter(config.openai_api_key),
            ProviderName.ANTHROPIC: AnthropicAdapter(config.anthropic_api_key),
            ProviderName.GROQ: GroqAdapter(config.groq_api_key),
            ProviderName.DEEPSEEK: DeepSeekAdapter(config.deepseek_api_key),
        }
    
    return ModelRouterService(providers)


# Create single instance to use across all requests
router_service = create_router_service()
router = APIRouter()


@router.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest) -> ChatCompletionResponse:
    """Create a chat completion using the appropriate AI provider."""
    try:
        return await router_service.create_chat_completion(request)
    except ProviderNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProviderNotConfiguredError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ModelNotSupportedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProviderAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/v1/models")
async def list_models() -> Dict[str, List[str]]:
    """List all available models grouped by provider."""
    return await router_service.get_available_models()


@router.get("/v1/providers", response_model=List[ProviderInfo])
async def list_providers() -> List[ProviderInfo]:
    """List all configured providers and their status."""
    return await router_service.get_provider_info()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}