from pydantic import BaseModel, PositiveInt, conint


class SearchAuthKeyBody(BaseModel):
    page: PositiveInt | None = 1
    limit: conint(gt=0, lt=500) | None = 25  # type: ignore
    id: str | None = None
    uuid: str | None = None
    authkey_start: str | None = None
    authkey_end: str | None = None
    created: str | None = None
    expiration: str | None = None
    read_only: bool | None = None
    user_id: str | None = None
    comment: str | None = None
    allowed_ips: str | list[str] | None = None
    last_used: str | None = None  # deprecated
