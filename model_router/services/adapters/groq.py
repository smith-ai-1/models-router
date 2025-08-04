"""Groq provider adapter."""

import time
from typing import List

from model_router.domain.exceptions import ProviderNotConfiguredError
from model_router.domain.models import ChatCompletionRequest, ChatCompletionResponse
from model_router.domain.providers import ProviderName, ProviderPrefix
from .base import ProviderAdapter


class GroqAdapter(ProviderAdapter):
    """Groq provider adapter."""

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key

    @property
    def provider_name(self) -> str:
        return ProviderName.GROQ

    @property
    def prefix(self) -> str:
        return ProviderPrefix.GROQ

    def is_configured(self) -> bool:
        return self._api_key is not None

    async def get_available_models(self) -> List[str]:
        return [
            "llama-3.1-405b-reasoning",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
        ]

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        if not self.is_configured():
            raise ProviderNotConfiguredError("Groq API key not configured")
        
        raise NotImplementedError("Groq integration not yet implemented")


class MockGroqAdapter(ProviderAdapter):
    """Mock Groq adapter for testing."""

    @property
    def provider_name(self) -> str:
        return "Groq (Mock)"

    @property
    def prefix(self) -> str:
        return ProviderPrefix.GROQ

    def is_configured(self) -> bool:
        return True

    async def get_available_models(self) -> List[str]:
        return ["llama-3.1-70b-versatile", "llama-3.1-8b-instant"]

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        return ChatCompletionResponse(
            id="chatcmpl-mock-groq",
            object="chat.completion",
            created=int(time.time()),
            model=self.extract_model_name(request.model),
            choices=[{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response from Groq adapter."
                },
                "finish_reason": "stop"
            }],
            usage={"prompt_tokens": 8, "completion_tokens": 8, "total_tokens": 16}
        )