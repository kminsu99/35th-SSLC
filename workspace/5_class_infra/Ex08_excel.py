from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from pathlib import Path

def create_excel_report(news_data):
    wb = Workbook() # 새 엑셀 파일 생성
    ws = wb.active  # 현재 활성화된 워크시트 가져오기
    ws.title = "Security_Report" 
    # 1. 헤더 설정 및 스타일 적용
    headers = ["순번", "뉴스 제목", "위험도"]
    ws.append(headers)

    # 첫 행(헤더) 강조
    header_fill = PatternFill(start_color="333333", fill_type="solid")
    for cell in ws[1]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = header_fill

    # 2. 데이터 추가
    for i, title in enumerate(news_data, 1):
        risk = "High" if "취약점" in title or "유출" in title else "Normal"
        row = [i, title, risk]
        ws.append(row)

        # 위험도가 High인 행은 빨간색 글자 처리
        if risk == "High":
            ws.cell(row=ws.max_row, column=3).font = Font(color="FF0000", bold=True)

    # wb.save("output/Daily_Security_Report.xlsx")
    # output/ 경로가 없을경우 자동으로 생성, 에러없이 실행되도록
    BASE_DIR = Path(__file__).parent
    SAVE_FOLDER = BASE_DIR / "output"
    SAVE_FOLDER.mkdir(parents=True, exist_ok=True)
    SOURCE_FILE = "Daily_Security_Report.xlsx"
    wb.save(SAVE_FOLDER/SOURCE_FILE)
    
    # 기존에 output 디렉토리가 있으면 실행, 없으면 에러 발생

if __name__ == "__main__":
    test_news = ["Windows 커널 취약점 발견", "신규 보안 패치 안내", "개인정보 유출 사고"]
    create_excel_report(test_news)