# OpenCV 이미지 변환 예제 - 크기 조절, 블러, 기본 필터링
import cv2
import numpy as np

print("=== OpenCV 이미지 변환 예제 ===")
print("이미지 크기 조절, 블러링, 기본 필터를 다루는 예제입니다.")

# 원본 이미지 생성 (체크보드 패턴)
def create_checkerboard(size, square_size):
    """체크보드 패턴 이미지 생성"""
    img = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(0, size, square_size):
        for j in range(0, size, square_size):
            if (i // square_size + j // square_size) % 2 == 0:
                img[i:i+square_size, j:j+square_size] = [255, 255, 255]
            else:
                img[i:i+square_size, j:j+square_size] = [100, 150, 200]
    
    # 중앙에 원 추가
    cv2.circle(img, (size//2, size//2), size//4, (0, 255, 0), -1)
    cv2.putText(img, 'Original', (size//2-50, size//2), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return img

# 원본 이미지 생성
original = create_checkerboard(400, 40)

print("\n1. 이미지 크기 조절 (resize)")
# 1. 크기 조절 예제들
resize_small = cv2.resize(original, (200, 200))  # 절대 크기
resize_large = cv2.resize(original, None, fx=1.5, fy=1.5)  # 배율 사용
resize_stretch = cv2.resize(original, (600, 200))  # 비율 변경

# 크기 정보 텍스트 추가
cv2.putText(resize_small, 'Small', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
cv2.putText(resize_large, 'Large', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
cv2.putText(resize_stretch, 'Stretched', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

print("   - 작은 크기: 200x200")
print("   - 큰 크기: 1.5배 확대")
print("   - 늘어뜨린 크기: 600x200")

# 2. 다양한 보간법
print("\n2. 다양한 보간법 (interpolation)")
interpolations = [
    (cv2.INTER_NEAREST, "NEAREST"),
    (cv2.INTER_LINEAR, "LINEAR"),
    (cv2.INTER_CUBIC, "CUBIC"),
    (cv2.INTER_LANCZOS4, "LANCZOS4")
]

interp_results = []
for interp, name in interpolations:
    resized = cv2.resize(original, (200, 200), interpolation=interp)
    cv2.putText(resized, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    interp_results.append(resized)

print("\n3. 가우시안 블러 (GaussianBlur)")
# 3. 블러 예제들
blur_results = []
blur_sizes = [5, 15, 31, 51]

for blur_size in blur_sizes:
    blurred = cv2.GaussianBlur(original, (blur_size, blur_size), 0)
    cv2.putText(blurred, f'Blur {blur_size}', (10, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    blur_results.append(blurred)
    print(f"   - 블러 크기 {blur_size}x{blur_size}")

print("\n4. 기타 블러 종류")
# 4. 다른 블러 종류들
blur_types = [
    (cv2.blur(original, (15, 15)), "Average Blur"),
    (cv2.medianBlur(original, 15), "Median Blur"),
    (cv2.bilateralFilter(original, 15, 80, 80), "Bilateral Filter")
]

other_blurs = []
for blurred, name in blur_types:
    cv2.putText(blurred, name, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    other_blurs.append(blurred)
    print(f"   - {name}")

# 결과 이미지들을 그리드로 배치
def create_grid(images, cols, title):
    """이미지들을 그리드로 배치"""
    rows = len(images) // cols + (1 if len(images) % cols else 0)
    if not images:
        return np.zeros((100, 100, 3), dtype=np.uint8)
    
    # 모든 이미지를 같은 크기로 리사이즈
    target_height, target_width = 400, 400
    resized_images = []
    for img in images:
        if img.shape[:2] != (target_height, target_width):
            img_resized = cv2.resize(img, (target_width, target_height))
        else:
            img_resized = img.copy()
        resized_images.append(img_resized)
    
    h, w = target_height, target_width
    grid = np.zeros((rows * h + 50, cols * w, 3), dtype=np.uint8)
    
    # 제목 추가
    cv2.putText(grid, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    for i, img in enumerate(resized_images):
        row = i // cols
        col = i % cols
        y_start = row * h + 50
        y_end = y_start + h
        x_start = col * w
        x_end = x_start + w
        grid[y_start:y_end, x_start:x_end] = img
    
    return grid

# 각 카테고리별 그리드 생성
print("\n5. 결과 이미지 생성 중...")
resize_grid = create_grid([original, resize_small, resize_large], 3, "Resize Examples")
interp_grid = create_grid(interp_results, 2, "Interpolation Methods")
blur_grid = create_grid(blur_results, 2, "Gaussian Blur Examples")
other_blur_grid = create_grid(other_blurs, 2, "Other Blur Types")

# 모든 결과를 하나의 창에 표시
print("\n=== 사용된 함수들 ===")
print("cv2.resize(src, dsize, fx, fy, interpolation)")
print("  - dsize: 출력 크기 (width, height)")
print("  - fx, fy: x, y 방향 배율")
print("  - interpolation: 보간법")
print("")
print("cv2.GaussianBlur(src, ksize, sigmaX, sigmaY)")
print("  - ksize: 커널 크기 (홀수)")
print("  - sigmaX, sigmaY: 가우시안 커널의 표준편차")
print("")
print("cv2.blur(src, ksize) - 평균 블러")
print("cv2.medianBlur(src, ksize) - 미디언 블러")
print("cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace) - 양방향 필터")

# 이미지 출력
cv2.imshow('Original', original)
cv2.imshow('Resize Examples', resize_grid)
cv2.imshow('Interpolation Methods', interp_grid)
cv2.imshow('Gaussian Blur', blur_grid)
cv2.imshow('Other Blurs', other_blur_grid)

print("\n아무 키나 누르면 종료합니다...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# 결과 이미지들 저장
cv2.imwrite('../ex_img/resize_examples.jpg', resize_grid)
cv2.imwrite('../ex_img/blur_examples.jpg', blur_grid)
print("예제 이미지들이 저장되었습니다.")
