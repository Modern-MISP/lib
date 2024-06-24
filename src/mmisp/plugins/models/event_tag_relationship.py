from typing import Union

from sqlmodel import Field
from typing_extensions import Annotated

from pydantic import BaseModel, UUID1, UUID3, UUID4, UUID5


class EventTagRelationship(BaseModel):
    """
    Encapsulates a relationship between a MISP Event and a Tag.
    """

    id: int | None = None
    event_id: int | Union[UUID1, UUID3, UUID4, UUID5]
    tag_id: int | None = None
    local: Annotated[int, Field(ge=0, le=1)] | None = None
    relationship_type: Annotated[str, StringConstraints(min_length=1)] | None = None
