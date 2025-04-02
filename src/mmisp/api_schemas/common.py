from datetime import datetime

from pydantic import BaseModel


class TagAttributesResponse(BaseModel):
    id: int
    name: str
    colour: str
    exportable: bool
    org_id: int | None = None
    user_id: int | None = None
    hide_tag: bool | None = None
    numerical_value: str | None = None
    is_galaxy: bool | None = None
    is_custom_galaxy: bool | None = None
    local_only: bool | None = None


class User(BaseModel):
    id: int
    org_id: int
    email: str
    autoalert: bool
    invited_by: int
    gpgkey: str | None = None
    certif_public: str | None = None
    termsaccepted: bool
    role_id: int
    change_pw: bool
    contactalert: bool
    disabled: bool
    expiration: datetime | int | None = None
    current_login: int
    """time in seconds"""
    last_login: int
    """time in seconds"""
    force_logout: bool
    date_created: int
    """time in seconds"""
    date_modified: int
    """time in seconds"""
    external_auth_required: bool
    external_auth_key: str | None = None
    last_api_access: int
    """time in seconds"""
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    totp: str | None = None
    hotp_counter: int | None = None
    last_pw_change: int | None = None
    """time in seconds"""
