from pydantic import BaseModel


class EventEditBody(BaseModel):
    info: str
    threat_level_id: str
    analysis: str
    distribution: str
    sharing_group_id: str
    uuid: str
    published: bool
    timestamp: str
    date: str
    Attribute: str
    Object: str
    Shadow_Attribute: str
    EventTag: str

    class Config:
        orm_mode = True
