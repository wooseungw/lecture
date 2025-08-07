# 파이썬 형변환(타입 변환) 예제

print("파이썬 형변환 예제")
print("=" * 25)

# 1. 기본 변수들
print("1. 기본 변수들")
score = 95
height = 175.5
name = "김철수"
is_student = True

print(f"점수: {score} ({type(score)})")
print(f"키: {height} ({type(height)})")
print(f"이름: {name} ({type(name)})")
print(f"학생 여부: {is_student} ({type(is_student)})")

# 2. 정수 → 다른 타입으로 변환
print("\n2. 정수 → 다른 타입으로 변환")
score_str = str(score)          # 정수 → 문자열
score_float = float(score)      # 정수 → 실수
score_bool = bool(score)        # 정수 → 불리언

print(f"정수 → 문자열: {score_str} ({type(score_str)})")
print(f"정수 → 실수: {score_float} ({type(score_float)})")
print(f"정수 → 불리언: {score_bool} ({type(score_bool)})")

# 3. 실수 → 다른 타입으로 변환
print("\n3. 실수 → 다른 타입으로 변환")
height_str = str(height)        # 실수 → 문자열
height_int = int(height)        # 실수 → 정수 (소수점 버림)
height_bool = bool(height)      # 실수 → 불리언

print(f"실수 → 문자열: {height_str} ({type(height_str)})")
print(f"실수 → 정수: {height_int} ({type(height_int)})")
print(f"실수 → 불리언: {height_bool} ({type(height_bool)})")

# 4. 문자열 → 다른 타입으로 변환
print("\n4. 문자열 → 다른 타입으로 변환")
number_str = "123"
price_str = "45.99"
empty_str = ""

number_int = int(number_str)      # 문자열 → 정수
price_float = float(price_str)    # 문자열 → 실수
name_bool = bool(name)            # 문자열 → 불리언 (빈 문자열이 아니면 True)
empty_bool = bool(empty_str)      # 빈 문자열 → 불리언 (False)

print(f"'{number_str}' → 정수: {number_int} ({type(number_int)})")
print(f"'{price_str}' → 실수: {price_float} ({type(price_float)})")
print(f"'{name}' → 불리언: {name_bool} ({type(name_bool)})")
print(f"빈 문자열 → 불리언: {empty_bool} ({type(empty_bool)})")

# 5. 불리언 → 다른 타입으로 변환
print("\n5. 불리언 → 다른 타입으로 변환")
true_str = str(True)            # 불리언 → 문자열
false_str = str(False)
true_int = int(True)            # True → 1
false_int = int(False)          # False → 0
true_float = float(True)        # True → 1.0

print(f"True → 문자열: '{true_str}' ({type(true_str)})")
print(f"False → 문자열: '{false_str}' ({type(false_str)})")
print(f"True → 정수: {true_int} ({type(true_int)})")
print(f"False → 정수: {false_int} ({type(false_int)})")
print(f"True → 실수: {true_float} ({type(true_float)})")

# 6. 실생활 예제 - 나이 입력받기 (시뮬레이션)
print("\n6. 실생활 예제 - 나이 계산")
birth_year_str = "1998"  # 실제로는 input()으로 받을 값
current_year = 2024

birth_year = int(birth_year_str)  # 문자열을 정수로 변환
age = current_year - birth_year

print(f"태어난 년도: {birth_year_str} (문자열)")
print(f"변환된 년도: {birth_year} (정수)")
print(f"현재 나이: {age}살")

# 7. 계산 결과 문자열로 만들기
print("\n7. 계산 결과 문자열로 만들기")
math_score = 85
english_score = 92
total = math_score + english_score
average = total / 2

# 숫자를 문자열로 변환하여 메시지 만들기
result_message = "수학: " + str(math_score) + "점, 영어: " + str(english_score) + "점"
average_message = "평균: " + str(round(average, 1)) + "점"

print(result_message)
print(average_message)

# f-string을 사용하면 자동으로 형변환됨
print(f"총점: {total}점, 평균: {average:.1f}점")

# 8. 0과 빈 값들의 불리언 변환
print("\n8. 0과 빈 값들의 불리언 변환")
values = [0, 1, -1, 0.0, 3.14, "", "hello", [], [1, 2, 3]]

print("값들을 불리언으로 변환:")
for value in values:
    print(f"{repr(value)} → {bool(value)}")

# 9. 형변환 활용 - 점수 등급 계산
print("\n9. 형변환 활용 - 점수 등급 계산")
score_input = "87"  # 입력받은 점수 (문자열)
score_num = int(score_input)  # 정수로 변환

if score_num >= 90:
    grade = "A"
elif score_num >= 80:
    grade = "B"
elif score_num >= 70:
    grade = "C"
else:
    grade = "F"

print(f"입력 점수: '{score_input}' (문자열)")
print(f"변환 점수: {score_num} (정수)")
print(f"등급: {grade}")

print("\n형변환 예제 완료!")
