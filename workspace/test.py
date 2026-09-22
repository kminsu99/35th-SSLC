#포함 연산자
# # str
# print("---string---")
# # print("a" in "apple")
# print("ap" not in "apple")
# #문자열속 단어 가능, 문자열속 문자열 불가능 // Trie는 아닌가봄

# #arr
# print("---arr---")
# fruits= ["apple","banana","orange"]
# print('print("apple" in fruits)')
# print("apple" in fruits)
# print('print("Apple" in fruits)')
# print("Apple" in fruits) #대문자 구별함

#식별 연산자

# a, b = 10, 10
# print(a==b)
# print(a is b)
# a = [10]
# c = [10]
# print(a==c)
# print(a is c)

#인덱싱

s = "abcdefgh"
# print(s[:])

#문자열 포맷
# 천 단위 쉼표 표시
# money = 123456748
# print(f"금액 : {money:,}원")
# 숫자형식, 2d, 02d, .2f
# print(f"{ss:.2f}"")


# 자릿수지정 : 서버번호-00X

# server_number = 3
# print(f"서버 번호-{server_number:3d}")

# import random
# random.randint(a, b)	#a ~ b 사이의 정수 난수
# random.uniform(a, b)	#a ~ b 사이의 실수 난수
# random.random()	#0 이상 1 미만의 실수 난수


"""
리스트 인덱스
메서드	설명
append(요소)	리스트 맨 마지막에 하나 추가
pop()	마지막 요소를 지움
extend([요소들])	리스트 마지막에 여러 개 추가
remove('요소값')	해당 요소값 지움
insert(idx, '데이터')	원하는 위치에 자료 삽입
리스트명[n:m]	n부터 m-1까지 데이터 추출
"""


# alerts = ['로그인 실패', '포트 스캔 탐지', '악성 파일 탐지', '비정상 접속', 'DDoS 공격 탐지'] 
# print(alerts)
# # (1) 'SQL Injection 탐지', 'Brute Force 공격 탐지'를 한꺼번에 리스트 마지막에 추가하세요.
# alerts.extend(['SQL Injection 탐지', 'Brute Force 공격 탐지'])
# # (2) alerts 리스트의 마지막 요소를 제거하세요.
# alerts.pop()
# # (3) 'SQL Injection 탐지', 'Brute Force 공격 탐지'를 다시 한꺼번에 추가하세요.
# alerts.extend(['SQL Injection 탐지', 'Brute Force 공격 탐지'])
# # (4) 'SQL Injection 탐지' 요소를 리스트에서 제거하세요.
# alerts.remove('SQL Injection 탐지')
# # (5) alerts 리스트의 네 번째 위치(인덱스 3)에 '랜섬웨어 탐지'를 추가하세요.
# alerts.insert(3, '랜섬웨어 탐지')
# # (6) alerts 리스트에서 3번째 요소부터 5번째 요소까지(인덱스 3~5)를 추출하여 출력하세요.
# print(alerts[3:6])
# print(alerts)

# alerts = ['로그인 실패', '포트 스캔 탐지', '악성 파일 탐지', '비정상 접속', 'DDoS 공격 탐지'] 
# print(alerts)
# alerts.extend(['SQL Injection 탐지', 'Brute Force 공격 탐지'])
# alerts.pop()
# alerts.extend(['SQL Injection 탐지', 'Brute Force 공격 탐지'])
# alerts.remove('SQL Injection 탐지')
# alerts.insert(3, '랜섬웨어 탐지')
# print(alerts[3:6])
# print(alerts)

#Q1
devices = {
    "router": "192.168.1.1",
    "switch": "192.168.1.2",
    "firewall": "192.168.1.254"
}
#A1
print(devices.get('firewall', '-1'))

#Q2
network = {
    "router": {
        "ip": "192.168.1.1",
        "vendor": "Cisco",
        "status": "UP"
    },
    "firewall": {
        "ip": "192.168.1.254",
        "vendor": "Fortinet",
        "status": "UP"
    }
}

#A2
print(network.get('firewall', {}).get('ip', '-2'))

#Q3
alerts = {
    "10.10.10.15": {
        "attack": "Port Scan",
        "severity": "High"
    },
    "10.10.10.20": {
        "attack": "Brute Force",
        "severity": "Critical"
    },
    "10.10.10.30": {
        "attack": "SQL Injection",
        "severity": "High"
    }
}

#Q3-1 "10.10.10.20"을 키로 사용하여 공격 종류를 출력하시오.
#A3-1
print(alerts.get('10.10.10.20', {}).get('attack', '-2'))

#Q3-2 "10.10.10.20"을 키로 사용하여 위험도를 출력하시오.
#A3-2
print(alerts.get('10.10.10.20', {}).get('severity', '-2'))

#Q4
security_logs = {
    "admin": "192.168.1.10",
    "manager": "192.168.1.20",
    "user01": "192.168.1.30"
}

username = "hacker"

"""`username`에 저장된 사용자 이름으로 접속 IP를 검색하시오.

단, 해당 사용자가 등록되어 있지 않은 경우 `"사용자 정보 없음"`이 출력되도록 하시오."""

#A4
print(security_logs.get(username, '사용자 정보 없음'))

#Q5
servers = {
    "web01": "192.168.10.10",
    "web02": "192.168.10.20",
    "db01": "192.168.10.30"
}

server_name = "web03"
"""`server_name`에 저장된 서버 이름으로 IP 주소를 검색하시오.

단, 등록되지 않은 서버인 경우 `"등록되지 않은 서버"`가 출력되도록 하시오."""

#A5
print(servers.get(server_name, '등록되지 않은 서버'))


#A1
print(devices.get('firewall'))
#A2
print(network.get('firewall', {}).get('ip'))
#A3-1
print(alerts.get('10.10.10.20', {}).get('attack'))
#A3-2
print(alerts.get('10.10.10.20', {}).get('severity'))
#A4
print(security_logs.get(username, '사용자 정보 없음'))
#A5
print(servers.get(server_name, '등록되지 않은 서버'))


l1 = ['a', 'b']
s1= {"a", "b"}
d1= {"a":"a1", "b":"b1"}
print('a' in l1)
print('a' in s1)
print(d1.get('a'))