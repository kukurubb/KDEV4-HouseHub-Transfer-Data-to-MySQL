from sqlalchemy import Column, String, Integer, Float, Numeric, Enum
from entity.base import Base


class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)
    value = Column(String(100), nullable=False)