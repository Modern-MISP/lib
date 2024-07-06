"""
All other modules intended to be agnostic of old legacy MISP formats
as much as possible and can be refactored gradually into a more reasonable
structure.

This is the compat-layer with legacy MISP: it understands the old JSON and
imports/exports that into the new data structure.
"""

import json
import re
from typing import Any, Dict, Iterable, List, Self, Type
from uuid import UUID

from sqlalchemy.types import UserDefinedType

from .graph import (
    Apperance,
    Frame,
    Graph,
    GraphValidationResult,
    Module,
    Node,
    NodeConnection,
    Trigger,
    WorkflowGraph,
)
from .input import Filter, Operator
from .modules import MODULE_REGISTRY, TRIGGER_REGISTRY, ModuleAction, ModuleConfiguration, ModuleLogic

INPUT_OUTPUT_NAME_PATTERN = re.compile("^(?:input|output)_(?P<num>[\\d]+)")

EMPTY_FILTER = {
    "operator": "",
    "path": "",
    "selector": "",
    "value": "",
}


class GraphValidation:
    """
    This class checks whether a graph is valid or not.
    """

    @classmethod
    def report(cls: Type[Self], result: GraphValidationResult) -> Dict[str, Any]:
        """
        Reports the results of the graph validation.
        Returns a dictionary with the results.

        Arguments:
            result:     GraphValidationResult object containing the results of the graph validation.
        """
        assert False


class GraphFactory:
    """
    This class is responsible for creating a MMSIP graph object from the legacy MISP JSON format.
    The class can also convert a graph in the legacy MISP JSON format from the DB to a modern graph
    object.
    """

    @classmethod
    def graph2jsondict(cls: Type[Self], graph: Graph) -> Dict[str, Any]:
        """
        Converts a modern MISP graph object to a graph in the legacy MISP JSON format used in the DB.

        Arguments:
            graph:  Graph object to convert to JSON.
        """
        reverse_edge_list = {id(node): str(local_id) for local_id, node in graph.nodes.items()}

        nodes = {
            str(local_id): cls.__node_to_dict(local_id, node, reverse_edge_list)
            for local_id, node in graph.nodes.items()
        }

        frames = graph.frames
        if len(list(frames)) > 0:
            nodes["_frames"] = {
                str(frame.uuid): {
                    "id": str(frame.uuid),
                    "text": frame.text,
                    "class": frame.clazz,
                    "nodes": [reverse_edge_list[id(node)] for node in frame.nodes],
                }
                for frame in frames
            }

        return nodes

    @classmethod
    def __node_to_dict(cls: Type[Self], id: int, node: Node, reverse_edge_list: Dict[int, str]) -> Dict[str, Any]:
        match node:
            case Trigger(
                inputs={},
                outputs=outputs,
                apperance=Apperance((pos_x, pos_y), typenode, css_class, node_uid),
                name=name,
                n_inputs=0,
                n_outputs=n_outputs,
                id=trigger_id,
                scope=scope,
                description=description,
                blocking=blocking,
                overhead=overhead,
                overhead_message=overhead_message,
                version=version,
                enable_multiple_edges_per_output=multiple_output_connection,
                icon=icon,
                disabled=disabled,
            ):
                ret_val: Dict = {
                    "id": id,
                    "data": {
                        "id": trigger_id,
                        "scope": scope,
                        "name": cls.__normalize_legacy_string(name),
                        "description": cls.__normalize_legacy_string(description),
                        "inputs": 0,
                        "outputs": n_outputs,
                        "misp_core_format": True,
                        "expect_misp_core_format": False,
                        "blocking": blocking,
                        "trigger_overhead": overhead.value,
                        "trigger_overhead_message": overhead_message,
                        "version": version,
                        "multiple_output_connection": multiple_output_connection,
                        "module_type": "trigger",
                        "html_template": "trigger",
                        "icon": icon,
                        "disabled": disabled,
                        # MISP module is not implemented.
                        "is_misp_module": False,
                        "is_custom": False,
                        "icon_class": "",
                    },
                    "class": css_class,
                    "typenode": typenode,
                    "inputs": [],
                    "outputs": cls.__edges_to_json("output", outputs, reverse_edge_list, n_outputs),
                    "pos_x": cls.__maybe_int(pos_x),
                    "pos_y": cls.__maybe_int(pos_y),
                }

                # So far, this was relatively straight-forward. Now let's tackle a
                # few corner-cases for the old garbage 🤡

                # saved_filters are super inconsistent. It's either EMPTY_FILTER from legacy.py
                # or
                # [
                #    { text: selector, value: ''} {text: value, value: ''}
                #    {text: operator, value: ''} {text: path, value: ''}
                # ]
                # and I have not idea which one is correct when.
                # For now, I'm not aware of filters being attached to triggers, so let's leave this
                # for now 🤷
                ret_val["data"]["saved_filters"] = EMPTY_FILTER
                ret_val["data"]["support_filters"] = False

                # node_uid is only set if it has a value. But it can be empty.
                if node_uid is not None:
                    ret_val["data"]["node_uid"] = node_uid

                if len(reverse_edge_list) > 1:
                    # Non-newly created workflow names have
                    # `+` instead of spaces.
                    ret_val["name"] = cls.__normalize_legacy_string(name)

                    # Also, a version and an empty list `indexed_params`
                    # (as opposed to `params`) exists.
                    ret_val["data"]["module_version"] = version
                    ret_val["data"]["indexed_params"] = []

                    # So far I haven't seen a versioned trigger, so let's
                    # hardcode it that way for now.
                    ret_val["data"]["previous_module_version"] = version
                else:
                    # Newly created workflows appear to have a non-normalized
                    # description and name, i.e. w/o spaces being replaced by `+`.
                    ret_val["data"]["description"] = description
                    ret_val["data"]["name"] = name
                    # Also these appear to have an empty list `params`.
                    ret_val["data"]["params"] = []

                return ret_val
            case Module(
                inputs=inputs,
                outputs=outputs,
                apperance=Apperance((pos_x, pos_y), typenode, cssClass, node_uid),
                name=name,
                id=module_id,
                version=version,
                previous_version=previous_version,
                configuration=configuration,
                enable_multiple_edges_per_output=multiple_output_connection,
                on_demand_filter=filter,
                n_inputs=n_inputs,
                n_outputs=n_outputs,
            ):
                name_escaped = cls.__normalize_legacy_string(name)

                match node:
                    case ModuleAction():
                        module_type = "action"
                    case ModuleLogic():
                        module_type = "logic"
                    case _:
                        raise ValueError(f"Module {node} must inherit either ModuleAction or ModuleLogic!")

                return {
                    "id": id,
                    "name": name_escaped,
                    "data": {
                        "id": module_id,
                        "indexed_params": [] if configuration.data == {} else configuration.data,
                        "saved_filters": {
                            "operator": filter.operator.value,
                            "selector": filter.selector,
                            "path": filter.path,
                            "value": filter.value,
                        }
                        if filter is not None
                        else EMPTY_FILTER,
                        "name": name_escaped,
                        "multiple_output_connection": multiple_output_connection,
                        "previous_module_version": previous_version,
                        "module_version": version,
                        "node_uid": node_uid,
                        "module_type": module_type,
                    },
                    "class": cssClass,
                    "typenode": typenode,
                    "inputs": cls.__edges_to_json("input", inputs, reverse_edge_list, n_inputs),
                    "outputs": cls.__edges_to_json("output", outputs, reverse_edge_list, n_outputs),
                    "pos_x": cls.__maybe_int(pos_x),
                    "pos_y": cls.__maybe_int(pos_y),
                }
            case _:
                raise ValueError(f"Unexpected node representation: {node}")

    @classmethod
    def __normalize_legacy_string(cls: Type[Self], val: str) -> str:
        # For reasons I'm not aware of, some of the descriptions and names
        # have a special normalisation in legacy MISP, i.e. spaces
        # are escaped with `+`.

        # FIXME double-check if anything else also gets escaped.
        return val.replace(" ", "+")

    @classmethod
    def __maybe_int(cls: Type[Self], value: float) -> int | float:
        if round(value) == value:
            return int(value)
        return value

    @classmethod
    def __edges_to_json(
        cls: Type[Self],
        direction: str,
        edges: Dict[int, List[NodeConnection]],
        reverse_edge_list: Dict[int, str],
        expected_num: int,
    ) -> Dict[str, Any] | List[None]:
        assert direction in ["output", "input"]
        opposite = "input" if direction == "output" else "output"

        if expected_num == 0:
            assert len(edges) == 0
            # empty input/output lists are a list instead of a dict because in PHP
            # both have the same underlying datatype and the json_encode transforms
            # an empty array into [].
            return []

        result = {
            f"{direction}_{n}": {
                "connections": [
                    {
                        "node": reverse_edge_list[id(connected_node)],
                        direction: f"{opposite}_{connected_input}",
                    }
                    for connected_input, connected_node in edge_elems
                ]
            }
            for n, edge_elems in edges.items()
        }

        # if no connections exist, but >0 outputs are defined, the JSON
        # representation contains the inputs/outputs, but with
        # connections being empty.
        if result == {}:
            return {f"{direction}_{i}": {"connections": []} for i in range(1, expected_num + 1)}

        return result

    @classmethod
    def jsondict2graph(cls: Type[Self], input: Dict[str, Any]) -> Graph:
        """
        Converts a graph in the legacy MIPS JSON format to a graph object.
        Returns the input graph as a modern MISP graph object.

        Arguments:
            input: JSON dictionary containing the graph information.
        """
        raw_nodes = {int(id_str): data for id_str, data in input.items() if not id_str.startswith("_frames")}
        nodes = {id: cls.__build_node(data) for id, data in raw_nodes.items()}
        frames = {
            id: Frame(data["text"], UUID(id), "", [nodes[int(id)] for id in data["nodes"]])
            for id, data in input.get("_frames", {}).items()
        }

        for id, data in raw_nodes.items():
            cls.__resolve_ports(id, data, "input", nodes)
            cls.__resolve_ports(id, data, "output", nodes)

        return WorkflowGraph(nodes, next(iter(nodes.values())), frames.values())

    @classmethod
    def __resolve_ports(
        cls: Type[Self], id: int, data: Dict[str, Any], direction: str, nodes: Dict[int, Module | Trigger]
    ) -> None:
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
    def __portlist_to_dict_items(input: Any) -> List[Any]:
        if input == []:
            return []
        return input.items()

    @staticmethod
    def __port_to_num(name: str) -> int:
        assert (result := INPUT_OUTPUT_NAME_PATTERN.match(name)) is not None
        return int(result.group("num"))

    @classmethod
    def __build_node(cls: Type[Self], input: Dict[str, Any]) -> Module | Trigger:
        data = input["data"]
        apperance = Apperance(
            pos=tuple(map(float, [input["pos_x"], input["pos_y"]])),  # type:ignore[arg-type]
            typenode=False,  # no module in legacy misp that sets this to true 🤷
            cssClass=input.get("class", ""),
            nodeUid=data.get("node_uid"),
        )

        if input["data"].get("module_type") == "trigger":
            trigger_cls = TRIGGER_REGISTRY.lookup(data["id"])
            return trigger_cls(  # type:ignore[call-arg]
                inputs={},
                outputs={},
                apperance=apperance,
                disabled=data.get("disabled", False),
                overhead_message=data.get("trigger_overhead_message", ""),
            )

        module_cls = MODULE_REGISTRY.lookup(data["id"])

        return module_cls(  # type:ignore[call-arg]
            inputs={},
            outputs={},
            enable_multiple_edges_per_output=data.get("multiple_output_connection", False),
            on_demand_filter=cls.__build_filter(data.get("saved_filters", {})),
            # FIXME maybe check if version is too old?
            previous_version=data.get("previous_module_version", "?"),
            version=data.get("module_version", module_cls.__dict__.get("version", "0.0")),
            apperance=apperance,
            configuration=ModuleConfiguration(data=dict(data.get("indexed_params", {}))),
        )

    @staticmethod
    def __build_filter(input: Dict[str, Any]) -> Filter | None:
        if input == {} or (
            # These can be empty, but MUST exist
            (selector := input.get("selector")) is None
            or (value := input.get("value")) is None
            or (path := input.get("path")) is None
            # These must not be empty
            or not (operator := input.get("operator"))
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

    def get_col_spec(self: Self, **kw) -> str:
        """
        Returns the colum specification for the custom SQLAlchemy type in LONGTEXT.
        """
        return "LONGTEXT"

    def bind_processor(self: Self, dialect: Any):  # ignore:type[override] # noqa: ANN201
        """
        Method for processing data before storing it in the database.

        Arguments:
            dialect:    SQLAlchemy dialect being used.
        """
        return lambda value: json.dumps(GraphFactory.graph2jsondict(value))

    def result_processor(self: Self, dialect: Any, coltype: Any):  # ignore:type[override] # noqa: ANN201
        """
        Defines how to process data retrieved from the database.
        Converts the JSON string stored in the database back into a graph object
        using the GraphFactory's jsondict2graph method.

        Arguments:
            dialect:    SQLAlchemy dialect being used.
            coltype:    Type of the column being processed.
        """
        return lambda value: GraphFactory.jsondict2graph(json.loads(value))

    def __to_list(self: Self, x: Dict[str, Any] | List[Any]) -> Iterable[Any]:
        if isinstance(x, dict):
            return x.values()
        else:
            return x
