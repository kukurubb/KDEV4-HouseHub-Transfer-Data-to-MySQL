import enum

class TransactionTypeEnum(enum.Enum):
    SALE = "매매"
    JEONSE = "전세"
    MONTHLY = "월세"

def map_naver_transaction_type(value):
    NAVER_TRANSCATION_TO_ENUM = {
        "매매": TransactionTypeEnum.SALE,
        "전세": TransactionTypeEnum.JEONSE,
        "월세": TransactionTypeEnum.MONTHLY,
    }
    return NAVER_TRANSCATION_TO_ENUM.get(value.strip())

def map_zigbang_transaction_type(value):
    ZIGBANG_TRANSCATION_TO_ENUM = {
        "매매": TransactionTypeEnum.SALE,
        "전세": TransactionTypeEnum.JEONSE,
        "월세": TransactionTypeEnum.MONTHLY,
    }
    return ZIGBANG_TRANSCATION_TO_ENUM.get(value.strip())

