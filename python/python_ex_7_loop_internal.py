import random

# 1부터 100 사이의 임의의 숫자를 정답으로 선택합니다.
secret_number = random.randint(1, 100)
attempts = 0 # 시도 횟수를 저장할 변수

print("1부터 100 사이의 숫자를 맞춰보세요!")

# while True와 break를 사용한 무한 루프 구조
while True:
    try:
        guess = int(input("추측한 숫자를 입력하세요: "))
        attempts += 1 # 시도 횟수 1 증가

        # if-elif-else를 사용하여 추측한 숫자와 정답을 비교
        if guess < secret_number:
            print("더 큰 숫자입니다! (Up)")
        elif guess > secret_number:
            print("더 작은 숫자입니다! (Down)")
        else: # guess == secret_number (정답을 맞춘 경우)
            print(f"정답입니다! {attempts}번 만에 맞추셨습니다.")
            break # while 루프를 탈출하여 게임을 종료합니다.

    except ValueError:
        print("오류: 숫자로만 입력해주세요.")