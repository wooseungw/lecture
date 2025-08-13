#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2 # OpenCV 라이브러리를 가져옵니다. 웹캠, 이미지/비디오 처리에 사용됩니다.
import mediapipe as mp # MediaPipe 라이브러리를 가져옵니다. 손 추적과 같은 머신러닝 솔루션을 제공합니다.

# MediaPipe에서 제공하는 그리기 유틸리티와 손 추적 솔루션을 변수에 할당합니다.
mp_drawing = mp.solutions.drawing_utils # 랜드마크(관절점)와 연결선(뼈대)을 그리는 데 사용됩니다.
mp_hands = mp.solutions.hands # 손 추적 모델을 사용하기 위한 모듈입니다.

# 웹캠에서 비디오 캡처를 시작합니다. '0'은 시스템의 기본 웹캠을 의미합니다.
cap = cv2.VideoCapture(0)

# MediaPipe의 Hands 모델을 설정하고 로드합니다.
# 'with' 구문을 사용하면 모델 리소스를 안전하게 관리할 수 있습니다.
with mp_hands.Hands(
    max_num_hands=4,               # 감지할 최대 손의 개수를 4개로 설정합니다.
    min_detection_confidence=0.5,  # 손 감지에 대한 최소 신뢰도 임계값을 0.5로 설정합니다.
    min_tracking_confidence=0.5) as hands: # 손 추적에 대한 최소 신뢰도 임계값을 0.5로 설정합니다.

    # 웹캠이 열려 있는 동안 계속 반복합니다.
    while cap.isOpened():
        # 웹캠에서 한 프레임(이미지)을 읽어옵니다. 'ret'은 성공 여부, 'frame'은 실제 이미지 데이터입니다.
        ret, frame = cap.read()
        if not ret: # 프레임을 제대로 읽어오지 못했다면 루프를 중단합니다.
            break

        # 성능 향상을 위해 이미지를 MediaPipe가 처리하기 전에 읽기 전용으로 만듭니다.
        # 또한, OpenCV의 BGR 색상 순서를 MediaPipe가 사용하는 RGB 색상 순서로 변환합니다.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # 변환된 이미지에서 손을 감지하고 랜드마크를 찾습니다.
        results = hands.process(image)

        # 화면에 결과를 그리기 위해 이미지를 다시 쓰기 가능 상태로 만들고, 색상 순서도 원래의 BGR로 되돌립니다.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 감지된 손이 있는지 확인합니다.
        if results.multi_hand_landmarks:
            # 여러 개의 손이 감지될 수 있으므로, 각 손에 대해 반복합니다.
            for hand_landmarks in results.multi_hand_landmarks:
                # 'mp_drawing.draw_landmarks' 함수를 사용하여 이미지에 손의 랜드마크와 연결선을 그립니다.
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # 'MediaPipe Hands'라는 이름의 창에 결과 이미지를 보여줍니다.
        cv2.imshow('MediaPipe Hands', image)
        # 1밀리초 동안 키 입력을 기다리고, 만약 'ESC' 키(ASCII 코드 27)가 눌리면 루프를 종료합니다.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# 사용이 끝난 웹캠 리소스를 해제합니다.
cap.release()
# 모든 OpenCV 창을 닫습니다.
cv2.destroyAllWindows()