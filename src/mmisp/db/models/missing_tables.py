from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class EventTemplateObjectDependency(Base):
    __tablename__ = "event_template_object_dependencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_template_id: Mapped[int] = mapped_column(Integer)
    object_template_uuid: Mapped[str] = mapped_column(String(40))
    object_template_name: Mapped[str] = mapped_column(String(255))
    minimum_version: Mapped[int] = mapped_column(Integer)


class EventTemplate(Base):
    __tablename__ = "event_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    org_id: Mapped[int] = mapped_column(Integer)
    creator_user_id: Mapped[int] = mapped_column(Integer)
    distribution: Mapped[int] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(Boolean)
    exposed: Mapped[bool] = mapped_column(Boolean)
    misp_default: Mapped[bool] = mapped_column(Boolean)
    version: Mapped[int] = mapped_column(Integer)
    definition: Mapped[str] = mapped_column(Text)
    created: Mapped[DateTime] = mapped_column(DateTime)
    modified: Mapped[DateTime] = mapped_column(DateTime)
