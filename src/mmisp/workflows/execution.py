"""
Models related to the execution of workflows.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models.workflow import Workflow
from .input import WorkflowInput


async def execute_workflow(workflow: Workflow, input: WorkflowInput, db: AsyncSession) -> bool:
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
    """

    return True
