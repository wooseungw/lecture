# 파이썬 파일 시스템 탐색 예제

print("파이썬 파일 시스템 탐색 예제")
print("=" * 35)

import os
from datetime import datetime

# 1. 현재 디렉토리 탐색
print("1. 현재 디렉토리 탐색")
current_path = "."

print(f"현재 위치: {os.path.abspath(current_path)}")
items = os.listdir(current_path)

files = []
directories = []

for item in items:
    if os.path.isfile(item):
        files.append(item)
    elif os.path.isdir(item):
        directories.append(item)

print(f"\n폴더 개수: {len(directories)}")
for directory in sorted(directories):
    print(f"  📁 {directory}")

print(f"\n파일 개수: {len(files)}")
for file in sorted(files):
    print(f"  📄 {file}")

# 2. 파일 크기와 수정 시간 확인
print("\n2. 파일 상세 정보")

python_files = [f for f in files if f.endswith('.py')]

for file in python_files[:5]:  # 처음 5개만 표시
    try:
        size = os.path.getsize(file)
        modified_time = os.path.getmtime(file)
        modified_date = datetime.fromtimestamp(modified_time)
        
        print(f"{file}:")
        print(f"  크기: {size} bytes")
        print(f"  수정일: {modified_date.strftime('%Y-%m-%d %H:%M:%S')}")
    except:
        print(f"{file}: 정보를 읽을 수 없습니다.")

# 3. 특정 확장자 파일 찾기
print("\n3. 특정 확장자 파일 찾기")

file_extensions = {}

for file in files:
    name, ext = os.path.splitext(file)
    if ext:
        ext = ext.lower()
        if ext in file_extensions:
            file_extensions[ext] += 1
        else:
            file_extensions[ext] = 1

print("확장자별 파일 개수:")
for ext, count in sorted(file_extensions.items()):
    print(f"  {ext}: {count}개")

# 4. 디렉토리 구조 표시 (1레벨만)
print("\n4. 디렉토리 구조 (1레벨)")

def show_directory_structure(path, prefix=""):
    try:
        items = sorted(os.listdir(path))
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print(f"{prefix}📁 {item}/")
            else:
                print(f"{prefix}📄 {item}")
    except PermissionError:
        print(f"{prefix}❌ 접근 권한 없음")

print("현재 디렉토리 구조:")
show_directory_structure(".", "  ")

# 5. 파일 검색 함수
print("\n5. 파일 검색")

def find_files_by_name(directory, pattern):
    """특정 패턴을 포함한 파일 찾기"""
    found_files = []
    
    try:
        for item in os.listdir(directory):
            if pattern.lower() in item.lower():
                found_files.append(item)
    except:
        pass
    
    return found_files

# Python 파일 검색
search_pattern = "python"
found = find_files_by_name(".", search_pattern)

print(f"'{search_pattern}'를 포함한 파일들:")
for file in found:
    print(f"  📄 {file}")

# 6. 파일 크기별 분류
print("\n6. 파일 크기별 분류")

size_categories = {
    "작은 파일 (< 1KB)": [],
    "중간 파일 (1KB ~ 10KB)": [],
    "큰 파일 (> 10KB)": []
}

for file in files:
    try:
        size = os.path.getsize(file)
        
        if size < 1024:
            size_categories["작은 파일 (< 1KB)"].append((file, size))
        elif size < 10240:
            size_categories["중간 파일 (1KB ~ 10KB)"].append((file, size))
        else:
            size_categories["큰 파일 (> 10KB)"].append((file, size))
    except:
        pass

for category, file_list in size_categories.items():
    print(f"\n{category}: {len(file_list)}개")
    for file, size in file_list[:3]:  # 각 카테고리에서 3개만 표시
        print(f"  📄 {file} ({size} bytes)")

# 7. 빈 디렉토리 확인
print("\n7. 빈 디렉토리 확인")

empty_dirs = []
for directory in directories:
    try:
        if len(os.listdir(directory)) == 0:
            empty_dirs.append(directory)
    except:
        pass

if empty_dirs:
    print("빈 디렉토리:")
    for directory in empty_dirs:
        print(f"  📁 {directory}")
else:
    print("빈 디렉토리가 없습니다.")

# 8. 최근 수정된 파일 찾기
print("\n8. 최근 수정된 파일 (상위 5개)")

file_times = []
for file in files:
    try:
        mtime = os.path.getmtime(file)
        file_times.append((file, mtime))
    except:
        pass

# 수정 시간순으로 정렬 (최근 것부터)
file_times.sort(key=lambda x: x[1], reverse=True)

print("최근 수정된 파일들:")
for file, mtime in file_times[:5]:
    modified_date = datetime.fromtimestamp(mtime)
    print(f"  📄 {file}")
    print(f"     수정일: {modified_date.strftime('%Y-%m-%d %H:%M:%S')}")

# 9. 경로 관련 유용한 함수들
print("\n9. 경로 관련 유용한 함수들")

sample_path = "data/documents/report.pdf"
print(f"예시 경로: {sample_path}")
print(f"디렉토리명: {os.path.dirname(sample_path)}")
print(f"파일명: {os.path.basename(sample_path)}")
print(f"파일명(확장자 제외): {os.path.splitext(sample_path)[0]}")
print(f"확장자: {os.path.splitext(sample_path)[1]}")
print(f"절대경로로 변환: {os.path.abspath(sample_path)}")

# 10. 시스템 정보
print("\n10. 시스템 정보")
print(f"현재 작업 디렉토리: {os.getcwd()}")
print(f"사용자 홈 디렉토리: {os.path.expanduser('~')}")
print(f"경로 구분자: '{os.sep}'")
print(f"현재 경로: '{os.curdir}'")
print(f"상위 경로: '{os.pardir}'")

print("\n파일 시스템 탐색 예제 완료!")
