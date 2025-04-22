from datetime import datetime
from typing import Self

from pydantic import BaseModel, field_serializer

from mmisp.lib.distribution import GalaxyDistributionLevels


class GetAllSearchGalaxiesAttributes(BaseModel):
    id: int
    uuid: str
    name: str
    type: str
    description: str
    version: str
    icon: str
    namespace: str
    kill_chain_order: str | None = None
    enabled: bool
    local_only: bool
    created: datetime
    modified: datetime
    org_id: int
    orgc_id: int
    default: bool
    distribution: GalaxyDistributionLevels

    @field_serializer("created", "modified")
    def serialize_timestamp(self: Self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
