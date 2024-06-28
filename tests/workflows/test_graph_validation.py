from typing import Self

from mmisp.workflows.graph import (
    ConfigurationError,
    CyclicGraphError,
    Graph,
    GraphValidationResult,
    InconsistentEdgeBetweenAdjacencyLists,
    MultipleEdgesPerOutput,
    Node,
    PathWarning,
)


class DummyNode(Node):
    pass


class DummyGraph(Graph):
    def check(self: Self) -> GraphValidationResult:
        return super().check()


def dummy_add_edge(_from: Node, to: Node) -> None:
    if _from.outputs.get(0) is None:
        _from.outputs[0] = [(0, to)]
    else:
        _from.outputs[0].append((0, to))
    if to.inputs.get(0) is None:
        to.inputs[0] = [(0, _from)]
    else:
        to.inputs[0].append((0, _from))


def test_node_check() -> None:
    inp = {0: [(0, None)], 1: [(0, None)]}
    out = {0: [(0, None), (0, None)], 1: [(0, None)], 2: [(0, None)]}
    dummy_node = DummyNode(inputs=inp, outputs=out, apperance=None, n_outputs=2)
    issues = dummy_node.check()
    assert len(issues.errors) == 3
    assert len(issues.warnings) == 0
    assert issues.errors[0] == ConfigurationError(
        dummy_node, "The number of registered inputs of the node exceeds its maximum allowed amount."
    )
    assert issues.errors[1] == ConfigurationError(
        dummy_node, "The number of registered outputs of the node exceeds its maximum allowed amount."
    )
    assert issues.errors[2] == MultipleEdgesPerOutput((dummy_node, 0))


def test_graph_validation_result() -> None:
    res1 = GraphValidationResult([MultipleEdgesPerOutput((None, 0)), ConfigurationError(None, "Error1")], [])
    res2 = GraphValidationResult([], [PathWarning(None, None, "Warn1", False)])
    res3 = GraphValidationResult([], [])
    assert res3.is_valid()
    res1.add_result(res2)
    res1.add_result(res3)
    print(res1)
    assert res1 == GraphValidationResult(
        [MultipleEdgesPerOutput((None, 0)), ConfigurationError(None, "Error1")],
        [PathWarning(None, None, "Warn1", False)],
    )


def test_graph_check_output_edge_no_input_edge() -> None:
    a = DummyNode(inputs={}, outputs={}, apperance=None)
    b = DummyNode(inputs={}, outputs={}, apperance=None)
    a.outputs[0] = [(0, b), (1, b)]
    a.enable_multiple_edges_per_output = True
    b.inputs[1] = [(0, a)]
    graph = DummyGraph({0: a, 1: b}, a, None)
    assert graph.check() == GraphValidationResult([InconsistentEdgeBetweenAdjacencyLists(a, 0, b, 0)], [])


def test_graph_check_input_edge_no_output_edge() -> None:
    a = DummyNode(inputs={}, outputs={}, apperance=None)
    b = DummyNode(inputs={}, outputs={}, apperance=None)
    a.outputs[0] = [(1, b)]
    a.enable_multiple_edges_per_output = True
    b.inputs[1] = [(0, a), (1, a)]
    graph = DummyGraph({0: a, 1: b}, a, None)
    assert graph.check() == GraphValidationResult([InconsistentEdgeBetweenAdjacencyLists(a, 1, b, 1)], [])


def test_graph_check_cycle() -> None:
    a = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
    b = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
    c = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
    d = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
    e = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
    f = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
    g = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
    h = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
    i = DummyNode(inputs={}, outputs={}, apperance=None, enable_multiple_edges_per_output=True)
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
            CyclicGraphError([(f, b), (e, f), (d, e), (b, d)]),
            CyclicGraphError([(f, a), (e, f), (d, e), (b, d), (a, b)]),
            CyclicGraphError([(h, g), (i, h), (g, i)]),
        ],
        [],
    )
