import asyncio
import string
from typing import Generator

import pytest
from nanoid import generate
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import Session, sessionmaker

from mmisp.db.config import config
from mmisp.db.database import Base
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


@pytest.fixture(scope="session")
def connection(event_loop):
    url = make_url(config.DATABASE_URL)

    if "mysql" in url.drivername:
        url = url.set(drivername="mysql+mysqlconnector")
    if "sqlite" in url.drivername:
        url = url.set(drivername="sqlite")

    print(url)

    engine = create_engine(url, echo=True)
    #    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


@pytest.fixture(scope="function")
def db(connection) -> Generator[Session, None, None]:
    with connection() as db:
        yield db


@pytest.fixture
def site_admin_role(db):
    role = generate_site_admin_role()
    db.add(role)
    db.commit()
    yield role
    db.delete(role)
    db.commit()


@pytest.fixture
def user_role(db):
    role = generate_read_only_role()
    db.add(role)
    db.commit()
    yield role
    db.delete(role)
    db.commit()


@pytest.fixture
def org_admin_role(db):
    role = generate_org_admin_role()
    db.add(role)
    db.commit()
    yield role
    db.delete(role)
    db.commit()


@pytest.fixture
def instance_owner_org(db):
    instance_owner_org = generate_organisation()
    db.add(instance_owner_org)
    db.commit()
    yield instance_owner_org
    db.delete(instance_owner_org)
    db.commit()


@pytest.fixture
def instance_org_two(db):
    org = generate_organisation()
    db.add(org)
    db.commit()
    yield org
    db.delete(org)
    db.commit()


@pytest.fixture
def instance_two_owner_org(db):
    org = generate_organisation()
    org.local = False
    db.add(org)
    db.commit()
    yield org
    db.delete(org)
    db.commit()


@pytest.fixture
def site_admin_user(db, site_admin_role, instance_owner_org):
    user = generate_user()
    user.org_id = instance_owner_org.id
    user.server_id = 0
    user.role_id = site_admin_role.id

    db.add(user)
    db.commit()
    db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    db.commit()

    yield user
    db.delete(user_setting)
    db.commit()
    db.delete(user)
    db.commit()


@pytest.fixture
def view_only_user(db, user_role, instance_owner_org):
    user = generate_user()
    user.org_id = instance_owner_org.id
    user.server_id = 0
    user.role_id = user_role.id

    db.add(user)
    db.commit()
    db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    db.commit()

    yield user
    db.delete(user_setting)
    db.commit()
    db.delete(user)
    db.commit()


@pytest.fixture
def instance_owner_org_admin_user(db, instance_owner_org, org_admin_role):
    user = generate_user()
    user.org_id = instance_owner_org.id
    user.server_id = 0
    user.role_id = org_admin_role.id

    db.add(user)
    db.commit()
    db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    db.commit()

    yield user
    db.delete(user_setting)
    db.commit()
    db.delete(user)
    db.commit()


@pytest.fixture
def instance_two_server(db, instance_two_owner_org):
    server = generate_server()
    server.name = "Instance Two Server"
    server.org_id = instance_two_owner_org.id
    server.url = "http://instance-two.mmisp.service"

    db.add(server)
    db.commit()
    yield server
    db.delete(server)
    db.commit()


@pytest.fixture
def instance_org_two_admin_user(db, instance_org_two, org_admin_role):
    user = generate_user()
    user.org_id = instance_org_two.id
    user.server_id = 0
    user.role_id = org_admin_role.id

    db.add(user)
    db.commit()
    db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    db.commit()

    yield user
    db.delete(user_setting)
    db.commit()
    db.delete(user)
    db.commit()


@pytest.fixture
def instance_two_owner_org_admin_user(db, instance_two_owner_org, instance_two_server, org_admin_role):
    user = generate_user()
    user.org_id = instance_two_owner_org.id
    user.server_id = instance_two_server.id
    user.role_id = org_admin_role.id

    db.add(user)
    db.commit()
    db.refresh(user)

    user_setting = generate_user_name()
    user_setting.user_id = user.id

    db.add(user_setting)
    db.commit()

    yield user
    db.delete(user_setting)
    db.commit()
    db.delete(user)
    db.commit()


@pytest.fixture
def organisation(db):
    organisation = generate_organisation()

    db.add(organisation)
    db.commit()
    db.refresh(organisation)

    yield organisation

    db.delete(organisation)
    db.commit()


@pytest.fixture
def event(db, organisation, site_admin_user):
    org_id = organisation.id
    event = generate_event()
    event.org_id = org_id
    event.orgc_id = org_id
    event.user_id = site_admin_user.id

    db.add(event)
    db.commit()
    db.refresh(event)

    yield event

    db.delete(event)
    db.commit()


@pytest.fixture
def event2(db, organisation, site_admin_user):
    org_id = organisation.id
    event = generate_event()
    event.org_id = org_id
    event.orgc_id = org_id
    event.user_id = site_admin_user.id

    db.add(event)
    db.commit()
    db.refresh(event)

    yield event

    db.delete(event)
    db.commit()


@pytest.fixture
def attribute(db, event):
    event_id = event.id
    attribute = generate_attribute(event_id)
    event.attribute_count += 1

    db.add(attribute)
    db.commit()
    db.refresh(attribute)

    yield attribute

    db.delete(attribute)
    event.attribute_count -= 1
    db.commit()


@pytest.fixture
def attribute2(db, event):
    event_id = event.id
    attribute = generate_attribute(event_id)

    db.add(attribute)
    db.commit()
    db.refresh(attribute)

    yield attribute

    db.delete(attribute)
    db.commit()


@pytest.fixture
def tag(db):
    tag = generate_tag()

    tag.user_id = 1
    tag.org_id = 1
    tag.is_galaxy = True
    tag.exportable = True

    db.add(tag)
    db.commit()
    db.refresh(tag)

    yield tag

    db.delete(tag)
    db.commit()


@pytest.fixture
def sharing_group(db, instance_owner_org):
    sharing_group = generate_sharing_group()
    sharing_group.organisation_uuid = instance_owner_org.uuid
    sharing_group.org_id = instance_owner_org.id

    db.add(sharing_group)
    db.commit()
    db.refresh(sharing_group)

    yield sharing_group

    db.delete(sharing_group)
    db.commit()


@pytest.fixture
def sharing_group2(db, instance_org_two):
    sharing_group = generate_sharing_group()
    sharing_group.organisation_uuid = instance_org_two.uuid
    sharing_group.org_id = instance_org_two.id

    db.add(sharing_group)
    db.commit()
    db.refresh(sharing_group)

    yield sharing_group

    db.delete(sharing_group)
    db.commit()


@pytest.fixture
def server(db, instance_owner_org):
    server = generate_server()
    server.org_id = instance_owner_org.id

    db.add(server)
    db.commit()
    yield server

    db.delete(server)
    db.commit()


@pytest.fixture
def galaxy(db):
    galaxy = generate_galaxy()

    db.add(galaxy)
    db.commit()
    db.refresh(galaxy)

    yield galaxy

    db.delete(galaxy)
    db.commit()


@pytest.fixture()
def auth_key(db, site_admin_user):
    clear_key = generate(string.ascii_letters + string.digits, size=40)

    auth_key = generate_auth_key()
    auth_key.user_id = site_admin_user.id
    auth_key.authkey = hash_secret(clear_key)
    auth_key.authkey_start = clear_key[:4]
    auth_key.authkey_end = clear_key[-4:]

    db.add(auth_key)

    db.commit()
    db.refresh(auth_key)

    yield clear_key, auth_key

    db.delete(auth_key)
    db.commit()
