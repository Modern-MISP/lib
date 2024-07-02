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
    IN_OR = "in_or" #FIXME what does this do?

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
            return value != None
        return False
    
    def _remove_not_matching_data(self: Self, data: RoamingData, path: str) -> None:
        """
        removes values from dictionary on  given cakePHP hash path that dont match 
        the filter values and the filter operator

        Args:
            data (dict or list): The input data from which to extract values.
            path (str): The path string specifying which values to extract.

        """

        def _recursive_delete(data: RoamingData | list, tokens: list) -> Any:
            """
            Recursive helper method for deleting non matching values from the dictionary.
            If a non-matching value is found in the last recursion layer, this is returned
            to the layer before that with the status "no_match". This layer then returns the
            current data object for the 3rd last recursion layer to remove the non-matching value
            from the dictionary.
            """

            
            if not tokens:
                #path destination and last recursion layer
                #compare the found value in the dict with the given value from the filter
                #using the operator from the filter.
                if self.match_value(data):
                    return "match"
                return "no_match"
            
            token = tokens.pop(0)
            
            if isinstance(data, dict):
                #go through every key, value pair in dict and match the current token from the path
                for key, value in dict(data).items():
                    if _match_token(key, token):
                        
                        return_code = _recursive_delete(value, tokens.copy())
                        if return_code == "no_match":
                            return data
                        elif return_code != "match" and return_code != None:
                                                        
                            for key, value in dict(data).items():
                                if return_code == value:
                                    del data[key]
                            
            elif isinstance(data, list):
                for item in list(data):
                    
                    return_code = _recursive_delete(item, tokens.copy())
                    if return_code == "no_match":
                        return data
                    elif return_code != "match" and return_code != None:
                        data.remove(return_code)
        
        
        def _match_token(key: str | int, token: str):
            #check if numeric key
            if token == '{n}':
                return isinstance(key, int) or key.isdigit()
            else:
                #check for exact key in dict.
                return key == token
            
        #split path into tokens separated by dots.
        tokens = path.split('.')
        _recursive_delete(data, tokens)
    
    def apply(self: Self, data: RoamingData) -> RoamingData:

        self._remove_not_matching_data(data, self.selector + '.' + self.path)
        return data
    
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
    __filtered_data: list[RoamingData]

    def __init__(self: Self, data: RoamingData, user: "User", workflow: "Workflow") -> None:
        self.__unfiltered_data = data
        self.__filtered_data = []
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

        if len(self.filters) == 0:
            return self.__unfiltered_data

        return self.__filtered_data

    def filter(self: Self) -> None:

        for filter in self.filters:
            current_filter_data = filter.apply(self.__unfiltered_data.copy())
            self.__filtered_data.append(current_filter_data)

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
