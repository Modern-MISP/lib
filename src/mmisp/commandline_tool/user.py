import fire

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from mmisp.util.crypto import hash_secret

from mmisp.db.models.role import Role
from mmisp.db.models.user import User
from mmisp.db.models.organisation import Organisation

async def create(session: AsyncSession, email: str, password: str, org: str | int, role: str | int):
    
    user = User()

    await check_email(session, email)
    user.email = email

    user.password = hash_secret(password)

    user.role_id = await get_element_id(session, role, "Role")

    user.org_id = await get_element_id(session, org, "Organisation")

    session.add(user)
    await session.commit()


async def get_element_id(session: AsyncSession, element: int | str, type: str) -> bool:
    Class = None
    if type == "Role":
        Class = Role
    elif type == "Organisation":
        Class = Organisation
    
    if isinstance(element, str):
        query = select(Class.id).where(Class.name == element)
    else:
        query = select(Class.id).where(Class.id == element)

    element = await session.execute(query)
    element = element.scalar_one_or_none()
    test = await session.execute(select(Class))
    if element is None:
        raise fire.core.FireError(type+" not found")
    return element

# TODO fix this
async def check_email(session: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    if user is not None:
        raise fire.core.FireError("User with email already exists")
