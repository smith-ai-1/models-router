"""User domain entity."""

from typing import Optional, Dict, Any

from model_router.domain.base import BaseEntity


class User(BaseEntity):
    """User domain entity."""
    
    email: Optional[str] = None
    additional_info: Optional[Dict[Any, Any]] = None