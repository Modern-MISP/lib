from typing import Self

from sqlalchemy import Boolean, DateTime, Integer, String

from mmisp.db.mypy import mapped_column
from mmisp.lib.permissions import Permission

from ..database import Base

RoleAttrs = {
    "__tablename__": "roles",
    "id": mapped_column(Integer, primary_key=True, nullable=False),
    "name": mapped_column(String(255), nullable=False),
    "created": mapped_column(DateTime, default=None),
    "modified": mapped_column(DateTime, default=None),
    "default_role": mapped_column(Boolean, nullable=False, default=False),
    "memory_limit": mapped_column(String(255), default=""),
    "max_execution_time": mapped_column(String(255), default=""),
    "restricted_to_site_admin": mapped_column(Boolean, nullable=False, default=False),
    "enforce_rate_limit": mapped_column(Boolean, nullable=False, default=False),
    "rate_limit_count": mapped_column(Integer, nullable=False, default=0),
} | {f"perm_{x.value}": mapped_column(Boolean, default=False) for x in Permission}

RoleModel = type("RoleModel", (Base,), RoleAttrs)


class Role(RoleModel, DictMixin):  # type:ignore[misc,valid-type]
    def get_permissions(self: Self) -> set[Permission]:
        d: list[Permission] = []

        for key in self.__mapper__.c.keys():
            if key.startswith("perm_") and getattr(self, key):
                d.append(Permission(key[len("perm_") :]))

        return set(d)

    def check_permission(self: Self, permission: Permission) -> bool:
        """
        Checks whether the role has the specified permission

        args:
            self: the role itself
            permission: the permission to check

        returns:
            true if role has permission
        """
        return getattr(self, "perm_" + permission.value)
