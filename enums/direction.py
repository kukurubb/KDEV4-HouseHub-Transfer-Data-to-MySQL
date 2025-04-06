import enum

class DirectionEnum(enum.Enum):
    EAST = "EAST"
    WEST = "WEST"
    SOUTH = "SOUTH"
    NORTH = "NORTH"
    SOUTHEAST = "SOUTHEAST"
    SOUTHWEST = "SOUTHWEST"
    NORTHEAST = "NORTHEAST"
    NORTHWEST = "NORTHWEST"

def map_naver_direction(value):
    NAVER_DIRECTION_TO_ENUM = {
        "동향": DirectionEnum.EAST,
        "서향": DirectionEnum.WEST,
        "남향": DirectionEnum.SOUTH,
        "북향": DirectionEnum.NORTH,
        "남동향": DirectionEnum.SOUTHEAST,
        "남서향": DirectionEnum.SOUTHWEST,
        "북동향": DirectionEnum.NORTHEAST,
        "북서향": DirectionEnum.NORTHWEST,
    }
    return NAVER_DIRECTION_TO_ENUM.get(value.strip())

def map_zigbang_direction(value):
    ZIGBANG_DIRECTION_TO_ENUM = {
        "E": DirectionEnum.EAST,
        "W": DirectionEnum.WEST,
        "S": DirectionEnum.SOUTH,
        "N": DirectionEnum.NORTH,
        "SE": DirectionEnum.SOUTHEAST,
        "SW": DirectionEnum.SOUTHWEST,
        "NE": DirectionEnum.NORTHEAST,
        "NW": DirectionEnum.NORTHWEST,
    }
    return ZIGBANG_DIRECTION_TO_ENUM.get(value.strip())