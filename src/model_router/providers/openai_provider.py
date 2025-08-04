"""OpenAI provider implementation."""


from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI provider."""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)

    def get_available_models(self) -> list[str]:
        """Get list of available OpenAI models."""
        return [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-4o-mini",
        ]

    async def create_chat_completion(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        temperature: float = 1.0,
        max_tokens: int | None = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stream: bool = False,
        stop: str | list[str] | None = None,
        n: int = 1,
    ) -> ChatCompletion:
        """Create chat completion using OpenAI."""

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=stream,
            stop=stop,
            n=n,
        )

        return response
