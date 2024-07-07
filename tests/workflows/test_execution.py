import uuid
from dataclasses import dataclass
from typing import Dict, List, Self, Tuple
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from mmisp.db.models.workflow import Workflow
from mmisp.lib.logging import ApplicationLogger
from mmisp.workflows.execution import execute_workflow
from mmisp.workflows.graph import Apperance, Module, Trigger, WorkflowGraph
from mmisp.workflows.input import WorkflowInput
from mmisp.workflows.modules import ModuleAction, Overhead


@pytest.mark.asyncio
async def test_trigger_disabled(trigger: Trigger, empty_wf: Workflow) -> None:
    trigger.disabled = True

    db = AsyncMock()
    user = Mock()
    logger = ApplicationLogger(db)
    assert (await execute_workflow(empty_wf, user, {}, db, logger))[0]


@pytest.mark.asyncio
async def test_nothing_to_do(empty_wf: Workflow) -> None:
    db = AsyncMock()
    user = Mock()
    logger = Mock()
    assert (await execute_workflow(empty_wf, user, {}, db, logger))[0]

    # we went a little further and thus a first log message should've been received.
    assert logger.log_workflow_debug_message.called == 1
    logger.log_workflow_debug_message.assert_called_with(empty_wf, "Started executing workflow for trigger `demo` (23)")


@pytest.mark.asyncio
async def test_normalization_error(wf: Workflow) -> None:
    db = AsyncMock()
    user = Mock()
    logger = Mock()

    assert not (await execute_workflow(wf, user, Mock(), db, logger))[0]
    assert logger.log_workflow_execution_error.called == 1
    logger.log_workflow_execution_error.assert_called_with(
        wf,
        (
            "Error while normalizing data for trigger. Error: \nNo dict was passed "
            + "to default normalize_data implementation of a trigger. Override your trigger "
            + "if other inputs shall be accepted. Got: <class 'unittest.mock.Mock'>"
        ),
    )


@pytest.mark.asyncio
async def test_execute(wf: Workflow) -> None:
    db = AsyncMock()
    user = Mock()
    logger = Mock()

    result = await execute_workflow(wf, user, {}, db, logger)
    assert result[0]
    assert logger.log_workflow_debug_message.call_count == 4
    assert not logger.log_workflow_execution_error.called

    logger.log_workflow_debug_message.assert_called_with(
        wf, ("Finished executing workflow for trigger `demo` (24). Outcome: success")
    )
    logger.log_workflow_debug_message.assert_any_call(
        wf,
        (
            "Executed node `demo`\nNode `demo` from Workflow `Demo workflow` (24) "
            "executed successfully with status: success"
        ),
    )


@pytest.mark.asyncio
async def test_execute_error(wf_fail: Workflow) -> None:
    db = AsyncMock()
    user = Mock()
    logger = Mock()

    result = await execute_workflow(wf_fail, user, {}, db, logger)
    assert not result[0]
    assert "Hello World" in result[1]
    assert logger.log_workflow_debug_message.call_count == 3
    assert not logger.log_workflow_execution_error.called

    logger.log_workflow_debug_message.assert_any_call(
        wf_fail,
        (
            "Executed node `demo`\nNode `demo` from Workflow `Demo workflow` (25) "
            "executed successfully with status: partial-success"
        ),
    )

    logger.log_workflow_debug_message.assert_called_with(
        wf_fail, ("Finished executing workflow for trigger `demo` (25). Outcome: failure")
    )


@pytest.fixture
def wf_fail(trigger: Trigger) -> Workflow:
    @dataclass
    class MockupModule(ModuleAction):
        id: str = "demo"
        name: str = "Demo :: Dumb Module"
        description: str = "..."
        icon: str = "none"

        async def exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, Self | None]:
            return False, None

    m1 = MockupModule(
        graph_id=2,
        inputs={0: [(0, trigger)]},
        outputs={},
        configuration={},
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )
    trigger.outputs[0] = [(0, m1)]

    return Workflow(
        id=25,
        uuid=str(uuid.uuid4()),
        name="Demo workflow",
        description="",
        timestamp=0,
        enabled=True,
        trigger_id="demo",
        debug_enabled=True,
        data=WorkflowGraph(
            nodes={0: trigger, 1: m1},
            root=trigger,
            frames=[],
        ),
    )


@pytest.fixture
def wf(trigger: Trigger, modules: Dict[int, Module]) -> Workflow:
    return Workflow(
        id=24,
        uuid=str(uuid.uuid4()),
        name="Demo workflow",
        description="",
        timestamp=0,
        enabled=True,
        trigger_id="demo",
        debug_enabled=True,
        data=WorkflowGraph(
            nodes={0: trigger, **modules},
            root=trigger,
            frames=[],
        ),
    )


@pytest.fixture
def modules(trigger: Trigger) -> List[Module]:
    @dataclass
    class MockupModule(ModuleAction):
        id: str = "demo"
        name: str = "Demo :: Dumb Module"
        description: str = "..."
        icon: str = "none"

        async def exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, Self | None]:
            if self.outputs[0] != []:
                return True, self.outputs[0][0][1]
            payload.user_messages += ["Hello World"]
            return True, None

    m1 = MockupModule(
        graph_id=2,
        inputs={0: [(0, trigger)]},
        outputs={},
        configuration={},
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )
    m2 = MockupModule(
        graph_id=3,
        inputs={0: [(0, m1)]},
        outputs={0: []},
        configuration={},
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )
    trigger.outputs[0] = [(0, m1)]
    m1.outputs[0] = [(0, m2)]

    return {1: m1, 2: m2}


@pytest.fixture
def empty_wf(trigger: Trigger) -> Workflow:
    return Workflow(
        id=23,
        uuid=str(uuid.uuid4()),
        name="Demo workflow",
        description="",
        timestamp=0,
        enabled=True,
        trigger_id="demo",
        debug_enabled=True,
        data=WorkflowGraph(
            nodes={0: trigger},
            root=trigger,
            frames=[],
        ),
    )


@pytest.fixture
def trigger() -> Trigger:
    return Trigger(
        graph_id=1,
        id="demo",
        name="demo",
        scope="local",
        description="Hello World",
        blocking=False,
        overhead=Overhead.LOW,
        inputs={},
        outputs={},
        apperance=Apperance((0, 0), False, "", None),
    )
