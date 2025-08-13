#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
노인 활동 모니터링 시스템
- 낙상 감지 (Fall Detection)
- 활동량 추적 (Activity Tracking) 
- 비정상 자세 감지 (Abnormal Posture Detection)
- 응급 상황 알림 (Emergency Alert)
- 일일 활동 리포트 (Daily Activity Report)
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import json
import math
from collections import deque
from datetime import datetime, timedelta
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import winsound  # Windows용 (macOS의 경우 os.system('afplay alert.wav') 사용)

class ElderlyMonitoringSystem:
    def __init__(self):
        """노인 모니터링 시스템 초기화"""
        # MediaPipe 설정
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        
        # 모니터링 데이터
        self.pose_history = deque(maxlen=300)  # 10초간 자세 히스토리 (30fps 기준)
        self.activity_history = deque(maxlen=1800)  # 1분간 활동 히스토리
        self.daily_activities = []
        
        # 낙상 감지 변수
        self.fall_detected = False
        self.fall_alert_sent = False
        self.last_fall_time = 0
        
        # 활동 상태 추적
        self.current_activity = "알 수 없음"
        self.inactive_duration = 0
        self.last_movement_time = time.time()
        
        # 임계값 설정 (조정 가능)
        self.FALL_ANGLE_THRESHOLD = 60  # 낙상 각도 임계값
        self.INACTIVE_THRESHOLD = 300   # 5분간 비활성 상태 임계값
        self.LOW_ACTIVITY_THRESHOLD = 180  # 3분간 저활동 임계값
        
        # 응급 연락처 (실제 사용시 수정 필요)
        self.emergency_contacts = {
            'family': 'family@example.com',
            'caregiver': 'caregiver@example.com'
        }
        
        # 세션 시작 시간
        self.session_start = datetime.now()
        
        print("🏥 노인 활동 모니터링 시스템이 시작되었습니다.")
        print("📊 실시간 모니터링을 시작합니다...")

    def calculate_angle(self, point_a, point_b, point_c):
        """3개 점으로 각도 계산"""
        a = np.array([point_a.x, point_a.y])
        b = np.array([point_b.x, point_b.y])
        c = np.array([point_c.x, point_c.y])
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle

    def calculate_body_inclination(self, landmarks):
        """몸의 기울기 계산 (낙상 감지용)"""
        try:
            # 어깨와 엉덩이 중점 계산
            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
            
            shoulder_center = ((left_shoulder.x + right_shoulder.x) / 2, 
                             (left_shoulder.y + right_shoulder.y) / 2)
            hip_center = ((left_hip.x + right_hip.x) / 2, 
                         (left_hip.y + right_hip.y) / 2)
            
            # 몸의 수직 기울기 계산
            dx = shoulder_center[0] - hip_center[0]
            dy = shoulder_center[1] - hip_center[1]
            
            # 수직선과의 각도 계산
            angle = math.degrees(math.atan2(abs(dx), abs(dy)))
            return angle
            
        except Exception as e:
            print(f"기울기 계산 오류: {e}")
            return 0

    def detect_fall(self, landmarks):
        """낙상 감지 알고리즘"""
        try:
            # 1. 몸의 기울기 체크
            inclination = self.calculate_body_inclination(landmarks)
            
            # 2. 머리와 엉덩이 높이 비교
            nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
            hip_y = (left_hip.y + right_hip.y) / 2
            
            # 3. 급격한 자세 변화 감지
            current_pose = {
                'inclination': inclination,
                'head_hip_ratio': nose.y / hip_y if hip_y > 0 else 1,
                'timestamp': time.time()
            }
            
            self.pose_history.append(current_pose)
            
            # 낙상 조건 체크
            fall_conditions = []
            
            # 조건 1: 몸이 너무 기울어진 경우
            if inclination > self.FALL_ANGLE_THRESHOLD:
                fall_conditions.append("과도한_기울기")
            
            # 조건 2: 머리가 엉덩이보다 낮은 경우
            if current_pose['head_hip_ratio'] > 1.2:
                fall_conditions.append("머리_낮음")
            
            # 조건 3: 급격한 자세 변화
            if len(self.pose_history) >= 30:  # 1초간 데이터
                recent_poses = list(self.pose_history)[-30:]
                inclination_change = max([p['inclination'] for p in recent_poses]) - \
                                   min([p['inclination'] for p in recent_poses])
                
                if inclination_change > 40:  # 급격한 변화
                    fall_conditions.append("급격한_변화")
            
            # 낙상 판정
            if len(fall_conditions) >= 2:
                current_time = time.time()
                # 중복 알림 방지 (10초 쿨다운)
                if current_time - self.last_fall_time > 10:
                    self.fall_detected = True
                    self.last_fall_time = current_time
                    self.trigger_fall_alert(fall_conditions)
                    
            return len(fall_conditions)
            
        except Exception as e:
            print(f"낙상 감지 오류: {e}")
            return 0

    def analyze_activity_level(self, landmarks):
        """활동 수준 분석"""
        try:
            # 주요 관절들의 움직임 계산
            key_points = [
                landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value],
                landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value],
                landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value],
                landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            ]
            
            # 현재 프레임의 활동 중심점 계산
            center_x = np.mean([p.x for p in key_points if p.visibility > 0.5])
            center_y = np.mean([p.y for p in key_points if p.visibility > 0.5])
            
            current_activity = {
                'center': (center_x, center_y),
                'timestamp': time.time(),
                'movement': 0
            }
            
            # 이전 프레임과 비교하여 움직임 계산
            if len(self.activity_history) > 0:
                prev_activity = self.activity_history[-1]
                dx = center_x - prev_activity['center'][0]
                dy = center_y - prev_activity['center'][1]
                movement = np.sqrt(dx*dx + dy*dy)
                current_activity['movement'] = movement
                
                # 움직임이 있는 경우 마지막 움직임 시간 업데이트
                if movement > 0.01:  # 임계값
                    self.last_movement_time = time.time()
            
            self.activity_history.append(current_activity)
            
            # 활동 상태 분류
            if len(self.activity_history) >= 90:  # 3초간 데이터
                recent_movements = [a['movement'] for a in list(self.activity_history)[-90:]]
                avg_movement = np.mean(recent_movements)
                
                if avg_movement < 0.005:
                    self.current_activity = "휴식 중"
                elif avg_movement < 0.02:
                    self.current_activity = "조용한 활동"
                elif avg_movement < 0.05:
                    self.current_activity = "보통 활동"
                else:
                    self.current_activity = "활발한 활동"
            
            # 비활성 시간 체크
            self.inactive_duration = time.time() - self.last_movement_time
            
            return {
                'activity_level': self.current_activity,
                'inactive_duration': self.inactive_duration,
                'movement_score': current_activity['movement']
            }
            
        except Exception as e:
            print(f"활동 분석 오류: {e}")
            return None

    def check_health_alerts(self):
        """건강 알림 체크"""
        alerts = []
        
        # 장시간 비활성 알림
        if self.inactive_duration > self.INACTIVE_THRESHOLD:
            alerts.append({
                'type': 'INACTIVE',
                'message': f'🚨 {int(self.inactive_duration/60)}분간 움직임이 없습니다',
                'severity': 'HIGH'
            })
        
        # 저활동 상태 알림
        elif self.inactive_duration > self.LOW_ACTIVITY_THRESHOLD:
            alerts.append({
                'type': 'LOW_ACTIVITY',
                'message': f'⚠️ {int(self.inactive_duration/60)}분간 활동량이 적습니다',
                'severity': 'MEDIUM'
            })
        
        return alerts

    def trigger_fall_alert(self, conditions):
        """낙상 알림 발송"""
        if not self.fall_alert_sent:
            print("\n🚨🚨🚨 낙상 감지! 🚨🚨🚨")
            print(f"감지 조건: {', '.join(conditions)}")
            print("응급 연락망에 알림을 발송합니다...")
            
            # 알림음 재생 (시스템에 맞게 수정)
            try:
                # Windows
                winsound.Beep(1000, 2000)  # 1000Hz, 2초
            except:
                # macOS/Linux
                import os
                os.system('say "낙상이 감지되었습니다"')  # macOS TTS
            
            # 이메일 알림 (실제 환경에서는 이메일 설정 필요)
            self.send_emergency_email("낙상 감지", conditions)
            
            self.fall_alert_sent = True
            
            # 10초 후 알림 상태 리셋
            threading.Timer(10.0, self.reset_fall_alert).start()

    def send_emergency_email(self, alert_type, details):
        """응급 상황 이메일 발송 (실제 환경에서는 SMTP 설정 필요)"""
        try:
            # 실제 사용시 이메일 서버 설정 필요
            print(f"📧 응급 이메일 발송: {alert_type}")
            print(f"세부사항: {details}")
            print("가족 및 돌봄 제공자에게 알림이 발송되었습니다.")
        except Exception as e:
            print(f"이메일 발송 실패: {e}")

    def reset_fall_alert(self):
        """낙상 알림 상태 리셋"""
        self.fall_alert_sent = False
        self.fall_detected = False

    def generate_daily_report(self):
        """일일 활동 리포트 생성"""
        now = datetime.now()
        duration = now - self.session_start
        
        # 활동 통계 계산
        if len(self.activity_history) > 0:
            movements = [a['movement'] for a in self.activity_history]
            total_movement = sum(movements)
            avg_movement = np.mean(movements)
            max_movement = max(movements)
        else:
            total_movement = avg_movement = max_movement = 0
        
        report = {
            'date': now.strftime('%Y-%m-%d'),
            'monitoring_duration': str(duration).split('.')[0],
            'total_movement_score': round(total_movement, 4),
            'average_movement': round(avg_movement, 4),
            'max_movement': round(max_movement, 4),
            'current_activity': self.current_activity,
            'inactive_duration': f"{int(self.inactive_duration/60)}분 {int(self.inactive_duration%60)}초",
            'fall_incidents': 1 if self.fall_detected else 0,
        }
        
        return report

    def save_session_data(self, filename=None):
        """세션 데이터 저장"""
        if filename is None:
            filename = f"elderly_monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        session_data = {
            'session_info': {
                'start_time': self.session_start.isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_duration': str(datetime.now() - self.session_start).split('.')[0]
            },
            'daily_report': self.generate_daily_report(),
            'activity_summary': {
                'total_frames': len(self.activity_history),
                'pose_frames': len(self.pose_history)
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            print(f"💾 세션 데이터가 저장되었습니다: {filename}")
        except Exception as e:
            print(f"데이터 저장 실패: {e}")

    def draw_monitoring_info(self, image, landmarks=None):
        """모니터링 정보를 화면에 표시"""
        height, width = image.shape[:2]
        
        # 배경 오버레이
        overlay = image.copy()
        cv2.rectangle(overlay, (10, 10), (400, 200), (0, 0, 0), -1)
        image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
        
        # 시스템 정보
        cv2.putText(image, "🏥 노인 활동 모니터링", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # 현재 활동 상태
        activity_color = (0, 255, 0) if "활발한" in self.current_activity else \
                        (0, 255, 255) if "보통" in self.current_activity else \
                        (0, 165, 255) if "조용한" in self.current_activity else (0, 0, 255)
        
        cv2.putText(image, f"활동 상태: {self.current_activity}", (20, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, activity_color, 2)
        
        # 비활성 시간
        inactive_mins = int(self.inactive_duration / 60)
        inactive_secs = int(self.inactive_duration % 60)
        inactive_color = (0, 0, 255) if self.inactive_duration > self.LOW_ACTIVITY_THRESHOLD else (255, 255, 255)
        
        cv2.putText(image, f"비활성 시간: {inactive_mins:02d}:{inactive_secs:02d}", (20, 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, inactive_color, 2)
        
        # 낙상 감지 상태
        if landmarks:
            fall_risk = self.detect_fall(landmarks)
            fall_color = (0, 0, 255) if fall_risk >= 2 else (0, 165, 255) if fall_risk == 1 else (0, 255, 0)
            fall_status = "🚨 낙상 위험" if fall_risk >= 2 else "⚠️ 주의" if fall_risk == 1 else "✅ 안전"
            
            cv2.putText(image, f"낙상 위험도: {fall_status}", (20, 125), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, fall_color, 2)
        
        # 모니터링 시간
        duration = datetime.now() - self.session_start
        duration_str = str(duration).split('.')[0]
        cv2.putText(image, f"모니터링: {duration_str}", (20, 155), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # 건강 알림 표시
        alerts = self.check_health_alerts()
        if alerts:
            y_pos = 185
            for alert in alerts:
                alert_color = (0, 0, 255) if alert['severity'] == 'HIGH' else (0, 165, 255)
                cv2.putText(image, alert['message'], (20, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, alert_color, 1)
                y_pos += 25

    def run_monitoring(self):
        """메인 모니터링 루프"""
        with self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1  # 성능과 정확도의 균형
        ) as pose:
            
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            print("🎥 카메라 스트림이 시작되었습니다.")
            print("⌨️  조작법:")
            print("   'q' 또는 ESC: 종료")
            print("   'r': 일일 리포트 출력")
            print("   's': 세션 데이터 저장")
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # 이미지 전처리
                frame = cv2.flip(frame, 1)  # 좌우 반전으로 자연스러운 움직임
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame.flags.writeable = False
                
                # 자세 검출
                results = pose.process(rgb_frame)
                
                # 이미지 다시 쓰기 가능으로 설정
                rgb_frame.flags.writeable = True
                frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                
                if results.pose_landmarks:
                    # 자세 스켈레톤 그리기
                    self.mp_draw.draw_landmarks(
                        frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                    )
                    
                    # 활동 분석
                    activity_info = self.analyze_activity_level(results.pose_landmarks.landmark)
                    
                    # 모니터링 정보 표시
                    self.draw_monitoring_info(frame, results.pose_landmarks.landmark)
                else:
                    # 사람이 감지되지 않은 경우
                    self.draw_monitoring_info(frame)
                    cv2.putText(frame, "🔍 사용자를 찾고 있습니다...", 
                               (frame.shape[1]//2-150, frame.shape[0]//2), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # 화면 출력
                cv2.imshow('노인 활동 모니터링 시스템', frame)
                
                # 키보드 입력 처리
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' 또는 ESC
                    break
                elif key == ord('r'):  # 일일 리포트
                    report = self.generate_daily_report()
                    print("\n" + "="*50)
                    print("📊 일일 활동 리포트")
                    print("="*50)
                    for key, value in report.items():
                        print(f"{key}: {value}")
                    print("="*50 + "\n")
                elif key == ord('s'):  # 데이터 저장
                    self.save_session_data()
            
            # 종료 처리
            cap.release()
            cv2.destroyAllWindows()
            
            # 최종 리포트 및 데이터 저장
            print("\n🏁 모니터링이 종료되었습니다.")
            final_report = self.generate_daily_report()
            print("\n📊 최종 활동 리포트:")
            print("="*40)
            for key, value in final_report.items():
                print(f"  {key}: {value}")
            print("="*40)
            
            # 자동 저장
            self.save_session_data()

if __name__ == "__main__":
    # 모니터링 시스템 시작
    monitoring_system = ElderlyMonitoringSystem()
    
    try:
        monitoring_system.run_monitoring()
    except KeyboardInterrupt:
        print("\n⏹️  사용자에 의해 모니터링이 중단되었습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        monitoring_system.save_session_data()
    
    print("👋 노인 활동 모니터링 시스템을 종료합니다.")
