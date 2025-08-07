# OpenCV 마우스 상호작용 예제 - 마우스로 그리기
import cv2
import numpy as np

print("=== OpenCV 마우스 상호작용 예제 ===")
print("마우스를 사용하여 다양한 도형을 그리는 예제입니다.")

# 전역 변수들
drawing = False  # 마우스 드래그 중인지 확인
mode = True      # True면 사각형, False면 원
ix, iy = -1, -1  # 시작 좌표
current_tool = 0  # 0: 사각형, 1: 원, 2: 자유 그리기, 3: 선
tool_names = ["Rectangle", "Circle", "Free Draw", "Line"]

# 색상과 두께 설정
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
color_names = ["Blue", "Green", "Red", "Cyan", "Magenta", "Yellow"]
current_color_idx = 0
thickness = 2

# 이미지 생성
img = np.ones((600, 800, 3), dtype=np.uint8) * 255
img_backup = img.copy()  # 임시 그리기용 백업

def draw_ui():
    """사용자 인터페이스 그리기"""
    global img
    
    # 상단 도구 패널
    cv2.rectangle(img, (0, 0), (800, 80), (200, 200, 200), -1)
    
    # 현재 도구 표시
    cv2.putText(img, f'Tool: {tool_names[current_tool]}', (10, 25), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # 현재 색상 표시
    current_color = colors[current_color_idx]
    cv2.putText(img, f'Color: {color_names[current_color_idx]}', (10, 50), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.circle(img, (250, 40), 15, current_color, -1)
    
    # 두께 표시
    cv2.putText(img, f'Thickness: {thickness}', (300, 35), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # 색상 팔레트
    for i, color in enumerate(colors):
        x = 400 + i * 35
        cv2.circle(img, (x, 40), 12, color, -1)
        if i == current_color_idx:
            cv2.circle(img, (x, 40), 15, (0, 0, 0), 2)
    
    # 조작 안내
    cv2.putText(img, 'Controls: T-Tool | C-Color | +/- Thickness | R-Reset | S-Save', 
               (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

def mouse_callback(event, x, y, flags, param):
    """마우스 콜백 함수"""
    global ix, iy, drawing, img, img_backup, current_tool, thickness, current_color_idx
    
    current_color = colors[current_color_idx]
    
    # UI 영역 클릭 처리
    if y <= 80:
        # 색상 팔레트 클릭
        for i, color in enumerate(colors):
            palette_x = 400 + i * 35
            if abs(x - palette_x) <= 15 and abs(y - 40) <= 15:
                current_color_idx = i
                print(f"색상 변경: {color_names[i]}")
                draw_ui()
                return
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        img_backup = img.copy()  # 임시 그리기를 위한 백업
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_temp = img_backup.copy()  # 백업에서 시작
            
            if current_tool == 0:  # 사각형
                cv2.rectangle(img_temp, (ix, iy), (x, y), current_color, thickness)
            elif current_tool == 1:  # 원
                radius = int(np.sqrt((x - ix)**2 + (y - iy)**2))
                cv2.circle(img_temp, (ix, iy), radius, current_color, thickness)
            elif current_tool == 2:  # 자유 그리기
                cv2.line(img, (ix, iy), (x, y), current_color, thickness)
                ix, iy = x, y  # 시작점 업데이트
                img_temp = img.copy()
            elif current_tool == 3:  # 선
                cv2.line(img_temp, (ix, iy), (x, y), current_color, thickness)
            
            # UI 다시 그리기
            draw_ui_on_temp(img_temp)
            cv2.imshow('Drawing Canvas', img_temp)
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        
        if current_tool == 0:  # 사각형
            cv2.rectangle(img, (ix, iy), (x, y), current_color, thickness)
        elif current_tool == 1:  # 원
            radius = int(np.sqrt((x - ix)**2 + (y - iy)**2))
            cv2.circle(img, (ix, iy), radius, current_color, thickness)
        elif current_tool == 3:  # 선
            cv2.line(img, (ix, iy), (x, y), current_color, thickness)
        
        # 자유 그리기는 이미 그려짐
        draw_ui()

def draw_ui_on_temp(temp_img):
    """임시 이미지에 UI 그리기"""
    # 상단 도구 패널
    cv2.rectangle(temp_img, (0, 0), (800, 80), (200, 200, 200), -1)
    
    # 현재 도구 표시
    cv2.putText(temp_img, f'Tool: {tool_names[current_tool]}', (10, 25), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # 현재 색상 표시
    current_color = colors[current_color_idx]
    cv2.putText(temp_img, f'Color: {color_names[current_color_idx]}', (10, 50), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.circle(temp_img, (250, 40), 15, current_color, -1)
    
    # 두께 표시
    cv2.putText(temp_img, f'Thickness: {thickness}', (300, 35), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # 색상 팔레트
    for i, color in enumerate(colors):
        x = 400 + i * 35
        cv2.circle(temp_img, (x, 40), 12, color, -1)
        if i == current_color_idx:
            cv2.circle(temp_img, (x, 40), 15, (0, 0, 0), 2)
    
    # 조작 안내
    cv2.putText(temp_img, 'Controls: T-Tool | C-Color | +/- Thickness | R-Reset | S-Save', 
               (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# 창 생성 및 마우스 콜백 설정
cv2.namedWindow('Drawing Canvas')
cv2.setMouseCallback('Drawing Canvas', mouse_callback)

# 초기 UI 그리기
draw_ui()

print("\n=== 조작법 ===")
print("마우스 드래그: 그리기")
print("T: 도구 변경 (사각형 → 원 → 자유그리기 → 선)")
print("C: 색상 변경")
print("+/-: 두께 조절")
print("R: 화면 지우기")
print("S: 저장")
print("Q: 종료")
print("색상 팔레트 클릭: 직접 색상 선택")

while True:
    cv2.imshow('Drawing Canvas', img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('t') or key == ord('T'):
        current_tool = (current_tool + 1) % len(tool_names)
        print(f"도구 변경: {tool_names[current_tool]}")
        draw_ui()
    elif key == ord('c') or key == ord('C'):
        current_color_idx = (current_color_idx + 1) % len(colors)
        print(f"색상 변경: {color_names[current_color_idx]}")
        draw_ui()
    elif key == ord('+'): 
        thickness = min(thickness + 1, 10)
        print(f"두께: {thickness}")
        draw_ui()
    elif key == ord('-'):
        thickness = max(thickness - 1, 1)
        print(f"두께: {thickness}")
        draw_ui()
    elif key == ord('r') or key == ord('R'):
        img = np.ones((600, 800, 3), dtype=np.uint8) * 255
        draw_ui()
        print("화면 지우기")
    elif key == ord('s') or key == ord('S'):
        # UI 영역 제외하고 저장
        save_img = img[80:, :].copy()  # UI 부분 제외
        filename = f'../ex_img/drawing_result_{int(cv2.getTickCount())}.jpg'
        cv2.imwrite(filename, save_img)
        print(f"저장됨: {filename}")

cv2.destroyAllWindows()

print("\n=== 마우스 콜백 함수 설명 ===")
print("cv2.setMouseCallback(window_name, callback_function)")
print("마우스 이벤트:")
print("- cv2.EVENT_LBUTTONDOWN: 왼쪽 버튼 누름")
print("- cv2.EVENT_LBUTTONUP: 왼쪽 버튼 뗌")  
print("- cv2.EVENT_MOUSEMOVE: 마우스 이동")
print("- cv2.EVENT_RBUTTONDOWN: 오른쪽 버튼 누름")
print("\n콜백 함수 파라미터:")
print("- event: 마우스 이벤트 타입")
print("- x, y: 마우스 좌표")
print("- flags: 키보드 상태 (Ctrl, Shift 등)")
print("- param: 사용자 정의 데이터")
print("\n마우스 상호작용 예제 완료!")
