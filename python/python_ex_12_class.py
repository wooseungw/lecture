class ClassName:
    # 초기화 메서드 (객체 생성 시 호출)
    def __init__(self, param1, param2):
        # 인스턴스 속성 (객체별 데이터)
        self.attribute1 = param1
        self.attribute2 = param2

    # 메서드 (객체의 기능)
    def method_name(self, param):
        # 메서드가 수행할 코드
        print(f"메서드 호출됨: {self.attribute1}, {param}")
        
# 클래스 이름()을 호출하여 객체(인스턴스)를 생성합니다.
my_object = ClassName("값1", "값2")

# 점(.) 연산자를 사용하여 객체의 속성과 메서드에 접근합니다.
print(my_object.attribute1)
my_object.method_name("전달값")