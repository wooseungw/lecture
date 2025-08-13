#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
노인 활동 모니터링 시스템 - 간단 데모
기본 기능만 포함한 가벼운 버전
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import math
from collections import deque

class SimpleElderlyMonitor:
    def __init__(self):
        """간단 모니터링 시스템 초기화"""
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        
        # 간단한 데이터 저장
        self.movement_history = deque(maxlen=90)  # 3초간
        self.pose_history = deque(maxlen=30)      # 1초간
        
        # 상태 변수
        self.current_activity = "대기 중"
        self.fall_risk_level = 0
        self.last_movement_time = time.time()
        
        print("🏥 간단 노인 모니터링 데모가 시작됩니다.")
        print("📺 카메라 화면에서 자세와 활동을 분석합니다.")

    def calculate_body_angle(self, landmarks):
        """몸의 기울기 간단 계산"""
        try:
            # 어깨와 엉덩이 중심점
            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
            
            shoulder_center = ((left_shoulder.x + right_shoulder.x) / 2, 
                             (left_shoulder.y + right_shoulder.y) / 2)
            hip_center = ((left_hip.x + right_hip.x) / 2, 
                         (left_hip.y + right_hip.y) / 2)
            
            # 수직선과의 각도 계산
            dx = shoulder_center[0] - hip_center[0]
            dy = shoulder_center[1] - hip_center[1]
            angle = math.degrees(math.atan2(abs(dx), abs(dy)))
            
            return angle
            
        except Exception:
            return 0

    def analyze_movement(self, landmarks):
        """간단한 움직임 분석"""
        try:
            # 주요 관절들의 중심점 계산
            key_points = [
                landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value],
                landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value],
                landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value],
                landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            ]
            
            center_x = np.mean([p.x for p in key_points if p.visibility > 0.5])
            center_y = np.mean([p.y for p in key_points if p.visibility > 0.5])
            
            movement = 0
            if len(self.movement_history) > 0:
                prev_center = self.movement_history[-1]
                dx = center_x - prev_center[0]
                dy = center_y - prev_center[1]
                movement = np.sqrt(dx*dx + dy*dy)
                
                if movement > 0.01:
                    self.last_movement_time = time.time()
            
            self.movement_history.append((center_x, center_y))
            
            # 활동 수준 분류
            if len(self.movement_history) >= 30:  # 1초간 데이터
                recent_moves = []
                for i in range(1, min(30, len(self.movement_history))):
                    curr = self.movement_history[-i]
                    prev = self.movement_history[-i-1]
                    move = np.sqrt((curr[0]-prev[0])**2 + (curr[1]-prev[1])**2)
                    recent_moves.append(move)
                
                avg_movement = np.mean(recent_moves)
                
                if avg_movement < 0.005:
                    self.current_activity = "😴 휴식 중"
                elif avg_movement < 0.02:
                    self.current_activity = "📖 조용한 활동"
                elif avg_movement < 0.05:
                    self.current_activity = "🚶 보통 활동"
                else:
                    self.current_activity = "🏃 활발한 활동"
            
            return movement
            
        except Exception:
            return 0

    def check_fall_risk(self, landmarks):
        """간단한 낙상 위험 체크"""
        try:
            # 몸 기울기
            body_angle = self.calculate_body_angle(landmarks)
            
            # 머리와 엉덩이 높이 비교
            nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
            hip_avg_y = (left_hip.y + right_hip.y) / 2
            
            head_hip_ratio = nose.y / hip_avg_y if hip_avg_y > 0 else 1
            
            # 위험도 계산
            risk_factors = 0
            
            if body_angle > 50:  # 몸이 많이 기울어짐
                risk_factors += 1
            
            if head_hip_ratio > 1.1:  # 머리가 엉덩이보다 낮음
                risk_factors += 1
            
            # 급격한 자세 변화 체크
            current_pose = {'angle': body_angle, 'ratio': head_hip_ratio}
            self.pose_history.append(current_pose)
            
            if len(self.pose_history) >= 15:  # 0.5초간 데이터
                recent_angles = [p['angle'] for p in list(self.pose_history)[-15:]]
                angle_change = max(recent_angles) - min(recent_angles)
                
                if angle_change > 30:  # 급격한 변화
                    risk_factors += 1
            
            self.fall_risk_level = risk_factors
            return risk_factors
            
        except Exception:
            return 0

    def draw_simple_info(self, image, landmarks=None):
        """간단한 정보 표시"""
        height, width = image.shape[:2]
        
        # 반투명 배경
        overlay = image.copy()
        cv2.rectangle(overlay, (10, 10), (350, 150), (0, 0, 0), -1)
        image = cv2.addWeighted(image, 0.8, overlay, 0.2, 0)
        
        # 제목
        cv2.putText(image, "노인 모니터링 데모", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # 현재 활동
        activity_color = (0, 255, 0) if "활발한" in self.current_activity else \
                        (0, 255, 255) if "보통" in self.current_activity else \
                        (255, 255, 0) if "조용한" in self.current_activity else (128, 128, 128)
        
        cv2.putText(image, f"상태: {self.current_activity}", (20, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, activity_color, 2)
        
        # 비활성 시간
        inactive_time = int(time.time() - self.last_movement_time)
        inactive_color = (0, 0, 255) if inactive_time > 60 else (255, 255, 255)
        cv2.putText(image, f"비활성: {inactive_time}초", (20, 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, inactive_color, 2)
        
        # 낙상 위험도
        if landmarks:
            fall_risk = self.check_fall_risk(landmarks)
            if fall_risk >= 2:
                risk_text = "🚨 위험"
                risk_color = (0, 0, 255)
            elif fall_risk == 1:
                risk_text = "⚠️ 주의"
                risk_color = (0, 165, 255)
            else:
                risk_text = "✅ 안전"
                risk_color = (0, 255, 0)
            
            cv2.putText(image, f"낙상: {risk_text}", (20, 125), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, risk_color, 2)
        
        # 비활성 경고
        if inactive_time > 120:  # 2분
            cv2.putText(image, "⚠️ 장시간 움직임 없음", (width//2-100, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    def run_demo(self):
        """데모 실행"""
        with self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=0  # 가장 빠른 모드
        ) as pose:
            
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("❌ 카메라를 열 수 없습니다.")
                return
            
            print("🎥 카메라 시작!")
            print("📝 조작법: 'q' 또는 ESC로 종료")
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # 좌우 반전으로 자연스러운 움직임
                frame = cv2.flip(frame, 1)
                
                # 자세 검출
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame.flags.writeable = False
                results = pose.process(rgb_frame)
                
                # 이미지 복원
                rgb_frame.flags.writeable = True
                frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                
                if results.pose_landmarks:
                    # 스켈레톤 그리기
                    self.mp_draw.draw_landmarks(
                        frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                    )
                    
                    # 움직임 분석
                    self.analyze_movement(results.pose_landmarks.landmark)
                    
                    # 정보 표시
                    self.draw_simple_info(frame, results.pose_landmarks.landmark)
                else:
                    # 사람이 감지되지 않은 경우
                    self.draw_simple_info(frame)
                    cv2.putText(frame, "사람을 찾고 있습니다...", 
                               (frame.shape[1]//2-120, frame.shape[0]//2), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # 화면 출력
                cv2.imshow('노인 활동 모니터링 데모', frame)
                
                # 키 입력 체크
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' 또는 ESC
                    break
            
            # 정리
            cap.release()
            cv2.destroyAllWindows()
            print("👋 데모를 종료합니다.")

if __name__ == "__main__":
    print("🚀 노인 활동 모니터링 간단 데모를 시작합니다!")
    print("⚡ 가벼운 버전으로 기본 기능만 제공합니다.\n")
    
    try:
        demo = SimpleElderlyMonitor()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단됨")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    print("✨ 전체 기능을 원한다면 'elderly_monitoring_system.py'를 실행하세요!")
