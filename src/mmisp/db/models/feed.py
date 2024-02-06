from sqlalchemy import Boolean, Column, Integer, String

from ..database import Base


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    provider = Column(String(255))
    url = Column(String(255))
    rules = Column(String(255))
    enabled = Column(String(255))
    distribution = Column(String(255))
    sharing_group_id = Column(Integer)
    tag_id = Column(Integer)
    default = Column(Boolean)
    source_format = Column(String(255))
    fixed_event = Column(String(255))
    delta_merge = Column(Boolean)
    event_id = Column(Integer)
    publish = Column(Boolean)
    override_ids = Column(Boolean)
    settings = Column(String(255))
    input_source = Column(String(255), index=True)
    delete_local_file = Column(Boolean)
    lookup_visible = Column(Boolean)
    headers = Column(String(255))
    caching_enabled = Column(Boolean)
    force_to_ids = Column(Boolean)
    orgc_id = Column(Integer, index=True)
    cache_timestamp = Column(String(255))
    cached_elements = Column(Integer)  # new
    coverage_by_other_feeds = Column(String(255))  # new
