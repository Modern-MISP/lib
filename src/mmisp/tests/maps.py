from itertools import product

access_test_objects_orgs = [f"org{i}" for i in range(1, 4)]

access_test_objects_users = [f"user_org{i}_{role}" for i in range(1, 4) for role in ["publisher", "read_only", "user"]]
access_test_objects_users.append("site_admin_user")

access_test_objects_user_by_org = {
    f"org{i}": [f"user_org{i}_{role}" for role in ["publisher", "read_only", "user"]] for i in range(1, 4)
}

access_test_objects_sg_by_org = {
    "org1": ["sg_org1_org2", "sg_org1_org3"],
    "org2": ["sg_org1_org2", "sg_org2_org3"],
    "org3": ["sg_org1_org3", "sg_org2_org3"],
}


def event_distribution_by_org(org):
    for i in range(0, 4):
        yield i
    for sg in access_test_objects_sg_by_org[org]:
        yield f"4_{sg}"


access_test_objects_event_by_org = {
    f"org{i}": [
        f"event_org{i}_{edl}_{pub}published" for edl in event_distribution_by_org(f"org{i}") for pub in ["", "un"]
    ]
    for i in range(1, 4)
}

site_admin_access = [
    ("site_admin_user", event) for event_list in access_test_objects_event_by_org.values() for event in event_list
]

public_events = [
    event
    for event_list in access_test_objects_event_by_org.values()
    for event in event_list
    if any(f"_{dl}_published" in event for dl in range(1, 4))
]

all_possible_user_event_pairs = set(
    (user, event)
    for user in access_test_objects_users
    for event_list in access_test_objects_event_by_org.values()
    for event in event_list
)

access_test_objects_shared_events_by_org = {
    org: [
        event
        for other_org in access_test_objects_orgs
        if other_org != org
        for event in access_test_objects_event_by_org[other_org]
        if any(sg in event for sg in access_test_objects_sg_by_org.get(org, []))
    ]
    for org in access_test_objects_orgs
}

access_test_object_user_event_sharing_group = [
    (user, event)
    for org, events in access_test_objects_shared_events_by_org.items()
    for user, event in product(access_test_objects_user_by_org[org], events)
]

access_test_object_user_event_own_org = [
    (user, event)
    for org, users in access_test_objects_user_by_org.items()
    for user in users
    for event in access_test_objects_event_by_org[org]
]

access_test_objects_public_user_event = [(user, event) for user in access_test_objects_users for event in public_events]

access_test_objects_user_event_access_expect_granted = list(
    set(
        access_test_object_user_event_sharing_group
        + access_test_object_user_event_own_org
        + site_admin_access
        + access_test_objects_public_user_event
    )
)
access_test_objects_user_event_access_expect_denied = list(
    all_possible_user_event_pairs - set(access_test_objects_user_event_access_expect_granted)
)

access_test_objects_user_event_edit_expect_granted = [
    (user, event)
    for user, event in access_test_object_user_event_own_org + access_test_object_user_event_sharing_group
    if "read_only" not in user
]
access_test_objects_user_event_edit_expect_granted.extend(site_admin_access)

access_test_objects_user_event_publish_expect_granted = [
    (user, event)
    for user, event in access_test_object_user_event_own_org + access_test_object_user_event_sharing_group
    if "publisher" in user
]
access_test_objects_user_event_publish_expect_granted.extend(site_admin_access)
