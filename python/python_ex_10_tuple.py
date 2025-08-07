# 파이썬 튜플 예제

print("파이썬 튜플 예제")
print("=" * 20)

# 1. 튜플 생성
print("1. 튜플 생성")
coordinates = (10, 20)  # 좌표 (x, y)
colors = ("빨강", "초록", "파랑")
mixed = ("안녕", 123, True, 3.14)
single_item = (42,)  # 단일 요소 튜플 (쉼표 필요!)

print(f"좌표 튜플: {coordinates}")
print(f"색상 튜플: {colors}")
print(f"혼합 튜플: {mixed}")
print(f"단일 요소 튜플: {single_item}")

# 괄호 없이도 튜플 생성 가능
no_parentheses = 1, 2, 3
print(f"괄호 없는 튜플: {no_parentheses}")

# 2. 튜플 요소 접근 (인덱스 사용)
print("\n2. 튜플 요소 접근")
print(f"x 좌표: {coordinates[0]}")
print(f"y 좌표: {coordinates[1]}")
print(f"첫 번째 색상: {colors[0]}")
print(f"마지막 색상: {colors[-1]}")
print(f"두 번째부터 끝까지: {colors[1:]}")

# 3. 튜플은 수정할 수 없음 (불변성)
print("\n3. 튜플의 불변성")
print("튜플은 생성 후 수정할 수 없습니다.")
print("# colors[0] = '노랑'  ← 이렇게 하면 오류가 발생합니다!")
print("불변성 덕분에 데이터가 실수로 변경되는 것을 방지할 수 있습니다.")

# 4. 튜플 언패킹 (값 분해)
print("\n4. 튜플 언패킹")
x, y = coordinates
print(f"언패킹: x = {x}, y = {y}")

red, green, blue = colors
print(f"색상 언패킹: 빨강 = {red}, 초록 = {green}, 파랑 = {blue}")

# 언패킹으로 변수 교환
a, b = 10, 20
print(f"교환 전: a = {a}, b = {b}")
a, b = b, a
print(f"교환 후: a = {a}, b = {b}")

# 5. 튜플 길이와 반복문
print("\n5. 튜플 길이와 반복문")
print(f"색상 개수: {len(colors)}")

print("모든 색상 출력:")
for color in colors:
    print(f"  - {color}")

print("인덱스와 함께 출력:")
for i, color in enumerate(colors):
    print(f"  {i+1}번: {color}")

# 6. 튜플 슬라이싱
print("\n6. 튜플 슬라이싱")
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print(f"전체 숫자: {numbers}")
print(f"처음 3개: {numbers[0:3]}")
print(f"5번째부터 8번째까지: {numbers[4:8]}")
print(f"마지막 3개: {numbers[-3:]}")
print(f"짝수 인덱스만: {numbers[::2]}")

# 7. 튜플 연결과 반복
print("\n7. 튜플 연결과 반복")
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
combined = tuple1 + tuple2
print(f"튜플 연결: {tuple1} + {tuple2} = {combined}")

repeated = tuple1 * 3
print(f"튜플 반복: {tuple1} * 3 = {repeated}")

# 8. 튜플 안에서 값 찾기
print("\n8. 튜플 안에서 값 찾기")
fruits = ("사과", "바나나", "오렌지", "바나나", "포도")
print(f"과일 튜플: {fruits}")

print(f"'바나나'가 있나요? {'바나나' in fruits}")
print(f"'딸기'가 있나요? {'딸기' in fruits}")
print(f"바나나의 첫 번째 위치: {fruits.index('바나나')}")
print(f"바나나의 개수: {fruits.count('바나나')}")

# 9. 함수에서 여러 값 반환 (튜플 사용)
print("\n9. 함수에서 여러 값 반환")

def get_student_info():
    return "홍길동", 25, "컴퓨터공학과", "A"

def calculate_stats(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    return total, average, minimum, maximum

# 함수 결과를 언패킹으로 받기
name, age, major, grade = get_student_info()
print(f"학생 정보: {name}, {age}세, {major}, 성적 {grade}")

test_scores = (85, 92, 78, 96, 88)
total, avg, min_score, max_score = calculate_stats(test_scores)
print(f"점수 통계: 총합 {total}, 평균 {avg:.1f}, 최저 {min_score}, 최고 {max_score}")

# 10. 중첩 튜플 (튜플 안의 튜플)
print("\n10. 중첩 튜플")
students = (
    ("김철수", 20, "컴퓨터공학", "A"),
    ("이영희", 19, "수학과", "B"),
    ("박민수", 21, "물리학과", "A")
)

print("전체 학생 정보:")
for i, student in enumerate(students, 1):
    name, age, major, grade = student
    print(f"  {i}. 이름: {name}, 나이: {age}, 전공: {major}, 성적: {grade}")

# 11. 튜플과 리스트 비교
print("\n11. 튜플과 리스트 비교")
list_data = [1, 2, 3]
tuple_data = (1, 2, 3)

print(f"리스트: {list_data} - 수정 가능, 대괄호 []")
list_data.append(4)
list_data[0] = 10
print(f"리스트 수정 후: {list_data}")

print(f"튜플: {tuple_data} - 수정 불가능, 소괄호 ()")
print("튜플은 안전하고 빠른 데이터 저장에 적합합니다.")

# 메모리 사용량과 속도 차이 설명
import sys
print(f"리스트 메모리 사용: {sys.getsizeof(list_data)} bytes")
print(f"튜플 메모리 사용: {sys.getsizeof(tuple_data)} bytes")

# 12. 실생활 예제 - 좌표와 RGB 색상
print("\n12. 실생활 예제 - 좌표와 RGB 색상")
# 좌표 데이터 (수정되면 안 되는 데이터)
point_a = (0, 0)
point_b = (100, 50)
point_c = (50, 100)

# RGB 색상 데이터
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

triangle_points = (point_a, point_b, point_c)
primary_colors = (red, green, blue)

print("삼각형 꼭짓점 좌표:")
for i, (x, y) in enumerate(triangle_points, 1):
    print(f"  점 {i}: ({x}, {y})")

print("기본 색상 (RGB):")
color_names = ("빨강", "초록", "파랑")
for name, (r, g, b) in zip(color_names, primary_colors):
    print(f"  {name}: RGB({r}, {g}, {b})")

# 13. 튜플을 딕셔너리 키로 사용
print("\n13. 튜플을 딕셔너리 키로 사용")
# 좌표를 키로 사용하는 맵
game_map = {
    (0, 0): "시작점",
    (5, 3): "보물",
    (10, 7): "몬스터",
    (15, 10): "출구"
}

print("게임 맵:")
for position, item in game_map.items():
    x, y = position
    print(f"  위치 ({x}, {y}): {item}")

# 특정 위치 검색
search_pos = (5, 3)
if search_pos in game_map:
    print(f"위치 {search_pos}에는 '{game_map[search_pos]}'이(가) 있습니다.")

print("\n튜플 예제 완료!")
