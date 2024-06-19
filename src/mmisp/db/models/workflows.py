from sqlalchemy import Boolean, Integer, String

from ..database import Base
from ...workflows.legacy import JSONGraphType
from mmisp.db.mypy import Mapped, mapped_column

from uuid import uuid4 as _uuid4


def uuid() -> str:
    return str(_uuid4())


class Workflows(Base):
    """
    A python class representation of the database model for workflows in MISP.

    The most central of the attributes in this model is the data attribute,
    containing the information about the workflow structure and the modules contained in the workflow,
    represented/stored as a JSON-String.
    (The other attributes are what their name sais, e.g. counter represents the numer
    of times the workflow was executed.)
    """

    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(40), default=uuid, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(191), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(191), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    trigger_id: Mapped[str] = mapped_column(String(191), nullable=False, index=True)
    debug_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=0)
    data: Mapped[str] = mapped_column(String, nullable=False, default=0)
