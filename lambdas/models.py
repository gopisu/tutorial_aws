from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class ExampleData(Base):
    __tablename__ = "example_data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
