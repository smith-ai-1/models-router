"""DeepSeek provider adapter."""

import time
from typing import List

from model_router.domain.exceptions import ProviderNotConfiguredError
from model_router.domain.models import ChatCompletionRequest, ChatCompletionResponse
from model_router.domain.providers import ProviderName, ProviderPrefix
from .base import ProviderAdapter


class DeepSeekAdapter(ProviderAdapter):
    """DeepSeek provider adapter."""

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key

    @property
    def provider_name(self) -> str:
        return ProviderName.DEEPSEEK

    @property
    def prefix(self) -> str:
        return ProviderPrefix.DEEPSEEK

    def is_configured(self) -> bool:
        return self._api_key is not None

    async def get_available_models(self) -> List[str]:
        return [
            "deepseek-chat",
            "deepseek-coder",
        ]

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        if not self.is_configured():
            raise ProviderNotConfiguredError("DeepSeek API key not configured")
        
        raise NotImplementedError("DeepSeek integration not yet implemented")


class MockDeepSeekAdapter(ProviderAdapter):
    """Mock DeepSeek adapter for testing."""

    @property
    def provider_name(self) -> str:
        return "DeepSeek (Mock)"

    @property
    def prefix(self) -> str:
        return ProviderPrefix.DEEPSEEK

    def is_configured(self) -> bool:
        return True

    async def get_available_models(self) -> List[str]:
        return ["deepseek-chat", "deepseek-coder"]

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        return ChatCompletionResponse(
            id="chatcmpl-mock-deepseek",
            object="chat.completion",
            created=int(time.time()),
            model=self.extract_model_name(request.model),
            choices=[{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response from DeepSeek adapter."
                },
                "finish_reason": "stop"
            }],
            usage={"prompt_tokens": 9, "completion_tokens": 9, "total_tokens": 18}
        )