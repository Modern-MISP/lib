from typing import Self

from pydantic import BaseModel, root_validator

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
    relationship_type: str = ""
    """The relationship type between the event and tag."""

    @root_validator
    @classmethod
    def check_tag_id_or_new_tag_provided(cls: type["NewEventTag"], values: dict) -> None:
        if not values["tag_id"] or values["tag"]:
            raise ValueError("At least one of the values tag_id or tag is required.")


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
    relationship_type: str = ""
    """The relationship type between the attribute and tag."""

    @root_validator
    @classmethod
    def check_tag_id_or_new_tag_provided(cls: type["NewEventTag"], values: dict) -> None:
        if not values["tag_id"] or values["tag"]:
            raise ValueError("At least one of the values tag_id or tag is required.")


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

    def append(self: Self, result_to_merge: "EnrichAttributeResult") -> None:
        """
        Merges two EnrichAttributeResult objects together.

        :param result_to_merge: The object that should be merged into this result.
        :type result_to_merge: EnrichAttributeResult
        """
        self.attributes.extend(result_to_merge.attributes)
        self.event_tags.extend(result_to_merge.event_tags)
