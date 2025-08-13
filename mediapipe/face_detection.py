#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 얼굴 탐지 - 다중 얼굴 인식 및 분석 시스템
import cv2 # OpenCV 라이브러리, 비디오 및 이미지 처리에 사용됩니다.
import mediapipe as mp # MediaPipe 라이브러리, 얼굴 감지에 사용됩니다.
import numpy as np # NumPy 라이브러리, 수치 계산 및 배열 처리에 사용됩니다.
import math # 수학 계산을 위한 라이브러리입니다.

# MediaPipe 초기화
mp_face_detection = mp.solutions.face_detection # MediaPipe의 얼굴 감지 솔루션을 가져옵니다.
mp_drawing = mp.solutions.drawing_utils # MediaPipe의 그리기 관련 유틸리티를 가져옵니다.

class FaceAnalyzer: # 얼굴 분석을 위한 클래스를 정의합니다.
    def __init__(self):
        self.face_count_history = []  # 프레임별 감지된 얼굴 수를 기록하는 리스트입니다.
        self.detection_confidence = 0.7  # 초기 얼굴 탐지 신뢰도 임계값입니다.
        self.face_emotions = {}  # 얼굴별 감정 상태를 저장할 딕셔너리입니다. (이 예제에서는 가상)
        self.face_ids = {}  # 감지된 얼굴에 ID를 부여하고 추적하기 위한 딕셔너리입니다.
        self.next_face_id = 1 # 다음에 할당할 새로운 얼굴 ID입니다.
        
    def estimate_distance(self, detection, image_width):
        """얼굴 크기로 거리 추정 (상대적)"""
        # 감지된 얼굴의 경계 상자(bounding box) 정보를 가져옵니다.
        bbox = detection.location_data.relative_bounding_box
        # 이미지 너비와 상대적 너비를 곱해 실제 픽셀 너비를 계산합니다.
        face_width = bbox.width * image_width
        # 경험적인 공식을 사용하여 거리를 추정합니다. (실제 물리적 거리는 아님)
        estimated_distance = max(1, int(300 / max(face_width, 50)))
        return estimated_distance
    
    def analyze_face_orientation(self, detection):
        """얼굴 방향 분석 (좌우)"""
        bbox = detection.location_data.relative_bounding_box
        # 얼굴 경계 상자의 중심 x 좌표를 계산합니다.
        center_x = bbox.xmin + bbox.width / 2
        
        # 중심 x 좌표가 이미지의 어느 쪽에 위치하는지에 따라 방향을 추정합니다.
        if center_x < 0.4:
            return "Right looking"
        elif center_x > 0.6:
            return "Left looking"
        else:
            return "Front looking"  # 정면을 보고 있는 경우
    
    def get_face_size_category(self, detection, image_width, image_height):
        """얼굴 크기 분류"""
        bbox = detection.location_data.relative_bounding_box
        # 얼굴 영역의 넓이를 계산합니다.
        face_area = bbox.width * bbox.height
        image_area = 1.0  # 상대 좌표에서 전체 이미지의 면적은 1입니다.
        
        # 전체 이미지 면적 대비 얼굴 면적의 비율을 계산합니다.
        face_ratio = face_area / image_area
        
        # 비율에 따라 얼굴 크기 카테고리와 색상을 반환합니다.
        if face_ratio > 0.1:
            return "Very Close", (0, 255, 0)  # 초록
        elif face_ratio > 0.05:
            return "Close", (0, 255, 255)      # 노랑
        elif face_ratio > 0.02:
            return "Normal", (255, 255, 0)        # 청록
        else:
            return "Far", (255, 0, 0)          # 빨강
    
    def track_face_id(self, detection):
        """간단한 얼굴 ID 추적"""
        bbox = detection.location_data.relative_bounding_box
        # 현재 감지된 얼굴의 중심 좌표를 계산합니다.
        center_x = bbox.xmin + bbox.width / 2
        center_y = bbox.ymin + bbox.height / 2
        
        # 이전에 추적되던 얼굴들과의 거리를 계산합니다.
        min_distance = float('inf')
        matched_id = None
        
        for face_id, (prev_x, prev_y) in self.face_ids.items():
            distance = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
            # 거리가 가장 가깝고, 특정 임계값보다 작은 경우 동일한 얼굴로 간주합니다.
            if distance < min_distance and distance < 0.2:
                min_distance = distance
                matched_id = face_id
        
        if matched_id:
            # 기존 얼굴의 위치를 현재 위치로 업데이트합니다.
            self.face_ids[matched_id] = (center_x, center_y)
            return matched_id
        else:
            # 새로운 얼굴일 경우, 새 ID를 할당하고 등록합니다.
            new_id = self.next_face_id
            self.face_ids[new_id] = (center_x, center_y)
            self.next_face_id += 1
            return new_id
    
    def cleanup_old_faces(self, current_detections):
        """화면에서 사라진 얼굴 ID 정리"""
        if not current_detections: # 현재 프레임에 감지된 얼굴이 없으면
            self.face_ids.clear() # 모든 ID를 삭제하고
            self.next_face_id = 1 # ID 카운터를 리셋합니다.
            return
        
        # 현재 프레임에 있는 모든 얼굴의 중심점을 수집합니다.
        current_centers = []
        for detection in current_detections:
            bbox = detection.location_data.relative_bounding_box
            center_x = bbox.xmin + bbox.width / 2
            center_y = bbox.ymin + bbox.height / 2
            current_centers.append((center_x, center_y))
        
        # 이전에 추적되던 ID들 중 현재 프레임에 없는 ID를 찾아 제거합니다.
        ids_to_remove = []
        for face_id, (prev_x, prev_y) in self.face_ids.items():
            found_match = False
            for center_x, center_y in current_centers:
                distance = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
                if distance < 0.2: # 임계값 내에서 매칭되는 얼굴이 있으면
                    found_match = True
                    break
            if not found_match: # 매칭되는 얼굴이 없으면
                ids_to_remove.append(face_id) # 제거 목록에 추가합니다.
        
        for face_id in ids_to_remove:
            del self.face_ids[face_id]
    
    def update_statistics(self, face_count):
        """얼굴 수 통계 업데이트"""
        self.face_count_history.append(face_count) # 현재 프레임의 얼굴 수를 히스토리에 추가합니다.
        if len(self.face_count_history) > 300:  # 최근 300프레임(약 10초)의 데이터만 유지합니다.
            self.face_count_history.pop(0)
    
    def get_statistics(self):
        """통계 정보 반환"""
        if not self.face_count_history:
            return 0, 0, 0
        
        # 평균, 최대, 최소 얼굴 수를 계산하여 반환합니다.
        avg_faces = sum(self.face_count_history) / len(self.face_count_history)
        max_faces = max(self.face_count_history)
        min_faces = min(self.face_count_history)
        
        return avg_faces, max_faces, min_faces
    
    def adjust_confidence(self, increase=True):
        """탐지 신뢰도 조절"""
        if increase: # 신뢰도를 높입니다.
            self.detection_confidence = min(1.0, self.detection_confidence + 0.05)
        else: # 신뢰도를 낮춥니다.
            self.detection_confidence = max(0.1, self.detection_confidence - 0.05)
        print(f"탐지 신뢰도: {self.detection_confidence:.2f}")

# 웹캠 시작
cap = cv2.VideoCapture(0) # 0번 카메라(기본 웹캠)를 엽니다.
analyzer = FaceAnalyzer() # FaceAnalyzer 클래스의 인스턴스를 생성합니다.

# 사용자 안내 메시지를 출력합니다.
print("=== 얼굴 탐지 시스템 ===")
print("↑/↓: 탐지 신뢰도 조절")
print("r: 통계 리셋")
print("s: 스크린샷")
print("q: 종료")

# 얼굴별 경계 상자에 사용할 색상 팔레트를 정의합니다.
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
          (255, 0, 255), (0, 255, 255), (128, 128, 128), (255, 128, 0)]

# MediaPipe 얼굴 감지 모델을 로드합니다.
with mp_face_detection.FaceDetection(
    model_selection=0,  # 0은 짧은 거리(2m 이내) 모델, 1은 긴 거리(5m) 모델입니다.
    min_detection_confidence=analyzer.detection_confidence
) as face_detection:
    
    frame_count = 0 # 프레임 카운터를 초기화합니다.
    
    while cap.isOpened(): # 웹캠이 열려 있는 동안 계속 반복합니다.
        ret, frame = cap.read() # 웹캠에서 한 프레임을 읽어옵니다.
        if not ret: # 프레임을 제대로 읽어오지 못했다면 루프를 종료합니다.
            break
        
        frame_count += 1 # 프레임 카운터를 1 증가시킵니다.
        
        # 이미지 처리
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 이미지를 BGR에서 RGB로 변환합니다.
        image.flags.writeable = False # 성능 향상을 위해 이미지에 쓰기 작업을 비활성화합니다.
        
        # 얼굴 탐지 수행
        results = face_detection.process(image) # MediaPipe 모델로 얼굴을 탐지합니다.
        
        # 이미지 다시 변환
        image.flags.writeable = True # 화면에 그리기 위해 쓰기 작업을 다시 활성화합니다.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # 이미지를 다시 RGB에서 BGR로 변환합니다.
        height, width = image.shape[:2] # 이미지의 높이와 너비를 가져옵니다.
        
        face_count = 0 # 현재 프레임의 얼굴 수를 초기화합니다.
        current_detections = [] # 현재 프레임에서 감지된 얼굴 정보를 저장할 리스트입니다.
        
        if results.detections: # 감지된 얼굴이 있으면
            current_detections = results.detections
            face_count = len(results.detections) # 얼굴 수를 셉니다.
            
            # 얼굴별 분석 및 그리기
            for i, detection in enumerate(results.detections):
                # 얼굴 ID를 추적하거나 새로 할당합니다.
                face_id = analyzer.track_face_id(detection)
                
                # 경계 상자의 상대 좌표를 실제 이미지 좌표로 변환합니다.
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * width)
                y = int(bbox.ymin * height)
                w = int(bbox.width * width)
                h = int(bbox.height * height)
                
                # 얼굴 ID에 따라 고유한 색상을 선택합니다.
                color = colors[face_id % len(colors)]
                
                # 얼굴 주위에 경계 상자를 그립니다.
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                
                # 얼굴 정보를 분석합니다.
                distance = analyzer.estimate_distance(detection, width) # 거리 추정
                orientation = analyzer.analyze_face_orientation(detection) # 방향 분석
                size_category, size_color = analyzer.get_face_size_category(detection, width, height) # 크기 분류
                confidence = detection.score[0] # 탐지 신뢰도
                
                # 분석된 정보를 텍스트로 화면에 표시합니다.
                info_y = y - 10 # 텍스트를 표시할 y 시작 위치
                cv2.putText(image, f"Face ID: {face_id}", (x, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                info_y -= 20
                cv2.putText(image, f"Conf: {confidence:.2f}", (x, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                
                info_y -= 15
                cv2.putText(image, f"Dist: ~{distance}cm", (x, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                
                info_y -= 15
                cv2.putText(image, orientation, (x, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                
                info_y -= 15
                cv2.putText(image, size_category, (x, info_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, size_color, 1)
                
                # 얼굴 중심에 점을 그립니다.
                center_x = int((bbox.xmin + bbox.width / 2) * width)
                center_y = int((bbox.ymin + bbox.height / 2) * height)
                cv2.circle(image, (center_x, center_y), 3, color, -1)
        
        # 화면에서 사라진 얼굴 ID를 정리합니다.
        analyzer.cleanup_old_faces(current_detections)
        
        # 통계를 업데이트합니다.
        analyzer.update_statistics(face_count)
        avg_faces, max_faces, min_faces = analyzer.get_statistics()
        
        # 화면 상단에 표시할 정보 패널을 생성합니다.
        info_panel = np.zeros((100, width, 3), dtype=np.uint8)
        
        # 정보 패널에 현재 상태 및 통계 정보를 표시합니다.
        cv2.putText(info_panel, f"Current Faces: {face_count}", (10, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(info_panel, f"Detection Confidence: {analyzer.detection_confidence:.2f}", (10, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.putText(info_panel, f"Avg: {avg_faces:.1f} | Max: {max_faces} | Min: {min_faces}", (10, 75), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # 정보 패널과 비디오 프레임을 수직으로 합칩니다.
        combined = np.vstack([info_panel, image])
        
        # 조작 안내 문구를 표시합니다.
        cv2.putText(combined, "UP/DOWN: Confidence | R: Reset | S: Screenshot | Q: Quit", 
                   (10, combined.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        cv2.imshow('Face Detection & Analysis', combined) # 최종 이미지를 창에 보여줍니다.
        
        # 키 입력을 처리합니다.
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # 'q' 키: 종료
            break
        elif key == 82:  # 위 방향키 (Keycode may vary)
            analyzer.adjust_confidence(increase=True) # 신뢰도 증가
            # 참고: MediaPipe 객체를 신뢰도 변경 후 재생성해야 적용됩니다. 이 예제에서는 생략됨.
        elif key == 84:  # 아래 방향키 (Keycode may vary)
            analyzer.adjust_confidence(increase=False) # 신뢰도 감소
        elif key == ord('r'): # 'r' 키: 리셋
            analyzer.face_count_history.clear()
            analyzer.face_ids.clear()
            analyzer.next_face_id = 1
            print("통계 리셋됨!")
        elif key == ord('s'): # 's' 키: 스크린샷
            filename = f'face_detection_{frame_count}.jpg'
            cv2.imwrite(filename, combined)
            print(f"스크린샷 저장: {filename}")

cap.release() # 사용이 끝난 웹캠 리소스를 해제합니다.
cv2.destroyAllWindows() # 모든 OpenCV 창을 닫습니다.

# 최종 통계 출력
print("\n=== 세션 통계 ===")
avg_faces, max_faces, min_faces = analyzer.get_statistics()
print(f"평균 얼굴 수: {avg_faces:.2f}")
print(f"최대 얼굴 수: {max_faces}")
print(f"최소 얼굴 수: {min_faces}")
print(f"총 프레임 수: {len(analyzer.face_count_history)}")
print(f"최종 탐지 신뢰도: {analyzer.detection_confidence:.2f}")
print("분석 완료!")