#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 레포지토리의 Python 파일들에 UTF-8 인코딩을 추가하는 스크립트
"""

import os
import glob
import re

def add_encoding_header(file_path):
    """Python 파일에 UTF-8 인코딩 헤더 추가"""
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 이미 인코딩이 있는지 확인
        if '# -*- coding: utf-8 -*-' in content:
            return False  # 이미 추가됨
        
        lines = content.split('\n')
        
        # 첫 번째 줄이 shebang인지 확인
        has_shebang = len(lines) > 0 and lines[0].startswith('#!')
        
        # 새로운 헤더 구성
        if has_shebang:
            # shebang이 있으면 그 다음에 인코딩 추가
            new_lines = [
                lines[0],  # shebang 유지
                '# -*- coding: utf-8 -*-'
            ] + lines[1:]
        else:
            # shebang이 없으면 맨 앞에 모두 추가
            new_lines = [
                '#!/usr/bin/env python3',
                '# -*- coding: utf-8 -*-'
            ] + lines
        
        # 파일에 쓰기
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True  # 수정됨
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """메인 함수"""
    base_dir = "/Users/seungwoo/Workspace/humans"
    
    # 모든 Python 파일 찾기
    python_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"총 {len(python_files)}개의 Python 파일을 찾았습니다.")
    
    modified_count = 0
    for file_path in python_files:
        if add_encoding_header(file_path):
            print(f"✓ 수정됨: {os.path.relpath(file_path, base_dir)}")
            modified_count += 1
        else:
            print(f"- 건너뜀: {os.path.relpath(file_path, base_dir)}")
    
    print(f"\n완료! {modified_count}개 파일이 수정되었습니다.")

if __name__ == "__main__":
    main()
