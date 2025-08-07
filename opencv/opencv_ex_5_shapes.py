# OpenCV 도형 그리기 예제 - 사각형, 원, 선 그리기
import cv2
import numpy as np

# 검은색 배경 이미지 생성 (500x500, 3채널)
img = np.zeros((500, 500, 3), dtype=np.uint8)

print("=== OpenCV 도형 그리기 예제 ===")
print("다양한 도형을 그려보는 기본 예제입니다.")

# 1. 사각형 그리기
print("\n1. 사각형 그리기")
cv2.rectangle(img, (50, 50), (200, 150), (0, 255, 0), 2)  # 초록색 테두리
cv2.rectangle(img, (250, 50), (400, 150), (255, 0, 0), -1)  # 파란색 채우기

# 사각형 설명 텍스트
cv2.putText(img, 'Rectangle Border', (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
cv2.putText(img, 'Rectangle Filled', (250, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

# 2. 원 그리기
print("2. 원 그리기")
cv2.circle(img, (125, 250), 50, (0, 255, 255), 3)  # 노란색 테두리
cv2.circle(img, (325, 250), 50, (255, 255, 0), -1)  # 청록색 채우기

# 원 설명 텍스트
cv2.putText(img, 'Circle Border', (75, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
cv2.putText(img, 'Circle Filled', (275, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

# 3. 선 그리기
print("3. 선 그리기")
cv2.line(img, (50, 350), (200, 350), (255, 255, 255), 2)  # 가로선 (흰색)
cv2.line(img, (250, 330), (400, 370), (255, 0, 255), 3)  # 대각선 (자홍색)
cv2.line(img, (300, 380), (350, 450), (0, 128, 255), 4)  # 세로선 (주황색)

# 선 설명 텍스트
cv2.putText(img, 'Lines', (50, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

# 4. 추가 도형들
print("4. 추가 도형들")
# 타원
cv2.ellipse(img, (100, 450), (40, 20), 0, 0, 360, (128, 255, 128), 2)

# 다각형 (삼각형)
points = np.array([[300, 400], [350, 450], [250, 450]], np.int32)
points = points.reshape((-1, 1, 2))
cv2.polylines(img, [points], True, (255, 128, 0), 2)

# 채워진 다각형 (사각형)
points2 = np.array([[380, 400], [450, 400], [450, 450], [380, 450]], np.int32)
points2 = points2.reshape((-1, 1, 2))
cv2.fillPoly(img, [points2], (128, 0, 255))

# 제목 추가
cv2.putText(img, 'OpenCV Shape Drawing Examples', (100, 30), 
           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

print("\n=== 사용된 함수들 ===")
print("cv2.rectangle(img, pt1, pt2, color, thickness)")
print("cv2.circle(img, center, radius, color, thickness)")
print("cv2.line(img, pt1, pt2, color, thickness)")
print("cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness)")
print("cv2.polylines(img, [points], isClosed, color, thickness)")
print("cv2.fillPoly(img, [points], color)")
print("\nthickness: -1이면 채우기, 양수면 테두리 두께")

# 이미지 출력
cv2.imshow('Shape Drawing Examples', img)
print("\n아무 키나 누르면 종료합니다...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# 이미지 저장
cv2.imwrite('../ex_img/shape_drawing_example.jpg', img)
print("예제 이미지가 저장되었습니다: shape_drawing_example.jpg")
