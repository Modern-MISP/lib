from typing import List

from pydantic import BaseModel

from mmisp.api_schemas.galaxy_clusters import GetGalaxyClusterResponse
from mmisp.api_schemas.galaxy_common import GetAllSearchGalaxiesAttributes


class SearchGalaxiesBody(BaseModel):
    id: str | None = None
    uuid: str | None = None
    name: str | None = None
    type: str | None = None
    description: str | None = None
    version: str | None = None
    icon: str | None = None
    namespace: str | None = None
    kill_chain_order: str | None = None
    enabled: bool | None = None
    local_only: bool | None = None

    class Config:
        orm_mode = True


class SearchGalaxiesbyValue(BaseModel):
    value: str


class ImportGalaxyGalaxy(BaseModel):
    uuid: str


class ExportGalaxyGalaxyElement(BaseModel):
    id: str | None = None
    galaxy_cluster_id: str | None = None
    key: str
    value: str


class ImportGalaxyBody(BaseModel):
    GalaxyCluster: GetGalaxyClusterResponse
    Galaxy: ImportGalaxyGalaxy

    class Config:
        orm_mode = True


class GetAllSearchGalaxiesResponse(BaseModel):
    Galaxy: GetAllSearchGalaxiesAttributes

    class Config:
        orm_mode = True


class GetGalaxyResponse(BaseModel):
    Galaxy: GetAllSearchGalaxiesAttributes
    GalaxyCluster: list[GetGalaxyClusterResponse]

    class Config:
        orm_mode = True


class GalaxySchema(BaseModel):
    id: str
    uuid: str
    name: str
    type: str
    description: str
    version: str
    icon: str
    namespace: str
    kill_chain_order: List[str]

    class Config:
        orm_mode = True


class ExportGalaxyAttributes(BaseModel):
    default: bool
    custom: bool | None = None
    distribution: str
    format: str | None = None
    download: bool | None = None


class ExportGalaxyBody(BaseModel):
    Galaxy: ExportGalaxyAttributes

    class Config:
        orm_mode = True


class DeleteForceUpdateImportGalaxyResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str

    class Config:
        orm_mode = True


class AttachClusterGalaxyResponse(BaseModel):
    saved: bool
    success: str
    check_publish: bool

    class Config:
        orm_mode = True


class AttachClusterGalaxyAttributes(BaseModel):
    target_id: int


class AttachClusterGalaxyBody(BaseModel):
    Galaxy: AttachClusterGalaxyAttributes

    class Config:
        orm_mode = True
