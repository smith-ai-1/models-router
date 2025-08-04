"""Application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()


class AppConfig:
    """Application configuration from environment variables."""

    def __init__(self):
        self.testing: bool = os.getenv("TESTING", "false").lower() == "true"
        self.openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
        self.groq_api_key: str | None = os.getenv("GROQ_API_KEY")
        self.deepseek_api_key: str | None = os.getenv("DEEPSEEK_API_KEY")

    def validate_required_keys(self) -> None:
        """Validate that at least one API key is configured."""
        if self.testing:
            return

        api_keys = [
            self.openai_api_key,
            self.anthropic_api_key,
            self.groq_api_key,
            self.deepseek_api_key,
        ]

        if not any(api_keys):
            raise ValueError("At least one API key must be configured")


config = AppConfig()
