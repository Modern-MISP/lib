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

    Arguments:
        workflow: The Graph representation of the workflow to be executed.
        input:    Initial payload for the workflow.
    """

    return True
