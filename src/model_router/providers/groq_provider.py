"""Groq provider implementation."""

from .base import BaseProvider


class GroqProvider(BaseProvider):
    """Groq provider (placeholder)."""

    def get_available_models(self) -> list[str]:
        """Get list of available Groq models."""
        return [
            "llama-3.1-70b",
            "llama-3.1-8b",
            "mixtral-8x7b",
        ]

    async def create_chat_completion(self, **kwargs):
        """Create chat completion using Groq."""
        raise NotImplementedError("Groq provider not implemented yet")
