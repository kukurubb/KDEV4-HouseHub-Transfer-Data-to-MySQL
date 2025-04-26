import glob
import os
import numpy as np
from typing import List

# 균등하게 나누는 코드 말고 나머지로 처리하는 코드로 변경
def make_batches(html_source_dir: str, batch_size: int = 1000) -> List[List[str]]:
    """
    디렉토리 내의 txt 파일들을 배치 단위로 나누는 함수
    
    Args:
        directory_path: txt 파일들이 있는 디렉토리 경로
        batch_size: 배치 크기 (기본값: 1000)
        
    Returns:
        List[List[str]]: 파일 경로들을 배치로 나눈 리스트
    """

    # 디렉토리 내의 모든 txt 파일 경로 수집
    html_source_files = glob.glob(os.path.join(html_source_dir, "*.txt"))
    
    # 파일이 없는 경우 빈 리스트 반환
    if not html_source_files:
        return []
    
    # 파일 리스트를 배치 크기로 나누기
    return np.array_split(html_source_files, np.ceil(len(html_source_files) / batch_size))