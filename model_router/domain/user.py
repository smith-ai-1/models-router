"""User domain entity."""

from typing import Any

from model_router.domain.base import BaseEntity


class User(BaseEntity):
    """User domain entity."""

    email: str | None = None
    additional_info: dict[Any, Any] | None = None
