import mediapipe as mp # MediaPipe 라이브러리를 가져옵니다.
import cv2 # OpenCV 라이브러리를 가져옵니다. 이미지 파일을 읽는 데 사용됩니다.

# MediaPipe의 이미지 분류 솔루션을 변수에 할당합니다.
mp_image = mp.solutions.image_classification

# 이미지 분류기(classifier)를 초기화합니다.
# model_selection=0은 MediaPipe에서 제공하는 기본 모델(예: EfficientNet-Lite0)을 사용하겠다는 의미입니다.
classifier = mp_image.ImageClassifier(model_selection=0)

# 분류할 이미지의 경로를 지정합니다.
###################################
image_path = 'ex_img/pointing_up.jpg'  # 이 부분을 원하는 이미지 파일 경로로 변경하여 사용하세요.
###################################

# OpenCV를 사용하여 지정된 경로의 이미지를 읽어옵니다.
image = cv2.imread(image_path)
# MediaPipe는 RGB 형식의 이미지를 입력으로 받으므로, OpenCV의 기본 BGR 형식을 RGB로 변환합니다.
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 이미지 분류를 실행합니다.
results = classifier.classify(image_rgb)

# 분류 결과를 출력합니다.
# results.classifications는 여러 분류 결과를 포함할 수 있는 리스트입니다.
for classification in results.classifications:
    # 각 분류 결과(classification)는 여러 카테고리(레이블과 점수)를 포함할 수 있습니다.
    for category in classification.categories:
        # 각 카테고리의 이름(레이블)과 신뢰도 점수를 출력합니다.
        # 점수는 소수점 둘째 자리까지 표시합니다.
        print(f'Label: {category.category_name}, Score: {category.score:.2f}')

# 사용이 끝난 분류기 리소스를 해제합니다.
classifier.close()