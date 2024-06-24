from typing import Union

from pydantic import BaseModel, UUID1, UUID3, UUID4, UUID5, constr
from sqlmodel import Field
from typing_extensions import Annotated


class AttributeTagRelationship(BaseModel):
    """
    Encapsulates a relationship between a MISP Event-Attribute and a Tag.
    """

    id: int | None = None
    attribute_id: int | Union[UUID1, UUID3, UUID4, UUID5] | None = None
    tag_id: int | None = None
    local: Annotated[int, Field(ge=0, le=1)] | None = None
    relationship_type: constr(min_length=1) | None = None
