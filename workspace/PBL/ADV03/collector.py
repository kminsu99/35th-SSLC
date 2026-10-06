#35기_파이썬_PBL_ADV03_강민수.zip

"""
문제상황
1. 사내 인프라(Linux, Cisco, PostgreSQL) 보안 업데이트 권고 확인 -> KISA 보호나라 사이트에 직접 접속 번거로움
2. 보호나라 '보안공지' RSS(https://www.boho.or.kr/kr/rss.do?bbsId=B0000133) 주기적 수집 -> MongoDB 중복 없이 저장
3. 사내 사용 제품(Linux, Cisco, PostgreSQL) 관련 공지 강조 -> Flask 웹 대시보드 구현
"""

"""
목표
feedparser - RSS 피드 수집 및 항목(entry) 파싱, title/link/pubDate 3개 필드만 제공하는 실제 정부기관 RSS 처리
pymongo - MongoDB 문서 저장 시 중복 데이터 검사 후 삽입
Flask, Jinja2 - 템플릿 조건부 렌더링({% if %})을 이용한 웹 대시보드 구현
"""

"""
요구사항
1. RSS 수집 : feedparser.parse() > 보호나라 보안공지 RSS 파싱, 
    각 공지의 제목(title), 링크(link), 발행일(published) 추출 (description/category 필드 미제공 -> title만으로 판단)
2. 중복 방지 저장 : 동일한 link의 공지가 컬렉션에 이미 있으면 다시 저장하지 않음
3. 감시 대상 제품 판별 : 제목에 "Linux", "Cisco", "PostgreSQL" 중 하나라도 포함 시 -> is_watched 필드 True로 함께 저장
4. 웹 대시보드 : Flask로 저장된 공지 최신순 최대 20건 조회 후 목록 표시, is_watched가 True인 공지는 빨간색 "[주요 제품]" 표시로 강조
5. 자동화 : 수집 스크립트는 schedule 모듈로 일정 주기(예: 10분)마다 자동 실행
"""

"""
문제 해결 가이드
1. RSS 데이터 수집 및 파싱(feedparser)
    1-1. 피드 요청: feedparser.parse(rss_url)로 RSS 가져와 feed.entries 순회
    1-2. 필드 추출: 각 entry에서 entry.title, entry.link, entry.published 꺼내 저장용 딕셔너리 구성 (description 필드 없음 주의)

2. MongoDB 중복 검사 및 저장(pymongo)
    2-1. 컬렉션 연결: MongoClient로 접속 후 db['security_advisories'] 컬렉션 사용
    2-2. 중복 체크: 저장 전 col.find_one({"link": entry.link})로 존재 여부 확인 -> 존재하면 continue로 건너뜀
    2-3. 감시 대상 판별: WATCH_VENDORS = ["Linux", "Cisco", "PostgreSQL"] 리스트 생성 -> any(v in entry.title for v in WATCH_VENDORS)로 is_watched 불리언 필드 계산
"""

#def rss_data_collection_parsing():
import feedparser
from datetime import datetime

#def save_if_not_exist_mongodb(data_list: list):
from pymongo import MongoClient

#main
import schedule, time

# 문제 해결 가이드
# 1. RSS 데이터 수집 및 파싱(feedparser)
#     1-1. 피드 요청: feedparser.parse(rss_url)로 RSS 가져와 feed.entries 순회
#     1-2. 필드 추출: 각 entry에서 entry.title, entry.link, entry.published 꺼내 저장용 딕셔너리 구성 (description 필드 없음 주의)

def rss_feed_collection_parsing():
    """
    RSS 데이터 수집 및 파싱(feedparser)\n
    feedparser.parse(rss_url)로 RSS 가져와 feed.entries 순회\n
    각 entry에서 entry.title, entry.link, entry.published 꺼내 저장용 딕셔너리 구성 (description 필드 없음 주의)\n
    return:
        entry_list []
    """
    
    rss_url = "https://www.boho.or.kr/kr/rss.do?bbsId=B0000133"
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print("RSS feed 수집 실패, ", e)
        return []
    # print(feed)

    ###요구사항 1. RSS 수집 : feedparser.parse() > 보호나라 보안공지 RSS 파싱, 
    ###         각 공지의 제목(title), 링크(link), 발행일(published) 추출 (description/category 필드 미제공 -> title만으로 판단)
    entry_list = []
    for data in feed.entries:
        entry_list.append({"title": data.get("title", ""),
                        "link" : data.get("link", ""),
                        "published" : data.get("published", "0000-00-00"),
                        "collected_at": datetime.now(), #collected_at를 app.py에서 쓰기위해 추가
                        })
    return entry_list

# 문제 해결 가이드
# 2. MongoDB 중복 검사 및 저장(pymongo)
#     2-1. 컬렉션 연결: MongoClient로 접속 후 db['security_advisories'] 컬렉션 사용
#     2-2. 중복 체크: 저장 전 col.find_one({"link": entry.link})로 존재 여부 확인 -> 존재하면 continue로 건너뜀
#     2-3. 감시 대상 판별: WATCH_VENDORS = ["Linux", "Cisco", "PostgreSQL"] 리스트 생성 -> any(v in entry.title for v in WATCH_VENDORS)로 is_watched 불리언 필드 계산

def save_if_not_exist_mongodb(entry_list: list):
    """
    MongoDB 중복 검사 및 저장(pymongo)\n
    DB에 동일 link가 있는지 중복검사 후 저장\n
    감시 대상 판별: WATCH_VENDORS = ["Linux", "Cisco", "PostgreSQL"] 리스트 생성 -> any(v in entry.title for v in WATCH_VENDORS)로 is_watched 불리언 필드 계산\n
    변경사항이 있는지 int 반환\n
    return:
        update_count: int
    """
    update_count = 0
    try:
        client = MongoClient('mongodb://localhost:27017/') # 로컬 PC에서 실행 중인 MongoDB에 연결
        db = client['security_db'] #DB Select
        col = db['security_advisories'] #Collection Select
        #중복아닌 entry만 db에 추가
        ### 요구사항 2. 중복 방지 저장 : 동일한 link의 공지가 컬렉션에 이미 있으면 다시 저장하지 않음
        ### 요구사항 3. 감시 대상 제품 판별 : 제목에 "Linux", "Cisco", "PostgreSQL" 중 하나라도 포함 시 -> is_watched 필드 True로 함께 저장
        WATCH_VENDORS = ["Linux", "Cisco", "PostgreSQL"]
        for entry in entry_list:
            if col.find_one({"link": entry.get("link", "")}): continue
            entry_doc = {
                "title" : entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "collected_at": entry.get("collected_at", ""),
                "is_watched": any(v in entry.get("title", "") for v in WATCH_VENDORS)
            }
            update_count += 1
            col.insert_one(entry_doc)
    except Exception as e:
        print(e)
    return update_count

def collect_advisories():
    """feed 수집, 처리 -> mongodb저장"""
    entry_list = rss_feed_collection_parsing()
    update_count = save_if_not_exist_mongodb(entry_list)
    print(f"{len(entry_list)}개 수집, {update_count}개 업데이트")

# 문제 해결 가이드
# 4. 자동화 스케줄링 및 운영 고려사항
#     4-1. 작업 예약: schedule.every(10).minutes.do(collect_advisories)로 주기적 실행 등록
#     4-2. 프로세스 분리: 수집(collector.py)과 웹 대시보드(app.py)를 독립 프로세스로 분리 -> 상호 영향 없이 안정적 동작
if __name__ == "__main__":
    collect_advisories()
    ### 요구사항 5. 자동화 : 수집 스크립트는 schedule 모듈로 일정 주기(예: 10분)마다 자동 실행
    schedule.every(0.1).minutes.do(collect_advisories)
    while True:
        schedule.run_pending()
        time.sleep(1)