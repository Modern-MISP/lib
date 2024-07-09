"""
Models related to the execution of workflows.
"""

from typing import List, Tuple

import sqlalchemy as sa
from jinja2 import BaseLoader, Environment
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models.user import User
from ..db.models.workflow import Workflow
from ..lib.logging import ApplicationLogger
from .graph import Module, Trigger, VerbatimWorkflowInput
from .input import WorkflowInput
from .modules import ModuleLogic


def _as_trigger(node: Module | Trigger) -> Trigger:
    match node:
        case Trigger() as t:
            return t
        case _:
            raise ValueError("Expected node to be a Trigger!")


def _as_module(node: Module | Trigger) -> Module:
    match node:
        case Module() as t:
            return t
        case _:
            raise ValueError("Expected node to be a Module!")


async def walk_nodes(
    input: WorkflowInput,
    current_node: Module,
    workflow: Workflow,
    logger: ApplicationLogger,
    db: AsyncSession,
    jinja2_engine: Environment,
) -> Tuple[bool, List[str]]:
    """
    Recursive graph walker implementation starting at a given node.
    Used by the workflow execution itself, but can also be used to resume
    workflow execution, e.g. for concurrent modules that schedule jobs
    with the successor nodes.

    Arguments:
        input:          Workflow payload for `current_node`.
        current_node:   Node to resume execution with.
        workflow:       Workflow entity. Used for logging.
        logger:         Application logger to write debug messages and errors
            from the execution.
        db:             Database session.
        jinja2_engine:  Instantiated templating engine to substitute placeholders
            in module configuration with values from the payload.
    """

    try:
        data = input.data
        if isinstance(data, dict):

            def _render(item: str) -> str:
                return jinja2_engine.from_string(item).render(**data)

            for config_key in current_node.template_params:
                current_config = current_node.configuration.data
                if config_key in current_config:
                    value = current_config[config_key]
                    if isinstance(value, str):
                        current_config[config_key] = _render(value)
                    elif isinstance(value, bool):
                        continue
                    else:
                        current_config[config_key] = [_render(v) for v in value]
        result, next_node = await current_node.exec(input, db)
    except Exception as e:
        logger.log_workflow_execution_error(workflow, f"Error while executing module {current_node.id}. Error: {e}")
        return False, []

    success_type = "partial-success" if not result and not isinstance(current_node, ModuleLogic) else "success"

    logger.log_workflow_debug_message(
        workflow,
        f"Executed node `{current_node.id}`\n"
        + f"Node `{current_node.id}` from Workflow `{workflow.name}` ({workflow.id}) executed "
        + f"successfully with status: {success_type}",
    )

    if not result:
        return False, input.user_messages

    if next_node is None:
        return True, input.user_messages

    # At this stage we don't do any cycle detection, but assume that only
    # valid graphs w/o cycles in it were saved by the API.
    return await walk_nodes(input, next_node, workflow, logger, db, jinja2_engine)


class UnsupportedModules(Exception):
    pass


async def execute_workflow(
    workflow: Workflow, user: User, input: VerbatimWorkflowInput, db: AsyncSession, logger: ApplicationLogger
) -> Tuple[bool, List[str]]:
    """
    Provides the functionality for executing a workflow, which consists of traversing
    the given workflow graph and its modules and executing these modules with their specific
    configurations.

    !!! note
        Legacy MISP allows non-blocking paths, i.e. multiple "roots" & no
        termination of the workflow execution if one of the paths fails.

        This "feature" is left out entirely here: this would not only break
        the assumption of having a single root, but also complicate the execution
        code further.

        This is only implemented for concurrent tasks, however

        * A job will be exposed in worker that allows to resume execution of
          a workflow at a given node. This is triggered for each of the concurrent
          nodes.

        * No intertwined state since all the state of an execution is carried around via
          the payload.

    Arguments:
        workflow: The Graph representation of the workflow to be executed.
        input:    Initial payload for the workflow.
        db:       SQLAlchemy session.
        logger:   Application logger to notify about errors or (if debug is enabled) execution steps.
    """

    if not workflow.enabled:
        return False, []

    graph = workflow.data
    trigger = _as_trigger(graph.root)

    if trigger.disabled:
        return True, []

    logger.log_workflow_debug_message(
        workflow, f"Started executing workflow for trigger `{trigger.name}` ({workflow.id})"
    )

    next_step = next(iter(trigger.outputs.values()), None)
    # Nothing to do.
    if not next_step:
        return True, []

    if any(not x.supported for x in graph.nodes.values()):
        raise UnsupportedModules()

    try:
        roaming_data = await trigger.normalize_data(db, input)
    except Exception as e:
        logger.log_workflow_execution_error(workflow, f"Error while normalizing data for trigger. Error: \n{e}")
        return False, []

    input = WorkflowInput(
        data=roaming_data,
        user=user,
        workflow=workflow,
    )

    await db.execute(sa.update(Workflow).where(Workflow.id == workflow.id).values({"counter": Workflow.counter + 1}))

    result = await walk_nodes(
        input, _as_module(next_step[0][1]), workflow, logger, db, Environment(loader=BaseLoader())
    )

    if result[0]:
        outcome = "success"
    else:
        outcome = "blocked" if trigger.blocking else "failure"

    logger.log_workflow_debug_message(
        workflow, f"Finished executing workflow for trigger `{trigger.name}` ({workflow.id}). Outcome: {outcome}"
    )

    return result
