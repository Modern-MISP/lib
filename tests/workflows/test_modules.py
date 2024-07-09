from datetime import date
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import mmisp.db.all_models  # noqa: F401
from mmisp.db.database import DatabaseSessionManager
from mmisp.db.models.event import Event, EventTag
from mmisp.db.models.organisation import Organisation
from mmisp.db.models.tag import Tag
from mmisp.workflows.graph import Apperance
from mmisp.workflows.modules import ModuleConfiguration, ModuleParam, ModuleParamType, TriggerEventAfterSave


def test_extraneous_keys() -> None:
    cfg = ModuleConfiguration(data={"foo": "bar"})

    errors = cfg.validate({})

    assert len(errors) == 1
    assert "Unspecified keys found in configuration: {'foo'}" in errors


def test_missing_key() -> None:
    cfg = ModuleConfiguration(data={})
    errors = cfg.validate({"foo": ModuleParam("foo", "Foo", ModuleParamType.INPUT, {})})

    assert len(errors) == 1
    assert "Missing configured key foo" in errors


def test_errors() -> None:
    cfg = ModuleConfiguration(data={"foo": 1, "bar": 2, "baz": 3, "fizzbuzz": True})
    errors = cfg.validate(
        {
            "foo": ModuleParam("foo", "Foo", ModuleParamType.CHECKBOX, {}),
            "bar": ModuleParam("bar", "Bar", ModuleParamType.PICKER, {"a": "b"}),
            "baz": ModuleParam("baz", "Baz", ModuleParamType.SELECT, {"a": "b"}),
            "fizzbuzz": ModuleParam("fizzbuzz", "Fizz Buzz", ModuleParamType.CHECKBOX, {}),
        }
    )

    assert len(errors) == 3

    assert "Param bar has an invalid value" in errors
    assert "Param baz has an invalid value" in errors
    assert "Param foo is expected to be a boolean" in errors


@pytest.mark.asyncio
async def test_event_normalize(event: Event, db: AsyncSession) -> None:
    trigger = TriggerEventAfterSave(
        inputs={},
        outputs={},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
    )

    result = await trigger.normalize_data(db, event)
    assert result["Event"]["id"] == 1
    assert result["Event"]["Tag"] == [
        {
            "id": 1,
            "name": "Test",
            "colour": "blue",
            "exportable": False,
        }
    ]
    assert result["Event"]["Orgc"] == {
        "id": 1,
        "uuid": "9a92b6c9-fdea-46e7-86b7-6bd475ce638a",
        "name": "Foo",
    }

    assert result["Event"]["date"] == "2024-02-13"


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
