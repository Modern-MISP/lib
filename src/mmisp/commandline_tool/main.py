import asyncio

import fire
from alembic import command
from alembic.config import Config as AlembicConfig
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

import mmisp.db.all_models  # noqa
from mmisp.commandline_tool import organisation, setup, user
from mmisp.db.config import config
from mmisp.db.database import Base, _build_alembic_config, sessionmanager

# This allows 'db_migrate' to detect changes automatically by linking the metadata
target_metadata = Base.metadata

# This is a simple command line tool that uses the fire library to create a command line tool for creating users
# and organisations and changing their details.


def _get_alembic_config() -> AlembicConfig:
    """Auxiliary function to get the Alembic config."""
    return _build_alembic_config()


def db_migrate(message: str) -> None:
    """Creates a new migration script by detecting changes in the models."""
    cfg = _get_alembic_config()
    command.revision(cfg, message=message, autogenerate=True)
    print(f"Migration '{message}' created successfully.")


def db_stamp() -> None:
    """Stamps the db with the current revision but not actually running the migrations."""
    cfg = _get_alembic_config()
    command.stamp(cfg, "heads")
    print("DB stamped successfully.")


def db_upgrade() -> None:
    """Applies all pending migrations to the database."""
    cfg = _get_alembic_config()
    command.upgrade(cfg, "head")
    print("Database updated to the latest version.")


def db_current() -> None:
    """Displays the current revision/version of the database."""
    cfg = _get_alembic_config()
    command.current(cfg)


def db_revision() -> None:
    """Applies pending migrations only if the database is not up to date."""
    cfg = _get_alembic_config()
    script = ScriptDirectory.from_config(cfg)
    expected_heads = set(script.get_heads())

    async def _get_current_heads_async() -> set[str]:
        engine = create_async_engine(config.DATABASE_URL, poolclass=NullPool)
        try:
            async with engine.connect() as conn:

                def _read_heads(connection: object) -> set[str]:
                    ctx = MigrationContext.configure(connection)  # type: ignore[arg-type]
                    return set(ctx.get_current_heads())

                return await conn.run_sync(_read_heads)
        finally:
            await engine.dispose()

    current_heads = asyncio.run(_get_current_heads_async())

    if current_heads == expected_heads:
        print("Database is already up to date.")
        return

    command.upgrade(cfg, "head")
    print("Database updated to the latest version.")


async def setup_db(create_init_values: bool = True) -> str:
    """Initializes the database schema and optionally populates initial values."""
    assert sessionmanager is not None
    # sessionmanager.init()
    # await sessionmanager.create_all()

    if create_init_values:
        async with sessionmanager.session() as session:
            await setup.setup(session)

    await sessionmanager.close()
    return "Database setup completed"


async def create_user(email: str, password: str, organisation: str | int, role: int | str = "user") -> str:
    """Creates a new user: create-user <email> <password> <organisation> [-r <role>]"""
    assert sessionmanager is not None
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.create(session, email, password, organisation, role)

    await sessionmanager.close()
    return "User created with email: {}, password: {}, in organisation: {}, with role: {}".format(
        email, password, organisation, role
    )


async def create_organisation(
    name: str,
    admin_email: int | str | None = None,
    description: str | None = None,
    type: str | None = None,
    nationality: str | None = None,
    sector: str | None = None,
    contacts_email: str | None = None,
    local: bool | None = None,
    restricted_domain: list[str] | None = None,
    landingpage: str | None = None,
) -> str:
    """Creates a new organisation: create-organisation <name> [options]"""
    assert sessionmanager is not None
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await organisation.create(
            session,
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

    await sessionmanager.close()

    output = "Organisation created with name: {} admin_email: {} description: {}"
    return output.format(name, admin_email, description)


async def change_password(email: str, password: str) -> str:
    """Changes the password for a specific user: change-password <email> <password>"""
    assert sessionmanager is not None
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.set_password(session, email, password)

    await sessionmanager.close()
    return "Password changed for user with email: {}".format(email)


async def change_email(email: str, new_email: str) -> str:
    """Updates a user's email: change-email <email> <new_email>"""
    assert sessionmanager is not None
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.set_email(session, email, new_email)

    await sessionmanager.close()
    return "Email changed for user with email: {} to {}".format(email, new_email)


async def change_role(email: str, role: str | int) -> str:
    """Updates a user's role: change-role <email> <role>"""
    assert sessionmanager is not None
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.set_role(session, email, role)

    await sessionmanager.close()
    return "Role changed for user with email: {} to {}".format(email, role)


async def edit_organisation(
    org: str | int,
    new_name: str | None = None,
    admin_email: int | str | None = None,
    description: str | None = None,
    type: str | None = None,
    nationality: str | None = None,
    sector: str | None = None,
    contacts_email: str | None = None,
    local: bool | None = None,
    restricted_domain: list[str] | None = None,
    landingpage: str | None = None,
) -> str:
    """Edits an existing organisation's details: edit-organisation <organisation> [options]"""
    assert sessionmanager is not None
    output = "organisation {} edited"
    sessionmanager.init()
    await sessionmanager.create_all()

    async with sessionmanager.session() as session:
        await organisation.edit_organisation(
            session,
            org,
            new_name,
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

    await sessionmanager.close()
    return output.format(org)


async def delete_organisation(org: str | int) -> str:
    """Removes an organisation from the database: delete-organisation <name>"""
    assert sessionmanager is not None
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await organisation.delete_organisation(session, org)

    await sessionmanager.close()
    return "organisation deleted with name: {}".format(org)


async def delete_user(email: str) -> str:
    """Removes a user from the database: delete-user <email>"""
    assert sessionmanager is not None
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.delete_user(session, email)

    await sessionmanager.close()
    return "User deleted with email: {} ".format(email)


def main() -> None:
    """Main entrypoint for mmisp-db CLI tool."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return fire.Fire(
        {
            # Database Migration Commands
            "db-migrate": db_migrate,
            "db-upgrade": db_upgrade,
            "db-current": db_current,
            "db-revision": db_revision,
            "db-stamp": db_stamp,
            # Management Commands
            "setup": setup_db,
            "create-user": create_user,
            "create-organisation": create_organisation,
            "change-password": change_password,
            "change-email": change_email,
            "change-role": change_role,
            "edit-organisation": edit_organisation,
            "delete-organisation": delete_organisation,
            "delete-user": delete_user,
        }
    )


if __name__ == "__main__":
    main()
