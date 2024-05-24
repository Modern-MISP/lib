


class GalaxyClusterBlocklists(Base):
    __tablename__ = 'galaxy_cluster_blocklists'

    cluster_uuid = Column(String(255), primary_key=True, nullable=False) #todo string oder uuid?
    #todo add more fields


class EventBlocklists(Base):
    __tablename__ = 'event_blocklists'

    event_uuid = Column(String(255), primary_key=True, nullable=False) #todo string oder uuid und wer primärschlüssel?
    org_uuid = Column(String(255), nullable=False) #todo string oder uuid?
    #todo add more fields
