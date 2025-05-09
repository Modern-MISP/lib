from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommonObjectTemplateElement(BaseModel):
    ui_priority: int = Field(..., alias="ui-priority")
    categories: list
    sane_default: list
    values_list: list
    description: str
    disable_correlation: bool | None
    multiple: bool


class ImportObjectTemplateElement(CommonObjectTemplateElement):
    misp_attribute: str = Field(..., alias="misp-attribute")
    recommended: bool
    to_ids: bool


class ObjectTemplatesRequirements(BaseModel):
    requiredOneOf: list[str] | None = None
    required: list[str] | None = None


class ImportObjectTemplate(BaseModel):
    version: int
    description: str
    meta_category: str = Field(..., alias="meta-category")
    uuid: UUID
    name: str


class ImportObjectTemplateFile(ImportObjectTemplate, ObjectTemplatesRequirements):
    attributes: dict[str, ImportObjectTemplateElement]


class ObjectTemplate(ImportObjectTemplate):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    user_id: int
    org_id: int
    requirements: ObjectTemplatesRequirements
    fixed: bool
    active: bool


class ObjectTemplateElement(CommonObjectTemplateElement):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    object_template_id: int
    object_relation: str
    type: str  # AttributeType?


class RespObjectTemplateView(BaseModel):
    ObjectTemplate: ObjectTemplate
    ObjectTemplateElement: list[ObjectTemplateElement]


class RespItemObjectTemplateIndex(BaseModel):
    ObjectTemplate: ObjectTemplate
