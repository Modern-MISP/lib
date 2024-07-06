from dataclasses import dataclass
from json import loads
from typing import Any, Dict

import pytest

from mmisp.workflows.graph import Apperance, Node, Trigger, WorkflowGraph
from mmisp.workflows.legacy import GraphFactory
from mmisp.workflows.modules import ModuleAttributeCommentOperation, ModuleTagIf, Overhead


def test_decode_basic(attribute_after_save_workflow: Dict[str, Any]) -> None:
    graph = GraphFactory.jsondict2graph(attribute_after_save_workflow)
    assert isinstance(graph, WorkflowGraph)

    assert len(graph.nodes) == 5
    assert len(graph.frames) == 1

    frame = list(graph.frames)[0]
    assert str(frame.uuid) == "072abe47-f136-4ef2-8932-1b67af93e27b"

    # make sure the root is also the first node
    assert graph.root is graph.nodes[1]
    assert isinstance(graph.root, Trigger)

    # ONLY one trigger
    assert all(not isinstance(node, Trigger) for node in list(graph.nodes)[1:])

    assert len(graph.root.inputs) == 0
    assert len(graph.root.outputs) == 1
    assert len(graph.root.outputs[1]) == 1

    # local ID of the previous node
    assert graph.root.outputs[1][0][0] == 1
    first_node: ModuleAttributeCommentOperation = graph.root.outputs[1][0][1]
    assert first_node.inputs[1][0][1] is graph.root
    assert isinstance(first_node, ModuleAttributeCommentOperation)

    assert first_node.configuration.data["comment"] == "just a test :D"

    assert len(first_node.outputs) == 1
    next_node = first_node.outputs[1][0][1]
    assert len(first_node.outputs[1]) == 1
    assert isinstance(next_node, ModuleTagIf)
    assert len(next_node.inputs) == 1
    assert next_node.inputs[1][0][1] is first_node
    assert len(next_node.outputs) == 2

    assert next_node.id == "tag-if"
    assert next_node.apperance.cssClass == "block-type-if block-type-logic expect-misp-core-format disabled"


def test_simple_workflow_to_dict() -> None:
    trigger = Trigger(
        id="attribute-after-save",
        name="Attribute after save",
        apperance=Apperance((1.0, 1.0), False, "disabled", "lalala"),
        inputs={},
        outputs={},
        graph_id=1,
        scope="attribute",
        description="wat",
        blocking=False,
        overhead=Overhead.HIGH,
    )

    workflow = WorkflowGraph({1: trigger}, trigger, [])
    workflow_json = GraphFactory.graph2jsondict(workflow)

    assert len(workflow_json) == 1
    assert "1" in workflow_json
    assert workflow_json["1"]["id"] == 1
    assert workflow_json["1"]["pos_x"] == 1.0
    assert workflow_json["1"]["pos_y"] == 1.0

    assert "name" not in workflow_json["1"]
    assert workflow_json["1"]["data"]["name"] == "Attribute after save"
    assert workflow_json["1"]["data"]["node_uid"] == "lalala"

    assert isinstance(workflow_json["1"]["inputs"], list)
    assert len(workflow_json["1"]["inputs"]) == 0
    assert isinstance(workflow_json["1"]["outputs"], dict)
    assert len(workflow_json["1"]["outputs"]) == 1
    assert len(workflow_json["1"]["outputs"]["output_1"]["connections"]) == 0


def test_invalid_class_type() -> None:
    @dataclass
    class Node_(Node):
        pass

    instance = Node_(inputs={}, outputs={}, graph_id=1)
    try:
        GraphFactory.graph2jsondict(WorkflowGraph({1: instance}, instance, []))
        pytest.fail()
    except ValueError:
        pass


def test_undefined_version(enrichment_before_query_workflow: Dict[str, Any]) -> None:
    workflow = GraphFactory.jsondict2graph(enrichment_before_query_workflow)

    assert isinstance(workflow.nodes[1], Trigger)

    assert workflow.nodes[2].id == "attach-warninglist"
    assert workflow.nodes[2].version == "0.0"  # the fallback


def test_symmetry(attribute_after_save_workflow: Dict[str, Any], empty_workflow: Dict[str, Any]) -> None:
    for workflow in [
        attribute_after_save_workflow,
        empty_workflow,
    ]:
        json_from_graph = GraphFactory.graph2jsondict(GraphFactory.jsondict2graph(workflow))
        # we ignore filter inconsistencies. See comment in `GraphFactory.__node_to_dict`
        # for rationale.
        del workflow["1"]["data"]["saved_filters"]
        del json_from_graph["1"]["data"]["saved_filters"]
        assert workflow == json_from_graph


@pytest.fixture
def enrichment_before_query_workflow() -> Dict[str, Any]:
    return loads(
        """{\"1\":{\"class\":\"block-type-trigger\",\"data\":{\"id\":\"enrichment-before-query\",\"scope\":\"others\",\"name\":\"Enrichment Before Query\",\"description\":\"This trigger is called just before a query against the enrichment service is done\",\"icon\":\"asterisk\",\"inputs\":0,\"outputs\":1,\"blocking\":true,\"misp_core_format\":true,\"trigger_overhead\":1,\"trigger_overhead_message\":\"\",\"is_misp_module\":false,\"is_custom\":false,\"expect_misp_core_format\":false,\"version\":\"0.1\",\"icon_class\":\"\",\"multiple_output_connection\":false,\"support_filters\":false,\"saved_filters\":[{\"text\":\"selector\",\"value\":\"\"},{\"text\":\"value\",\"value\":\"\"},{\"text\":\"operator\",\"value\":\"\"},{\"text\":\"path\",\"value\":\"\"}],\"params\":[],\"module_type\":\"trigger\",\"html_template\":\"trigger\",\"disabled\":true},\"id\":1,\"inputs\":[],\"outputs\":{\"output_1\":{\"connections\":[{\"node\":\"2\",\"output\":\"input_1\"}]}},\"pos_x\":0,\"pos_y\":0,\"typenode\":false},\"2\":{\"id\":2,\"data\":{\"id\":\"attach-warninglist\",\"name\":\"Attach warninglist\",\"module_type\":\"action\",\"indexed_params\":[]},\"pos_x\":700,\"pos_y\":0,\"inputs\":{\"input_1\":{\"connections\":[{\"node\":\"1\",\"input\":\"output_1\"},{\"node\":\"3\",\"input\":\"output_1\"}]}},\"outputs\":{\"output_1\":{\"connections\":[]}}},\"3\":{\"id\":3,\"data\":{\"id\":\"attach-warninglist\",\"name\":\"Attach warninglist\",\"module_type\":\"action\",\"indexed_params\":[]},\"pos_x\":0,\"pos_y\":-500,\"inputs\":{\"input_1\":{\"connections\":[{\"node\":\"4\",\"input\":\"output_1\"}]}},\"outputs\":{\"output_1\":{\"connections\":[{\"node\":\"2\",\"output\":\"input_1\"}]}}},\"4\":{\"id\":4,\"data\":{\"id\":\"Module_attribute_comment_operation\",\"name\":\"Attribute comment operation\",\"module_type\":\"action\",\"indexed_params\":[]},\"pos_x\":-450,\"pos_y\":-600,\"inputs\":{\"input_1\":{\"connections\":[]}},\"outputs\":{\"output_1\":{\"connections\":[{\"node\":\"3\",\"output\":\"input_1\"}]}}}}"""  # noqa
    )


@pytest.fixture
def attribute_after_save_workflow() -> Dict[str, Any]:
    """
    From https://gitlab.kit.edu/kit/kit-cert/mmisp/pse-workflows/mmisp-cheatsheet/-/blob/master/workflows.sql?ref_type=heads
    """
    return loads(
        """{\"1\":{\"id\":1,\"name\":\"Attribute+After+Save\",\"data\":{\"id\":\"attribute-after-save\",\"scope\":\"attribute\",\"name\":\"Attribute+After+Save\",\"description\":\"This+trigger+is+called+after+an+Attribute+has+been+saved+in+the+database\",\"icon\":\"cube\",\"inputs\":0,\"outputs\":1,\"blocking\":false,\"misp_core_format\":true,\"trigger_overhead\":3,\"trigger_overhead_message\":\"This+trigger+is+called+each+time+an+Attribute+has+been+saved.+This+means+that+when+a+large+quantity+of+Attributes+are+being+saved+(e.g.+Feed+pulling+or+synchronisation),+the+workflow+will+be+run+for+as+many+time+as+there+are+Attributes.\",\"is_misp_module\":false,\"is_custom\":false,\"expect_misp_core_format\":false,\"version\":\"0.1\",\"icon_class\":\"\",\"multiple_output_connection\":false,\"support_filters\":false,\"saved_filters\":{\"selector\":\"\",\"value\":\"\",\"operator\":\"\",\"path\":\"\"},\"module_type\":\"trigger\",\"html_template\":\"trigger\",\"disabled\":true,\"node_uid\":\"lj0afrvshbgoww\",\"indexed_params\":[],\"previous_module_version\":\"0.1\",\"module_version\":\"0.1\"},\"class\":\"block-type-trigger disabled\",\"typenode\":false,\"inputs\":[],\"outputs\":{\"output_1\":{\"connections\":[{\"node\":\"2\",\"output\":\"input_1\"}]}},\"pos_x\":-750,\"pos_y\":100},\"2\":{\"id\":2,\"name\":\"Attribute+comment+operation\",\"data\":{\"node_uid\":\"lm0b2x4ip99j5\",\"indexed_params\":{\"comment\":\"just a test :D\"},\"saved_filters\":{\"selector\":\"\",\"value\":\"tlp:white\",\"operator\":\"in\",\"path\":\"\"},\"module_type\":\"action\",\"id\":\"Module_attribute_comment_operation\",\"name\":\"Attribute+comment+operation\",\"multiple_output_connection\":false,\"previous_module_version\":\"0.1\",\"module_version\":\"0.1\"},\"class\":\"block-type-default expect-misp-core-format\",\"typenode\":false,\"inputs\":{\"input_1\":{\"connections\":[{\"node\":\"1\",\"input\":\"output_1\"}]}},\"outputs\":{\"output_1\":{\"connections\":[{\"node\":\"6\",\"output\":\"input_1\"}]}},\"pos_x\":-350,\"pos_y\":150},\"4\":{\"id\":4,\"name\":\"Enrich+Event\",\"data\":{\"node_uid\":\"ln039750trzo47\",\"indexed_params\":{\"modules\":\"circl_passivessl\"},\"saved_filters\":{\"selector\":\"\",\"value\":\"\",\"operator\":\"not_in\",\"path\":\"Tag.{n}.Name\"},\"module_type\":\"action\",\"id\":\"enrich-event\",\"name\":\"Enrich+Event\",\"multiple_output_connection\":false,\"previous_module_version\":\"0.2\",\"module_version\":\"0.2\"},\"class\":\"block-type-default expect-misp-core-format\",\"typenode\":false,\"inputs\":{\"input_1\":{\"connections\":[{\"node\":\"6\",\"input\":\"output_2\"}]}},\"outputs\":{\"output_1\":{\"connections\":[]}},\"pos_x\":800,\"pos_y\":725},\"6\":{\"id\":6,\"name\":\"IF+::+Tag\",\"data\":{\"indexed_params\":{\"scope\":\"event_attribute\",\"condition\":\"in_or\",\"tags\":[\"cossi:TLP=\\\"white\\\"\",\"PowerShell Installer\"],\"clusters\":[\"tea-matrix=\\\"Milk+in+tea\\\"\"]},\"saved_filters\":{\"selector\":\"\",\"value\":\"\",\"operator\":\"\",\"path\":\"\"},\"node_uid\":\"ls0tg7guii5qv8\",\"module_type\":\"logic\",\"id\":\"tag-if\",\"name\":\"IF+::+Tag\",\"multiple_output_connection\":false,\"previous_module_version\":\"0.4\",\"module_version\":\"0.4\"},\"class\":\"block-type-if block-type-logic expect-misp-core-format disabled\",\"typenode\":false,\"inputs\":{\"input_1\":{\"connections\":[{\"node\":\"2\",\"input\":\"output_1\"}]}},\"outputs\":{\"output_1\":{\"connections\":[{\"node\":\"7\",\"output\":\"input_1\"}]},\"output_2\":{\"connections\":[{\"node\":\"4\",\"output\":\"input_1\"}]}},\"pos_x\":125,\"pos_y\":75},\"7\":{\"id\":7,\"name\":\"Stop+execution\",\"data\":{\"indexed_params\":[],\"saved_filters\":{\"selector\":\"\",\"value\":\"\",\"operator\":\"\",\"path\":\"\"},\"node_uid\":\"no0s3zk3nfnq5\",\"module_type\":\"action\",\"id\":\"stop-execution\",\"name\":\"Stop+execution\",\"multiple_output_connection\":false,\"previous_module_version\":\"0.1\",\"module_version\":\"0.1\"},\"class\":\"block-type-default disabled\",\"typenode\":false,\"inputs\":{\"input_1\":{\"connections\":[{\"node\":\"6\",\"input\":\"output_1\"}]}},\"outputs\":[],\"pos_x\":900,\"pos_y\":-50},\"_frames\":{\"072abe47-f136-4ef2-8932-1b67af93e27b\":{\"id\":\"072abe47-f136-4ef2-8932-1b67af93e27b\",\"text\":\"PAP:RED+and+tlp:red+Blocking\",\"nodes\":[\"6\",\"7\"],\"class\":\"\"}}}"""  # noqa
    )


@pytest.fixture
def empty_workflow() -> Dict[str, Any]:
    return loads(
        """{\"1\":{\"class\":\"block-type-trigger\",\"data\":{\"id\":\"event-publish\",\"scope\":\"event\",\"name\":\"Event Publish\",\"description\":\"This trigger is called just before a MISP Event starts the publishing process\",\"icon\":\"upload\",\"inputs\":0,\"outputs\":1,\"blocking\":true,\"misp_core_format\":true,\"trigger_overhead\":1,\"trigger_overhead_message\":\"\",\"is_misp_module\":false,\"is_custom\":false,\"expect_misp_core_format\":false,\"version\":\"0.1\",\"icon_class\":\"\",\"multiple_output_connection\":false,\"support_filters\":false,\"saved_filters\":[{\"text\":\"selector\",\"value\":\"\"},{\"text\":\"value\",\"value\":\"\"},{\"text\":\"operator\",\"value\":\"\"},{\"text\":\"path\",\"value\":\"\"}],\"params\":[],\"module_type\":\"trigger\",\"html_template\":\"trigger\",\"disabled\":true},\"id\":1,\"inputs\":[],\"outputs\":{\"output_1\":{\"connections\":[]}},\"pos_x\":0,\"pos_y\":0,\"typenode\":false}}"""  # noqa
    )
