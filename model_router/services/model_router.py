"""Model router service."""

from typing import Dict, List

from model_router.domain.exceptions import ProviderNotFoundError, ProviderNotConfiguredError
from model_router.domain.models import ChatCompletionRequest, ChatCompletionResponse, ProviderInfo
from model_router.services.adapters.base import ProviderAdapter


class ModelRouterService:
    """Service for routing requests to appropriate AI providers."""

    def __init__(self, providers: Dict[str, ProviderAdapter]):
        self._providers = providers
        self._provider_by_prefix = {
            provider.prefix: provider for provider in providers.values()
        }

    def get_provider_for_model(self, model: str) -> ProviderAdapter:
        """Get the appropriate provider for a given model."""
        if "/" not in model:
            raise ProviderNotFoundError(f"Model '{model}' must include provider prefix (e.g., 'openai/{model}')")

        prefix = model.split("/")[0]
        
        if prefix not in self._provider_by_prefix:
            raise ProviderNotFoundError(f"No provider found for prefix '{prefix}'")

        provider = self._provider_by_prefix[prefix]
        
        if not provider.is_configured():
            raise ProviderNotConfiguredError(f"Provider '{prefix}' is not configured")

        return provider

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        """Route chat completion request to appropriate provider."""
        provider = self.get_provider_for_model(request.model)
        return await provider.create_chat_completion(request)

    async def get_provider_info(self) -> List[ProviderInfo]:
        """Get information about all configured providers."""
        provider_info = []
        
        for provider in self._providers.values():
            available_models = await provider.get_available_models()
            
            provider_info.append(ProviderInfo(
                name=provider.provider_name,
                prefix=provider.prefix,
                configured=provider.is_configured(),
                available_models=available_models
            ))

        return provider_info

    async def get_available_models(self) -> Dict[str, List[str]]:
        """Get all available models grouped by provider."""
        models_by_provider = {}
        
        for provider in self._providers.values():
            if provider.is_configured():
                models = await provider.get_available_models()
                # Add prefix to model names
                prefixed_models = [f"{provider.prefix}/{model}" for model in models]
                models_by_provider[provider.provider_name] = prefixed_models
        
        return models_by_provider