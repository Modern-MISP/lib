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
    gpgkey: str
    certif_public: str
    termsaccepted: bool
    role_id: str
    change_pw: bool
    contactalert: bool
    disabled: bool
    expiration: datetime
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
    external_auth_key: str
    last_api_access: str
    """time in seconds"""
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    totp: str | None = None
    hotp_counter: str | None = None
    last_pw_change: str
    """time in seconds"""

    class Config:
        orm_mode = True


class UsersViewMeResponse(BaseModel):
    User: User
    Role: Role
    UserSetting: list = []
    Organisation: Organisation


class UserAttributesResponse(BaseModel):
    id: str
    org_id: str | None = None
    email: str | None = None
    autoalert: bool
    invited_by: str | None = None
    gpgkey: str | None = None
    certif_public: str | None = None
    termsaccepted: bool | None = None
    role_id: str | None = None
    change_pw: bool | None = None
    contactalert: bool
    disabled: bool
    expiration: str | None = None
    current_login: str | None = None
    last_login: str | None = None
    force_logout: bool
    date_created:str
    date_modified: str | None = None
    external_auth_required: bool
    external_auth_key: str | None = None
    last_api_access: str | None = None
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    totp: str | None = None
    hotp_counter: str | None = None
    last_pw_change: str | None = None
