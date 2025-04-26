from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from entity.html_source import HtmlSource, Base
import pandas as pd
import traceback


def upload_html_source(df: pd.DataFrame, database_url: str):
    # DB 연결
    DATABASE_URL = database_url
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
            data = HtmlSource(
                crawling_propertiy_id=row["crawling_propertiy_id"],
                html_source=row["html_source"],
                is_error=row["is_error"],
                is_parsed=row["is_parsed"],
            )
            db.append(data)
            
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


def a():


    
    batches = make_batches(html_source_dir, batch_size=batch_size)