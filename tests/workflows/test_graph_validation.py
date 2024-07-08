from typing import Self

from mmisp.workflows.graph import (
    ConfigurationError,
    CyclicGraphError,
    Graph,
    GraphValidationResult,
    InconsistentEdgeBetweenAdjacencyLists,
    Module,
    MultipleEdgesPerOutput,
    Node,
    Trigger,
)


class DummyNode(Node):
    pass


class DummyGraph(Graph):
    def check(self: Self) -> GraphValidationResult:
        return super().check()


def dummy_add_edge(_from: Node, to: Node) -> None:
    if _from.outputs.get(1) is None:
        _from.outputs[1] = [(1, to)]
    else:
        _from.outputs[1].append((1, to))
    if to.inputs.get(1) is None:
        to.inputs[1] = [(1, _from)]
    else:
        to.inputs[1].append((1, _from))


def test_node_check() -> None:
    inp = {1: [(0, None)], 2: [(0, None)]}
    out = {1: [(0, None), (0, None)], 2: [(0, None)], 3: [(0, None)]}
    dummy_node = DummyNode(inputs=inp, outputs=out, n_outputs=2, graph_id=1)
    issues = dummy_node.check()
    # print(str(dummy_node.inputs.keys()) + "\n" + str(dummy_node.n_inputs))
    assert len(issues.errors) == 3
    assert issues.errors[0] == ConfigurationError(
        dummy_node, "There is an input port registered for this node outside of the valid range of [1, 1]."
    )
    assert issues.errors[1] == ConfigurationError(
        dummy_node, "There is an output port registered for this node outside of the valid range of [1, 2]."
    )
    assert issues.errors[2] == MultipleEdgesPerOutput((dummy_node, 1))


def test_graph_validation_result() -> None:
    res1 = GraphValidationResult([MultipleEdgesPerOutput((None, 0)), ConfigurationError(None, "Error1")])
    res2 = GraphValidationResult([])
    assert res2.is_valid()
    res1.add_result(res2)
    assert res1 == GraphValidationResult([MultipleEdgesPerOutput((None, 0)), ConfigurationError(None, "Error1")])


def test_graph_check_output_edge_no_input_edge() -> None:
    a = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    b = DummyNode(inputs={}, outputs={}, graph_id=1)
    a.outputs[1] = [(1, b), (2, b)]
    b.inputs[1] = [(1, a)]
    graph = DummyGraph({0: a, 1: b}, a, None)
    assert graph.check() == GraphValidationResult([InconsistentEdgeBetweenAdjacencyLists(a, 1, b, 2)])


def test_graph_check_input_edge_no_output_edge() -> None:
    a = DummyNode(inputs={}, outputs={}, graph_id=1)
    b = DummyNode(inputs={}, outputs={}, n_inputs=2, graph_id=1)
    a.outputs[1] = [(2, b)]
    b.inputs[2] = [(1, a), (2, a)]
    graph = DummyGraph({0: a, 1: b}, a, None)
    assert graph.check() == GraphValidationResult([InconsistentEdgeBetweenAdjacencyLists(a, 2, b, 2)])


def test_graph_check_cycle() -> None:
    a = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    b = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    c = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    d = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    e = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    f = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    g = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    h = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    i = DummyNode(inputs={}, outputs={}, enable_multiple_edges_per_output=True, graph_id=1)
    dummy_add_edge(a, b)
    dummy_add_edge(b, c)
    dummy_add_edge(b, d)
    dummy_add_edge(d, c)
    dummy_add_edge(d, e)
    dummy_add_edge(e, f)
    dummy_add_edge(f, b)
    dummy_add_edge(f, a)
    dummy_add_edge(g, a)
    dummy_add_edge(g, i)
    dummy_add_edge(i, h)
    dummy_add_edge(h, g)
    graph = DummyGraph({0: a, 1: b, 2: c, 3: d, 4: e, 5: f, 6: g, 7: h, 8: i}, a, None)
    assert graph.check() == GraphValidationResult(
        [
            CyclicGraphError([(f, 1, b, 1), (e, 1, f, 1), (d, 1, e, 1), (b, 1, d, 1)]),
            CyclicGraphError([(f, 1, a, 1), (e, 1, f, 1), (d, 1, e, 1), (b, 1, d, 1), (a, 1, b, 1)]),
            CyclicGraphError([(h, 1, g, 1), (i, 1, h, 1), (g, 1, i, 1)]),
        ]
    )


def test_if_node_subclasses_are_hashable() -> None:
    trigger = Trigger(
        inputs={},
        outputs={},
        graph_id=1,
        id="Test",
        name="Test",
        blocking=True,
        apperance=None,
        scope="None",
        description="Des",
        overhead=None,
    )
    assert trigger.__hash__() == id(trigger)
    assert trigger == trigger
    module = Module(
        inputs={},
        outputs={},
        graph_id=1,
        id="Test",
        name="Test",
        apperance=None,
        configuration=None,
        on_demand_filter=None,
    )
    assert module.__hash__() == id(module)
    assert module == module
