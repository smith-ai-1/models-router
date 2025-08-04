"""User service."""

from typing import Optional

from model_router.domain.user import User
from model_router.domain.call_context import CallContext
from model_router.storages.user_storage import InMemoryUserStorage
from model_router.logger import get_logger


class UserService:
    """Service for user operations."""

    def __init__(self, user_storage: InMemoryUserStorage):
        self._user_storage = user_storage
        self._logger = get_logger(__name__)

    async def get_user_by_uid(
        self, uid: str, call_context: Optional[CallContext] = None
    ) -> Optional[User]:
        """Get user by UID."""
        self._logger.info(f"Getting user by UID: {uid}", call_context=call_context)
        return await self._user_storage.get_by_uid(uid)