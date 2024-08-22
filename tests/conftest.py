import asyncio
import string

import pytest
import pytest_asyncio
from nanoid import generate

from mmisp.db.database import DatabaseSessionManager, sessionmanager
from mmisp.db.models.attribute import Attribute
from mmisp.util.crypto import hash_secret

from .generators.model_generators.attribute_generator import generate_attribute
from .generators.model_generators.auth_key_generator import generate_auth_key
from .generators.model_generators.event_generator import generate_event
from .generators.model_generators.galaxy_generator import generate_galaxy
from .generators.model_generators.organisation_generator import generate_organisation
from .generators.model_generators.role_generator import (
    generate_org_admin_role,
    generate_read_only_role,
    generate_site_admin_role,
)
from .generators.model_generators.server_generator import generate_server
from .generators.model_generators.sharing_group_generator import generate_sharing_group
from .generators.model_generators.tag_generator import generate_tag
from .generators.model_generators.user_generator import generate_user
from .generators.model_generators.user_setting_generator import generate_user_name


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_connection(event_loop):
    sm = DatabaseSessionManager()
    sm.init()
    await sm.create_all()
    yield sm


@pytest_asyncio.fixture
async def db(db_connection):
    async with db_connection.session() as session:
        yield session


@pytest_asyncio.fixture
async def site_admin_role(db):
    role = generate_site_admin_role()
    db.add(role)
    await db.commit()
    yield role
    await db.delete(role)
    await db.commit()


@pytest_asyncio.fixture
async def user_role(db):
    role = generate_read_only_role()
    db.add(role)
    await db.commit()
    yield role
    await db.delete(role)
    await db.commit()


@pytest_asyncio.fixture
async def org_admin_role(db):
    role = generate_org_admin_role()
    db.add(role)
    await db.commit()
    yield role
    await db.delete(role)
    await db.commit()


@pytest_asyncio.fixture
async def instance_owner_org(db):
    instance_owner_org = generate_organisation()
    db.add(instance_owner_org)
    await db.commit()
    yield instance_owner_org
    await db.delete(instance_owner_org)
    await db.commit()


@pytest_asyncio.fixture
async def instance_org_two(db):
    org = generate_organisation()
    db.add(org)
    await db.commit()
    yield org
    await db.delete(org)
    await db.commit()


@pytest_asyncio.fixture
async def instance_two_owner_org(db):
    org = generate_organisation()
    org.local = False
    db.add(org)
    await db.commit()
    yield org
    await db.delete(org)
    await db.commit()


@pytest_asyncio.fixture
async def site_admin_user(db, site_admin_role, instance_owner_org):
    user = generate_user()
    user.org_id = instance_owner_org.id
    user.server_id = 0
    user.role_id = site_admin_role.id

    db.add(user)
    await db.commit()
    await db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    await db.commit()

    yield user
    await db.delete(user_setting)
    await db.commit()
    await db.delete(user)
    await db.commit()


@pytest_asyncio.fixture
async def view_only_user(db, user_role, instance_owner_org):
    user = generate_user()
    user.org_id = instance_owner_org.id
    user.server_id = 0
    user.role_id = user_role.id

    db.add(user)
    await db.commit()
    await db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    await db.commit()

    yield user
    await db.delete(user_setting)
    await db.commit()
    await db.delete(user)
    await db.commit()


@pytest_asyncio.fixture
async def instance_owner_org_admin_user(db, instance_owner_org, org_admin_role):
    user = generate_user()
    user.org_id = instance_owner_org.id
    user.server_id = 0
    user.role_id = org_admin_role.id

    db.add(user)
    await db.commit()
    await db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    await db.commit()

    yield user
    await db.delete(user_setting)
    await db.commit()
    await db.delete(user)
    await db.commit()


@pytest_asyncio.fixture
async def instance_two_server(db, instance_two_owner_org):
    server = generate_server()
    server.name = "Instance Two Server"
    server.org_id = instance_two_owner_org.id
    server.url = "http://instance-two.mmisp.service"

    db.add(server)
    await db.commit()
    yield server
    await db.delete(server)
    await db.commit()


@pytest_asyncio.fixture
async def instance_org_two_admin_user(db, instance_org_two, org_admin_role):
    user = generate_user()
    user.org_id = instance_org_two.id
    user.server_id = 0
    user.role_id = org_admin_role.id

    db.add(user)
    await db.commit()
    await db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    await db.commit()

    yield user
    await db.delete(user_setting)
    await db.commit()
    await db.delete(user)
    await db.commit()


@pytest_asyncio.fixture
async def instance_two_owner_org_admin_user(db, instance_two_owner_org, instance_two_server, org_admin_role):
    user = generate_user()
    user.org_id = instance_two_owner_org.id
    user.server_id = instance_two_server.id
    user.role_id = org_admin_role.id

    db.add(user)
    await db.commit()
    await db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    await db.commit()

    yield user
    await db.delete(user_setting)
    await db.commit()
    await db.delete(user)
    await db.commit()


@pytest_asyncio.fixture
async def organisation(db):
    organisation = generate_organisation()

    db.add(organisation)
    await db.commit()
    await db.refresh(organisation)

    yield organisation

    await db.delete(organisation)
    await db.commit()


@pytest_asyncio.fixture
async def event(db, organisation, site_admin_user):
    org_id = organisation.id
    event = generate_event()
    event.org_id = org_id
    event.orgc_id = org_id
    event.user_id = site_admin_user.id

    db.add(event)
    await db.commit()
    await db.refresh(event)

    yield event

    await db.delete(event)
    await db.commit()


@pytest_asyncio.fixture
async def event2(db, organisation, site_admin_user):
    org_id = organisation.id
    event = generate_event()
    event.org_id = org_id
    event.orgc_id = org_id
    event.user_id = site_admin_user.id

    db.add(event)
    await db.commit()
    await db.refresh(event)

    yield event

    await db.delete(event)
    await db.commit()


@pytest_asyncio.fixture
async def attribute(db, event):
    event_id = event.id
    attribute = generate_attribute(event_id)
    event.attribute_count += 1

    db.add(attribute)
    await db.commit()
    await db.refresh(attribute)

    yield attribute

    await db.delete(attribute)
    event.attribute_count -= 1
    await db.commit()


@pytest_asyncio.fixture
async def attribute2(db, event):
    event_id = event.id
    attribute = generate_attribute(event_id)

    db.add(attribute)
    await db.commit()
    await db.refresh(attribute)

    yield attribute

    await db.delete(attribute)
    await db.commit()


@pytest_asyncio.fixture
async def attribute_multi(db, event):
    event_id = event.id
    attribute = Attribute(value="1.2.3.4|80", type="ip-src|port", category="Network Activity", event_id=event_id)

    db.add(attribute)
    await db.commit()
    await db.refresh(attribute)

    yield attribute

    await db.delete(attribute)
    await db.commit()


@pytest_asyncio.fixture
async def tag(db):
    tag = generate_tag()

    tag.user_id = 1
    tag.org_id = 1
    tag.is_galaxy = True
    tag.exportable = True

    db.add(tag)
    await db.commit()
    await db.refresh(tag)

    yield tag

    await db.delete(tag)
    await db.commit()


@pytest_asyncio.fixture
async def sharing_group(db, instance_owner_org):
    sharing_group = generate_sharing_group()
    sharing_group.organisation_uuid = instance_owner_org.uuid
    sharing_group.org_id = instance_owner_org.id

    db.add(sharing_group)
    await db.commit()
    await db.refresh(sharing_group)

    yield sharing_group

    await db.delete(sharing_group)
    await db.commit()


@pytest_asyncio.fixture
async def sharing_group2(db, instance_org_two):
    sharing_group = generate_sharing_group()
    sharing_group.organisation_uuid = instance_org_two.uuid
    sharing_group.org_id = instance_org_two.id

    db.add(sharing_group)
    await db.commit()
    await db.refresh(sharing_group)

    yield sharing_group

    await db.delete(sharing_group)
    await db.commit()


@pytest_asyncio.fixture
async def server(db, instance_owner_org):
    server = generate_server()
    server.org_id = instance_owner_org.id

    db.add(server)
    await db.commit()
    yield server

    await db.delete(server)
    await db.commit()


@pytest_asyncio.fixture
async def galaxy(db):
    galaxy = generate_galaxy()

    db.add(galaxy)
    await db.commit()
    await db.refresh(galaxy)

    yield galaxy

    await db.delete(galaxy)
    await db.commit()


@pytest_asyncio.fixture()
async def auth_key(db, site_admin_user):
    clear_key = generate(string.ascii_letters + string.digits, size=40)

    auth_key = generate_auth_key()
    auth_key.user_id = site_admin_user.id
    auth_key.authkey = hash_secret(clear_key)
    auth_key.authkey_start = clear_key[:4]
    auth_key.authkey_end = clear_key[-4:]

    db.add(auth_key)

    await db.commit()
    await db.refresh(auth_key)

    yield clear_key, auth_key

    await db.delete(auth_key)
    await db.commit()


sessionmanager.init()
