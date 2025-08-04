"""Provider constants and enums."""

from enum import Enum


class ProviderName(str, Enum):
    """Enum for provider names."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    DEEPSEEK = "deepseek"


class ProviderPrefix(str, Enum):
    """Enum for provider prefixes used in model names."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    DEEPSEEK = "deepseek"