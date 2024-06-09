from pydantic import BaseModel

class AddServer(BaseModel):
    serverId: str
    all_orgs: bool
