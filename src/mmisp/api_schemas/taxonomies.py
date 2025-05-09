from pydantic import BaseModel, ConfigDict

from mmisp.api_schemas.common import TagAttributesResponse


class ImportTaxonomyEntry(BaseModel):
    value: str
    numerical_value: int
    colour: str
    description: str
    expanded: str


class ImportTaxonomyValues(BaseModel):
    predicate: str
    entry: list[ImportTaxonomyEntry]


class ImportTaxonomyPredicates(BaseModel):
    value: str
    numerical_value: int | None = None
    colour: str | None = None
    description: str | None = None
    expanded: str | None = None
    exclusive: bool | None = None


class ImportTaxonomyFile(BaseModel):
    namespace: str
    description: str
    version: int
    exclusive: bool | None = None
    expanded: str
    type: list[str]
    refs: list[str]
    predicates: list[ImportTaxonomyPredicates]
    values: list[ImportTaxonomyValues] | None = None


class TaxonomyEntrySchema(BaseModel):
    tag: str
    expanded: str
    exclusive_predicate: bool
    description: str
    existing_tag: bool | TagAttributesResponse


class TaxonomyTagEntrySchema(BaseModel):
    tag: str
    expanded: str
    exclusive_predicate: bool
    description: str
    existing_tag: bool | TagAttributesResponse
    events: int
    attributes: int


class GetTagTaxonomyResponse(BaseModel):
    id: int
    namespace: str
    description: str
    version: int
    enabled: bool
    exclusive: bool
    required: bool
    highlighted: bool
    entries: list[TaxonomyTagEntrySchema]
    model_config = ConfigDict(from_attributes=True)


class TaxonomyView(BaseModel):
    id: int
    namespace: str
    description: str
    version: int
    enabled: bool
    exclusive: bool
    required: bool
    highlighted: bool


class ViewTaxonomyResponse(BaseModel):
    Taxonomy: TaxonomyView
    total_count: int
    current_count: int
    model_config = ConfigDict(from_attributes=True)


class GetIdTaxonomyResponse(BaseModel):
    id: int
    namespace: str
    description: str
    version: int
    enabled: bool
    exclusive: bool
    required: bool
    highlighted: bool
    entries: list[TaxonomyEntrySchema]
    model_config = ConfigDict(from_attributes=True)


class GetIdTaxonomyResponseWrapper(BaseModel):
    Taxonomy: GetIdTaxonomyResponse


class ExportTaxonomyEntry(BaseModel):
    value: str
    expanded: str
    description: str


class TaxonomyValueSchema(BaseModel):
    predicate: str
    entry: list[ExportTaxonomyEntry]


class TaxonomyPredicateSchema(BaseModel):
    value: str
    expanded: str
    description: str


class ExportTaxonomyResponse(BaseModel):
    namespace: str
    description: str
    version: int
    exclusive: bool
    predicates: list[TaxonomyPredicateSchema]
    values: list[TaxonomyValueSchema]
    model_config = ConfigDict(from_attributes=True)
