import fire

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from mmisp.db.models.role import Role
from mmisp.db.models.organisation import Organisation


async def setup(session: AsyncSession):
    user = Role()
    user.name = "user"
    await add_role_if_not_exist(session, user)

    admin = Role()
    admin.name = "admin"
    admin.perm_admin = True
    await add_role_if_not_exist(session, admin)

    site_admin = Role()
    site_admin.name = "site_admin"
    site_admin.perm_admin = True
    site_admin.perm_site_admin = True
    await add_role_if_not_exist(session, site_admin)

    ghost_org = Organisation()
    ghost_org.name = "ghost_org"
    await add_organisation_if_not_exist(session, ghost_org)


async def add_role_if_not_exist(session: AsyncSession, role: Role):
    query = select(Role).where(Role.name == role.name)
    role_db = await session.execute(query)
    role_db = role_db.scalar_one_or_none()
    if role_db is None:
        session.add(role)
        await session.commit()


async def add_organisation_if_not_exist(session: AsyncSession, organisation: Organisation):
    query = select(Organisation).where(Organisation.name == organisation.name)
    organisation_db = await session.execute(query)
    organisation_db = organisation_db.scalar_one_or_none()
    if organisation_db is None:
        session.add(organisation)
        await session.commit()
