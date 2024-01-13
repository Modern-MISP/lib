from .sharing_group import SharingGroup
from ..organisations.organisation import Organisation
from pydantic import BaseModel


class GetSharingGroupInfoResponseSharingGroupInfo(SharingGroup):
    org_count: int
    user_count: int
    created_by_email: str


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


class GetSharingGroupInfoResponse(BaseModel):
    SharingGroup: GetSharingGroupInfoResponseSharingGroupInfo
    Organisation: Organisation
    SharingGroupOrg: list[GetSharingGroupInfoResponseSharingGroupOrgItem]
    SharingGroupServer: list[GetSharingGroupInfoResponseSharingGroupServerItem]
