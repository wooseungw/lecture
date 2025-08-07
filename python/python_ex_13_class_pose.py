import math

# 1. 하나의 점을 표현하는 Point2D 클래스 (기초 부품)
class Point2D:
    """2차원 평면 위의 한 점(x, y)을 나타내는 클래스"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other_point):
        """다른 Point2D 객체까지의 거리를 계산하는 메서드"""
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        return math.sqrt(dx**2 + dy**2) # 유클리드 거리 계산

# 2. 여러 개의 점들을 관리하는 Figure 클래스 (조립품)
class Figure:
    """이름을 가진 여러 개의 2D 포인트들을 관리하는 클래스"""
    def __init__(self, name):
        self.name = name
        self.points = {}  # 점들을 {'이름': Point2D객체} 형태로 저장할 딕셔너리

    def add_point(self, point_name, x, y):
        """새로운 점을 추가하는 메서드"""
        self.points[point_name] = Point2D(x, y)
        print(f"[{self.name}] '{point_name}' 점({x}, {y}) 추가됨.")

    def get_distance(self, point_name1, point_name2):
        """이름으로 두 점을 찾아 거리를 계산하는 메서드"""
        if point_name1 in self.points and point_name2 in self.points:
            point1 = self.points[point_name1]
            point2 = self.points[point_name2]
            return point1.distance_to(point2)
        else:
            print("오류: 해당 이름의 점을 찾을 수 없습니다.")
            return None

    def show_info(self):
        """도형에 포함된 모든 점의 정보를 출력하는 메서드"""
        print(f"--- 도형 '{self.name}'의 정보 ---")
        if not self.points:
            print("  (아직 점이 없습니다)")
            return
        for name, point in self.points.items():
            print(f"  - {name}: ({point.x}, {point.y})")

# --- 클래스 사용 부분 ---

# '사람'이라는 이름의 Figure 객체 생성
person_figure = Figure("사람1")

# MediaPipe/OpenPose가 관절을 찾았다고 가정하고, 점들을 추가
person_figure.add_point("코", 95, 50)
person_figure.add_point("왼쪽_어깨", 60, 80)
person_figure.add_point("오른쪽_어깨", 130, 80)
person_figure.add_point("왼쪽_손목", 30, 150)

print("\n--- 정보 확인 ---")
person_figure.show_info()

print("\n--- 거리 계산 ---")
# 두 어깨 사이의 거리 계산
shoulder_dist = person_figure.get_distance("왼쪽_어깨", "오른쪽_어깨")
if shoulder_dist is not None:
    print(f"어깨 사이의 거리: {shoulder_dist:.2f}")

# 어깨와 손목 사이의 거리 계산 (팔 길이)
arm_length = person_figure.get_distance("왼쪽_어깨", "왼쪽_손목")
if arm_length is not None:
    print(f"왼쪽 팔 길이 (어깨-손목): {arm_length:.2f}")