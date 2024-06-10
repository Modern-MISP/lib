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

