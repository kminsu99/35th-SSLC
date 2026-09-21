
#-------------------------------------------------------
# 1. list
# 오늘 취약점 스캔을 돌려야 하는 호스트 대기열

scan_queue = ["prd-bastion-01", "prd-db-02", "stg-api-01"] # prd는 Production, stg는 Staging의 약어






# 아래 출력를 했을 때 어떤 결과가 나올지 미리 예측을 하시고 확인하시기 바랍니다.

# 패치 대상 관리
# patch_queue = ["prd-db-02", "prd-api-04"]
# patch_queue.append("stg-cache-01")     # 새 취약 호스트 추가
# patch_queue.insert(0, "prd-bastion-01")  # 치명적 취약점 호스트를 맨 앞으로
# patch_queue.remove("prd-api-04")       # 패치 완료된 호스트 제외
# patch_queue.sort()
# print(patch_queue)

#-------------------------------------------------------
# 2. tuple
#  (프로토콜, 포트, 액션)
#  감사 스크립트가 실행 도중에 방화벽 규칙을 실수로 고치면 안 되므로, 변경 불가로 묶습니다.
firewall_rule = ("TCP", 22, "ALLOW")

# print(f"프로토콜: {firewall_rule[0]}, 포트: {firewall_rule[1]}, 액션: {firewall_rule[2]}")

# firewall_rule[1] = 2222   -> TypeError: 'tuple' object does not support item assignment


#-------------------------------------------------------
# 3. 세트 
names = { "홍길동", "김철수", "이영희", "홍길동"}  # 중복된 이름은 1개만 남음





# — 비인가 개방 포트 탐지
# 이번 스캔에서 실제로 열려있는 포트들
scanned_open_ports = {22, 80, 443, 3306, 6379}

# 보안 정책상 공식 허용된 포트 목록
approved_ports = {22, 80, 443}

# 허용되지 않은데 열려있는 포트 (차집합)
# unauthorized_ports = scanned_open_ports - approved_ports
# 아래 출력를 했을 때 어떤 결과가 나올지 미리 예측을 하시고 확인하시기 바랍니다.
# print(f"비인가 개방 포트: {unauthorized_ports}")  

# 이전 주/이번 주 모두 열려있던 포트 (교집합, 상시 노출 포트)
# 교집합 : intersection() 또는 & 연산자 사용
# 합집합 : union() 또는 | 연산자 사용
# scanned_open_ports = {22, 80, 443, 3306, 6379}
# last_week_open_ports = {22, 443, 6379, 8080}
# persistent_exposed_ports = scanned_open_ports.intersection(last_week_open_ports)
# # 아래 출력를 했을 때 어떤 결과가 나올지 미리 예측을 하시고 확인하시기 바랍니다.
# print(f"2주 연속 노출 포트: {persistent_exposed_ports}") # {22, 443, 6379}


#-------------------------------------------------------
# 4. 딕셔너리

security_event = {
    "cve_id": "CVE-2026-30112",
    "host": "prd-db-02",
    "severity": "HIGH",
    "cvss": 8.1,
    "patched": False
}
print(f"취약점: {security_event['cve_id']} ({security_event['severity']})")



# 패치 완료 처리 및 담당자 추가




# cve_card = {"id": "CVE-2026-11450", "cvss": 9.4}
# print(cve_card.keys())     # dict_keys(['id', 'cvss'])
# print(cve_card.values())   # dict_values(['CVE-2026-11450', 9.4])
# print(cve_card.items())    # dict_items([('id', 'CVE-2026-11450'), ('cvss', 9.4)])



# get() : 없는 필드를 찾을 때 에러 대신 기본값 반환



