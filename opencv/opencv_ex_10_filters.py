# OpenCV 이미지 필터와 효과 예제 - 다양한 필터링 기법
import cv2
import numpy as np

print("=== OpenCV 이미지 필터와 효과 예제 ===")
print("다양한 필터링과 이미지 효과를 보여주는 예제입니다.")

# 테스트 이미지 생성
def create_test_image():
    """다양한 패턴이 있는 테스트 이미지 생성"""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 128
    
    # 체크보드 패턴
    for i in range(0, 200, 20):
        for j in range(0, 300, 20):
            if (i//20 + j//20) % 2 == 0:
                img[i:i+20, j:j+20] = [255, 255, 255]
    
    # 그라디언트
    for i in range(200, 400):
        intensity = int((i - 200) / 200 * 255)
        img[i, 300:600] = [intensity, intensity, 255-intensity]
    
    # 원과 사각형 추가
    cv2.circle(img, (150, 300), 60, (0, 255, 0), -1)
    cv2.rectangle(img, (400, 250), (550, 350), (255, 0, 0), -1)
    
    # 노이즈 추가
    noise = np.random.randint(-30, 30, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return img

# 원본 이미지 생성
original = create_test_image()

print("\n1. 기본 블러 필터들")
# 1. 다양한 블러 필터들
blur_average = cv2.blur(original, (15, 15))
blur_gaussian = cv2.GaussianBlur(original, (15, 15), 0)
blur_median = cv2.medianBlur(original, 15)
blur_bilateral = cv2.bilateralFilter(original, 15, 80, 80)

# 텍스트 추가
cv2.putText(blur_average, 'Average Blur', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(blur_gaussian, 'Gaussian Blur', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(blur_median, 'Median Blur', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(blur_bilateral, 'Bilateral Filter', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

print("2. 에지 검출 필터들")
# 2. 에지 검출
gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

# Sobel 에지 검출
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel_combined = np.sqrt(sobel_x**2 + sobel_y**2)
sobel_combined = np.uint8(np.clip(sobel_combined, 0, 255))

# Laplacian 에지 검출
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
laplacian = np.uint8(np.abs(laplacian))

# Canny 에지 검출
canny = cv2.Canny(gray, 50, 150)

# 에지 검출 결과를 컬러로 변환
sobel_colored = cv2.applyColorMap(sobel_combined, cv2.COLORMAP_JET)
laplacian_colored = cv2.applyColorMap(laplacian, cv2.COLORMAP_HOT)
canny_colored = cv2.applyColorMap(canny, cv2.COLORMAP_COOL)

# 텍스트 추가
cv2.putText(sobel_colored, 'Sobel Edge', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(laplacian_colored, 'Laplacian Edge', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(canny_colored, 'Canny Edge', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

print("3. 형태학적 연산")
# 3. 모폴로지 연산 (형태학적 연산)
kernel = np.ones((5, 5), np.uint8)

# 그레이스케일에서 이진화
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 형태학적 연산들
erosion = cv2.erode(binary, kernel, iterations=1)
dilation = cv2.dilate(binary, kernel, iterations=1)
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# 컬러로 변환
erosion_colored = cv2.applyColorMap(erosion, cv2.COLORMAP_WINTER)
dilation_colored = cv2.applyColorMap(dilation, cv2.COLORMAP_AUTUMN)
opening_colored = cv2.applyColorMap(opening, cv2.COLORMAP_SPRING)
closing_colored = cv2.applyColorMap(closing, cv2.COLORMAP_SUMMER)

# 텍스트 추가
cv2.putText(erosion_colored, 'Erosion', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(dilation_colored, 'Dilation', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(opening_colored, 'Opening', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(closing_colored, 'Closing', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

print("4. 특수 효과들")
# 4. 특수 효과들
# HSV 색공간으로 변환 후 조작
hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
hsv_modified = hsv.copy()
hsv_modified[:, :, 1] = hsv_modified[:, :, 1] * 1.5  # 채도 증가
hsv_modified = np.clip(hsv_modified, 0, 255).astype(np.uint8)
saturated = cv2.cvtColor(hsv_modified, cv2.COLOR_HSV2BGR)

# 감마 보정
def gamma_correction(img, gamma):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(img, table)

gamma_bright = gamma_correction(original, 0.5)  # 밝게
gamma_dark = gamma_correction(original, 2.0)    # 어둡게

# 히스토그램 평활화
gray_original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
equalized = cv2.equalizeHist(gray_original)
equalized_colored = cv2.applyColorMap(equalized, cv2.COLORMAP_RAINBOW)

# 텍스트 추가
cv2.putText(saturated, 'Saturated', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(gamma_bright, 'Gamma Bright', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(gamma_dark, 'Gamma Dark', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(equalized_colored, 'Histogram Equalized', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

print("5. 결과 이미지들을 표시합니다...")

# 이미지들을 그룹별로 표시
def show_image_group(images, titles, window_name, rows=2, cols=2):
    """여러 이미지를 하나의 창에 표시"""
    h, w = images[0].shape[:2]
    combined = np.zeros((h * rows, w * cols, 3), dtype=np.uint8)
    
    for i, (img, title) in enumerate(zip(images, titles)):
        if len(img.shape) == 2:  # 그레이스케일이면 컬러로 변환
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
        row = i // cols
        col = i % cols
        y_start, y_end = row * h, (row + 1) * h
        x_start, x_end = col * w, (col + 1) * w
        combined[y_start:y_end, x_start:x_end] = img
    
    cv2.imshow(window_name, combined)

# 1. 블러 필터들
blur_images = [original, blur_average, blur_gaussian, blur_median]
blur_titles = ["Original", "Average", "Gaussian", "Median"]
show_image_group(blur_images, blur_titles, "Blur Filters")

# 2. 에지 검출
edge_images = [cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), sobel_colored, laplacian_colored, canny_colored]
edge_titles = ["Original Gray", "Sobel", "Laplacian", "Canny"]
show_image_group(edge_images, edge_titles, "Edge Detection")

# 3. 형태학적 연산
morph_images = [cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR), erosion_colored, dilation_colored, opening_colored]
morph_titles = ["Binary", "Erosion", "Dilation", "Opening"]
show_image_group(morph_images, morph_titles, "Morphological Operations")

# 4. 특수 효과
effect_images = [original, saturated, gamma_bright, equalized_colored]
effect_titles = ["Original", "Saturated", "Gamma Corrected", "Hist Equalized"]
show_image_group(effect_images, effect_titles, "Special Effects")

print("\n=== 사용된 주요 함수들 ===")
print("블러 필터:")
print("- cv2.blur(): 평균 블러")
print("- cv2.GaussianBlur(): 가우시안 블러")
print("- cv2.medianBlur(): 미디언 블러")
print("- cv2.bilateralFilter(): 양방향 필터")
print("\n에지 검출:")
print("- cv2.Sobel(): Sobel 에지 검출")
print("- cv2.Laplacian(): Laplacian 에지 검출")
print("- cv2.Canny(): Canny 에지 검출")
print("\n형태학적 연산:")
print("- cv2.erode(): 침식")
print("- cv2.dilate(): 팽창")
print("- cv2.morphologyEx(): 열림/닫힘 연산")
print("\n기타:")
print("- cv2.threshold(): 이진화")
print("- cv2.equalizeHist(): 히스토그램 평활화")
print("- cv2.applyColorMap(): 컬러맵 적용")

print("\n아무 키나 누르면 종료합니다...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# 결과 저장
cv2.imwrite('../ex_img/filter_blur_effects.jpg', np.hstack([original, blur_gaussian, blur_median, blur_bilateral]))
cv2.imwrite('../ex_img/filter_edge_detection.jpg', np.hstack([sobel_colored, laplacian_colored, canny_colored, equalized_colored]))
print("필터 예제 이미지들이 저장되었습니다.")
