from enum import Enum
from typing import FrozenSet, List

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from mmisp.plugins.plugin_info import PluginInfo


class EnrichmentPluginType(str, Enum):
    """
    Enum describing all possible enrichment plugin types.
    """

    EXPANSION = "expansion"
    """Enrichment Plugins of this type generate new attributes that can be attached to a MISP-Event
    to add additional information permanently."""
    HOVER = "hover"
    """Enrichment Plugins of this type generate information that is usually only displayed once
    and should not be stored permanently in the database."""


class PluginIO(BaseModel):
    """
    Encapsulates information about the accepted and returned attribute types of a plugin.
    """

    # TODO[pydantic]: The following keys were removed: `allow_mutation`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(allow_mutation=False, str_strip_whitespace=True, str_min_length=1)

    INPUT: Annotated[List[str], Field(min_length=1)]
    """Attribute types accepted by the Enrichment Plugin."""
    OUTPUT: Annotated[List[str], Field(min_length=1)]
    """Attribute types returned by the Enrichment Plugin."""


class EnrichmentPluginInfo(PluginInfo):
    ENRICHMENT_TYPE: Annotated[FrozenSet[EnrichmentPluginType], Field(min_length=1)]
    """The type of the enrichment plugin."""
    MISP_ATTRIBUTES: PluginIO
    """The accepted and returned types of attributes of the enrichment plugin."""
