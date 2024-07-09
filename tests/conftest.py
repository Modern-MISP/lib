from datetime import date
from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import mmisp.db.all_models  # noqa: F401
from mmisp.db.database import DatabaseSessionManager
from mmisp.db.models.event import Event, EventTag
from mmisp.db.models.organisation import Organisation
from mmisp.db.models.tag import Tag


@pytest_asyncio.fixture
async def event(db: AsyncSession) -> AsyncGenerator[Event, None]:
    orgc = Organisation(
        id=1,
        name="Foo",
        uuid="9a92b6c9-fdea-46e7-86b7-6bd475ce638a",
        description="Blah",
        type="broke",
        nationality="german",
        sector="foo",
        contacts="",
        landingpage="",
    )
    db.add(orgc)
    tag = Tag(
        id=1,
        name="Test",
        colour="blue",
        exportable=False,
        org_id=1,
        user_id=1,
        hide_tag=False,
        numerical_value=1,
        is_galaxy=True,
        is_custom_galaxy=False,
        local_only=False,
    )
    db.add(tag)
    event = Event(
        id=1,
        org_id=1,
        orgc_id=1,
        user_id=1,
        sharing_group_id=1,
        threat_level_id=1,
        info="test event",
        date=date(year=2024, month=2, day=13),
        analysis=1,
    )
    db.add(event)
    eventtag = EventTag(id=1, event_id=1, tag_id=1)
    db.add(eventtag)
    yield event
    await db.delete(eventtag)
    await db.delete(event)
    await db.delete(tag)
    await db.delete(orgc)
    await db.commit()


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator[AsyncSession, None]:
    manager = DatabaseSessionManager("sqlite+aiosqlite:///mmisp-tests.db?check_same_thread=False")
    manager.init()
    await manager.create_all()
    async with manager.session() as session:
        yield session
    await manager.drop_all()
