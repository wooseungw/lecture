from PIL import Image

# 이미지 파일 경로
image_path = '../ex_img/victory.jpg'

try:
    # 이미지 열기
    image = Image.open(image_path)
    
    print(f"원본 이미지 크기: {image.size}")
    
    # 1. 이미지 90도 회전
    rotated_90 = image.rotate(90, expand=True)
    rotated_90.save('../ex_img/victory_rotate_90.jpg')
    print("90도 회전 이미지 저장 완료")
    
    # 2. 이미지 180도 회전
    rotated_180 = image.rotate(180)
    rotated_180.save('../ex_img/victory_rotate_180.jpg')
    print("180도 회전 이미지 저장 완료")
    
    # 3. 이미지 중앙 부분 자르기
    width, height = image.size
    
    # 중앙의 절반 크기로 자르기
    left = width // 4
    top = height // 4
    right = 3 * width // 4
    bottom = 3 * height // 4
    
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save('../ex_img/victory_cropped.jpg')
    print(f"자른 이미지 저장 완료 - 크기: {cropped_image.size}")
    
    # 4. 이미지 좌우 반전
    flipped_h = image.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_h.save('../ex_img/victory_flip_horizontal.jpg')
    print("좌우 반전 이미지 저장 완료")
    
    # 5. 이미지 상하 반전
    flipped_v = image.transpose(Image.FLIP_TOP_BOTTOM)
    flipped_v.save('../ex_img/victory_flip_vertical.jpg')
    print("상하 반전 이미지 저장 완료")
    
    print("모든 변환이 완료되었습니다!")

except FileNotFoundError:
    print(f"이미지 파일을 찾을 수 없습니다: {image_path}")
    print("ex_img 폴더에 victory.jpg 파일이 있는지 확인해주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
