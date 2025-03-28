import importlib.metadata
from typing import TYPE_CHECKING

from packaging.version import Version

sa_version = Version(importlib.metadata.version("sqlalchemy"))

if TYPE_CHECKING or sa_version >= Version("2.0"):
    from sqlalchemy.orm import Mapped, mapped_column  # type:ignore[attr-defined]
else:
    from sqlalchemy import Column

    Mapped = Column
    mapped_column = Column
