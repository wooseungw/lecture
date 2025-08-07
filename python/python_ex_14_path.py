# 파이썬 경로(Path) 예제 - 상대경로와 절대경로

print("파이썬 경로 예제")
print("=" * 25)

import os

# 1. 현재 작업 디렉토리 확인
print("1. 현재 작업 디렉토리 확인")
current_dir = os.getcwd()
print(f"현재 디렉토리: {current_dir}")

# 2. 절대경로 예제
print("\n2. 절대경로 예제")
# 절대경로는 루트(/)부터 시작하는 전체 경로
absolute_path = "/Users/seungwoo/Workspace/humans/python/data.txt"
print(f"절대경로 예제: {absolute_path}")
print("절대경로 특징:")
print("- 항상 루트 디렉토리(/)부터 시작")
print("- 어디서 실행하든 같은 파일을 가리킴")
print("- 길지만 명확함")

# 3. 상대경로 예제
print("\n3. 상대경로 예제")
# 상대경로는 현재 위치를 기준으로 한 경로
relative_path = "data/sample.txt"
relative_path2 = "../ex_img/victory.jpg"
relative_path3 = "./python_ex_1_variable.py"

print(f"현재 폴더 기준: {relative_path}")
print(f"상위 폴더 기준: {relative_path2}")
print(f"현재 폴더 명시: {relative_path3}")

print("\n상대경로 기호 설명:")
print("- .  : 현재 디렉토리")
print("- .. : 상위 디렉토리")
print("- / 또는 \\ : 디렉토리 구분자")

# 4. 경로 존재 확인
print("\n4. 경로 존재 확인")
current_file = "python_ex_14_path.py"
parent_dir = ".."
sample_file = "data/sample.txt"

print(f"현재 파일 존재: {os.path.exists(current_file)}")
print(f"상위 디렉토리 존재: {os.path.exists(parent_dir)}")
print(f"샘플 파일 존재: {os.path.exists(sample_file)}")

# 5. 경로 조작하기
print("\n5. 경로 조작하기")
# os.path.join을 사용하면 운영체제에 맞는 경로 구분자를 자동으로 사용
data_dir = "data"
filename = "student_info.txt"
full_path = os.path.join(data_dir, filename)

print(f"디렉토리: {data_dir}")
print(f"파일명: {filename}")
print(f"결합된 경로: {full_path}")

# 6. 경로 분리하기
print("\n6. 경로 분리하기")
sample_path = "data/documents/report.pdf"

directory = os.path.dirname(sample_path)  # 디렉토리 부분
filename = os.path.basename(sample_path)  # 파일명 부분
name, extension = os.path.splitext(filename)  # 이름과 확장자 분리

print(f"전체 경로: {sample_path}")
print(f"디렉토리 부분: {directory}")
print(f"파일명 부분: {filename}")
print(f"파일명(확장자 제외): {name}")
print(f"확장자: {extension}")

# 7. 실제 경로 예제
print("\n7. 실제 경로 예제")
print("Python 파일들의 실제 경로:")

python_files = [
    "python_ex_1_variable.py",
    "python_ex_8_list.py",
    "python_ex_9_dict.py"
]

for file in python_files:
    if os.path.exists(file):
        abs_path = os.path.abspath(file)
        print(f"  {file}")
        print(f"  → 절대경로: {abs_path}")
    else:
        print(f"  {file} (파일 없음)")

# 8. 디렉토리 내용 확인
print("\n8. 현재 디렉토리 내용")
files_and_dirs = os.listdir(".")
print("현재 디렉토리의 파일과 폴더:")

for item in sorted(files_and_dirs):
    if os.path.isfile(item):
        print(f"  📄 {item} (파일)")
    elif os.path.isdir(item):
        print(f"  📁 {item} (폴더)")

# 9. 경로 사용 시 주의사항
print("\n9. 경로 사용 시 주의사항")
print("상대경로 사용 시:")
print("- 현재 작업 디렉토리에 따라 결과가 달라짐")
print("- 프로그램 실행 위치를 확인해야 함")
print("- 이식성이 좋음 (다른 컴퓨터에서도 동작)")

print("\n절대경로 사용 시:")
print("- 항상 같은 파일을 가리킴")
print("- 다른 컴퓨터에서는 동작하지 않을 수 있음")
print("- 경로가 길어질 수 있음")

print("\n경로 예제 완료!")
