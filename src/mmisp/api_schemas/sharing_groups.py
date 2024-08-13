from datetime import datetime

from pydantic import BaseModel, Field

from mmisp.api_schemas.organisations import Organisation
from mmisp.api_schemas.responses.standard_status_response import StandardStatusResponse


class SharingGroup(BaseModel):
    id: str
    name: str
    releasability: str
    description: str
    uuid: str
    organisation_uuid: str
    org_id: str
    sync_user_id: str
    active: bool
    created: datetime
    modified: datetime
    local: bool
    roaming: bool


class SharingGroupServer(BaseModel):
    id: str
    sharing_group_id: str
    server_id: str
    all_orgs: bool


class SharingGroupOrg(BaseModel):
    id: str
    sharing_group_id: str
    org_id: str
    extend: bool


class GetAllSharingGroupsResponseResponseItemSharingGroup(BaseModel):
    id: str
    uuid: str
    name: str
    description: str
    releasability: str
    local: bool
    active: bool
    roaming: bool
    org_count: str


class DeleteSharingGroupLegacyResponse(StandardStatusResponse):
    id: str


class ViewUpdateSharingGroupLegacyResponseServerInfo(BaseModel):
    id: str
    name: str
    url: str


class ViewUpdateSharingGroupLegacyResponseSharingGroupServerItem(BaseModel):
    id: str
    sharing_group_id: str
    server_id: str
    all_orgs: bool
    Server: ViewUpdateSharingGroupLegacyResponseServerInfo


class ViewUpdateSharingGroupLegacyResponseOrganisationInfo(BaseModel):
    id: str
    uuid: str
    name: str
    local: bool


class ViewUpdateSharingGroupLegacyResponseSharingGroupOrgItem(BaseModel):
    id: str
    sharing_group_id: str
    org_id: str
    extend: bool
    Organisation: ViewUpdateSharingGroupLegacyResponseOrganisationInfo


class ViewUpdateSharingGroupLegacyResponse(BaseModel):
    SharingGroup: SharingGroup
    Organisation: Organisation
    SharingGroupOrg: list[ViewUpdateSharingGroupLegacyResponseSharingGroupOrgItem]
    SharingGroupServer: list[ViewUpdateSharingGroupLegacyResponseSharingGroupServerItem]


class UpdateSharingGroupLegacyBody(BaseModel):
    id: str | None = None
    """attribute will be ignored"""
    uuid: str | None = Field(default=None, max_length=36)
    """attribute will be ignored"""
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=65535)
    releasability: str | None = Field(default=None, max_length=65535)
    local: bool | None = None
    active: bool | None = None
    org_count: str | None = None
    """attribute will be ignored"""
    organisation_uuid: str | None = Field(default=None, max_length=36)
    """attribute will be ignored"""
    org_id: str | None = Field(default=None, max_length=10)
    """attribute will be ignored"""
    sync_user_id: str | None = Field(default=None, max_length=10)
    """attribute will be ignored"""
    created: datetime | None = None
    """attribute will be ignored"""
    modified: datetime | None = None
    """attribute will be ignored"""
    roaming: bool | None = None


class UpdateSharingGroupBody(BaseModel):
    name: str = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=65535)
    releasability: str = Field(default=None, max_length=65535)
    active: bool | None = None
    roaming: bool | None = None
    local: bool | None = None


class GetSharingGroupInfoResponseServerInfo(BaseModel):
    id: str
    name: str
    url: str


class GetSharingGroupInfoResponseSharingGroupServerItem(BaseModel):
    id: str
    sharing_group_id: str
    server_id: str
    all_orgs: bool
    Server: GetSharingGroupInfoResponseServerInfo


class GetSharingGroupInfoResponseOrganisationInfo(BaseModel):
    id: str
    uuid: str
    name: str
    local: bool


class GetSharingGroupInfoResponseSharingGroupOrgItem(BaseModel):
    id: str
    sharing_group_id: str
    org_id: str
    extend: bool
    Organisation: GetSharingGroupInfoResponseOrganisationInfo


class GetSharingGroupInfoResponseSharingGroupInfo(SharingGroup):
    org_count: int


class GetAllSharingGroupsResponseOrganisationInfo(BaseModel):
    id: str
    uuid: str
    name: str


class GetSharingGroupInfoResponse(BaseModel):
    SharingGroup: GetSharingGroupInfoResponseSharingGroupInfo
    Organisation: Organisation
    SharingGroupOrg: list[GetSharingGroupInfoResponseSharingGroupOrgItem]
    SharingGroupServer: list[GetSharingGroupInfoResponseSharingGroupServerItem]


class GetAllSharingGroupsResponseResponseItemSharingGroupOrgItem(BaseModel):
    id: str
    sharing_group_id: str
    org_id: str
    extend: bool
    Organisation: GetAllSharingGroupsResponseOrganisationInfo


class GetAllSharingGroupsResponseResponseItemSharingGroupServerItemServer(BaseModel):
    id: str
    name: str
    url: str


class GetAllSharingGroupsResponseResponseItemSharingGroupServerItem(BaseModel):
    server_id: str
    sharing_group_id: str
    all_orgs: bool
    Server: GetAllSharingGroupsResponseResponseItemSharingGroupServerItemServer


class GetAllSharingGroupsResponseResponseItem(BaseModel):
    SharingGroup: GetAllSharingGroupsResponseResponseItemSharingGroup
    Organisation: GetAllSharingGroupsResponseOrganisationInfo
    SharingGroupOrg: list[GetAllSharingGroupsResponseResponseItemSharingGroupOrgItem]
    SharingGroupServer: list[GetAllSharingGroupsResponseResponseItemSharingGroupServerItem]
    editable: bool
    deletable: bool


class GetAllSharingGroupsResponse(BaseModel):
    response: list[GetAllSharingGroupsResponseResponseItem]


class CreateSharingGroupLegacyResponseOrganisationInfo(BaseModel):
    id: str
    name: str
    uuid: str


class CreateSharingGroupLegacyResponse(BaseModel):
    SharingGroup: SharingGroup
    Organisation: CreateSharingGroupLegacyResponseOrganisationInfo
    SharingGroupOrg: list[SharingGroupOrg]
    SharingGroupServer: list[SharingGroupServer]


class CreateSharingGroupLegacyBody(BaseModel):
    uuid: str | None = None
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=65535)
    releasability: str | None = Field(default=None, max_length=65535)
    local: bool | None = None
    active: bool | None = None
    org_count: str | None = None
    """attribute will be ignored"""
    organisation_uuid: str | None = Field(default=None, max_length=36)
    org_id: str | None = Field(default=None, max_length=10)
    sync_user_id: str | None = Field(default=None, max_length=10)
    """attribute will be ignored"""
    created: datetime | None = None
    """attribute will be ignored"""
    modified: datetime | None = None
    """attribute will be ignored"""
    roaming: bool | None = None


class CreateSharingGroupBody(BaseModel):
    uuid: str | None = None
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=65535)
    releasability: str = Field(max_length=65535)
    organisation_uuid: str | None = Field(default=None, max_length=36)
    active: bool | None = None
    roaming: bool | None = None
    local: bool | None = None


class AddServerToSharingGroupLegacyBody(BaseModel):
    all_orgs: bool | None = None


class AddServerToSharingGroupBody(BaseModel):
    serverId: str
    all_orgs: bool | None = None


class AddOrgToSharingGroupLegacyBody(BaseModel):
    extend: bool | None = None


class AddOrgToSharingGroupBody(BaseModel):
    organisationId: str
    extend: bool | None = None
