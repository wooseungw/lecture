import cv2

image = cv2.imread('ex_img/thumbs_up.jpg')  # 이미지 읽기
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # 이미지 색상 변환 (BGR -> GRAY)
cv2.imwrite('ex_img/thumbs_up_gray.jpg', gray_image)    # 변환된 이미지 저장
