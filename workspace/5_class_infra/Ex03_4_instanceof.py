class BaseServer:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def check(self):
        pass

class WebServer(BaseServer):
    def run_service(self):
        pass


class DBServer(BaseServer):
    def run_service(self):
        pass

web = WebServer("WEB-01", "192.168.1.10")
db = DBServer("DB-01", "192.168.1.20")


# 상속 관계에서 자식 객체가 부모 타입인지, 또는 특정 서버 타입인지 체크할 때



# 실무 활용: 여러 타입이 섞인 서버 리스트에서 웹 서버만 골라 점검



