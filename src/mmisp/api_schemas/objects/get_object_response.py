from pydantic import BaseModel

from mmisp.api_schemas.attributes.get_all_attributes_response import GetAllAttributesResponse
from mmisp.api_schemas.events.get_event_response import ObjectEventResponse


class ObjectWithAttributesAndEventResponse(BaseModel):
    id: str
    name: str
    description: str
    meta_category: str
    event_id: str
    distribution: str
    template_uuid: str | None = None
    template_version: str | None = None
    uuid: str | None = None
    timestamp: str | None = None
    sharing_group_id: str | None = None
    comment: str | None = None
    deleted: bool | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    attributes: list[GetAllAttributesResponse] | None = None
    event: ObjectEventResponse | None = None


class ObjectViewResponse(BaseModel):
    object: ObjectWithAttributesAndEventResponse

    class Config:
        orm_mode = True
