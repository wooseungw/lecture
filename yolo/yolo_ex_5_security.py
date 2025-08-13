#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# YOLO 종합 예제 5: 스마트 보안 시스템
# 초보자를 위한 실전 활용 예제

import cv2
from ultralytics import YOLO
import numpy as np
import time
from datetime import datetime
import os

print("YOLO 종합 예제 5: 스마트 보안 시스템")
print("=" * 50)

class SmartSecuritySystem:
    def __init__(self):
        print("1. 스마트 보안 시스템 초기화 중...")
        
        # 모델 로드
        self.detection_model = YOLO('yolov8n.pt')
        print("   ✓ 객체 탐지 모델 로드 완료")
        
        # 관심 객체 (보안상 중요한 객체들)
        self.security_classes = {
            0: 'person',      # 사람 - 가장 중요!
            2: 'car',         # 자동차
            7: 'truck',       # 트럭
            15: 'cat',        # 고양이
            16: 'dog',        # 개
            67: 'cell phone'  # 핸드폰
        }
        
        # 알림 설정
        self.last_alert_time = {}
        self.alert_cooldown = 3  # 3초 간격으로 알림
        
        # 통계
        self.detection_history = []
        self.session_start = time.time()
        
        # 스크린샷 저장 폴더
        self.screenshot_dir = "security_screenshots"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            print(f"   ✓ 스크린샷 폴더 생성: {self.screenshot_dir}")
        
        print("   ✓ 보안 시스템 초기화 완료!")
    
    def is_alert_needed(self, class_name):
        """알림이 필요한지 확인 (중복 알림 방지)"""
        current_time = time.time()
        if class_name not in self.last_alert_time:
            self.last_alert_time[class_name] = current_time
            return True
        
        if current_time - self.last_alert_time[class_name] > self.alert_cooldown:
            self.last_alert_time[class_name] = current_time
            return True
        
        return False
    
    def save_screenshot(self, frame, detected_objects):
        """보안 이벤트 스크린샷 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        objects_str = "_".join(detected_objects[:3])  # 최대 3개 객체 이름
        filename = f"security_{timestamp}_{objects_str}.jpg"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        cv2.imwrite(filepath, frame)
        print(f"   📸 스크린샷 저장: {filename}")
        return filename
    
    def analyze_frame(self, frame):
        """프레임 분석 및 보안 이벤트 탐지"""
        results = self.detection_model(frame, verbose=False)
        detected_objects = []
        high_priority_alerts = []
        
        boxes = results[0].boxes
        if boxes is not None:
            for box in boxes:
                class_id = int(box.cls)
                confidence = float(box.conf)
                
                if class_id in self.security_classes and confidence > 0.6:
                    class_name = self.security_classes[class_id]
                    detected_objects.append(class_name)
                    
                    # 사람 탐지는 높은 우선순위
                    if class_name == 'person' and confidence > 0.7:
                        if self.is_alert_needed('person'):
                            high_priority_alerts.append(f"🚨 사람 탐지됨! (신뢰도: {confidence:.2f})")
                            self.save_screenshot(frame, ['person'])
                    
                    # 차량 탐지
                    elif class_name in ['car', 'truck'] and confidence > 0.6:
                        if self.is_alert_needed(class_name):
                            high_priority_alerts.append(f"🚗 {class_name} 탐지됨!")
        
        # 탐지 기록 저장
        if detected_objects:
            self.detection_history.append({
                'time': time.time(),
                'objects': detected_objects,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
        
        return results, detected_objects, high_priority_alerts
    
    def draw_security_info(self, frame, results, detected_objects, alerts):
        """보안 정보를 프레임에 그리기"""
        annotated_frame = frame.copy()
        
        # 객체 탐지 결과 그리기
        boxes = results[0].boxes
        if boxes is not None:
            for box in boxes:
                class_id = int(box.cls)
                confidence = float(box.conf)
                
                if class_id in self.security_classes and confidence > 0.6:
                    class_name = self.security_classes[class_id]
                    
                    # 바운딩 박스 색상 (사람은 빨간색으로 강조)
                    if class_name == 'person':
                        color = (0, 0, 255)  # 빨간색
                        thickness = 3
                    else:
                        color = (0, 255, 0)  # 초록색
                        thickness = 2
                    
                    # 바운딩 박스 그리기
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, thickness)
                    
                    # 라벨
                    label = f'{class_name}: {confidence:.2f}'
                    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                    
                    cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10),
                                 (x1 + label_size[0], y1), color, -1)
                    cv2.putText(annotated_frame, label, (x1, y1 - 5),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # 보안 시스템 상태 표시
        status_y = 30
        cv2.putText(annotated_frame, '🛡️  SMART SECURITY SYSTEM', 
                   (10, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        status_y += 40
        
        # 현재 시간
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(annotated_frame, f'Time: {current_time}', 
                   (10, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        status_y += 25
        
        # 탐지된 객체 목록
        if detected_objects:
            unique_objects = list(set(detected_objects))
            objects_text = f'Detected: {", ".join(unique_objects)}'
            cv2.putText(annotated_frame, objects_text, 
                       (10, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            status_y += 25
        else:
            cv2.putText(annotated_frame, 'Status: All Clear ✅', 
                       (10, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            status_y += 25
        
        # 알림 메시지
        for i, alert in enumerate(alerts[-3:]):  # 최근 3개 알림만 표시
            cv2.putText(annotated_frame, alert, 
                       (10, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            status_y += 25
        
        # 세션 통계
        session_time = int(time.time() - self.session_start)
        total_detections = len(self.detection_history)
        stats_text = f'Session: {session_time//60:02d}:{session_time%60:02d} | Events: {total_detections}'
        cv2.putText(annotated_frame, stats_text, 
                   (10, annotated_frame.shape[0] - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # 조작 가이드
        cv2.putText(annotated_frame, 'Q: Quit | S: Screenshot | R: Reset Stats', 
                   (10, annotated_frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return annotated_frame
    
    def run(self):
        """보안 시스템 실행"""
        print("\n2. 웹캠 연결 중...")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        
        if not cap.isOpened():
            print("   ⚠️  웹캠을 열 수 없습니다.")
            return
        
        print("   ✓ 웹캠 연결 완료!")
        print("\n3. 🛡️  보안 시스템 가동 시작")
        print("   💡 사람이 감지되면 자동으로 알림과 스크린샷이 저장됩니다.")
        print("   💡 'Q': 종료, 'S': 수동 스크린샷, 'R': 통계 리셋")
        
        all_alerts = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 프레임 분석
            results, detected_objects, new_alerts = self.analyze_frame(frame)
            all_alerts.extend(new_alerts)
            
            # 새 알림 출력
            for alert in new_alerts:
                print(f"   {alert}")
            
            # 화면에 정보 표시
            display_frame = self.draw_security_info(frame, results, detected_objects, all_alerts)
            
            cv2.imshow('🛡️  Smart Security System', display_frame)
            
            # 키보드 입력 처리
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = self.save_screenshot(display_frame, detected_objects or ['manual'])
                print(f"   📸 수동 스크린샷 저장: {filename}")
            elif key == ord('r'):
                self.detection_history = []
                all_alerts = []
                self.session_start = time.time()
                print("   🔄 통계 리셋됨")
        
        # 세션 요약
        cap.release()
        cv2.destroyAllWindows()
        
        print("\n🛡️  보안 시스템 종료")
        print("📊 세션 요약:")
        print(f"   - 총 가동 시간: {int(time.time() - self.session_start)}초")
        print(f"   - 총 탐지 이벤트: {len(self.detection_history)}건")
        print(f"   - 저장된 스크린샷: {len(os.listdir(self.screenshot_dir))}장")
        
        # 최근 이벤트 목록
        if self.detection_history:
            print("\n📋 최근 탐지 이벤트:")
            for event in self.detection_history[-5:]:  # 최근 5개만
                objects_str = ", ".join(event['objects'])
                print(f"   {event['timestamp']}: {objects_str}")

def main():
    # 보안 시스템 실행
    security_system = SmartSecuritySystem()
    security_system.run()
    
    print("\n📚 학습 포인트:")
    print("   - YOLO를 활용한 실시간 보안 시스템 구축")
    print("   - 특정 객체 탐지 시 자동 알림 및 스크린샷 저장")
    print("   - 중복 알림 방지를 위한 쿨다운 시스템")
    print("   - 탐지 이력 관리 및 통계 제공")
    print("   - 사용자 인터페이스와 키보드 제어")

if __name__ == "__main__":
    main()
