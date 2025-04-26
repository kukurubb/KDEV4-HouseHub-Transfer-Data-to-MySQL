from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import traceback

from entity.base import Base
from entity.crawling_property import CrawlingProperty
from entity.crawling_property_tag_map import CrawlingPropertyTagMap
from entity.tag import Tag

from common.utils.batchfy import make_batches
from common.utils.check_error import check_error_in_file

import pandas as pd
import json

def insert_crawling_properties(df, database_url):
    # DB 연결
    engine = create_engine(database_url, echo=True)

    # 테이블 생성
    Base.metadata.create_all(engine)

    # 세션 팩토리 생성
    SessionLocal = sessionmaker(bind=engine)

    # 세션 인스턴스 생성
    session = SessionLocal()

    # DB 삽입
    try:
        db = []

        for _, row in df.iterrows():
            property = CrawlingProperty(
                crawling_properties_id=row["crawling_properties_id"],
                property_type=row["property_type"],
                transaction_type=row["transaction_type"],
                province=row["province"],
                city=row["city"],
                dong=row["dong"],
                detail_address=row["detail_address"],
                area=row["area"],
                floor=row["floor"],
                all_floors=row["all_floors"],
                sale_price=row["sale_price"],
                deposit=row["deposit"],
                monthly_rent_fee=row["monthly_rent_fee"],
                direction=row["direction"],
                real_estate_agent_id=row["real_estate_agent_id"],
                real_estate_agent_name=row["real_estate_agent_name"],
                real_estate_agent_contact=row["real_estate_agent_contact"],
                real_estate_office_name=row["real_estate_office_name"],
                real_estate_office_address=row["real_estate_office_address"],
                bath_room_cnt=row["bath_room_cnt"],
                room_cnt=row["room_cnt"],
            )
            db.append(property)
            
        session.add_all(db)
        
        try:
            session.commit()
            print(f"✅ 데이터 삽입 완료! ({len(db)}건)")
        except Exception as commit_error:
            session.rollback()
            print("❌ 커밋 중 에러 발생:", commit_error)
            traceback.print_exc()

    except Exception as e:
        session.rollback()
        print("❌ 데이터 처리 중 에러 발생:", e)
        traceback.print_exc()
    finally:
        session.close()

def insert_tags(df, database_url):
    # DB 연결
    engine = create_engine(database_url, echo=True)

    # 테이블 생성
    Base.metadata.create_all(engine)

    # 세션 팩토리 생성
    SessionLocal = sessionmaker(bind=engine)

    # 세션 인스턴스 생성
    session = SessionLocal()

    # DB 삽입
    try:
        db = []

        for _, row in df.iterrows():
            tag = Tag(
                type=row["type"],
                value=row["value"]
            )
            db.append(tag)
            
        session.add_all(db)
        
        try:
            session.commit()
            print(f"✅ 데이터 삽입 완료! ({len(db)}건)")
        except Exception as commit_error:
            session.rollback()
            print("❌ 커밋 중 에러 발생:", commit_error)
            traceback.print_exc()

    except Exception as e:
        session.rollback()
        print("❌ 데이터 처리 중 에러 발생:", e)
        traceback.print_exc()
    finally:
        session.close()

def insert_mapping(df, database_url):
    # DB 연결
    engine = create_engine(database_url, echo=True)

    # 테이블 생성
    Base.metadata.create_all(engine)

    # 세션 팩토리 생성
    SessionLocal = sessionmaker(bind=engine)

    # 세션 인스턴스 생성
    session = SessionLocal()

    # DB 삽입
    try:
        db = []
        for _, row in df.iterrows():
            mapping = CrawlingPropertyTagMap(
                crawling_properties_id=row["crawling_properties_id"],
                tag_id=row["tag_id"]
            )
            db.append(mapping)
            
        session.add_all(db)

        try:
            session.commit()
            print(f"✅ 데이터 삽입 완료! ({len(db)}건)")
        except Exception as commit_error:
            session.rollback()
            print("❌ 커밋 중 에러 발생:", commit_error)
            traceback.print_exc()

    except Exception as e:
        session.rollback()
        print("❌ 데이터 처리 중 에러 발생:", e)
        traceback.print_exc()
    finally:
        session.close()
        
"""
1. 배치화
2. 에러체크
3. 파싱
4. 업로드

원래는 데이터베이스에서 데이터를 끌고와서 작업을 해야하지만
지금은 바쁘니까 로컬 파일에서 직접 작업한다.

나중에 코드 변경할 것
"""
def upload_parsed_data(parser, tags_dict, crawling_source_dir, database_url, batch_size):
    trig = True

    batches = make_batches(crawling_source_dir, batch_size=batch_size)

    for file_paths in batches:
        success_file_paths = []
        for file_path in file_paths:            
            with open(file_path, "r", encoding="utf-8-sig") as f:
                crawling_source = json.load(f)

                # 에러 체크
                status = check_error_in_file(
                    crawling_source,
                    error_code="errorCode.NotExistInformation",
                    error_message="해당하는 매물 정보가 존재하지 않습니다."
                )

                # 성공인 경우만 경로 수집
                if status == "Success":
                    success_file_paths.append(file_path)

        # 성공한 데이터에 대한 파싱 수행
        crawling_properties_df, crawling_property_tag_map_df, tags_df = parser.parse_data(success_file_paths, tags_dict)

        # 데이터베이스 업로드
        insert_crawling_properties(crawling_properties_df, database_url)

        if trig:
            insert_tags(tags_df, database_url)
            trig = False

        insert_mapping(crawling_property_tag_map_df, database_url)