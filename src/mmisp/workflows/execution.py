"""
Models related to the execution of workflows.
"""

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models.user import User
from ..db.models.workflow import Workflow
from ..lib.logging import ApplicationLogger
from .graph import Module, Trigger, VerbatimWorkflowInput
from .input import WorkflowInput
from .modules import ModuleLogic


def as_trigger(node: Module | Trigger) -> Trigger:
    match node:
        case Trigger() as t:
            return t
        case _:
            raise ValueError("Expected node to be a Trigger!")


def as_module(node: Module | Trigger) -> Module:
    match node:
        case Module() as t:
            return t
        case _:
            raise ValueError("Expected node to be a Module!")


async def walk_nodes(
    input: WorkflowInput, current_node: Module, workflow: Workflow, logger: ApplicationLogger, db: AsyncSession
) -> bool:
    try:
        result, next_node = await current_node.exec(input, db)
    except Exception as e:
        logger.log_workflow_execution_error(workflow, f"Error while executing module {current_node.id}. Error: {e}")
        return False

    success_type = "partial-success" if not result and not isinstance(current_node, ModuleLogic) else "success"

    logger.log_workflow_debug_message(
        workflow,
        f"Executed node `{current_node.id}`\n"
        + f"Node `{current_node.id}` from Workflow `{workflow.name}` ({workflow.id}) executed "
        + f"successfully with status: {success_type}",
    )

    if not result:
        return False

    if next_node is None:
        return True

    return await walk_nodes(input, next_node, workflow, logger, db)


async def execute_workflow(
    workflow: Workflow, user: User, input: VerbatimWorkflowInput, db: AsyncSession, logger: ApplicationLogger
) -> bool:
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

    graph = workflow.data
    trigger = as_trigger(graph.root)

    if trigger.disabled:
        return True

    logger.log_workflow_debug_message(
        workflow, f"Started executing workflow for trigger `{trigger.name}` ({workflow.id})"
    )

    next_step = next(iter(trigger.outputs.values()), None)
    # Nothing to do.
    if not next_step:
        return True

    try:
        roaming_data = await trigger.normalize_data(db, input)
    except Exception as e:
        logger.log_workflow_execution_error(workflow, f"Error while normalizing data for trigger. Error: \n{e}")
        return False

    input = WorkflowInput(
        data=roaming_data,
        user=user,
        workflow=workflow,
    )

    await db.execute(sa.update(Workflow).where(Workflow.id == workflow.id).values({"counter": Workflow.counter + 1}))

    result = await walk_nodes(input, as_module(next_step[0][1]), workflow, logger, db)

    if result:
        outcome = "success"
    else:
        outcome = "blocked" if trigger.blocking else "failure"

    logger.log_workflow_debug_message(
        workflow, f"Finished executing workflow for trigger `{trigger.name}` ({workflow.id}). Outcome: {outcome}"
    )

    return result
