from sqlalchemy import Column, String, Integer, Float, Numeric, Enum
from entity.base import Base
from enums.direction import DirectionEnum
from enums.property_type import PropertyTypeEnum
from enums.transaction_type import TransactionTypeEnum


class CrawlingProperty(Base):
    __tablename__ = "crawling_properties"

    crawling_properties_id = Column(String(100), primary_key=True)
    property_type = Column(Enum(PropertyTypeEnum), nullable=False)
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)
    province = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    dong = Column(String(50), nullable=True)
    detail_address = Column(String(100), nullable=True)
    area = Column(Float(24), nullable=True)
    floor = Column(String(20), nullable=True)
    all_floors = Column(String(50), nullable=True)
    sale_price = Column(Float(24), nullable=True)
    deposit = Column(Float(24), nullable=True)
    monthly_rent_fee = Column(Float(24), nullable=True)
    direction = Column(Enum(DirectionEnum), nullable=False)
    real_estate_agent_id = Column(String(100), nullable=True)
    real_estate_agent_name = Column(String(100), nullable=True)
    real_estate_agent_contact = Column(String(100), nullable=True)
    real_estate_office_name = Column(String(100), nullable=True)
    real_estate_office_address = Column(String(100), nullable=True)
    bath_room_cnt = Column(Float(24), nullable=True)
    room_cnt = Column(Float(24), nullable=True)