from datetime import datetime

from pydantic import BaseModel


class Organisation(BaseModel):
    id: str
    name: str
    date_created: datetime
    date_modified: datetime
    description: str | None = None
    type: str
    nationality: str | None = None
    sector: str | None = None
    created_by: str
    uuid: str
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: str | None = None
    landingpage: str | None = None

    class Config:
        orm_mode = True


class GetOrganisationResponse(BaseModel):
    id: str
    name: str
    date_created: datetime
    date_modified: datetime
    description: str | None = None
    type: str | None = None
    nationality: str | None = None
    sector: str | None = None
    created_by: str
    uuid: str | None = None
    contacts: str | None = None
    local: bool
    restricted_to_domain: str | None = None
    landingpage: str | None = None


class GetAllOrganisationsOrganisation(BaseModel):
    id: str
    name: str
    date_created: datetime
    date_modified: datetime
    description: str | None = None
    type: str | None = None
    nationality: str | None = None
    sector: str | None = None
    created_by: str
    uuid: str | None = None
    contacts: str | None = None
    local: bool
    restricted_to_domain: str | None = None
    landingpage: str | None = None
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

    class Config:
        orm_mode = True


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
    restricted_to_domain: str | None = None
    landingpage: str | None = None


class AddOrganisation(BaseModel):
    id: str
    name: str
    description: str | None = None
    type: str
    nationality: str | None = None
    sector: str | None = None
    created_by: str
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: str | None = None
    landingpage: str | None = None

    class Config:
        orm_mode = True


class EditOrganisation(BaseModel):
    name: str
    description: str | None = None
    type: str
    nationality: str | None = None
    sector: str | None = None
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: str | None = None
    landingpage: str | None = None

    class Config:
        orm_mode = True
