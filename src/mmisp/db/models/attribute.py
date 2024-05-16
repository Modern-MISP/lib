from typing import Self, Type

from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta

from mmisp.db.mixins import DictMixin
from mmisp.lib.attributes import categories, default_category, mapper_safe_clsname_val, to_ids
from mmisp.util.uuid import uuid

from ..database import Base
from .event import Event
from .tag import Tag


class Attribute(Base, DictMixin):
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(String(40), unique=True, default=uuid, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    object_id = Column(Integer, nullable=False, default=0, index=True)
    object_relation = Column(String(255), index=True)
    category = Column(String(255), nullable=False, index=True)
    type = Column(String(100), nullable=False, index=True)
    value1 = Column(Text, nullable=False)
    value2 = Column(Text, nullable=False, default="")
    to_ids = Column(Boolean, default=True, nullable=False)
    timestamp = Column(Integer, nullable=False, default=0)
    distribution = Column(Integer, nullable=False, default=0)
    sharing_group_id = Column(Integer, index=True, default=0)
    comment = Column(Text)
    deleted = Column(Boolean, nullable=False, default=False)
    disable_correlation = Column(Boolean, nullable=False, default=False)
    first_seen = Column(BigInteger, index=True)
    last_seen = Column(BigInteger, index=True)

    event = relationship("Event", back_populates="attributes", lazy="joined")

    __mapper_args__ = {"polymorphic_on": "type"}

    def __init__(self: Self, *arg, **kwargs) -> None:
        if kwargs["value1"] is None:
            split_val = kwargs["value"].split("|", 1)
            kwargs["value1"] = split_val[0]
            if len(split_val) == 2:
                kwargs["value2"] = split_val[1]

        super().__init__(*arg, **kwargs)

    @property
    def event_uuid(self: "Attribute") -> str:
        return self.event.uuid

    @hybrid_property
    def value(self: Self) -> str:
        if self.value2 == "":
            return self.value1
        return f"{self.value1}|{self.value2}"

    @value.setter
    def value(self: Self, value: str) -> None:
        split = value.split("|", 1)
        self.value1 = split[0]
        if len(split) == 2:
            self.value2 = split[1]


class AttributeTag(Base):
    __tablename__ = "attribute_tags"

    id = Column(Integer, primary_key=True, nullable=False)
    attribute_id = Column(Integer, ForeignKey(Attribute.id, ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey(Event.id, ondelete="CASCADE"), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey(Tag.id, ondelete="CASCADE"), nullable=False, index=True)
    local = Column(Boolean, nullable=False, default=False)


class AttributeMeta(DeclarativeMeta):
    def __new__(cls: Type[type], clsname: str, bases: tuple, dct: dict) -> "AttributeMeta":
        key = clsname[len("Attribute") :]
        dct["default_category"] = default_category[mapper_safe_clsname_val[key]]
        dct["categories"] = categories[mapper_safe_clsname_val[key]]
        dct["default_to_ids"] = to_ids[mapper_safe_clsname_val[key]]
        dct["__mapper_args__"] = {"polymorphic_identity": mapper_safe_clsname_val[key]}
        return super().__new__(cls, clsname, bases, dct)


for k, _ in mapper_safe_clsname_val.items():
    vars()["Attribute" + k] = AttributeMeta("Attribute" + k, (Attribute,), dict())
