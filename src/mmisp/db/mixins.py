from typing import Self

from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property


class DictMixin:
    def asdict(self: Self) -> dict:
        d = {}
        for key in self.__mapper__.c.keys():
            if not key.startswith("_"):
                d[key] = getattr(self, key)

        for key, prop in inspect(self.__class__).all_orm_descriptors.items():
            if isinstance(prop, hybrid_property):
                d[key] = getattr(self, key)
        return d
