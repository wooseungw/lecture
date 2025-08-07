import cv2
from ultralytics import YOLO

# 모델 로드
# 사전 학습된 가중치를 다운로드 하고, 불러오는 코드가 내장
model = YOLO('yolov8n-pose.pt')

# 이미지 읽기
image_path = 'pointing_up.jpg'  # 추론할 이미지 경로로 변경하세요
image = cv2.imread(image_path)

# YOLO Pose 추론
results = model(image)

# 결과 이미지 얻기 (keypoints와 skeleton이 그려진 이미지)
annotated_image = results[0].plot()

# 결과 이미지 보여주기
cv2.imshow('YOLO Pose Estimation', annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
