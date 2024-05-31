from pydantic import BaseModel


class Position(BaseModel):
    x: str
    y: str
    width: str
    height: str


class Value(BaseModel):
    widget: str
    position: Position


class ViewUserSettingResponseUserSetting(BaseModel):
    id: str
    setting: str
    value: dict | list
    user_id: str
    timestamp: str


class ViewUserSettingResponse(BaseModel):
    UserSetting: ViewUserSettingResponseUserSetting


class SetUserSettingResponseUserSetting(BaseModel):
    id: str
    setting: str
    value: dict | list
    user_id: str
    timestamp: str


class SetUserSettingResponse(BaseModel):
    UserSetting: SetUserSettingResponseUserSetting


class SetUserSettingBody(BaseModel):
    value: dict | list


class SearchUserSettingResponse(BaseModel):
    id: str
    setting: str
    value: Value
    user_id: str
    timestamp: str


class SearchUserSettingBody(BaseModel):
    id: str | None = None
    setting: str | None = None
    user_id: str | None = None


class UserSettingSchema(BaseModel):
    id: str
    setting: str
    value: dict | list
    user_id: str
    timestamp: str


class UserSettingResponse(BaseModel):
    UserSetting: UserSettingSchema


class GetUserSettingResponse(BaseModel):
    id: str
    setting: str
    value: str
    user_id: str
    timestamp: str
