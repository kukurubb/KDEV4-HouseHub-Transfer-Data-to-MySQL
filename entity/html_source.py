from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Numeric,
    Enum,
    Boolean
)
from sqlalchemy.dialects.mysql import (
    TINYTEXT,    # 최대 255 bytes
    TEXT,        # 최대 65,535 bytes (64KB)
    MEDIUMTEXT,  # 최대 16,777,215 bytes (16MB)
    LONGTEXT     # 최대 4,294,967,295 bytes (4GB)
)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HtmlSource(Base):
    __tablename__ = "html_sources"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    crawling_propertiy_id = Column(String(100), nullable=False)
    html_source = Column(TEXT(), nullable=False)
    is_error = Column(Boolean(), nullable=False)
    is_parsed = Column(Boolean(), nullable=False)