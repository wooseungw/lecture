#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math # 수학 연산을 위한 라이브러리입니다.
import urllib.request # URL에서 데이터를 다운로드하기 위한 라이브러리입니다.
import cv2 # OpenCV 라이브러리, 이미지 처리 및 조작에 사용됩니다.
from matplotlib import pyplot as plt # Matplotlib 라이브러리, 그래프 및 이미지 시각화에 사용됩니다.
import mediapipe as mp # MediaPipe 라이브러리, 제스처 인식에 사용됩니다.
from mediapipe.framework.formats import landmark_pb2 # MediaPipe 랜드마크 프로토콜 버퍼를 가져옵니다.
from mediapipe.tasks import python # MediaPipe Tasks Python API를 가져옵니다.
from mediapipe.tasks.python import vision # MediaPipe Vision Tasks를 가져옵니다.

# 예제 이미지 파일들을 다운로드합니다.
IMAGE_FILENAMES = ['thumbs_down.jpg', 'victory.jpg', 'thumbs_up.jpg', 'pointing_up.jpg'] # 다운로드할 이미지 파일 이름 목록
for name in IMAGE_FILENAMES: # 각 이미지 파일 이름에 대해 반복
    url = f'https://storage.googleapis.com/mediapipe-tasks/gesture_recognizer/{name}' # 이미지 다운로드 URL 구성
    urllib.request.urlretrieve(url, name) # URL에서 파일을 다운로드하여 로컬에 저장

# Matplotlib 그래프 설정을 변경합니다. (축, 레이블 등을 숨겨 이미지 표시를 깔끔하게 함)
plt.rcParams.update({
    'axes.spines.top': False,       # 위쪽 축 선 숨기기
    'axes.spines.right': False,     # 오른쪽 축 선 숨기기
    'axes.spines.left': False,      # 왼쪽 축 선 숨기기
    'axes.spines.bottom': False,    # 아래쪽 축 선 숨기기
    'xtick.labelbottom': False,     # 아래쪽 x축 레이블 숨기기
    'xtick.bottom': False,          # 아래쪽 x축 틱 숨기기
    'ytick.labelleft': False,       # 왼쪽 y축 레이블 숨기기
    'ytick.left': False,            # 왼쪽 y축 틱 숨기기
    'xtick.labeltop': False,        # 위쪽 x축 레이블 숨기기
    'xtick.top': False,             # 위쪽 x축 틱 숨기기
    'ytick.labelright': False,      # 오른쪽 y축 레이블 숨기기
    'ytick.right': False            # 오른쪽 y축 틱 숨기기
})

# Mediapipe 그리기 유틸리티 및 스타일을 설정합니다.
mp_hands = mp.solutions.hands # MediaPipe Hands 솔루션
mp_drawing = mp.solutions.drawing_utils # 랜드마크 그리기 유틸리티
mp_drawing_styles = mp.solutions.drawing_styles # 그리기 스타일 유틸리티

def display_one_image(image, title, subplot, titlesize=16):
    # Matplotlib 서브플롯에 이미지를 표시합니다.
    plt.subplot(*subplot)
    plt.imshow(image)
    if title: # 제목이 있으면
        # 이미지 위에 제목을 표시합니다.
        plt.title(title, fontsize=int(titlesize), color='black', fontdict={'verticalalignment':'center'}, pad=int(titlesize/1.5))
    # 다음 서브플롯 위치를 반환합니다.
    return (subplot[0], subplot[1], subplot[2]+1)

def display_batch_of_images_with_gestures_and_hand_landmarks(images, results):
    # MediaPipe Image 객체를 NumPy 배열로 변환합니다.
    images = [image.numpy_view() for image in images]
    # 결과에서 제스처 정보만 추출합니다.
    gestures = [top_gesture for (top_gesture, _) in results]
    # 결과에서 손 랜드마크 정보만 추출합니다.
    multi_hand_landmarks_list = [multi_hand_landmarks for (_, multi_hand_landmarks) in results]

    # 이미지 배치를 위한 행과 열 수를 계산합니다.
    rows = int(math.sqrt(len(images)))
    cols = len(images) // rows
    FIGSIZE = 13.0 # 그림의 기본 크기
    SPACING = 0.1 # 서브플롯 간의 간격
    subplot = (rows, cols, 1) # 첫 번째 서브플롯 위치
    # 그림의 크기를 설정합니다.
    plt.figure(figsize=(FIGSIZE/rows*cols, FIGSIZE) if rows >= cols else (FIGSIZE, FIGSIZE/cols*rows))

    # 각 이미지와 제스처에 대해 반복합니다.
    for i, (image, gesture) in enumerate(zip(images[:rows*cols], gestures[:rows*cols])):
        title = f"{gesture.category_name} ({gesture.score:.2f})" # 제목 문자열 생성 (제스처 이름과 점수)
        dynamic_titlesize = FIGSIZE * SPACING / max(rows, cols) * 40 + 3 # 동적 제목 크기 계산
        annotated_image = image.copy() # 원본 이미지를 복사하여 주석을 추가할 이미지 생성

        # 각 손 랜드마크에 대해 반복합니다.
        for hand_landmarks in multi_hand_landmarks_list[i]:
            # 랜드마크 정보를 프로토콜 버퍼 형식으로 변환합니다.
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
            ])
            # 이미지에 손 랜드마크와 연결선을 그립니다.
            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
        # 주석이 추가된 이미지를 서브플롯에 표시합니다.
        subplot = display_one_image(annotated_image, title, subplot, titlesize=dynamic_titlesize)

    plt.tight_layout() # 서브플롯 간의 간격을 자동으로 조정합니다.
    plt.subplots_adjust(wspace=SPACING, hspace=SPACING) # 서브플롯 간의 수평/수직 간격을 설정합니다.
    plt.show() # 그림을 화면에 표시합니다.

# 이미지 리사이즈 및 미리보기 설정을 정의합니다.
DESIRED_HEIGHT = 480 # 원하는 이미지 높이
DESIRED_WIDTH = 480 # 원하는 이미지 너비

def resize_and_show(image):
    h, w = image.shape[:2] # 이미지의 높이와 너비를 가져옵니다.
    if h < w: # 높이가 너비보다 작으면
        # 너비를 기준으로 이미지를 리사이즈합니다.
        img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
    else: # 너비가 높이보다 작거나 같으면
        # 높이를 기준으로 이미지를 리사이즈합니다.
        img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
    cv2.imshow('Preview', img) # 'Preview' 창에 리사이즈된 이미지를 표시합니다.
    cv2.waitKey(0) # 키 입력이 있을 때까지 대기합니다.
    cv2.destroyAllWindows() # 모든 OpenCV 창을 닫습니다.

# 이미지 미리보기 섹션
images = {name: cv2.imread(name) for name in IMAGE_FILENAMES} # 다운로드된 이미지 파일들을 읽어 딕셔너리에 저장
for name, image in images.items(): # 각 이미지에 대해 반복
    print(name) # 이미지 파일 이름 출력
    resize_and_show(image) # 이미지 리사이즈 후 미리보기

# 제스처 인식기 생성 섹션
# 기본 옵션을 설정합니다. 모델 파일의 경로를 지정합니다.
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
# 제스처 인식기 옵션을 설정합니다.
options = vision.GestureRecognizerOptions(base_options=base_options)
# 설정된 옵션으로 제스처 인식기를 생성합니다.
recognizer = vision.GestureRecognizer.create_from_options(options)

# 이미지에서 제스처 인식 및 결과 저장 섹션
mp_images = [] # MediaPipe Image 객체를 저장할 리스트
results = [] # 제스처 인식 결과를 저장할 리스트
for image_file_name in IMAGE_FILENAMES: # 각 이미지 파일 이름에 대해 반복
    image = mp.Image.create_from_file(image_file_name) # 파일에서 MediaPipe Image 객체 생성
    recognition_result = recognizer.recognize(image) # 이미지에서 제스처 인식 수행
    mp_images.append(image) # MediaPipe Image 객체를 리스트에 추가
    top_gesture = recognition_result.gestures[0][0] # 가장 높은 점수의 제스처 추출
    hand_landmarks = recognition_result.hand_landmarks # 손 랜드마크 추출
    results.append((top_gesture, hand_landmarks)) # 제스처와 랜드마크를 결과 리스트에 추가

# 결과 시각화 섹션
display_batch_of_images_with_gestures_and_hand_landmarks(mp_images, results) # 인식된 제스처와 랜드마크를 이미지에 그려서 표시