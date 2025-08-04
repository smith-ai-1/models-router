"""API routes for model router."""


from fastapi import APIRouter, Depends, HTTPException, Request

from model_router.config import config
from model_router.domain.call_context import CallContext
from model_router.domain.exceptions import (
    ModelNotSupportedError,
    ProviderAPIError,
    ProviderNotConfiguredError,
    ProviderNotFoundError,
)
from model_router.domain.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ProviderInfo,
)
from model_router.domain.providers import ProviderName
from model_router.logger import get_logger
from model_router.services.adapters.anthropic import (
    AnthropicAdapter,
    MockAnthropicAdapter,
)
from model_router.services.adapters.deepseek import DeepSeekAdapter, MockDeepSeekAdapter
from model_router.services.adapters.groq import GroqAdapter, MockGroqAdapter
from model_router.services.adapters.openai import MockOpenAIAdapter, OpenAIAdapter
from model_router.services.model_router import ModelRouterService


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
logger = get_logger(__name__)


def get_call_context(request: Request) -> CallContext:
    """Dependency to create CallContext from FastAPI request."""
    # Validate authorization header is present
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    # Extract user_id from Authorization header or other sources
    # For now, using None - can be enhanced later with JWT parsing
    user_id = None
    if auth_header and auth_header.startswith("Bearer "):
        # Here you could decode JWT token to get user_id
        # user_id = decode_jwt_token(auth_header[7:])
        pass

    return CallContext(user_id=user_id)


@router.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(
    chat_request: ChatCompletionRequest,
    call_context: CallContext = Depends(get_call_context)
) -> ChatCompletionResponse:
    """Create a chat completion using the appropriate AI provider."""
    logger.info(f"Chat completion request for model: {chat_request.model}", call_context=call_context)

    try:
        return await router_service.create_chat_completion(chat_request, call_context)
    except ProviderNotFoundError as e:
        logger.error(f"Provider not found: {str(e)}", call_context=call_context)
        raise HTTPException(status_code=400, detail=str(e))
    except ProviderNotConfiguredError as e:
        logger.error(f"Provider not configured: {str(e)}", call_context=call_context)
        raise HTTPException(status_code=503, detail=str(e))
    except ModelNotSupportedError as e:
        logger.error(f"Model not supported: {str(e)}", call_context=call_context)
        raise HTTPException(status_code=404, detail=str(e))
    except ProviderAPIError as e:
        logger.error(f"Provider API error: {str(e)}", call_context=call_context)
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/v1/models")
async def list_models(
    call_context: CallContext = Depends(get_call_context)
):
    """List all available models grouped by provider."""
    logger.info("Listing available models", call_context=call_context)
    models_by_provider = await router_service.get_available_models(call_context)

    # Convert to OpenAI-compatible format for backward compatibility
    model_list = []
    for provider_name, models in models_by_provider.items():
        for model in models:
            model_list.append({
                "id": model,
                "object": "model",
                "created": 1640000000,
                "owned_by": provider_name.lower().replace(" (mock)", "")
            })

    return {"object": "list", "data": model_list}


@router.get("/v1/providers", response_model=list[ProviderInfo])
async def list_providers(
    call_context: CallContext = Depends(get_call_context)
) -> list[ProviderInfo]:
    """List all configured providers and their status."""
    logger.info("Listing providers", call_context=call_context)
    return await router_service.get_provider_info(call_context)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
