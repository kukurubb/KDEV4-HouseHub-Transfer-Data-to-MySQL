import json
import pandas as pd
import numpy as np
from typing import Any
from glob import glob
from enums.direction import map_zigbang_direction
from enums.property_type import map_zigbang_property_type
from enums.transaction_type import map_zigbang_transaction_type


'''
코드를 크롤링 매물
태그
연결맵 순서로
돌아가는 함수 세개를 짜야될거 같음
그리고 이렇게 하면 유니크값에 대응할 수 있을 것 같음
'''


class ParsingZigbang:
    def __init__(
        self,
        property_details_dir,
        main_table_column_mapping,
        tag_table_column_mapping,
    ):
        self.main_table_column_mapping = main_table_column_mapping
        self.tag_table_column_mapping = tag_table_column_mapping
        self.merged_column_mapping = main_table_column_mapping | tag_table_column_mapping
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
        
    def explode_column(self, data, column_name):
        if not isinstance(data, list):
            return []

        result = []
        for item in data:
            if column_name in item:
                result.append(item[column_name])
        
        return result
    
    # subway 컬럼 내부의 중복 데이터를 하나의 리스트로 만듦
    def explode_subway_data(self, subway_list):
        if not isinstance(subway_list, list):
            return []
        
        result = set()
        for item in subway_list:
            lines = item.split(",")
            result.update(lines)
        
        return list(result)
    
    # 태그 및 맵핑 데이터프레임 생성
    def create_tag_and_map_df(self, df):
        tag_rows = []
        mapping_rows = []
        tag_id_counter = 1
        tag_map = {}  # (type, value) -> tag_id

        # 처리 대상 컬럼 전부
        tag_columns = df.columns

        for idx, row in df.iterrows():
            property_id = row["crawling_property_id"]
            # print(property_id)
            # if idx > 1000:
            #     break
            
            for col in tag_columns:
                value = row[col]

                # 문자열로 저장된 리스트 처리
                if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                    try:
                        value = eval(value)
                    except:
                        value = []

                if not isinstance(value, list):
                    value = [value]

                for v in value:
                    key = (col, v)

                    if col == "crawling_property_id":
                        continue

                    if key not in tag_map:
                        tag_map[key] = tag_id_counter
                        tag_rows.append({"tag_id": tag_id_counter, "type": col, "value": v})
                        tag_id_counter += 1

                    tag_id = tag_map[key]
                    mapping_rows.append({
                        "id": len(mapping_rows) + 1,
                        "property_id": property_id,
                        "tag_id": tag_id
                    })

        tag_df = pd.DataFrame(tag_rows)
        mapping_df = pd.DataFrame(mapping_rows)
        return tag_df, mapping_df
    
    # 데이터 파싱
    def parse_data(self):
        parsed_rows = []

        for file_path in self.file_paths:
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    raw_data = json.load(f)
                except Exception:
                    continue

                # 파싱 수행
                row = {}
                for col, path in self.merged_column_mapping.items():
                    value = self.extract_nested(raw_data, path)
                    row[col] = value
                parsed_rows.append(row)

        # crawling_property_df 후처리 ------------------------------------------------------------------------------------------------------------------------------

        # 데이터프레임 생성
        crawling_property_columns = list(self.main_table_column_mapping.keys())
        tmp_df = pd.DataFrame(parsed_rows)
        crawling_property_df = tmp_df.loc[:, crawling_property_columns]

        # ENUM 변환
        crawling_property_df["direction"] = crawling_property_df["direction"].apply(map_zigbang_direction)
        crawling_property_df["transaction_type"] = crawling_property_df["transaction_type"].apply(map_zigbang_transaction_type)
        crawling_property_df["property_type"] = crawling_property_df["property_type"].apply(map_zigbang_property_type)

        # property_id 형식 변환
        crawling_property_df['crawling_property_id'] = crawling_property_df['crawling_property_id'].apply(lambda x: f"zigbang_{x}")        

        # pandas 데이터프레임 사용 시 null 값이 NaN으로 표시됨
        # mysql에서는 NaN을 None으로 인식하지 못하기 때문에 변경 수행
        print(crawling_property_df["crawling_property_id"].isna().sum())
        crawling_property_df = crawling_property_df.replace({np.nan: None})
        print(len(crawling_property_df))


        # print(crawling_property_df)
        # print("\n\n\n\n\n\n")

        # tag_df 및 map_df 생성 및 후처리 --------------------------------------------------------------------------------------------------------
        
        # 데이터프레임 생성
        tag_columns = ["crawling_property_id"] + list(self.tag_table_column_mapping.keys())
        tag_before_exploded_df = tmp_df.loc[:, tag_columns]
        tag_after_exploded_df = pd.DataFrame()

        # 1차 태그 데이터프레임 생성
        tag_after_exploded_df["crawling_property_id"] = tag_before_exploded_df["crawling_property_id"].apply(lambda x: f"zigbang_{x}")        
        tag_after_exploded_df["parking_available"] = tag_before_exploded_df["parking_available"].apply(lambda x: 1 if x == "주차 가능" else 0)
        tag_after_exploded_df["pet_allowed"] = tag_before_exploded_df["pet_allowed"].apply(lambda x: 1 if x == "Y" else 0)
        tag_after_exploded_df["is_elevator"] = tag_before_exploded_df["is_elevator"].apply(lambda x: 1 if x == "True" else 0)
        tag_after_exploded_df["jeonse_loan"] = tag_before_exploded_df["jeonse_loan"].apply(lambda x: 1 if x == "Y" else 0)
        tag_after_exploded_df["nearby_pois"] = tag_before_exploded_df["nearby_pois"].apply(lambda x: self.explode_column(x, "poiType"))
        tag_after_exploded_df["delivery_service"] = tag_before_exploded_df["delivery_service"].apply(lambda x: self.explode_column(x, "companyName"))
        tag_after_exploded_df["amenity"] = tag_before_exploded_df["amenity"].apply(lambda x: self.explode_column(x, "description"))
        tag_after_exploded_df["subway"] = tag_before_exploded_df["subway"].apply(lambda x: self.explode_column(x, "description"))
        tag_after_exploded_df["subway"] = tag_after_exploded_df["subway"].apply(lambda x: self.explode_subway_data(x))
        
        # df 및 map_df 생성
        tag_df, map_df = self.create_tag_and_map_df(tag_after_exploded_df)
        # print(tag_df)
        # print("\n\n\n\n\n")
        # print(map_df)

        # pandas 데이터프레임 사용 시 null 값이 NaN으로 표시됨
        # mysql에서는 NaN을 None으로 인식하지 못하기 때문에 변경 수행
        tag_df = tag_df.replace({np.nan: None})
        map_df = map_df.replace({np.nan: None})

        # 맵핑을 위해 아이디 삽입이 잘 되었는지 확인하는 코드
        valid_ids = set(crawling_property_df["crawling_property_id"])  # 먼저 삽입된 property들 기준
        map_df = map_df[map_df["property_id"].isin(valid_ids)]

        invalid_ids = set(map_df["property_id"]) - set(crawling_property_df["crawling_property_id"])
        print("❗️유효하지 않은 property_id들:", invalid_ids)


        return crawling_property_df, tag_df, map_df