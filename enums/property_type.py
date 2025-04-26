import enum

class PropertyTypeEnum(enum.Enum):
    MULTIFAMILY = "다세대"
    SINGLEMULTIFAMILY = "단독/다가구"
    VILLA = "빌라"
    COMMERCIAL = "상가주택"
    APARTMENT = "아파트"
    ROWHOUSE = "연립"
    OFFICETEL = "오피스텔"
    ONE_ROOM = "원룸"
    COUNTRYHOUSE = "전원주택"

def map_naver_property_type(value):
    NAVER_PROPERTY_TO_ENUM = {
        "다세대": PropertyTypeEnum.MULTIFAMILY,
        "단독/다가구": PropertyTypeEnum.SINGLEMULTIFAMILY,
        "빌라": PropertyTypeEnum.VILLA,
        "상가주택": PropertyTypeEnum.COMMERCIAL,
        "아파트": PropertyTypeEnum.APARTMENT,
        "연립": PropertyTypeEnum.ROWHOUSE,
        "오피스텔": PropertyTypeEnum.OFFICETEL,
        "원룸": PropertyTypeEnum.ONE_ROOM,
        "전원주택": PropertyTypeEnum.COUNTRYHOUSE,
    }
    return NAVER_PROPERTY_TO_ENUM.get(value.strip())

def map_zigbang_property_type(value):
    ZIGBANG_PROPERTY_TO_ENUM = {
        "빌라": PropertyTypeEnum.VILLA,
    }
    return ZIGBANG_PROPERTY_TO_ENUM.get(value.strip())