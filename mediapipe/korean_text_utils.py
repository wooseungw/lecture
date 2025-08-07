# 한글 텍스트 렌더링 유틸리티
import cv2 # OpenCV 라이브러리, 이미지 처리에 사용됩니다.
import numpy as np # NumPy 라이브러리, 배열 처리에 사용됩니다.
from PIL import Image, ImageDraw, ImageFont # Python Imaging Library(PIL) 또는 Pillow 라이브러리에서 이미지에 텍스트를 그리기 위한 모듈들을 가져옵니다.
import os # 운영 체제와 상호 작용하여 파일 경로 등을 다루기 위해 사용됩니다.

class KoreanTextRenderer: # 한글 텍스트를 OpenCV 이미지에 렌더링하는 클래스를 정의합니다.
    """한글 텍스트를 OpenCV 이미지에 렌더링하는 클래스"""
    
    def __init__(self, font_size=20): # 클래스 초기화 메서드
        self.font_size = font_size # 기본 폰트 크기를 설정합니다.
        self.font = self._load_korean_font() # 한글 폰트를 로드하여 인스턴스 변수에 저장합니다.
    
    def _load_korean_font(self):
        """시스템에서 한글 폰트 로드"""
        # 다양한 운영 체제에 대한 일반적인 한글 폰트 경로 목록입니다.
        font_paths = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS 기본 한글 폰트
            "/System/Library/Fonts/Helvetica.ttc",         # macOS 대체 폰트
            "C:/Windows/Fonts/malgun.ttf",                 # Windows 맑은 고딕
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Ubuntu 나눔고딕
        ]
        
        # 폰트 경로 목록을 순회하며 사용 가능한 폰트를 찾습니다.
        for font_path in font_paths:
            try:
                if os.path.exists(font_path): # 해당 경로에 파일이 존재하면
                    # 폰트 파일을 로드하여 ImageFont 객체를 생성하고 반환합니다.
                    return ImageFont.truetype(font_path, self.font_size)
            except:
                continue # 오류 발생 시 다음 경로로 넘어갑니다.
        
        # 목록에 있는 모든 폰트를 로드하지 못한 경우, PIL의 기본 폰트를 사용합니다.
        return ImageFont.load_default()
    
    def draw_text(self, img, text, position, color=(255, 255, 255), font_size=None):
        """이미지에 한글 텍스트 그리기"""
        # 만약 함수 호출 시 새로운 폰트 크기가 지정되었다면, 폰트를 다시 로드합니다.
        if font_size and font_size != self.font_size:
            self.font_size = font_size
            self.font = self._load_korean_font()
        
        # OpenCV 이미지(NumPy 배열, BGR 색상 순서)를 PIL 이미지(RGB 색상 순서)로 변환합니다.
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil) # PIL 이미지에 그림을 그릴 수 있는 Draw 객체를 생성합니다.
        
        # OpenCV의 BGR 색상 순서를 PIL의 RGB 순서로 변환합니다.
        pil_color = (color[2], color[1], color[0])
        
        # 지정된 위치에 텍스트를 그립니다.
        draw.text(position, text, font=self.font, fill=pil_color)
        
        # 텍스트가 그려진 PIL 이미지를 다시 OpenCV 이미지(NumPy 배열, BGR)로 변환하여 반환합니다.
        img_result = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        return img_result
    
    def get_text_size(self, text):
        """텍스트 크기 계산"""
        # 임시 이미지를 만들어 텍스트가 차지할 영역(bounding box)의 크기를 계산합니다.
        img_temp = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(img_temp)
        bbox = draw.textbbox((0, 0), text, font=self.font)
        # (x1, y1, x2, y2) 형태의 bbox에서 너비와 높이를 계산하여 반환합니다.
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

# 클래스를 매번 생성하지 않고 쉽게 사용할 수 있도록 전역 렌더러 인스턴스를 생성합니다.
text_renderer = KoreanTextRenderer()

def draw_korean_text(img, text, position, font_size=20, color=(255, 255, 255)):
    """한글 텍스트를 이미지에 그리는 간단한 함수"""
    global text_renderer # 전역 인스턴스를 사용합니다.
    # 전역 렌더러의 draw_text 메서드를 호출하여 텍스트를 그립니다.
    return text_renderer.draw_text(img, text, position, color, font_size)

def draw_text_with_background(img, text, position, font_size=20, 
                            text_color=(255, 255, 255), bg_color=(0, 0, 0), 
                            padding=5):
    """배경이 있는 한글 텍스트 그리기"""
    global text_renderer # 전역 인스턴스를 사용합니다.
    
    # 텍스트 크기를 계산하기 위해 렌더러의 폰트 크기를 설정하고 폰트를 다시 로드합니다.
    text_renderer.font_size = font_size
    text_renderer.font = text_renderer._load_korean_font()
    text_width, text_height = text_renderer.get_text_size(text)
    
    # 텍스트 뒤에 배경이 될 사각형을 그립니다.
    x, y = position
    cv2.rectangle(img, 
                 (x - padding, y - padding), # 사각형 시작점 (패딩 적용)
                 (x + text_width + padding, y + text_height + padding), # 사각형 끝점 (패딩 적용)
                 bg_color, -1) # -1은 채워진 사각형을 의미합니다.
    
    # 배경 위에 텍스트를 그립니다.
    return text_renderer.draw_text(img, text, position, text_color, font_size)

# 이 스크립트가 직접 실행될 때만 아래 코드를 실행합니다. (모듈로 임포트될 때는 실행 안 됨)
if __name__ == "__main__":
    # 테스트용으로 검은색 이미지를 생성합니다.
    test_img = np.zeros((300, 600, 3), dtype=np.uint8)
    
    # 한글 텍스트 그리기 함수들을 테스트합니다.
    test_img = draw_korean_text(test_img, "안녕하세요! 한글 테스트입니다.", (50, 50), 24, (0, 255, 0))
    test_img = draw_korean_text(test_img, "자세 교정 시스템", (50, 100), 30, (255, 0, 0))
    test_img = draw_text_with_background(test_img, "배경이 있는 텍스트", (50, 150), 20, 
                                       (255, 255, 255), (100, 100, 100))
    
    # 결과 이미지를 화면에 표시합니다.
    cv2.imshow('Korean Text Test', test_img)
    cv2.waitKey(0) # 키 입력이 있을 때까지 대기합니다.
    cv2.destroyAllWindows() # 모든 OpenCV 창을 닫습니다.