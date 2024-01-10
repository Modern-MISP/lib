from pydantic import BaseModel


class AttributeAttributesResponse(BaseModel):
    id: str
    event_id: str
    object_id: str
    object_relation: str
    category: str
    type: str
    value: str
    value1: str  # new
    value2: str  # new
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: str
    sharing_group_id: str
    comment: str
    deleted: bool
    disable_correlation: bool
    first_seen: str
    last_seen: str

    class Config:
        orm_mode = True


class AttributesResponse(BaseModel):
    attribute: list[AttributeAttributesResponse]

    class Config:
        orm_mode = True
