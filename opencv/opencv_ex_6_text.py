# OpenCV 텍스트 그리기 예제 - 다양한 폰트와 스타일
import cv2
import numpy as np

# 흰색 배경 이미지 생성
img = np.ones((600, 800, 3), dtype=np.uint8) * 255

print("=== OpenCV 텍스트 그리기 예제 ===")
print("다양한 폰트와 텍스트 스타일을 보여주는 예제입니다.")

# 제목
cv2.putText(img, 'OpenCV Text Examples', (200, 50), 
           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

y_pos = 100  # 시작 y 위치

# 1. 다양한 폰트 타입
print("\n1. 다양한 폰트 타입")
fonts = [
    (cv2.FONT_HERSHEY_SIMPLEX, "FONT_HERSHEY_SIMPLEX"),
    (cv2.FONT_HERSHEY_PLAIN, "FONT_HERSHEY_PLAIN"),
    (cv2.FONT_HERSHEY_DUPLEX, "FONT_HERSHEY_DUPLEX"),
    (cv2.FONT_HERSHEY_COMPLEX, "FONT_HERSHEY_COMPLEX"),
    (cv2.FONT_HERSHEY_TRIPLEX, "FONT_HERSHEY_TRIPLEX"),
    (cv2.FONT_HERSHEY_COMPLEX_SMALL, "FONT_HERSHEY_COMPLEX_SMALL"),
    (cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, "FONT_HERSHEY_SCRIPT_SIMPLEX"),
    (cv2.FONT_HERSHEY_SCRIPT_COMPLEX, "FONT_HERSHEY_SCRIPT_COMPLEX"),
]

for font, font_name in fonts:
    cv2.putText(img, font_name, (50, y_pos), font, 0.8, (0, 0, 255), 2)
    y_pos += 40

# 2. 다양한 크기
print("2. 다양한 크기")
y_pos += 20
sizes = [0.5, 1.0, 1.5, 2.0]
for size in sizes:
    cv2.putText(img, f'Size {size}', (400, y_pos), 
               cv2.FONT_HERSHEY_SIMPLEX, size, (255, 0, 0), 2)
    y_pos += int(30 * size)

# 3. 다양한 색상
print("3. 다양한 색상")
colors = [
    ((255, 0, 0), "Blue"),
    ((0, 255, 0), "Green"),
    ((0, 0, 255), "Red"),
    ((255, 255, 0), "Cyan"),
    ((255, 0, 255), "Magenta"),
    ((0, 255, 255), "Yellow"),
    ((128, 128, 128), "Gray"),
    ((0, 0, 0), "Black")
]

x_pos = 50
for color, color_name in colors:
    cv2.putText(img, color_name, (x_pos, 500), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    x_pos += 90

# 4. 다양한 두께
print("4. 다양한 두께")
thicknesses = [1, 2, 3, 4, 5]
y_pos = 530
for thickness in thicknesses:
    cv2.putText(img, f'Thickness {thickness}', (50, y_pos), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 128, 0), thickness)
    y_pos += 30

# 5. 특수 효과 - 그림자 텍스트
print("5. 특수 효과")
shadow_text = "Shadow Text"
# 그림자 (검은색, 약간 오프셋)
cv2.putText(img, shadow_text, (402, 552), 
           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
# 메인 텍스트 (흰색)
cv2.putText(img, shadow_text, (400, 550), 
           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

# 6. 외곽선 텍스트
outline_text = "Outline Text"
# 외곽선 (검은색, 두껍게)
cv2.putText(img, outline_text, (400, 580), 
           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4)
# 내부 (노란색)
cv2.putText(img, outline_text, (400, 580), 
           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

print("\n=== cv2.putText() 함수 설명 ===")
print("cv2.putText(image, text, position, font, scale, color, thickness, lineType)")
print("- image: 텍스트를 그릴 이미지")
print("- text: 그릴 텍스트 (문자열)")
print("- position: 텍스트 시작 위치 (x, y)")
print("- font: 폰트 타입")
print("- scale: 폰트 크기 배율")
print("- color: 텍스트 색상 (B, G, R)")
print("- thickness: 텍스트 두께")
print("- lineType: 선의 타입 (cv2.LINE_AA는 안티앨리어싱)")

# 텍스트 크기 측정 예제
print("\n=== 텍스트 크기 측정 ===")
test_text = "Text Size"
text_size = cv2.getTextSize(test_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
print(f"'{test_text}' 크기: {text_size}")

# 측정된 크기로 배경 박스 그리기
text_x, text_y = 50, 80
cv2.rectangle(img, (text_x, text_y - text_size[1] - 10), 
             (text_x + text_size[0], text_y + 5), (200, 200, 200), -1)
cv2.putText(img, test_text, (text_x, text_y), 
           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# 이미지 출력
cv2.imshow('Text Examples', img)
print("\n아무 키나 누르면 종료합니다...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# 이미지 저장
cv2.imwrite('../ex_img/text_examples.jpg', img)
print("예제 이미지가 저장되었습니다: text_examples.jpg")
