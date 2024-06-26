from sqlalchemy import Boolean, Integer, String

from mmisp.db.database import Base
from mmisp.db.mypy import Mapped, mapped_column


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    colour: Mapped[int] = mapped_column(String(7), nullable=False)
    exportable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    hide_tag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    numerical_value: Mapped[int] = mapped_column(Integer, index=True)
    is_galaxy: Mapped[bool] = mapped_column(Boolean, default=False)
    is_custom_galaxy: Mapped[bool] = mapped_column(Boolean, default=False)
    local_only: Mapped[bool] = mapped_column(Boolean, default=False)
