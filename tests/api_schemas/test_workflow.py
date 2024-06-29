from json import loads
from typing import Any, Dict

import pytest
from fastapi import HTTPException

from mmisp.api_schemas.workflow import json_dict_to_workflow_entity, workflow_entity_to_json_dict
from mmisp.db.models.workflow import Workflow
from mmisp.workflows.graph import WorkflowGraph
from mmisp.workflows.modules import Trigger


def test_create_entity(attribute_after_save_workflow: Dict[str, Any]) -> None:
    workflow = json_dict_to_workflow_entity(attribute_after_save_workflow)
    assert isinstance(workflow, Workflow)
    assert isinstance(workflow.data, WorkflowGraph)

    assert workflow.id == "9"
    assert workflow.name == "Workflow for trigger attribute-after-save"
    assert workflow.timestamp == "1718632138"
    assert not workflow.enabled
    assert isinstance(workflow.data.root, Trigger)

    assert attribute_after_save_workflow == workflow_entity_to_json_dict(workflow)


def test_missing_toplevel_key() -> None:
    try:
        json_dict_to_workflow_entity({})
        pytest.fail()
    except HTTPException as he:
        assert he.status_code == 400
        assert he.detail == "JSON body must contain a 'Workflow' key!"


def test_missing_key() -> None:
    try:
        json_dict_to_workflow_entity({"Workflow": {}})
        pytest.fail()
    except HTTPException as he:
        assert he.status_code == 400
        assert he.detail == "Missing attribute 'id' in workflow JSON body"


@pytest.fixture
def attribute_after_save_workflow() -> Dict[str, Any]:
    return loads("""{
    "Workflow": {
        "id": "9",
        "uuid": "17fa92d1-7b40-444c-8629-a0686965d38b",
        "name": "Workflow for trigger attribute-after-save",
        "description": "",
        "timestamp": "1718632138",
        "enabled": false,
        "counter": "0",
        "trigger_id": "attribute-after-save",
        "debug_enabled": false,
        "data": {
            "1": {
                "class": "block-type-trigger",
                "data": {
                    "id": "attribute-after-save",
                    "scope": "attribute",
                    "name": "Attribute After Save",
                    "description": "This trigger is called after an Attribute has been saved in the database",
                    "icon": "cube",
                    "inputs": 0,
                    "outputs": 1,
                    "blocking": false,
                    "misp_core_format": true,
                    "trigger_overhead": 3,
                    "trigger_overhead_message": "This trigger is called each time an Attribute has been saved. [...]",
                    "is_misp_module": false,
                    "is_custom": false,
                    "expect_misp_core_format": false,
                    "version": "0.1",
                    "icon_class": "",
                    "multiple_output_connection": false,
                    "support_filters": false,
                    "saved_filters": [
                        {
                            "text": "selector",
                            "value": ""
                        },
                        {
                            "text": "value",
                            "value": ""
                        },
                        {
                            "text": "operator",
                            "value": ""
                        },
                        {
                            "text": "path",
                            "value": ""
                        }
                    ],
                    "params": [],
                    "module_type": "trigger",
                    "html_template": "trigger",
                    "disabled": false
                },
                "id": 1,
                "inputs": [],
                "outputs": {
                    "output_1": {
                        "connections": []
                    }
                },
                "pos_x": 0,
                "pos_y": 0,
                "typenode": false
            }
        },
        "listening_triggers": [
            {
                "id": "attribute-after-save",
                "scope": "attribute",
                "name": "Attribute After Save",
                "description": "This trigger is called after an Attribute has been saved in the database",
                "icon": "cube",
                "inputs": 0,
                "outputs": 1,
                "blocking": false,
                "misp_core_format": true,
                "trigger_overhead": 3,
                "trigger_overhead_message": "This trigger is called each time an Attribute has been saved. [...]",
                "is_misp_module": false,
                "is_custom": false,
                "expect_misp_core_format": false,
                "version": "0.1",
                "icon_class": "",
                "multiple_output_connection": false,
                "support_filters": false,
                "saved_filters": [
                    {
                        "text": "selector",
                        "value": ""
                    },
                    {
                        "text": "value",
                        "value": ""
                    },
                    {
                        "text": "operator",
                        "value": ""
                    },
                    {
                        "text": "path",
                        "value": ""
                    }
                ],
                "params": [],
                "module_type": "trigger",
                "html_template": "trigger",
                "disabled": false
            }
        ]
    }
}""")
