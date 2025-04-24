from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field, field_serializer

from mmisp.lib.distribution import GalaxyDistributionLevels


class CommonGalaxy(BaseModel):
    id: int
    uuid: str
    name: str
    type: str
    description: str
    version: str | int
    icon: str
    namespace: str
    enabled: bool
    local_only: bool
    kill_chain_order: str | None = None
    created: datetime
    modified: datetime
    org_id: int
    orgc_id: int
    default: bool
    distribution: GalaxyDistributionLevels

    @field_serializer("created", "modified")
    def serialize_timestamp(self: Self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


class GalaxyClusterMeta(BaseModel):
    external_id: int | None = None
    refs: list[str] | None = None
    kill_chain: str | None = None


class CommonGalaxyCluster(BaseModel):
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
    version: str | int
    distribution: GalaxyDistributionLevels | None = None
    sharing_group_id: int | None = None
    org_id: int
    orgc_id: int
    default: bool | None = None
    locked: bool | None = None
    extends_uuid: str | None = None
    extends_version: str | int | None = None
    published: bool | None = None
    deleted: bool | None = None
    meta: GalaxyClusterMeta | None = None
    tag_id: int
    local: bool | None = None
    relationship_type: bool | str = ""

    TargetingClusterRelation: list = Field(default_factory=list)


class GetAllSearchGalaxiesAttributes(CommonGalaxy):
    pass
