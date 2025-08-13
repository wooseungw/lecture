#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# YOLO 객체 탐지 예제 2: 실시간 웹캠 탐지
# 초보자를 위한 단계별 학습 자료

import cv2
from ultralytics import YOLO
import time

print("YOLO 객체 탐지 예제 2: 실시간 웹캠 탐지")
print("=" * 50)

# 1단계: 모델 로드
print("1. YOLO 모델 로드 중...")
model = YOLO('yolov8n.pt')
print("   ✓ 모델 로드 완료!")

# 2단계: 웹캠 연결
print("2. 웹캠 연결 중...")
cap = cv2.VideoCapture(0)

# 웹캠 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("   ⚠️  웹캠을 열 수 없습니다. 카메라가 연결되어 있는지 확인하세요.")
    exit()

print("   ✓ 웹캠 연결 완료!")

# 3단계: 실시간 탐지 시작
print("3. 실시간 객체 탐지 시작")
print("   💡 'q' 키를 누르면 종료됩니다.")
print("   💡 'p' 키를 누르면 일시정지/재개됩니다.")

# FPS 계산을 위한 변수
fps_counter = 0
start_time = time.time()
paused = False

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            print("   ⚠️  프레임을 읽을 수 없습니다.")
            break

        # 객체 탐지 실행
        results = model(frame, verbose=False)  # verbose=False로 출력 줄이기
        
        # 탐지 결과가 그려진 프레임
        annotated_frame = results[0].plot()
        
        # 탐지된 객체 수 표시
        boxes = results[0].boxes
        if boxes is not None:
            object_count = len(boxes)
            cv2.putText(annotated_frame, f'Objects: {object_count}', 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 각 객체의 클래스와 신뢰도 표시
            for i, box in enumerate(boxes):
                class_id = int(box.cls)
                confidence = float(box.conf)
                class_name = model.names[class_id]
                
                if confidence > 0.5:  # 신뢰도가 50% 이상인 것만 표시
                    text = f'{class_name}: {confidence:.1f}'
                    y_pos = 60 + (i * 25)
                    cv2.putText(annotated_frame, text, (10, y_pos), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # FPS 계산 및 표시
        fps_counter += 1
        if fps_counter % 30 == 0:  # 30프레임마다 계산
            end_time = time.time()
            fps = 30 / (end_time - start_time)
            start_time = time.time()
            
        if 'fps' in locals():
            cv2.putText(annotated_frame, f'FPS: {fps:.1f}', 
                       (annotated_frame.shape[1] - 120, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # 조작 가이드 표시
        cv2.putText(annotated_frame, 'Press Q to quit, P to pause', 
                   (10, annotated_frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('YOLO Real-time Detection', annotated_frame)
    
    # 키보드 입력 처리
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("   사용자가 종료를 요청했습니다.")
        break
    elif key == ord('p'):
        paused = not paused
        if paused:
            print("   ⏸️  일시정지됨")
        else:
            print("   ▶️  재개됨")
            start_time = time.time()  # FPS 계산 리셋

# 4단계: 정리
cap.release()
cv2.destroyAllWindows()

print("\n🎉 실시간 탐지 완료!")
print("📚 학습 포인트:")
print("   - 실시간 처리에서는 FPS(초당 프레임 수)가 중요합니다.")
print("   - 신뢰도 임계값을 조정하여 탐지 정확도를 제어할 수 있습니다.")
print("   - 웹캠 해상도가 높을수록 정확하지만 처리 속도가 느려집니다.")
print("   - GPU가 있다면 더 빠른 처리가 가능합니다.")
