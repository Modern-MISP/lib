from typing import Optional

from pydantic import BaseModel, ConfigDict, StringConstraints
from typing_extensions import Annotated

from mmisp.plugins.plugin_type import PluginType


class PluginInfo(BaseModel):
    """
    Encapsulates information about a plugin.
    """

    # TODO[pydantic]: The following keys were removed: `allow_mutation`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(str_strip_whitespace=True, allow_mutation=False)

    NAME: Annotated[str, StringConstraints(min_length=1)]
    """Name of the plugin"""
    PLUGIN_TYPE: PluginType
    """Type of the plugin"""
    DESCRIPTION: Optional[str] = None
    """Description of the plugin"""
    AUTHOR: Optional[str] = None
    """Author who wrote the plugin"""
    VERSION: Optional[str] = None
    """Version of the plugin"""
