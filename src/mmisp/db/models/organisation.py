from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text

from mmisp.db.mixins import DictMixin
from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class Organisation(Base, DictMixin):
    __tablename__ = "organisations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    date_modified: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(255))
    nationality: Mapped[str] = mapped_column(String(255))
    sector: Mapped[str] = mapped_column(String(255))
    created_by: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    uuid: Mapped[str] = mapped_column(String(255), unique=True)
    contacts: Mapped[str] = mapped_column(Text)
    local: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    restricted_to_domain: Mapped[str] = mapped_column(Text)
    landingpage: Mapped[str] = mapped_column(Text)
