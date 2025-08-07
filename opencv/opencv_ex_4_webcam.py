import cv2

cap = cv2.VideoCapture(0)  # 0번 웹캠 사용

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Webcam', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):  # 'q' 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
