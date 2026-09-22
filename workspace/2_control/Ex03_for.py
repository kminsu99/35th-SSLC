## 3-1. range() — 포트 스캔 시뮬레이션
# sum = 0
# for i in range(1,6):
#     sum += i
#     print(sum)
# print(f'합계 : {sum}')

# for i in range(10):
#     print(i)

# dan = int(input("input dan : "))
# for n in range(1,10):
#     print (f'{n} * {dan} = {dan * n}')



# 지정 범위만큼 반복문 실행
# for n in range(10):
# 	print(n)

# 21~25번 포트를 하나씩 점검
# for port in range(21, 26):
#     print(f"포트 {port} 점검 중...")
    
# 100단뒤 포트를 점검
# for port in range(1, 1000, 100):
#     print(f"포트 {port} 점검 중...")

## 3-2. 리스트 순회 — 스캔 대상 호스트 점검
# scan_queue = ["prd-bastion-01", "prd-db-02", "prd-api-04"]

# print("--- 전수 조사 시작 ---")
# for host in scan_queue:
#     print(f"[점검 중] 대상: {host} ... 연결 확인 완료")
# print("--- 점검 종료 ---")


## 3-3. 딕셔너리 순회 — CVE 카드 일괄 점검
# cve_inventory = {
#     "CVE-2026-30112": {"host": "prd-db-02", "cvss": 8.1, "patched": False},
#     "CVE-2026-11450": {"host": "prd-api-04", "cvss": 9.4, "patched": True},
# }
# for key, value in cve_inventory.items():
#     print(f"{key} - {value}")
# for cve_id, detail in cve_inventory.items():
#     status = "패치완료" if detail["patched"] else "미패치"
#     print(f"{cve_id} | 호스트: {detail['host']} | CVSS: {detail['cvss']} | {status}")


## 3-4. enumerate() — 로그 줄 번호와 함께 위험 패턴 탐지
# auth_logs = ["Login success", "Failed password for root", "Logout", "Failed password for admin"]

# for idx, item in enumerate(auth_logs):
#     print(f"{idx} , {item}")


# for line_num, log in enumerate(auth_logs, start=1):
#     if "Failed" in log:
#         print(f"[경고] {line_num}번째 줄에서 보안 위협 감지: {log}")



#============================================
'''
[ 문제 1 ]— 
    for문과 range()를 사용해서 1번부터 20번 포트 중 
    '짝수 번호'만 "포트 2 스캔 예정", "포트 4 스캔 예정" 형태로 출력해 봅시다. 
    (range()의 세 번째 인자, 간격을 활용하세요.)
'''
# for port in range(2, 21, 2):
#     print(f"포트 {port} 스캔 예정")


'''
**문제**  — `servers = ["WEB-01", "DB-01", "DB-02", "APP-01"]` 리스트가 있습니다. 

순회하면서 이름에 `"DB"`가 포함된 서버의 개수를 세어 `"DB 서버 총 2대"`처럼 출력해 봅시다.
'''
# servers = ["WEB-01", "DB-01", "DB-02", "APP-01"]
# server_count = 0
# for server_name in servers:
#     if(server_name.find("DB") != -1):
#         server_count+=1
# print(f"DB 서버 총 {server_count}대")


'''
[ 문제 3 ]— 
    auth_logs = ["Login success", "Failed password", "Failed password", "Login success", "Failed password"] 리스트가 있습니다. 
    enumerate()를 사용해서 "Failed"가 포함된 로그의 **줄 번호와 내용**을 함께 출력하고, 
    반복이 끝난 뒤 총 실패 횟수도 출력해 봅시다.
'''
# auth_logs = ["Login success", "Failed password", "Failed password", "Login success", "Failed password"]
# Failed_count = 0
# for line, details in enumerate(auth_logs, start=1):
#     print(f'{line} : {details}')
#     if(details.find("Failed") != -1):
#         Failed_count += 1
# print(f"Failed Count : {Failed_count}")


"""
### 문제 1. 딕셔너리와 리스트를 조합해 보안 점검 정보 출력하기

딕셔너리와 리스트를 조합하면 여러 서버의 보안 점검 정보를 저장할 수 있습니다. 
아래 실행 결과처럼 출력되도록 빈칸에 반복문과 `print()` 함수를 작성해 보세요.

output
# 보안 점검 대상 서버
WEB-01 443번 포트
WEB-02 80번 포트
DB-01 3306번 포트
WAS-01 8080번 포트
"""

# 보안 점검 대상 서버 목록
# servers = [
#     {"name": "WEB-01", "port": 443},
#     {"name": "WEB-02", "port": 80},
#     {"name": "DB-01", "port": 3306},
#     {"name": "WAS-01", "port": 8080}
# ]
# print("# 보안 점검 대상 서버")

# for server in servers:
#     print(f"{server.get('name','-1')} {server.get('port', -1)}번 포트")

"""
### 문제 2. 네트워크 로그에서 포트 번호별 접속 횟수 세기
"""

# 네트워크 접속 로그에서 확인된 포트 번호
# ports = [80, 443, 22, 80, 3306, 443, 22, 80, 8080, 443,
#          22, 3306, 80, 443, 8080, 22, 80, 443, 3306, 22]

# counter = {}

# for port in ports:
#     counter[port] = ports.count(port)
# # 최종 출력
# print(counter)


"""
### 문제 3 네트워크 장비 정보를 자료형에 따라 출력하기 `type()` 활용

네트워크 장비의 정보는 문자열, 숫자, 딕셔너리, 리스트 등 다양한 자료형으로 저장할 수 있습니다.

`type()`을 활용해 자료형을 구분하고, **딕셔너리와 리스트 내부의 데이터까지 출력**해 보세요.
"""

# 네트워크 장비 정보를 저장합니다.
network = {
    "hostname": "R1",
    "ip": "192.168.10.1",
    "port": {
        "http": 80,
        "https": 443
    },
    "protocol": ["TCP", "UDP", "ICMP"]
}

# for 반복문을 사용합니다.
for key in network:
    # TODO: 여기에 코드를 작성하세요.
    # (network[key]가 dict이면 그 내부를 한 번 더 반복,
    #  list이면 그 내부를 한 번 더 반복,
    #  그 외에는 바로 출력)
    if(type(network[key]) == type({})):
        for key2 in network[key]:
            print(f"{key2} : {network[key][key2]}")
    elif(type(network[key]) == type([])):
        for key2 in network[key]:
            print(f"{key} : {key2}")
    else:
        print(f"{key} : {network[key]}")
    
    
