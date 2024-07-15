import fire
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from mmisp.util.crypto import hash_secret

from mmisp.db.models.role import Role
from mmisp.db.models.user import User
from mmisp.db.models.organisation import Organisation
from mmisp.db.models.user_setting import UserSetting


async def create(session: AsyncSession, email: str, password: str, org: str | int, role: str | int):
    user = User()

    if await check_if_email_exists(session, email):
        raise fire.core.FireError("User with email already exists")
    user.email = email

    user.password = hash_secret(password)

    user.role_id = await get_element_id(session, role, "Role")

    user.org_id = await get_element_id(session, org, "Organisation")

    user.change_pw = True

    session.add(user)
    await session.commit()
    session.refresh(user)

    user_setting = UserSetting()
    user_setting.user_id = user.id
    user_setting.setting="user_name"
    user_setting.value=json.dumps({"name": str(user.email)}),
    print(user_setting.value)
    print(type(user_setting.value))
    session.add(user_setting)
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
    if element is None:
        raise fire.core.FireError(type+" not found")
    return element


async def check_if_email_exists(session: AsyncSession, email: str) -> bool:
    query = select(User).where(User.email == email)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    if user is None:
        return False
    return True


async def set_email(session: AsyncSession, email: str, new_email: str):
    if not await check_if_email_exists(session, email):
        raise fire.core.FireError("User with email does not exist")
    if await check_if_email_exists(session, new_email):
        raise fire.core.FireError("User with new email already exists")
    query = select(User).where(User.email == email)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    user.email = new_email
    await session.commit()


async def set_password(session: AsyncSession, email: str, password: str):
    if not await check_if_email_exists(session, email):
        raise fire.core.FireError("User with email does not exist")
    query = select(User).where(User.email == email)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    user.password = hash_secret(password)
    user.change_pw = True
    await session.commit()


async def set_role(session: AsyncSession, email: str, role: str | int):
    if not await check_if_email_exists(session, email):
        raise fire.core.FireError("User with email does not exist")
    query = select(User).where(User.email == email)
    user= await session.execute(query)
    user = user.scalar_one_or_none()
    user.role_id = await get_element_id(session, role, "Role")
    await session.commit()


async def delete_user(session: AsyncSession, email: str):
    if not await check_if_email_exists(session, email):
        raise fire.core.FireError("User with email does not exist")

    query = select(UserSetting).where(UserSetting.user_id == User.id)
    user_setting = await session.execute(query)
    user_setting = user_setting.scalars()
    for setting in user_setting:
        await session.delete(setting)

    query = select(User).where(User.email == email)
    user = await session.execute(query)
    user = user.scalar_one_or_none()
    await session.delete(user)
    await session.commit()
