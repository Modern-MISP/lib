"""
This package contains the data-structure representing the workflow graph
and the modules in it.

The sub-packages are specialisations, in this package the basic graph representation
is implemented.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Self, Tuple
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from .input import Filter, WorkflowInput
    from .modules import ModuleConfiguration, Overhead

NodeConnection = Tuple[int, "Node"]


@dataclass
class Apperance:
    """
    Value object with attributes that are only used in the visual editor.
    """

    pos: Tuple[float, float]
    """
    Tuple with x/y coordinates in the canvas where the current node is displayed.
    """

    typenode: bool
    """
    Unclear what exactly that is. Hardcoded to `False` for now since it's like this everywhere.
    """

    cssClass: str
    """
    CSS classes that the current node has in the visual editor.
    """

    nodeUid: str | None
    """
    Unique ID in the DOM set by the visual editor. Sometimes it's apparently `None` for
    unknown reasons.
    """


class GraphError(ABC):
    """
    Abstract base-class for validation errors in the graph structure. The idea is to
    display error kinds via

    ```python
    match error:
        case CyclicGraphError(path):
            pass
        case MultipleEdgesPerOutput(affected):
            pass
        # ...
    ```
    """


@dataclass
class CyclicGraphError(GraphError):
    """
    If a cycle was found in the graph it is invalid. This class represents that error.
    """

    cycle_path: List[Tuple["Node", "Node"]]
    """
    List of edges (from, to) that create a cycle.
    """


@dataclass
class MultipleEdgesPerOutput(GraphError):
    """
    A [`Node`][mmisp.workflows.graph.Node] has multiple inputs and outputs. Unless
    explicitly allowed, each output may only have a single connection to another node.
    An example for that is [`ModuleConcurrentTask`][mmisp.workflows.modules.ModuleConcurrentTask].

    This class represents the error if that's not allowed.
    """

    affected: Tuple["Node", List["Node"]]
    """
    All edges affected by the problem: first component of the tuple
    is the node with too many connections per output, the second component is a list
    of all nodes connected to this output.
    """


class MissingTrigger(GraphError):
    """
    Each workflow that isn't a blueprint must have a trigger as starting node.
    A violation of that is described with this class.

    !!! note
        Incidentally, in legacy MISP this isn't part of `checkGraph`, but
        only used in the validation rules of the `Workflow` model.

        In MMISP, both validations are unified.
    """


@dataclass
class UnsupportedWorkflow(GraphError):
    """
    Not all modules are implemented in modern MISP. All of them exist though
    to allow reading any workflow JSON here.

    If a workflow relies on unsupported modules, this error class is used.
    """

    module: str
    """
    ID of the unsupported module
    """


@dataclass
class ConfigurationError(GraphError):
    """
    Generic "configuration error" class. Useful to e.g. reject wrong parameters
    from the visual editor.
    """

    node: "Node"
    """
    Reference to the misconfigured node.
    """

    context: str
    """
    Error message.
    """


@dataclass
class PathWarning:
    """
    The `checkGraph` endpoint also allows to warn about workflow configurations. These
    are non-fatal. Right now this is only used if blocking nodes are used in a non-blocking
    context.

    Other uses may be e.g.
    * "expensive" configurations: blocking workflows are executed synchronously and
      modules in such a workflow shouldn't take too long.

    !!! note
        There are three node IDs in the legacy MISP variant. It seems as if
        the `to` node is used twice there.
    """

    from_: "Node"
    """
    Node the blocking node is connected with.
    """

    to: "Node"
    """
    Blocking node called within a non-blocking context.
    """

    message: str
    """
    Warning text.
    """

    blocking: bool
    """
    Whether the current module is blocking.
    """


@dataclass
class GraphValidationResult:
    """
    Accumulator for all validation results. The idea is to run graph-level checks such
    as cycle-detection in [`Graph.check`][mmisp.workflows.graph.Graph.check] and then run node-level
    checks in [`Node.check`][mmisp.workflows.graph.Node.check]. Whenever an error is encountered, it's
    added into this class.
    """

    errors: List[GraphError]
    """
    Fatal errors in the workflow graph. The graph is unusable like this.
    """

    warnings: List[PathWarning]
    """
    Warnings about the workflow graph. Non-fatal.
    """

    def add_result(self: Self, other: Self) -> None:
        """
        Merges another validation result into this accumulator object.

        Arguments:
            other: Another validation result added in here.
        """

    def is_valid(self: Self) -> bool:
        """
        If neither errors nor warnings are added, the graph is valid.
        """
        return self.errors == [] and self.warnings == []


@dataclass(kw_only=True)
class Node(ABC):
    """
    A single node in a graph. Can be a trigger - something that caused the workflow run -
    or a module - a behavioral component in the workflow graph.

    Inputs & outputs can be thought of like a layer 4 address where the node is the
    address and the input/output is the port number. So an edge doesn't just connect
    two nodes together, but tuples of `(output number, input)` and
    `(input number, output)`. This is needed because

    * The concurrent execution requires just a single output, but with multiple edges
      to other modules from it.
    * An If/Else module has two outputs: one node to execute if the condition is
      true and one if it isn't.

    It might've been possible to infer outputs by the order of the connections, but this
    would've lead to ambiguity because

    * If >1 module is connected to this module, it's not clear whether there are multiple
      connections leaving the same output (as in the concurrency module) or if each module
      has its own meaning (as in the if/else module).
    * It's valid to produce an if/else module with only else connecting to another node.
      In that case the first output in the list should actually be encoded as
      second list element since the first is empty.

    Because of that, infering inputs/outputs from the order seemed too error-prone
    and the legacy MISP structure was reused here.
    """

    inputs: Dict[int, List[NodeConnection]]
    """
    References to [`Node`][mmisp.workflows.graph.Node] objects connecting to this
    node. Grouped by the ID of the input.
    """

    outputs: Dict[int, List[NodeConnection]]
    """
    References to [`Node`][mmisp.workflows.graph.Node] objects that are connected to
    this node. Grouped by the ID of the output.

    The data-structure is recursive here (basically a doubly-linked list)
    using references to make walking the graph as easy as possible.
    """

    apperance: Apperance
    """
    Value object with miscellaneous settings for the visual editor.
    """

    n_inputs: int = 1
    """
    Number of _allowed_ inputs. If `inputs` exceeds this, the
    [`Node.check`][mmisp.workflows.graph.Node.check] method will return an error for this.
    """

    n_outputs: int = 1
    """
    Number of _allowed_ outputs. If `outputs` exceeds this, the
    [`Node.check`][mmisp.workflows.graph.Node.check] method will return an error for this.
    """

    def check(self: Self, with_warnings: bool = False) -> GraphValidationResult:
        """
        Checks if the module is correctly configured.

        Arguments:
            with_warnings: whether to also return warnings. Not needed when e.g.
            only persisting the graph.
        """
        assert False


@dataclass(kw_only=True)
class Module(Node):
    """
    A module is a workflow node that is either

    * an action, i.e. performs an operation with an observable effect
    * a logic module, i.e. forwards to a different module based on
      a condition
    * a filter, i.e. manipulates the
      [`WorkflowInput`][mmisp.workflows.input.WorkflowInput].

    A module implementation can be provided by writing a subclass that
    assigns values to at least `id`, `version`, `name`.
    """

    configuration: "ModuleConfiguration"
    """
    Values for the params required by this module.
    """

    on_demand_filter: Optional["Filter"]
    """
    Some modules allow filtering of data internally without modifying
    [`WorkflowInput`][mmisp.workflows.input.WorkflowInput]. The filter
    used for that is defined by this attribute.
    """

    previous_version: str = "?"
    """
    Previously used version of the module.
    """

    id: str
    """
    Unique identifier of the module. To be declared in the
    subclass implementing a concrete module.
    """

    name: str
    """
    Human-readable identifier of the module. To be declared in the
    subclass implementing a concrete module.
    """

    version: str = "0.0"
    """
    Current version of the module. To be declared in the
    subclass implementing a concrete module.
    """

    html_template: str = ""
    """
    HTML template provided by the visual editor to use.
    To be declared in the subclass implementing a concrete module.
    """

    on_demand_filtering_enabled: bool = False
    """
    Whether internal filtering is enabled.
    """

    enable_multiple_edges_per_output: bool = False
    """
    Whether it's OK to have multiple edges going from a single output.
    See [`Node`][mmisp.workflows.graph.Node] for more context. Used by e.g. the concurrent
    tasks module.
    """

    expect_misp_core_format: bool = True
    """
    Whether the workflow JSON is expected to be in the MISP format
    as defined in
    `https://www.misp-standard.org/rfc/misp-standard-core.html`.
    """

    blocking: bool = False
    """
    Whether or not the module is blocking, i.e. can abort the
    workflow if it fails. If it's not blocking and fails,
    execution continues.
    """

    async def initialize(self: Self, db: AsyncSession) -> None:
        """
        Initializes the parameters for a module. Done in a method
        since that may involve further DB operations.

        Arguments:
            db: SQLAlchemy session
        """

    def is_initialized(self: Self) -> bool:
        """
        Checks if the module was initialized which happens by calling
        [`Module.initialize`][mmisp.workflows.modules.Module.initialize].
        It's expected that the attribute
        `params` will be set by this method.
        """
        return hasattr(self, "params")

    def exec(self: Self, payload: "WorkflowInput") -> Tuple[bool, Self | None]:
        """
        Executes the module using the specific payload given by the workflow that calls
        the execution of the module.
        Execution strongly depends on the type of the module that is executed.

        The first component of the tuple indicates whether execution was successful.
        The second component of the tuple is the next node to be executed.

        Since this library allows arbitrarily many inputs & outputs, we cannot infer
        the next module from the success of the execution of this module (relevant for
        e.g. if/else).

        Arguments:
            payload: The workflows input for the specific module execution.
        """
        assert False


@dataclass(kw_only=True)
class Trigger(Node):
    """
    A trigger represents the starting point of a workflow.
    It can have only one output and no inputs. Each trigger
    is represented by this class, the attributes are loaded
    from the DB.

    Legacy MISP provides subclasses for each triggers, but
    since the properties were saved into the database anyways
    and no behavior was added to those classes, the idea was
    dropped entirely in MMISP.
    """

    name: str
    """
    Name of the trigger.
    """

    scope: str
    """
    Scope the trigger operates on. E.g. `event` or `attribute`.
    """

    description: str
    """
    Human-readable description of when the trigger gets executed.
    """

    expect_misp_core_format: bool
    """
    Whether the workflow JSON is expected to be in the MISP format
    as defined in
    `https://www.misp-standard.org/rfc/misp-standard-core.html`.
    """

    blocking: bool
    """
    If the workflow of a blocking trigger fails, the actual
    operation won't be carried out. For instance, if the
    "event before save"-trigger fails, the event will not
    besaved.
    """

    overhead: "Overhead"
    """
    Indicates the expensiveness/overhead of the trigger
    as indicated by the [`Overhead`][mmisp.workflows.modules.Overhead] enum.
    """

    raw_data: Dict[str, Any]
    """
    Dictionary with arbitrary values passed to the visual editor.
    """

    n_inputs: int = 0


@dataclass
class Frame:
    """
    Value object representing a frame in the visual editor. Only for visualization.
    """

    text: str
    """
    Title of the frame
    """

    uuid: UUID
    """
    Unique identifier of the frame. Used by the visual editor.
    """

    clazz: str
    """
    Additional CSS classes for the frame. `class` is a reserved keyword.
    """

    nodes: List[Node]
    """
    List of (references) to nodes that are visually encapsulated in the frame
    in the visual editor.
    """


@dataclass
class Graph(ABC):
    """
    A representation of a workflow graph. Consists of
    """

    nodes: Dict[int, Trigger | Module]
    """
    A list of all nodes inside the graph. Edges are represented by nodes
    having references to other nodes in their
    `inputs`/`outputs`.
    """

    root: Trigger | Module
    """
    Reference to the root of the graph.
    """

    frames: Iterable[Frame]
    """
    List of frame objects in the visual editor.
    """

    @abstractmethod
    def check(self: Self) -> GraphValidationResult:
        """
        Checks if the graph's structure is valid. Works as described in
        [`GraphValidationResult`][mmisp.workflows.graph.GraphValidationResult].
        """

    async def initialize_graph_modules(self: Self, db: AsyncSession) -> None:
        """
        This method is declared in `mmisp.workflows.modules`, but
        is a method of is part of [`Graph`][mmisp.workflows.graph.Graph].
        It injects `db` into each module. This is done to avoid
        circular import situations.

        !!! note
            For now, this is necessary since modules may require other
            objects from the database. E.g. the
            [`ModuleOrganisationIf`][mmisp.workflows.modules.ModuleOrganisationIf]
            loads the names of all organisations.

            There are a few ways forward:

            * Implement a more sophisticated SQLAlchemy type that
              allows to query other entities while placing the JSON
              into the [`Graph`][mmisp.workflows.graph.Graph] structure.

            * Factor the :attribute:`mmisp.workflows.modules.Module.params`
              structure out and inject it into the workflow editor on its own.

            For modernizing legacy MISP's workflows and retaining backwards
            compatibility, just injecting the DB into each node at the
            beginning is the simplest solution though.

        Arguments:
            db: SQLAlchemy DB session.
        """
        for node in self.nodes:
            if isinstance(node, Module):
                await node.initialize(db)
                assert node.is_initialized()


class WorkflowGraph(Graph):
    """
    This graph represents a workflow. That means that it MUST have a trigger as starting
    node and no trigger anywhere else.
    """

    def check(self: Self, with_warnings: bool = False) -> GraphValidationResult:
        assert False


class BlueprintGraph(Graph):
    """
    This graph represents a blueprint. Blueprints are reusable parts of a
    workflow graph and MUST NOT have a trigger.

    Whether that's the case can be enforced with the
    [`BlueprintGraph.check`][mmisp.workflows.graph.BlueprintGraph.check] method.
    """

    def check(self: Self, with_warnings: bool = False) -> GraphValidationResult:
        """
        Custom check method for blueprint graph.
        """
        assert False
