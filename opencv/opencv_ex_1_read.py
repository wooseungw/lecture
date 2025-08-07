import cv2

image = cv2.imread('ex_img/thumbs_up.jpg') # 이미지 읽기

cv2.imshow('Image', image)  # 제목, 띄우고 싶은 이미지
cv2.waitKey(0)  # 키 입력 대기
cv2.destroyAllWindows()     # 창 닫기