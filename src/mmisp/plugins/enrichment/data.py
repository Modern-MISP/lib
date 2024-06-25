from pydantic import BaseModel

from mmisp.api_schemas.attributes import AddAttributeBody
from mmisp.api_schemas.tags import TagCreateBody


class NewEventTag(BaseModel):
    """
    Encapsulates a new MISP Event Tag that has been created using enrichment.
    """

    tag_id: int | None = None
    """The ID of the tag if it already exists in the database."""
    tag: TagCreateBody | None = None
    """The tag if it doesn't exist yet in the Database."""
    local: bool | None = None
    """Whether the relationship to the event is only local or not."""
    relationship_type: str
    """The relationship type between the event and tag."""

    # TODO: Add validator that ensures that either tag_id or tag is set.


class NewAttributeTag(BaseModel):
    """
    Encapsulates a new MISP Attribute Tag created by enrichment.
    """

    tag_id: int | None = None
    """The ID of the tag if it already exists in the database."""
    tag: TagCreateBody | None = None
    """The tag if it doesn't exist yet in the Database."""
    local: bool | None = None
    """Whether the relationship to the attribute is only local or not."""
    relationship_type: str
    """The relationship type between the attribute and tag."""

    # TODO: Add validator that ensures that either tag_id or tag is set.


class NewAttribute(BaseModel):
    """
    Encapsulates a newly created attribute from the enrichment process that doesn't exist yet in the database.
    """

    attribute: AddAttributeBody
    """The attribute to create."""
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
