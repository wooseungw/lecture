from PIL import Image

# 이미지 파일 경로
image_path = '../ex_img/victory.jpg'

# 이미지 열기
image = Image.open(image_path)

print(f"원본 이미지 크기: {image.size}")

# 1. 이미지 크기를 반으로 줄이기
width, height = image.size
small_image = image.resize((width//2, height//2))
small_image.save('../ex_img/victory_small.jpg')
print(f"작은 이미지 저장 완료 - 크기: {small_image.size}")

# 2. 이미지 크기를 2배로 늘리기
big_image = image.resize((width*2, height*2))
big_image.save('../ex_img/victory_big.jpg')
print(f"큰 이미지 저장 완료 - 크기: {big_image.size}")

# 3. 정사각형으로 만들기 (200x200)
square_image = image.resize((200, 200))
square_image.save('../ex_img/victory_square.jpg')
print(f"정사각형 이미지 저장 완료 - 크기: {square_image.size}")

print("모든 크기 조정이 완료되었습니다!")
