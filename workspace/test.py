#35기_파이썬_PBL_ADV01_강민수.py
"""
시스템관리자,
서버증설 -> 담당자마다 제각각 형식으로 서버 정보 기록[IP, port]오타 사고 발생
노션(=서버 자산대장), 터미널에서 번호 입력 -> 서버 등록,조회,상태 변경, 폐기 기능(=서버 자산관리 CLI)
호스트명, IPaddr, port 형식 < 정규표현식 사전 검증 기능+

목표
1. 함수 구현 호출 : CRUD기능을 기능별 모듈화 > 재사용성up
2. 정규표현식(Regex)활용 : 호스트명, IPaddr, port > user input 검증, 무결성 유지
3. Notion API연동 : notion-client SDK 활용, 외부서비스 통신, 데이터 실시간 제어(CRUD)
4. 환경변수 자동화 : python-dotenv, load_dotenv, set_key사용 : 생선된ID -> .env 저장 자동화

요구사항
1. 메뉴 인터페이스 : loop 활용 user에게 menu제공, 입력요청, 0입력시 프로그램 종료
2. 조회(READ) : 현재 DB에 등록된 모든 server's host, ip, port, status, tag를 번호와 함께 출력
3. 생성(CREATE) : input(host, ip, port, status, tag) -> DB에 page추가, 신규 등록시 상태 'Active'고정
4. 수정(UPADTE) : 특정 서버를 번호로 선택하고 상태(select)를 Active/Maintenance/Decommissioned중 하나로 변경(덮어쓰기)
5. 삭제(DELETE) : 선택한 서버를 노션 휴지통(보관처리)으로 이동
6. 입력 검증(VALIDATION) : host, ip, port, status, tag -> 정규표현식으로 형식을 사전확인
"""
# 가이드1. 환경설정 및 API인증
# 가이드1-1. 라이브러리 로드
# notion앱에서 DB페이지 생성 후 ...클릭->개발자포털->신규연결->토큰생성
# page_id는 웹에서 DB페이지주소로 찾기 3e82fc0cd77080a6a884f92780547ee5
# ex)https://app.notion.com/p/3e82fc0cd77080a6a884f92780547ee5?v=3e82fc0cd77080f7be43000c8d15844e
# DB페이지에서 ...클릭->연결->토큰이름선택
import os, re
#python -m pip install notion-client
from notion_client import Client
from dotenv import load_dotenv, set_key, find_dotenv

# 가이드1-2. os.getenv()로 TOKEN, PAGE_ID할당, Client초기화
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")
try:
    notion = Client(auth=NOTION_TOKEN)
except Exception as e:
    print("notion API 호출 실패, ERROR: ", e)
# API TEST
# print(f"TOKEN : {NOTION_TOKEN}\nPAGE_ID : {NOTION_PARENT_PAGE_ID}")

# print("Data Source 개수:", len(response["results"]))
# for item in response["results"]:
#     print("ID:", item["id"])
#     print("OBJECT:", item["object"])
# 가이드1-3. 생성된 DATA_SOURCE_ID는 set_key()로 .env에 자동 저장
DATA_SOURCE_ID = os.getenv("DATA_SOURCE_ID")
if not DATA_SOURCE_ID:
    DATA_SOURCE_ID = response["results"][0]["id"]
    set_key(".env", "DATA_SOURCE_ID", response["results"][0]["id"])
print(f"DATA_SOURCE_ID : {DATA_SOURCE_ID}") #DATA SOURCE ID 출력


# 가이드2. 데이터 유효성 검증(Regex)
HOSTNAME_PATTERN = re.compile(r"^srv-(web|db|was|cache)-\d{2}$")
IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
PORT_PATTERN = re.compile

def validate_hostname(value: str) -> bool:
    return bool(HOSTNAME_PATTERN.match(value))

def validate_ip(value: str) -> bool:
    if not IP_PATTERN.match(value):
        return False
    return all(0 <= int(octet) <= 255 for octet in value.split("."))

def validate_port(value: str) -> bool:
    if not PORT_PATTERN.match(value):
        return False
    return 1 <= int(value) <= 65535

# 가이드3. Notion DB Scheme 설계
"""
title = host
rich_text = ip
number = port
select:Active/Maintenance/Decommissioned = status
multi_select:Web/DB/WAS/Cache = tag
"""

DATA_SOURCE_ID = os.getenv("DATA_SOURCE_ID")
# for row in response["results"]:
#     print("=" * 50)

#     for name, prop in row["properties"].items():
#         print(name, ":", prop)

# 요구사항1. 메뉴 인터페이스 : loop 활용 user에게 menu제공, 입력요청, 0입력시 프로그램 종료
def menu_interface():
    """메뉴 인터페이스 함수"""
    while True:
        print("""
    1. 전체 서버 목록 조회
    2. 신규 서버 등록
    3. 서버 상태 변경 ( Active / Maintenance / Decommissioned )
    4. 서버 폐기
    0. 프로그램 종료
    """)
        user_input = input("입력 : ")
        match user_input:
            case "1":
                print("1. 전체 서버 목록 조회")
                try:
                    db_read()
                except Exception as e:
                    print("DB READ 예외, ", e)
            case "2":
                print("2. 신규 서버 등록")
                try:
                    db_create()
                except Exception as e:
                    print("DB CREATE 예외, ", e)
            case "3":
                print("3")
            case "4":
                print("4")
            case "0":
                break
            case _:
                print("예상못한 입력")
        

# 요구사항2. 조회(READ) : 현재 DB에 등록된 모든 server's host, ip, port, status, tag를 번호와 함께 출력
def db_read():
    """
    db table 전체 조회(READ)함수
    속성(host, ip, port, status, tag)
    """
    response = notion.data_sources.query(data_source_id=DATA_SOURCE_ID)
    for row in response["results"]:
        print("="*50)
        for name, prop in row["properties"].items():
            prop_type = prop["type"]
            match prop_type:
                case "title":
                    value = prop["title"][0]["plain_text"] if prop["title"] else ""
                case "rich_text":
                    value = value = prop["rich_text"][0]["plain_text"] if prop["rich_text"] else ""
                case "number":
                    value = prop["number"]
                case "select":
                    value = prop["select"]["name"] if prop["select"] else ""
                case "multi_select":
                    value = ", ".join(x["name"] for x in prop["multi_select"])
                case _:
                    value = f"[{prop_type}]"
            print(f"{name}: {value}")
    return 0

# 요구사항3. 생성(CREATE) : input(host, ip, port, tag) 
# -> DB에 page추가, 신규 등록시 상태 'Active'고정
#validate_port
#validate_ip
#validate_hostname
def db_create():
    """DB 테이블에 새 page 추가
    호스트명, ip주소, 포트, 태그 입력 (상태는 Active고정)
    validate함수로 각 입력 검증"""
    #각 항목별 input() + valid()
    hostname, ip_addr, port = "", "", ""
    #(r"^srv-(web|db|was|cache)-\d{2}$")
    while not validate_hostname(hostname := input("호스트명 : ")):
        print(f"{hostname} - {validate_hostname(hostname)} <- 형식 오류, ex)srv-(string)-(int)")
    #IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
    while not validate_ip(ip_addr := input("IP주소 : ")):
        print(f"{ip_addr} - {validate_ip(ip_addr)} <- 형식 오류, ex)1.1.1.1")
    while not validate_port(port := input("포트 : ")):
        print(f"{port} - {validate_port(port)} <-형식 오류, ex)(int)")
    print(f"{hostname}, {ip_addr}, {port}")
    return 0
    while True:
        tag = input("태그 : ")
        if tag=="Web" | tag == "DB" | tag == "WAS" | tag == "Cache":
            break
        print("형식 오류")

    notion.pages.create(
        parent = {
                "type": "data_source_id",
                "data_source_id": DATA_SOURCE_ID
        },
        properties = {
            "호스트명" : {
                "title": [
                    {"text" : {"content" : hostname}}
                ]
            },
            "IP주소" : {
                "rich_text" : [
                    {"text" : {"content" : ip_addr}}
                ]
            },
            "포트" : {
                "number" : port
            },
            #신규 등록시 상태 'Active'고정
            "상태" : {
                "select" : [
                    {"name" : "Active"}
                ]
            },
            "태그" : {
                "multi_select" : [
                    {"name" : tag}
                ]
            },
        }
    )


menu_interface()