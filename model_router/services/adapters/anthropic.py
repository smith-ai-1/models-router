"""Anthropic provider adapter."""

import time
from typing import List

from model_router.domain.exceptions import ProviderNotConfiguredError
from model_router.domain.models import ChatCompletionRequest, ChatCompletionResponse
from model_router.domain.providers import ProviderName, ProviderPrefix
from .base import ProviderAdapter


class AnthropicAdapter(ProviderAdapter):
    """Anthropic provider adapter."""

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key

    @property
    def provider_name(self) -> str:
        return ProviderName.ANTHROPIC

    @property
    def prefix(self) -> str:
        return ProviderPrefix.ANTHROPIC

    def is_configured(self) -> bool:
        return self._api_key is not None

    async def get_available_models(self) -> List[str]:
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
        ]

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        if not self.is_configured():
            raise ProviderNotConfiguredError("Anthropic API key not configured")
        
        raise NotImplementedError("Anthropic integration not yet implemented")


class MockAnthropicAdapter(ProviderAdapter):
    """Mock Anthropic adapter for testing."""

    @property
    def provider_name(self) -> str:
        return "Anthropic (Mock)"

    @property
    def prefix(self) -> str:
        return ProviderPrefix.ANTHROPIC

    def is_configured(self) -> bool:
        return True

    async def get_available_models(self) -> List[str]:
        return ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"]

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        return ChatCompletionResponse(
            id="chatcmpl-mock-anthropic",
            object="chat.completion",
            created=int(time.time()),
            model=self.extract_model_name(request.model),
            choices=[{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response from Anthropic adapter."
                },
                "finish_reason": "stop"
            }],
            usage={"prompt_tokens": 12, "completion_tokens": 12, "total_tokens": 24}
        )