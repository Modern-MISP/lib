import fire

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from mmisp.db.models.organisation import Organisation

organisation_fields = []

async def create(session: AsyncSession, name: str | None, admin_email: str | None, description: str | None,
                 type: str | None, nationality: str | None, sector: str | None, contacts_email: str | None,
                 local: bool | None, restricted_domain: str| None, landingpage: str| None):
    organisation = Organisation()

    if await check_if_organsiastion_exists(session, name):
        raise fire.core.FireError("Organisation with name already exists")

    await set_attributes(organisation, name, admin_email, description, type, nationality, sector,
                         contacts_email, local, restricted_domain, landingpage)

    session.add(organisation)
    await session.commit()


async def check_if_organsiastion_exists(session: AsyncSession, name: str | int) -> bool:
    if isinstance(name, str):
        query = select(Organisation).where(Organisation.name == name)
    else:
        query = select(Organisation).where(Organisation.id == name)
    organisation = await session.execute(query)
    organisation = organisation.scalar_one_or_none()
    if organisation is None:
        return False
    return True


async def edit_organisation(session: AsyncSession, organisation: str | int, new_name: str | None,
                            admin_email: str | None, description: str | None, type: str | None, nationality: str | None,
                            sector: str | None, contacts_email: str | None, local: bool | None,
                            restricted_domain: str| None, landingpage: str| None):
    if isinstance(organisation, str):
        query = select(Organisation).where(Organisation.name == organisation)
    else:
        query = select(Organisation).where(Organisation.id == organisation)
    organisation = await session.execute(query)
    organisation = organisation.scalar_one_or_none()

    if organisation is None:
        raise fire.core.FireError("Organisation does not exist")

    await set_attributes(organisation, new_name, admin_email, description, type, nationality, sector,
                         contacts_email, local, restricted_domain, landingpage)

    await session.commit()


async def set_attributes(organisation: Organisation, name: str | None, admin_email: str | None, description: str | None,
                 type: str | None, nationality: str | None, sector: str | None, contacts_email: str | None,
                 local: bool | None, restricted_domain: str| None, landingpage: str| None):
    if name is not None:
        organisation.name = name
    if admin_email is not None:
        print("admin_email")
        organisation.created_by = admin_email
    if description is not None:
        print("description")
        organisation.description = description
    if type is not None:
        print("type")
        organisation.type = type
    if nationality is not None:
        print("nationality")
        organisation.nationality = nationality
    if sector is not None:
        print("sector")
        organisation.sector = sector
    if contacts_email is not None:
        print("contacts_email")
        organisation.contacts = contacts_email
    if local is not None:
        print("local")
        organisation.local = local
    if restricted_domain is not None:
        print("restricted_domain")
        organisation.restricted_to_domain = restricted_domain
    if landingpage is not None:
        print("landingpage")
        organisation.landingpage = landingpage


async def delete_organisation(session: AsyncSession, organisation: str | int):
    if isinstance(organisation, str):
        query = select(Organisation).where(Organisation.name == organisation)
    else:
        query = select(Organisation).where(Organisation.id == organisation)
    organisation = await session.execute(query)
    organisation = organisation.scalar_one_or_none()

    if organisation is None:
        raise fire.core.FireError("Organisation does not exist")

    await session.delete(organisation)
    await session.commit()
