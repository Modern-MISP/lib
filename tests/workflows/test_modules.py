import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from mmisp.db.models.event import Event
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
