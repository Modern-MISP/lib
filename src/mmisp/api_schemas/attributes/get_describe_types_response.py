from pydantic import BaseModel

from mmisp.lib.attributes import AttributeCategories, default_category, inverted_categories, to_ids


class GetDescribeTypesAttributes(BaseModel):
    sane_defaults: dict = {}
    for k, v in to_ids.items():
        sane_defaults.update(
            {
                k: {
                    "default_category": default_category[k],
                    "to_ids": v,
                }
            }
        )

    types: list[str] = list(default_category.keys())

    categories: list[str] = [member.value for member in AttributeCategories]

    category_type_mappings: dict = inverted_categories


class GetDescribeTypesResponse(BaseModel):
    result: GetDescribeTypesAttributes

    class Config:
        orm_mode = True
