# 예전 방식 — 매번 f.close()를 신경써야 함
# f = open("security_log.txt", "w", encoding="utf-8")
# f.write("Admin login detected")
# f.close()
# 3-1. with 블록 — 리소스를 안전하게 닫기

# with open("security_log.txt", "w", encoding="utf-8") as file:
#     file.write("Admin login detected")


# ## 3-2. CSV 파일 쓰기 — 일일 보안 점검 리포트

# import csv

# # 점검 데이터 (헤더 포함)
# report_data = [
#     ["호스트명", "IP_Address", "Status", "Last_Check"],
#     ["prd-web-01", "192.168.1.10", "Safe", "2026-08-29"],
#     ["prd-db-02", "192.168.1.20", "Vulnerable", "2026-08-29"],
#     ["prd-api-04", "192.168.1.30", "Safe", "2026-08-29"]
# ]

# with open("daily_security.csv", "w", newline="",encoding="utf-8-sig") as file:
#     writer = csv.writer(file)
#     writer.writerows(report_data)

# print("CSV 보고서 생성이 완료되었습니다.")


## 3-3. 딕셔너리를 이용한 쓰기(DictWriter) — 침입 탐지 로그
import csv

# 딕셔너리 형태의 IDS/IPS 탐지 로그
# logs = [
#     {"target": "방화벽", "event": "포트 스캔", "severity": "High"},
#     {"target": "IPS", "event": "SQL Injection", "severity": "Critical"},
#     {"target": "WAF", "event": "XSS Attempt", "severity": "Medium"}
# ]

# fieldnames = ["target", "event", "severity"]   # 엑셀의 맨 위 '열 이름' 정의

# with open("daily_log.csv", "w", newline="", encoding="utf-8-sig") as f:
#     writer = csv.DictWriter(f, fieldnames)
#     writer.writeheader()
#     writer.writerows(logs)




# [ 연습 ] daily_security_report.csv 파일을 읽어서 
# Status가 "Vulnerable"인 취약한 호스트를 찾아 
# 호스트 이름과 IP 주소를 출력하는 코드를 아래에 작성하세요
# with open("daily_security.csv", "r", encoding="utf-8-sig") as f:
#     reader = csv.DictReader(f)
#     # print(list(reader))
#     for row in reader:
#         if row.get("Status") == "Vulnerable":
#             # print(row)
#             print(f"host:{row.get('호스트명')}, ip: {row.get('IP_Address')}")






# 3-4. 파이썬 객체로 JSON 만들기 — json.dumps()
import json

# 보안 점검 결과 데이터 (파이썬 딕셔너리)
# scan_result = {
#     "target": "10.0.1.50",
#     "status": "Critical",
#     "open_ports": [22, 80, 443],
#     "is_admin_exposed": True
# }

# [1] 문자열로 변환 (indent는 가독성을 위한 들여쓰기)
# json_str = json.dumps(scan_result, indent=4)
# print(json_str)

"""
dump
dumps <- string
"""
# [2] 파일로 직접 저장하기 — 슬랙 웹훅 전송이나 다음 배치 스크립트가 읽음
# with open("scan_report.json", "w", encoding="utf-8") as f:
#     json.dump(scan_result, f, indent=4)
    

# 3-5. JSON을 파이썬 객체로 읽기 — json.load()
# with open("scan_report.json", "r", encoding="utf-8") as f:
#     file_data = json.load(f)
#     print(f"{file_data.get('target')}")
#     print(f"{file_data['target']}")





# #### [ 도전 문제 3-A ]

# ### 문제 3-A. CSV DictWriter / DictReader 왕복 저장·읽기

# 아래 보안 이벤트 데이터를 CSV 파일로 저장한 뒤, 
# 다시 읽어서 severity가 "Critical"인 항목만 출력하세요.

# ```jsx
# [ 도전 문제 3-A ]
# import csv

# events = [
#     {"host": "prd-web-01",  "event": "Port Scan",    "severity": "High"},
#     {"host": "prd-db-02",   "event": "SQL Injection", "severity": "Critical"},
#     {"host": "stg-api-03",  "event": "XSS Attempt",   "severity": "Medium"},
#     {"host": "prd-bastion", "event": "Brute Force",    "severity": "Critical"},
# ]
# # [ 도전 문제 3-A ]
# fieldnames = ["host", "event", "severity"]
# with open("event.csv", "w", newline="", encoding="utf-8-sig") as f:
#     writer = csv.DictWriter(f, fieldnames)
#     writer.writeheader()
#     writer.writerows(events)
# with open("event.csv", "r", encoding="utf-8-sig") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         if row['severity'] == "Critical":
#             print(f"[Critical] {row['host']} - {row['event']}")

# 1. security_events.csv로 저장 (DictWriter, utf-8-sig, newline="")

# # 2. 저장한 파일을 읽어서 severity가 "Critical"인 항목만 출력 (DictReader)
# ```

# 기대 출력:
# [Critical] prd-db-02 — SQL Injection
# [Critical] prd-bastion — Brute Force

# 💡 힌트: DictWriter 사용 시 fieldnames 리스트를 먼저 정의하고, writeheader()로 헤더를 쓴 뒤 writerows()로 데이터를 저장합니다.



# #### [ 도전 문제 3-B ]

# ### 문제 3-B. JSON 직렬화·역직렬화 + with 블록 안전 처리

# 아래 스캔 결과를 JSON 파일로 저장하고, 다시 읽어서 open_ports 중 1024 미만인 포트만 필터링해 출력하세요.
# 파일 입출력은 반드시 with 블록을 사용하고, 읽기 과정에는 try/except 예외처리를 포함하세요.

# ```jsx
# [ 도전 문제 3-B ]
import json

scan_result = {
    "target": "10.0.1.50",
    "scan_time": "2026-09-27",
    "open_ports": [22, 80, 443, 3306, 8080, 8443],
    "is_admin_exposed": True
}
# [ 도전 문제 3-B ]
# 1. scan_result.json 파일로 저장 (with 블록, indent=2)
# # 2. scan_result.json 파일을 읽어서 1024 미만 포트만 필터링 후 출력
#    (with 블록 + try/except 포함)
# [ 도전 문제 3-B ]
with open("scan_result.json", "w", encoding="utf-8") as f:
    try:
        json_str = json.dump(scan_result, f, indent=2)
    except Exception as e:
        print("file save failed : ", e)
with open("scan_result.json", "r", encoding="utf-8") as f:
    try:
        file_data = json.load(f)
    except:
        print("file load failed : ", e)
    port_list = []
    for port in file_data['open_ports']:
        if port < 1024:
            port_list.append(port)
    print(f"저장 완료: scan_result.json")
    print(f"1024 미만 개방 포트: {port_list}")

# 기대 출력:
# 저장 완료: scan_result.json
# 1024 미만 개방 포트: [22, 80, 443]

# 💡 힌트: json.dump()는 파일 객체에 직접 씁니다. json.load()는 파일 객체를 읽어 파이썬 딕셔너리로 반환합니다. 포트 필터링은 리스트 컴프리헨션이나 filter()로 가능합니다.