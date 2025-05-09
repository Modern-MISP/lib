from datetime import datetime
from typing import Self

from pydantic import BaseModel, field_serializer


class BaseOrganisation(BaseModel):
    id: int | None = None
    name: str | None = None
    nationality: str | None = None
    sector: str | None = None
    type: str | None = None
    uuid: str | None = None


class Organisation(BaseOrganisation):
    date_created: datetime
    date_modified: datetime
    description: str | None = None
    created_by: int
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: list | str | None = None
    landingpage: str | None = None

    @field_serializer("date_created", "date_modified")
    def serialize_timestamp(self: Self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


class GetOrganisationResponse(BaseModel):
    id: int
    name: str
    nationality: str | None = None
    sector: str | None = None
    type: str | None = None
    uuid: str | None = None
    # the fallback GENERIC_MISP_ORGANISATION doesn't have this property
    # str is needed because its returned as string
    date_created: datetime | None = None
    date_modified: datetime | None = None
    description: str | None = None
    created_by: int
    contacts: str | None = None
    local: bool
    restricted_to_domain: list | str | None = None
    landingpage: str | None = None

    @field_serializer("date_created", "date_modified")
    def serialize_timestamp(self: Self, value: datetime | None) -> str:
        if value is None:
            return ""
        return value.strftime("%Y-%m-%d %H:%M:%S")


class GetAllOrganisationsOrganisation(GetOrganisationResponse):
    user_count: int
    created_by_email: str


class GetAllOrganisationResponse(BaseModel):
    Organisation: GetAllOrganisationsOrganisation


class DeleteForceUpdateOrganisationResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str


class OrganisationUsersResponse(BaseModel):
    id: int
    name: str
    date_created: datetime | None = None
    date_modified: datetime | None = None
    description: str | None = None
    type: str | None = None
    nationality: str | None = None
    sector: str | None = None
    created_by: int | None = None
    uuid: str | None = None
    contacts: str | None = None
    local: bool | None = None
    restricted_to_domain: list | str | None = None
    landingpage: str | None = None

    @field_serializer("date_created", "date_modified")
    def serialize_timestamp(self: Self, value: datetime | None) -> str:
        if value is None:
            return ""
        return value.strftime("%Y-%m-%d %H:%M:%S")


class AddOrganisation(BaseModel):
    id: int
    name: str
    description: str | None = None
    type: str
    nationality: str | None = None
    sector: str | None = None
    created_by: int
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: list[str] | None = None
    landingpage: str | None = None


class EditOrganisation(BaseModel):
    name: str
    description: str | None = None
    type: str
    nationality: str | None = None
    sector: str | None = None
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: list[str] | None = None
    landingpage: str | None = None


class ShadowAttributeOrganisation(BaseModel):
    name: str
    uuid: str
    id: int


class ServerOrganisation(BaseModel):
    id: int
    name: str
    uuid: str
    nationality: str
    sector: str
    type: str
