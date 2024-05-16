from typing import Optional

from pydantic import BaseModel, Field


class AddAttributeAttributes(BaseModel):
    id: str
    event_id: str
    object_id: str
    object_relation: Optional[str] = Field(..., nullable=True)
    category: str
    type: str
    value: str
    value1: str
    value2: str
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: str
    sharing_group_id: str
    comment: str | None = None
    deleted: bool
    disable_correlation: bool
    first_seen: str | None = None
    last_seen: str | None = None
    attribute_tag: list[str] | None = Field(default_factory=list, alias="AttributeTag")


class AddAttributeResponse(BaseModel):
    Attribute: AddAttributeAttributes

    class Config:
        orm_mode = True
