from datetime import date
from typing import AsyncGenerator
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from mmisp.db.models.event import Event
from mmisp.workflows.graph import Apperance, Node
from mmisp.workflows.input import Filter, Operator, WorkflowInput
from mmisp.workflows.modules import (
    ModuleConfiguration,
    ModuleGenericFilterData,
    ModuleGenericFilterReset,
    ModuleIfGeneric,
    ModuleParam,
    ModuleParamType,
    ModulePublishEvent,
    ModuleTagIf,
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
async def test_if_generic() -> None:
    module = ModuleIfGeneric(
        inputs={}, outputs={}, graph_id=1, apperance=None, configuration=ModuleConfiguration({}), on_demand_filter=None
    )
    module_yes = Node(inputs={}, outputs={}, graph_id=1)
    module_no = Node(inputs={}, outputs={}, graph_id=1)
    module.outputs[1] = [(1, module_yes)]
    module.outputs[2] = [(1, module_no)]
    module.configuration.data["value"] = "V12"
    module.configuration.data["operator"] = "in"
    module.configuration.data["hash_path"] = "storages.{n}.vehicle.car.engine"
    input_data = {
        "storages": [
            {"vehicle": {"car": {"engine": "V12", "tires": "4"}, "motorcycle": {"engine": "V4", "tires": "3"}}},
            {"vehicle": {"yacht": {"engine": "V24", "max_speed": "80 knots"}}},
            {"vehicle": {"car": {"engine": "V8", "max_speed": "280km/h"}}},
        ]
    }
    next_node = await module.exec(WorkflowInput(data=input_data, user=None, workflow=None), None)
    assert next_node[0]
    assert next_node[1] == module_yes
    module.configuration.data["value"] = "V10"
    next_node = await module.exec(WorkflowInput(data=input_data, user=None, workflow=None), None)
    assert next_node[0]
    assert next_node[1] == module_no


@pytest.mark.asyncio
async def test_if_tag() -> None:
    module = ModuleTagIf(
        inputs={}, outputs={}, graph_id=1, apperance=None, configuration=ModuleConfiguration({}), on_demand_filter=None
    )
    module_yes = Node(inputs={}, outputs={}, graph_id=1)
    module_no = Node(inputs={}, outputs={}, graph_id=1)
    module.outputs[1] = [(1, module_yes)]
    module.outputs[2] = [(1, module_no)]
    module.configuration.data["scope"] = "event"
    module.configuration.data["condition"] = "in_and"
    module.configuration.data["tags"] = ["white", "green", "red"]
    input_data = {
        "Event": {"Tag": [{"name": "blue"}, {"name": "white"}, {"name": "purple"}, {"name": "green"}, {"name": "red"}]}
    }
    next_node = await module.exec(WorkflowInput(data=input_data, user=None, workflow=None), None)
    assert next_node[1] == module_yes


@pytest.mark.asyncio
async def test_event_normalize(event: Event, db: AsyncSession) -> None:
    trigger = TriggerEventAfterSave(
        inputs={},
        outputs={},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
    )

    result = await trigger.normalize_data(db, event)
    assert result["Event"]["id"] == "1"
    assert result["Event"]["Tag"] == [
        {
            "id": 1,
            "name": "Test",
            "colour": "blue",
            "exportable": False,
        }
    ]
    assert result["Event"]["Orgc"] == {
        "id": "1",
        "uuid": "9a92b6c9-fdea-46e7-86b7-6bd475ce638a",
        "name": "Foo",
        "local": False,
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


@pytest.mark.asyncio()
async def test_publish_event() -> None:
    instance = ModulePublishEvent(
        inputs={},
        outputs={1: []},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
        on_demand_filter=None,
        configuration=ModuleConfiguration(data={}),
    )

    await instance.initialize_for_visual_editor(Mock())

    assert instance.check().errors == []

    input = WorkflowInput({"Event": {"id": 1, "Tag": [{"name": "BTS tag"}, {"name": "Nord"}]}}, Mock(), Mock())

    mock_db = AsyncMock()
    mock_db.get.return_value = Event()

    await instance.exec(input, mock_db)

    mock_db.get.assert_called_once_with(Event, "1")
    assert mock_db.commit.call_count == 1
    assert mock_db.refresh.call_count == 1


@pytest.mark.asyncio()
async def test_publish_with_db(db: AsyncSession, event: AsyncGenerator) -> None:
    instance = ModulePublishEvent(
        inputs={},
        outputs={1: []},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
        on_demand_filter=None,
        configuration=ModuleConfiguration(data={}),
    )

    await instance.initialize_for_visual_editor(db)

    assert instance.check().errors == []

    input = WorkflowInput({"Event": {"id": 1, "Tag": [{"name": "BTS tag"}, {"name": "Nord"}]}}, Mock(), Mock())
    event = await db.get(Event, "1")

    assert not getattr(event, "published")
    assert getattr(event, "publish_timestamp") == 0

    result = await instance.exec(input, db)

    assert result == (True, None)

    event = await db.get(Event, "1")

    assert getattr(event, "published")
    assert getattr(event, "publish_timestamp") > 0


@pytest.mark.asyncio()
async def test_publish_not_existing_event(db: AsyncSession, event: AsyncGenerator) -> None:
    instance = ModulePublishEvent(
        inputs={},
        outputs={1: []},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
        on_demand_filter=None,
        configuration=ModuleConfiguration(data={}),
    )

    await instance.initialize_for_visual_editor(db)

    assert instance.check().errors == []

    input = WorkflowInput({"Event": {"id": 55, "Tag": [{"name": "BTS tag"}, {"name": "Nord"}]}}, Mock(), Mock())
    event = await db.get(Event, "55")

    assert event is None

    result = await instance.exec(input, db)

    assert result == (False, None)


@pytest.mark.asyncio()
async def test_publish_already_published_event(db: AsyncSession, event: AsyncGenerator) -> None:
    instance = ModulePublishEvent(
        inputs={},
        outputs={1: []},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
        on_demand_filter=None,
        configuration=ModuleConfiguration(data={}),
    )

    event = Event(
        id=3,
        org_id=1,
        orgc_id=1,
        user_id=1,
        published=True,
        publish_timestamp=17,
        sharing_group_id=1,
        threat_level_id=1,
        info="test event",
        date=date(year=2024, month=2, day=13),
        analysis=1,
    )
    db.add(event)
    await db.commit()

    await instance.initialize_for_visual_editor(db)

    assert instance.check().errors == []

    input = WorkflowInput({"Event": {"id": 3, "Tag": [{"name": "BTS tag"}, {"name": "Nord"}]}}, Mock(), Mock())
    event = await db.get(Event, "3")

    assert getattr(event, "published")
    assert getattr(event, "publish_timestamp") == 17

    result = await instance.exec(input, db)

    assert result == (True, None)

    event = await db.get(Event, "3")

    assert getattr(event, "published")
    assert getattr(event, "publish_timestamp") > 3

    await db.delete(event)
    await db.commit()


@pytest.mark.asyncio()
async def test_publish_event_output_node(db: AsyncSession, event: AsyncGenerator) -> None:
    outputNode = ModuleGenericFilterData(
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

    instance = ModulePublishEvent(
        inputs={},
        outputs={1: [(1, outputNode)]},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
        on_demand_filter=None,
        configuration=ModuleConfiguration(data={}),
    )

    await instance.initialize_for_visual_editor(db)

    assert instance.check().errors == []

    input = WorkflowInput({"Event": {"id": 1, "Tag": [{"name": "BTS tag"}, {"name": "Nord"}]}}, Mock(), Mock())
    event = await db.get(Event, "1")

    assert not getattr(event, "published")
    assert getattr(event, "publish_timestamp") == 0

    result = await instance.exec(input, db)

    assert result[0]
    assert result[1] is outputNode

    event = await db.get(Event, "1")

    assert getattr(event, "published")
    assert getattr(event, "publish_timestamp") > 0
