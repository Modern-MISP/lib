from sqlalchemy import Column, Integer

from ..database import Base


class OverCorrelatingValue(Base):
    """
    Class to represent the table of the over correlating values in the misp_sql database.
    """
    __tablename__ = "over_correlating_values"

    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(String, nullable=False, index=True)
    occurrence = Column(Integer, nullable=False, index=True)

class CorrelationValue(Base):
    """
    Class to represent the table of the correlation values in the misp_sql database.
    """
    __tablename__ = "correlation_values"

    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(String, nullable=False, index=True)


class CorrelationExclusions(Base):
    __tablename__ = 'correlation_exclusions'

    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(String, nullable=False, index=True)


class Correlation(Base):
    """
    Dataclass to encapsulate an entry from the "default_correlations"
    table in the misp database.
    """
    __tablename__ = 'default_correlations'

    id = Column(INTEGER(10), primary_key=True)
    attribute_id = Column(INTEGER(10), nullable=False, index=True)
    object_id = Column(INTEGER(10), nullable=False, index=True)
    event_id = Column(INTEGER(10), nullable=False, index=True)
    org_id = Column(INTEGER(10), nullable=False)
    distribution = Column(TINYINT(4), nullable=False)
    object_distribution = Column(TINYINT(4), nullable=False)
    event_distribution = Column(TINYINT(4), nullable=False)
    sharing_group_id = Column(INTEGER(10), nullable=False, server_default=text("0"))
    object_sharing_group_id = Column(INTEGER(10), nullable=False, server_default=text("0"))
    event_sharing_group_id = Column(INTEGER(10), nullable=False, server_default=text("0"))
    attribute_id_1 = Column(INTEGER(10), '1_attribute_id', nullable=False, index=True)
    object_id_1 = Column(INTEGER(10), '1_object_id', nullable=False, index=True)
    event_id_1 = Column(INTEGER(10), '1_event_id', nullable=False, index=True)
    org_id_1 = Column(INTEGER(10), '1_org_id', nullable=False)
    distribution_1 = Column(TINYINT(4), '1_distribution', nullable=False)
    object_distribution_1 = Column(TINYINT(4), '1_object_distribution', nullable=False)
    event_distribution_1 = Column(TINYINT(4), '1_event_distribution', nullable=False)
    sharing_group_id_1 = Column(INTEGER(10), '1_sharing_group_id', nullable=False, server_default=text("0"))
    object_sharing_group_id_1 = Column(INTEGER(10), '1_object_sharing_group_id', nullable=False,
                                            server_default=text("0"))
    event_sharing_group_id_1= Column(INTEGER(10), '1_event_sharing_group_id', nullable=False,
                                           server_default=text("0"))
    value_id= Column(INTEGER(10), nullable=False, index=True)
