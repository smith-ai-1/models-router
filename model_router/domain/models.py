"""Domain models for model router."""

from typing import Any

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: float | None = None
    max_tokens: int | None = None
    stream: bool | None = False


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[dict[str, Any]]
    usage: dict[str, int] | None = None


class ProviderInfo(BaseModel):
    name: str
    prefix: str
    configured: bool
    available_models: list[str]
