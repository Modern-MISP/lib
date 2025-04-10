from typing import Literal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from mmisp.api_schemas.common import NoneTag, TagAttributesResponse
from mmisp.api_schemas.events import AddEditGetEventGalaxyClusterRelation, GetAllEventsGalaxyClusterGalaxy
from mmisp.api_schemas.galaxy_common import CommonGalaxyCluster, GetAllSearchGalaxiesAttributes
from mmisp.api_schemas.organisations import GetOrganisationResponse, Organisation
from mmisp.api_schemas.galaxies import RestSearchGalaxyBody
from mmisp.api_schemas.galaxy_common import GetAllSearchGalaxiesAttributes
from mmisp.api_schemas.organisations import GetOrganisationElement, Organisation, GalaxyClusterOrganisationResponse
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
    Org: GetOrganisationElement | None = None
    Orgc: GetOrganisationElement | None = None


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
    galaxy_cluster_id: int | None = None
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
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: int
    source: str
    authors: list[str]
    version: str | None = None
    distribution: DistributionLevels
    sharing_group_id: int | None = None
    org_id: int
    orgc_id: int
    default: bool
    locked: bool
    extends_uuid: str | None = None
    extends_version: str | None = None
    published: bool = False
    deleted: bool = False
    GalaxyElement: list[AddUpdateGalaxyElement]


class AddGalaxyClusterResponse(BaseModel):
    pass


class GalaxyClusterRelation(BaseModel):
    id: int
    galaxy_cluster_id: int
    referenced_galaxy_cluster_id: int
    referenced_galaxy_cluster_uuid: str
    referenced_galaxy_cluster_type: str
    galaxy_cluster_uuid: str
    distribution: str
    sharing_group_id: int | None = None
    default: bool


class SearchGalaxyClusterGalaxyClustersDetails(BaseModel):
    id: int | None = None
    uuid: str
    collection_uuid: str | None = None
    type: str | None = None
    value: str | None = None
    tag_name: str | None = None
    description: str | None = None
    galaxy_id: int | None = None
    source: str | None = None
    authors: list[str] | None = None
    version: str
    distribution: str | None = None
    sharing_group_id: int | None = None
    org_id: int | None = None
    orgc_id: int | None = None
    default: bool | None = None
    locked: bool | None = None
    extends_uuid: str | None = None
    extends_version: str | None = None
    published: bool | None = None
    deleted: bool | None = None
    GalaxyElement: Optional[list[ExportGalaxyGalaxyElement]] = None
    Galaxy: RestSearchGalaxyBody
    GalaxyClusterRelation: Optional[GalaxyClusterRelation] = None
    Org: Optional[GalaxyClusterOrganisationResponse] = None
    Orgc: Optional[GalaxyClusterOrganisationResponse] = None


class SearchGalaxyClusterGalaxyClusters(BaseModel):
    GalaxyCluster: SearchGalaxyClusterGalaxyClustersDetails


class GalaxyClusterSearchResponse(BaseModel):
    response: list[SearchGalaxyClusterGalaxyClusters]

    class Config:
        orm_mode = True


class GalaxyClusterSearchBody(BaseModel):
    limit: int | None = None
    page: int | None = None
    id: list[int] | None = None
    uuid: list[str] | None = None
    galaxy_id: int | None = None
    galaxy_uuid: str | None = None
    published: bool | None = None
    value: str | None = None
    extends_uuid: str | None = None
    extends_version: str | None = None
    version: int | None = None
    distribution: int | None = None
    org_id: int | None = None
    orgc_id: int | None = None
    tag_name: str | None = None
    custom: bool | None = None  # not sure if bool
    minimal: bool | None = None
