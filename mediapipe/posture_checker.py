# 자세 교정 시스템 - 올바른 앉은 자세 분석
import cv2 # OpenCV 라이브러리, 이미지 및 비디오 처리에 사용
import mediapipe as mp # MediaPipe 라이브러리, 자세 추정에 사용
import numpy as np # NumPy 라이브러리, 수치 계산에 사용
import math # 수학 계산을 위한 라이브러리
from PIL import Image, ImageDraw, ImageFont # PIL 라이브러리, 이미지에 텍스트를 그리기 위해 사용

# MediaPipe 초기화
mp_pose = mp.solutions.pose # MediaPipe의 자세 추정 솔루션
mp_drawing = mp.solutions.drawing_utils # MediaPipe의 그리기 유틸리티

def calculate_angle(a, b, c): # 세 점을 이용해 각도를 계산하는 함수 정의
    """세 점을 이용해 각도 계산""" # 함수의 설명 문자열 (docstring)
    a = np.array(a) # 첫 번째 점을 NumPy 배열로 변환
    b = np.array(b) # 두 번째 점 (중심점)을 NumPy 배열로 변환
    c = np.array(c) # 세 번째 점을 NumPy 배열로 변환
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0]) # 두 벡터 사이의 각도를 라디안으로 계산
    angle = np.abs(radians * 180.0 / np.pi) # 라디안을 도로 변환하고 절대값을 취함
    
    if angle > 180.0: # 각도가 180도를 초과하면
        angle = 360 - angle # 360도에서 빼서 작은 각을 구함
        
    return angle # 계산된 각도를 반환

def draw_korean_text(img, text, position, font_size=20, color=(255, 255, 255)): # 이미지에 한글 텍스트를 그리는 함수 정의
    """한글 텍스트를 이미지에 그리는 함수""" # 함수의 설명 문자열 (docstring)
    # numpy 배열을 PIL 이미지로 변환
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # OpenCV 이미지를 PIL 이미지로 변환 (BGR -> RGB)
    draw = ImageDraw.Draw(img_pil) # PIL 이미지에 그리기 위한 객체 생성
    
    try: # 예외 처리 시작
        # macOS 시스템 한글 폰트 사용
        font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", font_size) # macOS의 기본 한글 폰트 로드
    except: # 폰트 로드 실패 시
        try: # 다른 폰트 시도
            # 대체 폰트 시도
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size) # 대체 폰트 (Helvetica) 로드
        except: # 대체 폰트도 실패 시
            # 기본 폰트 사용
            font = ImageFont.load_default() # PIL의 기본 폰트 로드
    
    # 텍스트 그리기
    draw.text(position, text, font=font, fill=color) # 지정된 위치에 텍스트를 그림
    
    # PIL 이미지를 다시 numpy 배열로 변환
    img_result = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) # PIL 이미지를 다시 OpenCV 이미지로 변환 (RGB -> BGR)
    return img_result # 텍스트가 그려진 이미지를 반환

def check_posture(landmarks): # 자세 상태를 분석하는 함수 정의
    """자세 상태를 분석하는 함수""" # 함수의 설명 문자열 (docstring)
    posture_status = [] # 자세 상태 메시지를 저장할 리스트 초기화
    
    # 어깨 기울기 확인
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, # 왼쪽 어깨의 x, y 좌표
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, # 오른쪽 어깨의 x, y 좌표
                     landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    
    shoulder_slope = abs(left_shoulder[1] - right_shoulder[1]) # 양쪽 어깨의 y좌표 차이(기울기) 계산
    
    if shoulder_slope > 0.05:  # 어깨가 5% 이상 기울어짐
        posture_status.append("어깨가 기울어져 있습니다") # 상태 메시지 추가
    else: # 그렇지 않으면
        posture_status.append("어깨 자세 양호") # 상태 메시지 추가
    
    # 목/머리 위치 확인
    nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, # 코의 x, y 좌표
            landmarks[mp_pose.PoseLandmark.NOSE.value].y]
    neck = [(left_shoulder[0] + right_shoulder[0]) / 2, # 목의 x, y 좌표 (양 어깨의 중간)
            (left_shoulder[1] + right_shoulder[1]) / 2]
    
    head_forward = abs(nose[0] - neck[0]) # 코와 목의 x좌표 차이 계산
    
    if head_forward > 0.1:  # 머리가 목보다 10% 이상 앞으로 나감
        posture_status.append("목이 앞으로 나와있습니다") # 상태 메시지 추가
    else: # 그렇지 않으면
        posture_status.append("목 자세 양호") # 상태 메시지 추가
    
    # 등 곧음 정도 확인 (어깨-엉덩이-무릎 각도)
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, # 왼쪽 엉덩이의 x, y 좌표
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    
    back_angle = calculate_angle(left_shoulder, left_hip, [left_hip[0], left_hip[1] + 0.1]) # 어깨-엉덩이-수직선의 각도 계산
    
    if back_angle < 160:  # 등이 너무 구부러짐 (각도가 160도 미만)
        posture_status.append("등이 구부러져 있습니다") # 상태 메시지 추가
    else: # 그렇지 않으면
        posture_status.append("등 자세 양호") # 상태 메시지 추가
    
    return posture_status # 분석된 자세 상태 메시지 리스트 반환

# 웹캠 시작
cap = cv2.VideoCapture(0) # 0번 웹캠(기본 웹캠)을 염

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose: # MediaPipe Pose 객체 생성 (최소 감지/추적 신뢰도 설정)
    while cap.isOpened(): # 웹캠이 열려있는 동안 반복
        ret, frame = cap.read() # 웹캠에서 프레임을 읽어옴
        if not ret: # 프레임을 읽어오지 못했다면
            break # 반복문 종료

        # 이미지 처리
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 프레임의 색상 공간을 BGR에서 RGB로 변환
        image.flags.writeable = False # 성능 향상을 위해 이미지에 쓰기 금지 설정
        
        # 포즈 감지
        results = pose.process(image) # MediaPipe로 자세 감지 수행
        
        # 이미지 다시 변환
        image.flags.writeable = True # 이미지에 다시 쓰기 허용
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # 색상 공간을 다시 RGB에서 BGR로 변환
        
        # 자세 분석
        try: # 예외 처리 시작
            landmarks = results.pose_landmarks.landmark # 감지된 자세 랜드마크 추출
            posture_feedback = check_posture(landmarks) # 자세 분석 함수 호출
            
            # 한글 피드백 표시
            for i, feedback in enumerate(posture_feedback): # 각 피드백 메시지에 대해 반복
                # 양호한 자세는 녹색, 문제 있는 자세는 빨간색
                color = (0, 255, 0) if "양호" in feedback else (255, 0, 0) # 피드백 내용에 따라 글자색 결정
                image = draw_korean_text(image, feedback, (10, 30 + i * 35), 24, color) # 이미지에 한글 피드백 텍스트를 그림
            
        except: # 랜드마크 감지에 실패했을 경우
            image = draw_korean_text(image, "자세를 인식할 수 없습니다", (10, 30), 24, (0, 0, 255)) # 에러 메시지를 그림
        
        # 포즈 랜드마크 그리기
        if results.pose_landmarks: # 자세 랜드마크가 감지되었다면
            mp_drawing.draw_landmarks( # 이미지에 랜드마크와 연결선을 그림
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, # 대상 이미지, 랜드마크, 연결선 정보
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), # 랜드마크 점 스타일
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)) # 랜드마크 연결선 스타일
        
        cv2.imshow('Posture Checker - 자세 교정 시스템', image) # 'Posture Checker'라는 이름의 창에 결과 이미지를 표시
        
        if cv2.waitKey(10) & 0xFF == ord('q'): # 10ms 동안 키 입력을 기다리고, 'q' 키가 눌리면
            break # 반복문 종료

cap.release() # 웹캠 리소스 해제
cv2.destroyAllWindows() # 모든 OpenCV 창을 닫음