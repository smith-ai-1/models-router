"""Base adapter interface for AI providers."""

from abc import ABC, abstractmethod
from typing import List, AsyncGenerator

from model_router.domain.models import ChatCompletionRequest, ChatCompletionResponse


class ProviderAdapter(ABC):
    """Abstract base class for AI provider adapters."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
        pass

    @property
    @abstractmethod
    def prefix(self) -> str:
        """Return the model prefix for this provider."""
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if the provider is properly configured."""
        pass

    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """Get list of available models from the provider."""
        pass

    @abstractmethod
    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse | AsyncGenerator[str, None]:
        """Create a chat completion using the provider's API."""
        pass

    def extract_model_name(self, full_model: str) -> str:
        """Extract the actual model name from the prefixed model string."""
        prefix_str = self.prefix.value if hasattr(self.prefix, 'value') else str(self.prefix)
        prefix_with_slash = f"{prefix_str}/"
        if full_model.startswith(prefix_with_slash):
            return full_model[len(prefix_with_slash):]
        return full_model