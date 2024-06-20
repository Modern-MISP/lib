"""
Data structure for the payload passed to the workflow and
filtering mechanism associated with it.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from ..db.models.workflows import Workflows

from ..db.models.user import User


RoamingData = Dict[str, Any]


class Operator(Enum):
    """
    Enum representing possible filter operations.
    """

    IN = "in"
    NOT_IN = "not_in"
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    ANY_VALUE = "any_value"
    IN_OR = "in_or"

    @classmethod
    def from_str(cls, input: str) -> Self:
        """
        Returns a member of this enum given the string
        representation of the operator.

        Arguments:
            input: string representation of the operator.
        """
        return cls(input)


@dataclass
class Filter:
    """
    The data passed to a workflow can be filtered on-demand.
    That means, all entries from the dict may be removed that
    don't match a condition.

    The condition that needs to match is represented by
    this object.

    There are two ways these filters can be applied:

    * via the
      [`ModuleGenericFilterData`][mmisp.workflows.modules.ModuleGenericFilterData]
      in place. Can be undone by adding
      [`ModuleGenericFilterReset`][mmisp.workflows.modules.ModuleGenericFilterReset]
      later on.

    * via a module with `on_demand_filtering_enabled` set to
      `True`. The filtering must be called by the module itself
      in that case.
    """

    selector: str
    """
    Attribute path pointing to a list inside the
    [`WorkflowInput`][mmisp.workflows.input.WorkflowInput].
    In this list, each element below attribute-path `path`
    will be checked against `value` using operation
    `operator`.

    For instance given the structure

    ```python
    {
        "foo": [
            {
                "bar": "lololo"
            },
            {
                "bar": "lalala"
            },
        ]
    }
    ```

    a filter with `selector` being `foo`, `path` being `bar`,
    `value` being `lololo` and `operator` being
    `not_equal` would result in

    ```python
    [
        {
            "bar": "lalala"
        }
    ]
    ```

    Path must be a
    [CakePHP hash path](https://book.cakephp.org/3/en/core-libraries/hash.html)
    since existing legacy MISP filters are using that format
    as well.
    """

    path: str
    """
    Attribute path in the list where each item will be
    checked against `value` using operation `operator`.
    """

    value: str | List[str]
    """
    Value to compare against. Can be a list for operations
    `in`/`not_in` or a string value for `equals`/etc..
    """

    operator: Operator
    """
    [`Operator`][mmisp.workflows.execution.Operator] to compare
    the item below `path` against `value`.
    """


class WorkflowInput:
    """
    When a workflow gets executed, it gets input data. For
    instance, the "after event save"-workflow gets a dictionary
    containing the event that was saved.

    Additionally, filters can be added by modules. That way,
    subsequent modules will only see a filtered subset
    of the workflow data. This operation can be undone.

    Filters are expressed using [`Filter`][mmisp.workflows.execution.Filter]
    class.
    """

    user: User
    """
    Represents the user execution a workflow. Is a system
    user with all privileges. Mostly useful for logging
    purposes.
    """

    workflow: "Workflows"
    """
    Reference to the workflow object being executed.
    """

    def __init__(self, data: RoamingData, user: User, workflow: "Workflows"):
        self.__unfiltered_data = data
        self.user = user
        self.workflow = workflow

    @property
    def data(self) -> RoamingData | List[RoamingData]:
        """
        Returns either all of the data given to the workflow input
        OR a list with filter results if a filter was added
        using [`WorkflowInput.add_filter`][mmisp.workflows.input.WorkflowInput.add_filter].
        """

    def add_filter(self, filter: Filter):
        """
        Adds another [`Filter`][mmisp.workflows.execution.Filter]
        to the workflow input.

        Arguments:
            filter: Filter to be added.
        """

    def reset_filters(self):
        """
        Removes all filters from the workflow input.
        [`WorkflowInput.data`][mmisp.workflows.input.WorkflowInput.data]
        will contain all of the data it has instead of a
        filtered portion now.
        """
