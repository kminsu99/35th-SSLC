class Server:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def info(self):
        # self가 있어야 '자신'의 name, ip를 꺼내올 수 있습니다
        print(f"자산명: {self.name}, 주소: {self.ip}")
        
# 여기
