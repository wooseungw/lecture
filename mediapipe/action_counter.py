# 운동 동작 카운터 - 스쿼트 횟수 자동 계산
import cv2 # OpenCV 라이브러리, 비디오 및 이미지 처리에 사용됩니다.
import mediapipe as mp # MediaPipe 라이브러리, 자세 추정(pose estimation)에 사용됩니다.
import numpy as np # NumPy 라이브러리, 수치 계산 및 배열 처리에 사용됩니다.
from korean_text_utils import draw_korean_text, draw_text_with_background # 한글 텍스트를 이미지에 그리기 위한 유틸리티 함수를 가져옵니다.

# MediaPipe 초기화
mp_pose = mp.solutions.pose # MediaPipe의 자세 추정 솔루션을 가져옵니다.
mp_drawing = mp.solutions.drawing_utils # MediaPipe의 그리기 관련 유틸리티를 가져옵니다.

def calculate_angle(a, b, c): # 세 점(관절)을 이용해 각도를 계산하는 함수를 정의합니다.
    """세 점을 이용해 각도 계산""" # 함수의 설명 문자열(docstring)입니다.
    a = np.array(a)  # 첫 번째 점의 좌표를 NumPy 배열로 변환합니다.
    b = np.array(b)  # 중간점(각도의 꼭짓점)의 좌표를 NumPy 배열로 변환합니다.
    c = np.array(c)  # 세 번째 점의 좌표를 NumPy 배열로 변환합니다.
    
    # arctan2를 사용하여 두 벡터(b-a, b-c) 사이의 각도를 라디안 단위로 계산합니다.
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    # 계산된 라디안 값을 도(degree) 단위로 변환하고 절대값을 취합니다.
    angle = np.abs(radians * 180.0 / np.pi)
    
    # 각도가 180도를 초과하는 경우, 더 작은 각(360 - angle)을 사용합니다.
    if angle > 180.0:
        angle = 360 - angle
        
    return angle # 계산된 각도를 반환합니다.

# 웹캠 시작
cap = cv2.VideoCapture(0) # 0번 카메라(기본 웹캠)를 엽니다.

# 스쿼트 카운터 변수
squat_counter = 0 # 스쿼트 횟수를 저장할 변수를 0으로 초기화합니다.
squat_stage = None  # 현재 스쿼트 단계를 저장할 변수입니다. "up"(일어선 상태) 또는 "down"(앉은 상태)이 됩니다.

# MediaPipe Pose 모델을 로드합니다. with 구문을 사용하여 리소스를 안전하게 관리합니다.
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # 웹캠이 열려 있는 동안 계속 반복합니다.
    while cap.isOpened():
        # 웹캠에서 한 프레임을 읽어옵니다. ret은 성공 여부, frame은 실제 이미지입니다.
        ret, frame = cap.read()
        # 프레임을 제대로 읽어오지 못했다면, 루프를 종료합니다.
        if not ret:
            break

        # 이미지 처리
        # MediaPipe에서 처리할 수 있도록 이미지의 색상 체계를 BGR에서 RGB로 변환합니다.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 성능 향상을 위해 이미지에 쓰기 작업을 비활성화합니다.
        image.flags.writeable = False
        
        # 포즈 감지
        # MediaPipe 모델을 사용하여 이미지에서 자세를 감지합니다.
        results = pose.process(image)
        
        # 이미지 다시 변환
        # 화면에 결과를 그리기 위해 다시 쓰기 작업을 활성화합니다.
        image.flags.writeable = True
        # 화면 표시는 OpenCV를 사용하므로, 색상 체계를 다시 RGB에서 BGR로 변환합니다.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 랜드마크 추출
        try: # 자세 랜드마크가 감지되지 않았을 경우를 대비해 예외 처리를 합니다.
            # 감지된 자세 랜드마크(관절 위치)를 가져옵니다.
            landmarks = results.pose_landmarks.landmark
            
            # 스쿼트 분석을 위한 관절 좌표 추출
            # 왼쪽 엉덩이, 무릎, 발목의 x, y 좌표를 가져옵니다.
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            # 무릎 각도 계산
            # 엉덩이-무릎-발목 세 점을 이용하여 무릎의 각도를 계산합니다.
            angle = calculate_angle(hip, knee, ankle)
            
            # 스쿼트 단계 판별
            if angle > 160:  # 무릎 각도가 160도 이상이면 (거의 선 상태)
                squat_stage = "up" # 현재 단계를 "up"으로 설정합니다.
            if angle < 90 and squat_stage == "up":  # 무릎 각도가 90도 미만이고, 이전 단계가 "up"이었을 때
                squat_stage = "down" # 현재 단계를 "down"으로 설정합니다. (스쿼트 완료)
                squat_counter += 1 # 스쿼트 횟수를 1 증가시킵니다.
                print(f"스쿼트 횟수: {squat_counter}") # 콘솔에 현재 횟수를 출력합니다.
            
            # 무릎 각도 표시 (화면에 그리기)
            angle_text = f'무릎 각도: {int(angle)}°' # 화면에 표시할 각도 텍스트를 만듭니다.
            # 무릎의 정규화된 좌표를 화면 좌표(640x480 기준)로 변환합니다.
            knee_pos = tuple(np.multiply(knee, [640, 480]).astype(int))
            # 배경이 있는 텍스트를 무릎 위치에 그립니다.
            image = draw_text_with_background(image, angle_text, knee_pos, 16, 
                                            (255, 255, 255), (0, 0, 0), 3)
                       
        except: # 랜드마크를 감지하지 못했을 때 아무 작업도 하지 않고 넘어갑니다.
            pass
        
        # 카운터 정보 표시
        # 화면 좌측 상단에 정보 표시를 위한 사각형 배경을 그립니다.
        cv2.rectangle(image, (0, 0), (300, 100), (245, 117, 16), -1)
        
        # 스쿼트 횟수 (한글)
        image = draw_korean_text(image, '스쿼트', (15, 15), 18, (0, 0, 0)) # '스쿼트'라는 제목을 그립니다.
        image = draw_korean_text(image, str(squat_counter), (10, 60), 36, (255, 255, 255)) # 계산된 스쿼트 횟수를 그립니다.
        
        # 현재 단계 (한글)
        image = draw_korean_text(image, '단계', (120, 15), 18, (0, 0, 0)) # '단계'라는 제목을 그립니다.
        # squat_stage 값('up'/'down')을 한글('올림'/'내림')로 변환합니다.
        stage_korean = {'up': '올림', 'down': '내림'}.get(squat_stage, squat_stage or '')
        image = draw_korean_text(image, stage_korean, (120, 60), 24, (255, 255, 255)) # 변환된 한글 단계를 그립니다.
        
        # 포즈 랜드마크 그리기
        if results.pose_landmarks: # 감지된 자세 랜드마크가 있다면
            # 이미지 위에 랜드마크(점)와 연결선(뼈대)을 그립니다.
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # 결과 이미지를 '스쿼트 카운터'라는 이름의 창에 보여줍니다.
        cv2.imshow('스쿼트 카운터 - Squat Counter', image)
        
        # 10ms 동안 키 입력을 기다리고, 'q' 키가 눌리면 루프를 종료합니다.
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# 사용이 끝난 웹캠 리소스를 해제합니다.
cap.release()
# 모든 OpenCV 창을 닫습니다.
cv2.destroyAllWindows()