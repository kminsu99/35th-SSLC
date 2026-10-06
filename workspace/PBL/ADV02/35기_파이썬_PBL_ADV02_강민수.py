#35기_파이썬_PBL_ADV02_강민수.py
#결과물 : .py코드

"""
문제상황
1. 매일 아침 보안 뉴스 사이트에 직접 접속해 최신 기사확인
2. 위험도가 높은 기사 엑셀 정리, 메일 보고
3. 기사 누락, 보고 지연 발생. -> 자동화 요구
4. 최신 보안뉴스 웹에서 수집 -> 위험도별 색 태그 -> 엑셀 리포트 저장 -> 엑셀파일첨부 HTML EMAIL 발송
"""

"""
목표
request, BeautifulSoup -  웹페이지에서 필요한 데이터(제목, 링크)구조적 추출
openpyxl - 수집한 데이터 엑셀 파일 저장, 조건에 따라 셀 서식(배경색, 글자색)다르게 적용
smtplib, email.mime - 파일이 첨부된 HTML 이메일 구성, 계정 정보 .env로 안전하게 관리1
"""

"""
요구사항
1. 데이터 수집 : request, BeautifulSoup > 보안뉴스사이트에서 기사 제목,링크 최소 5개이상 수집
2. 위험도 분류 : 제목에 "취약점", "유출", "해킹"등의 키워드 포함 시 -> 위험도 "High", 그외 "Noraml"
3. 엑셀 저장 : 순번,제목,링크,위험도 컬럼으로 엑셀 파일 생성, 헤드행 배경색 강조, 위험도 "High"행 글자 빨간색,Bold체
4. 메일 발송 : 생성된 엑셀파일을 첨부하고, 위험도가 "High"인 기사만 모아 클릭 가능한 HTML표로 보여주는 본문 작성 후 자동 발송
5. 보안 및 예외 처리: 이메일 계정 정보(ID,APP Password)는 .env파일로 로드, 네트워크 발송 오류는 try-except로 처리
"""

"""
문제 해결 가이드
1. 데이터 수집 엔진 설계(request, BeautifulSoup)
    1-1. Traget URL: 보안뉴스 사이트 대문페이지(https://boannews.com)대상 설정, header에 User-Agent를 추가
    1-2. Parsing 전략: 특정 class이름에 기대지 말고 soup.find_all("a")로 페이지의 모든 링크 탐색 후 조건 필터링
    1-3. 필터링 기준: 제목 15자 미만 제외(메뉴/배너), 중복 기사 제외, urljoin()생성링크에 대상 사이트 도메인 포함만 채택
    1-4. 위험도 판별: 제목 문자열에 위험 키워드가 포함되는지 검사해 각 기갓에 risk("High", "Noraml")값 할당

2. 엑셀 리포트 생성(openpyxl)
    2-1. 워크북 구성: Workbook()으로 생성 후 ws.append()로 헤더 및 기사 데이터 행 순차 추가.
    2-2. 서식 적용: PatternFill로 헤더 배경색 강조, 위험도 "High"행은 Font(color="FF0000", bold=True)적용
    2-3. 파일명 규칙: datatime.now().strftime()으로 당일 날짜가 포함된 파일명(ex: Secu_Repo_YYYYMMDD.xlxs)생성&저장

3. 이메일 발송 (smtplib, MIMEMultipart, 첨부파일)
    3-1. 본문 구성: 위험도 "High" 기사만 추출해 <table>과 <a>태그 기반의 HTML 문자열 구성 후 MIMEText(html, 'html')로 첨부
    3-2. 파일 첨부: 엑셀 파일을 'rb'모드로 열어 MIMEApplication으로 생성하고 Content-Disposition 헤더 추가
    3-3. 발송 처리: smtp.gmail.com(포트587)연결 -> stattls()암호화 -> .env 계정정보로 로그인 -> send_message() 발송

4. 통합 파이프라인 및 예외 처리
    4-1. main()함수에서 수집->엑셀저장->메일발송 순서로 파이프라인 연결
    4-2. 수집 결과 부재 및 네트워크/발송 오류 발생 시 비정상 종료 없이 try-except로 원인을 로깅
"""
import os
import re
from dotenv import load_dotenv

#def get_security_news_rows()
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#def create_excel_report(news_data)
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from datetime import datetime
from pathlib import Path

#def attach_upload_files
#def send_security_report
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
import pandas as pd

load_dotenv()

#5_class_infra/Ex06_bs4
###요구사항 1. 데이터 수집 : request, BeautifulSoup > 보안뉴스사이트에서 기사 제목,링크 최소 5개이상 수집
###요구사항 2. 위험도 분류 : 제목에 "취약점", "유출", "해킹"등의 키워드 포함 시 -> 위험도 "High", 그외 "Noraml"
def get_security_news_rows():
    """
    TARGET_URL(.env)에서 데이터 추출(request)\n
    BeautifulSoup로 파싱 후 처리된 데이터를 [리스트]로 반환
    \n
    dict : row {번호, 제목, 링크, 위험도}\n
    list : rows []\n
    return:
        rows
    """
    #가이드 1-1. Traget URL: 보안뉴스 사이트 대문페이지(https://boannews.com)대상 설정, header에 User-Agent를 추가
    #웹페이지 요청
    target_url = os.getenv("URL")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    } 

    try:
        response = requests.get(
            target_url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        print("✅ 연결 성공")
        print("상태 코드:", response.status_code)
    except Exception as e:
        print("❌ 웹사이트 연결 오류, ", e)
        return
    soup = BeautifulSoup(   response.text,  "html.parser"  )
    #가이드 1-2. Parsing 전략: 특정 class이름에 기대지 말고 soup.find_all("a")로 페이지의 모든 링크 탐색 후 조건 필터링
    links = soup.find_all("a")
    count = 0
    rows = []
    seen_titles = set()
    for a in links:
        if len(title := a.get_text()) < 15: continue    #가이드 1-3-1. 필터링 기준: 제목 15자 미만 제외(메뉴/배너)
        if title in seen_titles:            continue    #가이드 1-3-2. 중복 기사 제외
        if not (href := a.get('href')):     continue    # 링크가 없으면 제외
        # if "boannews" not in href:          continue    # 링크가 보안뉴스 외부 링크 제외 #요구사항에 보안뉴스 외부링크 제한 없음
        
        seen_titles.add(title)
        count += 1
        row = {}

        row["title"] = title
        #가이드 1-3-3. urljoin()생성링크에 대상 사이트 도메인 포함만 채택
        row["href"] = urljoin(target_url, href)
        #가이드 1-4. 위험도 판별 : 제목 문자열에 위험 키워드가 포함되는지 검사해 각 기갓에 risk("High", "Noraml")값 할당
        row["risk"] = "High" if re.compile("취약점|유출|해킹").search(title) else "Normal"
        # print(f'test: {row}') 
        rows.append(row)
        if count == 5: break
    if count == 0:
        print("❌ 뉴스 기사를 찾지 못했습니다.")
    return rows

###요구사항 3. 엑셀 저장 : 순번,제목,링크,위험도(headers) 컬럼으로 엑셀 파일 생성, 헤드행 배경색 강조, 위험도 "High"행 글자 빨간색,Bold체
def create_excel_report(news_data):
    """
    리스트형식(title, href, risk)데이터 받아온후 형식을 꾸민후\n
    return:
        savefilepath"""
    #가이드 2-1-1. 워크북 구성: Workbook()으로 생성
    wb = Workbook() # 새 엑셀 파일 생성
    ws = wb.active  # 현재 활성화된 워크시트 가져오기
    ws.title = "Security_Report"    #시트 탭 이름
    ###요구사항 3-1. 순번,제목,링크,위험도(headers) 컬럼
    headers = ["순번", "뉴스 제목", "링크", "위험도"]
    #가이드 2-1-2. ws.append()로 헤더 및 기사 데이터 행 순차 추가.
    ws.append(headers)

    #가이드 2-2. 서식 적용: PatternFill로 헤더 배경색 강조, 위험도 "High"행은 Font(color="FF0000", bold=True)적용
    ###요구사항 3-2. 헤드행 배경색 강조
    header_fill = PatternFill(start_color="333333", fill_type="solid")
    for cell in ws[1]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = header_fill

    
    # 데이터 추가
    for idx, news in enumerate(news_data, 1): #news_data 속성 title, href, risk
        row = [idx, news['title'], news['href'], news['risk']]
        ws.append(row)

        ###요구사항 3-3. 위험도 "High"행 글자 빨간색,Bold체
        if news['risk'] == "High":
            for cell in ws[ws.max_row]:
                cell.font = Font(color="FF0000", bold=True)

    BASE_DIR = Path(__file__).parent
    SAVE_FOLDER = BASE_DIR / "output"
    SAVE_FOLDER.mkdir(parents=True, exist_ok=True)
    #가이드 2-3. 파일명 규칙: datatime.now().strftime()으로 당일 날짜가 포함된 파일명(ex: Secu_Repo_YYYYMMDD.xlsx)생성&저장
    SOURCE_FILE = f"Security_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
    try:
        wb.save(SAVE_FOLDER/SOURCE_FILE)
    except Exception as e:
        print("파일 저장 실패, ", e)
        return -1
    return SAVE_FOLDER/SOURCE_FILE


###요구사항 4. 메일 발송 : 생성된 엑셀파일을 첨부하고, 위험도가 "High"인 기사만 모아 클릭 가능한 HTML표로 보여주는 본문 작성 후 자동 발송
def send_security_report(file_path):
    """
    file_path경로에 있는 파일을 첨부하여 메일 발송\n
    파일을 읽어서 조건으로 필터링 후 \<table\>형식으로 보여준다.
    """
    #.env로드
    to_email = os.getenv("RECEIVE_MAIL_USER")
    user_email = os.getenv("GOOGLE_EMAIL_USER")
    app_password = os.getenv("GOOGLE_EMAIL_PASS")
    smtp_server = os.getenv("GOOGLE_SMTP_SERVER")
    smtp_port = int(os.getenv("GOOGLE_SMTP_PORT"))  # 포트는 정수형으로 변환

    #가이드 3-1-1. 본문 구성: 위험도 "High" 기사만 추출해 <table>과 <a>태그 기반의 HTML 문자열 구성 후 
    msg = MIMEMultipart()
    msg['Subject'] = "[PBL ADV02] 실시간 보안 뉴스 리포트"
    msg['From'] = user_email
    msg['To'] = to_email

    #엑셀파일 읽어서 dict형태로 변환
    df = pd.read_excel(file_path)
    high = df[df["위험도"] == "High"].to_dict("records") #"record"가 있어야 python dict과 같은구조로 변환

    #html
    html_content = f"""
    <h3> [ 알림 ] 최신 보안 취약점 및 뉴스 목록</h3>
    <hr>
    <table>
        <thead>
            <tr>
                <th>순번</th>
                <th>뉴스 제목</th>
                <th>위험도</th>
            </tr>
        </thead>
        <tbody>
            {''.join(
                [f'<tr><td>{news["순번"]}</td><td><a href={news["링크"]}>{news["뉴스 제목"]}</a></td><td>{news["위험도"]}</td></tr>' 
                for news in high]
                )}
        </tbody>
    </table>
    <p style="color:gray;">본 메일은 인프라 관리 시스템에 의해 자동 발송되었습니다.</p>
    """

    #가이드 3-1-2. MIMEText(html, 'html')로 첨부
    msg.attach(MIMEText(html_content, 'html'))
    #가이드 3-2. 파일 첨부: 엑셀 파일을 'rb'모드로 열어 MIMEApplication으로 생성하고 Content-Disposition 헤더 추가
    file_path = Path(file_path)  # 문자열 경로를 Path 객체로 변환
    with file_path.open("rb") as file:
        attachment = MIMEApplication(file.read())
        attachment.add_header(
            "Content-Disposition", "attachment", filename=file_path.name
        )
    msg.attach(attachment)

    #서버 접속 및 발송
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 메일 서버와의 통신을 암호화합니다 (통신 구간 암호화)
            server.login(user_email, app_password)
            server.send_message(msg)
            print(f"[{user_email}] 메일 발송 성공!")
    except Exception as e:
        print(f"오류 발생: {e}")

###요구사항 5. 보안 및 예외 처리: 이메일 계정 정보(ID,APP Password)는 .env파일로 로드, 네트워크 발송 오류는 try-except로 처리
#가이드4. 통합 파이프라인 및 예외 처리
    # 4-1. main()함수에서 수집->엑셀저장->메일발송 순서로 파이프라인 연결
    # 4-2. 수집 결과 부재 및 네트워크/발송 오류 발생 시 비정상 종료 없이 try-except로 원인을 로깅
def main():
    try:
        rows = get_security_news_rows() #수집
    except Exception as e:
        print("뉴스 데이터 수집 실패, ", e)
    try:
        file_path = create_excel_report(rows) #엑셀 저장
    except Exception as e:
        print("엑셀 저장 실패, ", e)
    try:
        send_security_report(file_path) #메일 발송
    except Exception as e:
        print("네트워크 발송 오류, ", e)

if __name__ == "__main__":
    main()