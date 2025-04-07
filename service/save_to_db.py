from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from entity.base import Base
from entity.crawling_property import CrawlingProperty
from entity.crawling_property_tag_map import CrawlingPropertyTagMap
from entity.tags import Tag
from enums.direction import DirectionEnum
from enums.property_type import PropertyTypeEnum
from enums.transaction_type import TransactionTypeEnum
import pandas as pd
import traceback


"""
코드 겹치는 부분 리팩토링 필요!!!!!!!!!!!!!!!
"""

def insert_crawling_properties(df):
    # DB 연결
    DATABASE_URL = "mysql+mysqlconnector://root:rootpass@localhost:3306/testdb"
    engine = create_engine(DATABASE_URL, echo=True)

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
                crawling_property_id=row["crawling_property_id"],
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

def insert_tags(df):
    # DB 연결
    DATABASE_URL = "mysql+mysqlconnector://root:rootpass@localhost:3306/testdb"
    engine = create_engine(DATABASE_URL, echo=True)

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
                # tag_id=row["tag_id"],
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

def insert_mapping(df):
    # DB 연결
    DATABASE_URL = "mysql+mysqlconnector://root:rootpass@localhost:3306/testdb"
    engine = create_engine(DATABASE_URL, echo=True)

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
                # id=row["id"],
                property_id=row["property_id"],
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