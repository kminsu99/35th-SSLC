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
4. 웹 대시보드 : Flask로 저장된 공지 최신순 최대 20건 조회 후 목록 표시, is_watched가 True인 공지는 빨간색 "[주요 제품]" 표시로 강조
5. 자동화 : 수집 스크립트는 schedule 모듈로 일정 주기(예: 10분)마다 자동 실행
"""

"""
문제 해결 가이드
3. Flask 라우팅 및 템플릿 렌더링
    3-1. 데이터 조회: col.find().sort("collected_at", -1).limit(20)로 최신 공지 20건 리스트 변환
    3-2. 템플릿 전달: render_template()으로 공지 리스트를 템플릿에 전달
    3-3. 조건부 표시: 템플릿에서 {% if advisory.is_watched %}로 감시 대상 공지만 빨간색 강조 출력

4. 자동화 스케줄링 및 운영 고려사항
    4-1. 작업 예약: schedule.every(10).minutes.do(collect_advisories)로 주기적 실행 등록
    4-2. 프로세스 분리: 수집(collector.py)과 웹 대시보드(app.py)를 독립 프로세스로 분리 -> 상호 영향 없이 안정적 동작
"""

from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

try:
    client = MongoClient('mongodb://localhost:27017/') # 로컬 PC에서 실행 중인 MongoDB에 연결
    db = client['security_db'] #DB Select
    col = db['security_advisories'] #Collection Select
except Exception as e:
    print("DB ERROR, ", e)
    exit()

# 문제 해결 가이드
# 3. Flask 라우팅 및 템플릿 렌더링
#     3-1. 데이터 조회: col.find().sort("collected_at", -1).limit(20)로 최신 공지 20건 리스트 변환
#     3-2. 템플릿 전달: render_template()으로 공지 리스트를 템플릿에 전달
### 요구사항 4. 웹 대시보드 : Flask로 저장된 공지 최신순 최대 20건 조회 후 목록 표시, is_watched가 True인 공지는 빨간색 "[주요 제품]" 표시로 강조
@app.route("/")
def index():
    ###요구사항 4. 웹 대시보드 : Flask로 저장된 공지 최신순 최대 20건 조회
    advisory_list = list(col.find().sort("collected_at", -1).limit(20))
    return render_template('index.html', advisory_list = advisory_list)

# 문제 해결 가이드
# 4. 자동화 스케줄링 및 운영 고려사항
#     4-2. 프로세스 분리: 수집(collector.py)과 웹 대시보드(app.py)를 독립 프로세스로 분리 -> 상호 영향 없이 안정적 동작
# 개발시 python 실행가능하도록
if __name__ == "__main__":
    app.run(debug=True)