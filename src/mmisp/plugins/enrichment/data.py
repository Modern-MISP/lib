from pydantic import BaseModel

from mmisp.api_schemas.attributes import AddAttributeBody
from mmisp.api_schemas.tags import TagCreateBody
from mmisp.plugins.models.attribute_tag_relationship import AttributeTagRelationship
from mmisp.plugins.models.event_tag_relationship import EventTagRelationship


class NewEventTag(BaseModel):
    """
    Encapsulates a MISP Tag assigned to an event.
    """

    tag_id: int | None = None
    """The ID of the tag if it already exists in the database."""
    tag: TagCreateBody | None = None
    """The tag if it doesn't exist yet in the Database."""
    relationship: EventTagRelationship
    """The assignment and relationship to the event."""


class NewAttributeTag(BaseModel):
    """
    Encapsulates a MISP Tag and its assignment to an attribute.
    """

    tag_id: int | None = None
    """The ID of the tag if it already exists in the database."""
    tag: TagCreateBody | None = None
    """The tag if it doesn't exist yet in the Database."""
    relationship: AttributeTagRelationship
    """The assignment and relationship to the attribute."""


class NewAttribute(BaseModel):
    """
    Encapsulates a newly created attribute from the enrichment process.
    """

    attribute: AddAttributeBody
    """The attribute"""
    tags: list[NewAttributeTag] = []
    """Tags attached to the attribute"""


class EnrichAttributeResult(BaseModel):
    """
    Encapsulates the result of an enrich-attribute job.

    Contains newly created attributes and tags.
    """

    attributes: list[NewAttribute] = []
    """The created attributes."""
    event_tags: list[NewEventTag] = []
    """The created event tags. Can also be the IDs of already existing tags."""

    def append(self, result_to_merge: "EnrichAttributeResult"):
        """
        Merges two EnrichAttributeResult objects together.

        :param result_to_merge: The object that should be merged into this result.
        :type result_to_merge: EnrichAttributeResult
        """
        self.attributes.extend(result_to_merge.attributes)
        self.event_tags.extend(result_to_merge.event_tags)
