# region IMPORT
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.sql.expression import null

# endregion IMPORT


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(256), nullable=False)
    content = Column(String(400), nullable=False)
    published = Column(Boolean, server_default=text("0"))
    created_at = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
