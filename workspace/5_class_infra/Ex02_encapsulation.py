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

# 여기