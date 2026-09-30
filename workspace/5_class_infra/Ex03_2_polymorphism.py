from abc import ABC, abstractmethod

class BaseServer(ABC):
    def __init__(self, name: str, ip: str):
        self.name = name
        self.ip = ip
        self.status = "Unknown"

    @abstractmethod
    def check(self):
        pass  # 자식 클래스가 반드시 재정의해야 하는 추상 메서드

    def power_on(self):
        print(f"{self.name} 서버 전원 켜기")
        self.status = "Running"


class WebServer(BaseServer):
    # 추상 메서드 구현
    def check(self):
        print(f"{self.name} 웹 서버 점검...")

    def run_service(self):
        print("웹 서비스(80/443) 가동!")


class DBServer(BaseServer):
    def check(self):
        print(f"{self.name} DB 서버 점검...")

    def run_service(self):
        print("DB 서비스(3306) 가동!")

# 여기