"""
Models related to the execution of workflows.
"""

from .graph import WorkflowGraph
from .input import WorkflowInput


def execute_workflow(workflow: WorkflowGraph, input: WorkflowInput) -> bool:
    """
    Provides the functionality for executing a workflow, which consists of traversing
    the given workflow graph and its modules and executing these modules with their specific
    configurations.

    Arguments:
        workflow: The Graph representation of the workflow to be executed.
        input:    Initial payload for the workflow.
    """
    return True
