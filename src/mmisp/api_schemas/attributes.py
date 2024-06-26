from typing import Annotated, Any, Dict, Optional

from pydantic import BaseModel, Field, root_validator, validator

from mmisp.lib.attributes import (
    AttributeCategories,
    default_category,
    inverted_categories,
    literal_valid_attribute_types,
    mapper_val_safe_clsname,
    to_ids,
)


class GetAttributeTag(BaseModel):
    id: str
    name: str
    colour: str
    numerical_value: int | None = None
    is_galaxy: bool
    local: bool


class SearchAttributesObject(BaseModel):
    id: str
    distribution: str
    sharing_group_id: str


class SearchAttributesEvent(BaseModel):
    id: str
    org_id: str
    distribution: str
    info: str
    orgc_id: str
    uuid: str


class SearchAttributesAttributesDetails(BaseModel):
    id: str
    event_id: str | None = None
    object_id: str | None = None
    object_relation: str | None = None
    category: str
    type: str
    value: str
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: str
    sharing_group_id: str | None = None
    comment: str | None = None
    deleted: bool
    disable_correlation: bool
    first_seen: str | None = None
    last_seen: str | None = None
    Event: SearchAttributesEvent | None = None
    Object: SearchAttributesObject | None = None
    Tag: list[GetAttributeTag] = []


class SearchAttributesAttributes(BaseModel):
    Attribute: list[SearchAttributesAttributesDetails]


class SearchAttributesResponse(BaseModel):
    response: SearchAttributesAttributes


class SearchAttributesModelOverridesBaseScoreConfig(BaseModel):
    estimative_language_confidence_in_analytic_judgment: Annotated[
        int, Field(alias="estimative-language:confidence-in-analytic-judgment")
    ]
    estimative_language_likelihood_probability: Annotated[
        int, Field(alias="estimative-language:likelihood-probability")
    ]
    phishing_psychological_acceptability: Annotated[int, Field(alias="phishing:psychological-acceptability")]
    phishing_state: Annotated[int, Field(alias="phishing:state")]


class SearchAttributesModelOverrides(BaseModel):
    lifetime: int
    decay_speed: int
    threshold: int
    default_base_score: int
    base_score_config: SearchAttributesModelOverridesBaseScoreConfig


class SearchAttributesBody(BaseModel):
    returnFormat: str = "json"
    page: int | None = None
    limit: int | None = None
    value: str | None = None
    value1: str | None = None
    value2: str | None = None
    type: str | None = None
    category: str | None = None
    org: str | None = None
    tags: list[str] | None = None
    from_: str | None = None
    to: str | None = None
    last: int | None = None
    eventid: str | None = None
    with_attachments: Annotated[bool | None, Field(alias="withAttachments")] = None
    uuid: str | None = None
    publish_timestamp: str | None = None
    published: bool | None = None
    timestamp: str | None = None
    attribute_timestamp: str | None = None
    enforce_warninglist: Annotated[bool | None, Field(alias="enforceWarninglist")]
    to_ids: bool | None = None
    deleted: bool | None = None
    event_timestamp: str | None = None
    threat_level_id: str | None = None
    eventinfo: str | None = None
    sharinggroup: list[str] | None = None
    decaying_model: Annotated[str | None, Field(alias="decayingModel")] = None
    score: str | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    include_event_uuid: Annotated[bool | None, Field(alias="includeEventUuid")] = None
    include_event_tags: Annotated[bool | None, Field(alias="includeEventTags")] = None
    include_proposals: Annotated[bool | None, Field(alias="includeProposals")] = None
    requested_attributes: list[str] | None = None
    include_context: Annotated[bool | None, Field(alias="includeContext")] = None
    headerless: bool | None = None
    include_warninglist_hits: Annotated[bool | None, Field(alias="includeWarninglistHits")] = None
    attack_galaxy: Annotated[str | None, Field(alias="attackGalaxy")] = None
    object_relation: str | None = None
    include_sightings: Annotated[bool | None, Field(alias="includeSightings")] = None
    include_correlations: Annotated[bool | None, Field(alias="includeCorrelations")] = None
    model_overrides: Annotated[SearchAttributesModelOverrides | None, Field(alias="modelOverrides")] = None
    include_decay_score: Annotated[bool | None, Field(alias="includeDecayScore")] = None
    include_full_model: Annotated[bool | None, Field(alias="includeFullModel")] = None
    exclude_decayed: Annotated[bool | None, Field(alias="excludeDecayed")] = None

    class Config:
        orm_mode = True


class RestoreAttributeResponse(BaseModel):
    id: str
    event_id: str
    object_id: str
    object_relation: str
    category: str
    type: str
    value: str
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
    event_uuid: str  # new

    class Config:
        orm_mode = True


class GetDescribeTypesAttributes(BaseModel):
    sane_defaults: dict = {}
    for k, v in to_ids.items():
        sane_defaults.update(
            {
                k: {
                    "default_category": default_category[k],
                    "to_ids": v,
                }
            }
        )

    types: list[str] = list(mapper_val_safe_clsname.keys())

    categories: list[str] = [member.value for member in AttributeCategories]

    category_type_mappings: dict = inverted_categories


class GetDescribeTypesResponse(BaseModel):
    result: GetDescribeTypesAttributes

    class Config:
        orm_mode = True


class GetAttributeAttributes(BaseModel):
    id: str
    event_id: str
    object_id: str
    object_relation: Optional[str] = Field(..., nullable=True)
    category: str
    type: str
    value: str
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: str
    sharing_group_id: str
    comment: str | None = None
    deleted: bool
    disable_correlation: bool
    first_seen: Optional[str] = Field(..., nullable=True)
    last_seen: Optional[str] = Field(..., nullable=True)
    event_uuid: str
    tag: list[GetAttributeTag] | None = None


class GetAttributeResponse(BaseModel):
    Attribute: GetAttributeAttributes

    class Config:
        orm_mode = True


class GetAllAttributesResponse(BaseModel):
    id: str
    event_id: str | None = None
    object_id: str | None = None
    object_relation: str | None = None
    category: str | None = None
    type: str
    value1: str | None = None
    value2: str | None = None
    to_ids: bool | None = None
    uuid: str | None = None
    timestamp: str | None = None
    distribution: str | None = None
    sharing_group_id: str | None = None
    comment: str | None = None
    deleted: bool | None = None
    disable_correlation: bool | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    value: str | None = None

    @validator("sharing_group_id", always=True)
    def check_sharing_group_id(cls, value: Any, values: Dict[str, Any]) -> Optional[int]:  # noqa: ANN101
        """
        If distribution equals 4, sharing_group_id will be shown.
        """
        distribution = values.get("distribution", None)
        if distribution == "4" and value is not None:
            return value
        return None

    class Config:
        orm_mode = True


class EditAttributeTag(BaseModel):
    id: str
    name: str
    colour: str
    exportable: str
    user_id: str
    hide_tag: bool
    numerical_value: int
    is_galaxy: bool
    is_costum_galaxy: bool
    local_only: bool


class EditAttributeAttributes(BaseModel):
    id: str
    event_id: str
    object_id: str
    object_relation: str | None = None
    category: str
    type: str
    value: str
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
    tag: list[EditAttributeTag]


class EditAttributeResponse(BaseModel):
    Attribute: EditAttributeAttributes

    class Config:
        orm_mode = True


class EditAttributeBody(BaseModel):
    type: str | None = None
    value: str | None = None
    value1: str | None = None
    value2: str | None = None
    object_id: str | None = None
    object_relation: str | None = None
    category: str | None = None
    to_ids: bool | None = None
    uuid: str | None = None
    timestamp: str | None = None
    distribution: str | None = None
    sharing_group_id: str | None = None
    comment: str | None = None
    deleted: bool | None = None
    disable_correlation: bool | None = None
    first_seen: str | None = None
    last_seen: str | None = None

    class Config:
        orm_mode = True


class DeleteSelectedAttributeResponse(BaseModel):
    saved: bool
    success: bool
    name: str
    message: str
    url: str
    id: str

    class Config:
        orm_mode = True


class DeleteSelectedAttributeBody(BaseModel):
    id: str  # id = "all" deletes all attributes in the event
    allow_hard_delete: bool | None = None

    class Config:
        orm_mode = True


class DeleteAttributeResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True


class AddRemoveTagAttributeResponse(BaseModel):
    saved: bool
    success: Optional[str]
    check_publish: Optional[bool]
    errors: Optional[str]

    class Config:
        orm_mode = True


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


class AddAttributeBody(BaseModel):
    type: literal_valid_attribute_types
    value: str | None = None
    value1: str | None = None
    value2: str | None = None
    event_id: str | None = None
    object_id: str | None = None
    object_relation: str | None = None
    category: str | None = None
    to_ids: bool | None = None
    uuid: str | None = None
    timestamp: str | None = None
    distribution: str | None = None
    sharing_group_id: str | None = None
    comment: str | None = None
    deleted: bool | None = None
    disable_correlation: bool | None = None
    first_seen: str | None = None
    last_seen: str | None = None

    @root_validator
    def ensure_value_or_value1_is_set(cls, data: dict[str, Any]) -> Optional[dict[str, Any]]:  # noqa: ANN101
        required_values: list[str] = [str(data.get("value")), str(data.get("value1"))]
        if all(item is None for item in required_values):
            raise ValueError("value or value1 has to be set")
        return data


GetAttributeStatisticsTypesResponseAttrs = {x: Field(default=None) for x in mapper_val_safe_clsname.keys()}
GetAttributeStatisticsTypesResponseAttrs["__annotations__"] = {x: str | None for x in mapper_val_safe_clsname.keys()}
GetAttributeStatisticsTypesResponse = type(
    "GetAttributeStatisticsTypesResponse", (BaseModel,), GetAttributeStatisticsTypesResponseAttrs
)


class GetAttributeStatisticsCategoriesResponse(BaseModel):
    antivirus_detection: str = Field(alias="Antivirus detection")
    artifacts_dropped: str = Field(alias="Artifacts dropped")
    attribution: str = Field(alias="Attribution")
    external_analysis: str = Field(alias="External analysis")
    financial_fraud: str = Field(alias="Financial fraud")
    internal_reference: str = Field(alias="Internal reference")
    network_activity: str = Field(alias="Network activity")
    other: str = Field(alias="Other")
    payload_delivery: str = Field(alias="Payload delivery")
    payload_installation: str = Field(alias="Payload installation")
    payload_type: str = Field(alias="Payload type")
    persistence_mechanism: str = Field(alias="Persistence mechanism")
    person: str = Field(alias="Person")
    social_network: str = Field(alias="Social network")
    support__tool: str = Field(alias="Support Tool")
    targeting_data: str = Field(alias="Targeting data")

    class Config:
        orm_mode = True
