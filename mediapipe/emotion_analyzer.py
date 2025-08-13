#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 감정 분석기 - 얼굴 표정과 제스처를 조합한 감정 인식
import cv2 # OpenCV 라이브러리, 비디오 및 이미지 처리에 사용됩니다.
import mediapipe as mp # MediaPipe 라이브러리, 얼굴 메시 및 손 추적에 사용됩니다.
import numpy as np # NumPy 라이브러리, 수치 계산에 사용됩니다.

# MediaPipe 초기화
mp_face_mesh = mp.solutions.face_mesh # MediaPipe의 얼굴 메시 솔루션을 가져옵니다.
mp_hands = mp.solutions.hands # MediaPipe의 손 추적 솔루션을 가져옵니다.
mp_drawing = mp.solutions.drawing_utils # MediaPipe의 그리기 관련 유틸리티를 가져옵니다.

def analyze_face_emotion(landmarks):
    """얼굴 랜드마크로 감정 분석"""
    # 입꼬리 위치로 미소 감지
    mouth_left = landmarks[61]  # 입 왼쪽 끝 랜드마크
    mouth_right = landmarks[291] # 입 오른쪽 끝 랜드마크
    mouth_center = landmarks[13] # 입 중앙 아래 랜드마크
    
    # 입꼬리가 입 중앙보다 얼마나 위/아래에 있는지 계산하여 미소 정도를 파악합니다.
    mouth_curve = (mouth_left.y + mouth_right.y) / 2 - mouth_center.y
    
    # 눈썹 위치로 놀람/화남 감지
    left_eyebrow = landmarks[70]  # 왼쪽 눈썹 랜드마크
    right_eyebrow = landmarks[300] # 오른쪽 눈썹 랜드마크
    nose_tip = landmarks[1]      # 코끝 랜드마크
    
    # 눈썹이 코끝보다 얼마나 위에 있는지 계산하여 눈썹의 움직임을 파악합니다.
    eyebrow_height = (left_eyebrow.y + right_eyebrow.y) / 2 - nose_tip.y
    
    # 감정 판별
    if mouth_curve < -0.01:  # 입꼬리가 기준보다 많이 올라가 있으면 (y좌표는 위로 갈수록 작아짐)
        return "행복 😊"
    elif mouth_curve > 0.01: # 입꼬리가 기준보다 많이 내려가 있으면
        return "슬픔 😢"
    elif eyebrow_height < -0.05: # 눈썹이 기준보다 많이 올라가 있으면
        return "놀람 😮"
    else: # 그 외의 경우
        return "평온 😐"

def analyze_hand_gesture(hand_landmarks):
    """손 제스처로 감정/의도 분석"""
    # 각 손가락 끝점의 랜드마크를 가져옵니다.
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    
    # 손목을 기준점으로 사용합니다.
    wrist = hand_landmarks.landmark[0]
    
    # 각 손가락이 펴져있는지 확인하여 리스트에 저장합니다. (1: 펴짐, 0: 접힘)
    fingers_up = []
    
    # 엄지는 x 좌표를 기준으로 펴짐/접힘을 판단합니다. (손의 방향에 따라 달라질 수 있음)
    if thumb_tip.x > hand_landmarks.landmark[3].x:
        fingers_up.append(1)
    else:
        fingers_up.append(0)
    
    # 나머지 4개 손가락은 y 좌표를 기준으로 판단합니다. (손가락 끝이 중간 관절보다 위에 있으면 펴진 것)
    finger_tips = [8, 12, 16, 20]  # 검지, 중지, 약지, 소지 끝점 인덱스
    finger_pips = [6, 10, 14, 18]  # 각 손가락의 중간 관절(PIP) 인덱스
    
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers_up.append(1)
        else:
            fingers_up.append(0)
    
    # 제스처 판별
    total_fingers = sum(fingers_up) # 펴진 손가락의 총 개수를 계산합니다.
    
    if total_fingers == 0:
        return "주먹 ✊"
    elif total_fingers == 5:
        return "안녕 👋"
    elif fingers_up == [0, 1, 1, 0, 0]: # 검지와 중지만 펴진 경우
        return "평화 ✌️"
    elif fingers_up == [1, 0, 0, 0, 0]: # 엄지만 펴진 경우
        return "좋아요 👍"
    elif total_fingers == 1 and fingers_up[1] == 1: # 검지만 펴진 경우
        return "가리키기 👆"
    else:
        return f"손가락 {total_fingers}개"

# 웹캠 시작
cap = cv2.VideoCapture(0) # 0번 카메라(기본 웹캠)를 엽니다.

# MediaPipe 얼굴 메시와 손 모델을 로드합니다.
with mp_face_mesh.FaceMesh(
    max_num_faces=1,          # 최대 1개의 얼굴만 감지
    refine_landmarks=True,    # 눈, 입술 주변 랜드마크 정교화
    min_detection_confidence=0.5, # 최소 감지 신뢰도
    min_tracking_confidence=0.5) as face_mesh, \
     mp_hands.Hands(
        min_detection_confidence=0.5, # 최소 감지 신뢰도
        min_tracking_confidence=0.5) as hands:

    while cap.isOpened(): # 웹캠이 열려 있는 동안 계속 반복합니다.
        ret, frame = cap.read() # 웹캠에서 한 프레임을 읽어옵니다.
        if not ret: # 프레임을 제대로 읽어오지 못했다면 루프를 종료합니다.
            break

        # 이미지 처리
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 이미지를 BGR에서 RGB로 변환합니다.
        image.flags.writeable = False # 성능 향상을 위해 이미지에 쓰기 작업을 비활성화합니다.
        
        # 얼굴과 손 감지
        face_results = face_mesh.process(image) # 얼굴 메시 모델로 이미지를 처리합니다.
        hand_results = hands.process(image) # 손 모델로 이미지를 처리합니다.
        
        # 이미지 다시 변환
        image.flags.writeable = True # 화면에 그리기 위해 쓰기 작업을 다시 활성화합니다.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # 이미지를 다시 RGB에서 BGR로 변환합니다.
        
        # 얼굴 감정 분석
        face_emotion = "얼굴 인식 안됨" # 기본 감정 상태
        if face_results.multi_face_landmarks: # 감지된 얼굴이 있으면
            for face_landmarks in face_results.multi_face_landmarks: # 각 얼굴에 대해 반복
                face_emotion = analyze_face_emotion(face_landmarks.landmark) # 감정 분석 함수를 호출합니다.
                
                # 주요 얼굴 포인트만 그리기 (시각화를 위해)
                for i in [1, 61, 291, 13, 70, 300]:  # 코끝, 입꼬리, 입 중앙, 눈썹 포인트
                    # 정규화된 좌표를 이미지 좌표로 변환합니다.
                    x = int(face_landmarks.landmark[i].x * frame.shape[1])
                    y = int(face_landmarks.landmark[i].y * frame.shape[0])
                    cv2.circle(image, (x, y), 3, (0, 255, 0), -1) # 해당 위치에 원을 그립니다.
        
        # 손 제스처 분석
        hand_gesture = "손 인식 안됨" # 기본 제스처 상태
        if hand_results.multi_hand_landmarks: # 감지된 손이 있으면
            for hand_landmarks in hand_results.multi_hand_landmarks: # 각 손에 대해 반복
                hand_gesture = analyze_hand_gesture(hand_landmarks) # 제스처 분석 함수를 호출합니다.
                mp_drawing.draw_landmarks( # 손 랜드마크와 연결선을 그립니다.
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # 결과 표시
        cv2.putText(image, f'Face: {face_emotion}', 
                   (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA) # 얼굴 감정 결과를 화면에 표시합니다.
        
        cv2.putText(image, f'Hand: {hand_gesture}', 
                   (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA) # 손 제스처 결과를 화면에 표시합니다.
        
        # 종합 상태
        if "행복" in face_emotion and "좋아요" in hand_gesture:
            overall_mood = "매우 긍정적! 🌟"
            color = (0, 255, 0) # 초록색
        elif "슬픔" in face_emotion:
            overall_mood = "위로가 필요해요 💙"
            color = (255, 0, 0) # 파란색
        elif "평화" in hand_gesture:
            overall_mood = "평화로운 상태 ☮️"
            color = (0, 255, 255) # 노란색
        else:
            overall_mood = "일반적인 상태"
            color = (255, 255, 255) # 흰색
        
        cv2.putText(image, overall_mood, 
                   (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA) # 종합적인 상태를 화면에 표시합니다.
        
        cv2.imshow('Emotion Analyzer', image) # 결과 이미지를 창에 보여줍니다.
        
        if cv2.waitKey(10) & 0xFF == ord('q'): # 'q' 키가 눌리면 루프를 종료합니다.
            break

cap.release() # 사용이 끝난 웹캠 리소스를 해제합니다.
cv2.destroyAllWindows() # 모든 OpenCV 창을 닫습니다.