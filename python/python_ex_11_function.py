# 파이썬 함수 기본 사용법 예제

def print_gugudan(dan):
    """
    하나의 정수(dan)를 매개변수로 받아,
    해당 단의 구구단을 출력하는 함수입니다.
    """
    print(f"--- {dan}단 ---")
    for i in range(1, 10):
        print(f"{dan} x {i} = {dan * i}")

# 여기서부터 프로그램의 메인 로직 시작

# 1. 사용자 입력을 처리하는 부분
input_dan = int(input("출력할 구구단의 단(2~9)을 입력하세요: "))

# 2. 입력값의 유효성을 검사하는 부분
if 2 <= input_dan <= 9:
    # 3. 유효한 경우, 정의된 함수를 호출하는 부분
    print_gugudan(input_dan)
else:
    print("오류: 2에서 9 사이의 숫자만 입력해주세요.")