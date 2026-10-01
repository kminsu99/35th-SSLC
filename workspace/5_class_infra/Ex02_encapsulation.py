# class SecuritySystem:
#     def __init__(self):
#         self.__admin_pw = "secret123"  # __를 붙여 외부 접근 차단 (캡슐화)
#         self.admin_name = "admin"

#     def login(self, input_pw):
#         if input_pw == self.__admin_pw:
#             print("로그인 성공")
#         else:
#             print("접근 거부")

#     def __internal_check(self):
#         # 이름 앞에 __가 붙으면 클래스 내부에서만 호출 가능합니다
#         print("내부 점검 중")

# # 여기
# security = SecuritySystem()
# print(security.admin_name) #admin
# security.login("!@#")
# security.login("secret123")
# # print(security.__admin_pw)


"""
문제 1 — LogEntry 클래스를 만들고, __init__(self, ip, level, message)로
 로그 한 줄의 핵심 정보(IP, 로그 레벨, 메시지)만 추상화해서 저장하는 코드를 작성해 봅시다.
"""

# class LogEntry:
#     def __init__(self):
#         pass
#     def save(self, ip, level, msg):
#         self.ip = ip
#         self.level = level
#         self.msg = msg
# log = LogEntry()
# log.save("1.1.1.1", "Critical", "message-message")
# print(f"{log.ip}, {log.level}, {log.msg}")

"""
문제 2 — 위 SecuritySystem 클래스에 
change_password(self, old_pw, new_pw) 메서드를 추가해서, 
old_pw가 맞을 때만 self.__admin_pw를 new_pw로 바꾸도록 만들어 봅시다.
"""
class SecuritySystem:
    def __init__(self):
        self.__admin_pw = "secret123"  # __를 붙여 외부 접근 차단 (캡슐화)
        self.admin_name = "admin"

    def login(self, input_pw):
        if input_pw == self.__admin_pw:
            print("로그인 성공")
        else:
            print("접근 거부")

    def __internal_check(self):
        # 이름 앞에 __가 붙으면 클래스 내부에서만 호출 가능합니다
        print("내부 점검 중")
    def change_password(self, old_pw, new_pw):
        if old_pw == self.__admin_pw:
            self.__admin_pw = new_pw
            print("changed")
        else:
            print("failed")

# 출력

security = SecuritySystem()
security.change_password("wrong", "new_secret")   # 실패
security.change_password("secret123", "new_secret")  # 성공


"""
문제 3 — 관리자 비밀번호, API 키 같은 민감한 값을 클래스 안에서 
다룰 때 왜 __를 붙여 캡슐화하는 습관이 필요한지, 그리고 이것이 완벽한 보안 대책은 
아닌 이유를 함께 설명해 봅시다.
"""

"""
__은 직접 참조 어렵게
완벽한 접근/변조 차단은 아니기때문.
"""