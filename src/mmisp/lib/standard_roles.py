from mmisp.db.models.role import Role


def site_admin_role() -> Role:
    return Role(
        id=1,
        name="site_admin",
        perm_add=True,
        perm_modify=True,
        perm_modify_org=True,
        perm_publish=True,
        perm_delegate=True,
        perm_sync=True,
        perm_admin=True,
        perm_audit=True,
        perm_auth=True,
        perm_site_admin=True,
        perm_regexp_access=True,
        perm_tagger=True,
        perm_template=True,
        perm_sharing_group=True,
        perm_tag_editor=True,
        perm_sighting=True,
        perm_object_template=True,
        default_role=False,
        memory_limit="",
        max_execution_time="",
        restricted_to_site_admin=False,
        perm_publish_zmq=True,
        perm_publish_kafka=True,
        perm_decaying=True,
        enforce_rate_limit=False,
        rate_limit_count=0,
        perm_galaxy_editor=True,
        perm_warninglist=True,
        perm_view_feed_correlations=True,
    )


def org_admin_role() -> Role:
    return Role(
        id=2,
        name="admin",
        perm_add=True,
        perm_modify=True,
        perm_modify_org=True,
        perm_publish=True,
        perm_delegate=True,
        perm_sync=False,
        perm_admin=True,
        perm_audit=True,
        perm_auth=True,
        perm_site_admin=False,
        perm_regexp_access=False,
        perm_tagger=True,
        perm_template=True,
        perm_sharing_group=True,
        perm_tag_editor=True,
        perm_sighting=True,
        perm_object_template=False,
        default_role=False,
        memory_limit="",
        max_execution_time="",
        restricted_to_site_admin=False,
        perm_publish_zmq=True,
        perm_publish_kafka=True,
        perm_decaying=True,
        enforce_rate_limit=False,
        rate_limit_count=0,
        perm_galaxy_editor=True,
        perm_warninglist=False,
        perm_view_feed_correlations=False,
    )


def user_role() -> Role:
    return Role(
        id=3,
        name="user",
        perm_add=True,
        perm_modify=True,
        perm_modify_org=True,
        perm_publish=False,
        perm_delegate=False,
        perm_sync=False,
        perm_admin=False,
        perm_audit=True,
        perm_auth=True,
        perm_site_admin=False,
        perm_regexp_access=False,
        perm_tagger=True,
        perm_template=False,
        perm_sharing_group=False,
        perm_tag_editor=False,
        perm_sighting=True,
        perm_object_template=False,
        default_role=False,  # "default role" is true in Legacy Misp but "default" is false"
        memory_limit="",
        max_execution_time="",
        restricted_to_site_admin=False,
        perm_publish_zmq=False,
        perm_publish_kafka=False,
        perm_decaying=True,
        enforce_rate_limit=False,
        rate_limit_count=0,
        perm_galaxy_editor=True,
        perm_warninglist=False,
        perm_view_feed_correlations=False,
    )


def publisher_role() -> Role:
    return Role(
        id=4,
        name="publisher",
        perm_add=True,
        perm_modify=True,
        perm_modify_org=True,
        perm_publish=True,
        perm_delegate=True,
        perm_sync=False,
        perm_admin=False,
        perm_audit=True,
        perm_auth=True,
        perm_site_admin=False,
        perm_regexp_access=False,
        perm_tagger=True,
        perm_template=False,
        perm_sharing_group=False,
        perm_tag_editor=False,
        perm_sighting=True,
        perm_object_template=False,
        default_role=False,
        memory_limit="",
        max_execution_time="",
        restricted_to_site_admin=False,
        perm_publish_zmq=True,
        perm_publish_kafka=True,
        perm_decaying=True,
        enforce_rate_limit=False,
        rate_limit_count=0,
        perm_galaxy_editor=True,
        perm_warninglist=False,
        perm_view_feed_correlations=False,
    )


def sync_user_role() -> Role:
    return Role(
        id=5,
        name="sync_user",
        perm_add=True,
        perm_modify=True,
        perm_modify_org=True,
        perm_publish=True,
        perm_delegate=True,
        perm_sync=True,
        perm_admin=False,
        perm_audit=True,
        perm_auth=True,
        perm_site_admin=False,
        perm_regexp_access=False,
        perm_tagger=True,
        perm_template=False,
        perm_sharing_group=True,
        perm_tag_editor=True,
        perm_sighting=True,
        perm_object_template=False,
        default_role=False,
        memory_limit="",
        max_execution_time="",
        restricted_to_site_admin=False,
        perm_publish_zmq=True,
        perm_publish_kafka=True,
        perm_decaying=True,
        enforce_rate_limit=False,
        rate_limit_count=0,
        perm_galaxy_editor=True,
        perm_warninglist=False,
        perm_view_feed_correlations=False,
    )


def read_only_role() -> Role:
    return Role(
        id=6,
        name="read_only",
        perm_add=False,
        perm_modify=False,
        perm_modify_org=False,
        perm_publish=False,
        perm_delegate=False,
        perm_sync=False,
        perm_admin=False,
        perm_audit=True,
        perm_auth=True,
        perm_site_admin=False,
        perm_regexp_access=False,
        perm_tagger=False,
        perm_template=False,
        perm_sharing_group=False,
        perm_tag_editor=False,
        perm_sighting=False,
        perm_object_template=False,
        default_role=True,  # not the default role in Legacy Misp
        memory_limit="",
        max_execution_time="",
        restricted_to_site_admin=False,
        perm_publish_zmq=False,
        perm_publish_kafka=False,
        perm_decaying=False,
        enforce_rate_limit=False,
        rate_limit_count=0,
        perm_galaxy_editor=False,
        perm_warninglist=False,
        perm_view_feed_correlations=False,
    )


def get_standard_roles() -> list[Role]:
    return [site_admin_role(), org_admin_role(), user_role(), publisher_role(), sync_user_role(), read_only_role()]
