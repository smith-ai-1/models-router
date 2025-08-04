"""Model router service."""


from model_router.domain.call_context import CallContext
from model_router.domain.exceptions import (
    ProviderNotConfiguredError,
)
from model_router.domain.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ProviderInfo,
)
from model_router.logger import get_logger
from model_router.services.adapters.base import ProviderAdapter


class ModelRouterService:
    """Service for routing requests to appropriate AI providers."""

    def __init__(self, providers: dict[str, ProviderAdapter]):
        self._providers = providers
        self._provider_by_prefix = {}
        for provider in providers.values():
            prefix_str = provider.prefix.value if hasattr(provider.prefix, 'value') else str(provider.prefix)
            self._provider_by_prefix[prefix_str] = provider
        self._logger = get_logger(__name__)

    def get_provider_for_model(self, model: str) -> ProviderAdapter:
        """Get the appropriate provider for a given model."""
        if "/" not in model:
            # For backward compatibility, treat as "Model not found" (404)
            from model_router.domain.exceptions import ModelNotSupportedError
            raise ModelNotSupportedError(f"Model {model} not found")

        prefix = model.split("/")[0]

        if prefix not in self._provider_by_prefix:
            # For backward compatibility, treat as "Model not found" (404)
            from model_router.domain.exceptions import ModelNotSupportedError
            raise ModelNotSupportedError(f"Model {model} not found")

        provider = self._provider_by_prefix[prefix]

        if not provider.is_configured():
            raise ProviderNotConfiguredError(f"Provider '{prefix}' is not configured")

        return provider

    async def create_chat_completion(
        self, request: ChatCompletionRequest, call_context: CallContext | None = None
    ) -> ChatCompletionResponse:
        """Route chat completion request to appropriate provider."""
        self._logger.info(
            f"Routing chat completion for model: {request.model}",
            call_context=call_context
        )

        provider = self.get_provider_for_model(request.model)
        return await provider.create_chat_completion(request)

    async def get_provider_info(self, call_context: CallContext | None = None) -> list[ProviderInfo]:
        """Get information about all configured providers."""
        self._logger.info("Getting provider information", call_context=call_context)

        provider_info = []

        for provider in self._providers.values():
            available_models = await provider.get_available_models()

            prefix_str = provider.prefix.value if hasattr(provider.prefix, 'value') else str(provider.prefix)
            provider_info.append(ProviderInfo(
                name=provider.provider_name,
                prefix=prefix_str,
                configured=provider.is_configured(),
                available_models=available_models
            ))

        return provider_info

    async def get_available_models(self, call_context: CallContext | None = None) -> dict[str, list[str]]:
        """Get all available models grouped by provider."""
        self._logger.info("Getting available models", call_context=call_context)

        models_by_provider = {}

        for provider in self._providers.values():
            if provider.is_configured():
                models = await provider.get_available_models()
                # Add prefix to model names
                prefix_str = provider.prefix.value if hasattr(provider.prefix, 'value') else str(provider.prefix)
                prefixed_models = [f"{prefix_str}/{model}" for model in models]
                models_by_provider[provider.provider_name] = prefixed_models

        return models_by_provider
