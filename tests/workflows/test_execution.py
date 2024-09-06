import uuid
from dataclasses import dataclass, field
from typing import AsyncGenerator, Dict, List, Self, Tuple
from unittest.mock import AsyncMock, Mock

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mmisp.db.models.admin_setting import AdminSetting
from mmisp.db.models.event import Event
from mmisp.db.models.organisation import Organisation
from mmisp.db.models.role import Role
from mmisp.db.models.workflow import Workflow
from mmisp.lib.logging import ApplicationLogger
from mmisp.workflows.execution import (
    VerbatimWorkflowInput,
    _increase_workflow_execution_count,
    create_virtual_root_user,
    execute_workflow,
    workflow_by_trigger_id,
)
from mmisp.workflows.graph import Apperance, Module, Trigger, WorkflowGraph
from mmisp.workflows.input import RoamingData, WorkflowInput
from mmisp.workflows.misp_core_format import event_after_save_new_to_core_format
from mmisp.workflows.modules import (
    ModuleAction,
    ModuleConfiguration,
    ModulePublishEvent,
    ModuleStopExecution,
    Overhead,
    workflow_node,
)


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
async def test_virtual_user_no_org(db: AsyncSession, role: Role) -> None:
    try:
        await create_virtual_root_user(db)
        pytest.fail()
    except ValueError:
        pass


@pytest.mark.asyncio
async def test_create_virtual_user(db: AsyncSession, role: Role, org: Organisation) -> None:
    vu = await create_virtual_root_user(db)
    assert vu.id == 0
    assert vu.email == "SYSTEM"
    assert vu.org_id == org.id
    assert vu.role_id == role.id


@pytest_asyncio.fixture
async def role(db: AsyncSession) -> AsyncGenerator[Role, None]:
    role = Role(name="Admin", perm_site_admin=True)

    db.add(role)
    await db.commit()
    yield role
    await db.delete(role)
    await db.commit()


@pytest_asyncio.fixture
async def org(db: AsyncSession) -> AsyncGenerator[Organisation, None]:
    org = Organisation(name="Snens", local=True, description="Foo", type="Bar", nationality="Ger", sector="idk")
    db.add(org)
    await db.commit()
    yield org
    await db.delete(org)
    await db.commit()


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


@pytest.mark.asyncio
async def test_failing_workflow_rolls_back_transaction(publish_wf: Workflow, event: Event, db: AsyncSession) -> None:
    await db.commit()
    await db.refresh(event)
    result = await execute_workflow(publish_wf, Mock(), event, db, Mock())
    await db.commit()
    assert not result[0]
    assert result[1] == ["Execution stopped"]
    await db.refresh(event)
    assert not event.published


@pytest_asyncio.fixture
async def publish_wf(db: AsyncSession) -> AsyncGenerator[Workflow, None]:
    @workflow_node
    @dataclass(kw_only=True, eq=False)
    class FakeTrigger(Trigger):
        id: str = "fake"
        name: str = "Fake"
        version: str = "0.1"
        scope: str = "fake"
        blocking: bool = False
        description: str = "Fake"
        overhead: Overhead = Overhead.LOW

        async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
            assert isinstance(input, Event)
            return await event_after_save_new_to_core_format(db, input)

    appr = Apperance((0, 0), False, "", None)

    stop = ModuleStopExecution(
        graph_id=3,
        inputs={1: []},
        outputs={},
        apperance=appr,
        configuration=ModuleConfiguration({}),
        on_demand_filter=None,
    )

    publish = ModulePublishEvent(
        graph_id=2,
        inputs={1: []},
        outputs={1: [(1, stop)]},
        apperance=appr,
        configuration=ModuleConfiguration({}),
        on_demand_filter=None,
    )

    trigger = FakeTrigger(
        graph_id=1,
        inputs={1: []},
        outputs={1: [(1, publish)]},
        apperance=appr,
    )

    publish.inputs[1].append((1, trigger))
    stop.inputs[1].append((1, publish))

    wf = Workflow(
        id=26,
        uuid=str(uuid.uuid4()),
        name="Demo workflow",
        description="",
        timestamp=0,
        enabled=True,
        trigger_id="demo",
        debug_enabled=True,
        data=WorkflowGraph(
            nodes={1: trigger, 2: publish, 3: stop},
            root=trigger,
            frames=[],
        ),
    )
    db.add(wf)
    await db.commit()
    yield wf
    await db.delete(wf)
    await db.commit()


@pytest.mark.asyncio
async def test_execute_unsupported(wf: Workflow) -> None:
    db = AsyncMock()
    user = Mock()
    logger = Mock()
    wf.data.nodes[1].id = "mod-1"
    wf.data.nodes[1].supported = False
    wf.data.nodes[2].id = "mod-2"
    wf.data.nodes[2].supported = False

    status, messages = await execute_workflow(wf, user, {}, db, logger)
    assert not status
    # Python set iterates its elements in a random order, since we only list the detected node id and don't care
    # about the order in which they are displayed, we leave it like that.
    assert messages == [
        "Workflow could not be executed, because it contains unsupported modules with the following IDs: mod-1, mod-2"
    ] or messages == [
        "Workflow could not be executed, because it contains unsupported modules with the following IDs: mod-2, mod-1"
    ]


@pytest.mark.asyncio
async def test_increase_workflow_number(wf_in_db: Workflow, db: AsyncSession) -> None:
    await _increase_workflow_execution_count(db, wf_in_db.id)
    workflow = (await db.execute(select(Workflow).filter(Workflow.id == wf_in_db.id))).scalars().one()
    assert workflow.counter == 1

    await _increase_workflow_execution_count(db, wf_in_db.id)
    workflow = (await db.execute(select(Workflow).filter(Workflow.id == wf_in_db.id))).scalars().one()
    assert workflow.counter == 2


@pytest.mark.asyncio
async def test_wf_by_trigger(wf_in_db: Workflow, db: AsyncSession, enable_admin_setting: AdminSetting) -> None:
    wf = await workflow_by_trigger_id("demo", db)
    assert wf is not None
    assert wf.id == wf_in_db.id


@pytest.mark.asyncio
async def test_wf_by_trigger_when_feature_disabled(wf_in_db: Workflow, db: AsyncSession) -> None:
    assert not await workflow_by_trigger_id("demo", db)


@pytest_asyncio.fixture
async def enable_admin_setting(db: AsyncSession) -> AsyncGenerator[AdminSetting, None]:
    setting = AdminSetting(setting="workflow_feature_enabled", value="True")
    db.add(setting)
    await db.commit()
    yield setting
    await db.delete(setting)
    await db.commit()


@pytest_asyncio.fixture
async def wf_in_db(db: AsyncSession) -> AsyncGenerator[Workflow, None]:
    @workflow_node
    @dataclass(kw_only=True, eq=False)
    class FakeTrigger(Trigger):
        id: str = "fake"
        name: str = "Fake"
        version: str = "0.1"
        scope: str = "fake"
        blocking: bool = False
        description: str = "Fake"
        overhead: Overhead = Overhead.LOW

    trigger = FakeTrigger(
        graph_id=1,
        inputs={},
        outputs={},
        apperance=Apperance((0, 0), False, "", None),
    )

    wf = Workflow(
        uuid=str(uuid.uuid4()),
        name="Demo workflow",
        description="",
        timestamp=0,
        enabled=True,
        trigger_id="demo",
        debug_enabled=True,
        data=WorkflowGraph(
            nodes={1: trigger},
            root=trigger,
            frames=[],
        ),
    )
    db.add(wf)
    await db.commit()
    yield wf
    await db.delete(wf)
    await db.commit()


@pytest.mark.asyncio
async def test_jinja2(wf: Workflow, module_jinja2: Dict[int, Module]) -> None:
    db = AsyncMock()
    user = Mock()
    logger = Mock()

    wf.data.nodes[1] = module_jinja2
    del wf.data.nodes[2]

    # To anyone debugging this test:
    # exceptions are already handled in `walk_nodes()`. The easiest way
    # to get assertion errors from `MockupModule` is by adding `raise e`
    # to the `except` clause that wraps the jinja2 invocations.
    assert (await execute_workflow(wf, user, {"whom": "Misp"}, db, logger))[0]


@pytest.fixture
def module_jinja2(trigger: Trigger) -> List[Module]:
    @dataclass
    class MockupModule(ModuleAction):
        id: str = "demo"
        name: str = "Demo :: Dumb Module"
        description: str = "..."
        icon: str = "none"
        template_params: List[str] = field(default_factory=lambda: ["foo"])

        async def exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, Self | None]:
            assert self.configuration.data["foo"] == "Hello Misp"
            return True, None

    m1 = MockupModule(
        graph_id=2,
        inputs={0: [(0, trigger)]},
        outputs={},
        configuration=ModuleConfiguration({"foo": "Hello {{whom}}"}),
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )
    trigger.outputs[0] = [(0, m1)]

    return m1


@pytest.fixture
def wf_fail(trigger: Trigger) -> Workflow:
    @dataclass
    class MockupModule(ModuleAction):
        id: str = "demo"
        name: str = "Demo :: Dumb Module"
        description: str = "..."
        icon: str = "none"

        async def exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, Self | None]:
            payload.user_messages.append("Hello World")
            return False, None

    m1 = MockupModule(
        graph_id=2,
        inputs={0: [(0, trigger)]},
        outputs={},
        configuration=ModuleConfiguration({}),
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
            return True, None

    m1 = MockupModule(
        graph_id=2,
        inputs={0: [(0, trigger)]},
        outputs={},
        configuration=ModuleConfiguration({}),
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )
    m2 = MockupModule(
        graph_id=3,
        inputs={0: [(0, m1)]},
        outputs={0: []},
        configuration=ModuleConfiguration({}),
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
