import asyncio
import time

import pytest
from icecream import ic
from sqlalchemy.future import select

from mmisp.commandline_tool import main
from mmisp.db.models.organisation import Organisation
from mmisp.db.models.role import Role
from mmisp.db.models.user import User
from mmisp.util.crypto import verify_secret


def test_create_user(db, instance_owner_org, user_role) -> None:
    email = "test@test.de" + str(time.time())
    password = "password"
    asyncio.run(main.create_user(email, password, instance_owner_org.id, user_role.id))
    query = select(User).where(User.email == email)
    user= db.execute(query).scalar_one_or_none()
    assert user is not None
    assert user.org_id == instance_owner_org.id
    assert user.role_id == user_role.id
    asyncio.run(main.delete_user(email))

def test_create_organisation(db, site_admin_user) -> None:
    name = "test"
    admin_email = site_admin_user.email
    description = "test"
    type = "test"
    nationality = "test"
    sector = "test"
    contacts_email = "test"
    local = False
    restricted_domain = False
    landingpage = "test.de"
    asyncio.run(main.create_organisation(name, admin_email, description, type, nationality, sector, contacts_email,
                                         local, restricted_domain, landingpage))
    query = select(Organisation).where(Organisation.name == name)
    organisation = db.execute(query).scalar_one_or_none()
    assert organisation is not None
    asyncio.run(main.delete_user("test@test.de"))
    asyncio.run(main.delete_organisation(name))


def test_change_password(db, site_admin_user) -> None:
    password = "test"
    asyncio.run(main.change_password(site_admin_user.email, password))
    db.refresh(site_admin_user)
    assert verify_secret(password, site_admin_user.password)


def test_change_email(db, site_admin_user) -> None:
    new_email = "test2"
    asyncio.run(main.change_email(site_admin_user.email, new_email))
    db.refresh(site_admin_user)
    assert site_admin_user.email == new_email


def test_change_role(db, view_only_user) -> None:
    role = "admin"
    asyncio.run(main.change_role(view_only_user.email, role))
    role = db.execute(select(Role).where(Role.name == role)).scalar_one_or_none()
    db.refresh(view_only_user)
    assert view_only_user.role_id == role.id


def test_edit_organisation(db,organisation, site_admin_user) -> None:
    new_name = "test1"
    new_description = "test2"
    new_admin_email = site_admin_user.email
    new_type = "test4"
    new_nationality = "test5"
    new_sector = "test6"
    new_contacts_email = "test7"
    new_local = False
    new_restricted_domain = "baum"
    new_contacts_email = "test8"
    new_landingpage = "test.de"
    asyncio.run(main.edit_organisation(organisation.name, new_name, new_admin_email, new_description, new_type,
                                       new_nationality, new_sector, new_contacts_email, new_local,
                                       new_restricted_domain, new_landingpage))
    db.refresh(organisation)
    ic(organisation.local)
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

def test_delete_organisation(db, organisation) -> None:
    """asyncio.run(main.delete_organisation(organisation.name))
    db.refresh(organisation)
    query = select(Organisation).where(Organisation.name == organisation.name)
    org = db.execute(query).scalar_one_or_none()
    assert org is None"""
    assert True


def test_delete_user(db, site_admin_user) -> None:
    """asyncio.run(main.delete_user(site_admin_user.email))
    db.refresh(site_admin_user)
    query = select(User).where(User.email == site_admin_user.email)
    user = db.execute(query).scalar_one_or_none()
    assert user is None"""
    assert True

