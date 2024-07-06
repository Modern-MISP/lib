"""
This module contains subclasses for different node-types,
i.e. triggers and modules and implementations for modules
that were bundled with legacy MISP.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Generic, List, Self, Type, TypeVar

from .graph import ConfigurationError, Module, Node, Trigger


class ModuleParamType(Enum):
    """
    This enum provides supported form fields in the visual editor to
    configure a parameter represented by
    [`ModuleParam`][mmisp.workflows.modules.ModuleParam] for a
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
    def from_int(cls: Type[Self], input: int) -> Self:
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
    [`ModuleParamType`][mmisp.workflows.modules.ModuleParamType].
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

    def validate(self: Self, structure: ModuleParams) -> List[ConfigurationError]:
        """
        Check if the parameters specified here are correct. For e.g. a
        `select`-param with id "foobar", it will be checked if
        `data["foobar"]` is among the options provided by the select.

        Arguments:
            structure: The module param definitions to validate the
            configuration against.
        """
        assert False


class ModuleAction(Module):
    """
    Marker class representing an action module. Not relevant for the behavior,
    but for the HTTP responses to determine which kind of module this is.
    """


class ModuleLogic(Module):
    """
    Marker class representing a logic module. Not relevant for the behavior,
    but for the HTTP responses to determine which kind of module this is.
    """


T = TypeVar("T", bound="Node")


class NodeRegistry(Generic[T]):
    """
    Each module & trigger implementation can be registered here using the
    `@workflow_node` attribute/annotation.

    That way, modules from other packages can be added to MMISP
    by importing those packages once and giving all
    subclasses the `@workflow_node` annotation.
    """

    modules: Dict[str, Type[T]] = {}
    """
    List of modules registered by the `@workflow_node` attribute.
    """

    def lookup(self: Self, name: str) -> Type[T]:
        """
        Returns a reference to a module class implementation by
        the ID of the module.

        Arguments:
            name: Name of the module or trigger.
        """
        return self.modules[name]


MODULE_REGISTRY = NodeRegistry[Module]()
TRIGGER_REGISTRY = NodeRegistry[Trigger]()


def module_node(cls: Type[Module]) -> Type[Module]:
    """
    Annotation that registers the annotated class in the
    [`NodeRegistry`][mmisp.workflows.modules.NodeRegistry].
    That way modules are registered
    in the workflow application.
    """

    if not issubclass(cls, Module):
        raise ValueError(f"Class reference {cls} is not a subclass of mmisp.workflows.modules.Module!")
    MODULE_REGISTRY.modules[cls.id] = cls

    return cls


def trigger_node(cls: Type[Trigger]) -> Type[Trigger]:
    """
    Annotation analogous to `module_node`, but for triggers.
    """

    if not issubclass(cls, Trigger):
        raise ValueError(f"Class reference {cls} is not a subclass of mmisp.workflows.modules.Trigger!")

    TRIGGER_REGISTRY.modules[cls.id] = cls

    return cls


@trigger_node
@dataclass(kw_only=True)
class TriggerAttributeAfterSave(Trigger):
    id: str = "attribute-after-save"
    name: str = "Attribute After Save"
    scope: str = "attribute"
    icon: str = "cube"
    description: str = "This trigger is called after an Attribute has been saved in the database"
    blocking: bool = False
    overhead: Overhead = Overhead.HIGH


@trigger_node
@dataclass(kw_only=True)
class TriggerEnrichmentBeforeQuery(Trigger):
    id: str = "enrichment-before-query"
    scope: str = "others"
    name: str = "Enrichment Before Query"
    description: str = "This trigger is called just before a query against the enrichment service is done"
    icon: str = "asterisk"
    overhead: Overhead = Overhead.LOW
    blocking: bool = True


@trigger_node
@dataclass(kw_only=True)
class TriggerEventAfterSaveNewFromPull(Trigger):
    id: str = "event-after-save-new-from-pull"
    scope: str = "event"
    name: str = "Event After Save New From Pull"
    description: str = (
        "This trigger is called after a new Event has been saved in the database "
        "from a PULL operation. This trigger executes in place of `event-after-save-new`"
    )
    icon: str = "envelope"
    blocking: bool = False
    overhead: Overhead = Overhead.LOW


@trigger_node
@dataclass(kw_only=True)
class TriggerEventAfterSaveNew(Trigger):
    id: str = "event-after-save-new"
    scope: str = "event"
    name: str = "Event After Save New"
    description: str = "This trigger is called after a new Event has been saved in the database"
    icon: str = "envelope"
    blocking: bool = False
    overhead: Overhead = Overhead.LOW


@trigger_node
@dataclass(kw_only=True)
class TriggerEventAfterSave(Trigger):
    id: str = "event-after-save"
    scope: str = "event"
    name: str = "Event After Save"
    description: str = "This trigger is called after an Event or any of its elements has been saved in the database"
    icon: str = "envelope"
    blocking: bool = False
    overhead: Overhead = Overhead.HIGH


@trigger_node
@dataclass(kw_only=True)
class TriggerEventBeforeSave(Trigger):
    id: str = "event-before-save"
    scope: str = "event"
    name: str = "Event Before Save"
    description: str = (
        "This trigger is called before an Event or any of its elements is about to be saved in the database"
    )
    icon: str = "envelope"
    blocking: bool = True
    overhead: Overhead = Overhead.HIGH


@trigger_node
@dataclass(kw_only=True)
class TriggerEventPublish(Trigger):
    id: str = "event-publish"
    scope: str = "event"
    name: str = "Event Publish"
    description: str = "This trigger is called just before a MISP Event starts the publishing process"
    icon: str = "upload"
    blocking: bool = True
    overhead: Overhead = Overhead.LOW


@trigger_node
@dataclass(kw_only=True)
class TriggerLogAfterSave(Trigger):
    id: str = "log-after-save"
    scope: str = "log"
    name: str = "Log After Save"
    description: str = "This trigger is called after a Log event has been saved in the database"
    icon: str = "file"
    blocking: bool = False
    overhead: Overhead = Overhead.HIGH


@trigger_node
@dataclass(kw_only=True)
class TriggerObjectAfterSave(Trigger):
    id: str = "object-after-save"
    scope: str = "object"
    name: str = "Object After Save"
    description: str = "This trigger is called after an Object has been saved in the database"
    icon: str = "cubes"
    blocking: bool = False
    overhead: Overhead = Overhead.HIGH


@trigger_node
@dataclass(kw_only=True)
class TriggerPostAfterSave(Trigger):
    id: str = "post-after-save"
    scope: str = "post"
    name: str = "Post After Save"
    description: str = "This trigger is called after a Post has been saved in the database"
    icon: str = "comment"
    blocking: bool = False
    overhead: Overhead = Overhead.LOW


@trigger_node
@dataclass(kw_only=True)
class TriggerShadowAttributeBeforeSave(Trigger):
    id: str = "shadow-attribute-before-save"
    scope: str = "shadow-attribute"
    name: str = "Shadow Attribute Before Save"
    description: str = "This trigger is called just before a Shadow Attribute is saved in the database"
    icon: str = "comment"
    blocking: bool = True
    overhead: Overhead = Overhead.MEDIUM


@trigger_node
@dataclass(kw_only=True)
class TriggerSightingAfterSave(Trigger):
    id: str = "sighting-after-save"
    scope: str = "sighting"
    name: str = "Sighting After Save"
    description: str = "This trigger is called when a sighting has been saved"
    icon: str = "eye"
    blocking: bool = False
    overhead: Overhead = Overhead.MEDIUM


@trigger_node
@dataclass(kw_only=True)
class TriggerUserAfterSave(Trigger):
    id: str = "user-after-save"
    scope: str = "user"
    name: str = "User After Save"
    description: str = "This trigger is called after a user has been saved in the database"
    icon: str = "user-edit"
    blocking: bool = False
    overhead: Overhead = Overhead.LOW


@trigger_node
@dataclass(kw_only=True)
class TriggerUserBeforeSave(Trigger):
    id: str = "user-before-save"
    scope: str = "user"
    name: str = "User Before Save"
    description: str = "This trigger is called just before a user is save in the database"
    icon: str = "user-plus"
    blocking: bool = True
    overhead: Overhead = Overhead.LOW


@module_node
@dataclass(kw_only=True)
class ModuleIfGeneric(ModuleAction):
    id: str = "generic-if"
    n_outputs: int = 2
    name: str = "IF :: Generic"
    version: str = "0.2"
    description: str = (
        "Generic IF / ELSE condition block. The `then` output will be used "
        "if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"


@module_node
@dataclass(kw_only=True)
class ModuleEnrichEvent(ModuleAction):
    id: str = "enrich-event"
    name: str = "Enrich Event"
    version: str = "0.2"
    description: str = "Enrich all Attributes contained in the Event with the provided module."


@module_node
@dataclass(kw_only=True)
class ModuleAttributeCommentOperation(ModuleAction):
    id: str = "Module_attribute_comment_operation"
    version: str = "0.1"
    name: str = "Attribute comment operation"
    description: str = "Set the Attribute's comment to the selected value"
    icon: str = "edit"
    on_demand_filtering_enabled: bool = True


@module_node
@dataclass(kw_only=True)
class ModuleTagIf(ModuleLogic):
    id: str = "tag-if"
    n_outputs: int = 2
    name: str = "IF :: Tag"
    version: str = "0.4"
    description: str = (
        "Tag IF / ELSE condition block. The `then` output will be used if "
        "the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"


@module_node
@dataclass(kw_only=True)
class ModuleStopWorkflow(ModuleAction):
    id: str = "stop-execution"
    name: str = "Stop execution"
    version: str = "0.2"
    description: str = "Essentially stops the execution for blocking workflows. Do nothing for non-blocking ones"
    icon: str = "ban"


@module_node
@dataclass(kw_only=True)
class ModuleAttachWarninglist(ModuleAction):
    id: str = "attach-warninglist"
    name: str = "Add to warninglist"
    description: str = "Append attributes to an active custom warninglist."
    icon: str = "exclamation-triangle"
    on_demand_filtering_enabled: bool = True


@module_node
@dataclass(kw_only=True)
class ModuleConcurrentTask(ModuleLogic):
    """
    Accepts multiple connecting nodes and executes all of them
    concurrently.
    """

    id: str = "concurrent-task"
    name: str = "Concurrent Task"
    description: str = (
        "Allow breaking the execution process and running concurrent tasks."
        "You can connect multiple nodes the `concurrent` output."
    )
    icon: str = "random"
    enable_multiple_edges_per_output: bool = True
    html_template: str = "concurrent"


@module_node
@dataclass(kw_only=True)
class ModuleCountIf(ModuleLogic):
    id: str = "count-if"
    name: str = "IF :: Count"
    description: str = (
        "Count IF / ELSE condition block. It counts the amount of entry "
        "selected by the provided hashpath. The `then` output will be used "
        "if the encoded conditions is satisfied, otherwise the `else` "
        "output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"


@module_node
@dataclass(kw_only=True)
class ModuleDistributionIf(ModuleLogic):
    id: str = "distribution-if"
    name: str = "IF :: Distribution"
    version: str = "0.3"
    description: str = (
        "Distribution IF / ELSE condition block. The `then` output will "
        "be used if the encoded conditions is satisfied, otherwise the `else` "
        "output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"


@module_node
@dataclass(kw_only=True)
class ModuleGenericFilterData(ModuleLogic):
    """
    Configure a filter on the workflow payload. Every
    subsequent module will only see the filtered version
    unless the effect gets reversed with
    [ModuleGenericFilterReset][mmisp.workflows.modules.ModuleGenericFilterReset].
    """

    id: str = "generic-filter-data"
    name: str = "Filter :: Generic"
    version: str = "0.2"
    description: str = (
        "Generic data filtering block. The module filters incoming data and forward the matching data to its output."
    )
    icon: str = "filter"


@module_node
@dataclass(kw_only=True)
class ModuleGenericFilterReset(ModuleLogic):
    """
    Resets all filters declared for the workflow payload.
    """

    id: str = "generic-filter-reset"
    name: str = "Filter :: Remove filter"
    description: str = "Reset filtering"
    icon: str = "redo-alt"


@module_node
@dataclass(kw_only=True)
class ModuleOrganisationIf(ModuleLogic):
    """
    Module allowing to check if the organistaion property
    of the payload matches a condition.
    """

    id: str = "organisation-if"
    name: str = "IF :: Organisation"
    description: str = (
        "Organisation IF / ELSE condition block. The `then` output "
        "will be used if the encoded conditions is satisfied, otherwise "
        "the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"


@module_node
@dataclass(kw_only=True)
class ModulePublishedIf(ModuleLogic):
    id: str = "published-if"
    name: str = "IF :: Published"
    description: str = (
        "Published IF / ELSE condition block. The `then` output "
        "will be used if the encoded conditions is satisfied, otherwise "
        "the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"


@module_node
@dataclass(kw_only=True)
class ModuleThreatLevelIf(ModuleLogic):
    id: str = "threat-level-if"
    html_template: str = "if"
    n_outputs: int = 2
    name: str = "IF :: Threat Level"
    version: str = "0.1"
    description: str = (
        "Threat Level IF / ELSE condition block. The `then` output "
        "will be used if the encoded conditions is satisfied, otherwise "
        "the`else` output will be used."
    )
    icon: str = "code-branch"


@module_node
@dataclass(kw_only=True)
class ModuleAddEventblocklistEntry(ModuleAction):
    id: str = "add_eventblocklist_entry"
    version: str = "0.1"
    name: str = "Add Event Blocklist entry"
    description: str = "Create a new entry in the Event blocklist table"
    icon: str = "ban"


@module_node
@dataclass(kw_only=True)
class ModuleAssignCountryFromEnrichment(ModuleAction):
    id: str = "assign_country"
    name: str = "IF :: Threat Level"
    version: str = "0.1"
    description: str = (
        "Threat Level IF / ELSE condition block. The `then` output will be used if the "
        "encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2


@module_node
@dataclass(kw_only=True)
class ModuleAttachEnrichment(ModuleAction):
    id: str = "attach-enrichment"
    name: str = "Attach enrichment"
    version: str = "0.3"
    description: str = "Attach selected enrichment result to Attributes."
    icon: str = "asterisk"
    on_demand_filtering_enabled: bool = True


@module_node
@dataclass(kw_only=True)
class ModuleAttributeEditionOperation(ModuleAction):
    id: str = "attribute_edition_operation"
    name: str = "Attribute edition operation"
    description: str = "Base module allowing to modify attribute"
    icon: str = "edit"


@module_node
@dataclass(kw_only=True)
class ModuleAttributeIdsFlagOperation(ModuleAction):
    id: str = "attribute_ids_flag_operation"
    name: str = "Attribute IDS Flag operation"
    description: str = "Toggle or remove the IDS flag on selected attributes."
    icon: str = "edit"
    on_demand_filtering_enabled: bool = True


@module_node
@dataclass(kw_only=True)
class ModuleEventDistributionOperation(ModuleAction):
    id: str = "Module_event_distribution_operation"
    name: str = "Event distribution operation"
    description: str = "Set the Event's distribution to the selected level"
    icon: str = "edit"


@module_node
@dataclass(kw_only=True)
class ModuleMsTeamsWebhook(ModuleAction):
    id: str = "ms-teams-webhook"
    name: str = "MS Teams Webhook"
    version: str = "0.5"
    description: str = 'Perform callbacks to the MS Teams webhook provided by the "Incoming Webhook" connector'


@module_node
@dataclass(kw_only=True)
class ModulePublishEvent(ModuleAction):
    id: str = "publish-event"
    name: str = "Publish Event"
    version: str = "0.1"
    description: str = "Publish an Event in the context of the workflow"
    icon: str = "upload"


@module_node
@dataclass(kw_only=True)
class ModulePushZMQ(ModuleAction):
    id: str = "push-zmq"
    name: str = "Push to ZMQ"
    version: str = "0.2"
    description: str = "Push to the ZMQ channel"


@module_node
@dataclass(kw_only=True)
class ModuleSendLogMail(ModuleAction):
    id: str = "send-log-mail"
    name: str = "Send Log Mail"
    description: str = (
        "Allow to send a Mail to a list or recipients, based on a Log trigger."
        " Requires functional misp-modules to be functional."
    )
    icon: str = "envelope"


@module_node
@dataclass(kw_only=True)
class ModuleSendMail(ModuleAction):
    id: str = "send-mail"
    name: str = "Send Mail"
    description: str = (
        "Allow to send a Mail to a list or recipients. Requires functional misp-modules to be functional."
    )
    icon: str = "envelope"


@module_node
@dataclass(kw_only=True)
class ModuleSplunkHecExport(ModuleAction):
    id: str = "splunk-hec-export"
    name: str = "Splunk HEC export"
    version: str = "0.2"
    description: str = (
        "Export Event Data to Splunk HTTP Event Collector. Due to the potential high amount "
        "of requests, it's recommanded to put this module after a `concurrent_task` logic module."
    )


@module_node
@dataclass(kw_only=True)
class ModuleStopExecution(ModuleAction):
    id: str = "stop-execution"
    name: str = "Stop execution"
    version: str = "0.2"
    description: str = "Essentially stops the execution for blocking workflows. Do nothing for non-blocking ones"
    icon: str = "ban"
    n_outputs: int = 0


@module_node
@dataclass(kw_only=True)
class ModuleTagOperation(ModuleAction):
    id: str = "tag_operation"
    name: str = "Tag operation"
    description: str = "Add or remove tags on Event or Attributes."
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.2"


@module_node
@dataclass(kw_only=True)
class ModuleTagReplacementGeneric(ModuleAction):
    id: str = "tag_replacement_generic"
    name: str = "Tag Replacement Generic"
    description: str = "Attach a tag, or substitue a tag by another"
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.1"


@module_node
@dataclass(kw_only=True)
class ModuleTagReplacementPap(ModuleAction):
    id: str = "tag_replacement_pap"
    name: str = "Tag Replacement - PAP"
    description: str = "Attach a tag (or substitue) a tag by another for the PAP taxonomy"
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.1"


@module_node
@dataclass(kw_only=True)
class ModuleTagReplacementTlp(ModuleAction):
    id: str = "tag_replacement_tlp"
    name: str = "Tag Replacement - TLP"
    version: str = "0.1"
    description: str = "Attach a tag (or substitue) a tag by another for the TLP taxonomy"
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True


@module_node
@dataclass(kw_only=True)
class ModuleTelegramSendAlert(ModuleAction):
    id: str = "telegram-send-alert"
    name: str = "Telegram Send Alert"
    version: str = "0.1"
    description: str = "Send a message alert to a Telegram channel"


@module_node
@dataclass(kw_only=True)
class ModuleWebhook(ModuleAction):
    id: str = "webhook"
    name: str = "Webhook"
    version: str = "0.7"
    description: str = "Allow to perform custom callbacks to the provided URL"
