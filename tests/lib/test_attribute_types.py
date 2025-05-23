from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from mmisp.api_schemas.attribute_common import CommonAttribute
from mmisp.lib.attributes import AttributeType
from mmisp.lib.distribution import AttributeDistributionLevels

type_testcase = [
    ("ip-src", ["127.0.0.1", "2a00:1398:b::8d03:8006"], ["no-ip"]),
    ("sha1", ["da39a3ee5e6b4b0d3255bfef95601890afd80709"], ["no-sha1"]),
]


@pytest.mark.parametrize("attributetype, valid_values, invalid_values", type_testcase)
def test_validator(attributetype, valid_values, invalid_values):
    attribute_type = AttributeType.map_dbkey_attributetype[attributetype]
    category = attribute_type.default_category

    for v in valid_values:
        attr = CommonAttribute(
            id=1,
            event_id=1,
            object_id=0,
            sharing_group_id=0,
            timestamp=datetime.now(),
            category=category,
            type=attribute_type.dbkey,
            to_ids=False,
            uuid=uuid4(),
            distribution=AttributeDistributionLevels.OWN_ORGANIZATION,
            value=v,
        )
        assert attr.value == v

    for v in invalid_values:
        with pytest.raises(ValidationError):
            CommonAttribute(
                id=1,
                event_id=1,
                object_id=0,
                sharing_group_id=0,
                timestamp=datetime.now(),
                category=category,
                type=attribute_type.dbkey,
                to_ids=False,
                uuid=uuid4(),
                distribution=AttributeDistributionLevels.OWN_ORGANIZATION,
                value=v,
            )
