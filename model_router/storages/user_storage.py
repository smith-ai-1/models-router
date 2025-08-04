"""User storage implementations."""

from typing import Dict, List, Optional

from model_router.domain.user import User


class InMemoryUserStorage:
    """In-memory storage for users."""

    def __init__(self):
        self._users: Dict[str, User] = {}

    async def get_by_uid(self, uid: str) -> Optional[User]:
        """Get user by UID."""
        return self._users.get(uid)

    async def get_all(self) -> List[User]:
        """Get all users."""
        return list(self._users.values())

    async def save(self, user: User) -> User:
        """Save user to storage."""
        self._users[user.uid] = user
        return user