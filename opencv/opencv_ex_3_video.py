import cv2

cap = cv2.VideoCapture('ex_img/sample_video.mp4')  # 비디오 파일 경로

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Video', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):  # 'q' 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
