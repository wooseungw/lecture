#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2 # OpenCV 라이브러리를 가져옵니다. 웹캠, 이미지/비디오 처리에 사용됩니다.
import mediapipe as mp # MediaPipe 라이브러리를 가져옵니다. 자세 추적(pose estimation) 솔루션을 제공합니다.

# MediaPipe의 자세 추정 솔루션과 그리기 유틸리티를 변수에 할당합니다.
mp_pose = mp.solutions.pose # 자세 추적 모델을 사용하기 위한 모듈입니다.
mp_drawing = mp.solutions.drawing_utils # 랜드마크(관절점)와 연결선(뼈대)을 그리는 데 사용됩니다.

def detect_action(landmarks): # 랜드마크를 기반으로 행동을 감지하는 함수를 정의합니다.
    # 왼쪽 어깨, 왼쪽 손목, 왼쪽 엉덩이, 왼쪽 무릎 랜드마크의 좌표를 가져옵니다.
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]

    # 손 들기: 왼쪽 손목의 y좌표가 왼쪽 어깨의 y좌표보다 작으면 (즉, 손목이 어깨보다 위에 있으면) 손을 든 것으로 판단합니다.
    if left_wrist.y < left_shoulder.y:
        return "Hand Raised"
    # 앉기: 왼쪽 엉덩이와 왼쪽 무릎의 y좌표 차이가 작으면 (즉, 엉덩이가 무릎 높이까지 내려가면) 앉은 것으로 판단합니다.
    elif abs(left_hip.y - left_knee.y) < 0.1:
        return "Sitting"
    else: # 위의 조건에 해당하지 않으면 서있는 것으로 판단합니다.
        return "Standing"

# 웹캠에서 비디오 캡처를 시작합니다. '0'은 시스템의 기본 웹캠을 의미합니다.
cap = cv2.VideoCapture(0)

# MediaPipe의 Pose 모델을 설정하고 로드합니다.
# 'with' 구문을 사용하면 모델 리소스를 안전하게 관리할 수 있습니다.
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # 웹캠이 열려 있는 동안 계속 반복합니다.
    while cap.isOpened():
        # 웹캠에서 한 프레임(이미지)을 읽어옵니다. 'ret'은 성공 여부, 'frame'은 실제 이미지 데이터입니다.
        ret, frame = cap.read()
        if not ret: # 프레임을 제대로 읽어오지 못했다면 루프를 중단합니다.
            break

        # 이미지를 BGR에서 RGB로 변환합니다. MediaPipe는 RGB 형식의 이미지를 입력으로 받습니다.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 성능 향상을 위해 이미지를 MediaPipe가 처리하기 전에 읽기 전용으로 만듭니다.
        image.flags.writeable = False
        # 변환된 이미지에서 자세를 감지하고 랜드마크를 찾습니다.
        results = pose.process(image)

        # 화면에 결과를 그리기 위해 이미지를 다시 쓰기 가능 상태로 만들고, 색상 순서도 원래의 BGR로 되돌립니다.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        action = "" # 현재 감지된 행동을 저장할 변수를 초기화합니다.
        if results.pose_landmarks: # 자세 랜드마크가 감지되었다면
            # 'mp_drawing.draw_landmarks' 함수를 사용하여 이미지에 자세의 랜드마크와 연결선을 그립니다.
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            # 감지된 랜드마크를 사용하여 행동을 감지합니다.
            action = detect_action(results.pose_landmarks.landmark)
            # 감지된 행동을 이미지 위에 텍스트로 표시합니다.
            cv2.putText(image, f'Action: {action}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 'MediaPipe Pose Action Recognition'이라는 이름의 창에 결과 이미지를 보여줍니다.
        cv2.imshow('MediaPipe Pose Action Recognition', image)
        # 1밀리초 동안 키 입력을 기다리고, 만약 'ESC' 키(ASCII 코드 27)가 눌리면 루프를 종료합니다.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# 사용이 끝난 웹캠 리소스를 해제합니다.
cap.release()
# 모든 OpenCV 창을 닫습니다.
cv2.destroyAllWindows()