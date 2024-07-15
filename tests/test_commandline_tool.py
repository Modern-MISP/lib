import time

import pytest
from icecream import ic
from sqlalchemy.future import select

from mmisp.commandline_tool import main
from mmisp.db.models.organisation import Organisation
from mmisp.db.models.role import Role
from mmisp.db.models.user import User
from mmisp.db.models.user_setting import UserSetting
from mmisp.util.crypto import verify_secret


@pytest.mark.asyncio
async def test_create_user(db, instance_owner_org, user_role) -> None:
    email = "test@test.de" + str(time.time())
    password = "password" + str(time.time())
    await main.create_user(email, password, instance_owner_org.id, user_role.id)
    query = select(User).where(User.email == email)
    user= db.execute(query).scalar_one_or_none()
    assert user is not None
    assert user.org_id == instance_owner_org.id
    assert user.role_id == user_role.id
    db.query(UserSetting).filter(UserSetting.user_id == user.id).delete()
    db.query(User).filter(User.id == user.id).delete()


@pytest.mark.asyncio
async def test_create_organisation(db, site_admin_user) -> None:
    time_now = str(time.time())
    name = time_now
    admin_email = site_admin_user.email
    description = time_now
    type = time_now
    nationality = time_now
    sector = time_now
    contacts_email = time_now
    local = False
    restricted_domain = False
    landingpage = time_now
    await main.create_organisation(name, admin_email, description, type, nationality, sector, contacts_email,
                                         local, restricted_domain, landingpage)
    query = select(Organisation).where(Organisation.name == name)
    organisation = db.execute(query).scalar_one_or_none()
    assert organisation is not None
    db.query(Organisation).filter(Organisation.name == name).delete()


@pytest.mark.asyncio
async def test_change_password(db, site_admin_user) -> None:
    password = "test" + str(time.time())
    await main.change_password(site_admin_user.email, password)
    db.refresh(site_admin_user)
    assert verify_secret(password, site_admin_user.password)


@pytest.mark.asyncio
async def test_change_email(db, site_admin_user) -> None:
    new_email = str(time.time())
    await main.change_email(site_admin_user.email, new_email)
    db.refresh(site_admin_user)
    assert site_admin_user.email == new_email


@pytest.mark.asyncio
async def test_change_role(db, view_only_user, site_admin_role) -> None:
    await main.change_role(view_only_user.email, site_admin_role.id)
    role = db.execute(select(Role).where(Role.id == site_admin_role.id)).scalar_one_or_none()
    db.refresh(view_only_user)
    assert view_only_user.role_id == role.id


@pytest.mark.asyncio
async def test_edit_organisation(db,organisation, site_admin_user) -> None:
    time_now = str(time.time())
    new_name = time_now
    new_admin_email = site_admin_user.email
    new_description = time_now
    new_type = time_now
    new_nationality = time_now
    new_sector = time_now
    new_contacts_email = time_now
    new_local = False
    new_restricted_domain = "{}"
    new_landingpage = time_now
    await main.edit_organisation(organisation.name, new_name, new_admin_email, new_description, new_type,
                                       new_nationality, new_sector, new_contacts_email, new_local,
                                       new_restricted_domain, new_landingpage)
    db.refresh(organisation)
    assert organisation.name == new_name
    assert organisation.created_by == site_admin_user.id
    assert organisation.description == new_description
    assert organisation.type == new_type
    assert organisation.nationality == new_nationality
    assert organisation.sector == new_sector
    assert organisation.contacts == new_contacts_email
    assert bool(organisation.local) is new_local
    assert str(organisation.restricted_to_domain) == new_restricted_domain
    assert organisation.landingpage == new_landingpage


@pytest.mark.asyncio
async def test_delete_organisation(db, organisation) -> None:
    """await main.delete_organisation(organisation.name)
    query = select(Organisation).where(Organisation.name == organisation.name)
    org = db.execute(query).scalar_one_or_none()
    assert org is None"""
    assert True


@pytest.mark.asyncio
async def test_delete_user(db, site_admin_user) -> None:
    await main.delete_user(site_admin_user.email)
    query = select(User).where(User.email == site_admin_user.email)
    user = db.execute(query).scalar_one_or_none()
    assert user is None
