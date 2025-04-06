import enum

class PropertyTypeEnum(enum.Enum):
    VILLA = "빌라"
    APARTMENT = "아파트"
    OFFICETEL = "오피스텔"

def map_naver_property_type(value):
    NAVER_PROPERTY_TO_ENUM = {
        "빌라": PropertyTypeEnum.VILLA,
    }
    return NAVER_PROPERTY_TO_ENUM.get(value.strip())

def map_zigbang_property_type(value):
    ZIGBANG_PROPERTY_TO_ENUM = {
        "빌라": PropertyTypeEnum.VILLA,
    }
    return ZIGBANG_PROPERTY_TO_ENUM.get(value.strip())