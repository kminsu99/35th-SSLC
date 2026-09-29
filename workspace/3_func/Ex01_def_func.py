# ## 1-1. 함수 정의와 호출 — 서버 경보 발송

# def send_alert(server_name, status):
#     """서버 상태에 따른 경고 메세지를 생성하는 함수"""
#     print(f"[경보] 대상 장비: {server_name}")
#     print(f"[상태] 현재 상황: {status}")
#     print("-" * 20)

# send_alert('prd-db-02', 'CPU과부하')
# print("-" * 40)
# send_alert('prd-web-03', '비정상 로그인 감지')

# ## 1-2. Docstring — 동료가 코드를 열지 않고도 이해하게 만들기

# def check_port_status(port_number):
#     """
#     특정 포트 번호가 보안 정책상 허용된 포트인지 확인하는 함수.

#     Args:
#         port_number (int): 점검할 포트 번호
#     Returns:
#         bool: 허용 여부 (True: 안전, False: 위험)
#     """
#     allowed_ports = [80, 443, 22]
#     return port_number in allowed_ports

# result = check_port_status(80)
# print(f" 허용된 포트번호:{result}")
# print(f" 허용된 포트번호:{check_port_status(8800)}")
# print(f" 허용된 포트번호:{check_port_status(443)}")

# # bool(True, False)의 값으로 True면 안전 출력, else 위험 출력
# print("안전") if (result := check_port_status(2222)) else print("위험")

## 1-3. 스코프(Scope) — 전역 상태를 함수가 실수로 건드리지 않도록

# firewall_policy = "차단"
# def change_policy():
#     firewall_policy = "허용"
#     print(f"함수 안 정책: {firewall_policy}")

# change_policy()
# print(f"최종 정책: {firewall_policy}")

## 1-4. 전역변수를 수정 — 허용 IP 목록 수정
## 전역 변수 allowed_ips
# allowed_ips = ["10.0.0.1", "20.1.1.2"]

# # 전역 변수 allowed_ips에 추가하는 함수를 여기에 작성합니다.
# #----------------------------------------
# def add_ip(ip_addr: str):
#     """
#     매개변수로 넘어온 새 IP주소를 전역변수 allowed_ips에 추가하는 함수

#     Args:
#         ip_addr(str) : 추가할 새로운 아이피 주소
#     Returns:
#         None
#     """
#     allowed_ips.append(ip_addr)
# #----------------------------------------
# # add_ip 함수 호출
# add_ip("10.0.0.2")

# print(f"함수 외부 리스트: {allowed_ips}")   # ['10.0.0.1', '20.1.1.2', '10.0.0.2'] — 같이 바뀜

# def add_ip(new_ip):
#     #--------------------------------------
#     # 허용 IP 목록이 함수 안에 지역변수라면
#     allowed_ips = ["10.0.0.1", "20.1.1.2"]
    
#     allowed_ips.append(new_ip)   
#     print(f"함수 내부 리스트: {allowed_ips}")
#     return allowed_ips
# # add_ip 함수 호출
# allowed_ips = add_ip("10.0.0.2")

# print(f"함수 외부 리스트: {add_ip('10.0.0.2')}")   # ['10.0.0.1', '20.1.1.2', '10.0.0.2'] — 같이 바뀜


# 1-5. 유연하게 매개변수와 반환 
# def filter_high_risk(server_list:list):
#     """위험 수치가 높은 서버 이름만 리스트로 반환"""
#     return [s for s in server_list if s['risk'] > 80]

# inventory = [
#     {"name": "prd-web-01", "risk": 95},
#     {"name": "prd-db-02", "risk": 40},
#     {"name": "prd-bastion-01", "risk": 70},
#     {"name": "prd-db-04", "risk": 80},
# ]
# result = filter_high_risk(inventory)
# print(result )  # [{'name': 'prd-web-01', 'risk': 95} ]


# 1-6. 매개변수 기본값 — 점검 포트 기본값 지정
# def get_cpu_grade(server_name:str, cpu):
#     """
#     서버 이름과 CPU 사용률을 받아 위험 등급 메시지를 반환하는 함수
#     서버 이름(`server_name`)과 CPU 사용률(`cpu`)을 받아서, 사용률에 따라 등급 메시지를 **반환**하는 함수입니다.

#     - 90 이상              → `"🔴 위험"`
#     - 70 이상 90 미만      → `"🟡 주의"`
#     - 70 미만              → `"🟢 정상"`
#     """
#     # pass를 지우고 여기에 작성하세요
#     if cpu >= 90:
#         return f"[{server_name}] 🔴 위험 ({cpu}%)"
#     elif cpu >= 70:
#         return f"[{server_name}] 🟡 주의 ({cpu}%)"
#     else:
#         return f"[{server_name}] 🟢 정상 ({cpu}%)"
# print(get_cpu_grade("prd-web-01", 95))   # [prd-web-01] 🔴 위험 (95%)
# print(get_cpu_grade("prd-db-02",  73))   # [prd-db-02]  🟡 주의 (73%)
# print(get_cpu_grade("stg-api-03", 40))   # [stg-api-03] 🟢 정상 (40%)


# 1-7. 가변 인자 *args — 여러 대의 서버를 한 번에 점검

# def scan_network( ip_addr="127.0.0.1", port_number=80 ):
#     """지정된 IP와 포트를 스캔한다. 포트를 안 적으면 80번을 기본으로 한다."""
#     print(f"{ip_addr}:{port_number} 접속하였습니다")

# scan_network("192.168.0.1", 443)   # 포트: 443

# scan_network("192.168.0.1")        # 포트: 80
# scan_network()        # 포트: 80

# def check_servers( *args ):
#     """입력된 모든 서버를 순회하며 점검"""
#     print(f"총 {len(args)} 대의 서버 점검 시작...")
#     for server in args:
#         print(f"-> {server}")

## 몇 개를 넣어도 상관없음
# check_servers("prd-web-01")
# check_servers("prd-db-02", "prd-api-04", "stg-cache-01")


## 1-8. 가변 인자 **kwargs 
# def update_config( server_name, **options ):
#     """서버의 설정을 가변적으로 업데이트"""
#     print(f"[{server_name}] 설정 변경 내역")
#     for key, value in options.items():
#         print(f"{key}:{value}")

# # 옵션 이름을 내 마음대로 정해서 던질 수 있음
# update_config("prd-web-01", os="Linux", port=80, status="Active")
# update_config("prd-db-02", backup="Daily", zone="Asia-Northeast")





# 1-9. 실수 사례 — 가변 인자 순서 문제

# 실수 1: *args 뒤에는 반드시 이름이 있는 키워드 인자만 올 수 있다
# def scan_server(*targets, port):
#     for t in targets:
#         print(f"{t}:{port} 점검 중")

# 호출 시 port는 반드시 키워드로 지정해야 함
# scan_server("1.1.1.1", "2.2.2.2", 80) # TypeError: 
# scan_server("1.1.1.1", "2.2.2.2", port=80)

# 실수 2: *args를 두 개 이상 선언할 수는 없다
# def check_assets(*ips, *hostnames): -> SyntaxError

# 실수 3: **kwargs 뒤에는 *args가 논리적으로 올 수 없다
# def update_config(**options, *args): -> SyntaxError
# 이유: **kwargs는 '이름표가 붙은 모든 것'을 다 가져가버리기 때문에
# 그 뒤에 이름표 없는 *args가 오는 건 문법적으로 성립하지 않는다
# def update_config(*args, **options):
#     pass
# update_config(name="name1", os="window", port=80, tag="web")

#[ 도전문제 1-A ]
"""
### 문제 1-A. 서버 점검 함수 설계 (*args + 단일 책임 원칙)

아래 요구사항에 맞게 두 개의 함수를 각각 작성하세요.

1. `is_high_risk(risk_score)` : 위험 점수가 80 이상이면 `True`, 아니면 `False` 반환
2. `check_servers(*server_names)` : 여러 서버 이름을 받아 각 서버마다 `"[점검 중] <서버명>"` 출력 후, 점검한 서버 수를 반환

두 함수는 **서로를 호출하지 않습니다** (단일 책임 원칙).
"""
#힌트: *args로 받은 값은 튜플이므로 len()과 for문 모두 사용 가능합니다.
#[ 도전문제 1-A ]
# def is_high_risk(risk_score):
# 	return risk_score >= 80

# def check_servers(*server_names):
#     for server_name in server_names:
#         print(f"[점검 중] <{server_name}>")
#     return len(server_names)
    

# # 실행 예시
# print(is_high_risk(90))   # True
# print(is_high_risk(70))   # False

# count = check_servers("prd-web-01", "prd-db-02", "stg-api-03")
# print(f"점검 완료: {count}대")   # 점검 완료: 3대


# 1-10. 람다(Lambda) — 점검용 일회용 함수
# 일반 함수
# def is_privileged_port(port):
#     return port < 1024
# print(is_privileged_port(22))   # True

# is_privileged_port = lambda port: port<1024
# print(is_privileged_port(22))   # True

# 보안 로그에서 특정 위험 수치 이상만 뽑아낼 때 유용하다.
# risk_scores = [10, 45, 88, 20, 95, 70]

#filter()
# # 80점 이상(고위험)만 필터링
# danger_hosts = list(filter(lambda x: x>=80, risk_scores))
# # danger_hosts = lambda x: x>=0
# print(f"{danger_hosts}")

#map()
# 전체 IP 리스트 앞에 특정 태그를 붙이거나 형식을 바꿀 때 쓴다.
# blocked_ips = ["1.1.1.1", "2.2.2.2", "3.3.3.3"]

# 모든 IP 앞에 [BLOCKED] 태그 붙이기
# blocked_tag = map(lambda x: f"[BLOCKED] {x}", blocked_ips)
# print(list(blocked_tag))

# def add_tag(x):
#     return f"[BLOCKED] {x}"
# blocked_tag = map(add_tag, blocked_ips)
# print(list(blocked_tag))

#sorted()
# 딕셔너리 리스트를 특정 키값(예: 위험 점수) 순으로 정렬할 때 필수다.
servers = [
    {"name": "prd-web-01", "risk": 40},
    {"name": "prd-db-02",  "risk": 90},
    {"name": "prd-api-04", "risk": 75}
]

# risk 점수를 기준으로 내림차순 정렬
# sorted_risk_socore = sorted(servers, key= lambda s: s['risk'], reverse=True)
# print(sorted_risk_socore)
# def get_risk(s):
#     return s['risk']
# sorted_risk_socore = sorted(servers, key= get_risk, reverse=True)
# print(sorted_risk_socore)

# [ 연습문제 ]
"""
—  간단한 보안 리포트 생성

1. 포트 번호 리스트 `raw_data = [22, 80, 443, 8080, 21]` 가 있습니다.
2. `filter`와 `lambda`를 사용해 100번 미만의 잘 알려진 포트만 골라주세요.
3. `map`과 `lambda`를 사용해 골라낸 포트 뒤에 `":OPEN"` 문구를 붙여주세요.
4. 마지막으로 최종 결과를 리스트로 출력하세요.
"""

# raw_data = [22, 80, 443, 8080, 21]

# # -----------------------------------
# # 1. 100 미만 필터링 - 아래 작성합니다.
# filtered_port = list(filter(lambda x: x<100, raw_data))
# print(filtered_port)

# # -----------------------------------
# # 2. 형식 변경 - 아래 작성합니다.
# report = list(map(lambda x: f"{x}:OPEN", filtered_port))
# print(f"보안 점검 리포트: {report}")


"""
### 문제 1-B. lambda + filter / map / sorted 조합

아래 서버 인벤토리 데이터를 활용해 세 가지 작업을 각각 한 줄로 완성하세요.
"""
# # [ 도전 문제 1-B ]
# servers = [
#     {"name": "prd-web-01",  "risk": 55},
#     {"name": "prd-db-02",   "risk": 92},
#     {"name": "stg-api-03",  "risk": 78},
#     {"name": "prd-bastion", "risk": 88},
# ]

# # 1. risk가 80 이상인 서버만 골라내기 (filter + lambda)
# high_risk = filter(lambda x:x['risk']>=80, servers)

# # 2. 모든 서버 이름 앞에 "[점검대상] " 태그 붙이기 (map + lambda)
# tagged = map(lambda x: f"[점검대상] {x['name']}", servers)

# # 3. risk 점수 기준 내림차순 정렬 (sorted + lambda)
# sorted_servers = sorted(servers, key=lambda x:x['risk'], reverse=True)
# print(list(high_risk))
# print(list(tagged))
# print(sorted_servers)

