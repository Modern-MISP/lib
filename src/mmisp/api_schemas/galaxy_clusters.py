from datetime import datetime

from pydantic import BaseModel

from mmisp.api_schemas.events import AddEditGetEventGalaxyClusterRelation, GetAllEventsGalaxyClusterGalaxy
from mmisp.api_schemas.galaxy_common import GetAllSearchGalaxiesAttributes
from mmisp.api_schemas.organisations import GetOrganisationResponse, Organisation


class ExportGalaxyGalaxyElement(BaseModel):
    id: str | None = None
    galaxy_cluster_id: str | None = None
    key: str
    value: str


class GetGalaxyClusterResponse(BaseModel):
    id: str | None = None
    uuid: str | None = None
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: str
    source: str
    authors: list[str]
    version: str
    distribution: str
    sharing_group_id: str
    org_id: str
    orgc_id: str
    default: bool
    locked: bool
    extends_uuid: str | None = None
    extends_version: str
    published: bool
    deleted: bool
    Galaxy: GetAllSearchGalaxiesAttributes
    GalaxyElement: list[ExportGalaxyGalaxyElement]
    GalaxyClusterRelation: list
    RelationshipInbound: list
    Org: GetOrganisationResponse
    Orgc: GetOrganisationResponse


class GalaxyClusterResponse(BaseModel):
    GalaxyCluster: GetGalaxyClusterResponse

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class ExportGalaxyClusterResponse(BaseModel):
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
    distribution: str
    sharing_group_id: str
    org_id: str
    orgc_id: str
    default: bool
    locked: bool
    extends_uuid: str
    extends_version: str
    published: bool
    deleted: bool
    GalaxyElement: list[ExportGalaxyGalaxyElement]
    Galaxy: GetAllEventsGalaxyClusterGalaxy
    GalaxyClusterRelation: list[AddEditGetEventGalaxyClusterRelation] = []
    Org: Organisation
    Orgc: Organisation
