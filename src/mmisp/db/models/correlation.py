from sqlalchemy import Index, Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class OverCorrelatingValue(Base):
    """
    Class to represent the table of the over correlating values in the misp_sql database.
    """

    __tablename__ = "over_correlating_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String(191))
    occurrence: Mapped[int | None] = mapped_column(Integer, index=True)
    __table_args__ = (
        Index("ix_over_correlating_values_value", "value", unique=False),
        {"extend_existing": True},
    )


class CorrelationValue(Base):
    """
    Class to represent the table of the correlation values in the misp_sql database.
    """

    __tablename__ = "correlation_values"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String(255))
    __table_args__ = (Index("ix_correlation_values_value", "value", unique=False),)


class CorrelationExclusions(Base):
    __tablename__ = "correlation_exclusions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String(255))
    from_json: Mapped[int | None] = mapped_column(Integer, default=0)
    comment: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (
        Index("ix_correlation_exclusions_value", "value", unique=False),
        {"extend_existing": True},
    )


class DefaultCorrelation(Base):
    __tablename__ = "default_correlations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attribute_id: Mapped[int] = mapped_column(Integer, index=True)
    object_id: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(Integer, index=True)
    org_id: Mapped[int] = mapped_column(Integer)
    distribution: Mapped[int] = mapped_column(Integer)
    object_distribution: Mapped[int] = mapped_column(Integer)
    event_distribution: Mapped[int] = mapped_column(Integer)
    sharing_group_id: Mapped[int] = mapped_column(Integer)
    object_sharing_group_id: Mapped[int] = mapped_column(Integer)
    event_sharing_group_id: Mapped[int] = mapped_column(Integer)
    attribute_id_1: Mapped[int] = mapped_column("1_attribute_id", Integer, index=True)
    object_id_1: Mapped[int] = mapped_column("1_object_id", Integer, index=True)
    event_id_1: Mapped[int] = mapped_column("1_event_id", Integer, index=True)
    org_id_1: Mapped[int] = mapped_column("1_org_id", Integer)
    distribution_1: Mapped[int] = mapped_column("1_distribution", Integer)
    object_distribution_1: Mapped[int] = mapped_column("1_object_distribution", Integer)
    event_distribution_1: Mapped[int] = mapped_column("1_event_distribution", Integer)
    sharing_group_id_1: Mapped[int] = mapped_column("1_sharing_group_id", Integer)
    object_sharing_group_id_1: Mapped[int] = mapped_column("1_object_sharing_group_id", Integer)
    event_sharing_group_id_1: Mapped[int] = mapped_column("1_event_sharing_group_id", Integer)
    value_id: Mapped[int] = mapped_column(Integer, index=True)
    __table_args__ = (
        Index("ix_default_correlations_unique_correlation", "attribute_id", "1_attribute_id", "value_id", unique=False),
    )
