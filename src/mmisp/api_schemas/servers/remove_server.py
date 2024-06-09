from pydantic import BaseModel

class RemoveServer (BaseModel):
    id: str
    sharing_group_id: str
    server_id: str
    all_orgs: bool
    