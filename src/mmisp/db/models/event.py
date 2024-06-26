from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from mmisp.db.mypy import Mapped, mapped_column
from mmisp.util.uuid import uuid

from ..database import Base
from .organisation import Organisation
from .tag import Tag
from .user import User


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(40), unique=True, default=uuid, nullable=False, index=True)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey(Organisation.id), nullable=False, index=True)
    date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    info: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    analysis: Mapped[int] = mapped_column(Integer, nullable=False)
    attribute_count: Mapped[int] = mapped_column(Integer, default=0)
    orgc_id: Mapped[int] = mapped_column(Integer, ForeignKey(Organisation.id), nullable=False, index=True)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=0)
    proposal_email_lock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    threat_level_id: Mapped[int] = mapped_column(Integer, nullable=False)
    publish_timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sighting_timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    disable_correlation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    extends_uuid: Mapped[str] = mapped_column(String(40), default="", index=True)
    protected: Mapped[bool] = mapped_column(Boolean)

    attributes = relationship("Attribute", back_populates="event")


class EventReport(Base):
    __tablename__ = "event_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, default=uuid)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey(Event.id), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class EventTag(Base):
    __tablename__ = "event_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey(Event.id, ondelete="CASCADE"), nullable=False, index=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey(Tag.id, ondelete="CASCADE"), nullable=False, index=True)
    local: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
