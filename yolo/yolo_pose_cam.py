import cv2
import torch
from ultralytics import YOLO

# ultralytics YOLO-Pose 모델 설치 필요: pip install ultralytics

# 모델 로드 (yolov8-pose 모델 사용)
model = YOLO('yolov8n-pose.pt')  # 또는 'yolov8s-pose.pt', 'yolov8m-pose.pt' 등

# 웹캠 열기
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO Pose 추론
    results = model(frame)

    # 결과 이미지 얻기 (keypoints와 skeleton이 그려진 이미지)
    annotated_frame = results[0].plot()

    cv2.imshow('YOLO Pose Estimation', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()