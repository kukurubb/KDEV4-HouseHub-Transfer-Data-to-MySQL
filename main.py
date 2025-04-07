from service.save_to_db import insert_crawling_properties, insert_mapping, insert_tags
from service.parse_naver import ParsingNaver
from service.parse_zigbang import ParsingZigbang
from enums.direction import DirectionEnum
from enums.property_type import PropertyTypeEnum
from enums.transaction_type import TransactionTypeEnum


if __name__ == "__main__":
    # 컬럼 매핑
    main_table_column_mapping = {
        "zigbang": {
            "crawling_property_id": "item.itemId",
            "property_type": "item.serviceType",
            "transaction_type": "item.salesType",
            "province": "item.addressOrigin.local1",
            "city": "item.addressOrigin.local2",
            "dong": "item.addressOrigin.local3",
            "detail_address": "item.jibunAddress",
            "area": "item.area.전용면적M2",
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
            "bath_room_cnt": "item.bathroomCount",
            "room_cnt": "item.roomCount",
        },
    }

    tag_table_column_mapping = {
        "zigbang": {
            "parking_available": "item.parkingAvailableText",
            "pet_allowed": "item.petAllowed",
            "is_elevator": "item.elevator",
            "jeonse_loan": "item.jeonseLoanEligible",
            "nearby_pois": "item.neighborhoods.nearbyPois",
            "delivery_service": "item.neighborhoods.distributions",
            "amenity": "item.neighborhoods.amenities",
            "subway": "subways"
        }
    }

    property_details_dirs = {
        "zigbang": "./data/zigbang_property_details/*.txt",
        "naver": "./data/naver_property_details/*.txt",
    }

    # 직방 데이터 파싱 및 저장
    zigbang = ParsingZigbang(
        property_details_dirs["zigbang"],
        main_table_column_mapping["zigbang"],
        tag_table_column_mapping["zigbang"],
    )
    crawling_property_df, tag_df, map_df = zigbang.parse_data()
    insert_crawling_properties(crawling_property_df)
    # insert_tags(tag_df)
    # insert_mapping(map_df)