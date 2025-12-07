"""Base response."""


from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")

class BaseResponse(GenericModel, Generic[T]):  # noqa: UP046
    """Base response."""

    status: bool
    message: str
    data: T | None = None
