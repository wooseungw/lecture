# YOLO 학습 가이드 및 설치 방법
# 초보자를 위한 완전한 설정 가이드

print("🤖 YOLO 객체 탐지 학습 가이드")
print("=" * 60)

print("\n📦 1. 필수 라이브러리 설치")
print("-" * 30)
print("터미널에서 다음 명령어들을 순서대로 실행하세요:")
print()
print("pip install ultralytics")
print("pip install opencv-python")
print("pip install torch torchvision")  # PyTorch
print("pip install pillow")
print("pip install numpy")

print("\n🎯 2. YOLO 모델 종류")
print("-" * 30)
models = {
    'yolov8n.pt': '가장 빠름, 가장 작음 (6MB)',
    'yolov8s.pt': '빠름, 작음 (22MB)', 
    'yolov8m.pt': '보통 속도, 보통 크기 (52MB)',
    'yolov8l.pt': '느림, 큰 크기 (87MB)',
    'yolov8x.pt': '가장 느림, 가장 큼 (136MB)'
}

for model, desc in models.items():
    print(f"  {model:<15} - {desc}")

print("\n🏃‍♂️ 3. 포즈 추정 모델")
print("-" * 30)
pose_models = {
    'yolov8n-pose.pt': '포즈 추정용 nano 모델',
    'yolov8s-pose.pt': '포즈 추정용 small 모델',
    'yolov8m-pose.pt': '포즈 추정용 medium 모델'
}

for model, desc in pose_models.items():
    print(f"  {model:<18} - {desc}")

print("\n🔍 4. YOLO로 탐지 가능한 객체들 (총 80개)")
print("-" * 30)
coco_classes = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
    'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

# 카테고리별로 정리
categories = {
    '사람/동물': ['person', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe'],
    '교통수단': ['bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat'],
    '가구/가전': ['chair', 'couch', 'bed', 'dining table', 'tv', 'laptop', 'microwave', 'refrigerator'],
    '음식': ['bottle', 'cup', 'banana', 'apple', 'orange', 'pizza', 'cake'],
    '일상용품': ['backpack', 'handbag', 'cell phone', 'book', 'scissors', 'toothbrush']
}

for category, items in categories.items():
    print(f"\n  📂 {category}:")
    for i in range(0, len(items), 4):
        group = items[i:i+4]
        print(f"    {', '.join(group)}")

print("\n💻 5. 기본 사용법")
print("-" * 30)
basic_code = '''
from ultralytics import YOLO
import cv2

# 모델 로드
model = YOLO('yolov8n.pt')

# 이미지 탐지
results = model('your_image.jpg')
results[0].show()  # 결과 표시

# 웹캠 실시간 탐지
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow('YOLO', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
'''

print(basic_code)

print("\n⚙️ 6. 주요 매개변수")
print("-" * 30)
parameters = {
    'conf': '신뢰도 임계값 (0.0-1.0, 기본값: 0.25)',
    'iou': 'IoU 임계값 (0.0-1.0, 기본값: 0.45)', 
    'device': '실행 장치 ("cpu", "0" for GPU)',
    'classes': '특정 클래스만 탐지 ([0, 15, 16] for person, cat, dog)',
    'verbose': '출력 메시지 제어 (True/False)',
    'save': '결과 저장 여부 (True/False)'
}

for param, desc in parameters.items():
    print(f"  {param:<10} - {desc}")

print("\n🎨 7. 고급 사용 예제")
print("-" * 30)
advanced_code = '''
# 특정 객체만 탐지 (사람, 자동차)
results = model(frame, classes=[0, 2], conf=0.6)

# GPU 사용
results = model(frame, device='0')

# 결과 데이터 접근
for box in results[0].boxes:
    class_id = int(box.cls)
    confidence = float(box.conf) 
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    print(f"클래스: {model.names[class_id]}, 신뢰도: {confidence:.2f}")
'''

print(advanced_code)

print("\n🚨 8. 문제 해결")
print("-" * 30)
troubleshooting = [
    "🔧 'No module named ultralytics' → pip install ultralytics",
    "🔧 모델 다운로드 실패 → 인터넷 연결 확인", 
    "🔧 웹캠 열리지 않음 → 다른 앱에서 카메라 사용 중인지 확인",
    "🔧 느린 처리 속도 → yolov8n.pt 모델 사용 또는 해상도 낮추기",
    "🔧 GPU 사용 안됨 → torch GPU 버전 설치 확인"
]

for tip in troubleshooting:
    print(f"  {tip}")

print("\n🎓 9. 학습 순서 추천")
print("-" * 30)
learning_path = [
    "1️⃣ yolo_ex_1_basic.py - 기본 이미지 탐지",
    "2️⃣ yolo_ex_2_webcam.py - 실시간 웹캠 탐지", 
    "3️⃣ yolo_ex_3_counting.py - 특정 객체 카운팅",
    "4️⃣ yolo_ex_4_pose.py - 포즈 추정 및 동작 인식",
    "5️⃣ yolo_ex_5_security.py - 종합 보안 시스템"
]

for step in learning_path:
    print(f"  {step}")

print("\n🔗 10. 참고 자료")
print("-" * 30)
resources = [
    "📖 Ultralytics 공식 문서: https://docs.ultralytics.com",
    "💻 GitHub 저장소: https://github.com/ultralytics/ultralytics", 
    "🎥 YouTube 튜토리얼 검색: 'YOLO v8 tutorial'",
    "💬 커뮤니티: Stack Overflow, Reddit r/computervision"
]

for resource in resources:
    print(f"  {resource}")

print("\n✅ 설치 완료 후 첫 번째 테스트:")
print("-" * 30)
test_code = '''
from ultralytics import YOLO

# 모델 다운로드 테스트
model = YOLO('yolov8n.pt')
print("✅ YOLO 설치 및 모델 다운로드 성공!")
print(f"탐지 가능한 클래스 수: {len(model.names)}")
'''
print(test_code)

print(f"\n🎉 YOLO 학습 준비 완료!")
print(f"이제 yolo_ex_1_basic.py부터 차례대로 실행해보세요!")
