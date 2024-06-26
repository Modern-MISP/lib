from sqlalchemy import Boolean, ForeignKey, Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column
from mmisp.util.uuid import uuid

from ..database import Base
from .galaxy import Galaxy


class GalaxyCluster(Base):
    __tablename__ = "galaxy_clusters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(255), unique=True, default=uuid, index=True)
    collection_uuid: Mapped[str] = mapped_column(String(255), nullable=False, index=True, default="0")
    type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    tag_name: Mapped[str] = mapped_column(String(255), nullable=False, default="", index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    galaxy_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Galaxy.id, ondelete="CASCADE"), nullable=False, index=True
    )
    source: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    authors: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=0, index=True)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer, index=True, default=0)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=0)
    orgc_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=0)
    default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    extends_uuid: Mapped[str] = mapped_column(String(40), index=True)
    extends_version: Mapped[int] = mapped_column(Integer, default=0, index=True)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class GalaxyElement(Base):
    __tablename__ = "galaxy_elements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    galaxy_cluster_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(GalaxyCluster.id, ondelete="CASCADE"), nullable=False, index=True
    )
    key: Mapped[str] = mapped_column(String(255), nullable=False, default="", index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)


class GalaxyReference(Base):
    __tablename__ = "galaxy_reference"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    galaxy_cluster_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(GalaxyCluster.id, ondelete="CASCADE"), nullable=False, index=True
    )
    referenced_galaxy_cluster_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    referenced_galaxy_cluster_uuid: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    referenced_galaxy_cluster_type: Mapped[str] = mapped_column(Text, nullable=False)
    referenced_galaxy_cluster_value: Mapped[str] = mapped_column(Text, nullable=False)
