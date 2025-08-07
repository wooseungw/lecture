# 시스템에 저장된 정확한 아이디와 비밀번호
CORRECT_ID = "python_user"
CORRECT_PW = "12345"

# 사용자로부터 아이디를 입력받습니다.
user_id = input("아이디를 입력하세요: ")

# 첫 번째 조건문: 아이디 일치 여부 확인
if user_id == CORRECT_ID:
    # 아이디가 일치하는 경우, 비밀번호를 입력받습니다.
    user_pw = input("비밀번호를 입력하세요: ")

    # 두 번째 (중첩된) 조건문: 비밀번호 일치 여부 확인
    if user_pw == CORRECT_PW:
        print("로그인 성공!")
    else:
        print("비밀번호가 틀렸습니다.")
else:
    # 첫 번째 조건(아이디)이 거짓인 경우
    print("존재하지 않는 아이디입니다.")