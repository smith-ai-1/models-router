"""Base provider interface."""

from abc import ABC, abstractmethod

from openai.types.chat import ChatCompletion, ChatCompletionMessageParam


class BaseProvider(ABC):
    """Base class for AI providers."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    async def create_chat_completion(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        temperature: float = 1.0,
        max_tokens: int = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stream: bool = False,
        stop: str | list[str] = None,
        n: int = 1,
    ) -> ChatCompletion:
        """Create chat completion."""
        pass
