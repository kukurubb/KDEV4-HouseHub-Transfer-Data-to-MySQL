def check_error_in_file(html_source, error_code, error_message):
    """
    HTML 소스의 에러 상태를 확인하는 함수

    Args:
        html_source (dict): 확인할 HTML 소스 데이터 딕셔너리
        error_code (str): 확인할 에러 코드
        error_message (str): 확인할 에러 메시지

    Returns:
        str: 
            - "Error": error 키가 존재하고 code나 message가 일치하는 경우
            - "Success": error 키가 없거나 code와 message가 모두 일치하지 않는 경우

    Note:
        - html_source.get("error")가 None인 경우 "Success" 반환
        - error 키가 존재하고 code나 message가 일치하면 "Error" 반환
    """

    error = html_source.get("error")
    if error:
        if error.get("code") == error_code:
            return "Error"
        
        elif error.get("message") == error_message:
            return "Error"
        
    return "Success"