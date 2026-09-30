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
6. 입력 검증(VALIDATION) : host, ip, port -> 정규표현식으로 형식을 사전확인
"""
# 가이드1. 환경설정 및 API인증
# 가이드1-1. 라이브러리 로드
# notion앱에서 DB페이지 생성 후 ...클릭->개발자포털->신규연결->토큰생성
# page_id는 웹에서 DB페이지주소로 찾기 
# DB페이지에서 ...클릭->연결->토큰이름선택
import os, re
#python -m pip install notion-client
from notion_client import Client
from dotenv import load_dotenv, set_key, find_dotenv

# 가이드1-2. os.getenv()로 TOKEN, PAGE_ID할당, Client초기화
# .env 파일 로드
try:
    
    DOTEN_PATH = find_dotenv()
    load_dotenv(DOTEN_PATH)
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    NOTION_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")
except Exception as e:
    print(".env 에러", e)

# Notion 클라이언트
try:
    notion = Client(auth=NOTION_TOKEN)
except Exception as e:
    print("notion API 호출 실패, ERROR: ", e)


# 가이드2. 데이터 유효성 검증(Regex)
HOSTNAME_PATTERN = re.compile(r"^srv-(web|db|was|cache)-\d{2}$") #ex)srv-web-01
IP_PATTERN       = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$") #ex)192.0.0.111
PORT_PATTERN     = re.compile(r"^\d{1,5}$") #ex)65535

def validate_hostname(value: str) -> bool:
    """호스트명 패턴 유효성 검사"""
    return bool(HOSTNAME_PATTERN.match(value))

def validate_ip(value: str) -> bool:
    """IP주소 패턴 유효성 검사"""
    if not IP_PATTERN.match(value):
        return False
    return all(0 <= int(octet) <= 255 for octet in value.split("."))

def validate_port(value: str) -> bool:
    """포트넘버 패턴 유효성 검사"""
    if not PORT_PATTERN.match(value):
        return False
    return 1 <= int(value) <= 65535

# 가이드3. Notion DB Scheme 설계
#생성 notion.pages.create(parent={"data_source_id":...}, properties=...)
def create_database():
    """
    데이터베이스(DB)를 생성하는 함수.\n
    DB이름 : PBL-ADV01-DB\n
    속성 : 호스트명(title), IP주소(rich_text), 포트(number), 상태(select), 태그(multi_select)\n
    리턴 : (1)정상생성, (0)생성실패\n
    """
    # 데이터베이스 제목
    title = [
        {
            "type": "text",
            "text": {
                "content": "PBL-ADV01-DB"
            }
        }
    ]

    # 컬럼 정의
    properties = {
        "호스트명": {
            "title": {}
        },
        "IP주소": {
            "rich_text": {}
        },
        "포트": {
            "number": {
                "format": "number"
            }
        },
        "상태": {
            "select": {
                "options": [
                    {"name": "Active", "color": "green"},
                    {"name": "Maintenance", "color": "yellow"},
                    {"name": "Decommissioned", "color": "red"},
                ]
            }
        },
        "태그": {
            "multi_select": {
                "options": [
                    {"name": "Web", "color": "gray"},
                    {"name": "DB", "color": "gray"},
                    {"name": "WAS", "color": "gray"},
                    {"name": "Cache", "color": "gray"},
                ]
            }
        },
    }

    # DB 생성
    try:
        db = notion.databases.create(
            parent={
                "type": "page_id",
                "page_id": NOTION_PAGE_ID,
            },

            title=title,

            initial_data_source={
                "properties": properties
            },
        )
        # 생성된 DB에서 Data Source ID 가져오기
        db_info = notion.databases.retrieve(db["id"])
        data_source_id = db_info.get('data_sources', [])[0].get('id', "")
        # 가이드1-3. 생성된 DATA_SOURCE_ID는 set_key()로 .env에 자동 저장
        set_key(DOTEN_PATH, "DATA_SOURCE_ID", data_source_id, quote_mode="never")
    except Exception as e:
        print("DB CREATE FAILED, ", e)
        return 0
    print("NEW DB CREATE")
    return 1

# 요구사항1. 메뉴 인터페이스 : loop 활용 user에게 menu제공, 입력요청, 0입력시 프로그램 종료
def menu_interface():
    """메뉴 인터페이스 함수"""
    while True:
        print("""===========메뉴 인터페이스===========
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
                    DB_READ(DATA_SOURCE_ID)
                except Exception as e:
                    print("DB READ 오류, ", e)
            case "2":
                print("2. 신규 서버 등록")
                try:
                    DB_PAGE_ADD(DATA_SOURCE_ID)
                except Exception as e:
                    print("DB PAGE ADD 예외, ", e)
            case "3":
                print("3. 서버 상태 변경 ( Active / Maintenance / Decommissioned )")
                try:
                    DB_PAGE_UPDATE(DATA_SOURCE_ID)
                except Exception as e:
                    print("DB PAGE UPDATE 예외, ", e)
            case "4":
                print("4. 서버 폐기")
                try:
                    DB_PAGE_DELETE(DATA_SOURCE_ID)
                except Exception as e:
                    print("DB PAGE DELETE 예외, ", e)
            case "0":
                print("0. 프로그램 종료")
                return
            case _:
                print(f"예상못한 입력 : {user_input}")
        
# 요구사항2. 조회(READ) : 현재 DB에 등록된 모든 server's host, ip, port, status, tag를 번호와 함께 출력
#데이터베이스 조회
def DB_READ(data_source_id: str):
    """데이터 베이스를 조회하여 보여주는 함수"""
    try:
        response = notion.data_sources.query(
            data_source_id=data_source_id
        )
    except Exception as e:
        print("response < data_source_id 에러 ", e)

    try:
        print("\n=========== DATABASE INFO ===========")
        print(f"{'호스트명':>9}| {'IP주소':>13} : {'포트':<3}| {'상태':^13}|{'태그':>7}")
        for page in response["results"]:
            properties = page["properties"]
            # 호스트명
            host = properties.get("호스트명", {}).get("title", [{}])[0].get("plain_text", "")
            # IP주소
            ip_addr = properties.get("IP주소", {}).get("rich_text", [{}])[0].get("plain_text", "")
            # 포트
            port = properties.get("포트", {}).get("number")
            # 상태(Active/Maintenance/Decommissioned)
            status = properties.get("상태", {}).get("select", {}).get("name", "")
            # 태그
            tags = [
                tag.get("name", "")
                for tag in properties.get("태그", {}).get("multi_select", [])
            ]
            print(f"{host:>13}| {ip_addr:>15} : {port:<6}| {status:^15}|{tags}"
            )
    except Exception as e:
        print("DB 요소 출력 에러 ", e)

# 요구사항3. 생성(CREATE) : input(host, ip, port, tag) 
# -> DB에 page추가, 신규 등록시 상태 'Active'고정
#validate_hostname
#validate_ip
#validate_port
def DB_PAGE_ADD(data_source_id: str):
    """데이터베이스에 페이지를 추가하는 함수"""
    # host = "srv-db-01"
    # ip_addr = "172.111.111.111"
    # port = 65535
    # tags = ["Web", "WAS"]
    while True:
        host = input("호스트명 : ")
        if validate_hostname(host):
            break
        print("잘못된 호스트명 다시 입력해주세요( ex)srv-db-01 )")
    while True:
        ip_addr = input("IP주소 : ")
        if validate_ip(ip_addr):
            break
        print("잘못된 호스트명 다시 입력해주세요( ex)172.111.111.111 )")
    while True:
        port = input("포트 : ")
        if validate_port(port):
            break
        print("잘못된 포트 다시 입력해주세요( 1~65535 )")
    tags = []
    while True:
        tag = input("태그 입력(0입력시 종료) : ")
        if tag == "0":
            break
        if tag in [ "Web", "DB", "WAS", "Cache"]:
            tags.append(tag)
        else:
            print("잘못된 태그 다시 입력해주세요(Web/DB/WAS/Cache)")
    
    input_data = {
        "호스트명": {
            "title": [
                {"text": {"content": host}}
            ]
        },
        "IP주소": {
            "rich_text": [
                {"text": {"content": ip_addr}}
            ]
        },
        "포트": {
            "number": int(port)
        },
        "상태": {
            "select": {
                #Active/Maintenance/Decommissioned
                #Active 고정
                "name": "Active"
            }
        },
        "태그": {
            "multi_select": [
                {"name": tag}
                for tag in tags
            ]
        }
    }

    try:
        notion.pages.create(
            parent={
                "data_source_id": data_source_id
            },
            properties=input_data
        )
        print("DB ADD SUCCESS")
    except Exception as e:
        print("DB ADD FAILED ", e)

# 요구사항4. 수정(UPADTE) : 특정 서버를 번호로 선택하고 상태(select)를 Active/Maintenance/Decommissioned중 하나로 변경(덮어쓰기)
def DB_PAGE_UPDATE(data_source_id: str):
    """데이터베이스 페이지에서 특정 서버번호의 상태를 변경하는 함수
    server[idx][status] = user_change_status
    """
    result = notion.data_sources.query(
        data_source_id=data_source_id
    )
    pages = result["results"]
    update_idx = int(input('상태를 수정할 서버 번호를 입력하세요 -> '))
    if not update_idx <= len(pages):
        print(f"유효하지 않은 페이지 번호입니다. 입력값[{update_idx}] <= 페이지최대번호[{len(pages)}]")
        return
    page_id = pages[update_idx-1].get('id', "")
    status = ["Active", "Maintenance", "Decommissioned"]
    print("[0] Active / [1] Maintenance / [2] Decommissioned")
    try:
        user_input = int(input("상태입력 : "))
    except Exception as e:
        print("입력값에러 int형변환실패, ", e)
    if not 0 <= user_input <= 2:
        print("유효한 값이 아닙니다.")
        return
    try:
        notion.pages.update(
            page_id=page_id,
            properties = {
                "상태" : {
                    "select" : {"name": status[user_input]}
                }
            }
        )
    except Exception as e:
        print("DB PAGE UPDATE FAILED", e)
        return
    print("수정완료.")
    
# 요구사항5. 삭제(DELETE) : 선택한 서버를 노션 휴지통(보관처리)으로 이동
def DB_PAGE_DELETE(data_source_id: str):
    """유저가 선택한 데이터 베이스 페이지를 아카이브(휴지통)으로 보내는 함수"""
    result = notion.data_sources.query(
        data_source_id=data_source_id
    )
    pages = result["results"]
    delete_idx = int(input('삭제할 페이지 번호를 입력하세요 -> '))
    if not delete_idx <= len(pages):
        print(f"유효하지 않은 페이지 번호입니다. 입력값[{delete_idx}] <= 페이지최대번호[{len(pages)}]")
        return
    try:
        notion.pages.update(page_id=pages[delete_idx-1].get('id', ""), archived=True)
        print("서버가 삭제되었습니다.")
    except Exception as e:
        print("DB PAGE ARCHIVING FAILED, ", e)

#main
#DATA_SOURCE_ID가 env에 있는지 확인 후 없으면 DB생성
#init DB
if not (DATA_SOURCE_ID := os.getenv("DATA_SOURCE_ID")):
    if not create_database():
       #.env에서 DATA_SOURCE_ID 찾지못함, create_database()실패
       # 둘다 충족시 프로그램 종료
       raise Exception("DB CREATE/SEARCH FAILED")
    load_dotenv(DOTEN_PATH)
    DATA_SOURCE_ID = os.getenv("DATA_SOURCE_ID")
#메뉴 인터페이스 실행
menu_interface()