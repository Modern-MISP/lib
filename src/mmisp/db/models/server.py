from sqlalchemy import Boolean, Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    authkey: Mapped[str] = mapped_column(String(40), nullable=False)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    push: Mapped[bool] = mapped_column(Boolean, nullable=False)
    pull: Mapped[bool] = mapped_column(Boolean, nullable=False)
    push_sightings: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    push_galaxy_clusters: Mapped[bool] = mapped_column(Boolean, default=False)
    pull_galaxy_clusters: Mapped[bool] = mapped_column(Boolean, default=False)
    lastpulledid: Mapped[int] = mapped_column(Integer)
    lastpushedid: Mapped[int] = mapped_column(Integer)
    organization: Mapped[str] = mapped_column(String(10), default=None)
    remote_org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    publish_without_email: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    unpublish_event: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    self_signed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    pull_rules: Mapped[str] = mapped_column(Text, nullable=False)
    push_rules: Mapped[str] = mapped_column(Text, nullable=False)
    cert_file: Mapped[str] = mapped_column(String(255))
    client_cert_file: Mapped[str] = mapped_column(String(255))
    internal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    skip_proxy: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    caching_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
