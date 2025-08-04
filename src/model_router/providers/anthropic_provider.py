"""Anthropic provider implementation."""

from .base import BaseProvider


class AnthropicProvider(BaseProvider):
    """Anthropic provider (placeholder)."""

    def get_available_models(self) -> list[str]:
        """Get list of available Anthropic models."""
        return [
            "claude-3-sonnet",
            "claude-3-opus",
            "claude-3-haiku",
            "claude-3-5-sonnet",
        ]

    async def create_chat_completion(self, **kwargs):
        """Create chat completion using Anthropic."""
        raise NotImplementedError("Anthropic provider not implemented yet")
