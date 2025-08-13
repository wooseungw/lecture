#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mediapipe as mp # MediaPipe 라이브러리를 가져옵니다. 얼굴 랜드마크 감지에 사용됩니다.
import cv2 # OpenCV 라이브러리를 가져옵니다. 웹캠 및 이미지 처리에 사용됩니다.

# 감지할 최대 얼굴 수를 설정합니다.
num_faces = 2

# MediaPipe의 얼굴 메시(Face Mesh) 솔루션을 변수에 할당합니다.
mp_face_mesh = mp.solutions.face_mesh

# 얼굴 랜드마크 인식기를 초기화합니다.
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,      # 비디오 스트림(False) 모드로 설정합니다. True로 하면 단일 이미지에 최적화됩니다.
    max_num_faces=num_faces,      # 위에서 설정한 최대 얼굴 수로 제한합니다.
    refine_landmarks=True         # 눈, 입술 주변의 랜드마크를 더 정교하게 감지하도록 설정합니다.
)

# 웹캠을 엽니다. '0'은 시스템의 기본 웹캠을 의미합니다.
cap = cv2.VideoCapture(0)

# 웹캠이 성공적으로 열렸는지 확인하고, 열려 있는 동안 계속 반복합니다.
while cap.isOpened():
    # 웹캠에서 한 프레임을 읽어옵니다. 'ret'은 성공 여부, 'frame'은 실제 이미지입니다.
    ret, frame = cap.read()
    if not ret: # 프레임을 제대로 읽어오지 못했다면 루프를 중단합니다.
        break

    # MediaPipe 처리를 위해 이미지의 색상 체계를 OpenCV의 BGR에서 RGB로 변환합니다.
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 변환된 RGB 이미지에서 얼굴 랜드마크를 감지합니다.
    results = face_mesh.process(image_rgb)

    # 감지된 얼굴 랜드마크가 있는지 확인합니다.
    if results.multi_face_landmarks:
        # 여러 개의 얼굴이 감지될 수 있으므로, 각 얼굴에 대해 반복합니다.
        for face_landmarks in results.multi_face_landmarks:
            # 각 얼굴에 있는 모든 랜드마크(점)에 대해 반복합니다.
            for landmark in face_landmarks.landmark:
                # 이미지의 높이(h)와 너비(w)를 가져옵니다.
                h, w, _ = frame.shape
                # 랜드마크의 좌표는 0과 1 사이의 값으로 정규화되어 있으므로, 실제 픽셀 좌표로 변환합니다.
                x, y = int(landmark.x * w), int(landmark.y * h)
                # 계산된 (x, y) 좌표에 작은 녹색 원을 그립니다.
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

    # 랜드마크가 그려진 프레임을 'Face Landmarks'라는 이름의 창에 보여줍니다.
    cv2.imshow('Face Landmarks', frame)
    # 1밀리초 동안 키 입력을 기다리고, 만약 'ESC' 키(ASCII 코드 27)가 눌리면 루프를 종료합니다.
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 사용이 끝난 웹캠 리소스를 해제합니다.
cap.release()
# 모든 OpenCV 창을 닫습니다.
cv2.destroyAllWindows()
# 사용이 끝난 얼굴 랜드마크 인식기 리소스를 해제합니다.
face_mesh.close()