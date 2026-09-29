#35기_파이썬_PBL_CORE02_강민수
"""
취약점 스캐너가 작업 폴더에 "vuln_scan.log"파일 생성
이 로그 방치시 다음 스캔 결과와 뒤섞임. 따라서 스캔이 끝난 로그는 즉시 "archive"폴더로 옮겨 보관
로그에 나열된 열린 포트 중 사내 보안 정책상 "안전 포트"로 등록되지 않은 포트만 골라, 
엑셀(CVS) 취약점 리포트와 시스템 연동용 JSON 알림 파일로 변환하는 자동화

목표
함수 : docstring(설명,주석), tuple
filesys : pathlib(mkdir, isExist), glob(확장자search), shutil(파일이동)
데이터 직렬화(Serialization) : 파이썬 객체를 CSV와 JSON표준 포맷으로 변환 후 저장
고급 필터링 : filter(), lambda 조합, 데이터 필터링 추출
데이터 타입 변환 : 파이썬의 None이 JSON의 null로 변환, 데이터 호환성

요구사항
1. 로그 아카이빙 : 현재 폴더에 "vuln_scan.log"파일o, "archive"폴더x "pathlib"으로 생성 후
"shutil.move()"로 로그 파일을 "archive"폴더로 이동
2. 함수 설계 : "is_safe_port(port)"함수 제작, 함수 내부에는 Tuple형태 whitelist선언, 함수 docstring포함
safe_ports = (22, 80, 443)
3. 로그 파싱 : "archive"폴더로 이동한 로그 파일을 읽어 줄 단위로 분리, 
"Port: "로 시작하는 줄에서 포트번호만 정수(int)추출 (Split활용, len체크로 idx error방지)
4. 필터링 로직 : 일반적 반복문 대신 "lambda", "filter()"를 사용 하여 whitelist에 없는 위험포트 색적
5. 다중 포맷 리포팅
    CSV  : "vulnerable_ports.csv"파일로 저장(header : "Detected_Port", "Severity") -- 값은 "Critical"고정
    JSON : "vulnerability_alert.json"파일로 저장(들여쓰기 4칸)
6. 데이터 값 제어 : JSON 데이터의 "Assigned_engineer" 필드를 "None"으로 설정, 저장시 "null"로 치환 확인
"""

#사전 준비 : "vuln_scan.log"파일 생성
from pathlib import Path

#실무형 취약점 스캔 로그 데이터 생성
log_data = """Scan Time: 2026-09-07 02:00:11
Target: 10.0.2.15
Port: 21 STATUS: OPEN
Port: 22 STATUS: OPEN
Port: 443 STATUS: OPEN
Port: 3389 STATUS: OPEN
Port: 80 STATUS: OPEN
Port: 8080 STATUS: OPEN"""

if not Path("vuln_scan.log").exists():
    Path("vuln_scan.log").write_text(log_data, encoding="utf-8")
print("취약점 스캔 로그(vuln_scan.log) 생성 완료!")

#######################################################################################################

#아카이빙: "archive_dir.mkdir(exist_ok=True)"로 폴더준비, "shutil.move(str(원본), str(대상폴더))"로 로그 이동
# 1. 로그 아카이빙 : 현재 폴더에 "vuln_scan.log"파일o, "archive"폴더x "pathlib"으로 생성 후
archive_dir = Path("archive")
archive_dir.mkdir(exist_ok=True)
# 1. "shutil.move()"로 로그 파일을 "archive"폴더로 이동
import shutil
log_file = Path("vuln_scan.log")
if not Path(archive_dir/log_file):
    shutil.move(log_file, archive_dir)

#######################################################################################################

#2. 함수 설계 : "is_safe_port(port)"함수 제작, 함수 내부에는 Tuple형태 whitelist선언, 함수 docstring포함
safe_ports = (22, 80, 443)
def is_safe_port(port):
    """
    port가 화이트리스트(safe_ports)에 등록된 안전한 port인지 검증하는 함수.
    화이트리스트(safe_ports)에 등록된 port일 경우 True를 반환한다.
    Args:
        int
    return:
        boolean
    """
    return port in safe_ports

# print(is_safe_port(22), is_safe_port.__doc__) #is_safe_port 함수 test

#######################################################################################################

#"archive/vuln_scan.log open" as file, read
log_ports = []
with open(f"{archive_dir}/{log_file}", "r") as file:
    #3. 로그 파싱 : "archive"폴더로 이동한 로그 파일을 읽어 줄 단위로 분리
    # := 대입 + 값반환 c에서 ((line = readline())
    while line := file.readline():
        if line.find("Port: ") == -1:
            continue
        #3. "Port: "로 시작하는 줄에서 포트번호만 정수(int)추출 (Split활용, len체크로 idx error방지)
        if len(line[6:]):
            port = line[6:].split(" ", 1)[0]
        try:
            int(port)
            log_ports.append(int(port))
        except Exception as e:
            print("port 파싱 오류", e)
            break
# file pointer의 커서개념만 생각나고 어떻게 쓰는지 까먹어서 적은코드
# with open(f"{archive_dir}/{log_file}", "r") as file:
    # log_data = file.read()
# cursor = 0 #cursor
# while cursor < len(log_data): #커서가 문자열 끝 도달전까지 참
#     cursor += log_data[cursor:].find("Port: ") #커서위치 = :Port: "시작
#     #3. 로그 파싱 : "archive"폴더로 이동한 로그 파일을 읽어 줄 단위로 분리
#     line = log_data[cursor:].split("\n", 1)[0]
#     cursor += len(line) #커서위치 = Port로 구분한 줄 다음시작위치
#     #문자열처럼 인식되려면 str[cursor:], ":"를 붙여야함.
#     #split("구분자", "구분횟수")
#     #split시 배열처럼 동작함 첫번째 원소만 뽑으려면 [0]
#     #3. "Port: "로 시작하는 줄에서 포트번호만 정수(int)추출 (Split활용, len체크로 idx error방지)
#     # port = log_data[cursor+6:].split(" ", 1)[0]
#     # if len(line[6:]):
#     #     port = line[6:].split(" ", 1)[0]
#     # try:
#     #     int(port)
#     #     log_ports.append(int(port))
#     # except Exception as e:
#     #     print("port 파싱 오류", e)
#     #     break

#######################################################################################################

# 4. 필터링 로직 : 일반적 반복문 대신 "lambda", "filter()"를 사용 하여 whitelist에 없는 위험포트 색적
# lambda 매개변수: 반환값
# filter(조건함수, 대상)
# 대상"log_ports[요소]" -> 매개변수"port = log_ports[요소]" ->
# -> 반환값"not is_safe_port(port=log_ports[요소])"" -> 참이면 list에 매개변수port추가
warning_ports = list(filter(lambda port: not is_safe_port(port), log_ports))
# print(warning_ports) #print warning_ports

#######################################################################################################

# 5. 다중 포맷 리포팅
#     CSV  : "vulnerable_ports.csv"파일로 저장(header : "Detected_Port", "Severity") -- 값은 "Critical"고정
import csv

# CSV_DATA = "Detected_Port,Severity\n"
# for port in warning_ports:
#     CSV_DATA += f'{port},Critical\n'
# with open("vulnerable_ports.csv", "w", encoding="utf-8") as file:
#     file.write(CSV_DATA)
# print(CSV_DATA)
field_names = ["Detected_Port", "Severity"]
with open("vulnerable_ports.csv", "w", newline="",encoding="utf-8") as file:
    writer = csv.DictWriter(file, field_names)
    writer.writeheader()
    for port in warning_ports:
        writer.writerow({
            "Detected_Port": port,
            "Severity": "Critical",
        })


#######################################################################################################

#     JSON : "vulnerability_alert.json"파일로 저장(들여쓰기 4칸)
# 6. 데이터 값 제어 : JSON 데이터의 "Assigned_engineer" 필드를 "None"으로 설정, 저장시 "null"로 치환 확인

import json
JSON_DATA = [
    {"Assigned_engineer": None},
    ]
#json.dump(데이터, 파일, ensure_ascii=False, indent=4)
#ensure_ascii한글을 그대로 저장
with open("vulnerability_alert.json", "w", encoding="utf-8") as file:
    json.dump(JSON_DATA, file, indent=4)