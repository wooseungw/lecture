#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 행동 패턴 분석기 - 일정 시간동안의 활동을 분석하고 기록
import cv2 # OpenCV 라이브러리, 비디오 및 이미지 처리에 사용됩니다.
import mediapipe as mp # MediaPipe 라이브러리, 자세 추정(pose estimation)에 사용됩니다.
import numpy as np # NumPy 라이브러리, 수치 계산 및 배열 처리에 사용됩니다.
import time # 시간 관련 기능을 사용하기 위한 라이브러리입니다.
from collections import deque # 양방향 큐(deque)를 사용하기 위해 가져옵니다. 고정된 크기의 데이터를 저장하는 데 유용합니다.
import json # JSON 형식의 데이터를 처리하기 위해 사용됩니다.
import os # 운영 체제와 상호 작용하기 위한 라이브러리입니다. (파일 존재 여부 확인 등)

# MediaPipe 초기화
mp_pose = mp.solutions.pose # MediaPipe의 자세 추정 솔루션을 가져옵니다.
mp_drawing = mp.solutions.drawing_utils # MediaPipe의 그리기 관련 유틸리티를 가져옵니다.

class ActivityTracker: # 활동 추적을 위한 클래스를 정의합니다.
    def __init__(self):
        # 최근 10초간의 움직임 데이터를 저장할 deque를 생성합니다. (30fps 기준 300개 데이터)
        self.movement_history = deque(maxlen=300)
        self.activity_log = [] # 활동 로그를 저장할 리스트입니다.
        self.session_start = time.time() # 분석 세션 시작 시간을 기록합니다.
        self.last_position = None # 이전 프레임의 신체 중심 위치를 저장할 변수입니다.
        self.sitting_time = 0 # 앉아있는 시간을 누적할 변수입니다.
        self.standing_time = 0 # 서있는 시간을 누적할 변수입니다.
        self.moving_time = 0 # 움직이는 시간을 누적할 변수입니다.
        self.current_activity = "Unknown" # 현재 활동 상태를 저장할 변수입니다.
        
    def calculate_movement(self, landmarks):
        """움직임 정도 계산"""
        # 주요 신체 부위(코, 양쪽 어깨, 양쪽 엉덩이)의 랜드마크를 가져옵니다.
        key_points = [
            landmarks[mp_pose.PoseLandmark.NOSE.value],
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        ]
        
        # 주요 부위의 x, y 좌표의 평균을 계산하여 신체의 중심점을 구합니다.
        center_x = np.mean([p.x for p in key_points])
        center_y = np.mean([p.y for p in key_points])
        
        current_position = (center_x, center_y) # 현재 신체 중심 위치입니다.
        
        movement = 0 # 움직임 정도를 저장할 변수를 0으로 초기화합니다.
        if self.last_position: # 이전 위치가 기록되어 있다면
            # 이전 위치와 현재 위치 사이의 유클리드 거리를 계산하여 움직임 정도를 구합니다.
            movement = np.sqrt(
                (current_position[0] - self.last_position[0])**2 + 
                (current_position[1] - self.last_position[1])**2
            )
        
        self.last_position = current_position # 현재 위치를 다음 계산을 위해 저장합니다.
        self.movement_history.append(movement) # 계산된 움직임 정도를 히스토리에 추가합니다.
        
        return movement # 계산된 움직임 정도를 반환합니다.
    
    def classify_activity(self, landmarks):
        """현재 활동 분류"""
        # 양쪽 어깨 y좌표의 평균과 양쪽 엉덩이 y좌표의 평균을 계산합니다.
        shoulder_y = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y + 
                     landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2
        hip_y = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y + 
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y) / 2
        
        # 어깨와 엉덩이 사이의 수직 거리 비율을 계산합니다.
        torso_ratio = abs(shoulder_y - hip_y)
        
        # 최근 움직임의 평균을 계산합니다.
        if len(self.movement_history) > 10:
            # 최근 30개 프레임(약 1초)의 움직임 평균을 구합니다.
            recent_movement = np.mean(list(self.movement_history)[-30:])
        else:
            recent_movement = 0
        
        # 활동 분류
        if recent_movement > 0.02:  # 평균 움직임이 특정 임계값보다 크면
            activity = "활발한 움직임"
            self.moving_time += 1/30  # 움직인 시간에 프레임당 시간(1/30초)을 더합니다.
        elif torso_ratio < 0.25:  # 상체 비율이 작으면 (어깨와 엉덩이가 가까우면)
            activity = "앉아있음"
            self.sitting_time += 1/30 # 앉은 시간에 프레임당 시간을 더합니다.
        else:  # 그 외의 경우
            activity = "서있음"
            self.standing_time += 1/30 # 서있는 시간에 프레임당 시간을 더합니다.
        
        self.current_activity = activity # 현재 활동 상태를 업데이트합니다.
        return activity # 분류된 활동을 반환합니다.
    
    def get_activity_summary(self):
        """활동 요약 반환"""
        total_time = time.time() - self.session_start # 총 경과 시간을 계산합니다.
        
        # 요약 정보를 딕셔너리 형태로 만듭니다.
        summary = {
            "총 시간": f"{total_time:.1f}초",
            "앉아있는 시간": f"{self.sitting_time:.1f}초 ({self.sitting_time/total_time*100:.1f}%)",
            "서있는 시간": f"{self.standing_time:.1f}초 ({self.standing_time/total_time*100:.1f}%)",
            "움직인 시간": f"{self.moving_time:.1f}초 ({self.moving_time/total_time*100:.1f}%)",
            "현재 활동": self.current_activity
        }
        
        return summary # 요약 딕셔너리를 반환합니다.
    
    def save_session_log(self):
        """세션 기록 저장"""
        # 현재 세션의 데이터를 딕셔너리로 정리합니다.
        session_data = {
            "session_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": time.time() - self.session_start,
            "sitting_time": self.sitting_time,
            "standing_time": self.standing_time,
            "moving_time": self.moving_time
        }
        
        # JSON 파일로 저장
        log_file = "activity_log.json" # 로그 파일 이름을 지정합니다.
        if os.path.exists(log_file): # 로그 파일이 이미 존재하면
            with open(log_file, 'r', encoding='utf-8') as f: # 파일을 읽기 모드로 엽니다.
                logs = json.load(f) # 기존 로그 데이터를 불러옵니다.
        else: # 파일이 없으면
            logs = [] # 빈 리스트로 시작합니다.
        
        logs.append(session_data) # 현재 세션 데이터를 로그 리스트에 추가합니다.
        
        with open(log_file, 'w', encoding='utf-8') as f: # 파일을 쓰기 모드로 엽니다.
            # 로그 리스트를 JSON 파일에 저장합니다. (한글 깨짐 방지, 가독성 좋게)
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        print(f"활동 기록이 {log_file}에 저장되었습니다.") # 저장 완료 메시지를 출력합니다.

# 웹캠 시작
cap = cv2.VideoCapture(0) # 0번 카메라(기본 웹캠)를 엽니다.
tracker = ActivityTracker() # ActivityTracker 클래스의 인스턴스를 생성합니다.

# MediaPipe Pose 모델을 로드합니다. with 구문을 사용하여 리소스를 안전하게 관리합니다.
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened(): # 웹캠이 열려 있는 동안 계속 반복합니다.
        ret, frame = cap.read() # 웹캠에서 한 프레임을 읽어옵니다.
        if not ret: # 프레임을 제대로 읽어오지 못했다면 루프를 종료합니다.
            break

        # 이미지 처리
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 이미지를 BGR에서 RGB로 변환합니다.
        image.flags.writeable = False # 성능 향상을 위해 이미지에 쓰기 작업을 비활성화합니다.
        
        # 포즈 감지
        results = pose.process(image) # MediaPipe 모델로 자세를 감지합니다.
        
        # 이미지 다시 변환
        image.flags.writeable = True # 화면에 그리기 위해 쓰기 작업을 다시 활성화합니다.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # 이미지를 다시 RGB에서 BGR로 변환합니다.
        
        # 활동 분석
        try: # 자세 랜드마크가 감지되지 않았을 경우를 대비해 예외 처리를 합니다.
            landmarks = results.pose_landmarks.landmark # 감지된 자세 랜드마크를 가져옵니다.
            
            # 움직임 계산 및 활동 분류
            movement = tracker.calculate_movement(landmarks) # 움직임 정도를 계산합니다.
            activity = tracker.classify_activity(landmarks) # 현재 활동을 분류합니다.
            
            # 활동 요약 가져오기
            summary = tracker.get_activity_summary() # 활동 요약 정보를 가져옵니다.
            
            # 결과 화면에 표시
            y_offset = 30 # 텍스트를 표시할 y축 시작 위치입니다.
            cv2.putText(image, f"현재 활동: {activity}", 
                       (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2) # 현재 활동을 화면에 표시합니다.
            
            y_offset += 25 # y 위치를 아래로 이동합니다.
            cv2.putText(image, f"움직임 정도: {movement:.4f}", 
                       (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) # 움직임 정도를 화면에 표시합니다.
            
            # 시간 통계 표시
            y_offset += 30 # y 위치를 아래로 이동합니다.
            for key, value in summary.items(): # 요약 정보 딕셔너리를 반복합니다.
                if key != "현재 활동": # "현재 활동"은 이미 표시했으므로 제외합니다.
                    cv2.putText(image, f"{key}: {value}", 
                               (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1) # 각 통계 정보를 화면에 표시합니다.
                    y_offset += 20 # 다음 정보를 위해 y 위치를 이동합니다.
            
            # 움직임 히스토리 그래프 (간단한 선 그래프)
            if len(tracker.movement_history) > 1: # 움직임 히스토리가 1개 이상 있으면
                points = [] # 그래프를 그릴 점들을 저장할 리스트입니다.
                # 최근 100개의 움직임 데이터로 그래프를 그립니다.
                for i, movement_val in enumerate(list(tracker.movement_history)[-100:]):
                    x = 500 + i * 2 # x 좌표를 계산합니다.
                    y = 400 - int(movement_val * 10000)  # 움직임 값을 y 좌표로 변환하고 스케일링합니다.
                    y = max(300, min(400, y))  # y 좌표가 특정 범위를 벗어나지 않도록 제한합니다.
                    points.append((x, y)) # 계산된 점을 리스트에 추가합니다.
                
                # 점들을 선으로 연결하여 그래프를 그립니다.
                for i in range(1, len(points)):
                    cv2.line(image, points[i-1], points[i], (0, 255, 0), 1)
            
        except: # 랜드마크 감지에 실패했을 경우
            cv2.putText(image, "포즈를 인식할 수 없습니다", 
                       (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) # 에러 메시지를 화면에 표시합니다.
        
        # 포즈 랜드마크 그리기
        if results.pose_landmarks: # 감지된 자세 랜드마크가 있다면
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # 이미지 위에 랜드마크와 연결선을 그립니다.
        
        # 조작 안내
        cv2.putText(image, "Press 'q' to quit, 's' to save log", 
                   (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) # 종료 및 저장 키 안내를 표시합니다.
        
        cv2.imshow('Activity Pattern Analyzer', image) # 결과 이미지를 창에 보여줍니다.
        
        key = cv2.waitKey(10) & 0xFF # 10ms 동안 키 입력을 기다립니다.
        if key == ord('q'): # 'q' 키가 눌리면
            break # 루프를 종료합니다.
        elif key == ord('s'): # 's' 키가 눌리면
            tracker.save_session_log() # 현재까지의 로그를 저장합니다.

cap.release() # 사용이 끝난 웹캠 리소스를 해제합니다.
cv2.destroyAllWindows() # 모든 OpenCV 창을 닫습니다.

# 최종 세션 저장
tracker.save_session_log() # 프로그램 종료 시 최종 로그를 저장합니다.
print("세션이 종료되었습니다.") # 종료 메시지를 출력합니다.
print("최종 활동 요약:") # 최종 요약 정보를 출력합니다.
final_summary = tracker.get_activity_summary() # 최종 활동 요약을 가져옵니다.
for key, value in final_summary.items(): # 요약 정보를 하나씩 출력합니다.
    print(f"  {key}: {value}")