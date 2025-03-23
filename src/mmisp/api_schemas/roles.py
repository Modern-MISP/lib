from datetime import datetime
from typing import Any, Self

from pydantic import BaseModel

from mmisp.lib.permissions import Permission


class HasPermission(BaseModel):
    perm_add: bool
    perm_modify: bool
    """Manage Own Events."""
    perm_modify_org: bool
    """Manage Organisation Events."""
    perm_publish: bool
    """Publish Organisation Events."""
    perm_delegate: bool
    """Allow users to create delegation requests for their own org only events to trusted third parties."""
    perm_sync: bool
    """Synchronisation permission, can be used to connect two MISP instances create data on behalf of other users.
    Make sure that the role with this permission has also access to tagging and tag editing rights."""
    perm_admin: bool
    """Limited organisation admin - create, manage users of their own organisation."""
    perm_audit: bool
    """Access to the audit logs of the user\'s organisation."""
    perm_auth: bool
    """Users with this permission have access to authenticating via their Auth keys,
    granting them access to the API."""
    perm_site_admin: bool
    """Unrestricted access to any data and functionality on this instance."""
    perm_regexp_access: bool
    """Users with this role can modify the regex rules affecting how data is fed into MISP.
    Make sure that caution is advised with handing out roles that include this permission,
    user controlled executed regexes are dangerous."""
    perm_tagger: bool
    """Users with roles that include this permission can attach
    or detach existing tags to and from events/attributes."""
    perm_template: bool
    """Create or modify templates, to be used when populating events."""
    perm_sharing_group: bool
    """Permission to create or modify sharing groups."""
    perm_tag_editor: bool
    """This permission gives users the ability to create tags."""
    perm_sighting: bool
    """Permits the user to push feedback on attributes into MISP by providing sightings."""
    perm_object_template: bool
    """Create or modify MISP Object templates."""
    perm_publish_zmq: bool
    """Allow users to publish data to the ZMQ pubsub channel via the publish event to ZMQ button."""
    perm_publish_kafka: bool
    """Allow users to publish data to Kafka via the publish event to Kafka button."""
    perm_decaying: bool
    """Create or modify MISP Decaying Models."""
    perm_galaxy_editor: bool
    """Create or modify MISP Galaxies and MISP Galaxies Clusters."""
    perm_warninglist: bool
    """Allow to manage warninglists."""
    perm_view_feed_correlations: bool
    """Allow the viewing of feed correlations. Enabling this can come at a performance cost."""
    perm_skip_otp: bool | None = None
    perm_server_sign: bool | None = None
    perm_analyst_data: bool | None = None


class Role(HasPermission):
    id: int
    name: str
    created: datetime | str | None = None
    modified: datetime | str | None = None
    default_role: bool
    memory_limit: str | None
    max_execution_time: str | None
    restricted_to_site_admin: bool
    enforce_rate_limit: bool
    rate_limit_count: str  # number as string
    permission: str | None  # number as string
    permission_description: str | None


class RoleUsersResponse(HasPermission):
    id: int
    name: str
    created: datetime | str | None = None
    modified: datetime | str | None = None
    default_role: bool | None = None
    memory_limit: str | None = None
    max_execution_time: str | None = None
    restricted_to_site_admin: bool | None = None
    enforce_rate_limit: bool | None = None
    rate_limit_count: str | None = None  # number as string


class RoleAttributeResponse(HasPermission):
    id: int
    name: str
    created: datetime | str | None = None
    modified: datetime | str | None = None
    default_role: bool
    memory_limit: str | None
    max_execution_time: str | None
    restricted_to_site_admin: bool
    enforce_rate_limit: bool
    rate_limit_count: int
    permission: int | None = None
    permission_description: str | None = None
    default: bool | None = False


class GetRolesResponse(BaseModel):
    Role: RoleAttributeResponse

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class GetRoleResponse(BaseModel):
    Role: RoleAttributeResponse | None = None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class AddRoleBody(HasPermission):
    name: str
    default_role: bool
    memory_limit: str | None = None
    max_execution_time: str | None = None
    restricted_to_site_admin: bool
    enforce_rate_limit: bool
    rate_limit_count: int


class AddRoleResponse(BaseModel):
    Role: RoleAttributeResponse
    created: bool
    message: str

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class DeleteRoleResponse(BaseModel):
    Role: RoleAttributeResponse | None = None
    saved: bool
    success: bool | None = None
    name: str
    message: str
    url: str
    id: int
    errors: str | None = None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class EditRoleBody(HasPermission):
    name: str | None = None
    default_role: bool | None = None
    memory_limit: str | None = None
    max_execution_time: str | None = None
    restricted_to_site_admin: bool | None = None
    enforce_rate_limit: bool | None = None


class EditRoleResponse(BaseModel):
    Role: RoleAttributeResponse

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}

    def dict(self: Self, **kwargs) -> dict[str, Any]:
        data = super().dict(**kwargs)
        if "Role" in data:
            data["Role"].pop("default", None)
        return data


class ReinstateRoleResponse(BaseModel):
    Role: RoleAttributeResponse
    success: bool
    message: str
    url: str
    id: int

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class FilterRoleBody(BaseModel):
    # filter can be expanded by adding more criteria to filter for
    permissions: list[Permission] | None = None


class FilterRoleResponse(BaseModel):
    Role: RoleAttributeResponse

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class EditUserRoleBody(BaseModel):
    role_id: int


class EditUserRoleResponse(BaseModel):
    saved: bool
    success: bool | None = None
    name: str
    message: str
    url: str
    id: int
    Role: str | None = None


class GetUserRoleResponse(BaseModel):
    user_id: int


class DefaultRoleResponse(BaseModel):
    Role: RoleAttributeResponse | None = None
    saved: bool
    success: bool | None = None
    name: str
    message: str
    url: str
    id: int
    errors: str | None = None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}
