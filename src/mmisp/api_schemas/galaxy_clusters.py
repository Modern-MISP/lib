from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from mmisp.api_schemas.common import NoneTag, TagAttributesResponse
from mmisp.api_schemas.events import AddEditGetEventGalaxyClusterRelation, GetAllEventsGalaxyClusterGalaxy
from mmisp.api_schemas.galaxy_common import CommonGalaxyCluster, GetAllSearchGalaxiesAttributes
from mmisp.api_schemas.organisations import GetOrganisationResponse, Organisation
from mmisp.lib.distribution import DistributionLevels


class ImportGalaxyClusterValueMeta(BaseModel):
    type: list[str]
    complexity: str


class ImportGalaxyClusterValueRelated(BaseModel):
    dest_uuid: UUID = Field(validation_alias="dest-uuid")
    type: str


class ImportGalaxyClusterValue(BaseModel):
    value: str
    uuid: UUID
    related: list[ImportGalaxyClusterValueRelated] | None = None
    description: str = ""
    revoked: bool | None = None
    meta: ImportGalaxyClusterValueMeta | None = None


class ImportGalaxyCluster(BaseModel):
    description: str
    type: str
    version: int
    name: str
    uuid: UUID
    values: list[ImportGalaxyClusterValue]
    authors: list[str]
    source: str
    category: str

    distribution: Literal[3] = 3


class ExportGalaxyGalaxyElement(BaseModel):
    id: int | None = None
    galaxy_cluster_id: int | None = None
    key: str
    value: str


class GetGalaxyClusterResponse(CommonGalaxyCluster):
    meta: None = Field(default=None, exclude=True)  # type: ignore
    tag_id: None = Field(default=None, exclude=True)  # type: ignore
    local: None = Field(default=None, exclude=True)  # type: ignore
    relationship_type: None = Field(default=None, exclude=True)  # type: ignore

    GalaxyElement: list[ExportGalaxyGalaxyElement]
    Galaxy: GetAllSearchGalaxiesAttributes | None = None
    GalaxyClusterRelation: list = []
    RelationshipInbound: list = []
    Org: GetOrganisationResponse | None = None
    Orgc: GetOrganisationResponse | None = None


class GalaxyClusterResponse(BaseModel):
    GalaxyCluster: GetGalaxyClusterResponse
    Tag: NoneTag | TagAttributesResponse = Field(default_factory=NoneTag)


class ExportGalaxyClusterResponse(BaseModel):
    id: int
    uuid: UUID
    collection_uuid: UUID
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: int
    source: str
    authors: list[str]
    version: int
    distribution: str
    sharing_group_id: int
    org_id: int
    orgc_id: int
    default: bool
    locked: bool
    extends_uuid: UUID
    extends_version: int
    published: bool
    deleted: bool
    GalaxyElement: list[ExportGalaxyGalaxyElement]
    Galaxy: GetAllEventsGalaxyClusterGalaxy
    GalaxyClusterRelation: list[AddEditGetEventGalaxyClusterRelation] = []
    Org: Organisation
    Orgc: Organisation


class AddGalaxyElement(BaseModel):
    key: str
    value: str


class AddUpdateGalaxyElement(BaseModel):
    id: int | None = None
    key: str
    value: str


class AddGalaxyClusterRequest(BaseModel):
    value: str
    description: str
    source: str
    authors: list[str]
    distribution: DistributionLevels
    GalaxyElement: list[AddGalaxyElement]


class PutGalaxyClusterRequest(BaseModel):
    id: int
    value: str
    description: str
    source: str
    type: str
    uuid: UUID
    version: int
    authors: list[str]
    distribution: DistributionLevels
    GalaxyElement: list[AddUpdateGalaxyElement]


class AddGalaxyClusterResponse(BaseModel):
    pass
