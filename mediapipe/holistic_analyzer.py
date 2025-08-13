#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 종합 인간 행동 분석 시스템 - 얼굴, 손, 자세를 동시에 분석
import cv2 # OpenCV 라이브러리, 비디오 및 이미지 처리에 사용됩니다.
import mediapipe as mp # MediaPipe 라이브러리, 전체적인(holistic) 추적에 사용됩니다.
import numpy as np # NumPy 라이브러리, 수치 계산에 사용됩니다.
import time # 시간 관련 기능을 사용하기 위한 라이브러리입니다.

# MediaPipe 초기화
mp_holistic = mp.solutions.holistic # MediaPipe의 Holistic 솔루션을 가져옵니다.
mp_drawing = mp.solutions.drawing_utils # MediaPipe의 그리기 관련 유틸리티를 가져옵니다.
mp_drawing_styles = mp.solutions.drawing_styles # MediaPipe의 그리기 스타일을 가져옵니다.

class HolisticAnalyzer: # 전체적인 분석을 위한 클래스를 정의합니다.
    def __init__(self):
        self.start_time = time.time() # 분석 시작 시간을 기록합니다.
        self.analysis_history = [] # 분석 기록을 저장할 리스트입니다.
        
    def analyze_face_expression(self, face_landmarks):
        """얼굴 표정 분석"""
        if not face_landmarks: # 얼굴 랜드마크가 감지되지 않았으면
            return "얼굴 인식 안됨", 0.0
            
        # 입꼬리 위치 분석 (미소/찡그림)
        left_mouth = face_landmarks.landmark[61] # 왼쪽 입꼬리
        right_mouth = face_landmarks.landmark[291] # 오른쪽 입꼬리
        mouth_center = face_landmarks.landmark[13] # 입 중앙 아래
        
        # 양쪽 입꼬리의 y좌표 평균과 입 중앙의 y좌표를 비교하여 입의 곡률을 계산합니다.
        mouth_curve = ((left_mouth.y + right_mouth.y) / 2) - mouth_center.y
        
        # 눈 크기 분석 (놀람/졸림)
        left_eye_top = face_landmarks.landmark[159] # 왼쪽 눈 위쪽
        left_eye_bottom = face_landmarks.landmark[145] # 왼쪽 눈 아래쪽
        eye_openness = abs(left_eye_top.y - left_eye_bottom.y) # 눈을 뜬 정도를 계산합니다.
        
        # 표정 판별
        if mouth_curve < -0.008: # 입꼬리가 많이 올라갔으면 (미소)
            return "Smile", abs(mouth_curve) * 100
        elif mouth_curve > 0.008: # 입꼬리가 많이 내려갔으면 (찡그림)
            return "Twist", mouth_curve * 100
        elif eye_openness > 0.02: # 눈이 크게 떠졌으면 (놀람)
            return "Surprise", eye_openness * 50
        else: # 그 외의 경우
            return "Normal", 0.5

    def analyze_hand_state(self, left_hand, right_hand):
        """양손 상태 분석"""
        hand_states = [] # 양손의 상태를 저장할 리스트입니다.
        
        # 왼쪽 손과 오른쪽 손에 대해 각각 분석을 수행합니다.
        for hand_landmarks, hand_name in [(left_hand, "왼손"), (right_hand, "오른손")]:
            if hand_landmarks: # 손 랜드마크가 감지되었으면
                # 펴진 손가락의 개수를 셉니다.
                fingers = self.count_fingers(hand_landmarks)
                
                # 제스처 분석
                if fingers == 0:
                    gesture = "주먹 ✊"
                elif fingers == 5:
                    gesture = "열린 손 🖐️"
                elif fingers == 2:
                    # 검지와 중지가 펴져있는지 확인하여 '평화' 제스처를 구분합니다.
                    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
                    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
                    if index_up and middle_up:
                        gesture = "평화 ✌️"
                    else:
                        gesture = f"{fingers}개 손가락"
                elif fingers == 1:
                    gesture = "가리키기 👆"
                else:
                    gesture = f"{fingers}개 손가락"
                
                hand_states.append(f"{hand_name}: {gesture}")
            else: # 손이 감지되지 않았으면
                hand_states.append(f"{hand_name}: 인식 안됨")
        
        return hand_states # 분석된 양손의 상태를 반환합니다.
    
    def count_fingers(self, hand_landmarks):
        """손가락 개수 세기"""
        finger_tips = [4, 8, 12, 16, 20]  # 엄지, 검지, 중지, 약지, 소지 끝점 인덱스
        finger_pips = [3, 6, 10, 14, 18]  # 각 손가락의 중간 관절(PIP) 인덱스
        
        fingers = 0 # 펴진 손가락 수를 저장할 변수
        
        # 엄지는 x 좌표를 기준으로 펴짐/접힘을 판단합니다.
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            fingers += 1
            
        # 나머지 손가락들은 y 좌표를 기준으로 판단합니다. (손가락 끝이 중간 관절보다 위에 있으면 펴진 것)
        for tip, pip in zip(finger_tips[1:], finger_pips[1:]):
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                fingers += 1
                
        return fingers # 펴진 손가락 수를 반환합니다.
    
    def analyze_body_posture(self, pose_landmarks):
        """신체 자세 분석"""
        if not pose_landmarks: # 자세 랜드마크가 감지되지 않았으면
            return "자세 인식 안됨", []
            
        landmarks = pose_landmarks.landmark
        
        # 어깨 수평 확인
        left_shoulder = landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value]
        shoulder_tilt = abs(left_shoulder.y - right_shoulder.y) # 양 어깨의 y좌표 차이로 기울기를 계산합니다.
        
        # 머리 위치 확인
        nose = landmarks[mp_holistic.PoseLandmark.NOSE.value]
        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2 # 양 어깨의 중심 x좌표
        head_lean = abs(nose.x - shoulder_center_x) # 코와 어깨 중심의 x좌표 차이로 머리 기울기를 계산합니다.
        
        # 앉음/서있음 판별
        hip_y = (landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].y + 
                landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].y) / 2 # 양 엉덩이의 y좌표 평균
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2 # 양 어깨의 y좌표 평균
        
        if abs(hip_y - shoulder_y) < 0.25: # 어깨와 엉덩이의 y좌표 차이가 작으면 앉은 자세로 판단
            posture_type = "앉은 자세"
        else:
            posture_type = "선 자세"
        
        # 자세 평가
        posture_issues = [] # 자세 문제점을 저장할 리스트
        if shoulder_tilt > 0.05: # 어깨 기울기가 특정 임계값보다 크면
            posture_issues.append("어깨 기울어짐")
        if head_lean > 0.08: # 머리 기울기가 특정 임계값보다 크면
            posture_issues.append("머리 기울어짐")
            
        return posture_type, posture_issues # 자세 유형과 문제점을 반환합니다.
    
    def get_overall_assessment(self, face_emotion, hand_states, posture_type, posture_issues):
        """종합 평가"""
        assessment = [] # 종합 평가 내용을 저장할 리스트
        
        # 감정 상태 평가
        if "미소" in face_emotion:
            assessment.append("😊 긍정적인 감정 상태")
        elif "찡그림" in face_emotion:
            assessment.append("😞 스트레스 상태일 수 있음")
        else:
            assessment.append("😐 평온한 감정 상태")
            
        # 자세 상태 평가
        if len(posture_issues) == 0: # 문제점이 없으면
            assessment.append("✅ 좋은 자세 유지 중")
        else: # 문제점이 있으면
            assessment.append(f"⚠️ 자세 주의: {', '.join(posture_issues)}")
            
        # 손 활동성 평가
        active_hands = sum(1 for state in hand_states if "인식 안됨" not in state) # 인식된 손의 개수를 셉니다.
        if active_hands == 2:
            assessment.append("🤲 양손 활동 활발")
        elif active_hands == 1:
            assessment.append("👋 한손 활동 중")
        else:
            assessment.append("🤐 손 활동 없음")
            
        return assessment # 종합 평가 리스트를 반환합니다.

# 웹캠 시작
cap = cv2.VideoCapture(0) # 0번 카메라(기본 웹캠)를 엽니다.
analyzer = HolisticAnalyzer() # HolisticAnalyzer 클래스의 인스턴스를 생성합니다.

# MediaPipe Holistic 모델을 로드합니다.
with mp_holistic.Holistic(
    min_detection_confidence=0.5, # 최소 감지 신뢰도
    min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened(): # 웹캠이 열려 있는 동안 계속 반복합니다.
        ret, frame = cap.read() # 웹캠에서 한 프레임을 읽어옵니다.
        if not ret: # 프레임을 제대로 읽어오지 못했다면 루프를 종료합니다.
            break

        # 이미지 처리
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 이미지를 BGR에서 RGB로 변환합니다.
        image.flags.writeable = False # 성능 향상을 위해 이미지에 쓰기 작업을 비활성화합니다.
        
        # 전체 분석
        results = holistic.process(image) # Holistic 모델로 이미지를 처리하여 얼굴, 손, 자세 랜드마크를 얻습니다.
        
        # 이미지 다시 변환
        image.flags.writeable = True # 화면에 그리기 위해 쓰기 작업을 다시 활성화합니다.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # 이미지를 다시 RGB에서 BGR로 변환합니다.
        
        # 각 영역별 분석
        face_emotion, emotion_score = analyzer.analyze_face_expression(results.face_landmarks)
        hand_states = analyzer.analyze_hand_state(results.left_hand_landmarks, results.right_hand_landmarks)
        posture_type, posture_issues = analyzer.analyze_body_posture(results.pose_landmarks)
        
        # 종합 평가
        overall_assessment = analyzer.get_overall_assessment(
            face_emotion, hand_states, posture_type, posture_issues)
        
        # 결과 표시
        # 정보 표시를 위한 반투명 배경 영역을 생성합니다.
        overlay = image.copy()
        cv2.rectangle(overlay, (10, 10), (400, 200), (0, 0, 0), -1)
        image = cv2.addWeighted(overlay, 0.7, image, 0.3, 0)
        
        y_pos = 30 # 텍스트를 표시할 y 시작 위치
        cv2.putText(image, f"얼굴: {face_emotion}", (20, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2) # 얼굴 분석 결과 표시
        
        y_pos += 25
        for hand_state in hand_states: # 손 분석 결과 표시
            cv2.putText(image, hand_state, (20, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            y_pos += 20
            
        y_pos += 5
        cv2.putText(image, f"자세: {posture_type}", (20, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1) # 자세 유형 표시
        
        if posture_issues: # 자세 문제점이 있으면
            y_pos += 20
            cv2.putText(image, f"주의: {', '.join(posture_issues)}", (20, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 100, 255), 1) # 문제점 내용 표시
        
        # 종합 평가 표시
        y_pos = 250
        cv2.putText(image, "=== 종합 평가 ===", (20, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        for assessment in overall_assessment:
            y_pos += 25
            cv2.putText(image, assessment, (20, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) # 종합 평가 내용 표시
        
        # 랜드마크 그리기
        # 얼굴 랜드마크(윤곽선)를 그립니다.
        if results.face_landmarks:
            mp_drawing.draw_landmarks(
                image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                None, mp_drawing_styles.get_default_face_mesh_contours_style())
        
        # 왼쪽 손 랜드마크를 그립니다.
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        
        # 오른쪽 손 랜드마크를 그립니다.
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        
        # 자세 랜드마크를 그립니다.
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                mp_drawing_styles.get_default_pose_landmarks_style())
        
        cv2.imshow('Holistic Human Behavior Analysis', image) # 최종 이미지를 창에 보여줍니다.
        
        if cv2.waitKey(10) & 0xFF == ord('q'): # 'q' 키가 눌리면 루프를 종료합니다.
            break

cap.release() # 사용이 끝난 웹캠 리소스를 해제합니다.
cv2.destroyAllWindows() # 모든 OpenCV 창을 닫습니다.