#35기_파이썬_PBL_BASIC01_강민수
"""
CVE(취약점)목록관리, Critical Asset(핵심자산) 여부에 따라 우선순위 판단
신규 취약점 발견시 리스트 갱신
각 취약점의 패치 여부, 위험도(CVSS Score)즉시 파악 가능

요구사항
1. .env file, SCANNER_NAME READ, but is not exist -> Local-Scanner
2. vuln_assests : 각 취약점 정보 dict으로 갖는 list
3. ciritcal_hosts : 변경불가능(튜플)한 핵심 자산 호스트명 목록
4. user input : 신규CVE ID, 대상 호스트명 -> list에 반영
5. 상태 업데이트 : 특정 인덱스의 취약점 패치(patched)상태값 직접 수정
6. 수치 시뮬 : random -> 실수형(float) uniform, CVSS점수 (0~10)생성
7. 동적 출력 : f-string 사용, 소숫점 제한 출력 .2f
"""

import os
import random
from dotenv import load_dotenv

load_dotenv()
#1. .env file, SCANNER_NAME READ, but is not exist -> Local-Scanner
Scanner_Name = os.getenv("SCANNER_NAME", "Local-Scanner")

#2. vuln_assests : 각 취약점 정보 dict으로 갖는 list
vuln_assets    = [
    {"cve":"CVE-2024-1001", "host":"WEB-01", "patched": False},
    {"cve":"CVE-2024-1002", "host":"DB-01", "patched": True},
    ]
#3. ciritcal_hosts : 변경불가능(튜플)한 핵심 자산 호스트명 목록
critical_hosts = ("WEB-01", "DB-01")

#4. user input : 신규CVE ID, 대상 호스트명 -> list에 반영
new_cve = input("추가할 CVE ID : ")
new_host   = input("추가할 대상 호스트 : ")
print()
vuln_assets.append({"cve":new_cve, "host":new_host})

#5. 상태 업데이트 : 특정 인덱스의 취약점 패치(patched)상태값 직접 수정
vuln_assets[0]["patched"] = True

#6. 수치 시뮬 : random -> 실수형(float) uniform, CVSS점수 (0~10)생성
cvss_score = random.uniform(0,10)

#7. 동적 출력 : f-string 사용, 소숫점 제한 출력 .1f
print(f"총 {len(vuln_assets)}건의 취약점에 대한 패치 점검을 수행합니다.")
for vuln in vuln_assets:
    print("-" * 51)
    print(f"[스캐너: {Scanner_Name}] {vuln.get('cve')} ({vuln.get('host')}) 패치 상태: {vuln.get('patched')}")
    print(f"핵심 자산 여부: {vuln.get('host') in critical_hosts}", end="")
    if not vuln.get('host') in critical_hosts:
        print(f" / 현재 위험도: {cvss_score:.1f}", end="")
        cvss_score = random.uniform(0,10) #입력 여러개 받을 경우를 위해 임의값 재설정
    print()
