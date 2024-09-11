from mmisp.db.models.attribute import Attribute


def generate_attribute(event_id) -> Attribute:
    return Attribute(value="1.2.3.4", value1="1.2.3.4", type="ip-src", category="Network activity", event_id=event_id)
