import random

from mmisp.api_schemas.attributes import GetAttributeAttributes
from mmisp.lib.uuid import uuid
from mmisp.tests.generators.feed_generator import generate_number_as_str
from mmisp.tests.generators.object_generator import generate_ids_as_str, generate_random_date_str, generate_random_str
from mmisp.tests.generators.tag_generator import generate_get_attribute_tag_response


def generate_get_attribute_attributes_response() -> GetAttributeAttributes:
    return GetAttributeAttributes(
        id=generate_ids_as_str(),
        event_id=generate_ids_as_str(),
        object_id=generate_ids_as_str(),
        object_relation=generate_random_str(),
        category=generate_random_str(),
        type=generate_random_str(),
        value=generate_random_str(),
        to_ids=False,
        uuid=uuid(),
        timestamp=generate_random_date_str(),
        distribution=generate_number_as_str(),
        sharing_group_id=generate_ids_as_str(),
        comment=generate_random_str(),
        deleted=bool(random.getrandbits),
        disable_correlation=bool(random.getrandbits),
        first_seen=generate_random_date_str(),
        last_seen=generate_random_date_str(),
        event_uuid=uuid(),
        data=generate_random_str(),
        Tag=[generate_get_attribute_tag_response()]
    )
