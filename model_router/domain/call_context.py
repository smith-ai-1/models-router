"""Call context for tracing requests through the system."""

from dataclasses import dataclass, field

from model_router.domain.base import new_ksuid


@dataclass
class CallContext:
    """Context information for a request/call through the system."""

    user_id: str | None = None
    request_id: str | None = field(default_factory=new_ksuid)

    def __str__(self) -> str:
        return f"CallContext(user_id={self.user_id}, request_id={self.request_id})"
