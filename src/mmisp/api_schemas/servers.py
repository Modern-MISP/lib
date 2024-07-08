from pydantic import BaseModel

class AddServer(BaseModel):
    serverId: str
    all_orgs: bool

class RemoveServer (BaseModel):
    id: str
    sharing_group_id: str
    server_id: str
    all_orgs: bool

class ServersGetVersion(BaseModel):
    pass

class GetRemoteServersResponse(BaseModel):
    id: int
    name: str
    url: str
    authkey: str
    org_id: int | None = None
    push: bool
    pull: bool
    push_sightings: bool | None = None
    push_galaxy_clusters: bool | None = None
    pull_galaxy_clusters: bool | None = None
    remote_org_id: int
    publish_without_email: bool | None = None
    unpublish_event: bool | None = None
    self_signed: bool
    internal: bool | None = None
    skip_proxy: bool | None = None
    caching_enabled: bool | None = None
    priority: int | None = None
