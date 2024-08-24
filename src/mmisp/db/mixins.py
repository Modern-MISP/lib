from typing import Self

from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property


class DictMixin:
    def asdict(self: Self) -> dict:
        unloaded = inspect(self).unloaded
        d = {}
        for key in self.__mapper__.c.keys():  # type:ignore[attr-defined]
            if not key.startswith("_") and key not in unloaded:
                d[key] = getattr(self, key)

        for key, prop in inspect(self.__class__).all_orm_descriptors.items():  # type:ignore[union-attr]
            if isinstance(prop, hybrid_property):
                d[key] = getattr(self, key)
        return d
