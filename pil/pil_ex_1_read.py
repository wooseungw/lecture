from PIL import Image

# 이미지 파일 경로
image_path = 'ex_img/victory.jpg'

# 이미지 열기
image = Image.open(image_path)

# 이미지 정보 출력
print(f"Format: {image.format}, Size: {image.size}, Mode: {image.mode}")

# 이미지 보기
image.show()