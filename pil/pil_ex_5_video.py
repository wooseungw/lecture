from PIL import Image

# 이미지 파일 경로
image_path = '../ex_img/victory.jpg'

try:
    # 이미지 열기
    image = Image.open(image_path)
    
    print(f"원본 이미지 - Mode: {image.mode}, Size: {image.size}")
    
    # 1. 그레이스케일로 변환
    grayscale = image.convert('L')  # 'L'은 그레이스케일을 의미
    grayscale.save('../ex_img/victory_grayscale.jpg')
    print(f"그레이스케일 저장 완료 - Mode: {grayscale.mode}")
    
    # 2. 그레이스케일을 다시 RGB로 변환 (색상은 여전히 흑백)
    rgb_from_gray = grayscale.convert('RGB')
    rgb_from_gray.save('../ex_img/victory_gray_to_rgb.jpg')
    print(f"그레이스케일->RGB 저장 완료 - Mode: {rgb_from_gray.mode}")
    
    # 3. 흑백 (1비트) 이미지로 변환
    black_white = image.convert('1')  # '1'은 1비트 흑백을 의미
    black_white.save('../ex_img/victory_black_white.jpg')
    print(f"흑백 이미지 저장 완료 - Mode: {black_white.mode}")
    
    print("모든 색상 변환이 완료되었습니다!")
    print("저장된 파일들:")
    print("- victory_grayscale.jpg (회색조)")
    print("- victory_gray_to_rgb.jpg (회색조->RGB)")
    print("- victory_black_white.jpg (흑백)")

except FileNotFoundError:
    print(f"이미지 파일을 찾을 수 없습니다: {image_path}")
    print("ex_img 폴더에 victory.jpg 파일이 있는지 확인해주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
