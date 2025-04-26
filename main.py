from service.upload_parsed_data import upload_parsed_data
from service.parse_naver import ParsingNaver


if __name__ == "__main__":
    # 컬럼 매핑
    main_table_column_mapping = {
        "zigbang": {
            "crawling_properties_id": "item.itemId",
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
        "naver": {
            "crawling_properties_id": "articleDetail.articleNo",
            "property_type": "articleDetail.realestateTypeName",
            "transaction_type": "articleDetail.tradeTypeName",
            "province": "articleDetail.cityName",
            "city": "articleDetail.divisionName",
            "dong": "articleDetail.sectionName",
            "detail_address": "articleDetail.exposureAddress",
            "area": "articleSpace.exclusiveSpace",
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
            "bath_room_cnt": "articleDetail.roomCount",
            "room_cnt": "articleDetail.bathroomCount",
        },
    }
    
    # 말이 매핑이지 실제로는 매핑이 불가능한 컬럼들...
    tag_table_column_mapping = {
        # "zigbang": {
        #     "parking_available": "item.parkingAvailableText",
        #     "pet_allowed": "item.petAllowed",
        #     "is_elevator": "item.elevator",
        #     "jeonse_loan": "item.jeonseLoanEligible",
        #     "nearby_pois": "item.neighborhoods.nearbyPois",
        #     "delivery_service": "item.neighborhoods.distributions",
        #     "amenity": "item.neighborhoods.amenities",
        #     "subway": "subways"
        # },
        "naver": {
            "주차 가능 여부": "articleDetail.parkingPossibleYN",
            "옥탑방 여부": "articleOneroom.roofTopYN",
            "보안 시설": "articleFacility.securityFacilities",
            "생활 시설": "articleFacility.lifeFacilities",
            "부대 시설": "articleFacility.etcFacilities",
        }
    }

    tags_dict = {
        "naver": {
            "주차 가능 여부": ["주차 가능", "주차 불가능"],
            "옥탑방 여부": ["옥탑방 유", "옥탑방 무"],
            "보안 시설": ["비디오폰", "카드키", "CCTV", "경비원"],
            "생활 시설": ["침대", "세탁기", "싱크대", "TV", "냉장고"],
            "부대 시설": ["엘리베이터", "무인택배함", "테라스"],
            "방 개수": ["원룸", "투룸", "쓰리룸", "포룸"],
        }
    }


    # 연결 URL 구성
    username = "admin"
    password = "!a2497199"
    host = "househub.cv4m8y6uo0gz.ap-northeast-2.rds.amazonaws.com"
    port = 3306
    db_name = "househub_db"

    database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
    database_url = "mysql+mysqlconnector://root:rootpass@localhost:3306/testdb"

    # crawling_source_dir = {
    #     "zigbang": "./data/zigbang_property_details",
    #     "naver": r"D:\Kernel360_final_project\1. crawled_data\naver_seoul_v1\property_list\seoul_1_1",
    # }
    crawling_source_dir = {
        # "naver": r"D:\Kernel360_final_project\1. crawled_data\daejeon\property_list",
        # "naver": r"D:\Kernel360_final_project\1. crawled_data\naver_seoul_v1\property_list\seoul_1_1",
        "naver": r"D:\Kernel360_final_project\1. crawled_data\naver_seoul_v1\property_list\seoul_4_2",
    }
    
    # 네이버 데이터 파싱 및 저장
    naver_parser = ParsingNaver(
        main_table_column_mapping["naver"],
        tag_table_column_mapping["naver"]
    )
    upload_parsed_data(
        naver_parser,
        tags_dict["naver"],
        crawling_source_dir["naver"],
        database_url,
        batch_size=1000
    )