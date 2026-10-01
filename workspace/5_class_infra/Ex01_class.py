# class Server:
#     def __init__(self, name, ip):
#         self.name = name
#         self.ip = ip

#     def info(self):
#         # self가 있어야 '자신'의 name, ip를 꺼내올 수 있습니다
#         print(f"자산명: {self.name}, 주소: {self.ip}")

# # 여기
# web_srv = Server("srv-web-01", "1.1.1.1")
# web_srv.info()
# web_srv.name = "srv-db-01"
# web_srv.ip = "1.1.1.2"
# web_srv.info()
# """output
# 자산명: srv-web-01, 주소: 1.1.1.1
# 자산명: srv-db-01, 주소: 1.1.1.2
# """
# exit()

"""
### 📝 연습문제 — 클래스 · 생성자 · self

**문제 1**  — `FirewallRule` 클래스를 만들고, 
`__init__(self, rule_id, ip, action)`으로 규칙 번호·IP·허용/차단(action)을 저장한 뒤, 
인스턴스를 하나 생성해서 각 속성을 출력하는 코드를 작성해 봅시다.
"""
# class FirewallRule:
#     def __init__(self, rule_id, ip, action):
#         self.rule_id = rule_id
#         self.ip = ip
#         self.action = action
# # 출력확인
# rule1 = FirewallRule(1001, "203.0.113.55", "DENY")
# print(f"규칙 {rule1.rule_id}: {rule1.ip} -> {rule1.action}")

"""
문제 2 — 위 Server 클래스에 restart(self) 메서드를 추가해서, 
호출 시 self.status를 "Restarting"으로 바꾸고 "{name} 서버를 재시작합니다"를
 출력하도록 만들어 봅시다.
"""

# class Server:
#     def __init__(self, name, ip):
#         self.name = name
#         self.ip = ip
#     def restart(self):
#         self.status = "Restarting"
#         print(f"{self.name}서버를 재시작합니다")
# # 출력확인
# web_svr = Server("WEB-01", "192.168.1.10")
# web_svr.restart()   # WEB-01 서버를 재시작합니다
# print(web_svr.status)  # Restarting
# exit()

"""
문제 3  — self는 왜 인스턴스 메서드의 첫 번째 매개변수로 반드시 필요한지, 
그리고 self를 빼고 메서드를 정의하면 실제로 어떤 에러가 나는지 설명해 봅시다.
"""
# class FirewallRule:
#     def __init__(self, rule_id, ip, action):
#         self.rule_id = rule_id
#         ip = ip
#         self.action = action
# # 출력확인
# rule1 = FirewallRule(1001, "203.0.113.55", "DENY")
# print(f"규칙 {rule1.rule_id}: {rule1.ip} -> {rule1.action}")

class Server:
    def __init__(self, name, ip):
        self.name = name
        ip = ip
    def show1():
        print("show1 : ")
    def show2(a):
        print("show2 : ", a)
    def show3(self):
        print("show3 : ", self)
server = Server("srv-db-01", "1.1.1.1")
try:
    server.show1()
except Exception as e:
    print(e)
server.show2()
server.show3()
try:
    print(server.ip)
except Exception as e:
    print(e)
    
"""output
Server.show1() takes 0 positional arguments but 1 was given
show2 :  <__main__.Server object at 0x0000026A01790110>
show3 :  <__main__.Server object at 0x0000026A01790110>
'Server' object has no attribute 'ip'
"""