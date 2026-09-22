## 4-1. List Comprehension — 위험 CVSS만 추출

cvss_scores = [4.2, 9.8, 6.5, 7.1, 2.0, 9.1]

# 일반 반복문 버전
# critical_scores = []
# for score in cvss_scores:
#     if score >= 7.0:
#         critical_scores.append(score)


# critical_scores = [score for score in cvss_scores if score >= 7.0]

# print(f"1. 위험 등급(HIGH 이상) CVSS: {critical_scores}")





## 4-2. Set Comprehension — 유니크 공격자 IP 추출

raw_attacker_logs = ["203.0.113.55", "203.0.113.99", "198.51.100.7", "203.0.113.55"]
# set_data = set(raw_attacker_logs)
# print(set_data)

# print(raw_attacker_logs[0].split('.'))
# print(raw_attacker_logs[0].split('.')[0])

# unique_attackers = {ip for ip in raw_attacker_logs if ip.split('.')[0] == '203'}
# print(f"고유 공격자 IP : {unique_attackers}")






## 4-3. Dict Comprehension — 서버명 → IP 매핑 생성

# servers = ["WEB", "DB", "PROXY"]

# server_map = { server:f"10.0.0.{idx+1}" for idx, server in enumerate(servers)}
# print(server_map)





#============================================
###  연습문제 
'''
[ 문제 1 ] — 
    ports = [22, 80, 443, 3306, 8080, 6379, 21] 리스트가 있습니다. 
    List Comprehension으로 1024 미만(잘 알려진 포트, well-known port)인 값만 뽑아 새 리스트를 만들어 봅시다.
'''
ports = [22, 80, 443, 3306, 8080, 6379, 21]

well_known_port = [port for port in ports if port<1024]
print(well_known_port)


'''
[문제 2] — 
    아래 CVE 리스트가 있습니다. 
    Set Comprehension을 사용해서 패치가 안 된(patched: False) CVE ID만 담은 Set을 만들어 봅시다.
'''
cve_list = [
    {"id": "CVE-2026-1001", "patched": False},
    {"id": "CVE-2026-1002", "patched": True},
    {"id": "CVE-2026-1003", "patched": False},
]
# 값은 동일하지만 순서가 주석과 다르게 나올 수 있습니다.
cve_id_unpatched = {cve.get('id', '-1') for cve in cve_list if not cve.get('patched', '-1')}
print(cve_id_unpatched)


'''
[문제 3 ] — 
    아래 코드가 생성하는 딕셔너리의 결과를 먼저 예측해보고, 실행해서 확인해 봅시다.
'''
hosts = ["bastion", "db", "cache"]
risk_map = {h: ("HIGH" if h == "db" else "LOW") for h in hosts}
print(risk_map) # 결과를 예측하세요


