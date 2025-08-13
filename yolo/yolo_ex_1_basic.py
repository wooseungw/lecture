#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# YOLO 객체 탐지 예제 1: 기본 이미지 탐지
# 초보자를 위한 단계별 학습 자료

import cv2
from ultralytics import YOLO

# ultralytics YOLO 모델 설치 필요: pip install ultralytics

print("YOLO 객체 탐지 예제 1: 기본 이미지 탐지")
print("=" * 50)

# 1단계: 모델 로드
print("1. YOLO 모델 로드 중...")
model = YOLO('yolov8n.pt')  # nano 버전 (가장 빠름, 정확도는 보통)
print("   ✓ 모델 로드 완료!")

# 2단계: 이미지 로드
print("2. 이미지 로드 중...")
image_path = 'pointing_up.jpg'  # 테스트할 이미지 파일
image = cv2.imread(image_path)

if image is None:
    print("   ⚠️  이미지를 찾을 수 없습니다. 파일 경로를 확인하세요.")
    print("   현재 디렉토리에 'pointing_up.jpg' 파일이 있는지 확인하세요.")
    exit()

print("   ✓ 이미지 로드 완료!")

# 3단계: 객체 탐지 실행
print("3. 객체 탐지 실행 중...")
results = model(image)
print("   ✓ 탐지 완료!")

# 4단계: 탐지 결과 확인
print("4. 탐지 결과:")
for r in results:
    boxes = r.boxes
    if boxes is not None:
        print(f"   - 탐지된 객체 수: {len(boxes)}")
        for i, box in enumerate(boxes):
            # 클래스 이름과 신뢰도 출력
            class_id = int(box.cls)
            confidence = float(box.conf)
            class_name = model.names[class_id]
            print(f"     {i+1}. {class_name}: {confidence:.2f} (신뢰도)")
    else:
        print("   - 탐지된 객체가 없습니다.")

# 5단계: 결과 이미지 생성 및 표시
print("5. 결과 이미지 표시")
annotated_frame = results[0].plot()  # 탐지 결과가 그려진 이미지

# 원본과 결과를 나란히 표시
original_resized = cv2.resize(image, (640, 480))
result_resized = cv2.resize(annotated_frame, (640, 480))

# 이미지 합치기 (좌: 원본, 우: 결과)
combined = cv2.hconcat([original_resized, result_resized])

# 텍스트 추가
cv2.putText(combined, 'Original', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(combined, 'Detection Result', (650, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

cv2.imshow('YOLO Object Detection - Basic Example', combined)

print("   ✓ 이미지 창이 열렸습니다.")
print("   💡 아무 키나 누르면 종료됩니다.")

cv2.waitKey(0)
cv2.destroyAllWindows()

print("\n🎉 예제 완료!")
print("📚 학습 포인트:")
print("   - YOLO 모델은 80개의 일반적인 객체를 탐지할 수 있습니다.")
print("   - 신뢰도(confidence)가 높을수록 정확한 탐지입니다.")
print("   - yolov8n.pt는 가장 빠르지만, yolov8s.pt, yolov8m.pt 등은 더 정확합니다.")
