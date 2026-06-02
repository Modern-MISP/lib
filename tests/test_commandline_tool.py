import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import delete, select

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
    user = (await db.execute(query)).scalar_one_or_none()
    assert user is not None
    assert user.org_id == instance_owner_org.id
    assert user.role_id == user_role.id

    try:
        await main.create_user(email, password, instance_owner_org.id, user_role.id)
    except Exception as e:
        error = str(e)
        assert error == "User with email already exists"

    try:
        await main.create_user(email + "1", password, instance_owner_org.id + 1, user_role.id)
    except Exception as e:
        error = str(e)
        assert error == "Organisation not found"

    try:
        await main.create_user(email + "2", password, instance_owner_org.id, user_role.id + 1)
    except Exception as e:
        error = str(e)
        assert error == "Role not found"

    await db.execute(delete(UserSetting).where(UserSetting.user_id == user.id))
    await db.execute(delete(User).where(User.id == user.id))


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
    restricted_domain: list[str] = []
    landingpage = time_now
    await main.create_organisation(
        name, admin_email, description, type, nationality, sector, contacts_email, local, restricted_domain, landingpage
    )

    try:
        await main.create_organisation(
            name,
            admin_email,
            description,
            type,
            nationality,
            sector,
            contacts_email,
            local,
            restricted_domain,
            landingpage,
        )
    except Exception as e:
        error = str(e)
        assert error == "Organisation with name already exists"

    query = select(Organisation).where(Organisation.name == name)
    organisation = (await db.execute(query)).scalar_one_or_none()
    assert organisation is not None
    await db.execute(delete(Organisation).where(Organisation.name == name))


@pytest.mark.asyncio
async def test_change_password(db, site_admin_user) -> None:
    password = "test" + str(time.time())

    try:
        await main.change_password(site_admin_user.email + "1", password)
    except Exception as e:
        error = str(e)
        assert error == "User with email does not exist"

    await main.change_password(site_admin_user.email, password)
    await db.refresh(site_admin_user)
    assert verify_secret(password, site_admin_user.password)


@pytest.mark.asyncio
async def test_change_email(db, site_admin_user) -> None:
    new_email = str(time.time())

    try:
        await main.change_email(new_email, site_admin_user.email)
    except Exception as e:
        error = str(e)
        assert error == "User with email does not exist"

    try:
        await main.change_email(site_admin_user.email, site_admin_user.email)
    except Exception as e:
        error = str(e)
        assert error == "User with new email already exists"

    await main.change_email(site_admin_user.email, new_email)
    await db.refresh(site_admin_user)
    assert site_admin_user.email == new_email


@pytest.mark.asyncio
async def test_change_role(db, view_only_user, site_admin_role) -> None:
    try:
        await main.change_role(view_only_user.email + "1", site_admin_role.id)
    except Exception as e:
        error = str(e)
        assert error == "User with email does not exist"

    try:
        await main.change_role(view_only_user.email, site_admin_role.id + 1)
    except Exception as e:
        error = str(e)
        assert error == "Role not found"

    try:
        await main.change_role(view_only_user.email, view_only_user.role_id)
    except Exception as e:
        error = str(e)
        assert error == "User already has this role"

    await main.change_role(view_only_user.email, site_admin_role.id)
    role = (await db.execute(select(Role).where(Role.id == site_admin_role.id))).scalar_one_or_none()
    await db.refresh(view_only_user)
    assert view_only_user.role_id == role.id


@pytest.mark.asyncio
async def test_edit_organisation(db, organisation, site_admin_user) -> None:
    time_now = str(time.time())
    new_name = time_now
    new_admin_email = site_admin_user.email
    new_description = time_now
    new_type = time_now
    new_nationality = time_now
    new_sector = time_now
    new_contacts_email = time_now
    new_local = False
    new_restricted_domain: list[str] = []
    new_landingpage = time_now
    await main.edit_organisation(
        organisation.name,
        new_name,
        new_admin_email,
        new_description,
        new_type,
        new_nationality,
        new_sector,
        new_contacts_email,
        new_local,
        new_restricted_domain,
        new_landingpage,
    )
    await db.refresh(organisation)
    assert organisation.name == new_name
    assert organisation.created_by == site_admin_user.id
    assert organisation.description == new_description
    assert organisation.type == new_type
    assert organisation.nationality == new_nationality
    assert organisation.sector == new_sector
    assert organisation.contacts == new_contacts_email
    assert bool(organisation.local) is new_local
    assert organisation.restricted_to_domain == new_restricted_domain
    assert organisation.landingpage == new_landingpage

    try:
        await main.edit_organisation(
            organisation.name + "1",
            new_name,
            new_admin_email,
            new_description,
            new_type,
            new_nationality,
            new_sector,
            new_contacts_email,
            new_local,
            new_restricted_domain,
            new_landingpage,
        )
    except Exception as e:
        error = str(e)
        assert error == "Organisation does not exist"


@pytest.mark.asyncio
async def test_delete_organisation(db, organisation) -> None:
    await main.delete_organisation(organisation.name)
    await db.invalidate()
    query = select(Organisation).where(Organisation.name == organisation.name)
    org = (await db.execute(query)).scalar_one_or_none()
    assert org is None

    try:
        await main.delete_organisation(organisation.name + "1")
    except Exception as e:
        error = str(e)
        assert error == "Organisation does not exist"


@pytest.mark.asyncio
async def test_delete_user(db, site_admin_user) -> None:
    await main.delete_user(site_admin_user.email)
    query = select(User).where(User.email == site_admin_user.email)
    user = (await db.execute(query)).scalar_one_or_none()
    assert user is None

    try:
        await main.delete_user(site_admin_user.email + "1")
    except Exception as e:
        error = str(e)
        assert error == "User with email does not exist"


@pytest.mark.asyncio
async def test_setup(db) -> None:
    await main.setup_db()
    query_user = select(Role).where(Role.name == "user")
    user_role = (await db.execute(query_user)).scalar_one_or_none()
    assert user_role is not None
    query_admin = select(Role).where(Role.name == "admin")
    admin_role = (await db.execute(query_admin)).scalar_one_or_none()
    assert admin_role is not None
    query_site_admin = select(Role).where(Role.name == "site_admin")
    site_admin_role = (await db.execute(query_site_admin)).scalar_one_or_none()
    assert site_admin_role is not None
    query_admin = select(Role).where(Role.name == "publisher")
    publisher_role = (await db.execute(query_admin)).scalar_one_or_none()
    assert publisher_role is not None
    query_admin = select(Role).where(Role.name == "sync_user")
    sync_user_role = (await db.execute(query_admin)).scalar_one_or_none()
    assert sync_user_role is not None
    query_admin = select(Role).where(Role.name == "read_only")
    read_only_role = (await db.execute(query_admin)).scalar_one_or_none()
    assert read_only_role is not None
    query_org = select(Organisation).where(Organisation.name == "ghost_org")
    org = (await db.execute(query_org)).scalar_one_or_none()
    assert org is not None

    await db.delete(org)
    await db.delete(site_admin_role)
    await db.delete(admin_role)
    await db.delete(user_role)
    await db.delete(publisher_role)
    await db.delete(sync_user_role)
    await db.delete(read_only_role)
    await db.commit()


def test_db_revision_already_up_to_date(capsys):
    """When DB heads match expected heads, prints up-to-date message and skips upgrade."""
    head_rev = "abc123"

    mock_script = MagicMock()
    mock_script.get_heads.return_value = [head_rev]

    mock_conn = AsyncMock()
    mock_conn.run_sync = AsyncMock(return_value={head_rev})

    mock_engine = MagicMock()
    mock_engine.connect.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_engine.connect.return_value.__aexit__ = AsyncMock(return_value=False)
    mock_engine.dispose = AsyncMock()

    with (
        patch("mmisp.commandline_tool.main._get_alembic_config"),
        patch("mmisp.commandline_tool.main.ScriptDirectory") as mock_sd_cls,
        patch("mmisp.commandline_tool.main.create_async_engine", return_value=mock_engine),
        patch("mmisp.commandline_tool.main.command") as mock_command,
    ):
        mock_sd_cls.from_config.return_value = mock_script

        main.db_revision()

        mock_command.upgrade.assert_not_called()
        captured = capsys.readouterr()
        assert "already up to date" in captured.out


def test_db_revision_runs_upgrade_when_behind(capsys):
    """When DB heads differ from expected heads, runs upgrade and prints updated message."""
    expected_rev = "abc123"
    current_rev = "old999"

    mock_script = MagicMock()
    mock_script.get_heads.return_value = [expected_rev]

    mock_conn = AsyncMock()
    mock_conn.run_sync = AsyncMock(return_value={current_rev})

    mock_engine = MagicMock()
    mock_engine.connect.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_engine.connect.return_value.__aexit__ = AsyncMock(return_value=False)
    mock_engine.dispose = AsyncMock()

    with (
        patch("mmisp.commandline_tool.main._get_alembic_config"),
        patch("mmisp.commandline_tool.main.ScriptDirectory") as mock_sd_cls,
        patch("mmisp.commandline_tool.main.create_async_engine", return_value=mock_engine),
        patch("mmisp.commandline_tool.main.command") as mock_command,
    ):
        mock_sd_cls.from_config.return_value = mock_script

        main.db_revision()

        mock_command.upgrade.assert_called_once()
        captured = capsys.readouterr()
        assert "updated to the latest version" in captured.out
