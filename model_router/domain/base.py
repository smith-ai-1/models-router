"""Base domain classes."""

import datetime
from typing import TypeVar, Generic, Optional
from dataclasses import field

import ksuid
from pydantic import BaseModel, Field


def new_ksuid() -> str:
    """Generate a new KSUID string."""
    return str(ksuid.ksuid())


def utcnow() -> datetime.datetime:
    """Get current UTC datetime without timezone info."""
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)


T = TypeVar("T")


class BaseEntity(BaseModel):
    """Base class for all domain entities."""
    
    uid: str = Field(default_factory=new_ksuid)
    created_at: datetime.datetime = Field(default_factory=utcnow)
    updated_at: datetime.datetime = Field(default_factory=utcnow)

    db_exclude: set[str] = {"db_exclude"}

    def db_repr(self) -> dict:
        """Get dictionary representation excluding db_exclude fields."""
        return self.model_dump(exclude=self.db_exclude)


class Error(BaseModel):
    """Error information model."""
    code: Optional[str] = None
    message: Optional[str] = None


class DataErrorResponse(BaseModel, Generic[T]):
    """Generic response with data or error."""
    data: Optional[T] = None
    error: Optional[Error] = None