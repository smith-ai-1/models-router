"""Application configuration."""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class AppConfig:
    """Application configuration from environment variables."""

    def __init__(self):
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
        self.groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
        self.deepseek_api_key: Optional[str] = os.getenv("DEEPSEEK_API_KEY")

    def validate_required_keys(self) -> None:
        """Validate that at least one API key is configured."""
        api_keys = [
            self.openai_api_key,
            self.anthropic_api_key,
            self.groq_api_key,
            self.deepseek_api_key,
        ]
        
        if not any(api_keys):
            raise ValueError("At least one API key must be configured")


config = AppConfig()