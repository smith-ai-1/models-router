"""DeepSeek provider implementation."""

from .base import BaseProvider


class DeepSeekProvider(BaseProvider):
    """DeepSeek provider (placeholder)."""

    def get_available_models(self) -> list[str]:
        """Get list of available DeepSeek models."""
        return [
            "deepseek-chat",
            "deepseek-coder",
        ]

    async def create_chat_completion(self, **kwargs):
        """Create chat completion using DeepSeek."""
        raise NotImplementedError("DeepSeek provider not implemented yet")
