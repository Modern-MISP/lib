from unittest.mock import Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from mmisp.db.models.event import Event
from mmisp.workflows.graph import Apperance
from mmisp.workflows.input import Filter, Operator, WorkflowInput
from mmisp.workflows.modules import (
    ModuleConfiguration,
    ModuleGenericFilterData,
    ModuleGenericFilterReset,
    ModuleParam,
    ModuleParamType,
    TriggerEventAfterSave,
)


def test_extraneous_keys() -> None:
    cfg = ModuleConfiguration(data={"foo": "bar"})

    errors = cfg.validate({})

    assert len(errors) == 1
    assert "Unspecified keys found in configuration: {'foo'}" in errors


def test_errors() -> None:
    cfg = ModuleConfiguration(data={"foo": 1, "bar": 2, "baz": 3, "fizzbuzz": True})
    errors = cfg.validate(
        {
            "foo": ModuleParam("foo", "Foo", ModuleParamType.CHECKBOX, {}),
            "bar": ModuleParam("bar", "Bar", ModuleParamType.PICKER, {}),
            "baz": ModuleParam("baz", "Baz", ModuleParamType.SELECT, {"options": {"a": "b"}}),
            "fizzbuzz": ModuleParam("fizzbuzz", "Fizz Buzz", ModuleParamType.CHECKBOX, {}),
        }
    )

    assert len(errors) == 2

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


@pytest.mark.asyncio()
async def test_add_filter() -> None:
    instance = ModuleGenericFilterData(
        inputs={},
        outputs={1: []},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
        on_demand_filter=None,
        configuration=ModuleConfiguration(
            data={
                "filtering-label": "A",
                "selector": "Event.{n}.Tag.{n}",
                "value": "BTS tag",
                "hash_path": "name",
                "operator": Operator.EQUALS.value,
            }
        ),
        params={},
    )

    await instance.initialize_for_visual_editor(Mock())

    assert instance.check().errors == []

    input = WorkflowInput({"Event": [{"Tag": [{"name": "BTS tag"}, {"name": "Fnord"}]}]}, Mock(), Mock())

    await instance.exec(input, Mock())

    assert len(input.data["Event"][0]["Tag"]) == 1


@pytest.mark.asyncio()
async def test_rm_all_filters() -> None:
    instance = ModuleGenericFilterReset(
        inputs={},
        outputs={1: []},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
        on_demand_filter=None,
        configuration=ModuleConfiguration(data={"filtering-label": "all"}),
        params={},
    )

    await instance.initialize_for_visual_editor(Mock())

    assert instance.check().errors == []

    input = WorkflowInput({"Event": [{"Tag": [{"name": "BTS tag"}, {"name": "Fnord"}]}]}, Mock(), Mock())
    input.add_filter("A", Filter("Event.{n}.Tag.{n}", "name", Operator.EQUALS, "BTS tag"))
    assert len(input.data["Event"][0]["Tag"]) == 1
    input.add_filter("B", Filter("Event.{n}.Tag.{n}", "name", Operator.NOT_EQUALS, "BTS tag"))

    assert len(input.data["Event"][0]["Tag"]) == 0

    await instance.exec(input, Mock())

    assert len(input.data["Event"][0]["Tag"]) == 2
