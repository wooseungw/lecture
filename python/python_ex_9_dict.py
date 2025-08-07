# 파이썬 딕셔너리 예제

# 1. 딕셔너리 생성
student = {
    "이름": "김철수",
    "나이": 20,
    "학과": "컴퓨터공학",
    "학년": 2
}

empty_dict = {}  # 빈 딕셔너리
numbers_dict = {1: "일", 2: "이", 3: "삼"}

print(f"학생 정보: {student}")
print(f"빈 딕셔너리: {empty_dict}")
print(f"숫자 딕셔너리: {numbers_dict}")

# 2. 딕셔너리 값 접근
print(f"학생 이름: {student['이름']}")
print(f"학생 나이: {student['나이']}")

# get() 메서드 사용 (키가 없을 때 오류 방지)
print(f"학생 전화번호: {student.get('전화번호', '정보 없음')}")
print(f"학생 학과: {student.get('학과')}")

# 3. 딕셔너리에 새 항목 추가
print("\n3. 딕셔너리에 새 항목 추가")
student["성적"] = "A"
student["전화번호"] = "010-1234-5678"
student["취미"] = ["독서", "영화감상", "게임"]

print(f"정보 추가 후: {student}")

# 4. 딕셔너리 값 수정
print("\n4. 딕셔너리 값 수정")
print(f"변경 전 나이: {student['나이']}")
student["나이"] = 21
student["학년"] = 3
print(f"변경 후: 나이 {student['나이']}, 학년 {student['학년']}")

# 5. 딕셔너리에서 항목 삭제
print("\n5. 딕셔너리에서 항목 삭제")
removed_phone = student.pop("전화번호", "없음")  # pop으로 삭제하고 값 반환
print(f"삭제된 전화번호: {removed_phone}")

if "주소" in student:
    del student["주소"]
print(f"삭제 후 딕셔너리: {student}")

# 6. 딕셔너리 키, 값, 항목 가져오기
print("\n6. 딕셔너리 키, 값, 항목 가져오기")
print(f"모든 키: {list(student.keys())}")
print(f"모든 값: {list(student.values())}")
print(f"모든 항목: {list(student.items())}")

# 7. 딕셔너리 반복문
print("\n7. 딕셔너리 반복문")
print("학생 정보 출력:")
for key in student:
    print(f"  {key}: {student[key]}")

print("\n키와 값을 함께 출력:")
for key, value in student.items():
    print(f"  {key} → {value}")

# 8. 여러 학생 정보 관리 (중첩 딕셔너리)
print("\n8. 여러 학생 정보 관리")
students = {
    "김철수": {
        "나이": 20,
        "학과": "컴퓨터공학",
        "성적": "A",
        "과목점수": {"수학": 85, "영어": 90, "과학": 88}
    },
    "이영희": {
        "나이": 19,
        "학과": "수학과",
        "성적": "B",
        "과목점수": {"수학": 95, "영어": 78, "과학": 82}
    },
    "박민수": {
        "나이": 21,
        "학과": "물리학과",
        "성적": "A",
        "과목점수": {"수학": 92, "영어": 85, "과학": 96}
    }
}

print("전체 학생 수:", len(students))
for name, info in students.items():
    print(f"\n{name}:")
    for key, value in info.items():
        print(f"  {key}: {value}")

# 9. 특정 조건으로 학생 찾기
print("\n9. 특정 조건으로 학생 찾기")
print("성적이 A인 학생들:")
a_students = []
for name, info in students.items():
    if info["성적"] == "A":
        a_students.append(name)
        print(f"  - {name} ({info['학과']}, {info['나이']}세)")

print(f"\nA 학생 총 {len(a_students)}명")

# 10. 과목별 평균 점수 계산
print("\n10. 과목별 평균 점수 계산")
subjects = ["수학", "영어", "과학"]
subject_totals = {"수학": 0, "영어": 0, "과학": 0}

for name, info in students.items():
    for subject in subjects:
        subject_totals[subject] += info["과목점수"][subject]

print("과목별 평균 점수:")
for subject, total in subject_totals.items():
    average = total / len(students)
    print(f"  {subject}: {average:.1f}점")

# 11. 딕셔너리 합치기와 복사
print("\n11. 딕셔너리 합치기와 복사")
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
dict3 = {"b": 20, "e": 5}  # 'b' 키가 중복됨

# 딕셔너리 합치기 (update)
combined_dict = dict1.copy()  # 복사본 생성
combined_dict.update(dict2)   # dict2 내용 추가
print(f"dict1 + dict2: {combined_dict}")

combined_dict.update(dict3)   # dict3 내용 추가 (중복 키는 덮어씀)
print(f"dict3 추가 후: {combined_dict}")

# 12. 실생활 예제 - 상품 재고 관리
print("\n12. 실생활 예제 - 상품 재고 관리")
inventory = {
    "사과": {"가격": 1000, "재고": 50, "카테고리": "과일"},
    "바나나": {"가격": 1500, "재고": 30, "카테고리": "과일"},
    "우유": {"가격": 2500, "재고": 20, "카테고리": "유제품"},
    "빵": {"가격": 3000, "재고": 15, "카테고리": "베이커리"}
}

print("=== 상품 재고 현황 ===")
total_value = 0
for product, info in inventory.items():
    value = info["가격"] * info["재고"]
    total_value += value
    print(f"{product}: {info['가격']:,}원 x {info['재고']}개 = {value:,}원")

print(f"\n총 재고 가치: {total_value:,}원")

# 재고가 적은 상품 찾기
print("\n재고가 20개 이하인 상품:")
low_stock = []
for product, info in inventory.items():
    if info["재고"] <= 20:
        low_stock.append(product)
        print(f"  - {product}: {info['재고']}개")

# 13. 단어 빈도 계산
print("\n13. 단어 빈도 계산")
text = "파이썬은 재미있다 파이썬을 배우자 파이썬은 쉽다"
words = text.split()
word_count = {}

for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print(f"원문: {text}")
print("단어 빈도:")
for word, count in word_count.items():
    print(f"  '{word}': {count}회")

print("\n딕셔너리 예제 완료!")
