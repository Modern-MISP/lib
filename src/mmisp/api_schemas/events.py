from datetime import datetime

from pydantic import BaseModel, PositiveInt, conint

from mmisp.api_schemas.organisations import Organisation


class GetAllEventsGalaxyClusterGalaxy(BaseModel):
    id: str
    uuid: str
    name: str
    type: str
    description: str
    version: str
    icon: str
    namespace: str
    enabled: bool
    local_only: bool
    kill_chain_order: str | None = None


class AddEditGetEventGalaxyClusterMeta(BaseModel):
    external_id: str | None = None
    refs: list[str] | None = None
    kill_chain: str | None = None


class FreeTextImportWorkerData(BaseModel):
    data: str


class FreeTextImportWorkerUser(BaseModel):
    user_id: int


class FreeTextImportWorkerBody(BaseModel):
    user: FreeTextImportWorkerUser
    data: FreeTextImportWorkerData

    class Config:
        orm_mode = True


class AddAttributeViaFreeTextImportEventResponse(BaseModel):
    comment: str | None = None
    value: str
    original_value: str
    to_ids: str
    type: str
    category: str
    distribution: str

    class Config:
        orm_mode = True


class AddAttributeViaFreeTextImportEventAttributes(BaseModel):
    value: str


class AddAttributeViaFreeTextImportEventBody(BaseModel):
    Attribute: AddAttributeViaFreeTextImportEventAttributes

    class Config:
        orm_mode = True


class GetAllEventsGalaxyCluster(BaseModel):
    id: str
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: str
    source: str
    authors: list[str]
    version: str
    distribution: str | None = None
    sharing_group_id: str | None = None
    org_id: str
    orgc_id: str
    default: str | None = None
    locked: bool | None = None
    extends_uuid: str
    extends_version: str
    published: bool | None = None
    deleted: bool | None = None
    Galaxy: GetAllEventsGalaxyClusterGalaxy
    meta: AddEditGetEventGalaxyClusterMeta | None = None
    tag_id: str
    local: bool | None = None
    relationship_type: bool | str | None = None


class AddEditGetEventGalaxyClusterRelationTag(BaseModel):
    id: str
    name: str
    colour: str
    exportable: bool
    org_id: str
    user_id: str
    hide_tag: bool
    numerical_value: str
    is_galaxy: bool
    is_custom_galaxy: bool
    local_only: bool


class AddEditGetEventGalaxyClusterRelation(BaseModel):
    id: str
    galaxy_cluster_id: str
    referenced_galaxy_cluster_id: str
    referenced_galaxy_cluster_uuid: str
    referenced_galaxy_cluster_type: str
    galaxy_cluster_uuid: str
    distribution: str
    sharing_group_id: str | None = None
    default: bool
    Tag: list[AddEditGetEventGalaxyClusterRelationTag] = []


class AddEditGetEventGalaxyCluster(BaseModel):
    id: str
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: str
    source: str
    authors: list[str]
    version: str
    distribution: str | None = None
    sharing_group_id: str | None = None
    org_id: str
    orgc_id: str
    default: bool | None = None
    locked: bool | None = None
    extends_uuid: str | None = None
    extends_version: str | None = None
    published: bool | None = None
    deleted: bool | None = None
    GalaxyClusterRelation: list[AddEditGetEventGalaxyClusterRelation] = []
    Org: Organisation | None = None
    Orgc: Organisation | None = None
    meta: AddEditGetEventGalaxyClusterMeta | None = None
    tag_id: str
    attribute_tag_id: str | None = None
    event_tag_id: str | None = None
    local: bool | None = None
    relationship_type: bool | str = ""


class AddEditGetEventGalaxy(BaseModel):
    id: str
    uuid: str
    name: str
    type: str
    description: str
    version: str
    icon: str
    namespace: str
    enabled: bool
    local_only: bool
    kill_chain_order: str | None = None
    GalaxyCluster: list[AddEditGetEventGalaxyCluster] = []


class AddEditGetEventOrg(BaseModel):
    id: str
    name: str
    uuid: str | None = None
    local: bool | None = None


class AddEditGetEventTag(BaseModel):
    id: str
    name: str
    colour: str
    exportable: bool
    user_id: str
    hide_tag: bool
    numerical_value: int | None = None
    is_galaxy: bool
    is_custom_galaxy: bool
    local_only: bool
    local: bool
    relationship_type: bool | str | None = None


class AddEditGetEventAttribute(BaseModel):
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
    Galaxy: list[AddEditGetEventGalaxy] = []
    ShadowAttribute: list[str] = []
    Tag: list[AddEditGetEventTag] = []


class AddEditGetEventShadowAttribute(BaseModel):
    value: str
    to_ids: bool
    type: str
    category: str


class AddEditGetEventEventReport(BaseModel):
    id: str
    uuid: str
    event_id: str
    name: str
    content: str
    distribution: str
    sharing_group_id: str
    timestamp: str
    deleted: bool


class AddEditGetEventObject(BaseModel):
    id: str
    name: str
    meta_category: str
    description: str
    template_uuid: str
    template_version: str
    event_id: str
    uuid: str
    timestamp: str
    distribution: str
    sharing_group_id: str
    comment: str
    deleted: bool
    first_seen: str | None = None
    last_seen: str | None = None
    ObjectReference: list[str] = []
    Attribute: list[AddEditGetEventAttribute] = []


class AddEditGetEventDetails(BaseModel):
    id: str
    orgc_id: str
    org_id: str
    date: str
    threat_level_id: str
    info: str
    published: bool
    uuid: str
    attribute_count: str
    analysis: str
    timestamp: str
    distribution: str
    proposal_email_lock: bool
    locked: bool
    publish_timestamp: str
    sharing_group_id: str
    disable_correlation: bool
    extends_uuid: str
    protected: bool | None = None
    event_creator_email: str
    Org: AddEditGetEventOrg
    Orgc: AddEditGetEventOrg
    Attribute: list[AddEditGetEventAttribute] = []
    ShadowAttribute: list[AddEditGetEventShadowAttribute] = []
    RelatedEvent: list[AddEditGetEventEventReport] = []
    Galaxy: list[AddEditGetEventGalaxy] = []
    Object: list[AddEditGetEventObject] = []
    EventReport: list[AddEditGetEventEventReport] = []
    CryptographicKey: list[str] = []
    Tag: list[AddEditGetEventTag] = []


class AddEditGetEventResponse(BaseModel):
    Event: AddEditGetEventDetails

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class GetAllEventsOrg(BaseModel):
    id: str
    name: str
    uuid: str | None = None


class UnpublishEventResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str
    id: str | None = None

    class Config:
        orm_mode = True


class SearchEventsResponse(BaseModel):
    response: list[AddEditGetEventResponse]

    class Config:
        orm_mode = True


class SearchEventsBody(BaseModel):
    returnFormat: str
    page: int | None = None
    limit: int | None = None
    value: str | None = None
    type: str | None = None
    category: str | None = None
    org: str | None = None
    tags: list[str] | None = None
    event_tags: list[str] | None = None
    searchall: str | None = None
    from_: str | None = None
    to: str | None = None
    last: int | None = None
    eventid: str | None = None
    withAttachments: bool | None = None
    sharinggroup: list[str] | None = None
    metadata: bool | None = None
    uuid: str | None = None
    publish_timestamp: str | None = None
    timestamp: str | None = None
    published: bool | None = None
    enforceWarninglist: bool | None = None
    sgReferenceOnly: bool | None = None
    requested_attributes: list[str] | None = None
    includeContext: bool | None = None
    headerless: bool | None = None
    includeWarninglistHits: bool | None = None
    attackGalaxy: str | None = None
    to_ids: bool | None = None
    deleted: bool | None = None
    excludeLocalTags: bool | None = None
    date: str | None = None
    includeSightingdb: bool | None = None
    tag: str | None = None
    object_relation: str | None = None
    threat_level_id: str | None = None

    class Config:
        orm_mode = True


class PublishEventResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str
    id: str | None = None

    class Config:
        orm_mode = True


class GetAllEventsEventTagTag(BaseModel):
    id: str
    name: str
    colour: str
    is_galaxy: bool


class IndexEventsEventTag(BaseModel):
    id: str
    event_id: str
    tag_id: str
    local: bool
    Tag: GetAllEventsEventTagTag


class IndexEventsAttributes(BaseModel):
    id: str
    org_id: str
    date: str
    info: str
    uuid: str
    published: bool
    analysis: str
    attribute_count: str
    orgc_id: str
    timestamp: str
    distribution: str
    sharing_group_id: str
    proposal_email_lock: bool
    locked: bool
    threat_level_id: str
    publish_timestamp: str
    sighting_timestamp: str
    disable_correlation: bool
    extends_uuid: str
    protected: bool | None = None
    Org: GetAllEventsOrg
    Orgc: GetAllEventsOrg
    GalaxyCluster: list[GetAllEventsGalaxyCluster] = []
    EventTag: list[IndexEventsEventTag] = []

    class Config:
        orm_mode = True


class IndexEventsBody(BaseModel):
    page: PositiveInt | None = None
    limit: conint(gt=0, lt=500) | None = None  # type: ignore
    sort: int | None = None
    direction: int | None = None
    minimal: bool | None = None
    attribute: str | None = None
    eventid: str | None = None
    datefrom: str | None = None
    dateuntil: str | None = None
    org: str | None = None
    eventinfo: str | None = None
    tag: str | None = None
    tags: list[str] | None = None
    distribution: str | None = None
    sharinggroup: str | None = None
    analysis: str | None = None
    threatlevel: str | None = None
    email: str | None = None
    hasproposal: str | None = None
    timestamp: str | None = None
    publish_timestamp: str | None = None
    searchDatefrom: str | None = None
    searchDateuntil: str | None = None

    class Config:
        orm_mode = True


class ObjectEventResponse(BaseModel):
    id: str
    info: str
    org_id: str | None = None
    orgc_id: str | None = None


class GetAllEventsEventTag(BaseModel):
    id: str
    event_id: str
    tag_id: str
    local: bool
    relationship_type: bool | str | None = None
    Tag: GetAllEventsEventTagTag | None = None


class GetAllEventsResponse(BaseModel):
    id: str
    org_id: str  # owner org
    distribution: str
    info: str
    orgc_id: str  # creator org
    uuid: str
    date: str
    published: bool
    analysis: str
    attribute_count: str
    timestamp: str
    sharing_group_id: str
    proposal_email_lock: bool
    locked: bool
    threat_level_id: str
    publish_timestamp: str
    sighting_timestamp: str
    disable_correlation: bool
    extends_uuid: str
    event_creator_email: str | None = None  # omitted
    protected: str | None = None
    Org: GetAllEventsOrg
    Orgc: GetAllEventsOrg
    GalaxyCluster: list[GetAllEventsGalaxyCluster]
    EventTag: list[GetAllEventsEventTag]

    class Config:
        orm_mode = True


class EditEventBody(BaseModel):
    info: str | None = None
    org_id: str | None = None
    distribution: str | None = None
    orgc_id: str | None = None
    uuid: str | None = None
    date: str | None = None
    published: bool | None = None
    analysis: str | None = None
    attribute_count: str | None = None
    timestamp: str | None = None
    sharing_group_id: str | None = None
    proposal_email_lock: bool | None = None
    locked: bool | None = None
    threat_level_id: str | None = None
    publish_timestamp: str | None = None
    sighting_timestamp: str | None = None
    disable_correlation: bool | None = None
    extends_uuid: str | None = None
    event_creator_email: str | None = None
    protected: str | None = None
    cryptographic_key: str | None = None

    class Config:
        orm_mode = True


class DeleteEventResponse(BaseModel):
    saved: bool
    success: bool | None = None
    name: str
    message: str
    url: str
    id: str
    errors: str | None = None

    class Config:
        orm_mode = True


class AddRemoveTagEventsResponse(BaseModel):
    saved: bool
    success: str | None = None
    check_publish: bool | None = None
    errors: str | None = None

    class Config:
        orm_mode = True


class AddEventBody(BaseModel):
    info: str
    org_id: str | None = None
    distribution: str | None = None
    orgc_id: str | None = None
    uuid: str | None = None
    date: str | None = None
    published: bool | None = None
    analysis: str | None = None
    attribute_count: str | None = None
    timestamp: str | None = None
    sharing_group_id: str | None = None
    proposal_email_lock: bool | None = None
    locked: bool | None = None
    threat_level_id: str | None = None
    publish_timestamp: str | None = None
    sighting_timestamp: str | None = None
    disable_correlation: bool | None = None
    extends_uuid: str | None = None
    protected: str | None = None

    class Config:
        orm_mode = True


class AddEventTag(BaseModel):
    name: str


class AddEditGetEventRelatedEventAttributesOrg(BaseModel):
    id: str
    name: str
    uuid: str


class AddEditGetEventRelatedEventAttributes(BaseModel):
    id: str
    date: str
    threat_level_id: str
    info: str
    published: str
    uuid: str
    analysis: str
    timestamp: str
    distribution: str
    org_id: str
    orgc_id: str
    Org: AddEditGetEventRelatedEventAttributesOrg
    Orgc: AddEditGetEventRelatedEventAttributesOrg


class AddEditGetEventRelatedEvent(BaseModel):
    Event: list[AddEditGetEventRelatedEventAttributes] = []
