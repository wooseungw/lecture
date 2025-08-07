# 파이썬 리스트 기본 사용법 예제

# 1. 리스트 생성
fruits = ["사과", "바나나", "오렌지"]
numbers = [1, 2, 3, 4, 5]
mixed = ["안녕", 123, True, 3.14]

print(f"과일 리스트: {fruits}")
print(f"숫자 리스트: {numbers}")
print(f"혼합 리스트: {mixed}")

# 2. 리스트 요소 접근 (인덱스 사용)
print(f"첫 번째 과일: {fruits[0]}")
print(f"두 번째 과일: {fruits[1]}")
print(f"마지막 과일: {fruits[-1]}")  # 음수 인덱스로 뒤에서부터 접근

# 3. 리스트에 요소 추가
fruits.append("포도")  # 맨 뒤에 추가
print(f"포도 추가 후: {fruits}")

fruits.insert(1, "딸기")  # 특정 위치에 추가
print(f"딸기를 1번 위치에 추가: {fruits}")

# 4. 리스트에서 요소 제거
fruits.remove("바나나")  # 특정 값 제거
print(f"바나나 제거 후: {fruits}")

removed_fruit = fruits.pop()  # 마지막 요소 제거하고 반환
print(f"마지막 요소 제거: {removed_fruit}")
print(f"제거 후 리스트: {fruits}")

# 5. 리스트 길이와 반복문
print(f"현재 과일 개수: {len(fruits)}")

print("모든 과일 출력:")
for fruit in fruits:
    print(f"- {fruit}")

print("인덱스와 함께 출력:")
for i in range(len(fruits)):
    print(f"{i+1}번: {fruits[i]}")

# 6. 리스트 슬라이싱
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"전체 숫자: {numbers}")
print(f"처음 3개: {numbers[0:3]}")
print(f"3번째부터 끝까지: {numbers[3:]}")
print(f"마지막 3개: {numbers[-3:]}")

# 7. 리스트 정렬
random_numbers = [5, 2, 8, 1, 9, 3]
print(f"정렬 전: {random_numbers}")

random_numbers.sort()  # 오름차순 정렬
print(f"오름차순 정렬: {random_numbers}")

random_numbers.sort(reverse=True)  # 내림차순 정렬
print(f"내림차순 정렬: {random_numbers}")

# 8. 리스트 내포(List Comprehension) - 간단한 예제
squares = [x * x for x in range(1, 6)]
print(f"1~5의 제곱: {squares}")

even_numbers = [x for x in range(1, 11) if x % 2 == 0]
print(f"1~10 중 짝수: {even_numbers}")
