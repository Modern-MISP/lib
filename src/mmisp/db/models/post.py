from sqlalchemy import Column, DateTime, TEXT, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlmodel import Field

from ..database import Base


class Post(Base):
    """
    Encapsulates a MISP Post.
    """
    __tablename__ = 'posts'

    id = Field(INTEGER(11), primary_key=True)
    date_created = Column(DateTime, nullable=False)
    date_modified = Column(DateTime, nullable=False)
    user_id = Column(INTEGER(11), nullable=False)
    contents = Column(Text, nullable=False)
    post_id = Column(INTEGER(11), nullable=False, index=True, server_default=text("0"))
    thread_id = Column(INTEGER(11), nullable=False, index=True, server_default=text("0"))
