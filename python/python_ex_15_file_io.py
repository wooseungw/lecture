# 파이썬 파일 입출력(File I/O) 예제

import os

# 1. 텍스트 파일 쓰기 (기본)
# data 디렉토리가 없으면 생성
if not os.path.exists("data"):
    os.makedirs("data")

# 파일에 텍스트 쓰기
filename = "data/sample.txt"
content = "안녕하세요, 파이썬!\n이것은 첫 번째 줄입니다.\n이것은 두 번째 줄입니다."

with open(filename, "w", encoding="utf-8") as file:
    file.write(content)

# 2. 텍스트 파일 읽기
with open(filename, "r", encoding="utf-8") as file:
    read_content = file.read()
    print("파일 내용:")
    print(read_content)

# 3. 한 줄씩 읽기
with open(filename, "r", encoding="utf-8") as file:
    line_number = 1
    for line in file:
        print(f"{line_number}번 줄: {line.strip()}")  # strip()으로 줄바꿈 제거
        line_number += 1

# 4. 파일에 추가하기
additional_content = "\n이 줄은 나중에 추가되었습니다."

with open(filename, "a", encoding="utf-8") as file:
    file.write(additional_content)

# 추가 후 내용 확인
with open(filename, "r", encoding="utf-8") as file:
    updated_content = file.read()
    print("업데이트된 파일 내용:")
    print(updated_content)

# 5. 학생 정보 파일 만들기 (CSV 형태)
students = [
    "김철수,20,컴퓨터공학과,A",
    "이영희,19,수학과,B",
    "박민수,21,물리학과,A",
    "정수진,20,화학과,B"
]

student_file = "data/students.csv"

with open(student_file, "w", encoding="utf-8") as file:
    file.write("이름,나이,전공,성적\n")  # 헤더 추가
    for student in students:
        file.write(student + "\n")

# 6. CSV 파일 읽고 처리하기
with open(student_file, "r", encoding="utf-8") as file:
    lines = file.readlines()
    
    print("학생 목록:")
    for i, line in enumerate(lines):
        if i == 0:  # 헤더는 건너뛰기
            continue
        
        parts = line.strip().split(",")
        name, age, major, grade = parts
        print(f"  {name}: {age}세, {major}, 성적 {grade}")

# 7. 성적 통계 계산하여 파일로 저장
grade_count = {"A": 0, "B": 0, "C": 0}

with open(student_file, "r", encoding="utf-8") as file:
    lines = file.readlines()
    
    for line in lines[1:]:  # 헤더 제외
        parts = line.strip().split(",")
        grade = parts[3]
        if grade in grade_count:
            grade_count[grade] += 1

# 통계 파일 생성
stats_file = "data/grade_statistics.txt"
with open(stats_file, "w", encoding="utf-8") as file:
    file.write("성적 통계 보고서\n")
    file.write("=" * 20 + "\n")
    
    total_students = sum(grade_count.values())
    file.write(f"전체 학생 수: {total_students}명\n\n")
    
    for grade, count in grade_count.items():
        percentage = (count / total_students) * 100 if total_students > 0 else 0
        file.write(f"{grade} 등급: {count}명 ({percentage:.1f}%)\n")

# 8. 파일 정보 확인
files_to_check = [
    "data/sample.txt",
    "data/students.csv",
    "data/grade_statistics.txt"
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        print(f"{file_path}:")
        print(f"  크기: {file_size} bytes")
        print(f"  존재: 예")
    else:
        print(f"{file_path}: 파일이 존재하지 않습니다.")

# 9. 간단한 일기 프로그램 - 현재 날짜로 파일명 생성
from datetime import datetime

diary_content = """오늘은 파이썬 파일 입출력을 배웠다.
파일을 읽고 쓰는 것이 생각보다 간단했다.
앞으로 데이터를 파일로 저장해서 관리할 수 있을 것 같다."""

# 현재 날짜로 파일명 생성
today = datetime.now().strftime("%Y-%m-%d")
diary_filename = f"data/diary_{today}.txt"

with open(diary_filename, "w", encoding="utf-8") as file:
    file.write(f"일기 - {today}\n")
    file.write("=" * 30 + "\n")
    file.write(diary_content)

# 10. 파일 모드 정리 (참고용)
# 'r': 읽기 모드 (파일이 존재해야 함)
# 'w': 쓰기 모드 (파일을 덮어씀)
# 'a': 추가 모드 (파일 끝에 내용 추가)
# 'r+': 읽기+쓰기 모드
# 'x': 새 파일 생성 모드 (파일이 이미 있으면 오류)
# encoding='utf-8': 한글을 포함한 모든 문자를 올바르게 처리, 다른 운영체제에서도 호환성 보장

# 생성된 파일 목록 표시
if os.path.exists("data"):
    for item in os.listdir("data"):
        print(f"  📄 data/{item}")
