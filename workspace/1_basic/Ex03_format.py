


# -----------------------------------------
#  1.  문자열 포맷
# name = "홍길동" 
# age = 20 
# print(f"이름: {name}, 나이: {age}")

# print("이름: {}, 나이: {}".format(name, age))
# print("이름2: {0}, 나이: {1}".format(name, age))
# print("이름3: {1}, 나이: {0}".format(name, age))

# print("이름: %s, 나이: %d" % (name, age))

# print("이름:", name, ", 나이:", age) # format 형식 출력 아님


# [1-1]. 문자열 포맷팅
user = "홍길동"
target = "192.168.10.5"
action = "Login Failed"
# [보안알림] 사용자 홍길동가 192.168.10.5 서버에 Login Failed 하였습니다.
# print(f"[보안알림] 사용자 {user}가 {target} 서버에 {action} 하였습니다.")
# print("[보안알림] 사용자 {}가 {} 서버에 {} 하였습니다.".format(user, target, action))
# print("[보안알림] 사용자 %s가 %s 서버에 %s 하였습니다." % (user, target, action))





# [1-2]. 숫자 포맷팅
# age = 25
# score = 95
# print(f"나이: {age}세")
# print(f"점수: {score}점")

# 천 단위 쉼표 표시

# money = 123456748
# print(f"금액 : {money:,}원")


# 자릿수지정 : 서버번호-00X

# server_number = 3
# print(f"서버 번호-{server_number:3d}")
# print(f"서버 번호-{server_number:03d}")


# [1-3]. 실수 포맷팅

# cpu_usage = 33.3456
# print(f"CPU 사용률 : {cpu_usage}%")
# print(f"CPU 사용률 : {cpu_usage:.2f}%")

# mem_usage = 84.78978
# #소숫점 1자리 출력
# print(f"MEM 사용률 : {mem_usage:.1f}%") #자동 반올림



#--------------------------------
# 2. 입력받기

# name = input("이름을 입력하세요: ")
# age = int(input("나이를 입력하세요: "))
# height = float(input("키를 입력하세요: "))
# print(f"이름: {name}, 나이: {age}, 키: {height}")

'''
    [연습문제]
    서버이름(web)과 서버번호(1)를 입력받아 아래와 같이 출력되도록 하세요.

    [출력결과]
    서버: web-0001
'''

# server_name = input("Input Server Name : ")
# server_number = int(input("Input Servere Number : "))
# print(f"서버: {server_name}-{server_number:04d}")



#--------------------------------
# 3. 임의의 수

import random

server_id = random.randint(1,45)
print(f"server_id : {server_id:02d}")

server_usage = random.uniform(1,45)
print(f"server_usage : {server_usage:02f}")

