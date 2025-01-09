import uuid

import pytest

from mmisp.db.models.workflow import Workflow
from mmisp.lib.logger import db_log, print_request_log, reset_db_log, reset_request_log
from mmisp.workflows.graph import Apperance, Trigger, WorkflowGraph
from mmisp.workflows.modules import Overhead


def test_no_log(workflow: Workflow, capsys) -> None:
    reset_request_log()
    workflow.debug_enabled = False

    logger = workflow.get_logger()
    logger.debug(workflow, "Something happened")

    print_request_log()
    captured = capsys.readouterr()
    assert "Something happened" not in captured.out


def test_log(workflow: Workflow, capsys) -> None:
    reset_request_log()
    reset_db_log()
    logger = workflow.get_logger()

    logger.debug("Something happened")

    print_request_log()
    captured = capsys.readouterr()
    assert "Something happened" in captured.out

    assert db_log.get([])

    for log_entry in db_log.get([]):
        assert log_entry.model_id == 23
        assert log_entry.action == "execute_workflow"
        assert log_entry.user_id == 0
        assert log_entry.title == "Something happened"


def test_error_log_no_debug(workflow: Workflow, capsys) -> None:
    reset_request_log()
    reset_db_log()
    debug = False
    workflow.debug_enabled = debug

    logger = workflow.get_logger()
    logger.error("Something happened")

    print_request_log()
    captured = capsys.readouterr()
    assert "Something happened" in captured.out

    assert db_log.get([])

    for log_entry in db_log.get([]):
        assert log_entry.model_id == 23
        assert log_entry.action == "execute_workflow"
        assert log_entry.user_id == 0
        assert log_entry.title == "Something happened"


def test_error_log_debug(workflow: Workflow, capsys) -> None:
    reset_request_log()
    reset_db_log()
    debug = True
    workflow.debug_enabled = debug

    logger = workflow.get_logger()
    logger.error("Something happened")
    print_request_log()
    captured = capsys.readouterr()
    assert "Something happened" in captured.out

    assert db_log.get([])

    for log_entry in db_log.get([]):
        assert log_entry.model_id == 23
        assert log_entry.action == "execute_workflow"
        assert log_entry.user_id == 0
        assert log_entry.title == "Something happened"


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
