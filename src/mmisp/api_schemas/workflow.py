"""
API schemas for workflows. No classes here, just transformers.

Intended use for incoming JSON is

```python
async def update_workflow(
    workflow: Annotated[Workflow, Depends(json_dict_to_workflow_entity)]
):
    pass
```

and for returning a JSON representation for a workflow:
```python
async def get_workflow(
    ...
) -> Annotated[Workflow, Depends(workflow_entity_to_json_dict)]:
    pass
```
"""

from typing import Any, Dict

from fastapi import HTTPException

from ..db.models.workflow import Workflow
from ..workflows.legacy import GraphFactory


def json_dict_to_workflow_entity(input: Dict[str, Dict[str, Any]]) -> Workflow:
    if "Workflow" not in input:
        raise HTTPException(status_code=400, detail="JSON body must contain a 'Workflow' key!")

    workflow_data = input["Workflow"]
    try:
        return Workflow(
            id=workflow_data["id"],
            uuid=workflow_data["uuid"],
            name=workflow_data["name"],
            description=workflow_data["description"],
            timestamp=workflow_data["timestamp"],
            enabled=workflow_data["enabled"],
            counter=workflow_data["counter"],
            trigger_id=workflow_data["trigger_id"],
            debug_enabled=workflow_data["debug_enabled"],
            data=GraphFactory.jsondict2graph(workflow_data["data"]),
        )
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"Missing attribute {ke} in workflow JSON body")


def workflow_entity_to_json_dict(workflow: Workflow) -> Dict[str, Dict[str, Any]]:
    graph_json = GraphFactory.graph2jsondict(workflow.data)
    return {
        "Workflow": {
            "id": workflow.id,
            "uuid": workflow.uuid,
            "name": workflow.name,
            "description": workflow.description,
            "timestamp": workflow.timestamp,
            "enabled": workflow.enabled,
            "counter": workflow.counter,
            "trigger_id": workflow.trigger_id,
            "debug_enabled": workflow.debug_enabled,
            "data": graph_json,
            "listening_triggers": [graph_json[next(iter(graph_json))]["data"]],
        }
    }
