from sqlalchemy import Column, String

from ..database import Base


class Galaxy(Base):
    id = Column(String, primary_key=True)
    uuid = Column(String)
    name = Column(String)
    type = Column(String)
    description = Column(String)
    version = Column(String)
    icon = Column(String)
    namespace = Column(String)
    kill_chain_order = Column(list[str])
