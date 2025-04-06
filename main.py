from service.save_to_db import insert_sample_data
from service.parse_naver import ParsingNaver
from service.parse_zigbang import ParsingZigbang
from enums.direction import DirectionEnum
from enums.property_type import PropertyTypeEnum
from enums.transaction_type import TransactionTypeEnum


if __name__ == "__main__":
    # 컬럼 매핑
    column_mapping = {
        "zigbang": {
            "crawling_properties_id": "item.itemId",
            "property_type": "item.serviceType",
            "transaction_type": "item.salesType",
            "province": "item.addressOrigin.local1",
            "city": "item.addressOrigin.local2",
            "dong": "item.addressOrigin.local3",
            "detail_address": "item.jibunAddress",
            "floor": "item.floor.floor",
            "all_floors": "item.floor.allFloors",
            "sale_price": "item.price.sales",
            "deposit": "item.price.deposit",
            "monthly_rent_fee": "item.price.rent",
            "direction": "item.roomDirection",
            "real_estate_agent_id": "agent.agentUserNo",
            "real_estate_agent_name": "agent.agentName",
            "real_estate_agent_contact": "agent.agentPhone",
            "real_estate_office_name": "agent.agentTitle",
            "real_estate_office_address": "agent.agentAddress",
        },
        "naver": {
            "crawling_properties_id": "articleDetail.articleNo",
            "property_type": "articleDetail.realestateTypeName",
            "transaction_type": "articleDetail.tradeTypeName",
            "province": "articleDetail.cityName",
            "city": "articleDetail.divisionName",
            "dong": "articleDetail.sectionName",
            "detail_address": "articleDetail.exposureAddress",
            "floor": "articleFloor.correspondingFloorCount",
            "all_floors": "articleFloor.totalFloorCount",
            "sale_price": "articlePrice.dealPrice",
            "deposit": "articlePrice.warrantPrice",
            "monthly_rent_fee": "articlePrice.rentPrice",
            "direction": "articleAddition.direction",
            "real_estate_agent_id": "articleRealtor.realtorId",
            "real_estate_agent_name": "articleRealtor.representativeName",
            "real_estate_agent_contact": "articleRealtor.cellPhoneNo",
            "real_estate_office_name": "articleRealtor.realtorName",
            "real_estate_office_address": "articleRealtor.address",
        },
    }
    property_details_dirs = {
        "zigbang": "./data/zigbang_property_details/*.txt",
        "naver": "./data/naver_property_details/*.txt",
    }
    
    # 네이버 데이터 파싱 및 저장
    naver = ParsingNaver(property_details_dirs["naver"], column_mapping["naver"])
    naver_df = naver.parse_data()
    insert_sample_data(naver_df)

    # 직방 데이터 파싱 및 저장
    zigbang = ParsingZigbang(property_details_dirs["zigbang"], column_mapping["zigbang"])
    zigbang_df = zigbang.parse_data()
    insert_sample_data(zigbang_df)