"""
Data structure for the payload passed to the workflow and
filtering mechanism associated with it.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Self, Type

if TYPE_CHECKING:
    from ..db.models.user import User
    from ..db.models.workflow import Workflow

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
    def from_str(cls: Type[Self], input: str) -> Self:
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
    [`Operator`][mmisp.workflows.input.Operator] to compare
    the item below `path` against `value`.
    """

    def __init__(self: Self, selector: str, path: str, operator: Operator, value: str | List[str]) -> None:
        self.selector = selector
        self.path = path
        self.operator = operator
        self.value = value

    def match_value(self: Self, value: Any) -> bool:
        """
        Check if a value matches a filter.

        Arguments:
            value: The value to check.
            filter: The filter to match against.

        Returns:
            True if the value matches the filter, False otherwise.
        """
        if self.operator == Operator.EQUALS:
            return value == self.value
        elif self.operator == Operator.NOT_EQUALS:
            return value != self.value
        elif self.operator == Operator.IN:
            return value in self.value if isinstance(self.value, list) else False
        elif self.operator == Operator.NOT_IN:
            return value not in self.value if isinstance(self.value, list) else False
        elif self.operator == Operator.ANY_VALUE:
            return True
        elif self.operator == Operator.IN_OR:
            #FIXME idk what in or does
            pass
        return False
    
    def _extract(self, data, path, filter_value):
        """
        Extracts values from a nested dictionary based on cakePHP hash path.
        Returns a list of extracted values.

        Args:
            data (dict or list): The input data from which to extract values.
            path (str): The path string specifying which values to extract.

        """

        def _recursive_delete(data, tokens):
            """
            Recursive helper method for extracting values based on tokens.
            """

            if not tokens:
                #FIXME 0/1 better names etc.
                if data == filter_value:
                    return 0
                return 1
            
            token = tokens.pop(0)
            
            if isinstance(data, dict):
                #go through every key, value pair in dict and match the current token from the path
                for key, value in data.items():
                    if _match_token(key, token):
                        #put in extra function
                        return_code = _recursive_delete(value, tokens.copy())
                        if return_code == 1:
                            return data
                        elif return_code != 0 and return_code != None:
                            print("TODO")
                            #FIXME what happenes if the element shouldnt be removed from a list?
                            
            elif isinstance(data, list):
                for item in list(data):
                    #put in extra function because should be same as this!
                    return_code = _recursive_delete(item, tokens.copy())
                    if return_code == 1:
                            return data
                    elif return_code != 0 and return_code != None:
                        data.remove(return_code)
        
        
        def _match_token(key, token):
            #check if numeric key
            if token == '{n}':
                return isinstance(key, int) or key.isdigit()
            else:
                #check for exact key in dict.
                return key == token
            
        #split path into tokens separated by dots.
        tokens = path.split('.')
        return _recursive_delete(data, tokens)
    
    def apply(self: Self, data: dict | list):
        #FIXME what does apply do?
        #FIXME is path + selector mixing actually working?
        selection = self._extract(data, self.selector + '.' + self.path, self.value)
        return data
        #FIXME
        #able to extract the correct filtered values
        #how to create full filtered_data object

class WorkflowInput:
    """
    When a workflow gets executed, it gets input data. For
    instance, the "after event save"-workflow gets a dictionary
    containing the event that was saved.

    Additionally, filters can be added by modules. That way,
    subsequent modules will only see a filtered subset
    of the workflow data. This operation can be undone.

    Filters are expressed using [`Filter`][mmisp.workflows.input.Filter]
    class.
    """

    user: "User"
    """
    Represents the user execution a workflow. Is a system
    user with all privileges. Mostly useful for logging
    purposes.
    """

    workflow: "Workflow"
    """
    Reference to the workflow object being executed.
    """

    filters: list[Filter]

    def __init__(self: Self, data: RoamingData, user: "User", workflow: "Workflow") -> None:
        self.__unfiltered_data = data
        self.user = user
        self.workflow = workflow
        self.filters = []

    @property
    def data(self: Self) -> RoamingData | List[RoamingData]:
        """
        Returns either all of the data given to the workflow input
        OR a list with filter results if a filter was added
        using [`WorkflowInput.add_filter`][mmisp.workflows.input.WorkflowInput.add_filter].
        """
        return self.__unfiltered_data

    def add_filter(self: Self, filter: Filter) -> None:
        """
        Adds another [`Filter`][mmisp.workflows.input.Filter]
        to the workflow input.

        Arguments:
            filter: Filter to be added.
        """

        self.filters.append(filter)

    def reset_filters(self: Self) -> None:
        """
        Removes all filters from the workflow input.
        [`WorkflowInput.data`][mmisp.workflows.input.WorkflowInput.data]
        will contain all of the data it has instead of a
        filtered portion now.
        """
        self.filters = []
