# 파이썬 변수 사용법 예제

# 1. 기본 변수 선언 및 값 할당
name = "김철수"  # 문자열 변수
age = 25        # 정수 변수
height = 175.5  # 실수 변수
is_student = True  # 불리언 변수

print(f"이름: {name}")
print(f"나이: {age}")
print(f"키: {height}cm")
print(f"학생 여부: {is_student}")

# 2. 변수 타입 확인
print(f"name의 타입: {type(name)}")
print(f"age의 타입: {type(age)}")
print(f"height의 타입: {type(height)}")
print(f"is_student의 타입: {type(is_student)}")

# 3. 변수 값 변경
age = 26
is_student = False
print(f"변경 후 나이: {age}")
print(f"변경 후 학생 여부: {is_student}")

# 4. 여러 변수에 동시 할당
print("\n4. 여러 변수에 동시 할당")
x = y = z = 10
print(f"x = {x}, y = {y}, z = {z}")

a, b, c = 1, 2, 3
print(f"a = {a}, b = {b}, c = {c}")

# 5. 변수 이름 규칙 예제
print("\n5. 변수 이름 규칙 예제")
student_name = "이영희"      # 좋은 예: 소문자와 언더스코어
student_age = 20
max_score = 100
is_passed = True

print(f"학생 이름: {student_name}")
print(f"학생 나이: {student_age}")
print(f"최고 점수: {max_score}")
print(f"합격 여부: {is_passed}")

# 6. 문자열 변수 활용
print("\n6. 문자열 변수 활용")
first_name = "홍"
last_name = "길동"
full_name = first_name + last_name
print(f"성: {first_name}")
print(f"이름: {last_name}")
print(f"전체 이름: {full_name}")

greeting = "안녕하세요, "
message = greeting + full_name + "님!"
print(f"인사말: {message}")

# 7. 숫자 변수 계산
print("\n7. 숫자 변수 계산")
korean_score = 85
english_score = 90
math_score = 95

total_score = korean_score + english_score + math_score
average_score = total_score / 3

print(f"국어: {korean_score}점")
print(f"영어: {english_score}점")
print(f"수학: {math_score}점")
print(f"총점: {total_score}점")
print(f"평균: {average_score:.1f}점")

# 8. 실생활 예제 - 쇼핑 계산기
print("\n8. 실생활 예제 - 쇼핑 계산기")
apple_price = 1000      # 사과 개당 가격
apple_count = 5         # 사과 개수
banana_price = 1500     # 바나나 개당 가격
banana_count = 3        # 바나나 개수

apple_total = apple_price * apple_count
banana_total = banana_price * banana_count
total_amount = apple_total + banana_total

print(f"사과 {apple_count}개: {apple_total}원")
print(f"바나나 {banana_count}개: {banana_total}원")
print(f"총 금액: {total_amount}원")

# 9. 변수 교환
print("\n9. 변수 교환")
num1 = 10
num2 = 20

print(f"교환 전: num1 = {num1}, num2 = {num2}")

# 파이썬에서는 쉽게 변수를 교환할 수 있습니다
num1, num2 = num2, num1

print(f"교환 후: num1 = {num1}, num2 = {num2}")

print("\n변수 예제 완료!")