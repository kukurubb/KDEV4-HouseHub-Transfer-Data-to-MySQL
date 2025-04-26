import json
import pandas as pd
import numpy as np
from typing import Any
from glob import glob
from enums.direction import map_naver_direction
from enums.property_type import map_naver_property_type
from enums.transaction_type import map_naver_transaction_type

"""
최종적으로 df 3개가 반환되어야 함
"""
class ParsingNaver:
    def __init__(
        self,
        main_table_column_mapping,
        tag_table_column_mapping,
    ):
        self.main_table_column_mapping = main_table_column_mapping
        self.tag_table_column_mapping = tag_table_column_mapping
        self.merged_column_mapping = main_table_column_mapping | tag_table_column_mapping

    # 중첩 키 추출 유틸 함수
    def extract_nested(self, data: dict, json_key: str) -> Any:
        """
        중첩된 딕셔너리에서 점(.)으로 구분된 경로를 따라 값을 추출하는 함수

        Args:
            data (dict): 파싱할 중첩 딕셔너리 데이터
            json_key (str): 추출할 값의 경로 (예: "articleDetail.articleNo")

        Returns:
            Any: 추출된 값. 경로가 존재하지 않을 경우 None 반환

        Example:
            data = {
                "a": {
                    "b": {
                        "c": 123
                    }
                }
            }
            json_key = "a.b.c"

            return value = 123
        """
        for key in json_key.split("."):
            data = data.get(key, None)
            if data is None:
                return None
            
        return data

    def convert_json_to_df(self, file_paths):
        """
        merged_column_mapping 에 따라 데이터 파싱
        후처리 별도 적용
        """
        parsed_rows = []
        for file_path in file_paths:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                row = {
                    column_name: self.extract_nested(raw_data, json_key)
                    for column_name, json_key in self.merged_column_mapping.items()
                }
                parsed_rows.append(row)

        return pd.DataFrame(parsed_rows)

    def post_process(self, df):
        # null 값이 테이블 제거 ------------------------------------------------------------------------------------
        df = df.dropna(subset=["property_type", "transaction_type", "province", "city", "area", "direction"])

        # transaction_type에서 단기임대 항목 제거(추후 협의를 통해 사용 여부 변동 가능)
        df = df[df["transaction_type"] != "단기임대"]

        # 매물 데이터 후처리 ---------------------------------------------------------------------------------------
        # ENUM 변환
        df["direction"] = df["direction"].apply(map_naver_direction)
        df["transaction_type"] = df["transaction_type"].apply(map_naver_transaction_type)
        df["property_type"] = df["property_type"].apply(map_naver_property_type)

        # crawling_properties_id 형식 변환
        df['crawling_properties_id'] = df['crawling_properties_id'].apply(lambda x: f"naver_{x}")

        # room_cnt 형식 변환
        df['room_cnt'] = df['room_cnt'].apply(lambda x: '0' if str(x).strip() == '-' else x)
        df['room_cnt'] = df['room_cnt'].astype(int)

        # bath_room_cnt 형식 변환
        df['bath_room_cnt'] = df['bath_room_cnt'].apply(lambda x: '0' if str(x).strip() == '-' else x)
        df['bath_room_cnt'] = df['bath_room_cnt'].astype(int)

        # # detail_address 형식 변환(사용x)
        # df["detail_address"] = df["detail_address"].apply(lambda x: str(x).split()[-1] if pd.notnull(x) else x)

        # 태그 데이터 후처리 ---------------------------------------------------------------------------------------
        # 주차 가능 여부 형식 변환
        df["주차 가능 여부"] = df["주차 가능 여부"].apply(lambda x: "주차 가능" if x == "Y" else "주차 불가능")

        # 옥탑방 여부 형식 변환
        df["옥탑방 여부"] = df["옥탑방 여부"].apply(lambda x: "옥탑방 유" if x == "Y" else "옥탑방 무")

        # pandas 데이터프레임 사용 시 null 값이 NaN으로 표시됨
        # mysql에서는 NaN을 None으로 인식하지 못하기 때문에 변경 수행
        df = df.replace({np.nan: None})

        return df
    
    def create_dfs(self, df, tags_dict):
        # 태그 value로 태그 유형을 찾기 위한 dictionary 생성
        tag_value_to_type = {}
        for tag_type, tag_values in tags_dict.items():
            for tag_value in tag_values:
                tag_value_to_type[tag_value] = tag_type

        # crawling_properties 테이블 생성
        crawling_properties_df = df.drop(
            columns=[
                "주차 가능 여부",
                "옥탑방 여부",
                "보안 시설",
                "생활 시설",
                "부대 시설",
            ]
        )

        # tags 테이블 생성
        tags_df = pd.DataFrame(
            columns=["tag_id", "type", "value"]
        )
        for idx, (tag_value, tag_type) in enumerate(tag_value_to_type.items()):
             tag_id = idx + 1
             tags_df.loc[idx] = [tag_id, tag_type, tag_value]

        # crawling_property_tag_map 테이블 생성
        """
        어떻게 동작하면 되는가?
        1. crawling_properties 테이블에서 각 파트의 값을 읽는다.
        2. 펼친다.
        3. 펼친 값을 태그 테이블에서 찾는다.
        4. 찾은 태그의 태그 id를 crawling_property_tag_map 테이블에 추가한다.
        """
        crawling_property_tag_map_df = pd.DataFrame(
            columns=["crawling_properties_id", "tag_id"]
        )
        idx = 0
        for _, row in df.iterrows():
            crawling_properties_id = row["crawling_properties_id"]
            
            # 주차 가능 여부
            tag_id = tags_df[tags_df["value"] == row["주차 가능 여부"]]["tag_id"]
            if not tag_id.empty:
                crawling_property_tag_map_df.loc[idx] = [crawling_properties_id, tag_id.values[0]]
                idx += 1

            # 옥탑방 여부
            tag_id = tags_df[tags_df["value"] == row["옥탑방 여부"]]["tag_id"]
            if not tag_id.empty:
                crawling_property_tag_map_df.loc[idx] = [crawling_properties_id, tag_id.values[0]]
                idx += 1

            # 보안 시설
            values = row["보안 시설"]
            if values:
                for value in values:
                    tag_id = tags_df[tags_df["value"] == value]["tag_id"]
                    if not tag_id.empty:
                        crawling_property_tag_map_df.loc[idx] = [crawling_properties_id, tag_id.values[0]]
                        idx += 1

            # 생활 시설
            values = row["생활 시설"]
            if values:
                for value in values:
                    tag_id = tags_df[tags_df["value"] == value]["tag_id"]
                    if not tag_id.empty:
                        crawling_property_tag_map_df.loc[idx] = [crawling_properties_id, tag_id.values[0]]
                        idx += 1

            # 부대 시설
            values = row["부대 시설"]
            if values:
                for value in values:
                    tag_id = tags_df[tags_df["value"] == value]["tag_id"]
                    if not tag_id.empty:
                        crawling_property_tag_map_df.loc[idx] = [crawling_properties_id, tag_id.values[0]]
                        idx += 1

            # 방 개수
            room_cnt = int(row["room_cnt"])
            if room_cnt == 1:
                value = "원룸"
            elif room_cnt == 2:
                value = "투룸"
            elif room_cnt == 3:
                value = "쓰리룸"
            elif room_cnt >= 4:
                value = "포룸 이상"

            tag_id = tags_df[tags_df["value"] == value]["tag_id"]   
            if not tag_id.empty:
                crawling_property_tag_map_df.loc[idx] = [crawling_properties_id, tag_id.values[0]]
                idx += 1
                
        # 디버그 용 코드
        # crawling_properties_df.to_csv(r"D:\Kernel360_final_project\transfer_data_to_mysql2\crawling_properties_df.csv")
        # crawling_property_tag_map_df.to_csv(r"D:\Kernel360_final_project\transfer_data_to_mysql2\crawling_property_tag_map_df.csv")

        return crawling_properties_df, crawling_property_tag_map_df, tags_df
    
    def parse_data(self, file_paths, tags_dict):
        df = self.convert_json_to_df(file_paths)
        df = self.post_process(df)
        crawling_properties_df, crawling_property_tag_map_df, tags_df = self.create_dfs(df, tags_dict)

        return crawling_properties_df, crawling_property_tag_map_df, tags_df