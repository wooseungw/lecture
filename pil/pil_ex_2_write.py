from PIL import Image

# 이미지 파일 경로
image_path = '../ex_img/victory.jpg'

# 이미지 열기
image = Image.open(image_path)

# 이미지 정보 출력
print(f"원본 이미지 - Format: {image.format}, Size: {image.size}, Mode: {image.mode}")

# 새로운 이름으로 이미지 저장 (복사)
output_path = '../ex_img/victory_copy.jpg'
image.save(output_path)

print(f"이미지가 복사되어 저장되었습니다: {output_path}")

# PNG 형식으로도 저장해보기
png_path = '../ex_img/victory_copy.png'
image.save(png_path)

print(f"PNG 형식으로도 저장되었습니다: {png_path}")
