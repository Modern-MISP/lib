from datetime import datetime

from pydantic import BaseModel

from mmisp.api_schemas.organisations import OrganisationUsersResponse
from mmisp.api_schemas.roles import RoleUsersResponse


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


class UserAttributesBody(BaseModel):
    org_id: str | None = None
    authkey: str | None = None
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
    nids_sid: int | None = None


class AddUserBody(BaseModel):
    authkey: str
    contactalert: bool
    nids_sid: int
    org_id: str
    email: str
    termsaccepted: bool
    disabled: bool
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    password: str
    name: str
    """role_id newly added"""
    role_id: str


class AddUserResponseData(BaseModel):
    id: str
    org_id: int
    server_id: int
    email: str
    autoalert: bool
    authkey: str
    invited_by: int
    gpgkey: str | None = None
    certif_public: str | None = None
    nids_sid: int
    termsaccepted: bool
    newsread: int | None = None
    role_id: int
    change_pw: bool
    contactalert: bool
    disabled: bool
    expiration: int | None = None
    current_login: int
    force_logout: bool
    date_created: int
    date_modified: int
    sub: str | None = None
    external_auth_required: bool
    external_auth_key: str | None = None
    last_api_access: int
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    totp: bool | None = None
    hotp_counter: int | None = None
    last_pw_change: int | None = None


class AddUserResponse(BaseModel):
    User: AddUserResponseData


class GetUsersUser(BaseModel):
    id: int
    org_id: int
    server_id: int
    email: str
    autoalert: bool
    auth_key: str | None
    invited_by: int
    gpg_key: str | None
    certif_public: str | None
    nids_sid: int
    termsaccepted: bool
    newsread: int | None
    role_id: int
    change_pw: bool
    contactalert: bool
    disabled: bool
    expiration: int | None
    current_login: int | None
    last_login: int | None
    last_api_access: int | None
    force_logout: bool
    date_created: int | None
    date_modified: int | None
    last_pw_change: int | None
    totp: bool | None
    """detailed information bellow"""
    hotp_counter: int | None
    notification_daily: bool | None
    notification_weekly: bool | None
    notification_monthly: bool | None
    external_auth_required: bool | None
    external_auth_key: str | None
    sub: str | None
    """new contents bellow"""
    name: str
    contact: bool
    notification: bool


class GetUsersElement(BaseModel):
    User: GetUsersUser
    Role: RoleUsersResponse
    Organisation: OrganisationUsersResponse
    UserSetting: dict | None = None


class GetAllUsersResponse(BaseModel):
    users: list[GetUsersElement]


class UserWithName(BaseModel):
    user: User
    name: str
