import json
import pandas as pd
import numpy as np
from typing import Any
from glob import glob
from enums.direction import map_naver_direction
from enums.property_type import map_naver_property_type
from enums.transaction_type import map_naver_transaction_type


class ParsingNaver:
    def __init__(self, property_details_dir, column_mapping):
        self.column_mapping = column_mapping
        self.file_paths = glob(property_details_dir)

    # 중첩 키 추출 유틸 함수
    def extract_nested(self, data: dict, path: str) -> Any:
        try:
            for key in path.split("."):
                data = data.get(key, None)
                if data is None:
                    return None
            return data
        except Exception:
            return None

    # 데이터 파싱
    def parse_data(self):
        parsed_rows = []
        for file_path in self.file_paths:
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    raw_data = json.load(f)
                except Exception:
                    continue
                row = {
                    col: self.extract_nested(raw_data, path)
                    for col, path in self.column_mapping.items()
                }
                parsed_rows.append(row)

        # 데이터프레임 생성
        df = pd.DataFrame(parsed_rows)

        # ENUM 변환
        df["direction"] = df["direction"].apply(map_naver_direction)
        df["transaction_type"] = df["transaction_type"].apply(map_naver_transaction_type)
        df["property_type"] = df["property_type"].apply(map_naver_property_type)

        # property_id 형식 변환
        df['crawling_properties_id'] = df['crawling_properties_id'].apply(lambda x: f"naver_{x}")

        # room_cnt 형식 변환
        df['room_cnt'] = df['room_cnt'].apply(lambda x: '0' if str(x).strip() == '-' else x)
        df['room_cnt'] = df['room_cnt'].astype(int)

        # bath_room_cnt 형식 변환
        df['bath_room_cnt'] = df['bath_room_cnt'].apply(lambda x: '0' if str(x).strip() == '-' else x)
        df['bath_room_cnt'] = df['bath_room_cnt'].astype(int)

        # # detail_address 주소 변환(사용x)
        # df["detail_address"] = df["detail_address"].apply(lambda x: str(x).split()[-1] if pd.notnull(x) else x)

        # pandas 데이터프레임 사용 시 null 값이 NaN으로 표시됨
        # mysql에서는 NaN을 None으로 인식하지 못하기 때문에 변경 수행
        df = df.replace({np.nan: None})

        return df