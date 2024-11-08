from typing import Self

from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property


class DictMixin:
    def asdict(self: Self, omit: set[str] | None = None) -> dict:
        if omit is None:
            omit = set()

        unloaded = inspect(self).unloaded
        d = {}
        for key in self.__mapper__.c.keys():  # type:ignore[attr-defined]
            if key in omit:
                continue
            if not key.startswith("_") and key not in unloaded:
                d[key] = getattr(self, key)

        for key, prop in inspect(self.__class__).all_orm_descriptors.items():  # type:ignore[union-attr]
            if key in omit:
                continue
            if isinstance(prop, hybrid_property):
                d[key] = getattr(self, key)
        return d


class UpdateMixin:
    def patch(self: Self, **kwargs) -> None:
        """
        Update model fields with provided keyword arguments.
        Do not alter attributes not in kwargs

        Args:
            **kwargs: Key-value pairs to update the model fields.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def put(self: Self, **kwargs) -> None:
        """
        Update all model fields with provided keyword arguments or set them to none.

        Args:
            **kwargs: Key-value pairs to update the model fields.
        """
        for key in self.__mapper__.c.keys():  # type:ignore[attr-defined]
            if key.startswith("_"):
                continue
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, None)

        for key, prop in inspect(self.__class__).all_orm_descriptors.items():  # type:ignore[union-attr]
            if not isinstance(prop, hybrid_property):
                continue
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, None)
