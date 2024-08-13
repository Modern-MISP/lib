import uuid
from unittest.mock import Mock

import pytest

from mmisp.db.models.workflow import Workflow
from mmisp.lib.logging import ApplicationLogger
from mmisp.workflows.graph import Apperance, Trigger, WorkflowGraph
from mmisp.workflows.modules import Overhead


def test_no_log(workflow: Workflow) -> None:
    workflow.debug_enabled = False

    mock = Mock()
    logger = ApplicationLogger(mock)

    log_entry = logger.log_workflow_debug_message(workflow, "Something happened")

    assert log_entry is None
    assert mock.add.called == 0


def test_log(workflow: Workflow) -> None:
    mock = Mock()
    logger = ApplicationLogger(mock)

    log_entry = logger.log_workflow_debug_message(workflow, "Something happened")

    assert mock.add.called == 1
    mock.add.assert_called_with(log_entry)

    assert log_entry.model_id == 23
    assert log_entry.action == "execute_workflow"
    assert log_entry.user_id == 0
    assert log_entry.title == "Something happened"


def test_error_log(workflow: Workflow) -> None:
    # Make sure that this gets written regardless of
    # whether or not debugging is enabled.
    for debug in [True, False]:
        workflow.debug_enabled = debug
        mock = Mock()
        logger = ApplicationLogger(mock)

        log_entry = logger.log_workflow_execution_error(workflow, "Something happened")

        assert mock.add.called == 1
        mock.add.assert_called_with(log_entry)

        assert log_entry.model_id == 23
        assert log_entry.action == "execute_workflow"


@pytest.fixture
def workflow(trigger: Trigger) -> Workflow:
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
            nodes=[trigger],
            root=trigger,
            frames=[],
        ),
    )


@pytest.fixture
def trigger() -> Trigger:
    return Trigger(
        id="demo",
        name="demo",
        scope="local",
        description="Hello World",
        blocking=False,
        overhead=Overhead.LOW,
        inputs={},
        outputs={},
        graph_id=1,
        apperance=Apperance((0, 0), False, "", None),
    )
