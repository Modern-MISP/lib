from pydantic import BaseModel


class SearchGetAuthKeysResponseItemUser(BaseModel):
    id: str
    email: str


class SearchGetAuthKeysResponseItemAuthKey(BaseModel):
    id: str
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str
    read_only: bool
    user_id: str
    comment: str
    allowed_ips: list[str]
    unique_ips: list[str]


class SearchGetAuthKeysResponseItem(BaseModel):
    AuthKey: SearchGetAuthKeysResponseItemAuthKey
    User: SearchGetAuthKeysResponseItemUser

    class Config:
        orm_mode = True
