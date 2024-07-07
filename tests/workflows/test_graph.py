from typing import Self
from unittest.mock import Mock

import pytest

from mmisp.workflows.graph import Apperance, Module
from mmisp.workflows.input import WorkflowInput


@pytest.mark.asyncio
async def test_default_exec_impl() -> None:
    m = Module(
        graph_id=1,
        id="demo",
        name="Demo Name",
        inputs={},
        outputs={0: [(0, Mock())]},
        configuration={},
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )

    assert await m.exec(WorkflowInput({}, Mock(), Mock())) == (False, None)


@pytest.mark.asyncio
async def test_default_exec_impl_success() -> None:
    class Module_(Module):
        async def _exec(self: Self, payload: WorkflowInput) -> bool:
            return True

    next_step = Mock()
    m = Module_(
        graph_id=1,
        id="demo",
        name="Demo Name",
        inputs={},
        outputs={0: [(0, next_step)]},
        configuration={},
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )

    result = await m.exec(WorkflowInput({}, Mock(), Mock()))
    assert result[0]
    assert result[1] == next_step


@pytest.mark.asyncio
async def test_default_exec_impl_2_outputs() -> None:
    m = Module(
        graph_id=1,
        id="demo",
        name="Demo Name",
        inputs={},
        n_outputs=2,
        outputs={0: [(0, Mock())], 1: []},
        configuration={},
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )

    try:
        await m.exec(WorkflowInput({}, Mock(), Mock())) == (False, None)
        pytest.fail()
    except AssertionError as e:
        assert "Module.exec() assumes exactly one output." in str(e)


@pytest.mark.asyncio
async def test_default_exec_impl_multiple_edges_per_output() -> None:
    m = Module(
        graph_id=1,
        id="demo",
        name="Demo Name",
        inputs={},
        outputs={0: [(0, Mock())]},
        enable_multiple_edges_per_output=True,
        configuration={},
        on_demand_filter=None,
        apperance=Apperance((0, 0), False, "mock", None),
    )

    try:
        await m.exec(WorkflowInput({}, Mock(), Mock())) == (False, None)
        pytest.fail()
    except AssertionError as e:
        assert "Module.exec() assumes each output allows only a single edge." in str(e)
