"""
This module contains subclasses for different node-types,
i.e. triggers and modules and implementations for modules
that were bundled with legacy MISP.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Type, Any, Self, List

from ..db.database import Session
from .graph import Node, ConfigurationError
from .input import Filter, WorkflowInput


class ModuleParamType(Enum):
    """
    This enum provides supported form fields in the visual editor to
    configure a parameter represented by
    [`ModuleParam`][misp.workflows.modules.ModuleParam] for a
    module.
    """

    INPUT = "input"
    HASHPATH = "hashpath"
    TEXTAREA = "textarea"
    SELECT = "select"
    PICKER = "picker"
    CHECKBOX = "checkbox"
    RADIO = "radio"


class Overhead(Enum):
    """
    Represents overhead of a module. That means e.g. how often it will be
    executed on a typical MISP installation.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @classmethod
    def from_int(cls, input: int) -> Self:
        """
        Returns a member of this enum given the int
        representation of the overhead.

        Arguments:
            input: numeric representation of the overhead.
        """
        return cls(input)


@dataclass
class ModuleParam:
    """
    Each module can be configured in the visual editor, e.g. an
    if/else module needs an operator, a value to check against and
    an attribute-path to a the value to check against. All of these
    values are configurable.

    This class represents a single parameter passed to a module.
    """

    id: str
    """
    Identifier for the parameter. Must be unique in the context
    of a single module.
    """

    label: str
    """
    Human-readable label in the visual editor for this parameter.
    """

    kind: ModuleParamType
    """
    Which type of input is expected. Denoted by
    [`ModuleParamType`][misp.workflows.modules.ModuleParamType].
    """

    options: Dict[str, Any]
    """
    Additional options passed to the visual editor. The other
    options are useful for e.g. validation of actual workflow
    inputs. All the other parameters (e.g. placeholder) are
    passed into this dictionary.
    """

    jinja_supported: bool = False
    """
    If `True`, the input from the visual editor for this parameter
    is a jinja2 template. A template gets the
    [`WorkflowInput`][mmisp.workflows.input.WorkflowInput] data
    as input.
    """


ModuleParams = Dict[str, ModuleParam]


@dataclass
class ModuleConfiguration:
    """
    Parameters for a module. If a module defines a textarea with ID
    `foobar` as param, this class expects a dictionary

    ```python
    {
        "foobar": "mytext"
    }
    ```

    These params are defined in the visual editor and thus saved
    together with the module.
    """

    data: Dict[str, Any]
    """
    The dictionaryh containing values for the parameters a module
    needs.
    """

    def validate(self, structure: ModuleParams) -> List[ConfigurationError]:
        """
        Check if the parameters specified here are correct. For e.g. a
        `select`-param with id "foobar", it will be checked if
        `data["foobar"]` is among the options provided by the select.

        Arguments:
            structure: The module param definitions to validate the
            configuration against.
        """


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

    configuration: ModuleConfiguration
    """
    Values for the params required by this module.
    """

    on_demand_filter: Filter | None
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
    See [`Node`][misp.workflows.modules.Node] for more context. Used by e.g. the concurrent
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

    async def initialize(self, db: Session):
        """
        Initializes the parameters for a module. Done in a method
        since that may involve further DB operations.

        Arguments:
            db: SQLAlchemy session
        """

    def is_initialized(self) -> bool:
        """
        Checks if the module was initialized which happens by calling
        [`Module.initialize`][mmisp.workflows.modules.Module.initialize].
        It's expected that the attribute
        `params` will be set by this method.
        """
        return hasattr(self, "params")

    def exec(self, payload: WorkflowInput) -> bool:
        """
        Executes the module using the specific payload given by the workflow that calls
        the execution of the module.
        Execution strongly depends on the type of the module that is executed.

        :param:
            payload: The workflows input for the specific module execution.
        :return:
            A boolean indicating if the execution was successful.
        """


async def initialize_graph_modules(self, db: Session):
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
    be saved.
    """

    overhead: Overhead
    """
    Indicates the expensiveness/overhead of the trigger
    as indicated by the [`Overhead`][mmisp.workflows.modules.Overhead] enum.
    """

    raw_data: Dict[str, Any]
    """
    Dictionary with arbitrary values passed to the visual editor.
    """

    n_inputs: int = 0


class ModuleRegistry:
    """
    Each module implementation can be registered here using the
    `@workflow_module` attribute/annotation.

    That way, modules from other packages can be added to MMISP
    by importing those packages once and giving all
    subclasses the `@workflow_module` annotation.
    """

    modules: Dict[str, Type[Module]] = {}
    """
    List of modules registered by the `@workflow_module` attribute.
    """

    @classmethod
    def lookup(cls, name: str) -> Type[Module]:
        """
        Returns a reference to a module class implementation by
        the ID of the module.

        Arguments:
            name: Name of the module.
        """
        return cls.modules[name]


def workflow_module(cls):
    """
    Annotation that registers the annotated class in the
    [`ModuleRegistry`][misp.workflows.modules.ModuleRegistry].
    That way modules are registered
    in the workflow application.
    """

    if not issubclass(cls, Module):
        raise ValueError(
            f"Class reference {cls} is not a subclass of mmisp.workflows.modules.Module!"
        )
    ModuleRegistry.modules[cls.id] = cls


@workflow_module
@dataclass(kw_only=True)
class ModuleIfGeneric(Module):
    id: str = "generic-if"
    n_outputs: int = 2
    name: str = "IF :: Generic"
    version: str = "0.2"
    description: str = (
        "Generic IF / ELSE condition block. The `then` output will be used if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"


@workflow_module
@dataclass(kw_only=True)
class ModuleEnrichEvent(Module):
    id: str = "enrich-event"
    name: str = "Enrich Event"
    version: str = "0.2"
    description: str = (
        "Enrich all Attributes contained in the Event with the provided module."
    )
    expect_misp_core_format: bool = True


@workflow_module
@dataclass(kw_only=True)
class ModuleAttributeCommentOperation(Module):
    id: str = "Module_attribute_comment_operation"
    version: str = "0.1"
    name: str = "Attribute comment operation"
    description: str = "Set the Attribute's comment to the selected value"
    icon: str = "edit"
    on_demand_filtering_enabled: bool = True


@workflow_module
@dataclass(kw_only=True)
class ModuleTagIf(Module):
    id: str = "tag-if"
    n_outputs: int = 2
    name: str = "IF :: Tag"
    version: str = "0.4"
    description: str = (
        "Tag IF / ELSE condition block. The `then` output will be used if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"


@workflow_module
@dataclass(kw_only=True)
class ModuleStopWorkflow(Module):
    id: str = "stop-execution"
    name: str = "Stop execution"
    version: str = "0.2"
    description: str = (
        "Essentially stops the execution for blocking workflows. Do nothing for non-blocking ones"
    )
    icon: str = "ban"


@workflow_module
@dataclass(kw_only=True)
class ModuleAttachWarninglist(Module):
    id: str = "attach-warninglist"
    name: str = "Add to warninglist"
    description: str = "Append attributes to an active custom warninglist."
    icon: str = "exclamation-triangle"
    on_demand_filtering_enabled: bool = True


@workflow_module
@dataclass(kw_only=True)
class ModuleConcurrentTask(Module):
    id: str = "concurrent-task"
    name: str = "Concurrent Task"
    description: str = (
        "Allow breaking the execution process and running concurrent tasks. You can connect multiple nodes the `concurrent` output."
    )
    icon: str = "random"
    enable_multiple_edges_per_output: bool = True
    html_template: str = "concurrent"


@workflow_module
@dataclass(kw_only=True)
class ModuleCountIf(Module):
    id: str = "count-if"
    name: str = "IF :: Count"
    description: str = (
        "Count IF / ELSE condition block. It counts the amount of entry selected by the provided hashpath. The `then` output will be used if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"


@workflow_module
@dataclass(kw_only=True)
class ModuleDistributionIf(Module):
    id: str = "distribution-if"
    name: str = "IF :: Distribution"
    version: str = "0.3"
    description: str = (
        "Distribution IF / ELSE condition block. The `then` output will be used if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"


@workflow_module
@dataclass(kw_only=True)
class ModuleGenericFilterData(Module):
    id: str = "generic-filter-data"
    name: str = "Filter :: Generic"
    version: str = "0.2"
    description: str = (
        "Generic data filtering block. The module filters incoming data and forward the matching data to its output."
    )
    icon: str = "filter"


@workflow_module
@dataclass(kw_only=True)
class ModuleGenericFilterReset(Module):
    id: str = "generic-filter-reset"
    name: str = "Filter :: Remove filter"
    description: str = "Reset filtering"
    icon: str = "redo-alt"


@workflow_module
@dataclass(kw_only=True)
class ModuleOrganisationIf(Module):
    id: str = "organisation-if"
    name: str = "IF :: Organisation"
    description: str = (
        "Organisation IF / ELSE condition block. The `then` output will be used if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"


@workflow_module
@dataclass(kw_only=True)
class ModulePublishedIf(Module):
    id: str = "published-if"
    name: str = "IF :: Published"
    description: str = (
        "Published IF / ELSE condition block. The `then` output will be used if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"


@workflow_module
@dataclass(kw_only=True)
class ModuleThreatLevelIf(Module):
    id: str = "threat-level-if"
    html_template: str = "if"
    n_outputs: int = 2
    name: str = "IF :: Threat Level"
    version: str = "0.1"
    description: str = (
        "Threat Level IF / ELSE condition block. The `then` output will be used if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"


@workflow_module
@dataclass(kw_only=True)
class ModuleAddEventblocklistEntry(Module):
    id: str = "add_eventblocklist_entry"
    version: str = "0.1"
    name: str = "Add Event Blocklist entry"
    description: str = "Create a new entry in the Event blocklist table"
    icon: str = "ban"


@workflow_module
@dataclass(kw_only=True)
class ModuleAssignCountryFromEnrichment(Module):
    id: str = "assign_country"
    name: str = "IF :: Threat Level"
    version: str = "0.1"
    description: str = (
        "Threat Level IF / ELSE condition block. The `then` output will be used if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2


@workflow_module
@dataclass(kw_only=True)
class ModuleAttachEnrichment(Module):
    id: str = "attach-enrichment"
    name: str = "Attach enrichment"
    version: str = "0.3"
    description: str = "Attach selected enrichment result to Attributes."
    icon: str = "asterisk"
    on_demand_filtering_enabled: bool = True


@workflow_module
@dataclass(kw_only=True)
class ModuleAttributeEditionOperation(Module):
    id: str = "attribute_edition_operation"
    name: str = "Attribute edition operation"
    description: str = "Base module allowing to modify attribute"
    icon: str = "edit"
    expect_misp_core_format: bool = True


@workflow_module
@dataclass(kw_only=True)
class ModuleAttributeIdsFlagOperation(Module):
    id: str = "attribute_ids_flag_operation"
    name: str = "Attribute IDS Flag operation"
    description: str = "Toggle or remove the IDS flag on selected attributes."
    icon: str = "edit"
    on_demand_filtering_enabled: bool = True


@workflow_module
@dataclass(kw_only=True)
class ModuleEventDistributionOperation(Module):
    id: str = "Module_event_distribution_operation"
    name: str = "Event distribution operation"
    description: str = "Set the Event's distribution to the selected level"
    icon: str = "edit"


@workflow_module
@dataclass(kw_only=True)
class ModuleMsTeamsWebhook(Module):
    id: str = "ms-teams-webhook"
    name: str = "MS Teams Webhook"
    version: str = "0.5"
    description: str = (
        'Perform callbacks to the MS Teams webhook provided by the "Incoming Webhook" connector'
    )


@workflow_module
@dataclass(kw_only=True)
class ModulePublishEvent(Module):
    id: str = "publish-event"
    name: str = "Publish Event"
    version: str = "0.1"
    description: str = "Publish an Event in the context of the workflow"
    icon: str = "upload"


@workflow_module
@dataclass(kw_only=True)
class ModulePushZMQ(Module):
    id: str = "push-zmq"
    name: str = "Push to ZMQ"
    version: str = "0.2"
    description: str = "Push to the ZMQ channel"


@workflow_module
@dataclass(kw_only=True)
class ModuleSendLogMail(Module):
    id: str = "send-log-mail"
    name: str = "Send Log Mail"
    description: str = (
        "Allow to send a Mail to a list or recipients, based on a Log trigger. Requires functional misp-modules to be functional."
    )
    icon: str = "envelope"


@workflow_module
@dataclass(kw_only=True)
class ModuleSendMail(Module):
    id: str = "send-mail"
    name: str = "Send Mail"
    description: str = (
        "Allow to send a Mail to a list or recipients. Requires functional misp-modules to be functional."
    )
    icon: str = "envelope"


@workflow_module
@dataclass(kw_only=True)
class ModuleSplunkHecExport(Module):
    id: str = "splunk-hec-export"
    name: str = "Splunk HEC export"
    version: str = "0.2"
    description: str = (
        "Export Event Data to Splunk HTTP Event Collector. Due to the potential high amount of requests, it's recommanded to put this module after a `concurrent_task` logic module."
    )


@workflow_module
@dataclass(kw_only=True)
class ModuleStopExecution(Module):
    id: str = "stop-execution"
    name: str = "Stop execution"
    version: str = "0.2"
    description: str = (
        "Essentially stops the execution for blocking workflows. Do nothing for non-blocking ones"
    )
    icon: str = "ban"
    n_outputs: int = 0


@workflow_module
@dataclass(kw_only=True)
class ModuleTagOperation(Module):
    id: str = "tag_operation"
    name: str = "Tag operation"
    description: str = "Add or remove tags on Event or Attributes."
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.2"


@workflow_module
@dataclass(kw_only=True)
class ModuleTagReplacementGeneric(Module):
    id: str = "tag_replacement_generic"
    name: str = "Tag Replacement Generic"
    description: str = "Attach a tag, or substitue a tag by another"
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.1"


@workflow_module
@dataclass(kw_only=True)
class ModuleTagReplacementPap(Module):
    id: str = "tag_replacement_pap"
    name: str = "Tag Replacement - PAP"
    description: str = (
        "Attach a tag (or substitue) a tag by another for the PAP taxonomy"
    )
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.1"


@workflow_module
@dataclass(kw_only=True)
class ModuleTagReplacementTlp(Module):
    id: str = "tag_replacement_tlp"
    name: str = "Tag Replacement - TLP"
    version: str = "0.1"
    description: str = (
        "Attach a tag (or substitue) a tag by another for the TLP taxonomy"
    )
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True


@workflow_module
@dataclass(kw_only=True)
class ModuleTelegramSendAlert(Module):
    id: str = "telegram-send-alert"
    name: str = "Telegram Send Alert"
    version: str = "0.1"
    description: str = "Send a message alert to a Telegram channel"


@workflow_module
@dataclass(kw_only=True)
class ModuleWebhook(Module):
    id: str = "webhook"
    name: str = "Webhook"
    version: str = "0.7"
    description: str = "Allow to perform custom callbacks to the provided URL"
