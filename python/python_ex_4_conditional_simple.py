# 파이썬 간단한 조건문 예제

print("파이썬 간단한 조건문 예제")
print("=" * 30)

# 1. 기본 if 문
print("1. 기본 if 문")
age = 20  # 나이 변수

if age >= 19:
    print(f"나이: {age}세, 성인입니다.")

print("프로그램 계속 실행...")

# 2. if-else 문
print("\n2. if-else 문")
score = 85  # 점수

if score >= 60:
    print(f"점수: {score}점, 합격입니다!")
else:
    print(f"점수: {score}점, 불합격입니다.")

# 3. 여러 조건 비교
print("\n3. 여러 조건 비교")
temperature = 25  # 온도

if temperature > 30:
    print("더워요!")
else:
    print("적당하거나 시원해요.")

# 4. 문자열 비교
print("\n4. 문자열 비교")
weather = "맑음"

if weather == "맑음":
    print("좋은 날씨입니다!")
else:
    print("날씨가 좋지 않네요.")

# 5. 불리언 값 사용
print("\n5. 불리언 값 사용")
is_raining = False

if is_raining:
    print("우산을 가져가세요.")
else:
    print("우산이 필요 없어요.")

# 6. 숫자 비교
print("\n6. 숫자 비교")
number = 15

if number % 2 == 0:
    print(f"{number}는 짝수입니다.")
else:
    print(f"{number}는 홀수입니다.")

print("\n조건문 예제 완료!")