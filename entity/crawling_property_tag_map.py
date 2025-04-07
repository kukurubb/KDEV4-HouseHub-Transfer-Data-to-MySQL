from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from entity.base import Base


class CrawlingPropertyTagMap(Base):
    __tablename__ = "crawling_property_tag_map"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    property_id = Column(String(100), ForeignKey("crawling_property.crawling_property_id"))
    tag_id = Column(Integer, ForeignKey("tags.tag_id"))
