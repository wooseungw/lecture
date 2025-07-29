# 변수 선언
string_variable = "Hello, World!"
int_number = 1
float_number = 1.0
print("Hello, World!")
print(string_variable)

print(int_number)
print("Integer:", int_number)
print(float_number)

# 타입 확인, 변경
print(type(string_variable))  # <class 'str'>
print(type(int_number))        # <class 'int'>
print(type(float_number))      # <class 'float'>
float_to_int = int(float_number)
print(float_to_int, type(float_to_int))  # 1