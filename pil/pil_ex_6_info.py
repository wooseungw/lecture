from PIL import Image
import os

def show_image_info(image_path):
    """이미지 정보를 자세히 보여주는 함수"""
    image = Image.open(image_path)
    
    print(f"\n파일: {os.path.basename(image_path)}")
    print("-" * 30)
    print(f"형식: {image.format}")
    print(f"크기: {image.size} (가로 x 세로)")
    print(f"모드: {image.mode}")
    print(f"가로: {image.width}px")
    print(f"세로: {image.height}px")
    
    # 파일 크기 확인
    file_size = os.path.getsize(image_path)
    if file_size < 1024:
        print(f"파일 크기: {file_size} bytes")
    elif file_size < 1024 * 1024:
        print(f"파일 크기: {file_size/1024:.1f} KB")
    else:
        print(f"파일 크기: {file_size/(1024*1024):.1f} MB")
    
    # 색상 모드 설명
    if image.mode == 'RGB':
        print("색상: 컬러 (빨강, 초록, 파랑)")
    elif image.mode == 'L':
        print("색상: 그레이스케일 (흑백)")
    elif image.mode == 'RGBA':
        print("색상: 컬러 + 투명도")
    elif image.mode == '1':
        print("색상: 흑백 (1비트)")
    
    return image

if __name__ == "__main__":
    print("PIL 이미지 정보 확인 예제")
    print("=" * 35)
    
    # 여러 이미지 파일 확인
    image_files = [
        'ex_img/victory.jpg',
        'ex_img/thumbs_up.jpg',
        'ex_img/thumbs_down.jpg',
        'ex_img/pointing_up.jpg'
    ]
    
    for image_path in image_files:
        if os.path.exists(image_path):
            image = show_image_info(image_path)
        else:
            print(f"\n파일을 찾을 수 없습니다: {os.path.basename(image_path)}")
    
    print("\n모든 이미지 정보 확인이 완료되었습니다!")
