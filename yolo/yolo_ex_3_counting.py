# YOLO 객체 탐지 예제 3: 특정 객체 탐지 및 카운팅
# 초보자를 위한 단계별 학습 자료

import cv2
from ultralytics import YOLO
import numpy as np

print("YOLO 객체 탐지 예제 3: 특정 객체 탐지 및 카운팅")
print("=" * 50)

# 1단계: 관심 객체 설정
TARGET_CLASSES = {
    0: 'person',      # 사람
    2: 'car',         # 자동차  
    7: 'truck',       # 트럭
    15: 'cat',        # 고양이
    16: 'dog',        # 개
    39: 'bottle',     # 병
    41: 'cup',        # 컵
    67: 'cell phone'  # 핸드폰
}

print("1. 탐지할 객체 목록:")
for class_id, name in TARGET_CLASSES.items():
    print(f"   - {name}")

# 2단계: 모델 로드
print("\n2. YOLO 모델 로드 중...")
model = YOLO('yolov8n.pt')
print("   ✓ 모델 로드 완료!")

# 3단계: 웹캠 연결
print("3. 웹캠 연결 중...")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("   ⚠️  웹캠을 열 수 없습니다.")
    exit()

print("   ✓ 웹캠 연결 완료!")

# 4단계: 객체 카운터 초기화
object_counts = {name: 0 for name in TARGET_CLASSES.values()}
max_counts = {name: 0 for name in TARGET_CLASSES.values()}

print("4. 실시간 특정 객체 탐지 시작")
print("   💡 'q' 키를 누르면 종료됩니다.")
print("   💡 'r' 키를 누르면 카운터를 리셋합니다.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 5단계: 객체 탐지 실행
    results = model(frame, verbose=False)
    annotated_frame = frame.copy()
    
    # 현재 프레임의 객체 카운터 초기화
    current_counts = {name: 0 for name in TARGET_CLASSES.values()}
    
    # 6단계: 탐지 결과 처리
    boxes = results[0].boxes
    if boxes is not None:
        for box in boxes:
            class_id = int(box.cls)
            confidence = float(box.conf)
            
            # 관심 객체이고 신뢰도가 충분한 경우
            if class_id in TARGET_CLASSES and confidence > 0.5:
                class_name = TARGET_CLASSES[class_id]
                current_counts[class_name] += 1
                
                # 바운딩 박스 그리기
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # 객체별 색상 지정
                colors = {
                    'person': (0, 255, 0),      # 초록
                    'car': (255, 0, 0),         # 파랑
                    'truck': (255, 100, 0),     # 주황
                    'cat': (0, 255, 255),       # 노랑
                    'dog': (255, 0, 255),       # 자홍
                    'bottle': (128, 0, 128),    # 보라
                    'cup': (255, 165, 0),       # 오렌지
                    'cell phone': (0, 0, 255)   # 빨강
                }
                
                color = colors.get(class_name, (255, 255, 255))
                
                # 바운딩 박스 그리기
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                # 라벨 텍스트
                label = f'{class_name}: {confidence:.2f}'
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                
                # 라벨 배경
                cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                             (x1 + label_size[0], y1), color, -1)
                
                # 라벨 텍스트
                cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # 7단계: 카운터 업데이트
    for name in TARGET_CLASSES.values():
        object_counts[name] = current_counts[name]
        max_counts[name] = max(max_counts[name], current_counts[name])
    
    # 8단계: 통계 정보 표시
    y_pos = 30
    cv2.putText(annotated_frame, 'Object Detection & Counting', 
               (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    y_pos += 30
    
    # 현재 탐지된 객체만 표시
    active_objects = [name for name, count in current_counts.items() if count > 0]
    if active_objects:
        for name in active_objects:
            text = f'{name}: {current_counts[name]} (Max: {max_counts[name]})'
            cv2.putText(annotated_frame, text, (10, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            y_pos += 20
    else:
        cv2.putText(annotated_frame, 'No target objects detected', 
                   (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    # 조작 가이드
    guide_text = 'Press Q to quit, R to reset counters'
    cv2.putText(annotated_frame, guide_text, (10, annotated_frame.shape[0] - 10), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    cv2.imshow('YOLO Specific Object Detection & Counting', annotated_frame)
    
    # 키보드 입력 처리
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        max_counts = {name: 0 for name in TARGET_CLASSES.values()}
        print("   🔄 카운터 리셋됨")

# 9단계: 최종 결과 출력
cap.release()
cv2.destroyAllWindows()

print("\n🎉 특정 객체 탐지 완료!")
print("\n📊 최종 통계:")
for name, count in max_counts.items():
    if count > 0:
        print(f"   - 최대 {name} 개수: {count}")

print("\n📚 학습 포인트:")
print("   - 특정 클래스 ID로 원하는 객체만 필터링할 수 있습니다.")
print("   - 실시간으로 객체 개수를 카운팅할 수 있습니다.")
print("   - 바운딩 박스와 라벨을 직접 커스터마이징할 수 있습니다.")
print("   - 색상 코딩으로 다양한 객체를 구분할 수 있습니다.")

print("\n🔍 YOLO에서 탐지 가능한 주요 객체들:")
all_classes = model.names
for i, name in all_classes.items():
    if i < 20:  # 처음 20개만 표시
        print(f"   {i:2d}: {name}")
print("   ... (총 80개 클래스)")
