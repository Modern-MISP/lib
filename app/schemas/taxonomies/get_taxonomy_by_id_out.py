from pydantic import BaseModel

from app.schemas.tag_schema import TagSchema


class TaxonomyEntrySchema:
    tag: str
    expanded: str
    exclusive_predicate: bool
    description: str
    existing_tag: bool | TagSchema  # Kann auch Tag Objekt sein, nicht zwingend bool laut Pflichtenheft. In Implementierung schauen


class TaxonomyEntrySchema(BaseModel):
    id: str
    namespace: str
    description: str
    version: str
    enabled: bool
    exclusive: bool
    required: bool
    highlighted: bool

    class Config:
        orm_mode = True
