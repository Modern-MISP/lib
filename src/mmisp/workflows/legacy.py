"""
All other modules intended to be agnostic of old legacy MISP formats
as much as possible and can be refactored gradually into a more reasonable
structure.

This is the compat-layer with legacy MISP: it understands the old JSON and
imports/exports that into the new data structure.
"""

import json
import re
from uuid import UUID
from typing import Dict, Any

from sqlalchemy.types import UserDefinedType
from ..workflows import (
    Graph,
    Node,
    Apperance,
    Frame,
    WorkflowGraph,
    GraphValidationResult,
)
from .modules import Trigger, ModuleRegistry, ModuleConfiguration, Overhead
from .execution import Filter, Operator

INPUT_OUTPUT_NAME_PATTERN = re.compile("^(?:input|output)_(?P<num>[\\d]+)")


class GraphValidation:

    """
    This class checks whether a graph is valid or not.
    """

    @classmethod
    def report(cls, result: GraphValidationResult) -> Dict[str, Any]:
        """
        Reports the results of the graph validation.
        Returns a dictionary with the results.

        :param result: GraphValidationResult object containing the results of the graph validation.
        """
        assert False


class GraphFactory:

    """
    This class is responsible for creating a MMSIP graph object from the legacy MISP JSON format.
    The class can also convert a graph in the legacy MISP JSON format from the DB to a modern graph
    object.
    """

    @classmethod
    def graph2jsondict(cls, graph: Graph) -> Dict[str, Any]:
        """
        Converts a modern MISP graph object to a graph in the legacy MISP JSON format used in the DB.

        :param graph: Graph object to convert to JSON.
        """
        assert False

    @classmethod
    def jsondict2graph(cls, input: Dict[str, Any]) -> Graph:
        """
        Converts a graph in the legacy MIPS JSON format to a graph object.
        Returns the input graph as a modern MISP graph object.

        :param input: JSON dictionary containing the graph information.
        """
        raw_nodes = {
            int(id_str): data
            for id_str, data in input.items()
            if not id_str.startswith("_frames")
        }
        nodes = {id: cls.__build_node(data) for id, data in raw_nodes.items()}
        frames = {
            id: Frame(
                data["text"], UUID(id), "", [nodes[int(id)] for id in data["nodes"]]
            )
            for id, data in input.get("_frames", {}).items()
        }

        for id, data in raw_nodes.items():
            cls.__resolve_ports(id, data, "input", nodes)
            cls.__resolve_ports(id, data, "output", nodes)

        return WorkflowGraph(nodes, next(iter(nodes.values())), frames.values())

    @classmethod
    def __resolve_ports(
        cls, id: int, data: Dict[str, Any], direction: str, nodes: Dict[int, Node]
    ):
        dir_plural = f"{direction}s"
        for my_port_str, connections in cls.__portlist_to_dict_items(data[dir_plural]):
            my_port = cls.__port_to_num(my_port_str)
            for connection in connections["connections"]:
                port_list = getattr(nodes[id], dir_plural)
                if my_port not in port_list:
                    port_list[my_port] = []
                port_list[my_port].append(
                    (
                        cls.__port_to_num(connection[direction]),
                        nodes[int(connection["node"])],
                    )
                )

    @staticmethod
    def __portlist_to_dict_items(input: Any):
        if input == []:
            return []
        return input.items()

    @staticmethod
    def __port_to_num(name: str) -> int:
        assert (result := INPUT_OUTPUT_NAME_PATTERN.match(name)) is not None
        return int(result.group("num"))

    @classmethod
    def __build_node(cls, input: Dict[str, Any]) -> Node:
        data = input["data"]
        appereance = Apperance(
            pos=tuple(map(float, [input["pos_x"], input["pos_y"]])),
            typenode=False,  # no module in legacy misp that sets this to true 🤷
            cssClass=input.get("class", ""),
            nodeUid=data.get("node_uid"),
        )

        if input["data"].get("module_type") == "trigger":
            return Trigger(
                name=data["name"],
                description=data["description"],
                scope=data["scope"],
                overhead=Overhead.from_int(data["trigger_overhead"]),
                expect_misp_core_format=data["misp_core_format"],
                blocking=data["blocking"],
                inputs={},
                outputs={},
                appereance=appereance,
                raw_data=data,
            )

        module_cls = ModuleRegistry.lookup(data["id"])

        return module_cls(
            inputs={},
            outputs={},
            enable_multiple_edges_per_output=data.get(
                "multiple_output_connection", False
            ),
            on_demand_filter=cls.__build_filter(data.get("saved_filters", {})),
            # FIXME maybe check if version is too old?
            previous_version=data.get("previous_module_version", "?"),
            appereance=appereance,
            configuration=ModuleConfiguration(
                data=dict(data.get("indexed_params", {}))
            ),
        )

    @staticmethod
    def __build_filter(input: Dict[str, Any]) -> Filter | None:
        if input == {} or (
            # These can be empty, bust MUST exist
            (selector := input.get("selector")) is None
            or (value := input.get("value")) is None
            # These must not be empty
            or not (operator := input.get("operator"))
            or not (path := input.get("path"))
        ):
            return None

        return Filter(
            selector=selector,
            value=value,
            operator=Operator.from_str(operator),
            path=path,
        )


class JSONGraphType(UserDefinedType):
    """
    SQLAlchemy type used to store and retrieve graph objects in the database.
    This type handles the conversion between a modern MISP graph object and its JSON
    representation for the compatibility with legacy MISP.
    """
    def get_col_spec(self, **kw):
        """
        Returns the colum specification for the custom SQLAlchemy type in LONGTEXT.

        :param kw: keyword arguments
        """
        return "LONGTEXT"

    def bind_processor(self, dialect):
        """
        Method for processing data before storing it in the database.

        :param dialect: SQLAlchemy dialect being used.
        """
        pass

    def result_processor(self, dialect, coltype):
        """
        Defines how to process data retrieved from the database.
        Converts the JSON string stored in the database back into a graph object
        using the GraphFactory's jsondict2graph method.

        :param dialect: SQLAlchemy dialect being used.
        :param coltype: Type of the column being processed.
        """
        return lambda value: GraphFactory.jsondict2graph(json.loads(value))

    def __to_list(self, x):
        if isinstance(x, dict):
            return x.values()
        else:
            return x
