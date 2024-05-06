from typing import Self

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from mmisp.lib.permissions import Permission

from ..database import Base

RoleAttrs = {
    "__tablename__": "roles",
    "id": Column(Integer, primary_key=True, nullable=False),
    "name": Column(String(255), nullable=False),
    "created": Column(DateTime, default=None),
    "modified": Column(DateTime, default=None),
    "default_role": Column(Boolean, nullable=False, default=False),
    "memory_limit": Column(String(255), default=""),
    "max_execution_time": Column(String(255), default=""),
    "restricted_to_site_admin": Column(Boolean, nullable=False, default=False),
    "enforce_rate_limit": Column(Boolean, nullable=False, default=False),
    "rate_limit_count": Column(Integer, nullable=False, default=0),
} | {f"perm_{x.value}": Column(Boolean, default=False) for x in Permission}

RoleModel = type("RoleModel", (Base,), RoleAttrs)


class Role(RoleModel):
    def get_permissions(self: Self) -> set[Permission]:
        d: list[Permission] = []

        for key in self.__mapper__.c.keys():
            if key.startswith("perm_") and getattr(self, key):
                d.append(Permission(key[len("perm_") :]))

        return set(d)
