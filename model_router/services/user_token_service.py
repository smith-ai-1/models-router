"""User token service for authentication."""

from typing import Dict, Optional

from model_router.domain.call_context import CallContext
from model_router.logger import get_logger


class UserTokenService:
    """Service for managing user authentication tokens."""

    def __init__(self):
        # token -> user_uid mapping
        self._tokens: Dict[str, str] = {}
        self._logger = get_logger(__name__)

    def add_token(self, token: str, user_uid: str) -> None:
        """Add token for user."""
        self._tokens[token] = user_uid

    async def get_user_uid_by_token(
        self, token: str, call_context: Optional[CallContext] = None
    ) -> Optional[str]:
        """Get user UID by token."""
        self._logger.info(f"Getting user UID by token", call_context=call_context)
        return self._tokens.get(token)

    async def validate_token(
        self, token: str, call_context: Optional[CallContext] = None
    ) -> bool:
        """Check if token is valid."""
        self._logger.info(f"Validating token", call_context=call_context)
        return token in self._tokens