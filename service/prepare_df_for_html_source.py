from service.utils import make_batches, get_file_name
from service.check_naver_error_html import check_error_in_file

import pandas as pd
import json

def prepare_df_for_html_source(file_paths, html_source_dir, batch_size, company_name):
    """
    1. 배치화를 한다.
    2. 에러체크를 수행한다.
    3. 매물 id 이름을 뽑는다.
    3. html을 업로드한다.
    """

    batches = make_batches(html_source_dir, batch_size=batch_size)

    # HTML 소스 파일 업로드
    df = pd.DataFrame(
        columns=[
            "crawling_propertiy_id",
            "html_source",
            "is_error",
            "is_parsed",
        ]
    )

    data = []
    for file_path in file_paths:            
        with open(file_path, "r", encoding="utf-8-sig") as f:
            html_source = json.load(f)

            # 에러 체크
            status = check_error_in_file(
                html_source,
                error_code="errorCode.NotExistInformation",
                error_message="해당하는 매물 정보가 존재하지 않습니다."
            )

            # html_sources 테이블 데이터 생성
            crawling_property_id = get_file_name(file_path)
            file_name = f"{company_name}_{crawling_property_id}"
            data.append([file_name, html_source, status, "False"])

        # 배치 종료 후 데이터베이스 업로드 수행
