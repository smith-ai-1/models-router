"""OpenAI provider adapter."""

import time
from typing import List, AsyncGenerator

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from model_router.domain.exceptions import ProviderAPIError, ModelNotSupportedError
from model_router.domain.models import ChatCompletionRequest, ChatCompletionResponse
from model_router.domain.providers import ProviderName, ProviderPrefix
from .base import ProviderAdapter


class OpenAIAdapter(ProviderAdapter):
    """OpenAI provider adapter."""

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key
        self._client = AsyncOpenAI(api_key=api_key) if api_key else None

    @property
    def provider_name(self) -> str:
        return ProviderName.OPENAI

    @property
    def prefix(self) -> str:
        return ProviderPrefix.OPENAI

    def is_configured(self) -> bool:
        return self._api_key is not None

    async def get_available_models(self) -> List[str]:
        return [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-4o-mini",
        ]

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse | AsyncGenerator[str, None]:
        if not self._client:
            raise ProviderAPIError("OpenAI client not configured")

        model_name = self.extract_model_name(request.model)
        available_models = await self.get_available_models()
        
        if model_name not in available_models:
            raise ModelNotSupportedError(f"Model {model_name} not supported by OpenAI")

        try:
            # Convert domain models to OpenAI format
            openai_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in request.messages
            ]

            response: ChatCompletion = await self._client.chat.completions.create(
                model=model_name,
                messages=openai_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=request.stream or False,
            )

            # Convert OpenAI response to domain model
            return ChatCompletionResponse(
                id=response.id,
                object=response.object,
                created=response.created,
                model=response.model,
                choices=[choice.model_dump() for choice in response.choices],
                usage=response.usage.model_dump() if response.usage else None,
            )

        except Exception as e:
            raise ProviderAPIError(f"OpenAI API error: {str(e)}")


class MockOpenAIAdapter(ProviderAdapter):
    """Mock OpenAI adapter for testing."""

    @property
    def provider_name(self) -> str:
        return "OpenAI (Mock)"

    @property
    def prefix(self) -> str:
        return ProviderPrefix.OPENAI

    def is_configured(self) -> bool:
        return True

    async def get_available_models(self) -> List[str]:
        return ["gpt-3.5-turbo", "gpt-4o"]

    async def create_chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        model_name = self.extract_model_name(request.model)
        return ChatCompletionResponse(
            id="chatcmpl-mock",
            object="chat.completion",
            created=int(time.time()),
            model=model_name,
            choices=[{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response from OpenAI adapter."
                },
                "finish_reason": "stop"
            }],
            usage={"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}
        )