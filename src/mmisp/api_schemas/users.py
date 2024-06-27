from datetime import datetime

from pydantic import BaseModel

from mmisp.api_schemas.organisations import Organisation
from mmisp.api_schemas.roles import Role


class User(BaseModel):
    id: str
    org_id: str
    email: str
    autoalert: bool
    invited_by: str
    gpgkey: str | None = None
    certif_public: str | None = None
    termsaccepted: bool
    role_id: str
    change_pw: bool
    contactalert: bool
    disabled: bool
    expiration: datetime | None = None
    current_login: str
    """time in seconds"""
    last_login: str
    """time in seconds"""
    force_logout: bool
    date_created: str
    """time in seconds"""
    date_modified: str
    """time in seconds"""
    external_auth_required: bool
    external_auth_key: str | None = None
    last_api_access: str
    """time in seconds"""
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    totp: str | None = None
    hotp_counter: str | None = None
    last_pw_change: str | None = None
    """time in seconds"""

class Config:
    orm_mode = True


class UsersViewMeResponse(BaseModel):
    User: User
    Role: Role
    UserSetting: list = []
    Organisation: Organisation


class UserAttributesBody(BaseModel):
    org_id: str | None = None
    email: str | None = None
    autoalert: bool | None = None
    gpgkey: str | None = None
    certif_public: str | None = None
    termsaccepted: bool | None = None
    role_id: str | None = None
    change_pw: bool | None = None
    contactalert: bool | None = None
    disabled: bool | None = None
    expiration: datetime | None = None
    force_logout: bool | None = None
    external_auth_required: bool | None = None
    external_auth_key: str | None = None
    notification_daily: bool | None = None
    notification_weekly: bool | None = None
    notification_monthly: bool | None = None
    totp: str | None = None
    hotp_counter: str | None = None
    name: str | None = None


class AddUserBody(BaseModel):
    org_id: str
    email: str
    gpgkey: str
    termsaccepted: bool
    role_id: str
    disabled: bool
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    totp: str | None = None
    password: str
    name: str


class AddUserResponse(BaseModel):
    id: str


class GetAllUsersUser(BaseModel):
    id: int
    organisation: int
    role: int
    nids: int
    name: str
    email: str
    last_login: int
    created: int
    totp: bool | None
    contact: bool
    notification: bool
    gpg_key: str
    terms: bool


class GetAllUsersResponse(BaseModel):
    users: list[GetAllUsersUser]


class UserWithName(BaseModel):
    user: User
    name: str
