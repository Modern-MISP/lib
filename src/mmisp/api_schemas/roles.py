from datetime import datetime

from pydantic import BaseModel

from mmisp.lib.permissions import Permission


class Role(BaseModel):
    id: int
    name: str
    created: datetime | str | None = None
    modified: datetime | str | None = None
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
    default_role: bool
    memory_limit: str | None
    max_execution_time: str | None
    restricted_to_site_admin: bool
    perm_publish_zmq: bool
    """Allow users to publish data to the ZMQ pubsub channel via the publish event to ZMQ button."""
    perm_publish_kafka: bool
    """Allow users to publish data to Kafka via the publish event to Kafka button."""
    perm_decaying: bool
    """Create or modify MISP Decaying Models."""
    enforce_rate_limit: bool
    rate_limit_count: str  # number as string
    perm_galaxy_editor: bool
    """Create or modify MISP Galaxies and MISP Galaxies Clusters."""
    perm_warninglist: bool
    """Allow to manage warninglists."""
    perm_view_feed_correlations: bool
    """Allow the viewing of feed correlations. Enabling this can come at a performance cost."""
    permission: str | None  # number as string
    permission_description: str | None
    perm_skip_otp: bool | None = None
    perm_server_sign: bool | None = None

    class Config:
        orm_mode = True


class RoleUsersResponse(BaseModel):
    id: int
    name: str
    created: datetime | str | None = None
    modified: datetime | str | None = None
    perm_add: bool | None = None
    perm_modify: bool | None = None
    perm_modify_org: bool | None = None
    perm_publish: bool | None = None
    perm_delegate: bool | None = None
    perm_sync: bool | None = None
    perm_admin: bool | None = None
    perm_audit: bool | None = None
    perm_auth: bool
    perm_site_admin: bool
    perm_regexp_access: bool | None = None
    perm_tagger: bool | None = None
    perm_template: bool | None = None
    perm_sharing_group: bool | None = None
    perm_tag_editor: bool | None = None
    perm_sighting: bool | None = None
    perm_object_template: bool | None = None
    default_role: bool | None = None
    memory_limit: str | None = None
    max_execution_time: str | None = None
    restricted_to_site_admin: bool | None = None
    perm_publish_zmq: bool | None = None
    perm_publish_kafka: bool | None = None
    perm_decaying: bool | None = None
    enforce_rate_limit: bool | None = None
    rate_limit_count: str | None = None  # number as string
    perm_galaxy_editor: bool | None = None
    perm_warninglist: bool | None = None
    perm_view_feed_correlations: bool | None = None
    perm_skip_otp: bool | None = None
    perm_server_sign: bool | None = None


class RoleAttributeResponse(BaseModel):
    id: int
    name: str
    created: datetime | str | None = None
    modified: datetime | str | None = None
    perm_add: bool
    perm_modify: bool
    perm_modify_org: bool
    perm_publish: bool
    perm_delegate: bool
    perm_sync: bool
    perm_admin: bool
    perm_audit: bool
    perm_auth: bool
    perm_site_admin: bool
    perm_regexp_access: bool
    perm_tagger: bool
    perm_template: bool
    perm_sharing_group: bool
    perm_tag_editor: bool
    perm_sighting: bool
    perm_object_template: bool
    default_role: bool
    memory_limit: str | None
    max_execution_time: str | None
    restricted_to_site_admin: bool
    perm_publish_zmq: bool
    perm_publish_kafka: bool
    perm_decaying: bool
    enforce_rate_limit: bool
    rate_limit_count: int
    perm_galaxy_editor: bool
    perm_warninglist: bool
    perm_view_feed_correlations: bool
    perm_analyst_data: bool | None = None
    permission: int | None = None
    permission_description: str | None = None
    default: bool | None = False
    perm_skip_otp: bool | None = False
    perm_server_sign: bool | None = None

    def __init__(self, **data):
        super().__init__(**data)

        if self.perm_add and self.perm_modify and self.perm_publish:
            self.permission = 3
            self.permission_description = "publish"
        elif self.perm_add and self.perm_modify_org:
            self.permission = 2
            self.permission_description = "manage_org"
        elif self.perm_add and self.perm_modify:
            self.permission = 1
            self.permission_description = "manage_own"
        else:
            self.permission = 0
            self.permission_description = "read_only"

        if self.default_role:
            self.default = True


class GetRolesResponse(BaseModel):
    Role: RoleAttributeResponse

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class GetRoleResponse(BaseModel):
    Role: RoleAttributeResponse | None = None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class AddRoleBody(BaseModel):
    name: str
    perm_add: bool
    perm_modify: bool
    perm_modify_org: bool
    perm_publish: bool
    perm_delegate: bool
    perm_sync: bool
    perm_admin: bool
    perm_audit: bool
    perm_auth: bool
    perm_site_admin: bool
    perm_regexp_access: bool
    perm_tagger: bool
    perm_template: bool
    perm_sharing_group: bool
    perm_tag_editor: bool
    perm_sighting: bool
    perm_object_template: bool
    default_role: bool
    memory_limit: str | None = None
    max_execution_time: str | None = None
    restricted_to_site_admin: bool
    perm_publish_zmq: bool
    perm_publish_kafka: bool
    perm_decaying: bool
    enforce_rate_limit: bool
    rate_limit_count: int
    perm_galaxy_editor: bool
    perm_warninglist: bool
    perm_view_feed_correlations: bool


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


class EditRoleBody(BaseModel):
    name: str | None = None
    perm_add: bool | None = None
    perm_modify: bool | None = None
    perm_modify_org: bool | None = None
    perm_publish: bool | None = None
    perm_delegate: bool | None = None
    perm_sync: bool | None = None
    perm_admin: bool | None = None
    perm_audit: bool | None = None
    perm_auth: bool | None = None
    perm_site_admin: bool | None = None
    perm_regexp_access: bool | None = None
    perm_tagger: bool | None = None
    perm_template: bool | None = None
    perm_sharing_group: bool | None = None
    perm_tag_editor: bool | None = None
    perm_sighting: bool | None = None
    perm_object_template: bool | None = None
    default_role: bool | None = None
    memory_limit: str | None = None
    max_execution_time: str | None = None
    restricted_to_site_admin: bool | None = None
    perm_publish_zmq: bool | None = None
    perm_publish_kafka: bool | None = None
    perm_decaying: bool | None = None
    enforce_rate_limit: bool | None = None
    perm_galaxy_editor: bool | None = None
    perm_warninglist: bool | None = None
    perm_view_feed_correlations: bool | None = None


class EditRoleResponse(BaseModel):
    Role: RoleAttributeResponse

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}

    @classmethod
    def from_role(cls, role_data: dict):
        role_data.pop("default", None)
        return cls(Role=RoleAttributeResponse(**role_data))


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
