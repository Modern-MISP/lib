"""
Data structure for the payload passed to the workflow and
filtering mechanism associated with it.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Self, Type
import copy

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

    @classmethod
    def from_str(cls: Type[Self], input: str) -> Self:
        """
        Returns a member of this enum given the string
        representation of the operator.

        Arguments:
            input: string representation of the operator.
        """
        return cls(input)


class FilterError(Exception):
    """
    Abstract class representing possible invalid Filter inputs
    """


@dataclass
class InvalidSelectionError(FilterError):
    """
    If the selection passed to the filter is invalid this error is returned.
    Examples for invalid selections are datatypes other from String, hashpahts,
    that dont lead to a list or empty strings
    """

    message: str


@dataclass
class InvalidPathError(FilterError):
    """
    If the path passed to the filter is invalid this error is returned.
    e.g.: empty String
    """

    message: str


@dataclass
class InvalidOperationError(FilterError):
    """
    If the operation passed to the filter is invalid this error is returned.
    e.g.: Operation.to_str fails to return a valid operation.
    """

    message: str


@dataclass
class InvalidValueError(FilterError):
    """
    If the value passed to the filter is invalid this error is returned.
    e.g.: input not of type str or List[str]
    """

    message: str


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
    MMSIP filter currently only support limited hash path functionality.
    
    **NOTE**
    Supported features are the dot-separated paths consisting of keys and
    '{n}' indicating iterating over a list or a dictionary with numeric keys.

    Additional hash path functionality such as Matchers could be added to MMISP later.
    """

    path: str
    """
    Attribute path in the list where each item will be
    checked against `value` using operation `operator`.
    """

    operator: Operator
    """
    [`Operator`][mmisp.workflows.input.Operator] to compare
    the item below `path` against `value`.
    """

    value: str | List[str]
    """
    Value to compare against. Can be a list for operations
    `in`/`not_in` or a string value for `equals`/etc..
    """

    def match_value(self: Self, value: Any) -> bool:
        """
        Check if a value matches a filter.

        Arguments:
            value: The value to check.
            filter: The filter to match against.

        Returns:
            True if the value matches the filter, False otherwise.
        """

        value_str = str(value)

        if self.operator == Operator.EQUALS:
            return value_str == self.value
        elif self.operator == Operator.NOT_EQUALS:
            return value_str != self.value
        elif self.operator == Operator.IN:
            return value_str in self.value if isinstance(self.value, list) else False
        elif self.operator == Operator.NOT_IN:
            return value_str not in self.value if isinstance(self.value, list) else False
        elif self.operator == Operator.ANY_VALUE:
            return value != None
        return False

    def _match_token(self: Self, key: str | int, token: str) -> bool:
        # check if numeric key
        if token == "{n}":
            return isinstance(key, int) or key.isdigit()
        else:
            # check for exact key in dict.
            return key == token

    def _extract_selection(self: Self, data: RoamingData | List[RoamingData]) -> List[RoamingData]:
        """
        Extracts values from a nested dictionary based selector (cakePHP hash path).
        Returns a list of extracted values.

        Args:
            data (dict or list): The input data from which to extract values.
            path (str): The path string specifying which values to extract.

        """

        path = self.selector
        results = []

        def _recursive_extract(data: RoamingData, tokens: List[str]) -> None:
            """
            Recursive helper method for extracting values based on tokens.
            """

            if not tokens and not isinstance(data, list):
                results.append(data)
                return
            elif not tokens and isinstance(data, list):
                raise InvalidSelectionError("Path does not lead to a valid selection.")

            token = tokens.pop(0)
            match = False

            if isinstance(data, dict):
                for key, value in data.items():
                    if self._match_token(key, token):
                        match = True
                        _recursive_extract(value, tokens.copy())

                if not match:
                    raise InvalidSelectionError("Path does not lead to a valid selection.")
            elif isinstance(data, list) and token == "{n}":
                for item in data:
                    _recursive_extract(item, tokens.copy())

            else:
                raise InvalidSelectionError("Path does not lead to a valid selection.")

        tokens = path.split(".")

        _recursive_extract(data, tokens)

        if len(results) == 1 and (isinstance(results[0], list)):
            return results[0]
        return results

    def _remove_not_matching_data(
        self: Self, selection: RoamingData | List[RoamingData], data: RoamingData | List[RoamingData], path: str
    ) -> None:
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
                # path destination and last recursion layer
                # compare the found value in the dict with the given value from the filter
                # using the operator from the filter.
                if self.match_value(data):
                    return "match"
                return "no_match"

            token = tokens.pop(0)

            if isinstance(data, dict):
                key_found = False
                # go through every key, value pair in dict and match the current token from the path
                for key, value in dict(data).items():
                    if self._match_token(key, token):
                        key_found = True
                        return_code = _recursive_delete(value, tokens.copy())
                        if return_code == "no_match":
                            return data
                        elif return_code != "match" and return_code != None:
                            for key, value in dict(data).items():
                                if return_code == value:
                                    del data[key]

                if self.operator == Operator.ANY_VALUE and not key_found:
                    return data

            elif isinstance(data, list) and token == "{n}":
                for item in list(data):
                    return_code = _recursive_delete(item, tokens.copy())
                    if return_code == "no_match":
                        return data
                    elif return_code != "match" and return_code != None:
                        data.remove(return_code)

        # split path into tokens separated by dots.

        tokens = path.split(".")
        return_code = _recursive_delete(data, tokens)
        if return_code != None:
            if isinstance(selection, list):
                selection.remove(return_code)
            elif isinstance(selection, dict):
                for key, value in dict(selection).items():
                    if return_code == value:
                        del selection[key]

    def apply(self: Self, data: RoamingData) -> RoamingData | List[RoamingData]:
        selection = self._extract_selection(data)
        selection_copy = selection.copy()

        for item in selection_copy:
            self._remove_not_matching_data(selection, item, self.path)

        return selection

    def validate(self: Self) -> None:
        # check selection

        if self.selector == "":
            raise InvalidSelectionError("empty selection")

        # check path
        if self.path == "":
            raise InvalidPathError("empty path")

        # check operator
        if not isinstance(self.operator, Operator):
            raise InvalidOperationError("invalid operator")

        # check value
        if self.operator in [Operator.IN, Operator.NOT_IN]:
            if not isinstance(self.value, list):
                raise InvalidValueError("incorrect type")

        elif self.operator == Operator.ANY_VALUE:
            if self.value != "":
                raise InvalidValueError("any value operator does not accept a value")

        return None


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

    def __init__(self: Self, data: RoamingData, user: "User", workflow: "Workflow") -> None:
        self.__unfiltered_data = data
        self.__filtered_data: list = None
        self.user = user
        self.workflow = workflow
        self.filters: List[Filter] = []

    @property
    def data(self: Self) -> RoamingData | List[RoamingData]:
        """
        Returns either all of the data given to the workflow input
        OR a list with filter results if a filter was added
        using [`WorkflowInput.add_filter`][mmisp.workflows.input.WorkflowInput.add_filter].
        """

        if len(self.filters) == 0:
            return self.__unfiltered_data

        if self.__filtered_data == None:
            self.__filtered_data = []
            self.filter()

        return self.__filtered_data

    def filter(self: Self) -> None:
        filter_data = copy.deepcopy(self.__unfiltered_data)

        for i, filter in enumerate(self.filters):
            if i == 0:
                filter_data = filter.apply(filter_data)
            else:
                filter_data = filter.apply(filter_data[-1])

            self.__filtered_data.append(filter_data)

    def add_filter(self: Self, filter: Filter) -> None:
        """
        Adds another [`Filter`][mmisp.workflows.input.Filter]
        to the workflow input.

        Arguments:
            filter: Filter to be added.
        """

        filter.validate()

        self.filters.append(filter)
        self.filtered_data = None

    def reset_filters(self: Self) -> None:
        """
        Removes all filters from the workflow input.
        [`WorkflowInput.data`][mmisp.workflows.input.WorkflowInput.data]
        will contain all of the data it has instead of a
        filtered portion now.
        """
        self.filters = []
