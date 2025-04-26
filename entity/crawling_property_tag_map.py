from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from entity.base import Base


class CrawlingPropertyTagMap(Base):
    __tablename__ = "crawling_property_tag_map"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    crawling_properties_id = Column(String(100), ForeignKey("crawling_properties.crawling_properties_id"))
    tag_id = Column(Integer, ForeignKey("tags.tag_id"))