# 파이썬 연산자 예제

print("파이썬 연산자 예제")
print("=" * 25)

# 1. 산술 연산자
print("1. 산술 연산자")
a = 15
b = 4

print(f"a = {a}, b = {b}")
print(f"a + b = {a + b}")      # 덧셈
print(f"a - b = {a - b}")      # 뺄셈
print(f"a * b = {a * b}")      # 곱셈
print(f"a / b = {a / b}")      # 나눗셈 (실수)
print(f"a // b = {a // b}")    # 나눗셈 (정수, 몫)
print(f"a % b = {a % b}")      # 나머지
print(f"a ** b = {a ** b}")    # 거듭제곱

# 2. 비교 연산자
print("\n2. 비교 연산자")
x = 10
y = 20

print(f"x = {x}, y = {y}")
print(f"x == y: {x == y}")     # 같음
print(f"x != y: {x != y}")     # 다름
print(f"x > y: {x > y}")       # 큼
print(f"x < y: {x < y}")       # 작음
print(f"x >= y: {x >= y}")     # 크거나 같음
print(f"x <= y: {x <= y}")     # 작거나 같음

# 3. 논리 연산자
print("\n3. 논리 연산자")
age = 25
has_license = True
is_student = False

print(f"나이: {age}, 면허증 소유: {has_license}, 학생: {is_student}")
print(f"성인이면서 면허가 있음: {age >= 18 and has_license}")
print(f"학생이거나 65세 이상: {is_student or age >= 65}")
print(f"학생이 아님: {not is_student}")

# 4. 할당 연산자
print("\n4. 할당 연산자")
score = 80
print(f"초기 점수: {score}")

score += 10    # score = score + 10
print(f"10점 추가 후: {score}")

score -= 5     # score = score - 5
print(f"5점 감점 후: {score}")

score *= 2     # score = score * 2
print(f"2배로 증가 후: {score}")

score //= 3    # score = score // 3
print(f"3으로 나눈 몫: {score}")

# 5. 문자열 연산자
print("\n5. 문자열 연산자")
first_name = "김"
last_name = "철수"

full_name = first_name + last_name  # 문자열 연결
print(f"이름 합치기: '{first_name}' + '{last_name}' = '{full_name}'")

greeting = "안녕하세요! "
repeated_greeting = greeting * 3    # 문자열 반복
print(f"인사말 반복: '{greeting}' * 3 = '{repeated_greeting}'")

# 6. 멤버십 연산자
print("\n6. 멤버십 연산자")
fruits = ["사과", "바나나", "오렌지"]
my_name = "홍길동"

print(f"과일 목록: {fruits}")
print(f"'사과'가 목록에 있나요? {'사과' in fruits}")
print(f"'포도'가 목록에 있나요? {'포도' in fruits}")
print(f"'딸기'가 목록에 없나요? {'딸기' not in fruits}")

print(f"이름: '{my_name}'")
print(f"'홍'이 이름에 있나요? {'홍' in my_name}")
print(f"'김'이 이름에 없나요? {'김' not in my_name}")

# 7. 실생활 예제 - 쇼핑몰 할인 계산
print("\n7. 실생활 예제 - 쇼핑몰 할인 계산")
original_price = 50000    # 원래 가격
discount_rate = 20        # 할인율 (%)
is_member = True         # 회원 여부
min_amount = 30000       # 최소 주문 금액

# 할인 금액 계산
discount_amount = original_price * discount_rate // 100
discounted_price = original_price - discount_amount

# 추가 회원 할인
if is_member:
    member_discount = discounted_price * 5 // 100
    final_price = discounted_price - member_discount
else:
    member_discount = 0
    final_price = discounted_price

# 무료 배송 조건 확인
free_shipping = final_price >= min_amount

print(f"원래 가격: {original_price:,}원")
print(f"할인율: {discount_rate}%")
print(f"할인 금액: {discount_amount:,}원")
print(f"할인 후 가격: {discounted_price:,}원")
print(f"회원 할인: {member_discount:,}원")
print(f"최종 가격: {final_price:,}원")
print(f"무료 배송 ({min_amount:,}원 이상): {free_shipping}")

# 8. 온도 변환 계산
print("\n8. 온도 변환 계산")
celsius = 25    # 섭씨 온도

# 섭씨를 화씨로 변환: F = C * 9/5 + 32
fahrenheit = celsius * 9 / 5 + 32
kelvin = celsius + 273.15

print(f"섭씨: {celsius}°C")
print(f"화씨: {fahrenheit}°F")
print(f"켈빈: {kelvin}K")

# 온도에 따른 날씨 판단
if celsius <= 0:
    weather = "매우 추움"
elif celsius <= 10:
    weather = "추움"
elif celsius <= 20:
    weather = "선선함"
elif celsius <= 30:
    weather = "따뜻함"
else:
    weather = "더움"

print(f"날씨: {weather}")

# 9. 연산자 우선순위 예제
print("\n9. 연산자 우선순위 예제")
result1 = 2 + 3 * 4      # 곱셈이 먼저 실행
result2 = (2 + 3) * 4    # 괄호가 먼저 실행
result3 = 10 / 2 * 3     # 좌에서 우로 실행
result4 = 2 ** 3 ** 2    # 거듭제곱은 우에서 좌로 실행

print(f"2 + 3 * 4 = {result1}")
print(f"(2 + 3) * 4 = {result2}")
print(f"10 / 2 * 3 = {result3}")
print(f"2 ** 3 ** 2 = {result4}")

print("\n연산자 예제 완료!")