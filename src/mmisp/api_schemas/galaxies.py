from datetime import datetime
from typing import Any, List, Self

from pydantic import BaseModel, ConfigDict, field_serializer

from mmisp.api_schemas.common import TagAttributesResponse
from mmisp.api_schemas.events import AddEditGetEventGalaxyClusterRelation, GetAllEventsGalaxyClusterGalaxy
from mmisp.api_schemas.galaxy_common import GetAllSearchGalaxiesAttributes
from mmisp.api_schemas.organisations import Organisation
from mmisp.lib.distribution import GalaxyDistributionLevels


class SearchGalaxiesBody(BaseModel):
    id: int | None = None
    uuid: str | None = None
    name: str | None = None
    type: str | None = None
    description: str | None = None
    version: int | None = None
    icon: str | None = None
    namespace: str | None = None
    kill_chain_order: str | None = None
    enabled: bool | None = None
    local_only: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class SearchGalaxiesbyValue(BaseModel):
    value: str


class ImportGalaxyGalaxy(BaseModel):
    uuid: str


class ExportGalaxyGalaxyElement(BaseModel):
    id: int | None = None
    galaxy_cluster_id: int | None = None
    key: str
    value: str


class GetGalaxyClusterResponse(BaseModel):
    id: int
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: int
    source: str
    authors: list[str]
    version: int
    distribution: GalaxyDistributionLevels
    sharing_group_id: int
    org_id: int
    orgc_id: int
    default: bool
    locked: bool
    extends_uuid: str
    extends_version: int
    published: bool
    deleted: bool
    GalaxyElement: list[ExportGalaxyGalaxyElement]


class ImportGalaxyBody(BaseModel):
    GalaxyCluster: GetGalaxyClusterResponse
    Galaxy: ImportGalaxyGalaxy
    model_config = ConfigDict(from_attributes=True)


class GetAllSearchGalaxiesResponse(BaseModel):
    Galaxy: GetAllSearchGalaxiesAttributes
    model_config = ConfigDict(from_attributes=True)


class GetGalaxyResponse(BaseModel):
    Galaxy: GetAllSearchGalaxiesAttributes
    GalaxyCluster: list[GetGalaxyClusterResponse]
    model_config = ConfigDict(from_attributes=True)


class GalaxySchema(BaseModel):
    id: int
    uuid: str
    name: str
    type: str
    description: str
    version: int
    icon: str
    namespace: str
    kill_chain_order: List[str]
    created: datetime
    modified: datetime
    org_id: int
    orgc_id: int
    default: bool
    distribution: GalaxyDistributionLevels
    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created", "modified")
    def serialize_timestamp(self: Self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


class ExportGalaxyClusterResponse(BaseModel):
    id: int
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: int
    source: str
    authors: list[str]
    version: int
    distribution: GalaxyDistributionLevels
    sharing_group_id: int
    org_id: int
    orgc_id: int
    default: bool
    locked: bool
    extends_uuid: str
    extends_version: int
    published: bool
    deleted: bool
    GalaxyElement: list[ExportGalaxyGalaxyElement]
    Galaxy: GetAllEventsGalaxyClusterGalaxy
    GalaxyClusterRelation: list[AddEditGetEventGalaxyClusterRelation] = []
    Org: Organisation
    Orgc: Organisation
    model_config = ConfigDict(from_attributes=True)


class TargetingClusterRelation(BaseModel):
    id: int
    galaxy_cluster_id: int
    referenced_galaxy_cluster_id: int
    referenced_galaxy_cluster_uuid: str
    referenced_galaxy_cluster_type: str
    galaxy_cluster_uuid: str
    distribution: GalaxyDistributionLevels
    sharing_group_id: int | None = None
    default: bool
    Tag: list[TagAttributesResponse]


class GalaxyClustersViewResponse(BaseModel):
    id: int
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: int
    source: str
    authors: list[str]
    version: int
    distribution: GalaxyDistributionLevels
    sharing_group_id: int
    org_id: int
    orgc_id: int
    default: bool
    locked: bool
    extends_uuid: str
    extends_version: int
    published: bool
    deleted: bool
    GalaxyElement: list[ExportGalaxyGalaxyElement]
    Galaxy: GetAllEventsGalaxyClusterGalaxy
    GalaxyClusterRelation: list[AddEditGetEventGalaxyClusterRelation] = []
    Org: Organisation
    Orgc: Organisation
    TargetingClusterRelation: list["TargetingClusterRelation"] | None = None
    RelationshipInbound: list[Any] | None = None  # Unknown what is stored in the list, so far only receiving empty list


class ExportGalaxyAttributes(BaseModel):
    default: bool
    custom: bool | None = None
    distribution: GalaxyDistributionLevels
    format: str | None = None
    download: bool | None = None


class ExportGalaxyBody(BaseModel):
    Galaxy: ExportGalaxyAttributes
    model_config = ConfigDict(from_attributes=True)


class DeleteForceUpdateImportGalaxyResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str
    model_config = ConfigDict(from_attributes=True)


class AttachClusterGalaxyResponse(BaseModel):
    saved: bool
    success: str
    check_publish: bool
    model_config = ConfigDict(from_attributes=True)


class AttachClusterGalaxyAttributes(BaseModel):
    target_id: int


class AttachClusterGalaxyBody(BaseModel):
    Galaxy: AttachClusterGalaxyAttributes
    model_config = ConfigDict(from_attributes=True)
