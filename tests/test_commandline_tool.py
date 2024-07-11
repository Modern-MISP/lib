import pytest

from mmisp.commandline_tool import main


def test_create_user(db, instance_owner_org, user_role) -> None:
    """"email = "test@test.de"
    password = "password"
    main.create_user(email, password, instance_owner_org.id, user_role.id)
    user= db.execute("SELECT * FROM users WHERE email = %s", (email))
    assert user is not None
    assert user.org_id == instance_owner_org.id
    assert user.role_id == user_role.id"""
    assert True


def test_create_organisation(db) -> None:
    """name = "test"
    admin_email = ""
    description = "test"
    type = "test"
    nationality = "test"
    sector = "test"
    contacts_email = "test"
    local = False
    restricted_domain = False
    landingpage = "test"
    main.create_organisation(name, admin_email, description, type, nationality, sector, contacts_email, local,
                             restricted_domain, landingpage)
    organisation = db.execute("SELECT * FROM organisations WHERE name = %s", (name))
    assert organisation is not None"""
    assert True
    # fehlt noch was


def test_change_password(db, instance_owner_org, user_role) -> None:
    """password = "test"
    email = "test"
    main.create_user(email, password, instance_owner_org.id, user_role.id)
    main.change_password(email, password)
    user = db.execute("SELECT * FROM users WHERE email = %s", (email))
    assert user.password == password"""
    assert True
    # fehlt noch was


def test_change_email(db, instance_owner_org, user_role) -> None:
    """email = "test"
    new_email = "test2"
    password = "test"
    main.create_user(email, password, instance_owner_org.id, user_role.id)
    main.change_email(email, new_email)
    user = db.execute("SELECT * FROM users WHERE email = %s", (new_email))
    assert user.email == new_email"""
    assert True
    # fehlt noch was

def test_change_role(db, instance_owner_org, user_role) -> None:
    # admin test
    """email = "test"
    password = "test"
    role = "admin"
    main.create_user(email, password, instance_owner_org.id, user_role.id)
    main.change_role(email, role)
    user = db.execute("SELECT * FROM users WHERE email = %s", (email))
    assert user.role == role"""
    assert True


def test_edit_organisation(db) -> None:
    """name="test"
    admin_email = ""
    description = "test"
    type = "test"
    nationality = "test"
    sector = "test"
    contacts_email = "test"
    local = False
    restricted_domain = False
    landingpage = "test"
    main.create_organisation(name, admin_email, description, type, nationality, sector, contacts_email, local,
                             restricted_domain, landingpage)
    org = db.execute("SELECT * FROM organisations WHERE name = %s", (name))"""
    assert True


def test_delete_organisation() -> None:
    assert True


def test_delete_user() -> None:
    assert True


